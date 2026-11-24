#!/usr/bin/env python3
"""Draw the front page for the news-image entry.

This script paints a single newspaper page that sums up the world news
of Tuesday 24 November 2026. It uses Pillow and nothing else, touches
no network, uses no randomness and stamps no time anywhere, so every
run paints exactly the same pixels and writes exactly the same file.

How to run it, from the entry root:

    python3 tools/render.py

It writes entry.png next to the entry root (one level up from this
file). The program in main.ts then copies that file to the output
directory; this script is the part that actually draws the picture.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# --- Page geometry -------------------------------------------------------
# The whole page is a square, 1024 pixels on a side.
PAGE_W = 1024
PAGE_H = 1024
MARGIN = 36
RIGHT_EDGE = 988

# --- Palette -------------------------------------------------------------
# Every colour below is part of the page's look; changing any of them
# would change the picture, so they are fixed here in one place.
PAPER_BG = (251, 248, 241)
NAVY_BG = (16, 36, 62)
NAVY_LIGHT = (28, 58, 92)
GOLD_ACCENT = (201, 162, 39)
GOLD_PALE = (242, 230, 190)
TEXT_INK = (26, 26, 26)
TEXT_MUTED = (90, 90, 90)
CARD_BG = (255, 255, 255)
RULE_LINE = (210, 205, 195)
WHITE = (255, 255, 255)

# Story accent colours, one per grid story.
TEAL_ACCENT = (14, 124, 107)
GREEN_ACCENT = (26, 127, 55)
RED_ACCENT = (179, 38, 30)
ORANGE_ACCENT = (211, 84, 0)
SLATE_ACCENT = (91, 91, 122)

# Medallion tints, the pale fill behind each little icon.
TEAL_TINT = (224, 240, 236)
GREY_TINT = (244, 244, 244)

# --- Type ----------------------------------------------------------------
FONT_FOLDER = "/usr/share/fonts/truetype/dejavu"


def load_font(filename, points):
    """Load one DejaVu face at the given point size."""
    return ImageFont.truetype(os.path.join(FONT_FOLDER, filename), points)


# Type scale for the page, largest first.
TYPE = {
    "title": load_font("DejaVuSans-Bold.ttf", 58),
    "date": load_font("DejaVuSans-Bold.ttf", 30),
    "kicker": load_font("DejaVuSans-Bold.ttf", 21),
    "headline": load_font("DejaVuSans-Bold.ttf", 52),
    "summary": load_font("DejaVuSans.ttf", 26),
    "cell_kicker": load_font("DejaVuSans-Bold.ttf", 18),
    "cell_headline": load_font("DejaVuSans-Bold.ttf", 27),
    "cell_summary": load_font("DejaVuSans.ttf", 21),
    "ticker": load_font("DejaVuSans-Bold.ttf", 23),
    "footer": load_font("DejaVuSans.ttf", 18),
}


# --- Text helpers --------------------------------------------------------
def fit_lines(canvas, text, typeface, width_px):
    """Break text into lines no wider than width_px.

    Paragraphs are split on newlines first; within a paragraph words
    are added one at a time until the next word would overflow, then a
    new line starts. A single word wider than the limit still goes on
    its own line rather than being dropped.
    """
    fitted = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        current = ""
        for word in words:
            candidate = (current + " " + word).strip()
            if canvas.textlength(candidate, font=typeface) <= width_px or not current:
                current = candidate
            else:
                fitted.append(current)
                current = word
        if current:
            fitted.append(current)
    return fitted


def paint_lines(canvas, lines, typeface, x, y, colour, leading):
    """Paint lines of text top to bottom, returning the y below them."""
    cursor = y
    for line in lines:
        canvas.text((x, cursor), line, font=typeface, fill=colour)
        cursor += leading
    return cursor


def centred(canvas, text, typeface, y, colour):
    """Paint one line centred on the page at height y."""
    width = canvas.textlength(text, font=typeface)
    canvas.text(((PAGE_W - width) / 2, y), text, font=typeface, fill=colour)


# --- Icons ---------------------------------------------------------------
# Each glyph draws inside a medallion centred at (cx, cy). The radius
# argument is the medallion radius; the glyphs use it only where the
# original drawing did, and otherwise use fixed offsets, so the shapes
# come out exactly as drawn before.
def draw_medallion(canvas, cx, cy, radius, accent, tint, glyph):
    canvas.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=tint, outline=accent, width=4,
    )
    glyph(canvas, cx, cy, radius, accent)


def glyph_globe(canvas, cx, cy, radius, accent):
    span = int(radius * 0.62)
    canvas.ellipse(
        [cx - span, cy - span, cx + span, cy + span],
        outline=accent, width=5,
    )
    canvas.arc(
        [cx - span, cy - span, cx + span, cy + span],
        start=200, end=340, fill=accent, width=4,
    )
    canvas.ellipse(
        [cx - span, cy - int(span * 0.38), cx + span, cy + int(span * 0.38)],
        outline=accent, width=4,
    )
    canvas.line([cx, cy - span, cx, cy + span], fill=accent, width=4)
    # A crack across the top: the deal breaks.
    canvas.line(
        [(cx - 6, cy - span - 14), (cx + 8, cy - span + 6),
         (cx - 4, cy - span + 22)],
        fill=RED_ACCENT, width=5, joint="curve",
    )


def glyph_bars(canvas, cx, cy, radius, accent):
    baseline = cy + int(radius * 0.45)
    columns = [(-34, 22), (-10, 38), (14, 56)]
    for offset_x, height in columns:
        canvas.rectangle(
            [cx + offset_x, baseline - height, cx + offset_x + 16, baseline],
            fill=accent,
        )
    canvas.line(
        [(cx - 42, baseline - 66), (cx - 18, baseline - 44),
         (cx + 6, baseline - 52), (cx + 38, baseline - 78)],
        fill=accent, width=5, joint="curve",
    )
    canvas.polygon(
        [(cx + 38, baseline - 78), (cx + 24, baseline - 76),
         (cx + 36, baseline - 62)],
        fill=accent,
    )


def glyph_vessel(canvas, cx, cy, radius, accent):
    canvas.polygon(
        [(cx - 40, cy + 2), (cx + 40, cy + 2),
         (cx + 30, cy + 28), (cx - 30, cy + 28)],
        fill=accent,
    )
    canvas.rectangle([cx - 3, cy - 32, cx + 3, cy + 2], fill=accent)
    canvas.rectangle([cx + 3, cy - 32, cx + 24, cy - 16], fill=accent)
    canvas.line([(cx - 34, cy + 40), (cx + 34, cy + 40)], fill=accent, width=4)


def glyph_flame(canvas, cx, cy, radius, accent):
    outline = [
        (cx, cy - 52), (cx + 20, cy - 18), (cx + 34, cy + 4),
        (cx + 26, cy + 34), (cx + 8, cy + 48), (cx - 12, cy + 48),
        (cx - 30, cy + 30), (cx - 32, cy + 2), (cx - 18, cy - 22),
    ]
    canvas.polygon(outline, fill=accent)
    canvas.ellipse([cx - 10, cy + 6, cx + 12, cy + 38], fill=GOLD_ACCENT)


def glyph_towers(canvas, cx, cy, radius, accent):
    canvas.rectangle([cx - 40, cy - 20, cx - 8, cy + 40], fill=accent)
    canvas.rectangle([cx + 2, cy - 38, cx + 38, cy + 40], fill=accent)
    for win_x in (-32, -20):
        for win_y in (-10, 6, 22):
            canvas.rectangle(
                [cx + win_x, cy + win_y, cx + win_x + 6, cy + win_y + 6],
                fill=PAPER_BG,
            )
    for win_x in (10, 24):
        for win_y in (-28, -12, 4, 20):
            canvas.rectangle(
                [cx + win_x, cy + win_y, cx + win_x + 6, cy + win_y + 6],
                fill=PAPER_BG,
            )
    canvas.line([(cx - 40, cy + 40), (cx + 38, cy + 40)], fill=accent, width=4)
    canvas.line(
        [(cx + 2, cy - 38), (cx + 16, cy - 52), (cx + 30, cy - 38)],
        fill=RED_ACCENT, width=5, joint="curve",
    )


# --- Page sections -------------------------------------------------------
def paint_masthead(canvas):
    """Navy banner with the paper's name and the date it sums up."""
    canvas.rectangle([0, 0, PAGE_W, 116], fill=NAVY_BG)
    centred(canvas, "THE WORLD IN ONE DAY", TYPE["title"], 14, WHITE)
    centred(canvas, "TUESDAY, 24 NOVEMBER 2026", TYPE["date"], 76, GOLD_ACCENT)
    canvas.rectangle([0, 116, PAGE_W, 120], fill=GOLD_ACCENT)


def paint_lead_story(canvas):
    """The lead story: COP31 collapses in Antalya, no deal."""
    left = MARGIN
    canvas.text(
        (left, 140), "CLIMATE  •  ANTALYA, TURKEY",
        font=TYPE["kicker"], fill=TEAL_ACCENT,
    )
    draw_medallion(canvas, 118, 288, 74, TEAL_ACCENT, TEAL_TINT, glyph_globe)
    canvas.text((226, 176), "COP31 COLLAPSES", font=TYPE["headline"], fill=NAVY_BG)
    first_para = (
        "The UN climate summit ends with no deal — the longest COP ever — "
        "as nations split over fossil fuels."
    )
    bottom = paint_lines(
        canvas,
        fit_lines(canvas, first_para, TYPE["summary"], 724),
        TYPE["summary"], 226, 246, TEXT_INK, 34,
    )
    second_para = (
        "The EU and UK reject a pact that never mentions oil, coal or gas."
    )
    paint_lines(
        canvas,
        fit_lines(canvas, second_para, TYPE["summary"], 724),
        TYPE["summary"], 226, bottom + 6, TEXT_MUTED, 34,
    )
    # A thin rule separates the lead story from the grid below it.
    canvas.line([(36, 408), (988, 408)], fill=RULE_LINE, width=2)


# The four grid stories, in reading order: markets, Ukraine war,
# Indonesia, Gaza. Each entry carries its kicker, accent colour, glyph,
# headline and summary exactly as researched for 24 November 2026.
GRID_STORIES = [
    {
        "kicker": "MARKETS  •  NEW YORK",
        "accent": GREEN_ACCENT,
        "glyph": glyph_bars,
        "headline": "Huang returns, Nvidia soars 31%",
        "summary": (
            "Shares jump and the Nasdaq climbs 6.5% as Jensen Huang is "
            "reinstated as chief executive."
        ),
    },
    {
        "kicker": "UKRAINE WAR  •  AT SEA",
        "accent": RED_ACCENT,
        "glyph": glyph_vessel,
        "headline": "Russian ships hit off Libya and Finland",
        "summary": (
            "Kyiv claims a warship sunk near Benghazi; a cargo vessel burns "
            "after a drone strike."
        ),
    },
    {
        "kicker": "INDONESIA  •  BANTEN",
        "accent": ORANGE_ACCENT,
        "glyph": glyph_flame,
        "headline": "24 dead in candy factory fire",
        "summary": (
            "Rescuers search the wreckage for about 30 workers still missing "
            "after the weekend blaze."
        ),
    },
    {
        "kicker": "GAZA",
        "accent": SLATE_ACCENT,
        "glyph": glyph_towers,
        "headline": "Strikes kill UN worker and others",
        "summary": (
            "Israeli strikes hit Gaza as settler arson in the West Bank draws "
            "condemnation."
        ),
    },
]


def paint_story_grid(canvas):
    """Four stories in a two-by-two grid below the lead."""
    cell_w, cell_h, gap = 468, 216, 16
    top = 428
    for index, story in enumerate(GRID_STORIES):
        col = index % 2
        row = index // 2
        x0 = MARGIN + col * (cell_w + gap)
        y0 = top + row * (cell_h + gap)
        accent = story["accent"]
        canvas.rectangle(
            [x0, y0, x0 + cell_w, y0 + cell_h],
            fill=CARD_BG, outline=RULE_LINE, width=2,
        )
        canvas.rectangle([x0, y0, x0 + cell_w, y0 + 6], fill=accent)
        draw_medallion(
            canvas, x0 + 62, y0 + 62, 42, accent, GREY_TINT, story["glyph"],
        )
        text_x = x0 + 122
        canvas.text(
            (text_x, y0 + 18), story["kicker"],
            font=TYPE["cell_kicker"], fill=accent,
        )
        headline_lines = fit_lines(
            canvas, story["headline"], TYPE["cell_headline"], cell_w - 140,
        )
        after_headline = paint_lines(
            canvas, headline_lines, TYPE["cell_headline"],
            text_x, y0 + 46, NAVY_BG, 32,
        )
        paint_lines(
            canvas,
            fit_lines(canvas, story["summary"], TYPE["cell_summary"], cell_w - 140),
            TYPE["cell_summary"], text_x, after_headline + 4, TEXT_INK, 26,
        )


def paint_sport_strip(canvas):
    """A gold ticker with the day's sport: Alcaraz, and chess in Geneva."""
    canvas.rectangle(
        [36, 892, 988, 952], fill=GOLD_PALE, outline=GOLD_ACCENT, width=2,
    )
    ticker = (
        "SPORT — Alcaraz wins first ATP Finals title  •  "
        "Chess title match opens in Geneva"
    )
    # Shrink the ticker type until it fits the strip, one point at a time.
    size = 23
    while size > 16:
        face = load_font("DejaVuSans-Bold.ttf", size)
        if canvas.textlength(ticker, font=face) <= 920:
            break
        size -= 1
    centred(canvas, ticker, face, 912, NAVY_BG)


def paint_footer(canvas):
    """One quiet line under the ticker, naming the day again."""
    centred(
        canvas,
        "The world news of Tuesday 24 November 2026, as reported today.",
        TYPE["footer"], 972, TEXT_MUTED,
    )


# --- Entry point ---------------------------------------------------------
def build_front_page():
    """Paint the whole page and return the finished image."""
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER_BG)
    canvas = ImageDraw.Draw(page)
    paint_masthead(canvas)
    paint_lead_story(canvas)
    paint_story_grid(canvas)
    paint_sport_strip(canvas)
    paint_footer(canvas)
    return page


def output_path():
    """The entry.png beside the entry root (this file's parent's parent)."""
    here = os.path.dirname(os.path.abspath(__file__))
    joined = os.path.join(here, "..", "entry.png")
    return os.path.normpath(joined)


def main():
    page = build_front_page()
    destination = output_path()
    page.save(destination, "PNG")
    print("wrote", destination, os.path.getsize(destination), "bytes")


if __name__ == "__main__":
    main()
