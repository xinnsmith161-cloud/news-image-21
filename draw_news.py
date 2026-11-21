#!/usr/bin/env python3
"""Draw the front page of The World for Saturday, 21 November 2026.

A one-day newspaper: masthead, one lead story, five smaller stories and an
in-brief strip. Every headline names an event reported on 21 November 2026.
Run: python3 draw_news.py  ->  writes entry.png beside this file.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (17, 17, 17)
RED = (163, 22, 33)
GREY = (90, 83, 72)
RULE = (17, 17, 17)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(lines, fnt, x0, x1, y, fill, leading):
    for line in lines:
        lw = d.textlength(line, font=fnt)
        d.text(((x0 + x1 - lw) / 2, y), line, font=fnt, fill=fill)
        y += leading
    return y


def block(kicker, headline, deck, x0, x1, y, ksize, hsize, dsize, align="left"):
    f_k = font(SANS_B, ksize)
    f_h = font(SERIF_B, hsize)
    f_d = font(SANS, dsize)
    max_w = x1 - x0
    if align == "center":
        d.text(((x0 + x1 - d.textlength(kicker, font=f_k)) / 2, y), kicker,
               font=f_k, fill=RED)
    else:
        d.text((x0, y), kicker, font=f_k, fill=RED)
    y += ksize + 8
    hlines = wrap(headline, f_h, max_w)
    for line in hlines:
        if align == "center":
            d.text(((x0 + x1 - d.textlength(line, font=f_h)) / 2, y), line,
                   font=f_h, fill=INK)
        else:
            d.text((x0, y), line, font=f_h, fill=INK)
        y += hsize + 6
    y += 2
    dlines = wrap(deck, f_d, max_w)
    for line in dlines:
        if align == "center":
            d.text(((x0 + x1 - d.textlength(line, font=f_d)) / 2, y), line,
                   font=f_d, fill=INK)
        else:
            d.text((x0, y), line, font=f_d, fill=INK)
        y += dsize + 6
    return y


def rule(y, weight=2, x0=48, x1=W - 48):
    d.line([(x0, y), (x1, y)], fill=RULE, width=weight)


# ---- masthead ----
M = 48
mast = font(SERIF_B, 96)
title = "The World"
tw = d.textlength(title, font=mast)
d.text(((W - tw) / 2, 18), title, font=mast, fill=INK)
rule(128, 3)
date_f = font(SANS_B, 25)
dateline = "Saturday, 21 November 2026"
dw = d.textlength(dateline, font=date_f)
d.text(((W - dw) / 2, 138), dateline, font=date_f, fill=INK)
small = font(SANS, 16)
d.text((M, 141), "ONE DAY, WHOLE WORLD", font=small, fill=GREY)
right = "LATE EDITION"
d.text((W - M - d.textlength(right, font=small), 141), right, font=small,
       fill=GREY)
rule(176, 2)

# ---- lead story ----
y = block(
    "WAR IN EUROPE",
    "Russian missiles strike Kyiv, and land in Poland",
    "More than 400 drones and 110 missiles hit Ukraine overnight, killing "
    "at least eight in Kyiv and damaging bridges and rail. Warsaw says two "
    "missiles and a suspected drone fell on Polish soil, and calls it a "
    "deliberate provocation.",
    M, W - M, 196, 20, 47, 22, align="center")
rule(y + 8, 2)
y += 24

# ---- row A: two stories ----
col_w = (W - 2 * M - 28) // 2
left = (M, M + col_w)
right = (M + col_w + 28, W - M)
yA = y
end_l = block(
    "CLIMATE  |  ANTALYA",
    "Climate talks run into overtime as fossil fuels vanish from draft",
    "COP31 goes a day past its deadline after a new text drops every "
    "mention of oil, gas and coal. A third draft is due on Saturday.",
    left[0], left[1], yA, 16, 28, 18)
end_r = block(
    "MIDDLE EAST  |  RIYADH",
    "Three missiles at Riyadh stopped on third night of alerts",
    "Saudi defences intercept Houthi ballistic missiles over the capital "
    "before dawn. No casualties are reported; alerts sounded a third "
    "night running.",
    right[0], right[1], yA, 16, 28, 18)
y = max(end_l, end_r)
d.line([(W // 2, yA + 4), (W // 2, y - 8)], fill=(180, 172, 155), width=1)
rule(y + 6, 1)
y += 24

# ---- row B: three stories ----
third_w = (W - 2 * M - 2 * 24) // 3
cols = [(M + i * (third_w + 24), M + i * (third_w + 24) + third_w)
        for i in range(3)]
yB = y
ends = []
ends.append(block(
    "DISASTER  |  PERU",
    "6.7 quake shakes Peru, felt in Lima",
    "The tremor strikes near Junin at 7:09 p.m. local time. No deaths are "
    "reported; homes are damaged and roads blocked by rockfalls.",
    cols[0][0], cols[0][1], y, 15, 25, 17))
ends.append(block(
    "MARKETS  |  NEW YORK",
    "AI sell-off pushes Wall Street into correction",
    "The S&P 500 falls 3.7% and the Nasdaq wipes out its 2026 gains as "
    "Anthropic shares slide days after a $2 trillion debut.",
    cols[1][0], cols[1][1], y, 15, 25, 17))
ends.append(block(
    "HEALTH  |  BARCELONA",
    "Cancer pill shrinks tumours in 6 of 10 patients",
    "In a small early trial, daraxonrasib with chemotherapy leaves "
    "tumours undetectable in one in 12 patients. Larger trials await.",
    cols[2][0], cols[2][1], y, 15, 25, 17))
y = max(ends)
for cx in (cols[1][0] - 12, cols[2][0] - 12):
    d.line([(cx, yB + 4), (cx, y - 6)],
           fill=(180, 172, 155), width=1)
rule(y + 6, 1)
y += 14

# ---- in brief strip ----
brief_f = font(SANS_B, 17)
d.text((M, y), "IN BRIEF", font=brief_f, fill=RED)
by = y + 26
brief_lines = [
    "Iran says it downed a 58th U.S. MQ-9 drone over the Strait of Hormuz; "
    "the U.S. has not confirmed the claim.",
    "Britain and the EU sign post-Brexit deals on food trade, carbon "
    "markets and youth mobility.",
]
bf = font(SANS, 17)
for line in brief_lines:
    d.text((M + 14, by), "\u2022  " + line, font=bf, fill=INK)
    by += 25

# ---- footer ----
rule(H - 56, 2)
foot = font(SANS, 14)
note = ("Sources: Reuters, Associated Press, Al Jazeera, BBC, Financial "
        "Times, The Guardian, Medindia  |  Drawn for 21 November 2026")
fw = d.textlength(note, font=foot)
d.text(((W - fw) / 2, H - 40), note, font=foot, fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
