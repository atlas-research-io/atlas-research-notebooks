import marimo

__generated_with = "0.14.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import io
    import os
    import json
    import subprocess
    import tempfile
    import urllib.request
    import datetime as dt
    import numpy as np
    import pandas as pd
    import yfinance as yf
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, FFMpegWriter
    return FFMpegWriter, FuncAnimation, dt, io, json, mo, np, os, pd, plt, subprocess, tempfile, urllib, yf


@app.cell
def _(mo):
    mo.md("# Israel voted. Nobody won. The bettors had it first.")
    return


@app.cell
def _(dt, json, pd, urllib, yf):
    TOKENS = {
        "Netanyahu": "20006732765674855733524007935991362439352594042415161039767275461950712817548",
        "Eisenkot": "52487256270918227930942830546248720603566203568229607048093730748840489555808",
        "Bennett": "58945936829392654397399777214757608864525173988558750256164021442231118224154",
    }

    def poly_history(token, interval, fidelity):
        url = f"https://clob.polymarket.com/prices-history?market={token}&interval={interval}&fidelity={fidelity}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; AtlasResearch/1.0)"})
        raw = urllib.request.urlopen(req, timeout=30).read().decode()
        h = json.loads(raw)["history"]
        s = pd.Series([p["p"] for p in h], index=[dt.datetime.fromtimestamp(p["t"], dt.timezone.utc) for p in h])
        return s[~s.index.duplicated()].sort_index()

    odds_year = pd.DataFrame({k: poly_history(t, "max", 1440) for k, t in TOKENS.items()}).ffill().dropna()
    odds_night = pd.DataFrame({k: poly_history(t, "1w", 60) for k, t in TOKENS.items()}).ffill().dropna()
    odds_night = odds_night.loc[pd.Timestamp("2026-10-27 12:00", tz="UTC"):]

    YEAR_EVENTS = [
        ("2026-02-28", "War on Iran\nbegins"),
        ("2026-06-17", "Islamabad memo,\nfighting pauses"),
        ("2026-07-27", "Eisenkot\novertakes"),
        ("2026-10-27", "Election\nday"),
    ]

    SEATS = [
        ("Likud", "Netanyahu", 26, "right"),
        ("Yashar", "Eisenkot", 21, "opp"),
        ("Joint List", "Jabareen", 12, "arab"),
        ("Together", "Bennett", 12, "opp"),
        ("Democrats", "Golan", 8, "opp"),
        ("Ra'am", "Abbas", 7, "arab"),
        ("Yisrael Beiteinu", "Lieberman", 7, "opp"),
        ("UTJ", "Asher", 7, "right"),
        ("Otzma Yehudit", "Ben-Gvir", 7, "right"),
        ("Shas", "Deri", 7, "right"),
        ("RZP-Zehut", "Smotrich", 6, "right"),
    ]
    seats = pd.DataFrame(SEATS, columns=["party", "leader", "seats", "bloc"])
    blocs = seats.groupby("bloc")["seats"].sum()

    px = yf.download(["EIS", "ILS=X", "BZ=F"], start="2026-10-20", end="2026-10-29", auto_adjust=True, progress=False)["Close"]
    day_move = (px.loc["2026-10-28"] / px.loc["2026-10-27"] - 1) * 100
    REPORTED = {"EIS": -4.9, "BZ=F": -2.6}

    def move(ticker):
        v = float(day_move.get(ticker, float("nan")))
        return v if v == v else REPORTED[ticker]

    MOVES = [
        ("Israel ETF (EIS), New York", move("EIS")),
        ("Tel Aviv 35", -2.3),
        ("Shekel vs dollar", -2.2),
        ("Israel 10-year yield, bp", 8),
        ("Brent crude", move("BZ=F")),
    ]
    odds_year.tail(3), blocs, day_move
    return MOVES, REPORTED, SEATS, TOKENS, YEAR_EVENTS, blocs, day_move, move, odds_night, odds_year, poly_history, px, seats


@app.cell
def _(FFMpegWriter, FuncAnimation, np, os, plt, subprocess, tempfile, urllib):
    from matplotlib import font_manager
    from matplotlib.lines import Line2D
    from matplotlib.patches import Circle, Ellipse
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer

    ATLAS = {
        "bg": "#0f0f0f",
        "ink": "#f4f1ea",
        "muted": "#8a8780",
        "accent": "#4a9d9a",
        "hot": "#d4607a",
        "amber": "#e0a24f",
        "blue": "#6b97e0",
        "violet": "#9385e3",
        "font": "Atlas Sans",
        "serif": "Atlas Serif",
        "mono": "Atlas Mono",
    }
    BLOC_COLOR = {"right": ATLAS["hot"], "opp": ATLAS["accent"], "arab": ATLAS["amber"]}
    FPS = 24

    FONT_DIR = os.path.join(tempfile.gettempdir(), "atlas-fonts")
    os.makedirs(FONT_DIR, exist_ok=True)
    FONT_SRC = [
        ("Atlas Serif", "https://github.com/google/fonts/raw/main/ofl/sourceserif4/SourceSerif4%5Bopsz%2Cwght%5D.ttf", {"opsz": 24}),
        ("Atlas Sans", "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf", {"opsz": 14}),
        ("Atlas Mono", "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf", 400),
        ("Atlas Mono", "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Bold.ttf", 700),
    ]

    def _fetch(url):
        path = os.path.join(FONT_DIR, url.rsplit("/", 1)[1].replace("%5B", "[").replace("%5D", "]").replace("%2C", ","))
        if not os.path.exists(path):
            req = urllib.request.Request(url, headers={"User-Agent": "atlas-research"})
            with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as f:
                f.write(r.read())
        return path

    def _rename(font, family, weight):
        style = "Bold" if weight >= 600 else "Regular"
        for rec in font["name"].names:
            if rec.nameID in (1, 16):
                rec.string = family
            elif rec.nameID in (2, 17):
                rec.string = style
            elif rec.nameID == 4:
                rec.string = f"{family} {style}"
            elif rec.nameID == 6:
                rec.string = f"{family.replace(' ', '')}-{style}"
        font["OS/2"].usWeightClass = weight
        if weight >= 600:
            font["OS/2"].fsSelection = (font["OS/2"].fsSelection | (1 << 5)) & ~(1 << 6)
            font["head"].macStyle |= 1
        else:
            font["OS/2"].fsSelection = (font["OS/2"].fsSelection | (1 << 6)) & ~(1 << 5)
            font["head"].macStyle &= ~1

    def load_fonts():
        for family, url, spec in FONT_SRC:
            src = _fetch(url)
            weights = (400, 700) if isinstance(spec, dict) else (spec,)
            for weight in weights:
                out = os.path.join(FONT_DIR, f"{family.replace(' ', '')}-{weight}.ttf")
                if not os.path.exists(out):
                    f = TTFont(src)
                    if isinstance(spec, dict):
                        instancer.instantiateVariableFont(f, {**spec, "wght": weight}, inplace=True)
                    _rename(f, family, weight)
                    f.save(out)
                font_manager.fontManager.addfont(out)
        plt.rcParams["font.family"] = ATLAS["font"]

    try:
        load_fonts()
    except Exception as exc:
        print("fonts unavailable, falling back:", exc)
        ATLAS.update(font="DejaVu Sans", serif="DejaVu Serif", mono="DejaVu Sans Mono")

    def _mark(fig):
        bg = fig.add_axes([0, 0, 1, 1], zorder=-10)
        bg.set_axis_off()
        bg.set_xlim(0, 1)
        bg.set_ylim(0, 1)
        gx, gy = np.meshgrid(np.arange(0.04, 0.97, 0.045), np.arange(0.11, 0.80, 0.08))
        bg.scatter(gx, gy, s=2.2, color=ATLAS["ink"], alpha=0.05, linewidths=0)
        bg.add_line(Line2D([0, 1], [0.992, 0.992], color=ATLAS["accent"], lw=1.5, solid_capstyle="butt"))
        globe = fig.add_axes([0.954, 0.036, 0.0219, 0.0389], zorder=5)
        globe.set_axis_off()
        globe.set_xlim(-1.15, 1.15)
        globe.set_ylim(-1.15, 1.15)
        globe.set_aspect("equal")
        kw = dict(fill=False, ec=ATLAS["accent"], lw=0.9, alpha=0.35)
        globe.add_patch(Circle((0, 0), 1, **kw))
        globe.add_patch(Ellipse((0, 0), 0.9, 2, **kw))
        globe.add_line(Line2D([-0.95, 0.95], [0.4, 0.4], color=ATLAS["accent"], lw=0.7, alpha=0.35))
        globe.add_line(Line2D([-0.95, 0.95], [-0.4, -0.4], color=ATLAS["accent"], lw=0.7, alpha=0.35))

    def canvas(rect=(0.08, 0.16, 0.86, 0.60)):
        fig = plt.figure(figsize=(12.8, 7.2), dpi=100, facecolor=ATLAS["bg"])
        _mark(fig)
        ax = fig.add_axes(list(rect))
        ax.set_facecolor("none")
        for s in ax.spines.values():
            s.set_visible(False)
        ax.tick_params(colors=ATLAS["muted"], labelsize=10.5, length=0)
        for lab in ax.get_xticklabels() + ax.get_yticklabels():
            lab.set_family(ATLAS["mono"])
        return fig, ax

    def chrome(fig, kicker, title, subtitle, source):
        fig.text(0.08, 0.95, kicker.upper(), color=ATLAS["accent"], fontsize=10.5, family=ATLAS["mono"], va="top")
        fig.text(0.08, 0.91, title, color=ATLAS["ink"], fontsize=27, fontweight="bold", family=ATLAS["serif"], va="top")
        fig.text(0.08, 0.845, subtitle, color=ATLAS["muted"], fontsize=13, family=ATLAS["font"], va="top")
        fig.text(0.08, 0.05, source, color=ATLAS["muted"], fontsize=9.5, family=ATLAS["mono"])
        fig.text(0.945, 0.05, "atlas-research.io", color=ATLAS["accent"], fontsize=10.5, family=ATLAS["mono"], ha="right")

    def ease(t):
        return 1 - (1 - t) ** 2

    def save_scene(fig, draw, frames):
        anim = FuncAnimation(fig, draw, frames=frames, blit=False)
        path = tempfile.mktemp(suffix=".mp4")
        anim.save(path, writer=FFMpegWriter(fps=FPS, codec="libx264", extra_args=["-pix_fmt", "yuv420p", "-movflags", "faststart"]), savefig_kwargs={"facecolor": ATLAS["bg"]})
        plt.close(fig)
        return path

    def concat(paths):
        lst = tempfile.mktemp(suffix=".txt")
        with open(lst, "w") as f:
            for p in paths:
                f.write(f"file '{p}'\n")
        out = tempfile.mktemp(suffix=".mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], check=True)
        with open(out, "rb") as f:
            return f.read()

    def read(path):
        with open(path, "rb") as f:
            return f.read()

    return ATLAS, BLOC_COLOR, FPS, canvas, chrome, concat, ease, read, save_scene

@app.cell
def _(ATLAS, FPS, YEAR_EVENTS, canvas, chrome, ease, np, odds_year, pd, save_scene):
    fig1, ax1 = canvas()
    chrome(fig1, "THE BET, ONE YEAR", "In September the market gave Netanyahu a 28% chance", "Polymarket odds of being the next prime minister, daily. The war made him, the war unmade him, the count brought him back.", "Source: Polymarket price history, Nov 2025 to 28 Oct 2026. Atlas Research.")
    n1 = len(odds_year)
    x1 = np.arange(n1)
    ax1.set_xlim(0, n1 * 1.17)
    ax1.set_ylim(0, 0.8)
    ax1.set_yticks([0, 0.25, 0.5, 0.75])
    ax1.set_yticklabels(["0%", "25%", "50%", "75%"], family=ATLAS["font"])
    ax1.grid(axis="y", color="#2a2a2a", linewidth=0.8)
    months1 = [i for i in range(1, n1) if odds_year.index[i].month != odds_year.index[i - 1].month]
    ax1.set_xticks(months1)
    ax1.set_xticklabels([odds_year.index[i].strftime("%b") for i in months1], family=ATLAS["font"])
    (lb,) = ax1.plot([], [], color=ATLAS["hot"], linewidth=3)
    (le,) = ax1.plot([], [], color=ATLAS["accent"], linewidth=3)
    tb = ax1.text(0, 0, "", color=ATLAS["hot"], fontsize=14, fontweight="bold", va="center", family=ATLAS["font"])
    te = ax1.text(0, 0, "", color=ATLAS["accent"], fontsize=14, fontweight="bold", va="center", family=ATLAS["font"])
    ev1 = [(int(np.searchsorted(odds_year.index, pd.Timestamp(d, tz="UTC"))), lab) for d, lab in YEAR_EVENTS]
    ev1_lines = [ax1.axvline(i, color=ATLAS["muted"], linewidth=0.8, linestyle="--", alpha=0) for i, _ in ev1]
    ev1_texts = [ax1.text(i + 2, 0.78 - 0.07 * (k % 2), "", color=ATLAS["muted"], fontsize=10, family=ATLAS["font"], va="top", linespacing=1.15) for k, (i, _) in enumerate(ev1)]
    draw1 = int(FPS * 11)
    hold1 = int(FPS * 3)

    def scene1(frame):
        n = int(ease(min(1, frame / draw1)) * (n1 - 1)) + 1
        b = odds_year["Netanyahu"].values
        e = odds_year["Eisenkot"].values
        lb.set_data(x1[:n], b[:n])
        le.set_data(x1[:n], e[:n])
        gap = 0.05 if abs(b[n - 1] - e[n - 1]) < 0.08 else 0
        tb.set_position((n + 2, b[n - 1] + (gap if b[n - 1] >= e[n - 1] else -gap)))
        tb.set_text(f"Netanyahu {b[n-1]*100:.0f}%")
        te.set_position((n + 2, e[n - 1] + (gap if e[n - 1] > b[n - 1] else -gap)))
        te.set_text(f"Eisenkot {e[n-1]*100:.0f}%")
        for (i, lab), ln, t in zip(ev1, ev1_lines, ev1_texts):
            if i < n:
                ln.set_alpha(1)
                t.set_text(lab)
        return [lb, le, tb, te] + ev1_lines + ev1_texts

    scene1_path = save_scene(fig1, scene1, draw1 + hold1)
    return (scene1_path,)


@app.cell
def _(ATLAS, FPS, canvas, chrome, ease, np, odds_night, save_scene):
    fig2, ax2 = canvas()
    chrome(fig2, "ELECTION NIGHT, HOUR BY HOUR", "Then the exit polls were wrong", "Polymarket odds through the night. Exit polls at 22:00 Israel time said a tie. The count said otherwise by 3am.", "Source: Polymarket hourly price history, 27 to 28 Oct 2026, UTC. Atlas Research.")
    n2 = len(odds_night)
    x2 = np.arange(n2)
    ax2.set_xlim(0, n2 * 1.12)
    ax2.set_ylim(0, 0.8)
    ax2.set_yticks([0, 0.25, 0.5, 0.75])
    ax2.set_yticklabels(["0%", "25%", "50%", "75%"], family=ATLAS["font"])
    ax2.grid(axis="y", color="#2a2a2a", linewidth=0.8)
    ticks2 = list(range(0, n2, max(1, n2 // 6)))
    ax2.set_xticks(ticks2)
    ax2.set_xticklabels([odds_night.index[i].strftime("%a %H:%M") for i in ticks2], family=ATLAS["font"], fontsize=10)
    (lb2,) = ax2.plot([], [], color=ATLAS["hot"], linewidth=3)
    (le2,) = ax2.plot([], [], color=ATLAS["accent"], linewidth=3)
    tb2 = ax2.text(0, 0, "", color=ATLAS["hot"], fontsize=14, fontweight="bold", va="center", family=ATLAS["font"])
    te2 = ax2.text(0, 0, "", color=ATLAS["accent"], fontsize=14, fontweight="bold", va="center", family=ATLAS["font"])
    polls_i = int(np.searchsorted(odds_night.index, odds_night.index[0].replace(hour=20, minute=0)))
    ax2.axvline(polls_i, color=ATLAS["muted"], linewidth=0.8, linestyle="--")
    ax2.text(polls_i + 0.3, 0.76, "Polls close,\nexit polls: tie", color=ATLAS["muted"], fontsize=10, family=ATLAS["font"], va="top", linespacing=1.15)
    draw2 = int(FPS * 9)
    hold2 = int(FPS * 3)

    def scene2(frame):
        n = int(ease(min(1, frame / draw2)) * (n2 - 1)) + 1
        b = odds_night["Netanyahu"].values
        e = odds_night["Eisenkot"].values
        lb2.set_data(x2[:n], b[:n])
        le2.set_data(x2[:n], e[:n])
        gap = 0.05 if abs(b[n - 1] - e[n - 1]) < 0.08 else 0
        tb2.set_position((n + 0.5, b[n - 1] + (gap if b[n - 1] >= e[n - 1] else -gap)))
        tb2.set_text(f"Netanyahu {b[n-1]*100:.0f}%")
        te2.set_position((n + 0.5, e[n - 1] + (gap if e[n - 1] > b[n - 1] else -gap)))
        te2.set_text(f"Eisenkot {e[n-1]*100:.0f}%")
        return [lb2, le2, tb2, te2]

    scene2_path = save_scene(fig2, scene2, draw2 + hold2)
    return (scene2_path,)


@app.cell
def _(ATLAS, BLOC_COLOR, FPS, blocs, canvas, chrome, ease, np, save_scene, seats):
    fig3, ax3 = canvas(rect=(0.30, 0.14, 0.62, 0.62))
    chrome(fig3, "THE COUNT", "26 seats, and nobody gets to 61", "Preliminary Knesset result, 90% counted. Netanyahu's bloc 53, the opposition 48, the Arab parties 19. Majority is 61.", "Source: Central Elections Committee via Wikipedia, 28 Oct 2026, 90.2% counted. Official results 4 Nov. Atlas Research.")
    n3 = len(seats)
    y3 = np.arange(n3)[::-1]
    colors3 = [BLOC_COLOR[b] for b in seats["bloc"]]
    bars3 = ax3.barh(y3, [0] * n3, height=0.66, color=colors3)
    ax3.set_xlim(0, 32)
    ax3.set_ylim(-0.7, n3 - 0.3)
    ax3.set_xticks([])
    ax3.set_yticks([])
    tr3 = ax3.get_yaxis_transform()
    for yi, p, l in zip(y3, seats["party"], seats["leader"]):
        ax3.text(-0.015, yi + 0.12, p, color=ATLAS["ink"], fontsize=13, fontweight="bold", ha="right", va="center", family=ATLAS["font"], transform=tr3)
        ax3.text(-0.015, yi - 0.22, l, color=ATLAS["muted"], fontsize=9.5, ha="right", va="center", family=ATLAS["font"], transform=tr3)
    vals3 = [ax3.text(0, yi, "", color=ATLAS["ink"], fontsize=13, fontweight="bold", va="center", family=ATLAS["font"]) for yi in y3]
    legend3 = [
        (f"Netanyahu bloc {int(blocs['right'])}", ATLAS["hot"]),
        (f"Opposition {int(blocs['opp'])}", ATLAS["accent"]),
        (f"Arab parties {int(blocs['arab'])}", ATLAS["amber"]),
    ]
    for k, (lab, c) in enumerate(legend3):
        fig3.text(0.30 + k * 0.21, 0.795, "■ " + lab, color=c, fontsize=11, fontweight="bold", family=ATLAS["font"])
    per_bar3 = int(FPS * 0.45)
    hold3 = int(FPS * 3)

    def scene3(frame):
        for i in range(n3):
            t = ease(min(1, max(0, (frame - i * per_bar3) / per_bar3)))
            v = seats["seats"].iloc[i] * t
            bars3[i].set_width(v)
            vals3[i].set_x(v + 0.4)
            vals3[i].set_text(f"{v:.0f}" if t > 0 else "")
        return list(bars3) + vals3

    scene3_path = save_scene(fig3, scene3, n3 * per_bar3 + hold3)
    return (scene3_path,)


@app.cell
def _(ATLAS, FPS, MOVES, canvas, chrome, ease, np, save_scene):
    fig4, ax4 = canvas(rect=(0.34, 0.18, 0.58, 0.56))
    chrome(fig4, "WHAT IT COST BY LUNCH", "Tel Aviv priced the deadlock in a day", "Wednesday 28 October. Stocks, the shekel and bonds all sold off on a government that may take weeks to form.", "Source: Yahoo Finance for EIS and Brent; Reuters and Times of Israel for TA-35, shekel and bond yields, 28 Oct 2026. Atlas Research.")
    labels4 = [m[0] for m in MOVES]
    v4 = [m[1] for m in MOVES]
    n4 = len(v4)
    y4 = np.arange(n4)[::-1]
    colors4 = [ATLAS["hot"] if (v < 0 or "yield" in lab) else ATLAS["accent"] for lab, v in MOVES]
    bars4 = ax4.barh(y4, [0] * n4, height=0.62, color=colors4)
    lo4, hi4 = min(v4 + [0]), max(v4 + [0])
    ax4.set_xlim(lo4 * 1.5 - 1, hi4 * 1.5 + 1)
    ax4.set_ylim(-0.7, n4 - 0.3)
    ax4.set_xticks([])
    ax4.set_yticks([])
    ax4.axvline(0, color=ATLAS["muted"], linewidth=0.8)
    tr4 = ax4.get_yaxis_transform()
    for yi, lab in zip(y4, labels4):
        ax4.text(-0.015, yi, lab, color=ATLAS["ink"], fontsize=14, fontweight="bold", ha="right", va="center", family=ATLAS["font"], transform=tr4)
    texts4 = [ax4.text(0, yi, "", color=ATLAS["ink"], fontsize=14, fontweight="bold", va="center", family=ATLAS["font"]) for yi in y4]
    per_bar4 = int(FPS * 0.6)
    hold4 = int(FPS * 3)

    def scene4(frame):
        for i in range(n4):
            t = ease(min(1, max(0, (frame - i * per_bar4) / per_bar4)))
            v = v4[i] * t
            bars4[i].set_width(v)
            unit = "bp" if "yield" in labels4[i] else "%"
            texts4[i].set_x(v + 0.3 if v >= 0 else v - 0.3)
            texts4[i].set_ha("left" if v >= 0 else "right")
            texts4[i].set_text(f"{v:+.1f}{unit}" if t > 0 else "")
        return list(bars4) + texts4

    scene4_path = save_scene(fig4, scene4, n4 * per_bar4 + hold4)
    return (scene4_path,)


@app.cell
def _(ATLAS, FPS, canvas, chrome, ease, save_scene):
    fig5, ax5 = canvas(rect=(0.08, 0.14, 0.86, 0.64))
    chrome(fig5, "WHAT HAPPENS NEXT", "Everyone is waiting for November 3", "The chain from a Knesset deadlock to the price of oil, in the order it will happen.", "Source: Iran International, Al Jazeera, CBS, 27 to 28 Oct 2026; Polymarket. Atlas Research.")
    ax5.set_xlim(0, 1)
    ax5.set_ylim(0, 1)
    ax5.set_xticks([])
    ax5.set_yticks([])
    STEPS = [
        ("1", "Official results 4 Nov. Herzog hands someone the mandate within 7 days.\nNetanyahu stays caretaker PM. Talks could take weeks."),
        ("2", "US midterms 3 Nov. Trump told Israelis to re-elect Netanyahu\nto \"finish the job\" in Iran."),
        ("3", "Netanyahu, Wednesday: a rare chance, with Trump,\n\"to remove the existential threat of Iran once and for all.\""),
        ("4", "US media: the military is ready to strike within days if ordered.\nIn Tehran, people are forming groups to warn each other of jets."),
        ("5", "Hormuz is already closed 241 days. Brent is $111.\nA second round puts every number in this video back on the board."),
    ]
    rows5 = []
    for k, (num, txt) in enumerate(STEPS):
        y = 0.92 - k * 0.19
        circ = ax5.text(0.02, y, num, color=ATLAS["bg"], fontsize=13, fontweight="bold", ha="center", va="center", family=ATLAS["font"], bbox=dict(boxstyle="circle,pad=0.35", fc=ATLAS["accent"], ec="none"), alpha=0)
        body = ax5.text(0.07, y, txt, color=ATLAS["ink"], fontsize=13.5, va="center", family=ATLAS["font"], linespacing=1.3, alpha=0)
        rows5.append((circ, body))
    per5 = int(FPS * 1.6)
    hold5 = int(FPS * 4)

    def scene5(frame):
        for k, (c, b) in enumerate(rows5):
            a = ease(min(1, max(0, (frame - k * per5) / (per5 * 0.5))))
            c.set_alpha(a)
            b.set_alpha(a)
        return [t for r in rows5 for t in r]

    scene5_path = save_scene(fig5, scene5, len(STEPS) * per5 + hold5)
    return (scene5_path,)


@app.cell
def _(concat, mo, read, scene1_path, scene2_path, scene3_path, scene4_path, scene5_path):
    full_mp4 = concat([scene1_path, scene2_path, scene3_path, scene4_path, scene5_path])
    mo.vstack([
        mo.video(full_mp4, controls=True, autoplay=True, loop=True, muted=True),
        mo.hstack([
            mo.download(data=full_mp4, filename="israel-voted-nobody-won.mp4", mimetype="video/mp4", label="Download full animation"),
            mo.download(data=read(scene1_path), filename="israel-1-the-bet.mp4", mimetype="video/mp4", label="Scene 1"),
            mo.download(data=read(scene2_path), filename="israel-2-election-night.mp4", mimetype="video/mp4", label="Scene 2"),
            mo.download(data=read(scene3_path), filename="israel-3-the-count.mp4", mimetype="video/mp4", label="Scene 3"),
            mo.download(data=read(scene4_path), filename="israel-4-what-it-cost.mp4", mimetype="video/mp4", label="Scene 4"),
            mo.download(data=read(scene5_path), filename="israel-5-what-next.mp4", mimetype="video/mp4", label="Scene 5"),
        ]),
    ])
    return (full_mp4,)


if __name__ == "__main__":
    app.run()
