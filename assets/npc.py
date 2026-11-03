from PIL import Image

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


def render(name, scale=1):
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
