import marimo

__generated_with = "0.14.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import os
    import json
    import subprocess
    import tempfile
    import urllib.request
    import numpy as np
    import pandas as pd
    from PIL import Image, ImageDraw, ImageFont
    return Image, ImageDraw, ImageFont, json, mo, np, os, pd, subprocess, tempfile, urllib


@app.cell(hide_code=True)
def _(mo):
    mo.md("# Israel voted. Nobody won.")
    return


@app.cell(hide_code=True)
def _(Image, ImageDraw, ImageFont, os, subprocess, tempfile, urllib):
    LW, LH, SCALE = 320, 180, 4
    ASSET_DIR = os.path.join(tempfile.gettempdir(), "atlas-pixel-assets")
    os.makedirs(ASSET_DIR, exist_ok=True)
    RAW = "https://raw.githubusercontent.com/atlas-research-io/atlas-research-notebooks/main"

    def fetch(rel):
        path = os.path.join(ASSET_DIR, rel.replace("/", "_"))
        if not os.path.exists(path):
            req = urllib.request.Request(f"{RAW}/{rel}", headers={"User-Agent": "atlas-research"})
            with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as f:
                f.write(r.read())
        return path

    FONT_PATH = fetch("fonts/PokemonClassic.ttf")

    def backdrop(name):
        return Image.open(fetch(f"assets/backdrops/{name}.png")).convert("RGB")

    DOLLAR = [
        "..#..",
        ".####",
        "#.#..",
        ".###.",
        "..#.#",
        "####.",
        "..#..",
    ]

    P = {
        "text": (64, 64, 72),
        "shadow": (200, 200, 208),
        "panel": (248, 248, 248),
        "panel_line": (104, 128, 152),
        "panel_dark": (40, 48, 64),
        "hp_bg": (72, 72, 80),
        "hp_tag": (248, 200, 72),
        "hp_tag_text": (104, 72, 16),
        "green": (88, 208, 128),
        "green_l": (152, 240, 184),
        "yellow": (248, 208, 56),
        "red": (232, 72, 72),
        "pink": (212, 96, 122),
        "pink_l": (240, 160, 180),
        "teal": (56, 150, 146),
        "teal_l": (140, 210, 205),
        "out": (24, 24, 32),
        "platform": (120, 184, 96),
        "platform_rim": (72, 136, 64),
    }


    class Scene:
        def __init__(self, backdrop=None):
            self.im = Image.new("RGB", (LW, LH), (136, 216, 152))
            if backdrop is not None:
                self.im.paste(backdrop, (0, 0))
            self.d = ImageDraw.Draw(self.im)
            self.font = ImageFont.truetype(FONT_PATH, 8)

        def platform(self, cx, cy, rx, ry):
            self.d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=P["platform_rim"])
            self.d.ellipse([cx - rx + 2, cy - ry + 1, cx + rx - 2, cy + ry - 2], fill=P["platform"])

        def sprite(self, rgba, x, y):
            self.im.paste(rgba, (x, y), rgba)

        def panel(self, x0, y0, x1, y1):
            self.d.rectangle([x0 + 2, y0, x1 - 2, y1], fill=P["panel"])
            self.d.rectangle([x0, y0 + 2, x1, y1 - 2], fill=P["panel"])
            self.d.line([x0 + 2, y0, x1 - 2, y0], fill=P["panel_dark"])
            self.d.line([x0 + 2, y1, x1 - 2, y1], fill=P["panel_dark"])
            self.d.line([x0, y0 + 2, x0, y1 - 2], fill=P["panel_dark"])
            self.d.line([x1, y0 + 2, x1, y1 - 2], fill=P["panel_dark"])
            for (x, y) in ((x0 + 1, y0 + 1), (x1 - 1, y0 + 1), (x0 + 1, y1 - 1), (x1 - 1, y1 - 1)):
                self.d.point((x, y), fill=P["panel_dark"])
            self.d.rectangle([x0 + 2, y0 + 2, x1 - 2, y1 - 2], outline=P["panel_line"])

        def textbox(self):
            x0, y0, x1, y1 = 4, LH - 44, LW - 5, LH - 4
            self.d.rectangle([x0, y0, x1, y1], fill=P["panel_line"])
            self.d.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], fill=P["panel"])
            self.d.rectangle([x0 + 2, y0 + 2, x1 - 2, y1 - 2], outline=P["panel_line"])
            self.d.rectangle([x0 + 3, y0 + 3, x1 - 3, y1 - 3], outline=P["panel"])
            for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
                self.d.point((x, y), fill=self.im.getpixel((x, y)) if False else P["panel_line"])

        def glyph(self, x, y, s, color):
            cx = x
            for ch in s:
                if ch == "$":
                    for j, row in enumerate(DOLLAR):
                        for i, c in enumerate(row):
                            if c == "#":
                                self.d.point((cx + i, y + 2 + j), fill=color)
                    cx += 6
                    continue
                mask = Image.new("L", (16, 16), 0)
                ImageDraw.Draw(mask).text((0, 0), ch, fill=255, font=self.font)
                mask = mask.point(lambda v: 255 if v > 90 else 0)
                self.im.paste(Image.new("RGB", (16, 16), color), (cx, y), mask)
                cx += int(round(self.font.getlength(ch)))
            return cx

        def text(self, x, y, s, color="text", shadow=True):
            if shadow:
                self.glyph(x + 1, y + 1, s, P["shadow"])
            return self.glyph(x, y, s, P[color] if isinstance(color, str) else color)

        def hp(self, x, y, frac, width=48, color=None):
            self.d.rectangle([x, y, x + 11, y + 6], fill=P["hp_tag"], outline=P["panel_dark"])
            H = ["#.#", "###", "#.#"]
            Pg = ["##.", "#.#", "##.", "#..", "#.."]
            for j, row in enumerate(["#.#.##.", "#.#.#.#", "###.##.", "#.#.#..", "#.#.#.."]):
                for i, c in enumerate(row):
                    if c == "#":
                        self.d.point((x + 3 + i, y + 1 + j), fill=P["hp_tag_text"])
            bx = x + 12
            self.d.rectangle([bx, y + 1, bx + width + 1, y + 5], fill=P["hp_bg"], outline=P["panel_dark"])
            f = max(0.0, min(1.0, frac))
            fw = int(round(width * f))
            if color is None:
                color = "green" if f > 0.5 else ("yellow" if f > 0.2 else "red")
            if fw > 0:
                self.d.rectangle([bx + 1, y + 2, bx + fw, y + 4], fill=P[color])
                light = P.get(color + "_l", P["green_l"])
                self.d.rectangle([bx + 1, y + 2, bx + fw, y + 2], fill=light)

        def status(self, x, y, name, pct, color, right=False):
            w = 124
            self.panel(x, y, x + w, y + 26)
            self.text(x + 8, y + 4, name)
            self.text(x + w - 8 - 6 * len(f"{pct*100:.0f}%") + 2, y + 4, f"{pct*100:.0f}%", color=color)
            self.hp(x + 8, y + 16, pct, width=w - 36, color=color)

        def frame(self):
            return self.im.resize((LW * SCALE, LH * SCALE), Image.NEAREST)


    def dialogue(sc, lines, progress=1.0):
        sc.textbox()
        total = sum(len(l) for l in lines)
        shown = int(total * progress)
        y = LH - 36
        for l in lines:
            take = max(0, min(len(l), shown))
            sc.text(13, y, l[:take])
            shown -= len(l)
            y += 14
        if progress >= 1:
            x, yy = LW - 18, LH - 13
            sc.d.polygon([(x, yy), (x + 6, yy), (x + 3, yy + 3)], fill=P["panel_dark"])



    def dialogue(sc, lines, progress=1.0):
        sc.textbox()
        total = sum(len(l) for l in lines)
        shown = int(total * progress)
        y = LH - 36
        for l in lines:
            take = max(0, min(len(l), shown))
            sc.text(13, y, l[:take])
            shown -= len(l)
            y += 14
        if progress >= 1:
            x, yy = LW - 18, LH - 13
            sc.d.polygon([(x, yy), (x + 6, yy), (x + 3, yy + 3)], fill=P["panel_dark"])

    def write_mp4(frames, path, fps=24, hold=2):
        tmp = tempfile.mkdtemp()
        k = 0
        for fr in frames:
            for _ in range(hold):
                fr.save(os.path.join(tmp, f"{k:05d}.png"))
                k += 1
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(tmp, "%05d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "faststart", path], check=True)
        return path

    BASE = [
        "....kkkkkkkk....",
        "...khhhhhhhhk...",
        "..khhhhhhhhhhk..",
        "..khhhhhhhhhhk..",
        "..khHhhhhhhhHk..",
        "..kHssssssssHk..",
        "..kssssssssssk..",
        "..kssesssssessk.",
        "..kssesssssessk.",
        "..kssssssssssSk.",
        "...kSssssssssk..",
        "....kSSSSSSSk...",
        ".....kkssskk....",
        "....kccwtwcck...",
        "...kcccwtwcccck.",
        "..ksccccctcccsk.",
        "..kkccccccccckk.",
        "...kCCCCCCCCCk..",
        "....kpppkpppk...",
        "....kPPPkPPPk...",
        "....kffkkkffk...",
    ]

    DEFAULT = {
        "k": (40, 40, 56),
        "h": (120, 120, 128), "H": (88, 88, 96),
        "s": (240, 208, 176), "S": (208, 160, 128),
        "e": (40, 40, 56),
        "c": (48, 56, 104), "C": (32, 40, 80),
        "t": (200, 40, 40), "w": (248, 248, 248),
        "p": (48, 56, 104), "P": (32, 40, 80),
        "f": (40, 32, 32),
        "b": (232, 232, 232), "B": (192, 192, 200),
        "m": (176, 96, 96),
    }

    NPCS = {
        "trump": {
            "pal": {"h": (248, 216, 96), "H": (216, 176, 56), "s": (240, 168, 104), "S": (208, 128, 72), "c": (40, 48, 96), "C": (24, 32, 72), "p": (40, 48, 96), "P": (24, 32, 72), "t": (216, 40, 40)},
            "rows": {1: "...khhhhhhhhhk..", 4: "..khhhhhhhhhHhk.", 5: "..kHhhhhhhhhhHk.", 6: "..kHssssssssHk..", 10: "...kSssmmmsssk.."},
        },
        "netanyahu": {
            "pal": {"h": (176, 176, 176), "H": (128, 128, 136), "s": (240, 208, 176), "S": (208, 160, 128), "c": (56, 56, 72), "C": (40, 40, 56), "p": (56, 56, 72), "P": (40, 40, 56), "t": (120, 168, 224)},
            "rows": {0: "....kkkkkkkk....", 1: "...kssssssssk...", 2: "..kssssssssssk..", 3: "..kssssssssssk..", 4: "..khsssssssshk..", 5: "..khhssssssshhk.", 6: "..khsssssssshk..", 7: "..khsesssssehk..", 8: "..khsesssssehk..", 9: "..kssssSSsssSk..", 10: "...kSsskkkssSk..", 11: "....kSSSSSSSk..."},
        },
        "eisenkot": {
            "pal": {"h": (160, 160, 160), "H": (120, 120, 128), "s": (236, 200, 168), "S": (200, 152, 120), "c": (64, 88, 64), "C": (40, 64, 40), "p": (56, 56, 64), "P": (40, 40, 48), "t": (248, 248, 248)},
            "rows": {1: "...khhhhhhhhk...", 2: "..khhhhhhhhhhk..", 3: "..kHssssssssHk..", 4: "..kssssssssssk..", 13: "....kccwwwcck..."},
        },
        "xi": {
            "pal": {"h": (32, 28, 32), "H": (16, 16, 24), "s": (240, 200, 160), "S": (208, 160, 120), "c": (40, 44, 64), "C": (24, 28, 44), "p": (40, 44, 64), "P": (24, 28, 44), "t": (200, 40, 40)},
            "rows": {5: "..khhhhhhhhhhk..", 6: "..kHssssssssHk.."},
        },
        "putin": {
            "pal": {"h": (224, 208, 176), "H": (184, 168, 136), "s": (248, 216, 192), "S": (216, 176, 152), "c": (40, 48, 96), "C": (24, 32, 72), "p": (40, 48, 96), "P": (24, 32, 72), "t": (200, 40, 40)},
            "rows": {3: "..kHssssssssHk..", 4: "..kHssssssssHk..", 5: "..kssssssssssk.."},
        },
        "khamenei": {
            "pal": {"h": (32, 32, 40), "H": (16, 16, 24), "s": (232, 200, 168), "S": (200, 160, 128), "c": (40, 40, 48), "C": (24, 24, 32), "p": (40, 40, 48), "P": (24, 24, 32)},
            "rows": {0: "...kkkkkkkkkk...", 1: "..khhhhhhhhhhk..", 2: ".khhhhhhhhhhhhk.", 3: ".khhhhhhhhhhhhk.", 4: "..khhhhhhhhhhk..", 10: "...kbbbbbbbbbk..", 11: "....kbbbbbbbk...", 12: ".....kkbbbkk....", 13: "....kccccccck...", 14: "...kccccccccck..", 15: "..kscccccccccsk.", 18: "....kccccccck...", 19: "....kCCCCCCCk..."},
        },
        "zelensky": {
            "pal": {"h": (72, 48, 40), "H": (48, 32, 24), "s": (232, 192, 160), "S": (200, 152, 120), "c": (96, 112, 72), "C": (64, 80, 48), "p": (56, 56, 64), "P": (40, 40, 48), "b": (72, 48, 40), "B": (48, 32, 24)},
            "rows": {10: "...kbbssssbbk...", 11: "....kbbbbbbbk...", 13: "....kccccccck...", 14: "...kccccccccck.."},
        },
        "modi": {
            "pal": {"h": (232, 232, 232), "H": (192, 192, 200), "s": (200, 152, 112), "S": (168, 120, 88), "c": (232, 144, 56), "C": (192, 104, 32), "p": (248, 248, 240), "P": (208, 208, 200)},
            "rows": {10: "...kbbssssbbk...", 11: "....kbbbbbbbk...", 13: "....kcwwwwwck...", 14: "...kccwwwwwcck..", 15: "..kscwwwwwwwcsk.", 16: "..kkccwwwwwcckk."},
        },
        "starmer": {
            "pal": {"h": (168, 168, 176), "H": (128, 128, 136), "s": (240, 208, 184), "S": (208, 168, 144), "c": (40, 48, 96), "C": (24, 32, 72), "p": (40, 48, 96), "P": (24, 32, 72), "t": (160, 40, 56)},
            "rows": {7: "..kskeekskeeksk.", 8: "..kssesssssessk."},
        },
        "trader": {
            "pal": {"h": (56, 150, 146), "H": (38, 92, 90), "s": (236, 196, 160), "S": (200, 152, 120), "c": (56, 150, 146), "C": (38, 92, 90), "p": (56, 56, 64), "P": (40, 40, 48), "t": (56, 150, 146), "w": (56, 150, 146)},
            "rows": {5: "..khhssssssshhk.", 6: "..khsssssssshk..", 7: "..khsesssssehk..", 8: "..khsesssssehk..", 9: "..khsssssssshk..", 13: "....kccccccck...", 14: "...kccccccccck.."},
        },
        "politician": {"pal": {}, "rows": {}},
    }



    def npc_render(name, scale=1):
        spec = NPCS[name]
        pal = {**DEFAULT, **spec["pal"]}
        rows = [spec["rows"].get(i, r) for i, r in enumerate(BASE)]
        im = Image.new("RGBA", (16 * scale, len(rows) * scale), (0, 0, 0, 0))
        px = im.load()
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch == ".":
                    continue
                col = pal[ch] + (255,)
                for dy in range(scale):
                    for dx in range(scale):
                        px[i * scale + dx, j * scale + dy] = col
        return im

    return DOLLAR, LH, LW, P, Scene, backdrop, dialogue, npc_render, write_mp4


@app.cell(hide_code=True)
def _(LH, LW, P, Scene, backdrop, dialogue, npc_render, write_mp4, json, pd, tempfile, urllib):

    NET = "20006732765674855733524007935991362439352594042415161039767275461950712817548"
    EIS = "52487256270918227930942830546248720603566203568229607048093730748840489555808"
    IL = "Asia/Jerusalem"

    def hist(tok, interval, fidelity):
        req = urllib.request.Request(f"https://clob.polymarket.com/prices-history?market={tok}&interval={interval}&fidelity={fidelity}", headers={"User-Agent": "Mozilla/5.0"})
        h = json.loads(urllib.request.urlopen(req).read())["history"]
        s = pd.Series([p["p"] for p in h], index=pd.to_datetime([p["t"] for p in h], unit="s", utc=True)).sort_index()
        return s[~s.index.duplicated()]

    year = pd.DataFrame({"net": hist(NET, "max", 1440), "eis": hist(EIS, "max", 1440)}).ffill().dropna()
    year = year[year.index <= pd.Timestamp("2026-10-28", tz="UTC")]
    night = pd.DataFrame({"net": hist(NET, "1w", 60), "eis": hist(EIS, "1w", 60)}).ffill().dropna()
    night = night[(night.index >= pd.Timestamp("2026-10-27 14:00", tz="UTC")) & (night.index <= pd.Timestamp("2026-10-28 08:00", tz="UTC"))]
    night.index = night.index.tz_convert(IL)

    BG_TOWN = backdrop("bg-knesset2")
    BG_FIELD = backdrop("battle-field")
    BG_EXCH = backdrop("bg-exchange")
    BG_LAWN = backdrop("bg-lawn")
    SP = {n: npc_render(n) for n in ("trader", "netanyahu", "eisenkot", "trump")}
    SP3 = {n: npc_render(n, 3) for n in ("netanyahu", "eisenkot")}

    YEAR_EVENTS = [
        (pd.Timestamp("2026-02-28", tz="UTC"), ["NETANYAHU used STRIKE IRAN!", "Hormuz closes. Odds jump to 62%."]),
        (pd.Timestamp("2026-06-17", tz="UTC"), ["The war drags on. Hormuz stays shut.", "NETANYAHU's odds are falling..."]),
        (pd.Timestamp("2026-07-27", tz="UTC"), ["EISENKOT overtakes!", "First time ahead in the market."]),
        (pd.Timestamp("2026-10-25", tz="UTC"), ["Two days out:", "NETANYAHU 27%. EISENKOT 50%."]),
    ]
    NIGHT_EVENTS = [
        (pd.Timestamp("2026-10-27 22:00", tz=IL), ["Polls close. Exit polls say: TIE.", "Opposition declares victory on air."]),
        (pd.Timestamp("2026-10-28 01:00", tz=IL), ["Half the vote is counted.", "NETANYAHU's bloc is at 55."]),
        (pd.Timestamp("2026-10-28 05:00", tz=IL), ["NETANYAHU used COUNT THE VOTES!", "It's super effective."]),
    ]
    BLOCS = [("NETANYAHU BLOC", 53, "pink", "Likud, UTJ, Otzma, Shas, RZP"), ("OPPOSITION", 48, "teal", "Yashar, Together, Democrats, more"), ("ARAB PARTIES", 19, "yellow", "Joint List, Ra'am. A record.")]
    COST = [("ISRAEL ETF", "-4.9%", 0.49), ("TEL AVIV 35", "-2.3%", 0.23), ("SHEKEL vs USD", "-2.2%", 0.22), ("10-YEAR YIELD", "+8 bp", 0.3), ("BRENT CRUDE", "+1.3%", 0.13)]
    NEXT = [
        ["Results reach HERZOG on 4 Nov.", "One leader gets 28 days to form a coalition."],
        ["US midterms on 3 Nov.", "TRUMP: re-elect NETANYAHU to finish the job."],
        ["NETANYAHU: a rare chance, with TRUMP,", "to remove the Iran threat once and for all."],
        ["US officials told Gulf allies:", "strikes possible as early as 4 Nov."],
        ["Hormuz: closed 245 days. Brent $113.", "Round two puts it all back on the board."],
    ]

    def clock(sc, t, kicker=None):
        sc.panel(228, 8, 312, 26)
        sc.text(236, 13, t, shadow=False)
        if kicker:
            sc.text(140, 13, kicker, color="teal")

    def battle(net, eis, lines, prog, t, kicker):
        sc = Scene(BG_FIELD)
        sc.platform(248, 84, 46, 9)
        sc.platform(80, 138, 50, 9)
        e = SP3["netanyahu"]; sc.sprite(e, 248 - e.width // 2, 84 - e.height + 8)
        p = SP3["eisenkot"]; sc.sprite(p, 80 - p.width // 2, 138 - p.height + 8)
        sc.status(8, 10, "NETANYAHU", net, "pink")
        sc.status(190, 104, "EISENKOT", eis, "teal")
        clock(sc, t, kicker)
        dialogue(sc, lines, prog)
        return sc.frame()

    frames = []
    prev = year.index[0]
    for ts, lines in YEAR_EVENTS:
        seg = year[(year.index > prev) & (year.index <= ts)].iloc[::8]
        for idx, row in seg.iterrows():
            frames.append(battle(row["net"], row["eis"], ["", ""], 0, idx.strftime("%b %Y"), "ONE YEAR"))
        last = year[year.index <= ts].iloc[-1]
        for k in range(1, 25):
            frames.append(battle(last["net"], last["eis"], lines, k / 24, ts.strftime("%b %Y"), "ONE YEAR"))
        for k in range(10):
            frames.append(battle(last["net"], last["eis"], lines, 1.0, ts.strftime("%b %Y"), "ONE YEAR"))
        prev = ts

    def town(net, eis, lines, prog, t):
        sc = Scene(BG_TOWN)
        sc.sprite(SP["netanyahu"], 150, 92)
        sc.sprite(SP["eisenkot"], 176, 96)
        sc.status(8, 8, "NETANYAHU", net, "pink")
        sc.status(8, 40, "EISENKOT", eis, "teal")
        clock(sc, t, "ELECTION NIGHT")
        dialogue(sc, lines, prog)
        return sc.frame()

    prev = night.index[0]
    idx_poster = 0
    for ts, lines in NIGHT_EVENTS:
        seg = night[(night.index > prev) & (night.index <= ts)]
        fn = town if ts.hour != 5 else battle
        for idx, row in seg.iterrows():
            for _ in range(2):
                frames.append(fn(row["net"], row["eis"], ["", ""], 0, idx.strftime("%a %H:%M")) if fn is town else fn(row["net"], row["eis"], ["", ""], 0, idx.strftime("%a %H:%M"), "ELECTION NIGHT"))
        last = night[night.index <= ts].iloc[-1]
        for k in range(1, 25):
            frames.append(fn(last["net"], last["eis"], lines, k / 24, ts.strftime("%a %H:%M")) if fn is town else fn(last["net"], last["eis"], lines, k / 24, ts.strftime("%a %H:%M"), "ELECTION NIGHT"))
        for k in range(10):
            frames.append(fn(last["net"], last["eis"], lines, 1.0, ts.strftime("%a %H:%M")) if fn is town else fn(last["net"], last["eis"], lines, 1.0, ts.strftime("%a %H:%M"), "ELECTION NIGHT"))
        if ts.hour == 22:
            idx_poster = len(frames) - 1
        prev = ts

    def count(n_rows, prog, done):
        sc = Scene(BG_TOWN)
        sc.panel(8, 6, 312, 130)
        sc.text(16, 11, "THE COUNT", color="teal"); sc.text(136, 11, "120 seats. 61 to govern.", color=(120, 120, 128), shadow=False)
        for i, (name, seats, col, who) in enumerate(BLOCS[:n_rows]):
            y = 30 + i * 32
            t = prog if i == n_rows - 1 else 1
            sc.text(16, y - 4, name)
            sc.text(16, y + 9, who, color=(120, 120, 128), shadow=False)
            sc.hp(150, y + 2, seats / 120 * t, width=110, color=col)
            sc.text(276, y - 2, f"{int(round(seats * t))}", color=col)
        mx = 162 + int(110 * 61 / 120)
        for yy in range(24, 126, 3):
            sc.d.point((mx, yy), fill=P["panel_dark"])
        sc.text(mx + 3, 112, "61")
        dialogue(sc, ["Likud lost five seats and still won.", "Nobody reaches 61."], 1.0 if done else 0)
        return sc.frame()

    for i in range(1, len(BLOCS) + 1):
        for k in range(1, 13):
            frames.append(count(i, k / 12, False))
    for k in range(36):
        frames.append(count(len(BLOCS), 1, True))
    idx_count = len(frames) - 1

    def cost(n_hits, flash):
        sc = Scene(BG_EXCH)
        sc.sprite(SP["trader"], 150, 110)
        if flash:
            sc.d.rectangle([0, 0, LW, LH], fill=(255, 255, 255))
        sc.panel(8, 8, 224, 96)
        sc.text(16, 13, "WHAT IT COST BY LUNCH", color="teal")
        for i, (name, dmg, frac) in enumerate(COST[:n_hits]):
            y = 28 + i * 13
            sc.text(16, y - 2, name)
            sc.hp(126, y + 1, 1 - frac, width=30, color="pink")
            sc.text(178, y - 2, dmg, color="pink" if dmg.startswith("-") else (184, 120, 24))
        clock(sc, "Wed 28 Oct")
        dialogue(sc, ["TEL AVIV took the hit before a single", "coalition meeting."], 1.0 if n_hits >= len(COST) else 0)
        return sc.frame()

    for i in range(1, len(COST) + 1):
        frames.append(cost(i, True))
        for k in range(9):
            frames.append(cost(i, False))
    for k in range(20):
        frames.append(cost(len(COST), False))
    idx_cost = len(frames) - 1

    def nxt(step, prog):
        sc = Scene(BG_LAWN)
        sc.sprite(SP["trump"], 148, 118)
        sc.sprite(SP["netanyahu"], 172, 120)
        sc.panel(8, 8, 226, 26)
        sc.text(16, 13, f"WHAT HAPPENS NEXT  {step + 1} of 5", color="teal")
        dialogue(sc, NEXT[step], prog)
        return sc.frame()

    for st in range(len(NEXT)):
        for k in range(1, 25):
            frames.append(nxt(st, k / 24))
        for k in range(12):
            frames.append(nxt(st, 1.0))


    out_path = write_mp4(frames, tempfile.mktemp(suffix=".mp4"))
    return frames, out_path


@app.cell(hide_code=True)
def _(mo, out_path):
    with open(out_path, "rb") as _fh:
        mp4 = _fh.read()
    mo.vstack([
        mo.video(mp4, controls=True, autoplay=True, loop=True, muted=True),
        mo.download(data=mp4, filename="israel-voted-nobody-won.mp4", mimetype="video/mp4", label="Download animation"),
    ])
    return


if __name__ == "__main__":
    app.run()
