#!/usr/bin/env python3
"""Generate PWA icons: torii gate on a bordo rounded square."""
import os
from PIL import Image, ImageDraw

OUT = "/Users/klemenlorber/Library/Mobile Documents/com~apple~CloudDocs/Japonska/japonska-2026-stran/icons"
os.makedirs(OUT, exist_ok=True)

BORDO = (123, 34, 48, 255)
BORDO_DARK = (94, 26, 37, 255)
CREAM = (251, 243, 226, 255)
GOLD = (216, 169, 78, 255)


def draw_icon(size, rounded=True):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size / 512.0  # scale helper

    # background: vertical gradient bordo -> bordo_dark
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bgd = ImageDraw.Draw(bg)
    for y in range(size):
        t = y / size
        col = tuple(int(BORDO[i] + (BORDO_DARK[i] - BORDO[i]) * t) for i in range(3)) + (255,)
        bgd.line([(0, y), (size, y)], fill=col)
    if rounded:
        mask = Image.new("L", (size, size), 0)
        md = ImageDraw.Draw(mask)
        md.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * 0.22), fill=255)
        img.paste(bg, (0, 0), mask)
    else:
        img.paste(bg, (0, 0))
    d = ImageDraw.Draw(img)

    # gold sun disc behind torii
    cx, cy, r = 256 * s, 208 * s, 150 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(GOLD[0], GOLD[1], GOLD[2], 70))

    # torii gate in cream
    def rect(x0, y0, x1, y1, fill=CREAM):
        d.rectangle([x0 * s, y0 * s, x1 * s, y1 * s], fill=fill)

    # kasagi (top beam, slightly curved ends via polygon)
    d.polygon([
        (76 * s, 150 * s), (436 * s, 150 * s),
        (444 * s, 118 * s), (256 * s, 132 * s), (68 * s, 118 * s),
    ], fill=CREAM)
    # shimaki (second beam)
    rect(96, 158, 416, 186)
    # nuki (lower beam)
    rect(112, 240, 400, 268)
    # gakuzuka (center strut)
    rect(242, 186, 270, 240)
    # pillars (slightly inclined)
    d.polygon([(128 * s, 158 * s), (168 * s, 158 * s), (178 * s, 420 * s), (138 * s, 420 * s)], fill=CREAM)
    d.polygon([(344 * s, 158 * s), (384 * s, 158 * s), (374 * s, 420 * s), (334 * s, 420 * s)], fill=CREAM)

    return img


for size, name, rounded in [
    (512, "icon-512.png", True),
    (192, "icon-192.png", True),
    (180, "apple-touch-icon.png", False),  # iOS zaobli sam
]:
    draw_icon(size, rounded).save(os.path.join(OUT, name))
    print("written", name)
