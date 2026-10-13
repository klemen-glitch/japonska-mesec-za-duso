#!/usr/bin/env python3
"""Ikone za potovanje Zmajeva pustolovščina: zmaj (emoji) na zeleni podlagi."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "lj_icons")
os.makedirs(OUT, exist_ok=True)
G1, G2 = (47, 143, 107), (22, 92, 70)

font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 160)
em = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
ImageDraw.Draw(em).text((20, 20), "🐉", font=font, embedded_color=True)
bbox = em.getbbox()
em = em.crop(bbox)


def icon(size, rounded=True):
    bg = Image.new("RGBA", (size, size))
    d = ImageDraw.Draw(bg)
    for y in range(size):
        t = y / size
        d.line([(0, y), (size, y)], fill=tuple(int(G1[i] + (G2[i] - G1[i]) * t) for i in range(3)) + (255,))
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    if rounded:
        m = Image.new("L", (size, size), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * 0.22), fill=255)
        img.paste(bg, (0, 0), m)
    else:
        img.paste(bg, (0, 0))
    w = int(size * 0.62)
    e = em.resize((w, int(w * em.height / em.width)), Image.LANCZOS)
    img.alpha_composite(e, ((size - e.width) // 2, (size - e.height) // 2))
    return img


for size, name, rounded in [(512, "icon-512.png", True), (192, "icon-192.png", True), (180, "apple-touch-icon.png", False)]:
    icon(size, rounded).save(os.path.join(OUT, name))
    print("written", name)

open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="22" fill="#2f8f6b"/>'
    '<text x="50" y="68" font-size="58" text-anchor="middle">🐉</text></svg>')
