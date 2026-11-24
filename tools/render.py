#!/usr/bin/env python3
"""Render the news-image entry: a one-page front page summing up the world
news of Tuesday 24 November 2026.

Drawn with Pillow only, from the headlines researched for that day. No
network, no randomness, no timestamps: the same run always writes the same
bytes. Run from the entry root:  python3 tools/render.py
Writes entry.png beside this script's parent directory (the entry root).
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (251, 248, 241)
NAVY = (16, 36, 62)
NAVY_SOFT = (28, 58, 92)
GOLD = (201, 162, 39)
GOLD_SOFT = (242, 230, 190)
INK = (26, 26, 26)
MUTED = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (210, 205, 195)

TEAL = (14, 124, 107)
GREEN = (26, 127, 55)
RED = (179, 38, 30)
ORANGE = (211, 84, 0)
SLATE = (91, 91, 122)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 58)
F_DATE = font("DejaVuSans-Bold.ttf", 30)
F_KICKER = font("DejaVuSans-Bold.ttf", 21)
F_HEAD = font("DejaVuSans-Bold.ttf", 52)
F_SUM = font("DejaVuSans.ttf", 26)
F_CELL_KICKER = font("DejaVuSans-Bold.ttf", 18)
F_CELL_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_CELL_SUM = font("DejaVuSans.ttf", 21)
F_TICKER = font("DejaVuSans-Bold.ttf", 23)
F_FOOT = font("DejaVuSans.ttf", 18)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        line = ""
        for word in words:
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= max_w or not line:
                line = trial
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def circle_icon(draw, cx, cy, r, accent, tint, draw_fn):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=tint,
                 outline=accent, width=4)
    draw_fn(draw, cx, cy, r, accent)


def icon_globe(draw, cx, cy, r, accent):
    s = int(r * 0.62)
    draw.ellipse([cx - s, cy - s, cx + s, cy + s], outline=accent, width=5)
    draw.arc([cx - s, cy - s, cx + s, cy + s], start=200, end=340,
             fill=accent, width=4)
    draw.ellipse([cx - s, cy - int(s * 0.38), cx + s, cy + int(s * 0.38)],
                 outline=accent, width=4)
    draw.line([cx, cy - s, cx, cy + s], fill=accent, width=4)
    # crack: the deal breaks
    draw.line([(cx - 6, cy - s - 14), (cx + 8, cy - s + 6),
               (cx - 4, cy - s + 22)], fill=RED, width=5, joint="curve")


def icon_chart(draw, cx, cy, r, accent):
    base = cy + int(r * 0.45)
    bars = [(-34, 22), (-10, 38), (14, 56)]
    for dx, h in bars:
        draw.rectangle([cx + dx, base - h, cx + dx + 16, base],
                       fill=accent)
    draw.line([(cx - 42, base - 66), (cx - 18, base - 44),
               (cx + 6, base - 52), (cx + 38, base - 78)],
              fill=accent, width=5, joint="curve")
    draw.polygon([(cx + 38, base - 78), (cx + 24, base - 76),
                  (cx + 36, base - 62)], fill=accent)


def icon_ship(draw, cx, cy, r, accent):
    draw.polygon([(cx - 40, cy + 2), (cx + 40, cy + 2),
                  (cx + 30, cy + 28), (cx - 30, cy + 28)], fill=accent)
    draw.rectangle([cx - 3, cy - 32, cx + 3, cy + 2], fill=accent)
    draw.rectangle([cx + 3, cy - 32, cx + 24, cy - 16], fill=accent)
    draw.line([(cx - 34, cy + 40), (cx + 34, cy + 40)], fill=accent, width=4)


def icon_flame(draw, cx, cy, r, accent):
    pts = [(cx, cy - 52), (cx + 20, cy - 18), (cx + 34, cy + 4),
           (cx + 26, cy + 34), (cx + 8, cy + 48), (cx - 12, cy + 48),
           (cx - 30, cy + 30), (cx - 32, cy + 2), (cx - 18, cy - 22)]
    draw.polygon(pts, fill=accent)
    draw.ellipse([cx - 10, cy + 6, cx + 12, cy + 38], fill=GOLD)


def icon_city(draw, cx, cy, r, accent):
    draw.rectangle([cx - 40, cy - 20, cx - 8, cy + 40], fill=accent)
    draw.rectangle([cx + 2, cy - 38, cx + 38, cy + 40], fill=accent)
    for wx in (-32, -20):
        for wy in (-10, 6, 22):
            draw.rectangle([cx + wx, cy + wy, cx + wx + 6, cy + wy + 6],
                           fill=PAPER)
    for wx in (10, 24):
        for wy in (-28, -12, 4, 20):
            draw.rectangle([cx + wx, cy + wy, cx + wx + 6, cy + wy + 6],
                           fill=PAPER)
    draw.line([(cx - 40, cy + 40), (cx + 38, cy + 40)], fill=accent, width=4)
    draw.line([(cx + 2, cy - 38), (cx + 16, cy - 52), (cx + 30, cy - 38)],
              fill=RED, width=5, joint="curve")


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 116], fill=NAVY)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 14), title, font=F_TITLE, fill=(255, 255, 255))
    date = "TUESDAY, 24 NOVEMBER 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 76), date, font=F_DATE, fill=GOLD)
    d.rectangle([0, 116, W, 120], fill=GOLD)

    # ---- Lead story: COP31 ----------------------------------------------
    lx, ly = 36, 140
    d.text((lx, ly), "CLIMATE  •  ANTALYA, TURKEY", font=F_KICKER, fill=TEAL)
    circle_icon(d, 118, 288, 74, TEAL, (224, 240, 236), icon_globe)
    head = "COP31 COLLAPSES"
    d.text((226, 176), head, font=F_HEAD, fill=NAVY)
    sub = ("The UN climate summit ends with no deal — the longest COP ever — "
           "as nations split over fossil fuels.")
    y = 246
    y = draw_lines(d, wrap(d, sub, F_SUM, 724), F_SUM, 226, y, INK, 34)
    sub2 = ("The EU and UK reject a pact that never mentions oil, coal or gas.")
    draw_lines(d, wrap(d, sub2, F_SUM, 724), F_SUM, 226, y + 6, MUTED, 34)
    d.line([(36, 408), (988, 408)], fill=LINE, width=2)

    # ---- Grid of four stories -------------------------------------------
    cells = [
        ("MARKETS  •  NEW YORK", GREEN, icon_chart,
         "Huang returns, Nvidia soars 31%",
         "Shares jump and the Nasdaq climbs 6.5% as Jensen Huang is "
         "reinstated as chief executive."),
        ("UKRAINE WAR  •  AT SEA", RED, icon_ship,
         "Russian ships hit off Libya and Finland",
         "Kyiv claims a warship sunk near Benghazi; a cargo vessel burns "
         "after a drone strike."),
        ("INDONESIA  •  BANTEN", ORANGE, icon_flame,
         "24 dead in candy factory fire",
         "Rescuers search the wreckage for about 30 workers still missing "
         "after the weekend blaze."),
        ("GAZA", SLATE, icon_city,
         "Strikes kill UN worker and others",
         "Israeli strikes hit Gaza as settler arson in the West Bank draws "
         "condemnation."),
    ]
    gx, gy = 36, 428
    cw, ch, gap = 468, 216, 16
    for i, (kicker, accent, icon, headline, summary) in enumerate(cells):
        cx0 = gx + (i % 2) * (cw + gap)
        cy0 = gy + (i // 2) * (ch + gap)
        d.rectangle([cx0, cy0, cx0 + cw, cy0 + ch], fill=CARD,
                    outline=LINE, width=2)
        d.rectangle([cx0, cy0, cx0 + cw, cy0 + 6], fill=accent)
        circle_icon(d, cx0 + 62, cy0 + 62, 42, accent, (244, 244, 244), icon)
        tx = cx0 + 122
        d.text((tx, cy0 + 18), kicker, font=F_CELL_KICKER, fill=accent)
        hl = wrap(d, headline, F_CELL_HEAD, cw - 140)
        y = draw_lines(d, hl, F_CELL_HEAD, tx, cy0 + 46, NAVY, 32)
        draw_lines(d, wrap(d, summary, F_CELL_SUM, cw - 140),
                   F_CELL_SUM, tx, y + 4, INK, 26)

    # ---- Sport ticker ----------------------------------------------------
    d.rectangle([36, 892, 988, 952], fill=GOLD_SOFT, outline=GOLD, width=2)
    tick = ("SPORT — Alcaraz wins first ATP Finals title  •  "
            "Chess title match opens in Geneva")
    size = 23
    while size > 16:
        fnt = font("DejaVuSans-Bold.ttf", size)
        if d.textlength(tick, font=fnt) <= 920:
            break
        size -= 1
    tw = d.textlength(tick, font=fnt)
    d.text(((W - tw) / 2, 912), tick, font=fnt, fill=NAVY)

    # ---- Footer ----------------------------------------------------------
    foot = "The world news of Tuesday 24 November 2026, as reported today."
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, 972), foot, font=F_FOOT, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "entry.png")
    out = os.path.normpath(out)
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    render()
