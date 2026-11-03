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
    "paxton": {
        "pal": {"h": (56, 40, 32), "H": (32, 24, 16), "s": (240, 200, 168), "S": (208, 160, 128), "c": (40, 48, 96), "C": (24, 32, 72), "p": (40, 48, 96), "P": (24, 32, 72), "t": (200, 40, 40)},
        "rows": {4: "..khhhhhhhhhhk..", 5: "..kHssssssssHk..", 7: "..kskeekskeeksk.", 8: "..kssesssssessk."},
    },
    "talarico": {
        "pal": {"h": (72, 48, 36), "H": (48, 32, 24), "s": (240, 204, 172), "S": (208, 160, 128), "c": (40, 48, 96), "C": (24, 32, 72), "p": (40, 48, 96), "P": (24, 32, 72), "t": (88, 140, 220)},
        "rows": {5: "..kHhhhhhhhhHk..", 6: "..kssssssssssk.."},
    },
    "lula": {
        "pal": {"h": (200, 200, 208), "H": (152, 152, 160), "s": (216, 168, 128), "S": (184, 136, 96), "c": (40, 48, 96), "C": (24, 32, 72), "p": (40, 48, 96), "P": (24, 32, 72), "t": (200, 40, 40), "b": (200, 200, 208)},
        "rows": {10: "...kbbssssbbk...", 11: "....kbbbbbbbk..."},
    },
    "milei": {
        "pal": {"h": (40, 32, 32), "H": (24, 16, 16), "s": (240, 204, 172), "S": (208, 160, 128), "c": (32, 32, 40), "C": (16, 16, 24), "p": (32, 32, 40), "P": (16, 16, 24), "t": (248, 248, 248), "b": (40, 32, 32)},
        "rows": {0: "...kkkkkkkkkk...", 1: "..khhhhhhhhhhk..", 2: ".khhhhhhhhhhhhk.", 3: ".khhhhhhhhhhhhk.", 4: ".khhHhhhhhhHhhk.", 5: ".khHssssssssHhk.", 6: ".khssssssssssHk.", 9: "..kbsssssssssbk.", 10: "...kbbssssbbbk..", 11: "....kbbbbbbbk..."},
    },
    "erdogan": {
        "pal": {"h": (176, 176, 184), "H": (128, 128, 136), "s": (232, 196, 160), "S": (200, 152, 120), "c": (40, 40, 56), "C": (24, 24, 40), "p": (40, 40, 56), "P": (24, 24, 40), "t": (200, 40, 40), "b": (176, 176, 184)},
        "rows": {4: "..khhhhhhhhhhk..", 5: "..kHssssssssHk..", 10: "...kSsbbbbbssk.."},
    },
    "mbs": {
        "pal": {"h": (248, 248, 248), "H": (216, 216, 224), "s": (216, 176, 136), "S": (184, 136, 96), "c": (248, 248, 248), "C": (216, 216, 224), "p": (248, 248, 248), "P": (216, 216, 224), "t": (248, 248, 248), "b": (48, 40, 40), "k": (40, 40, 56)},
        "rows": {0: "....kkkkkkkk....", 1: "...khhhhhhhhk...", 2: "..khkkkkkkkkhk..", 3: "..khhhhhhhhhhk..", 4: "..khhssssssshhk.", 5: "..khsssssssshhk.", 6: "..khsssssssshk..", 7: "..khsesssssehk..", 8: "..khsesssssehk..", 9: "..khsbbbbbbshk..", 10: "..khbbbbbbbbhk..", 11: "...khbbbbbbhk...", 13: "....kccwwwcck...", 14: "...kccccccccck..", 15: "..ksccccccccsk.."},
    },
    "lai": {
        "pal": {"h": (40, 40, 48), "H": (24, 24, 32), "s": (240, 204, 168), "S": (208, 160, 128), "c": (40, 48, 96), "C": (24, 32, 72), "p": (40, 48, 96), "P": (24, 32, 72), "t": (56, 150, 146)},
        "rows": {5: "..khhhhhhhhhhk..", 6: "..kHssssssssHk..", 7: "..kskeekskeeksk."},
    },
    "sheinbaum": {
        "pal": {"h": (88, 64, 48), "H": (56, 40, 32), "s": (240, 204, 172), "S": (208, 160, 128), "c": (120, 48, 96), "C": (88, 32, 72), "p": (48, 48, 64), "P": (32, 32, 48), "t": (120, 48, 96), "w": (120, 48, 96)},
        "rows": {1: "...khhhhhhhhhk..", 2: "..khhhhhhhhhhhk.", 3: ".khhhhhhhhhhhhk.", 4: ".khhHhhhhhhhHhk.", 5: ".khHssssssssHhk.", 6: ".khssssssssssHk.", 9: ".khssssssssssHk.", 10: "..khSssssssssHk.", 11: "...kkSSSSSSSkk..", 13: "....kccccccck...", 14: "...kccccccccck.."},
    },
    "carney": {
        "pal": {"h": (168, 168, 176), "H": (128, 128, 136), "s": (240, 208, 184), "S": (208, 168, 144), "c": (40, 48, 96), "C": (24, 32, 72), "p": (40, 48, 96), "P": (24, 32, 72), "t": (200, 40, 40)},
        "rows": {4: "..khhhhhhhhhhk..", 5: "..kHssssssssHk.."},
    },
    "merz": {
        "pal": {"h": (216, 216, 224), "H": (176, 176, 184), "s": (240, 208, 184), "S": (208, 168, 144), "c": (40, 40, 56), "C": (24, 24, 40), "p": (40, 40, 56), "P": (24, 24, 40), "t": (40, 40, 56)},
        "rows": {1: "...khhhhhhhhk...", 2: "..kHssssssssHk..", 3: "..kssssssssssk..", 4: "..kssssssssssk..", 7: "..kskeekskeeksk."},
    },
    "macron": {
        "pal": {"h": (88, 72, 56), "H": (56, 48, 40), "s": (240, 208, 184), "S": (208, 168, 144), "c": (40, 48, 96), "C": (24, 32, 72), "p": (40, 48, 96), "P": (24, 32, 72), "t": (40, 48, 96)},
        "rows": {5: "..kHssssssssHk.."},
    },
    "powell": {
        "pal": {"h": (224, 224, 232), "H": (184, 184, 192), "s": (240, 208, 184), "S": (208, 168, 144), "c": (56, 56, 72), "C": (40, 40, 56), "p": (56, 56, 72), "P": (40, 40, 56), "t": (120, 48, 96)},
        "rows": {4: "..khhhhhhhhhhk..", 5: "..kHssssssssHk.."},
    },
    "bessent": {
        "pal": {"h": (200, 200, 208), "H": (152, 152, 160), "s": (240, 208, 184), "S": (208, 168, 144), "c": (40, 48, 96), "C": (24, 32, 72), "p": (40, 48, 96), "P": (24, 32, 72), "t": (56, 150, 146)},
        "rows": {7: "..kskeekskeeksk.", 8: "..kssesssssessk."},
    },
    "analyst": {
        "pal": {"h": (96, 56, 40), "H": (64, 40, 24), "s": (240, 204, 172), "S": (208, 160, 128), "c": (56, 150, 146), "C": (38, 92, 90), "p": (56, 56, 64), "P": (40, 40, 48), "t": (56, 150, 146), "w": (56, 150, 146)},
        "rows": {1: "...khhhhhhhhhk..", 2: "..khhhhhhhhhhhk.", 3: ".khhhhhhhhhhhhk.", 4: ".khhHhhhhhhhHhk.", 5: ".khHssssssssHhk.", 6: ".khssssssssssHk.", 9: ".khssssssssssHk.", 10: "..khSssssssssHk.", 11: "...kkSSSSSSSkk..", 13: "....kccccccck...", 14: "...kccccccccck.."},
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


FLAG_W, FLAG_H = 12, 8

FLAGS = {
    "us": {"pal": {"r": (200, 40, 56), "w": (248, 248, 248), "b": (40, 56, 128)}, "rows": ["bwbwbrrrrrrr", "wbwbwwwwwwww", "bwbwbrrrrrrr", "wbwbwwwwwwww", "rrrrrrrrrrrr", "wwwwwwwwwwww", "rrrrrrrrrrrr", "wwwwwwwwwwww"]},
    "texas": {"pal": {"r": (200, 40, 56), "w": (248, 248, 248), "b": (40, 56, 128)}, "rows": ["bbbbwwwwwwww", "bbbbwwwwwwww", "bbwbwwwwwwww", "bwwwbwwwwwww", "bbwbbrrrrrrr", "bwbwbrrrrrrr", "bbbbbrrrrrrr", "bbbbbrrrrrrr"]},
    "israel": {"pal": {"b": (32, 88, 200), "w": (248, 248, 248)}, "rows": ["wwwwwwwwwwww", "bbbbbbbbbbbb", "wwwwwbwwwwww", "wwwwbbbwwwww", "wwwbbbbbwwww", "wwwwwbwwwwww", "bbbbbbbbbbbb", "wwwwwwwwwwww"]},
    "china": {"pal": {"r": (216, 40, 40), "y": (248, 216, 56)}, "rows": ["rrrrrrrrrrrr", "ryrrryrrrrrr", "yyyrryrrrrrr", "ryrryrrrrrrr", "rrrryrrrrrrr", "rrrrrrrrrrrr", "rrrrrrrrrrrr", "rrrrrrrrrrrr"]},
    "russia": {"pal": {"w": (248, 248, 248), "b": (40, 56, 160), "r": (208, 40, 48)}, "rows": ["wwwwwwwwwwww", "wwwwwwwwwwww", "wwwwwwwwwwww", "bbbbbbbbbbbb", "bbbbbbbbbbbb", "rrrrrrrrrrrr", "rrrrrrrrrrrr", "rrrrrrrrrrrr"]},
    "iran": {"pal": {"g": (40, 144, 72), "w": (248, 248, 248), "r": (208, 40, 48)}, "rows": ["gggggggggggg", "gggggggggggg", "gggggggggggg", "wwwwwrwwwwww", "wwwwrrrwwwww", "rrrrrrrrrrrr", "rrrrrrrrrrrr", "rrrrrrrrrrrr"]},
    "ukraine": {"pal": {"b": (32, 96, 208), "y": (248, 216, 56)}, "rows": ["bbbbbbbbbbbb", "bbbbbbbbbbbb", "bbbbbbbbbbbb", "bbbbbbbbbbbb", "yyyyyyyyyyyy", "yyyyyyyyyyyy", "yyyyyyyyyyyy", "yyyyyyyyyyyy"]},
    "india": {"pal": {"o": (248, 144, 48), "w": (248, 248, 248), "g": (40, 136, 64), "b": (40, 56, 128)}, "rows": ["oooooooooooo", "oooooooooooo", "oooooooooooo", "wwwwwbbwwwww", "wwwwwbbwwwww", "gggggggggggg", "gggggggggggg", "gggggggggggg"]},
    "uk": {"pal": {"b": (32, 48, 136), "w": (248, 248, 248), "r": (208, 40, 48)}, "rows": ["bwbbbrrbbbwb", "wwwbbrrbbwww", "bwwwbrrbwwwb", "rrrrrrrrrrrr", "rrrrrrrrrrrr", "bwwwbrrbwwwb", "wwwbbrrbbwww", "bwbbbrrbbbwb"]},
    "brazil": {"pal": {"g": (32, 144, 72), "y": (248, 216, 56), "b": (40, 56, 128)}, "rows": ["gggggggggggg", "gggggyyggggg", "gggyyyyyyggg", "ggyyybbyyygg", "ggyyybbyyygg", "gggyyyyyyggg", "gggggyyggggg", "gggggggggggg"]},
    "argentina": {"pal": {"b": (120, 184, 232), "w": (248, 248, 248), "y": (248, 200, 56)}, "rows": ["bbbbbbbbbbbb", "bbbbbbbbbbbb", "bbbbbbbbbbbb", "wwwwwyywwwww", "wwwwwyywwwww", "bbbbbbbbbbbb", "bbbbbbbbbbbb", "bbbbbbbbbbbb"]},
    "mexico": {"pal": {"g": (32, 128, 72), "w": (248, 248, 248), "r": (208, 40, 48), "b": (120, 88, 48)}, "rows": ["ggggwwwwrrrr", "ggggwwwwrrrr", "ggggwwwwrrrr", "ggggwwbwrrrr", "ggggwbbwrrrr", "ggggwwbwrrrr", "ggggwwwwrrrr", "ggggwwwwrrrr"]},
    "chile": {"pal": {"b": (40, 56, 160), "w": (248, 248, 248), "r": (208, 40, 48)}, "rows": ["bbbbwwwwwwww", "bwbbwwwwwwww", "bbbbwwwwwwww", "bbbbwwwwwwww", "rrrrrrrrrrrr", "rrrrrrrrrrrr", "rrrrrrrrrrrr", "rrrrrrrrrrrr"]},
    "taiwan": {"pal": {"b": (32, 56, 160), "w": (248, 248, 248), "r": (208, 40, 48)}, "rows": ["bbbbbbrrrrrr", "bbwbbbrrrrrr", "bwwwbbrrrrrr", "bbwbbbrrrrrr", "rrrrrrrrrrrr", "rrrrrrrrrrrr", "rrrrrrrrrrrr", "rrrrrrrrrrrr"]},
    "japan": {"pal": {"w": (248, 248, 248), "r": (208, 40, 48)}, "rows": ["wwwwwwwwwwww", "wwwwwwwwwwww", "wwwwwrrwwwww", "wwwwrrrrwwww", "wwwwrrrrwwww", "wwwwwrrwwwww", "wwwwwwwwwwww", "wwwwwwwwwwww"]},
    "korea": {"pal": {"w": (248, 248, 248), "r": (208, 40, 48), "b": (32, 56, 160), "k": (40, 40, 56)}, "rows": ["wwwwwwwwwwww", "wkkwwwwwwkkw", "wwwwwrrwwwww", "wwwwrrrrwwww", "wwwwbbbbwwww", "wwwwwbbwwwww", "wkkwwwwwwkkw", "wwwwwwwwwwww"]},
    "germany": {"pal": {"k": (40, 40, 56), "r": (208, 40, 48), "y": (248, 200, 56)}, "rows": ["kkkkkkkkkkkk", "kkkkkkkkkkkk", "kkkkkkkkkkkk", "rrrrrrrrrrrr", "rrrrrrrrrrrr", "yyyyyyyyyyyy", "yyyyyyyyyyyy", "yyyyyyyyyyyy"]},
    "france": {"pal": {"b": (32, 56, 160), "w": (248, 248, 248), "r": (208, 40, 48)}, "rows": ["bbbbwwwwrrrr"] * 8},
    "saudi": {"pal": {"g": (32, 112, 64), "w": (248, 248, 248)}, "rows": ["gggggggggggg", "gggggggggggg", "ggwwgwwgwwgg", "ggwwgwwgwwgg", "gggggggggggg", "gwwwwwwwwwwg", "gggggggggggg", "gggggggggggg"]},
    "turkey": {"pal": {"r": (208, 40, 48), "w": (248, 248, 248)}, "rows": ["rrrrrrrrrrrr", "rrrwwrrrrrrr", "rrwwrrrrrrrr", "rwwrrrrwrrrr", "rwwrrrrwrrrr", "rrwwrrrrrrrr", "rrrwwrrrrrrr", "rrrrrrrrrrrr"]},
    "eu": {"pal": {"b": (32, 56, 160), "y": (248, 200, 56)}, "rows": ["bbbbbbbbbbbb", "bbbbbybbbbbb", "bbbybbbybbbb", "bbybbbbbybbb", "bbybbbbbybbb", "bbbybbbybbbb", "bbbbbybbbbbb", "bbbbbbbbbbbb"]},
    "canada": {"pal": {"r": (208, 40, 48), "w": (248, 248, 248)}, "rows": ["rrrwwwwwwrrr", "rrrwwwrwwrrr", "rrrwwrrrwrrr", "rrrwrrrrrrrr", "rrrwwrrrwrrr", "rrrwwwrwwrrr", "rrrwwwrwwrrr", "rrrwwwwwwrrr"]},
    "venezuela": {"pal": {"y": (248, 200, 56), "b": (32, 56, 160), "r": (208, 40, 48), "w": (248, 248, 248)}, "rows": ["yyyyyyyyyyyy", "yyyyyyyyyyyy", "yyyyyyyyyyyy", "bbbwbwbwbbbb", "bbbbbbbbbbbb", "rrrrrrrrrrrr", "rrrrrrrrrrrr", "rrrrrrrrrrrr"]},
    "poly": {"pal": {"k": (24, 24, 32), "w": (248, 248, 248)}, "rows": ["kkkkkkkkkkkk", "kkwwwwwwwwkk", "kkwkkkkkkwkk", "kkwkkkkkkwkk", "kkwkkkkkkwkk", "kkwwwwwwwwkk", "kkkkkkkkkkkk", "kkkkkkkkkkkk"]},
}


def flag(name, scale=1, pole=False):
    spec = FLAGS[name]
    rows = spec["rows"]
    w, h = FLAG_W, FLAG_H
    im = Image.new("RGBA", ((w + (2 if pole else 0)) * scale, (h + (4 if pole else 0)) * scale), (0, 0, 0, 0))
    px = im.load()
    ox = 2 if pole else 0
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            col = spec["pal"][ch] + (255,)
            for dy in range(scale):
                for dx in range(scale):
                    px[(i + ox) * scale + dx, j * scale + dy] = col
    if pole:
        for y in range((h + 4) * scale):
            for dx in range(scale):
                px[dx, y] = (104, 104, 112, 255)
    return im


def sheet(scale=3, cols=8):
    names = list(NPCS)
    fl = list(FLAGS)
    cw, ch = 20 * scale, 26 * scale
    rows_n = -(-len(names) // cols)
    rows_f = -(-len(fl) // cols)
    im = Image.new("RGB", (cols * cw, rows_n * ch + rows_f * 14 * scale), (136, 216, 152))
    for k, n in enumerate(names):
        im.paste(render(n, scale), ((k % cols) * cw + 2 * scale, (k // cols) * ch + 2 * scale), render(n, scale))
    y0 = rows_n * ch
    for k, n in enumerate(fl):
        f = flag(n, scale, pole=True)
        im.paste(f, ((k % cols) * cw + 2 * scale, y0 + (k // cols) * 14 * scale + scale), f)
    return im
