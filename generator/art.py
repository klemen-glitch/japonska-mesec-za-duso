# -*- coding: utf-8 -*-
"""Ročno izdelane SVG ilustracije za vsako lokacijo (jesenske barve).
Vsaka scena je samostojen <svg>, gradienti imajo ključ lokacije v ID-ju,
da se pri več scenah na isti strani (kartice) ne prekrivajo."""

W, H = 1200, 460

# paleta
CREAM = "#fbf5ea"
GOLD = "#d8a94e"
GOLD_DK = "#b9832c"
ORANGE = "#c96a2a"
BORDO = "#7b2230"
BORDO_DK = "#5e1a25"
INK = "#3a2a20"
VERM = "#c24a3a"        # vermiljon (torii, pagode)
VERM_DK = "#8f3128"
SEA = "#3f7480"
SEA_DK = "#2c5560"
SEA_LT = "#7fb0b3"
FOREST = "#436e4c"
FOREST_DK = "#2d4c37"
MOSS = "#6f9256"
STONE = "#8a8478"
NIGHT = "#3c3357"

LEAF_COLORS = [BORDO, ORANGE, GOLD, "#a8402c"]

ALT = {
    "tokio": "Ilustracija Tokia: Tokijski stolp in mesto v jesenskem soncu",
    "chichibu": "Ilustracija gozdnatih gora in svetišča v narodnem parku Chichibu",
    "kawaguchiko": "Ilustracija gore Fuji nad jezerom Kawaguchi z jesenskimi javorji",
    "minobusan": "Ilustracija gorskega templja in pagode na gori Minobu",
    "izu": "Ilustracija obale polotoka Izu z valovi in soncem nad morjem",
    "kumano": "Ilustracija velikih torijev in gora romarske poti Kumano Kodo",
    "koyasan": "Ilustracija pagode in kamnitih luči na sveti gori Koya-san",
    "iya": "Ilustracija visečega mostu iz trte nad sotesko v dolini Iya",
    "ine": "Ilustracija ribiške vasice Ine s hišami funaya nad vodo",
    "nara": "Ilustracija templja Todai-ji z jelenom in jesenskimi javorji v Nari",
    "kyoto": "Ilustracija pagode med jesenskimi javorji v Kjotu",
    "osaka": "Ilustracija gradu Osaka in mestne panorame ob mraku",
    "hiroshima": "Ilustracija plavajoče torije svetišča Itsukušima na otoku Miyajima",
}


# ---------------------------------------------------------------- pomožne oblike

def _leaf(cx, cy, s, rot, color, op=1.0):
    d = ("M50 4 C53 22 65 20 69 15 C65 27 71 31 85 29 C75 37 79 45 83 51 "
         "C73 51 71 59 75 69 C65 63 59 67 57 79 L54 98 L46 98 L43 79 "
         "C41 67 35 63 25 69 C29 59 27 51 17 51 C21 45 25 37 15 29 "
         "C29 31 35 27 31 15 C35 20 47 22 50 4 Z")
    return (f'<g transform="translate({cx},{cy}) rotate({rot}) scale({s}) translate(-50,-50)" '
            f'opacity="{op}"><path d="{d}" fill="{color}"/>'
            f'<path d="M50 40 L50 98" stroke="{BORDO_DK}" stroke-width="2.5" opacity="0.35"/></g>')


def _leaves(spec):
    return "".join(_leaf(*s) for s in spec)


def _sun(cx, cy, r, color, op=0.9):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="{op}"/>'


def _mtn(pts, color, op=1.0):
    p = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polygon points="{p}" fill="{color}" opacity="{op}"/>'


def _cedar(x, base, h, color):
    w = h * 0.42
    t = (f'<rect x="{x-2}" y="{base-h*0.18}" width="4" height="{h*0.2}" fill="{BORDO_DK}"/>')
    tiers = ""
    for i, f in enumerate((1.0, 0.78, 0.54, 0.3)):
        ty = base - h * 0.15 - (h * 0.75) * (i / 4.0)
        tw = w * f
        th = h * 0.32
        tiers += _mtn([(x - tw / 2, ty), (x + tw / 2, ty), (x, ty - th)], color)
    return t + tiers


def _torii(x, base, h, color, dark):
    w = h * 0.82
    post = h * 0.09
    top_y = base - h
    parts = [
        f'<rect x="{x-w/2}" y="{top_y}" width="{post}" height="{h}" fill="{color}"/>',
        f'<rect x="{x+w/2-post}" y="{top_y}" width="{post}" height="{h}" fill="{color}"/>',
        f'<rect x="{x-w/2-post*0.7}" y="{top_y+h*0.22}" width="{w+post*1.4}" height="{h*0.075}" fill="{color}"/>',
    ]
    kw = w + post * 2.4
    ky = top_y - h * 0.02
    parts.append(
        f'<path d="M{x-kw/2} {ky+h*0.09} Q{x} {ky-h*0.04} {x+kw/2} {ky+h*0.09} '
        f'L{x+kw/2} {ky+h*0.02} Q{x} {ky-h*0.11} {x-kw/2} {ky+h*0.02} Z" fill="{dark}"/>')
    parts.append(f'<rect x="{x-post*0.7}" y="{top_y+h*0.03}" width="{post*1.4}" height="{h*0.2}" fill="{dark}"/>')
    return "".join(parts)


def _pagoda(x, base, h, color, dark):
    w = h * 0.62
    parts = [f'<rect x="{x-w*0.09}" y="{base-h}" width="{w*0.18}" height="{h*0.05}" fill="{dark}"/>']  # finial
    parts.append(f'<circle cx="{x}" cy="{base-h}" r="{w*0.05}" fill="{GOLD}"/>')
    tiers = 5
    for i in range(tiers):
        f = 0.5 + 0.5 * (i / (tiers - 1))
        tw = w * f
        ty = base - h * 0.93 + (h * 0.9) * (i / tiers)
        bh = h * 0.9 / tiers
        # body
        parts.append(f'<rect x="{x-tw*0.34}" y="{ty}" width="{tw*0.68}" height="{bh*0.72}" fill="{color}"/>')
        # roof
        rw = tw * 1.05
        parts.append(
            f'<path d="M{x-rw/2} {ty} Q{x-rw*0.3} {ty-bh*0.5} {x} {ty-bh*0.42} '
            f'Q{x+rw*0.3} {ty-bh*0.5} {x+rw/2} {ty} Z" fill="{dark}"/>')
    return "".join(parts)


def _waves(y, color, op=1.0):
    step = 120
    d = f"M0 {y}"
    x = 0
    up = True
    while x < W:
        d += f" Q{x+step/2} {y-(16 if up else -16)} {x+step} {y}"
        x += step
        up = not up
    d += f" L{W} {H} L0 {H} Z"
    return f'<path d="{d}" fill="{color}" opacity="{op}"/>'


def _house(x, base, w, h, roof, wall):
    return (f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" fill="{wall}"/>'
            f'<path d="M{x-w*0.1} {base-h} L{x+w/2} {base-h-h*0.5} L{x+w*1.1} {base-h} Z" fill="{roof}"/>'
            f'<rect x="{x+w*0.3}" y="{base-h*0.6}" width="{w*0.4}" height="{h*0.4}" fill="{BORDO_DK}" opacity="0.5"/>')


def _defs(key, sky_top, sky_bot):
    return (f'<defs><linearGradient id="sky-{key}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{sky_top}"/>'
            f'<stop offset="1" stop-color="{sky_bot}"/></linearGradient></defs>')


def _open(key, sky_top, sky_bot):
    return (f'<svg class="scene-svg" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="{ALT[key]}" xmlns="http://www.w3.org/2000/svg" '
            f'preserveAspectRatio="xMidYMid slice">'
            f'{_defs(key, sky_top, sky_bot)}'
            f'<rect width="{W}" height="{H}" fill="url(#sky-{key})"/>')


# ------------------------------------------------------------------- scene po lokaciji

def _tokio():
    s = _open("tokio", "#f7d59c", "#fbe4cf")
    s += _sun(940, 150, 78, "#f3a94e", 0.85)
    s += _mtn([(0, 330), (250, 250), (520, 320), (800, 250), (1000, 300), (1200, 260), (1200, 460), (0, 460)], "#e9b877")
    # mesto
    city = ""
    xs = [(120, 150, 70), (200, 120, 90), (300, 190, 60), (620, 160, 80),
          (720, 210, 70), (1040, 140, 90), (1130, 100, 70)]
    for x, ht, w in xs:
        city += f'<rect x="{x}" y="{360-ht}" width="{w}" height="{ht}" fill="#9c5a3c"/>'
    s += city
    # Skytree (stožčast stolp z jamborjem)
    sx = 475
    s += (f'<polygon points="{sx-3},150 {sx+3},150 {sx+15},360 {sx-15},360" fill="#8a5a42"/>'
          f'<polygon points="{sx-9},250 {sx+9},250 {sx+15},360 {sx-15},360" fill="{VERM_DK}" opacity="0.25"/>'
          f'<rect x="{sx-1.5}" y="72" width="3" height="80" fill="#8a5a42"/>'
          f'<circle cx="{sx}" cy="150" r="9" fill="{ORANGE}"/>')
    # Tokijski stolp
    tx = 850
    s += (f'<polygon points="{tx},130 {tx-46},360 {tx+46},360" fill="{VERM}"/>'
          f'<polygon points="{tx},130 {tx-30},260 {tx+30},260" fill="{VERM_DK}" opacity="0.35"/>'
          f'<rect x="{tx-46}" y="300" width="92" height="10" fill="{VERM_DK}"/>'
          f'<rect x="{tx-30}" y="250" width="60" height="9" fill="{VERM_DK}"/>'
          f'<rect x="{tx-6}" y="96" width="12" height="40" fill="{VERM_DK}"/>')
    s += f'<rect x="0" y="360" width="{W}" height="100" fill="#a86a44"/>'
    s += _leaves([(150, 120, 0.7, 20, BORDO), (1050, 260, 0.9, -15, ORANGE),
                  (620, 90, 0.6, 40, GOLD), (380, 300, 0.75, 10, BORDO_DK),
                  (990, 380, 0.7, -30, ORANGE)])
    return s + "</svg>"


def _chichibu():
    s = _open("chichibu", "#e7efd6", "#f6f1df")
    s += _sun(280, 140, 66, "#f0e2b0", 0.7)
    s += _mtn([(0, 300), (300, 170), (600, 300), (900, 190), (1200, 300), (1200, 460), (0, 460)], "#8fb27a")
    s += _mtn([(0, 360), (250, 250), (520, 350), (760, 250), (1050, 350), (1200, 300), (1200, 460), (0, 460)], FOREST)
    for x, h in [(120, 150), (200, 190), (300, 150), (1000, 160), (1090, 200), (1160, 150)]:
        s += _cedar(x, 400, h, FOREST_DK)
    # svetišče + stopnice
    s += ('<rect x="560" y="300" width="90" height="70" fill="#7a4432"/>'
          '<path d="M545 300 L605 262 L665 300 Z" fill="#5e1a25"/>')
    s += _torii(605, 300, 92, VERM, VERM_DK)
    for i in range(6):
        s += f'<rect x="{560+i*3}" y="{372+i*12}" width="{90-i*6}" height="9" fill="{STONE}"/>'
    s += f'<rect x="0" y="392" width="{W}" height="80" fill="#5c7a4a"/>'
    s += _leaves([(180, 110, 0.75, 15, ORANGE), (930, 150, 0.7, -20, GOLD),
                  (700, 240, 0.6, 35, BORDO), (430, 300, 0.7, -10, ORANGE)])
    return s + "</svg>"


def _izu():
    s = _open("izu", "#c9e8ee", "#eef8f6")
    s += _sun(920, 150, 84, "#f4b45e", 0.85)
    s += _mtn([(0, 300), (180, 220), (360, 300), (0, 300)], "#9ec6b0")
    # morje
    s += f'<rect x="0" y="300" width="{W}" height="160" fill="{SEA_LT}"/>'
    s += _waves(320, SEA, 0.9)
    s += _waves(360, SEA_DK, 0.85)
    # obala / klif iz lave
    s += ('<path d="M0 300 L0 200 C120 210 180 250 230 300 Z" fill="#6b4a3a"/>'
          '<path d="M230 300 C180 250 120 210 0 200 L0 240 C110 250 160 270 210 300 Z" fill="#8a6350"/>')
    # sončni odsev
    s += f'<rect x="880" y="300" width="80" height="150" fill="#f4d089" opacity="0.4"/>'
    # jadrnica
    s += ('<path d="M1000 336 L1050 336 L1030 360 L1010 360 Z" fill="#fbf3e2"/>'
          '<rect x="1024" y="300" width="4" height="38" fill="#7a4432"/>'
          '<path d="M1028 302 L1058 334 L1028 334 Z" fill="#c24a3a"/>')
    s += _leaves([(150, 120, 0.75, 20, BORDO), (760, 130, 0.6, -25, GOLD),
                  (520, 90, 0.65, 40, ORANGE)])
    return s + "</svg>"


def _kumano():
    s = _open("kumano", "#f4e6c0", "#faf1de")
    s += _sun(300, 150, 60, "#f0cf8a", 0.75)
    s += _mtn([(0, 320), (300, 200), (620, 330), (900, 210), (1200, 320), (1200, 460), (0, 460)], "#c9a06a")
    s += _mtn([(0, 380), (280, 280), (560, 380), (860, 280), (1200, 370), (1200, 460), (0, 460)], "#9c7a4c")
    for x, h in [(140, 170), (240, 210), (960, 180), (1080, 220)]:
        s += _cedar(x, 410, h, FOREST_DK)
    # veliki torii (Oyunohara)
    s += _torii(620, 400, 230, VERM, VERM_DK)
    s += f'<rect x="0" y="400" width="{W}" height="70" fill="#8a6a44"/>'
    s += _leaves([(180, 120, 0.8, 15, BORDO), (900, 140, 0.7, -20, ORANGE),
                  (470, 300, 0.7, 30, GOLD), (760, 330, 0.65, -10, BORDO_DK)])
    return s + "</svg>"


def _koyasan():
    s = _open("koyasan", "#d7c8dd", "#f2e6dc")
    s += _sun(930, 140, 62, "#f0dca8", 0.6)
    s += _mtn([(0, 330), (320, 210), (640, 330), (960, 210), (1200, 320), (1200, 460), (0, 460)], "#8f86a0")
    for x, h in [(120, 200), (210, 250), (300, 200), (980, 210), (1080, 260), (1160, 200)]:
        s += _cedar(x, 420, h, FOREST_DK)
    # pagoda Konpon Daito
    s += _pagoda(600, 415, 250, VERM, VERM_DK)
    # kamnite luči
    for lx in (430, 500, 720, 790):
        s += (f'<rect x="{lx-8}" y="378" width="16" height="34" fill="{STONE}"/>'
              f'<rect x="{lx-13}" y="366" width="26" height="14" fill="#a59a86"/>'
              f'<circle cx="{lx}" cy="360" r="7" fill="#f4c96a"/>')
    s += f'<rect x="0" y="412" width="{W}" height="60" fill="#6a6152"/>'
    s += _leaves([(170, 120, 0.75, 18, BORDO), (860, 150, 0.7, -22, GOLD),
                  (500, 300, 0.65, 30, ORANGE)])
    return s + "</svg>"


def _iya():
    s = _open("iya", "#e9e2c6", "#f7f0dd")
    s += _sun(950, 140, 60, "#f0d492", 0.7)
    s += _mtn([(0, 250), (200, 150), (430, 260), (430, 460), (0, 460)], "#a87f4c")
    s += _mtn([(770, 260), (980, 150), (1200, 250), (1200, 460), (770, 460)], "#9c7444")
    # soteska in reka
    s += f'<path d="M430 260 L430 460 L770 460 L770 260 Z" fill="{SEA_LT}"/>'
    s += f'<path d="M470 380 Q600 400 730 380 L730 460 L470 460 Z" fill="{SEA}"/>'
    # gozd na stenah
    for x, h in [(120, 150), (250, 190), (340, 150), (880, 160), (1000, 200), (1090, 150)]:
        s += _cedar(x, 300, h, FOREST_DK)
    # viseči most iz trte
    s += ('<path d="M430 250 Q600 340 770 250" fill="none" stroke="#7a5a34" stroke-width="8"/>'
          '<path d="M430 232 Q600 322 770 232" fill="none" stroke="#8a6a3e" stroke-width="5"/>')
    for i in range(1, 12):
        t = i / 12.0
        x = 430 + (770 - 430) * t
        y = 250 - 4 * (2 * t - 1) ** 2 * 0 + (250 + (250 - 250) * t)
        yc = 250 + (90) * (1 - (2 * t - 1) ** 2)
        s += f'<line x1="{x:.0f}" y1="{250 - 18}" x2="{x:.0f}" y2="{yc:.0f}" stroke="#6b4a2a" stroke-width="3"/>'
    s += _leaves([(180, 120, 0.8, 15, BORDO), (900, 130, 0.7, -20, ORANGE),
                  (600, 150, 0.6, 40, GOLD)])
    return s + "</svg>"


def _ine():
    s = _open("ine", "#cfe6ea", "#eef6f4")
    s += _sun(250, 140, 58, "#f0dca0", 0.7)
    s += _mtn([(0, 300), (250, 200), (520, 300), (0, 300)], MOSS)
    s += _mtn([(680, 300), (950, 200), (1200, 300), (1200, 320), (680, 320)], "#5c7a4a")
    # voda
    s += f'<rect x="0" y="300" width="{W}" height="160" fill="{SEA_LT}"/>'
    s += _waves(330, SEA, 0.85)
    # funaya (hiše na vodi)
    for i, x in enumerate((120, 250, 380, 760, 900, 1030)):
        wall = "#c9a06a" if i % 2 else "#b98a52"
        s += f'<rect x="{x}" y="250" width="90" height="60" fill="#7a5a3a"/>'    # spodnji del nad vodo
        s += _house(x, 250, 90, 70, VERM_DK, wall)
    # čoln
    s += ('<path d="M540 340 L660 340 L636 366 L564 366 Z" fill="#7a4432"/>'
          '<rect x="596" y="322" width="4" height="18" fill="#5e1a25"/>')
    s += _leaves([(180, 120, 0.75, 18, BORDO), (1050, 150, 0.7, -20, ORANGE),
                  (600, 110, 0.6, 40, GOLD)])
    return s + "</svg>"


def _kyoto():
    s = _open("kyoto", "#f6e0af", "#fcf1dc")
    s += _sun(950, 140, 74, "#f0b862", 0.8)
    s += _mtn([(0, 320), (300, 210), (620, 330), (940, 210), (1200, 320), (1200, 460), (0, 460)], "#cf9a58")
    # javorji (krošnje)
    for x, cy, r, col in [(140, 300, 70, BORDO), (250, 320, 56, ORANGE),
                          (980, 300, 74, VERM), (1090, 330, 56, GOLD)]:
        s += f'<rect x="{x-6}" y="{cy}" width="12" height="120" fill="#6b4426"/>'
        s += f'<circle cx="{x-24}" cy="{cy}" r="{r*0.7:.0f}" fill="{col}"/>'
        s += f'<circle cx="{x+22}" cy="{cy-10}" r="{r*0.75:.0f}" fill="{col}"/>'
        s += f'<circle cx="{x}" cy="{cy-30}" r="{r*0.8:.0f}" fill="{col}"/>'
    # bambus
    for bx in (430, 452, 474, 496):
        s += f'<rect x="{bx}" y="200" width="7" height="220" fill="{MOSS}"/>'
    # pagoda
    s += _pagoda(650, 415, 240, VERM, VERM_DK)
    s += f'<rect x="0" y="412" width="{W}" height="60" fill="#a06a3c"/>'
    s += _leaves([(200, 120, 0.85, 18, BORDO), (860, 130, 0.75, -22, ORANGE),
                  (560, 110, 0.7, 40, GOLD), (330, 250, 0.7, -12, BORDO_DK),
                  (1030, 250, 0.7, 25, ORANGE)])
    return s + "</svg>"


def _osaka():
    s = _open("osaka", "#e7c9a6", "#f7e6d2")
    s += _sun(240, 150, 70, "#f3a24e", 0.8)
    s += _mtn([(0, 340), (300, 280), (700, 340), (1000, 285), (1200, 335), (1200, 460), (0, 460)], "#c89a6a")
    # mesto
    for x, ht, w, col in [(90, 150, 70, "#9c6a4a"), (170, 200, 80, "#8a5a3e"),
                          (270, 140, 60, "#9c6a4a"), (940, 170, 70, "#8a5a3e"),
                          (1030, 220, 80, "#7a4a34"), (1130, 150, 70, "#9c6a4a")]:
        s += f'<rect x="{x}" y="{380-ht}" width="{w}" height="{ht}" fill="{col}"/>'
        for wy in range(0, ht - 20, 26):
            s += f'<rect x="{x+8}" y="{382-ht+wy}" width="{w-16}" height="10" fill="#f4c96a" opacity="0.5"/>'
    # grad Osaka
    gx = 600
    s += _pagoda(gx, 380, 200, "#6a7a54", "#3f4d33")  # zeleni strehi gradu
    s += (f'<rect x="{gx-70}" y="380" width="140" height="40" fill="{STONE}"/>'
          f'<polygon points="{gx-70},380 {gx-40},350 {gx+40},350 {gx+70},380" fill="#6b6252"/>')
    # zlati okrasek
    s += f'<circle cx="{gx-30}" cy="200" r="6" fill="{GOLD}"/><circle cx="{gx+30}" cy="200" r="6" fill="{GOLD}"/>'
    s += f'<rect x="0" y="380" width="{W}" height="90" fill="#8a5a3c"/>'
    # kanal odsev
    s += f'<rect x="0" y="418" width="{W}" height="52" fill="#5c3a28" opacity="0.35"/>'
    s += _leaves([(180, 120, 0.8, 18, BORDO), (900, 130, 0.72, -20, ORANGE),
                  (500, 110, 0.65, 40, GOLD)])
    return s + "</svg>"


def _kawaguchiko():
    s = _open("kawaguchiko", "#dfe7f0", "#fbeede")
    s += _sun(960, 120, 54, "#f3c276", 0.7)
    # zadnje gore
    s += _mtn([(0, 300), (260, 240), (520, 300), (0, 300)], "#9fb0c0")
    s += _mtn([(760, 300), (1000, 240), (1200, 300), (1200, 320), (760, 320)], "#9fb0c0")
    # gora Fuji
    fx, apex = 600, 70
    s += _mtn([(360, 320), (fx - 44, 120), (fx, apex), (fx + 44, 120), (840, 320)], "#6f7f96")
    # snežni vrh
    s += ('<path d="M%d %d L%d %d Q%d %d %d %d Q%d %d %d %d Q%d %d %d %d Z" fill="#f7fbff"/>'
          % (fx - 70, 150, fx, apex, fx - 24, 128, fx - 40, 150,
             fx, 140, fx + 40, 150, fx + 24, 128, fx + 70, 150))
    # jezero
    s += f'<rect x="0" y="320" width="{W}" height="140" fill="{SEA_LT}"/>'
    # odsev Fujija
    s += _mtn([(470, 320), (fx, 400), (730, 320)], "#9fb6c6", 0.6)
    s += _waves(344, SEA, 0.8)
    # pagoda Chureito na levem hribu + javorji
    s += _pagoda(150, 300, 130, VERM, VERM_DK)
    for x, cy, r, col in [(250, 250, 46, BORDO), (1040, 250, 50, ORANGE), (1120, 270, 40, GOLD)]:
        s += f'<rect x="{x-5}" y="{cy}" width="10" height="80" fill="#6b4426"/>'
        s += f'<circle cx="{x}" cy="{cy-18}" r="{r}" fill="{col}"/>'
    s += _leaves([(200, 110, 0.8, 18, BORDO), (900, 120, 0.7, -20, ORANGE),
                  (470, 150, 0.6, 40, GOLD)])
    return s + "</svg>"


def _minobusan():
    s = _open("minobusan", "#efe7c8", "#f8f1df")
    s += _sun(300, 140, 60, "#f0d692", 0.7)
    s += _mtn([(0, 330), (320, 200), (640, 330), (960, 200), (1200, 320), (1200, 460), (0, 460)], "#7f9a6a")
    s += _mtn([(0, 380), (280, 290), (620, 380), (960, 290), (1200, 370), (1200, 460), (0, 460)], FOREST)
    for x, h in [(120, 190), (210, 240), (300, 190), (980, 200), (1080, 250), (1160, 190)]:
        s += _cedar(x, 420, h, FOREST_DK)
    # tempelj + pagoda
    s += ('<rect x="520" y="300" width="160" height="80" fill="#7a4432"/>'
          '<path d="M500 300 L600 258 L700 300 Z" fill="#5e1a25"/>')
    s += _pagoda(760, 400, 210, VERM, VERM_DK)
    # stopnice
    for i in range(7):
        s += f'<rect x="{545+i*4}" y="{380+i*11}" width="{110-i*8}" height="8" fill="{STONE}"/>'
    # javorji
    for x, cy, r, col in [(430, 300, 48, ORANGE), (900, 310, 44, BORDO)]:
        s += f'<rect x="{x-5}" y="{cy}" width="10" height="90" fill="#6b4426"/>'
        s += f'<circle cx="{x}" cy="{cy-16}" r="{r}" fill="{col}"/>'
    s += f'<rect x="0" y="406" width="{W}" height="60" fill="#5c7a4a"/>'
    s += _leaves([(180, 120, 0.75, 16, BORDO), (1000, 140, 0.7, -20, GOLD),
                  (600, 150, 0.6, 35, ORANGE)])
    return s + "</svg>"


def _nara():
    s = _open("nara", "#f4e2b2", "#fbf2dd")
    s += _sun(960, 140, 66, "#f0b862", 0.8)
    s += _mtn([(0, 300), (300, 220), (640, 310), (960, 220), (1200, 300), (1200, 460), (0, 460)], "#cf9a58")
    # javorji
    for x, cy, r, col in [(120, 300, 60, BORDO), (1060, 300, 64, ORANGE), (1150, 330, 48, GOLD)]:
        s += f'<rect x="{x-6}" y="{cy}" width="12" height="110" fill="#6b4426"/>'
        s += f'<circle cx="{x}" cy="{cy-20}" r="{r}" fill="{col}"/>'
    # Daibutsuden (velika dvorana)
    bx = 560
    s += (f'<rect x="{bx-150}" y="300" width="300" height="100" fill="#8a5a3c"/>'
          f'<path d="M{bx-185} 300 Q{bx} 232 {bx+185} 300 Z" fill="#5e1a25"/>'
          f'<path d="M{bx-150} 300 Q{bx} 254 {bx+150} 300 Z" fill="#7a3a30"/>'
          f'<circle cx="{bx-55}" cy="268" r="7" fill="{GOLD}"/><circle cx="{bx+55}" cy="268" r="7" fill="{GOLD}"/>'
          f'<rect x="{bx-20}" y="330" width="40" height="70" fill="#3a241a"/>')
    # kamnita luč
    s += ('<rect x="300" y="360" width="20" height="40" fill="#a59a86"/>'
          '<rect x="294" y="346" width="32" height="16" fill="#8a8478"/>'
          '<circle cx="310" cy="340" r="8" fill="#f4c96a"/>')
    s += f'<rect x="0" y="398" width="{W}" height="64" fill="#8a6a44"/>'
    # jelen
    dx, dy = 820, 392
    s += (f'<ellipse cx="{dx}" cy="{dy-26}" rx="34" ry="18" fill="#8a5a3a"/>'
          f'<rect x="{dx-26}" y="{dy-20}" width="7" height="24" fill="#8a5a3a"/>'
          f'<rect x="{dx-6}" y="{dy-20}" width="7" height="24" fill="#8a5a3a"/>'
          f'<rect x="{dx+14}" y="{dy-20}" width="7" height="24" fill="#7a4a30"/>'
          f'<path d="M{dx+28} {dy-34} Q{dx+48} {dy-42} {dx+46} {dy-60}" stroke="#8a5a3a" stroke-width="7" fill="none"/>'
          f'<circle cx="{dx+48}" cy="{dy-62}" r="9" fill="#8a5a3a"/>'
          f'<path d="M{dx+45} {dy-66} l-6 -12 M{dx+52} {dy-66} l6 -12" stroke="#6b4426" stroke-width="3"/>')
    s += _leaves([(200, 120, 0.8, 18, BORDO), (900, 130, 0.72, -20, GOLD),
                  (520, 150, 0.6, 40, ORANGE)])
    return s + "</svg>"


def _hiroshima():
    s = _open("hiroshima", "#cfe3ea", "#eef6f4")
    s += _sun(300, 140, 58, "#f0dca0", 0.7)
    s += _mtn([(0, 300), (260, 210), (560, 300), (0, 300)], MOSS)
    s += _mtn([(640, 300), (940, 200), (1200, 300), (1200, 320), (640, 320)], "#5c7a4a")
    # morje
    s += f'<rect x="0" y="300" width="{W}" height="160" fill="{SEA_LT}"/>'
    s += _waves(330, SEA, 0.85)
    # plavajoča velika torija
    s += _torii(600, 420, 200, VERM, VERM_DK)
    # odsev
    s += f'<rect x="548" y="380" width="104" height="60" fill="{VERM_DK}" opacity="0.2"/>'
    # javor na bregu
    s += f'<rect x="150" y="250" width="10" height="70" fill="#6b4426"/><circle cx="155" cy="240" r="40" fill="{BORDO}"/>'
    s += f'<rect x="1050" y="250" width="10" height="70" fill="#6b4426"/><circle cx="1055" cy="238" r="44" fill="{ORANGE}"/>'
    s += _leaves([(230, 130, 0.75, 18, BORDO), (900, 120, 0.7, -20, GOLD),
                  (600, 110, 0.6, 40, ORANGE)])
    return s + "</svg>"


_BUILDERS = {
    "tokio": _tokio, "chichibu": _chichibu, "kawaguchiko": _kawaguchiko,
    "minobusan": _minobusan, "izu": _izu, "kumano": _kumano, "koyasan": _koyasan,
    "iya": _iya, "ine": _ine, "nara": _nara, "kyoto": _kyoto, "osaka": _osaka,
    "hiroshima": _hiroshima,
}


def location_scene(key):
    return _BUILDERS[key]()


def home_scene():
    key = "home"
    s = (f'<svg class="scene-svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Ilustracija: jesenska Japonska — gore, torii in javorji" '
         f'xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">'
         f'{_defs(key, "#f6d79e", "#fcefd8")}'
         f'<rect width="{W}" height="{H}" fill="url(#sky-{key})"/>')
    s += _sun(600, 165, 96, "#f2ac50", 0.85)
    s += _mtn([(0, 330), (300, 200), (620, 330), (940, 200), (1200, 320), (1200, 460), (0, 460)], "#e0aa6e")
    s += _mtn([(0, 390), (260, 290), (560, 390), (860, 290), (1200, 380), (1200, 460), (0, 460)], "#b3764a")
    for x, h in [(120, 190), (210, 240), (1000, 210), (1090, 250)]:
        s += _cedar(x, 420, h, FOREST_DK)
    s += _torii(600, 410, 210, VERM, VERM_DK)
    s += f'<rect x="0" y="410" width="{W}" height="60" fill="#8a5a3c"/>'
    s += _leaves([(180, 120, 0.9, 18, BORDO), (980, 130, 0.85, -20, ORANGE),
                  (420, 110, 0.7, 40, GOLD), (760, 240, 0.75, -12, BORDO_DK),
                  (300, 300, 0.7, 25, ORANGE), (1050, 300, 0.7, -30, GOLD)])
    return s + "</svg>"
