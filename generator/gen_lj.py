# -*- coding: utf-8 -*-
"""Gradnja potovanja »Zmajeva pustolovščina« (Ljubljana). Zagon: python3 gen_lj.py

Uporablja skupne predloge iz gen.py; vsebino in besedila prepiše z lj_content.py."""
import os
import datetime as dt

import gen as G
import art
import art_lj
import lj_content as C

# --------------------------------------------------------------------------- nastavitve
G.CFG.clear()
G.CFG.update(C.CFG)
G.CFG["pin"] = "#2f8f6b"
G.CFG["css"] = """  <style>
    :root { --accent:#1f7a5a; --accent-ink:#1f7a5a; --accent-soft:#e8f5ee; --pin:#2f8f6b; --orange:#c8553d; --gold:#b08a2e; }
    @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --accent:#6fd0a6; --accent-ink:#6fd0a6; --accent-soft:#14261e; --pin:#2f8f6b; --orange:#e08a6c; --gold:#d2b256; } }
    :root[data-theme="dark"] { --accent:#6fd0a6; --accent-ink:#6fd0a6; --accent-soft:#14261e; --pin:#2f8f6b; --orange:#e08a6c; --gold:#d2b256; }
  </style>"""
G.TXT.update(C.TXT)
G.TXT["sights_h"] = "🦒 Kaj videti in početi"
G.OUT = os.path.join(G.SITE_DIR, G.CFG["slug"])

G.LOCATIONS[:] = C.LOCATIONS
for name in ("GUIDE", "EXTRAS", "RUBRICS", "IZZIVI", "MAPS", "VIDEOS"):
    obj = getattr(G, name)
    obj.clear()
G.GUIDE.update(C.GUIDE)
G.EXTRAS.update(C.EXTRAS)
G.RUBRICS.update(C.RUBRICS)
G.IZZIVI.update(C.IZZIVI)
G.MAPS.update(C.MAPS)
G.MAPS.pop("domov", None)          # isti kraj kot vlak — ne podvajaj na zemljevidu poti
G.ITINERARY = C.ITINERARY
G.DAYS = {"vlak": "dopoldne", "emonec": "1 noč", "center": "popoldne s Katjo", "zoo": "glavni dan", "domov": "popoldne"}
G.TRIP_START = dt.date(*C.TRIP_START)
G.REGION_KEY = C.REGION_KEY
G.DAYTRIP_BASE = {}
G.CHECKLIST = C.CHECKLIST
G.LODGING = C.LODGING
G.BOOK = C.BOOK
G.LEG_LINKS = C.LEG_LINKS
G.QUICKBUY = C.QUICKBUY
G.DOZ_SEARCH = False
G.FOOD_LINKS = C.FOOD_LINKS
G.STATIONS_LABEL = "Postaje pustolovščine"
G.NAV_PRIMARY = [
    ("index.html", "index", "🏠", "Domov"),
    ("kako.html", "kako", "🎓", "Kako uporabljati"),
    ("nacrt.html", "nacrt", "🗺️", "Načrt poti"),
    ("izziv.html", "izziv", "📸", "Izzivi"),
    ("nalozi.html", "nalozi", "📤", "Naloži fotografije"),
    ("priprave.html", "priprave", "🎒", "Priprave"),
    ("nujno.html", "nujno", "🆘", "Nujno"),
]
G.FOOTER = G.make_footer("🐉 Zmajeva pustolovščina · 15.–16. oktober 2026 · Maribor → Ljubljana",
                         "Z ljubeznijo pripravljeno za Ano in Maksa")
G.RUBRIC_META = [
    ("najlepsi_trenutek", "🌟 Najlepši trenutek", "rubric-moment"),
    ("ura_zase", "☕ Odmor za dva", "rubric-hour"),
    ("mandala", "✏️ Za risanje in zapisek", "rubric-mandala"),
]
art.home_scene = art_lj.home_scene
esc = G.esc
N_IZZIVOV = sum(len(v) for v in C.IZZIVI.values())


def videos_section_lj(loc):
    links = " · ".join(f'<a href="{G.yt_search_url(p)}" target="_blank" rel="noopener">»{esc(p)}«</a>'
                       for p in loc["phrases"])
    return ('<section class="card-section" aria-labelledby="videi">\n  <h2 id="videi">🎬 Videi za navdih</h2>\n'
            f'  <p class="video-more">Poglejta na YouTube, preden greta (ali po poti): {links}</p>\n</section>\n')


G.videos_section = videos_section_lj


# --------------------------------------------------------------------------- domača stran
QUICK_LINKS = [
    ("nacrt.html", "🗺️", "Načrt poti", "2 dneva, korak za korakom"),
    ("zoo.html", "🦁", "Živalski vrt", "poglobljen načrt in izzivi"),
    ("izziv.html", "📸", "Foto izzivi", f"{N_IZZIVOV} izzivov in presenečenja"),
    ("nalozi.html", "📤", "Naloži fotografije", "album iz vajinih telefonov"),
    ("priprave.html", "🎒", "Priprave", "kontrolni seznam"),
    ("priprave.html#povezave", "🔗", "Kupi in rezerviraj", "vlak, zoo, hotel"),
    ("nacrt.html#prehodi", "🚆", "Prevozi", "vlak, avtobus 18, povezave"),
    ("nujno.html", "🆘", "Nujno", "112, 113, hotel"),
]


def index_page():
    out = G.head(C.CFG["title"] + " — Ljubljana", C.CFG["desc"], with_map=True)
    out += G.nav("index")
    out += "<main>\n"
    out += f"""<section class="hero">
  {G.banner_html("hero", art.home_scene(), "Zmajeva pustolovščina — Ljubljana", "home-banner")}
  <p class="leaves" aria-hidden="true">🐉 🦁 🐘</p>
  <h1>Zmajeva<br><span class="h1-sub">pustolovščina</span></h1>
  <p class="dates">15.–16. oktober 2026 · Maribor → Ljubljana</p>
  <p class="tagline">Žepni vodnik za Ano in Maksa: vlak, hotel, Katja in cel dan med živalmi. Načrt, ideje, foto izzivi in presenečenja.</p>
  <a class="photo-button" href="nalozi.html">📸 Vajin album — naloži fotografije</a>
</section>
<section class="today-card" id="today" hidden aria-live="polite"></section>
"""
    out += '<nav class="quick-links" aria-label="Glavna poglavja">\n'
    for href, e, t, d in QUICK_LINKS:
        out += (f'  <a href="{href}"><span class="ql-emoji" aria-hidden="true">{e}</span>'
                f'<span class="ql-t">{esc(t)}</span><span class="ql-d">{esc(d)}</span></a>\n')
    out += "</nav>\n"
    out += """<section class="card-section map-route-sec" aria-labelledby="pot">
  <h2 id="pot">🗺️ Vajina pot po Ljubljani</h2>
  <div class="route-map" id="route-map" role="img" aria-label="Zemljevid poti po Ljubljani: postaja, hotel, center, živalski vrt"></div>
  <p class="map-legend"><span class="lg-line"></span> pot po postajah. Tapnita številko za vodnik.</p>
  <p class="visit-sum" id="visit-sum"></p>
</section>
"""
    out += '<section class="welcome card-section" aria-labelledby="welcome">\n  <h2 id="welcome">👋 Pozdravljena, zmajska ekipa</h2>\n'
    for ptxt in C.WELCOME:
        out += f"  <p>{esc(ptxt)}</p>\n"
    out += f"  <p>Čaka vaju <strong>{N_IZZIVOV} foto izzivov</strong> — največ v živalskem vrtu. Ana in Maks: kamere pripravljene! 🐉</p>\n</section>\n"
    out += '<h2 class="section-title">Vajine postaje</h2>\n<ul class="cards">\n'
    for i, loc in enumerate(G.LOCATIONS):
        stop = f"Postaja {i + 1}"
        lbl = G.stop_label(loc)
        if lbl:
            stop += f" · {lbl}"
        out += f"""  <li>
    <a href="{loc['key']}.html">
      <span class="card-scene">{G.card_media(loc['key'], art.location_scene(loc['key']))}</span>
      <span class="card-body">
        <span class="stop-num">{stop}</span> <span class="visit-tag" data-visit-tag="{loc['key']}" hidden>✅ Obiskano</span>
        <span class="card-title">{loc['emoji']} {esc(loc['name'])}</span>
        <span class="card-teaser">{esc(loc['teaser'])}</span>
        <span class="card-more">Odpri vodnik →</span>
      </span>
    </a>
  </li>
"""
    out += "</ul>\n"
    out += '<div class="back-row"><a class="back-button" href="nujno.html">🆘 Nujne informacije</a></div>\n'
    out += G.trip_script() + G.route_script()
    out += "</main>\n" + G.FOOTER
    return out


# --------------------------------------------------------------------------- nujno, priprave
def nujno_page():
    out = G.head("Nujno · Zmajeva pustolovščina",
                 "Nujne številke, kaj storiti ob težavi in prostor za pomembne številke.")
    out += G.nav("nujno")
    out += "<main>\n"
    out += G._page_hero("🆘", "Mir v žepu", "Nujne informacije", "Upamo, da jih ne bosta potrebovala — a dobro je, da so tu")
    out += C.NUJNO_CALLS_HTML
    out += '<section class="card-section" aria-labelledby="tezava">\n  <h2 id="tezava">🧭 Kaj storiti ob težavi</h2>\n'
    for e, h, t in C.NUJNO_STEPS:
        out += (f'  <details class="step-box"><summary><span class="sb-e">{e}</span>{esc(h)}</summary>'
                f'<p>{esc(t)}</p></details>\n')
    out += "</section>\n"
    out += C.NUJNO_NOTES_HTML
    out += '<div class="back-row"><a class="back-button" href="index.html">🏠 Nazaj na pregled</a></div>\n'
    out += "</main>\n" + G.FOOTER
    return out


PRIPRAVE = [
    ("🚂", "Pot in prevoz", [
        ("Vlak", "Maribor ↔ Ljubljana traja približno 2 uri. Vozni red in vozovnice: potniski.sz.si ali na blagajni. Pridita na peron pet minut prej."),
        ("Hotel", "Hotel Emonec, Wolfova ulica 12 — od železniške postaje okoli 12 minut peš. Prtljago lahko odložita že ob prihodu."),
        ("Avtobus v zoo", "Linija št. 18 (smer Stožice), postaja »Živalski vrt«. Čez dan vozi približno vsakih 14 minut; za plačilo preverita možnosti v aplikaciji Ljubljana Bus."),
    ]),
    ("🦁", "Živalski vrt: koristno vedeti", [
        ("Odpiralni čas", "Oktobra po objavljenih podatkih 9.00–18.00; točno uro zadnjega vstopa preverita na zoo.si."),
        ("Vstopnice", "Lahko jih kupita vnaprej na trgovina.zoo.si in se izogneta vrsti."),
        ("Hoja", "Poti je 5–6 km, ponekod po pobočju. Udobni čevlji so pomembnejši od vsega drugega."),
        ("Pravila", "Živali ne hranimo, ne kričimo in ne tolčemo po steklu. V Mini ZOO počepnemo in počakamo, da pride žival sama."),
    ]),
    ("🌤️", "Vreme in oblačila", [
        ("Oktobra", "Računajta na hladnejše dni (okoli 5–15 °C) in možnost dežja. Plasti: majica, pulover, jakna, kapa."),
        ("Obutev", "Nepremočljivi, udobni čevlji; rezervne nogavice v nahrbtniku."),
        ("Dež", "Zoo ima tudi notranje prostore (vivarij); v mestu so muzeji in kavarne."),
    ]),
]


def priprave_page():
    out = G.head("Priprave · Zmajeva pustolovščina",
                 "Prevoz, živalski vrt, vreme in kontrolni seznam za odhod.")
    out += G.nav("priprave")
    out += "<main>\n"
    out += G._page_hero("🎒", "Da bo vse gladko", "Priprave", "Prevoz · živalski vrt · vreme · seznam")
    out += '<nav class="chip-row" aria-label="Vsebina">\n'
    for i, (e, t, _) in enumerate(PRIPRAVE):
        out += f'  <a class="chip" href="#p{i}">{e} {esc(t)}</a>\n'
    out += '  <a class="chip" href="#povezave">🔗 Kupi in rezerviraj</a>\n'
    out += '  <a class="chip" href="#seznam">✅ Kontrolni seznam</a>\n</nav>\n'
    out += G.quickbuy_section()
    for i, (e, t, items) in enumerate(PRIPRAVE):
        out += f'<section class="card-section" aria-labelledby="p{i}">\n  <h2 id="p{i}">{e} {esc(t)}</h2>\n  <ul class="nice-list">\n'
        for name, text in items:
            out += f"    <li><strong>{esc(name)}</strong> — {esc(text)}</li>\n"
        out += "  </ul>\n</section>\n"
    out += G.checklist_section()
    out += '<div class="back-row"><a class="back-button" href="index.html">🏠 Nazaj na pregled</a></div>\n'
    out += "</main>\n" + G.FOOTER
    return out


# --------------------------------------------------------------------------- navodila (wizard)
def wiz_steps():
    demo_menu = ('<div class="demo-bar"><span>🐉 Zmajeva pustolovščina</span><span class="demo-pill">☰ Meni</span></div>'
                 '<ul class="demo-list"><li>🏠 Domov</li><li>🗺️ Načrt poti</li><li>📸 Izzivi</li>'
                 '<li>📤 Naloži fotografije</li><li>🆘 Nujno</li><li class="demo-more">… in vseh 5 postaj</li></ul>')
    demo_today = ('<div class="today-card demo-today"><div class="today-kicker">📅 Danes · 16. okt</div>'
                  '<h2>Dan 2 od 2 — Cel dan v živalskem vrtu</h2><p class="today-region">Živalski vrt</p>'
                  '<p>Avtobus št. 18, slon Ganga, morski levi in Mini ZOO.</p></div>')
    demo_station = ('<div class="demo-chips"><span>🦒 Kaj videti</span><span>📍 Zemljevid</span><span>🗓️ Predlog dneva</span>'
                    '<span>📸 Foto izzivi</span><span>🍦 Hrana</span><span>☔ Če dežuje</span>'
                    '<span>🌟 Najlepši trenutek</span><span>✏️ Risanje</span><span>📖 Dnevnik</span></div>')
    demo_izziv = ('<div class="demo-izziv" data-demo="unlock">'
                  '<div class="izziv-head"><span class="izziv-mark demo-mark">📸</span>'
                  '<span class="izziv-text">Ana in Maks pod vhodnim napisom ali pri vhodu v zoo.</span></div>'
                  '<div class="izziv-surprise locked demo-locked"><span class="sur-ic">🎁</span>'
                  '<span>Presenečenje čaka — odklene se, ko naložita sliko ali video.</span></div>'
                  '<div class="izziv-surprise open demo-open" hidden><div class="sur-head"><span class="sur-ic">💡</span>'
                  '<span><span class="sur-kind">Zanimivost odklenjena</span><strong>Zoo pod Rožnikom</strong></span></div>'
                  '<p>Živalski vrt leži na južnem pobočju Rožnika — v naravnem gozdu in na travnikih.</p></div>'
                  '<button type="button" class="pin-btn demo-btn">▶ Preizkusita: naloži sliko</button></div>')
    demo_upload = ('<div class="gate-row"><span class="gate-lbl">Nalagaš kot:</span>'
                   '<span class="gate-name">Ana</span><span class="gate-name on">Maks</span></div>'
                   '<div class="demo-upload"><span class="demo-select">🦁 Živalski vrt ▾</span>'
                   '<span class="demo-bigbtn">📷 Izberi fotografije ali video</span></div>')
    demo_nujno = ('<div class="call-grid demo-calls"><div class="call-btn call-red"><span class="c-num">112</span><span class="c-lbl">Nujna pomoč</span></div>'
                  '<div class="call-btn call-red"><span class="c-num">113</span><span class="c-lbl">Policija</span></div></div>')
    demo_install = ('<div class="demo-install"><div><strong>🍎 iPhone (Safari)</strong><br>Deli ⬆️ → »Dodaj na začetni zaslon«</div>'
                    '<div><strong>🤖 Android (Chrome)</strong><br>Meni ⋮ → »Dodaj na začetni zaslon«</div></div>')
    return [
        ("🐉", "Dobrodošla, zmajska ekipa!", [
            "To je vajin žepni vodnik za dva dneva v Ljubljani (15.–16. oktober 2026): načrt dneva, ideje, foto izzivi in nujne informacije.",
            "Predstavitev traja približno dve minuti. Tapnita »Naprej« in videla bosta vse, kar zna ta stran."], "", None, ""),
        ("☰", "Meni — vse na enem mestu", [
            "Gumb »Meni« zgoraj desno odpre pregleden meni: glavne strani in vseh 5 postaj. Je na vsaki strani."],
         demo_menu, None, ".menu-toggle"),
        ("📅", "Danes — kaj je na vrsti", [
            "Med pustolovščino domača stran sama pokaže, kateri dan je danes: kje sta in kaj je v načrtu. Pred odhodom kaže odštevanje."],
         demo_today, None, ""),
        ("🗺️", "Načrt poti in zemljevid", [
            "Načrt poti ima oba dneva in prehode (vlak, peš, avtobus). Na domači strani je zemljevid vseh postaj po vrsti."],
         "", ("nacrt.html", "Odpri načrt poti →"), ""),
        ("🦁", "Postaje — vodnik za vsak del poti", [
            "Vsaka postaja ima ideje, zemljevid, predlog dneva, nasvete in osebne rubrike. Največ je v živalskem vrtu: poglobljen načrt za cel dan."],
         demo_station, ("zoo.html", "Poglej primer: Živalski vrt →"), ""),
        ("✅", "Obiskano", [
            "Na vsaki postaji je gumb »Označi kot obiskano«. Kar označita, ostane shranjeno v vajinem telefonu."],
         "", None, ""),
        ("📸", "Foto izzivi in presenečenja", [
            f"Skupaj je {N_IZZIVOV} foto izzivov — največ v živalskem vrtu. Pod vsakim je »drobni tisk«: zakaj se slikata tam.",
            "Ko za izziv naložita sliko, se opravi in odklene presenečenje: zanimivost, skrivnost ali majhna nagrada. Preizkusita spodaj!"],
         demo_izziv, ("izziv.html", "Odpri vse izzive →"), ""),
        ("📤", "Naloži fotografije", [
            "Fotografije in videe naložita kar s telefona. Izbereta, kdo sta (Ana ali Maks), nato postajo in slike.",
            "Vse pristane v vajinem skupnem albumu, ki ga vidita le vidva. Na koncu ga z enim klikom prenesta kot .zip."],
         demo_upload, ("nalozi.html", "Odpri album →"), ""),
        ("🆘", "Nujno — mir v žepu", [
            "Posebna stran s številkami 112 in 113 ter nasveti, kaj storiti, če se kdo izgubi ali če se zgodi kaj nepričakovanega. Upamo, da je ne bosta potrebovala."],
         demo_nujno, ("nujno.html", "Odpri nujne informacije →"), ""),
        ("🎒", "Priprave", [
            "Prevoz, živalski vrt, vreme in kontrolni seznam za odhod (obkljukata, telefon si zapomni)."],
         "", ("priprave.html", "Odpri priprave →"), ""),
        ("📲", "Dodajta stran na domači zaslon", [
            "Da bo stran kot prava aplikacija (ikona na zaslonu, odpira se čez cel zaslon). Ob prvem odprtju z domačega zaslona bosta kodo vnesla še enkrat."],
         demo_install, None, ""),
        ("🐲", "Pripravljena!", [
            "To je vse. Stran lahko to predstavitev kadar koli ponovita — v meniju poiščita »Kako uporabljati«. Lepo pot, Ana in Maks!"],
         "", ("index.html", "Na domačo stran →"), ""),
    ]


G._wiz_steps = wiz_steps


# --------------------------------------------------------------------------- gradnja
def build():
    os.makedirs(G.OUT, exist_ok=True)
    G.copy_assets([])
    # ikone za to potovanje
    icons_src = os.path.join(G.HERE, "lj_icons")
    icons_out = os.path.join(G.OUT, "icons")
    for name in os.listdir(icons_src):
        G.shutil.copy2(os.path.join(icons_src, name), os.path.join(icons_out, name))
    pages = G.write_pages([("index.html", index_page), ("nacrt.html", G.nacrt_page), ("priprave.html", priprave_page),
                           ("nalozi.html", G.nalozi_page), ("izziv.html", G.izziv_page), ("nujno.html", nujno_page),
                           ("kako.html", G.kako_page)])
    for i, loc in enumerate(G.LOCATIONS):
        name = f"{loc['key']}.html"
        with open(os.path.join(G.OUT, name), "w", encoding="utf-8") as f:
            f.write(G.location_page(i, loc))
        pages.append(name)
        print(f"written {name}")
    G.write_pwa(pages)
    print(f"done — {G.OUT} · izzivov: {N_IZZIVOV}")


if __name__ == "__main__":
    build()
