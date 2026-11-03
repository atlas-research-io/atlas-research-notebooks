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


    def flag(self, name, x, y, scale=1, pole=False):
        f = _npc["flag"](name, scale, pole)
        self.im.paste(f, (x, y), f)

    def axes(self, box, ylabels=(), xlabels=(), color="panel_dark"):
        x0, y0, x1, y1 = box
        c = P[color]
        self.d.line([x0, y0, x0, y1], fill=c)
        self.d.line([x0, y1, x1, y1], fill=c)
        for k, lab in enumerate(ylabels):
            yy = y1 - int(round((y1 - y0) * k / max(1, len(ylabels) - 1)))
            self.d.line([x0 - 2, yy, x0, yy], fill=c)
            self.text(x0 - 4 - 6 * len(lab), yy - 3, lab, shadow=False)
        for k, lab in enumerate(xlabels):
            xx = x0 + int(round((x1 - x0) * k / max(1, len(xlabels) - 1)))
            self.d.line([xx, y1, xx, y1 + 2], fill=c)
            self.text(xx - 3 * len(lab), y1 + 4, lab, shadow=False)

    def line(self, values, box, color="teal", lo=None, hi=None, progress=1.0, thick=2):
        x0, y0, x1, y1 = box
        if not values:
            return
        lo = min(values) if lo is None else lo
        hi = max(values) if hi is None else hi
        span = (hi - lo) or 1.0
        n = max(2, int(round(len(values) * progress)))
        pts = []
        for k, v in enumerate(values[:n]):
            xx = x0 + int(round((x1 - x0) * k / max(1, len(values) - 1)))
            yy = y1 - int(round((y1 - y0) * (v - lo) / span))
            pts.append((xx, yy))
        c = P[color] if isinstance(color, str) else color
        for t in range(thick):
            self.d.line([(x, y - t) for x, y in pts], fill=c, width=1)
        return pts

    def bars(self, values, box, colors=None, lo=0, hi=None, progress=1.0, gap=2):
        x0, y0, x1, y1 = box
        if not values:
            return
        hi = max(values) if hi is None else hi
        span = (hi - lo) or 1.0
        bw = max(2, (x1 - x0 - gap * (len(values) - 1)) // len(values))
        for k, v in enumerate(values):
            frac = max(0.0, min(1.0, (v - lo) / span)) * progress
            h = int(round((y1 - y0) * frac))
            xx = x0 + k * (bw + gap)
            c = colors[k] if colors else "teal"
            c = P[c] if isinstance(c, str) else c
            if h > 0:
                self.d.rectangle([xx, y1 - h, xx + bw - 1, y1], fill=c)
                self.d.rectangle([xx, y1 - h, xx + bw - 1, y1 - h], fill=P.get("teal_l") if c == P["teal"] else c)
                self.d.rectangle([xx, y1 - h, xx + bw - 1, y1], outline=P["out"])

    def big(self, x, y, s, color="text", scale=2):
        tmp = Scene.__new__(Scene)
        tmp.im = Image.new("RGB", (LW, 16), P["panel"])
        tmp.d = ImageDraw.Draw(tmp.im)
        tmp.font = self.font
        mask = Image.new("L", (LW, 16), 0)
        tmp.im = Image.new("RGB", (LW, 16), (0, 0, 0))
        tmp.d = ImageDraw.Draw(tmp.im)
        w = tmp.glyph(0, 0, s, (255, 255, 255))
        m = tmp.im.convert("L").point(lambda v: 255 if v > 90 else 0).crop((0, 0, max(1, w), 16))
        m = m.resize((m.width * scale, m.height * scale), Image.NEAREST)
        c = P[color] if isinstance(color, str) else color
        self.im.paste(Image.new("RGB", m.size, P["shadow"]), (x + scale, y + scale), m)
        self.im.paste(Image.new("RGB", m.size, c), (x, y), m)
        return x + m.width

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




_npc = {}
exec(open(fetch("assets/npc.py")).read(), _npc)
NPCS = _npc["NPCS"]
FLAGS = _npc["FLAGS"]

def npc_render(name, scale=1):
    return _npc["render"](name, scale)

def flag_render(name, scale=1, pole=False):
    return _npc["flag"](name, scale, pole)
