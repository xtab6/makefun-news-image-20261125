#!/usr/bin/env python3
"""news-image-20261125: one front-page image summing up 25 November 2026.

Deterministic PIL render (no network, no clock, no randomness): the program
writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png), 1024x1024 PNG.
Run twice -> byte-identical output.

Headlines verified 25 Nov 2026 (Reuters world-news summary; AP/Reuters via
the day's roundups): Ukraine confirms the Gulf of Finland ship strike;
Houthi drone hits Riyadh's tallest tower; the AI-stock sell-off; Pakistan's
first astronaut aboard Shenzhou-24; the Gaza strike; Hasina's planned return;
the Rohingya returns; AIDS deaths at a 20-year low; the Nepal quake; the
Giuliani Medal of Freedom.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
BASE = os.path.dirname(os.path.abspath(__file__))

# Palette: newsprint cream, navy ink, gold rule, brick red accents.
CREAM = (247, 243, 234)
PAPER = (252, 250, 244)
NAVY = (20, 36, 62)
NAVY_LT = (38, 62, 96)
GOLD = (196, 154, 60)
RED = (178, 44, 36)
TEAL = (31, 78, 121)
TEAL_LT = (58, 110, 150)
LAND = (216, 196, 138)
LAND2 = (146, 178, 120)
INK = (26, 26, 26)
GREY = (96, 96, 96)
RULE = (180, 172, 152)

F_SERIF_B = os.path.join(BASE, "fonts", "DejaVuSerif-Bold.ttf")
F_SANS_B = os.path.join(BASE, "fonts", "DejaVuSans-Bold.ttf")
F_SANS = os.path.join(BASE, "fonts", "DejaVuSans.ttf")


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading if leading is not None else int(fnt.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def fit_line(draw, text, fnt, max_w):
    """Longest leading prefix of words that fits max_w (single line)."""
    words = text.split()
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            break
    return cur


def draw_globe(img, draw, cx, cy, r):
    """Stylised globe: ocean disc, abstract continents, graticule, pins."""
    # Ocean disc on its own layer so land is clipped to the circle.
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(layer)
    g.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL + (255,))
    # Abstract continent blobs (fractions of r, x right / y down from centre).
    blobs = [
        ([(-0.92, -0.30), (-0.78, -0.72), (-0.42, -0.78), (-0.30, -0.55),
          (-0.48, -0.38), (-0.62, -0.18), (-0.86, -0.05)], LAND),
        ([(-0.55, 0.05), (-0.42, 0.28), (-0.28, 0.62), (-0.12, 0.55),
          (-0.18, 0.25), (-0.38, 0.12)], LAND2),
        ([(0.02, -0.28), (0.18, -0.42), (0.34, -0.30), (0.30, -0.02),
          (0.16, 0.12), (0.02, -0.05)], LAND),
        ([(0.38, -0.72), (0.62, -0.80), (0.88, -0.62), (0.92, -0.30),
          (0.70, -0.18), (0.52, -0.38), (0.40, -0.55)], LAND),
        ([(0.62, 0.28), (0.78, 0.22), (0.86, 0.42), (0.72, 0.52),
          (0.60, 0.42)], LAND2),
        ([(0.05, 0.45), (0.22, 0.55), (0.30, 0.75), (0.14, 0.82),
          (0.02, 0.62)], LAND),
    ]
    for pts, col in blobs:
        g.polygon([(cx + px * r, cy + py * r) for px, py in pts], fill=col + (255,))
    # Graticule: vertical ellipses + horizontal chords.
    for k in (-0.55, 0.0, 0.55):
        g.ellipse([cx + k * r - int(0.42 * r), cy - r, cx + k * r + int(0.42 * r),
                   cy + r], outline=(255, 255, 255, 70), width=2)
    for k in (-0.55, 0.0, 0.55):
        yy = cy + k * r
        half = int((r * r - (k * r) ** 2) ** 0.5)
        g.line([cx - half, yy, cx + half, yy], fill=(255, 255, 255, 70), width=2)
    # Pins: (label, fx, fy) for the four mapped stories.
    pins = [("1", 0.10, -0.62), ("2", 0.30, 0.05), ("3", 0.62, -0.22),
            ("4", -0.72, -0.12)]
    pin_fnt = font(F_SANS_B, 20)
    for label, fx, fy in pins:
        px, py = cx + fx * r, cy + fy * r
        g.ellipse([px - 13, py - 13, px + 13, py + 13], fill=RED + (255,),
                  outline=(255, 255, 255, 255), width=2)
        tw = g.textlength(label, font=pin_fnt)
        g.text((px - tw / 2, py - 11), label, font=pin_fnt,
               fill=(255, 255, 255, 255))
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    img.paste(layer, (0, 0), mask)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=4)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    mast = font(F_SERIF_B, 64)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 10), title, font=mast, fill=(255, 255, 255))
    sub = font(F_SANS_B, 19)
    sub_t = "WEDNESDAY, 25 NOVEMBER 2026  ·  WORLD NEWS IN ONE IMAGE"
    sw = d.textlength(sub_t, font=sub)
    d.text(((W - sw) / 2, 84), sub_t, font=sub, fill=GOLD)
    d.rectangle([0, 118, W, 122], fill=GOLD)

    # ---- Hero: globe left, lead stories right ---------------------------
    hero_y, hero_h = 138, 352
    d.rectangle([24, hero_y, 616, hero_y + hero_h], fill=PAPER,
                outline=RULE, width=2)
    draw_globe(img, d, 320, hero_y + 138, 128)
    cap = font(F_SANS_B, 15)
    for i, cap_t in enumerate(("ONE DAY, ONE PLANET",
                               "THE STORIES THAT MOVED THE WORLD")):
        cw = d.textlength(cap_t, font=cap)
        d.text((320 - cw / 2, hero_y + 284 + i * 20), cap_t, font=cap,
               fill=NAVY)
    leg_f = font(F_SANS, 14)
    leg_t = "1 Gulf of Finland   2 Riyadh   3 Tiangong   4 Washington"
    lw = d.textlength(leg_t, font=leg_f)
    d.text((320 - lw / 2, hero_y + 326), leg_t, font=leg_f, fill=GREY)

    # Lead story block (right of globe).
    x0 = 640
    d.text((x0, hero_y + 6), "LEAD STORY — UKRAINE",
           font=font(F_SANS_B, 17), fill=RED)
    y = draw_wrapped(d, x0, hero_y + 32,
                     "Kyiv confirms drone strike on Russian cargo ship",
                     font(F_SERIF_B, 27), 336, NAVY, leading=32)
    y = draw_wrapped(d, x0, y + 8,
                     "Zelenskiy owns Saturday's Gulf of Finland attack; ally "
                     "Norway urges caution in such operations.",
                     font(F_SANS, 16), 336, INK, leading=20) + 10
    d.line([x0, y, 1000, y], fill=RULE, width=2)
    y += 12
    d.text((x0, y), "MIDDLE EAST — RIYADH", font=font(F_SANS_B, 17), fill=RED)
    y = draw_wrapped(d, x0, y + 26,
                     "Houthi drone hits Riyadh's tallest tower",
                     font(F_SERIF_B, 23), 336, NAVY, leading=28)
    draw_wrapped(d, x0, y + 6,
                 "Eleven wounded, Saudi civil defence says, as Yemen's war "
                 "spills over.",
                 font(F_SANS, 15), 336, INK, leading=19)

    # ---- Story grid: 2 columns x 4 rows ---------------------------------
    stories = [
        ("1", "MARKETS",
         "AI trade collapses as tariff fears hit Wall Street",
         "Nasdaq -1.5%, Nvidia -6%, Micron -11%; the Dow rose 0.8%."),
        ("2", "SPACE",
         "Pakistan's first astronaut lifts off to Tiangong",
         "Zeeshan Ali aboard Shenzhou-24 — a first for Pakistan."),
        ("3", "GAZA",
         "Strike kills Hamas security chief in Gaza City",
         "Naeem Abu Nahel among at least seven Palestinians killed Tuesday."),
        ("4", "BANGLADESH",
         "Hasina plans return from exile on 16 December",
         "Ousted PM to come home on Victory Day, spokesperson says."),
        ("5", "MYANMAR",
         "Malaysia to send 6,500 Rohingya back in December",
         "Five days after the ICJ's genocide ruling on Myanmar."),
        ("6", "HEALTH",
         "AIDS deaths fall to 570,000, lowest in 20 years",
         "But HIV funding fell 18% — and US funding 26%, UNAIDS warns."),
        ("7", "NEPAL",
         "Magnitude 5.6 quake shakes Koshi near Tibet",
         "Tremor struck eastern Nepal on Tuesday morning."),
        ("8", "USA",
         "Trump awards Giuliani the Medal of Freedom",
         "Former New York mayor honoured at the White House."),
    ]
    grid_y, grid_h = 502, 428
    col_w, row_h = 476, 107
    badge_f = font(F_SANS_B, 18)
    kick_f = font(F_SANS_B, 15)
    head_f = font(F_SERIF_B, 20)
    deck_f = font(F_SANS, 13)
    for i, (num, kicker, head, deck) in enumerate(stories):
        col, row = i % 2, i // 2
        gx = 24 + col * (col_w + 24)
        gy = grid_y + row * row_h
        d.rectangle([gx, gy, gx + col_w, gy + row_h - 8], fill=PAPER,
                    outline=RULE, width=1)
        d.ellipse([gx + 12, gy + 12, gx + 40, gy + 40], fill=RED)
        tw = d.textlength(num, font=badge_f)
        d.text((gx + 26 - tw / 2, gy + 15), num, font=badge_f,
               fill=(255, 255, 255))
        d.text((gx + 52, gy + 10), kicker, font=kick_f, fill=RED)
        draw_wrapped(d, gx + 52, gy + 32, head, head_f, col_w - 64, NAVY,
                     leading=23)
        d.text((gx + 12, gy + 78), fit_line(d, deck, deck_f, col_w - 24),
               font=deck_f, fill=INK)

    # ---- Footer ticker ----------------------------------------------------
    fy = 940
    d.rectangle([0, fy, W, H], fill=NAVY)
    tick_f = font(F_SANS_B, 16)
    tick = ("ALSO TODAY:  EU unveils new Russia sanctions  ·  Sarkozy corruption "
            "case to trial  ·  NATO jets for Poland  ·  Russian jets enter Korea's "
            "air zone  ·  UAE crash toll rises to 13  ·  GTA 6 out worldwide")
    lines = wrap(d, tick, tick_f, W - 48)
    yy = fy + 12
    for ln in lines:
        d.text((24, yy), ln, font=tick_f, fill=(255, 255, 255))
        yy += 22

    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
