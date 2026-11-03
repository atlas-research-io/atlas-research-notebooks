import os, subprocess, tempfile, urllib.request
from PIL import Image, ImageDraw, ImageFont

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

