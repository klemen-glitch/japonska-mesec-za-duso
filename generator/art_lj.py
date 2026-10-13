# -*- coding: utf-8 -*-
"""Ilustracije za potovanje »Zmajeva pustolovščina« (Ljubljana).
Uporablja pomožne funkcije iz art.py in se vpiše v njegov register scen."""
import art
from art import W, H, _open, _defs, _sun, _mtn

GREEN = "#2f8f6b"
GREEN_DK = "#1f5f48"
GREEN_LT = "#8cc9a8"
MINT = "#d9efe2"
SKY1, SKY2 = "#bfe3f2", "#fdf3df"
WARM = "#f4c26b"
RED = "#c8553d"
BLUE = "#3f78a8"
WATER = "#79b4cf"
WATER_DK = "#4f8fb0"
STONE = "#c9b79c"
WALL = "#ecd9b8"
ROOF = "#b9573b"
INK = "#2a3a35"
GREY = "#8f9a96"

art.ALT.update({
    "vlak": "Ilustracija vlaka, ki pelje skozi zelene gričke proti Ljubljani",
    "emonec": "Ilustracija hotela v starem delu Ljubljane z lučjo in kovčkom",
    "center": "Ilustracija Ljubljanskega gradu na gričku, zmajskega mostu in reke Ljubljanice",
    "zoo": "Ilustracija živalskega vrta: žirafa, slon in drevesa na pobočju Rožnika",
    "domov": "Ilustracija vlaka ob sončnem zahodu na poti domov",
})


# ------------------------------------------------------------------ gradniki

def _cloud(x, y, s=1.0, op=0.9):
    return (f'<g opacity="{op}" transform="translate({x},{y}) scale({s})" fill="#fff">'
            '<ellipse cx="0" cy="0" rx="58" ry="22"/><ellipse cx="-34" cy="8" rx="34" ry="16"/>'
            '<ellipse cx="38" cy="8" rx="38" ry="17"/><ellipse cx="14" cy="-14" rx="30" ry="18"/></g>')


def _tree(x, base, h, color=GREEN_DK, trunk="#6b4a34"):
    return (f'<rect x="{x-4}" y="{base-h*0.3}" width="8" height="{h*0.3}" fill="{trunk}"/>'
            f'<ellipse cx="{x}" cy="{base-h*0.62}" rx="{h*0.32}" ry="{h*0.4}" fill="{color}"/>')


def _pine(x, base, h, color=GREEN_DK):
    w = h * 0.4
    s = f'<rect x="{x-3}" y="{base-h*0.15}" width="6" height="{h*0.15}" fill="#6b4a34"/>'
    for i, f in enumerate((1.0, 0.78, 0.55)):
        y = base - h * 0.12 - i * h * 0.27
        s += _mtn([(x - w * f / 2, y), (x + w * f / 2, y), (x, y - h * 0.34)], color)
    return s


def _window(x, y, w, h, lit=False):
    fill = "#ffe08a" if lit else "#9cc3d6"
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{fill}"/>'
            f'<rect x="{x+w/2-1}" y="{y}" width="2" height="{h}" fill="{WALL}" opacity="0.8"/>')


def _dragon(x, y, s=1.0, flip=False):
    """Zmaj Ljubljane: zelen, s krili in zavitim repom (stilizirano)."""
    sx = -s if flip else s
    return (f'<g transform="translate({x},{y}) scale({sx},{s})">'
            # rep
            f'<path d="M-120 40 C-170 20 -170 -30 -130 -40 C-160 -10 -140 10 -100 20 Z" fill="{GREEN_DK}"/>'
            # telo
            f'<path d="M-110 30 C-80 -40 20 -50 70 -20 C90 -8 100 0 112 -4 L118 14 C100 28 80 22 62 12 '
            f'C20 -10 -40 0 -70 52 Z" fill="{GREEN}"/>'
            # trebuh
            f'<path d="M-60 40 C-30 0 20 -5 60 14 C30 8 -20 14 -60 40 Z" fill="{WARM}" opacity="0.85"/>'
            # krilo
            f'<path d="M-20 -20 C-30 -80 10 -110 50 -118 C40 -100 52 -92 70 -92 C52 -80 62 -66 80 -62 '
            f'C58 -54 44 -34 30 -22 Z" fill="{GREEN_LT}" stroke="{GREEN_DK}" stroke-width="3"/>'
            # glava
            f'<path d="M100 -8 C112 -30 140 -34 160 -22 C170 -16 168 -4 156 -2 L128 6 C118 14 104 12 100 -8 Z" fill="{GREEN}"/>'
            f'<path d="M112 -26 L106 -46 L124 -32 Z M130 -32 L128 -52 L142 -34 Z" fill="{RED}"/>'
            f'<circle cx="138" cy="-16" r="4.5" fill="#fff"/><circle cx="139" cy="-16" r="2.2" fill="{INK}"/>'
            # noge
            f'<path d="M-30 40 L-40 62 L-20 62 L-8 44 Z M40 30 L36 56 L56 56 L58 32 Z" fill="{GREEN_DK}"/>'
            '</g>')


def _castle(x, base, s=1.0):
    """Ljubljanski grad na gričku (stilizirano)."""
    return (f'<g transform="translate({x},{base}) scale({s})">'
            f'<path d="M-230 0 C-200 -60 -120 -110 -20 -118 C80 -124 190 -90 240 0 Z" fill="#6aa57a"/>'
            f'<rect x="-120" y="-190" width="240" height="78" fill="{WALL}"/>'
            f'<rect x="-120" y="-190" width="240" height="8" fill="{STONE}"/>'
            f'<rect x="-30" y="-262" width="62" height="78" fill="{WALL}"/>'
            f'<polygon points="-38,-262 0,-300 38,-262" fill="{ROOF}"/>'
            f'<rect x="-6" y="-244" width="14" height="22" rx="7" fill="#9cc3d6"/>'
            f'<rect x="-130" y="-228" width="46" height="40" fill="{WALL}"/>'
            f'<polygon points="-136,-228 -107,-258 -78,-228" fill="{ROOF}"/>'
            f'<rect x="84" y="-218" width="40" height="30" fill="{WALL}"/>'
            f'<polygon points="80,-218 104,-244 128,-218" fill="{ROOF}"/>'
            + "".join(f'<rect x="{wx}" y="-170" width="12" height="22" rx="6" fill="#9cc3d6"/>' for wx in (-96, -60, 40, 76))
            + '</g>')


# ------------------------------------------------------------------ scene

def _vlak():
    s = _open("vlak", "#cfe8f5", "#fdf0d8")
    s += _sun(960, 120, 62, "#f6c76a", 0.85)
    s += _cloud(220, 100, 1.0, 0.9) + _cloud(620, 70, 0.7, 0.8) + _cloud(1060, 210, 0.6, 0.7)
    s += _mtn([(0, 300), (200, 210), (420, 300), (700, 220), (980, 300), (1200, 240), (1200, 460), (0, 460)], "#a7d1b8")
    s += _mtn([(0, 350), (260, 280), (520, 350), (820, 290), (1200, 350), (1200, 460), (0, 460)], "#7fb995")
    # gričevje z vinogradi (vrste)
    s += f'<path d="M0 380 C200 320 420 340 640 360 C860 380 1020 330 1200 350 L1200 460 L0 460 Z" fill="{GREEN}"/>'
    for i in range(9):
        y = 372 + i * 6
        s += f'<path d="M{40+i*16} {y} C300 {y-24} 520 {y-6} 760 {y+6}" stroke="{GREEN_DK}" stroke-width="2" fill="none" opacity="0.35"/>'
    for x, h in [(90, 80), (180, 100), (1040, 90), (1130, 110)]:
        s += _tree(x, 372, h)
    # cerkvica na hribu
    s += f'<rect x="868" y="304" width="22" height="26" fill="{WALL}"/><polygon points="864,304 879,286 894,304" fill="{ROOF}"/>'
    # tir in vlak
    s += f'<rect x="0" y="392" width="{W}" height="68" fill="#8d7a64"/>'
    s += f'<rect x="0" y="388" width="{W}" height="6" fill="#5f5648"/>'
    for x in range(0, W, 46):
        s += f'<rect x="{x}" y="404" width="26" height="6" fill="#5b4a3a"/>'
    # vagoni
    for i, x in enumerate((50, 390, 730)):
        col = RED if i == 2 else "#f4f1ea"
        s += (f'<rect x="{x}" y="318" width="320" height="74" rx="14" fill="{col}"/>'
              f'<rect x="{x}" y="372" width="320" height="10" fill="{BLUE}"/>')
        for k in range(6):
            s += f'<rect x="{x+22+k*48}" y="334" width="34" height="26" rx="5" fill="#9cc3d6"/>'
        s += f'<circle cx="{x+60}" cy="396" r="12" fill="{INK}"/><circle cx="{x+260}" cy="396" r="12" fill="{INK}"/>'
    # lokomotiva spredaj
    s += (f'<path d="M1110 318 L1110 392 L1050 392 L1050 318 Q1050 298 1080 298 Q1110 298 1110 318 Z" fill="{RED}"/>'
          f'<rect x="1062" y="322" width="36" height="26" rx="5" fill="#cfe8f5"/>')
    return s + "</svg>"


def _emonec():
    s = _open("emonec", "#274a63", "#f0b985")
    s += _sun(240, 190, 52, "#ffe4a0", 0.9)
    for x, y, r in [(520, 60, 2), (700, 90, 2.4), (860, 50, 2), (980, 120, 2.2), (400, 110, 1.8), (1090, 70, 2)]:
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity="0.8"/>'
    # stare hiše v ozadju
    for x, w, h, col in [(20, 130, 170, "#e8c9a2"), (160, 120, 210, "#d8b48a"), (900, 120, 200, "#e0c096"), (1030, 150, 170, "#e8c9a2")]:
        s += f'<rect x="{x}" y="{392-h}" width="{w}" height="{h}" fill="{col}"/>'
        s += f'<polygon points="{x-6},{392-h} {x+w/2},{392-h-46} {x+w+6},{392-h}" fill="{ROOF}"/>'
        for wx in range(x + 16, x + w - 24, 40):
            for wy in range(392 - h + 24, 360, 50):
                s += _window(wx, wy, 22, 30, lit=((wx + wy) % 3 == 0))
    # hotel
    hx, hw, hh = 330, 540, 250
    s += f'<rect x="{hx}" y="{392-hh}" width="{hw}" height="{hh}" fill="#f1dfbf"/>'
    s += f'<rect x="{hx}" y="{392-hh}" width="{hw}" height="14" fill="{STONE}"/>'
    s += f'<polygon points="{hx-14},{392-hh} {hx+hw/2},{392-hh-70} {hx+hw+14},{392-hh}" fill="{ROOF}"/>'
    for r in range(3):
        for c in range(7):
            s += _window(hx + 26 + c * 72, 392 - hh + 34 + r * 66, 36, 44, lit=((r * 7 + c) % 2 == 0))
    # vhod
    s += f'<rect x="{hx+hw/2-44}" y="326" width="88" height="66" rx="6" fill="#5b3a2c"/>'
    s += f'<rect x="{hx+hw/2-60}" y="316" width="120" height="14" rx="4" fill="{GREEN}"/>'
    s += f'<text x="{hx+hw/2}" y="327" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="11" font-weight="700" fill="#fff">HOTEL EMONEC</text>'
    # ulica in svetilka
    s += f'<rect x="0" y="392" width="{W}" height="68" fill="#6d6a68"/>'
    for x in range(10, W, 110):
        s += f'<rect x="{x}" y="424" width="60" height="5" rx="2" fill="#e8e1d2" opacity="0.7"/>'
    s += f'<rect x="298" y="270" width="6" height="122" fill="{INK}"/><circle cx="301" cy="262" r="12" fill="#ffe08a"/>'
    s += f'<circle cx="301" cy="262" r="30" fill="#ffe08a" opacity="0.25"/>'
    # kovček
    s += (f'<rect x="942" y="352" width="76" height="54" rx="8" fill="{RED}"/><rect x="962" y="342" width="36" height="12" rx="5" fill="none" stroke="{INK}" stroke-width="4"/>'
          f'<rect x="942" y="372" width="76" height="5" fill="#fff" opacity="0.5"/>'
          f'<rect x="1034" y="366" width="56" height="40" rx="7" fill="{BLUE}"/><rect x="1049" y="358" width="26" height="10" rx="4" fill="none" stroke="{INK}" stroke-width="3"/>')
    return s + "</svg>"


def _center():
    s = _open("center", "#b8def0", "#fdf1dc")
    s += _sun(1010, 110, 54, "#f6c76a", 0.85)
    s += _cloud(170, 90, 0.9, 0.85) + _cloud(700, 60, 0.7, 0.8)
    # grič z gradom
    s += _castle(300, 330, 1.0)
    # mesto ob reki
    for x, w, h, col in [(560, 90, 90, "#f0d5ae"), (656, 70, 110, "#e5b98d"), (730, 100, 80, "#f1e0c2"),
                         (880, 100, 100, "#e9c9a0"), (986, 80, 130, "#f0d5ae"), (1072, 110, 90, "#e5b98d")]:
        s += f'<rect x="{x}" y="{340-h}" width="{w}" height="{h}" fill="{col}"/>'
        s += f'<polygon points="{x-4},{340-h} {x+w/2},{340-h-24} {x+w+4},{340-h}" fill="{ROOF}"/>'
        for wx in range(x + 14, x + w - 16, 28):
            for wy in range(340 - h + 14, 320, 30):
                s += _window(wx, wy, 14, 20)
    # drevesa ob bregu
    for x, h in [(500, 110), (840, 100)]:
        s += _tree(x, 346, h)
    # reka
    s += f'<rect x="0" y="340" width="{W}" height="120" fill="{WATER}"/>'
    for y in (370, 398, 426):
        s += f'<path d="M0 {y} Q150 {y-8} 300 {y} T600 {y} T900 {y} T1200 {y}" stroke="#fff" stroke-width="2" fill="none" opacity="0.45"/>'
    # most (zmajski) čez reko
    s += f'<path d="M420 346 Q 700 300 980 346 L980 362 Q 700 322 420 362 Z" fill="{STONE}"/>'
    s += f'<rect x="420" y="338" width="560" height="10" fill="#a8977c"/>'
    for ax in (520, 700, 880):
        s += f'<path d="M{ax-70} 372 Q{ax} 316 {ax+70} 372 L{ax+70} 392 L{ax-70} 392 Z" fill="{WATER_DK}" opacity="0.85"/>'
    # zmaji na mostu (levi in desni stebriček)
    s += _dragon(440, 332, 0.28, flip=False) + _dragon(960, 332, 0.28, flip=True)
    # odsev
    s += f'<rect x="0" y="392" width="{W}" height="68" fill="{WATER_DK}" opacity="0.35"/>'
    return s + "</svg>"


def _giraffe(x, base, s=1.0):
    spots = "".join(f'<ellipse cx="{x+dx*s}" cy="{base+dy*s}" rx="{7*s}" ry="{9*s}" fill="#9a5b22" opacity="0.8"/>'
                    for dx, dy in [(-8, -108), (10, -130), (-6, -150), (12, -176), (0, -206), (-2, -60), (20, -64)])
    return (f'<rect x="{x-24*s}" y="{base-70*s}" width="{12*s}" height="{70*s}" fill="#e6b45a"/>'
            f'<rect x="{x+12*s}" y="{base-70*s}" width="{12*s}" height="{70*s}" fill="#d9a447"/>'
            f'<ellipse cx="{x}" cy="{base-82*s}" rx="{44*s}" ry="{28*s}" fill="#e9b85c"/>'
            f'<polygon points="{x+20*s},{base-92*s} {x+42*s},{base-92*s} {x+30*s},{base-232*s} {x+10*s},{base-232*s}" fill="#e9b85c"/>'
            f'<ellipse cx="{x+28*s}" cy="{base-240*s}" rx="{22*s}" ry="{13*s}" fill="#e9b85c"/>'
            f'<rect x="{x+22*s}" y="{base-262*s}" width="{3*s}" height="{14*s}" fill="#7a4a1c"/><rect x="{x+34*s}" y="{base-262*s}" width="{3*s}" height="{14*s}" fill="#7a4a1c"/>'
            f'<circle cx="{x+36*s}" cy="{base-242*s}" r="{2.6*s}" fill="{INK}"/>' + spots)


def _elephant(x, base, s=1.0):
    g = "#9aa3a8"
    return (f'<rect x="{x-60*s}" y="{base-60*s}" width="{26*s}" height="{60*s}" rx="{8*s}" fill="{g}"/>'
            f'<rect x="{x+34*s}" y="{base-60*s}" width="{26*s}" height="{60*s}" rx="{8*s}" fill="{g}"/>'
            f'<ellipse cx="{x}" cy="{base-92*s}" rx="{84*s}" ry="{54*s}" fill="#aab2b6"/>'
            f'<circle cx="{x+78*s}" cy="{base-112*s}" r="{42*s}" fill="#aab2b6"/>'
            f'<path d="M{x+110*s} {base-100*s} C{x+140*s} {base-76*s} {x+132*s} {base-30*s} {x+116*s} {base-22*s}" '
            f'stroke="#aab2b6" stroke-width="{18*s}" stroke-linecap="round" fill="none"/>'
            f'<ellipse cx="{x+50*s}" cy="{base-108*s}" rx="{26*s}" ry="{34*s}" fill="{g}"/>'
            f'<circle cx="{x+92*s}" cy="{base-124*s}" r="{3.6*s}" fill="{INK}"/>'
            f'<path d="M{x+104*s} {base-84*s} q{16*s} {10*s} {20*s} {-2*s}" stroke="#f3efe6" stroke-width="{6*s}" stroke-linecap="round" fill="none"/>')


def _zoo():
    s = _open("zoo", "#c3e6f0", "#fdf3da")
    s += _sun(1040, 100, 50, "#f6c76a", 0.9)
    s += _cloud(220, 90, 0.9, 0.9) + _cloud(640, 60, 0.6, 0.8)
    s += _mtn([(0, 300), (260, 200), (560, 290), (860, 190), (1200, 290), (1200, 460), (0, 460)], "#9fd0b0")
    s += _mtn([(0, 350), (300, 270), (640, 350), (940, 270), (1200, 340), (1200, 460), (0, 460)], "#6fb086")
    for x, h in [(60, 150), (130, 190), (1090, 170), (1160, 200), (420, 120), (800, 130)]:
        s += _pine(x, 372, h, GREEN_DK)
    # trata in pot
    s += f'<rect x="0" y="372" width="{W}" height="88" fill="#7ec28f"/>'
    s += f'<path d="M-20 440 C300 400 700 430 1220 392 L1220 420 C700 460 300 432 -20 470 Z" fill="#e7d8b4"/>'
    # vhodna lesena tabla
    s += (f'<rect x="196" y="262" width="10" height="112" fill="#7a5638"/><rect x="316" y="262" width="10" height="112" fill="#7a5638"/>'
          f'<rect x="170" y="238" width="182" height="46" rx="10" fill="#f3e3bd" stroke="#7a5638" stroke-width="5"/>'
          f'<text x="261" y="268" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="22" font-weight="800" fill="{GREEN_DK}">ZOO</text>')
    s += _giraffe(560, 380, 1.0)
    s += _elephant(820, 392, 1.0)
    s += _tree(980, 380, 120, "#3f8a5c")
    s += _leaf_birds()
    return s + "</svg>"


def _leaf_birds():
    return ''.join(f'<path d="M{x} {y} q10 -10 20 0 q10 -10 20 0" stroke="{INK}" stroke-width="2.4" fill="none" opacity="0.5"/>'
                   for x, y in [(430, 110), (480, 80), (760, 120)])


def _domov():
    s = _open("domov", "#f8b97a", "#fde6c4")
    s += _sun(880, 270, 120, "#f3855a", 0.55)
    s += _sun(880, 270, 70, "#f6c76a", 0.95)
    s += _cloud(260, 110, 1.0, 0.7) + _cloud(980, 90, 0.7, 0.6)
    s += _mtn([(0, 340), (240, 270), (520, 340), (860, 280), (1200, 340), (1200, 460), (0, 460)], "#7f8fb0")
    s += f'<path d="M0 392 C240 350 520 372 760 384 C960 394 1100 360 1200 372 L1200 460 L0 460 Z" fill="#4f7d6a"/>'
    # domček z dimnikom
    s += (f'<rect x="130" y="306" width="140" height="92" fill="{WALL}"/><polygon points="116,306 200,244 284,306" fill="{ROOF}"/>'
          f'<rect x="232" y="252" width="22" height="40" fill="#8a5a46"/>'
          f'<rect x="186" y="340" width="34" height="58" rx="4" fill="#5b3a2c"/>' + _window(142, 322, 28, 30, True) + _window(232, 322, 28, 30, True))
    # tir + vlak (majhen, v daljavi)
    s += f'<rect x="0" y="404" width="{W}" height="56" fill="#6c5a48"/><rect x="0" y="402" width="{W}" height="5" fill="#463a2e"/>'
    s += f'<rect x="420" y="352" width="420" height="52" rx="12" fill="#f4f1ea"/><rect x="420" y="388" width="420" height="8" fill="{BLUE}"/>'
    for k in range(7):
        s += f'<rect x="{440+k*56}" y="364" width="34" height="20" rx="4" fill="#9cc3d6"/>'
    s += f'<path d="M840 352 L900 372 L900 404 L840 404 Z" fill="{RED}"/>'
    s += f'<circle cx="480" cy="406" r="9" fill="{INK}"/><circle cx="780" cy="406" r="9" fill="{INK}"/>'
    for x, y in [(70, 90), (520, 60), (640, 130), (1100, 60)]:
        s += f'<circle cx="{x}" cy="{y}" r="2" fill="#fff" opacity="0.7"/>'
    return s + "</svg>"


def home_scene():
    key = "home"
    art.ALT[key] = "Ilustracija: zmaj nad Ljubljanskim gradom in mestom"
    s = (f'<svg class="scene-svg" viewBox="0 0 {W} {H}" role="img" aria-label="{art.ALT[key]}" '
         f'xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">'
         f'{_defs(key, "#b9e0f0", "#fdf1dc")}<rect width="{W}" height="{H}" fill="url(#sky-{key})"/>')
    s += _sun(240, 120, 70, "#f6c76a", 0.9)
    s += _cloud(520, 90, 1.0, 0.9) + _cloud(980, 130, 0.8, 0.85) + _cloud(120, 250, 0.6, 0.7)
    s += _mtn([(0, 330), (300, 240), (620, 330), (940, 250), (1200, 330), (1200, 460), (0, 460)], "#a7d1b8")
    s += _castle(860, 400, 1.15)
    s += f'<path d="M0 400 C300 380 700 410 1200 392 L1200 460 L0 460 Z" fill="{WATER}"/>'
    s += f'<path d="M0 420 Q150 412 300 420 T600 420 T900 420 T1200 420" stroke="#fff" stroke-width="2" fill="none" opacity="0.5"/>'
    for x, h in [(80, 150), (170, 190), (330, 120)]:
        s += _tree(x, 404, h, "#3f8a5c")
    s += _dragon(470, 190, 1.05, flip=False)
    return s + "</svg>"


art._BUILDERS.update({"vlak": _vlak, "emonec": _emonec, "center": _center, "zoo": _zoo, "domov": _domov})
