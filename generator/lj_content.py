# -*- coding: utf-8 -*-
"""Vsebina potovanja »Zmajeva pustolovščina« (Ana in Maks v Ljubljani, 15.–16. oktober 2026).
Ton: topel, dvojina (vidva, gresta, naložita). Negotova dejstva so previdno napisana."""

CFG = {
    "id": "ljubljana",
    "slug": "lj-d4phmm7xw",
    "title": "Zmajeva pustolovščina",
    "short": "Zmajeva pustolovščina",
    "brand": "🐉 Zmajeva pustolovščina",
    "theme": "#2f8f6b",
    "desc": "Ana in Maks v Ljubljani: 15.–16. oktober 2026 — vlak, hotel, Katja in cel dan v živalskem vrtu.",
    "people": ["Ana", "Maks"],
    "dates": "15.–16. oktober 2026",
    "base_url": "https://klemen-glitch.github.io/japonska-mesec-za-duso",
    "country": {"name": "Slovenija", "c": [46.12, 14.82], "z": 8},
    "geo_radius_km": 12,
    "after": ["Bravo, zmajska ekipa!",
              "Poglejta <a href=\"nalozi.html\">skupni album</a> in iz slik sestavita svojo Zmajevo knjigo."],
    "t": {
        "locked": "Presenečenje čaka — odklene se, ko naložita sliko ali video.",
        "empty": "Album je še prazen — naložita prvo fotografijo. 📸",
        "thanks": "naloženih ✓ — odlično!",
        "more": "Odpri vodnik za to postajo →",
        "afterHero": "Pustolovščina je za vama — poglejta album, sestavita Zmajevo knjigo in preizkusita kviz.",
        "afterBtn": "📖 Odpri Zmajevo knjigo",
        "pre": "Pustolovščina se začne {date}. Poglejta <a href=\"priprave.html\">priprave</a> in kontrolni seznam.",
    },
}

TRIP_START = (2026, 10, 15)

TXT = {
    "loc_title": "{name} · Zmajeva pustolovščina",
    "loc_desc": "{name}: kaj početi, izzivi in nasveti — Zmajeva pustolovščina, Ljubljana.",
    "magda": "🐉 Zmajeva skrivnost",
    "diary": "📖 Zmajev dnevnik",
    "diary_hint": "Prostor za vajine vtise, skice in najboljši trenutek s te postaje.",
    "nalozi_title": "Naloži fotografije · Zmajeva pustolovščina",
    "izziv_title": "Foto izzivi · Zmajeva pustolovščina",
    "izziv_hero": ("📸", "Skupaj gradita Zmajevo knjigo", "Foto izzivi", "Za Ano in Maksa"),
    "izziv_idea": ("Dva dneva in ena noč bosta minila hitro. Zato za vsako postajo ujameta nekaj slik — ne le razglednic, ampak "
                   "<strong>vaju na teh krajih</strong>: skupaj, ob smehu, ob živalih. Iz teh slik bo po vrnitvi nastala "
                   "<strong>vajina Zmajeva knjiga</strong>. Največ izzivov čaka v živalskem vrtu!"),
    "izziv_final": ("Zadnje presenečenje: izberita <strong>najljubšo sliko vsake postaje</strong> in jo uvrstita v Zmajevo knjigo — "
                    "prva slika (vlak) in zadnja (domov) bosta ob straneh, vmes pa vajina Ljubljana. "
                    "Z gumbom »Prenesi vse slike« na strani Naloži dobita cel album z enim klikom."),
    "izziv_final_title": "🏆 Vse izzive sta opravila!",
    "nalozi_note": "Izberita postajo in naložita slike ali videe. Vse pristane v spodnjem skupnem albumu — vidita ga samo vidva (in kdor ima vajino kodo).",
    "nalozi_hero": ("📤", "Vajine fotografije in videi", "Naloži fotografije",
                    "Izberita postajo in naložita slike ali videe kar s telefona"),
    "izziv_how": [
        ("Izberita izziv", "pri vsaki postaji jih je nekaj. Odprita postajo in poglejta, kaj vaju čaka."),
        ("Naložita fotografijo ali video", "kar s telefona. Prvič vaju vprašamo le, kdo nalaga (Ana ali Maks)."),
        ("Odklenita presenečenje", "zanimivost, skrivnost ali nagrada. Opravljen izziv pade na dno in pokaže sličico."),
    ],
    "izziv_why": "Zakaj to počneta?",
    "izziv_fine": ("Drobni tisk: vsak izziv ima pod seboj »drobni tisk« — zakaj se slikata prav tam in kaj je ta kraj. "
                   "Presenečenja so zanimivosti, legende in majhne nagrade (nobenih izmišljenih kuponov — le pravi predlogi)."),
    "izziv_intro_desc": "Vsi foto izzivi Zmajeve pustolovščine — naložita sliko in izziv je opravljen.",
    "izzivi_intro": ("Naložita fotografijo (ali video) za izziv — takoj se označi kot opravljen in se spodaj pokaže sličica. "
                     "Iz tega nastane vajin skupni album."),
    "nacrt_title": "Načrt poti — Zmajeva pustolovščina",
    "nacrt_desc": "Dvodnevni načrt: Maribor → Ljubljana, Hotel Emonec, Katja, živalski vrt (15.–16. oktober 2026).",
    "nacrt_hero": ("🗺️", "Hrbtenica pustolovščine", "Načrt poti — 2 dneva", "Dan za dnem, od Maribora do živalskega vrta"),
    "kako_title": "Kako uporabljati · Zmajeva pustolovščina",
    "album_title": "📸 Vajin album",
    "kviz_hero": ("🧠", "Preizkusita znanje", "Zmajev kviz", "14 vprašanj o živalih, zmajih in Ljubljani"),
    "kviz_intro": "Odgovori so skriti v zanimivostih na postajah. Vsak odgovor pokaže razlago — tako se vmes tudi kaj naučita.",
    "lov_hero": ("🔎", "Zbirajta na poti", "Zmajev lov", "Označita vsako žival in vsakega zmaja, ki ju opazita"),
    "lov_intro": "Odprita med potjo, tapnita, ko kaj opazita, in na koncu preštejta. Maks šteje zmaje, Ana živali — ali obratno! Označbe ostanejo v vajinem telefonu.",
    "knjiga_hero": ("📖", "Iz vajinih slik", "Zmajeva knjiga", "Fotografije iz albuma po postajah, pripravljene za tisk"),
    "knjiga_intro": "Knjiga se sestavi sama iz slik, ki ju naložita. Z ✕ izpustita slike, ki jih nočeta, nato jo natisneta ali shranita kot PDF.",
    "facts_h": "💡 Še več zanimivosti",
    "rez_hero": ("🧾", "Vse na enem mestu", "Moje rezervacije", "Hotel, vozovnice in vstopnice — vidita jih oba"),
    "dnevnik_hero": ("✍️", "Za Zmajevo knjigo", "Zmajev dnevnik", "Kratek povzetek vsakega dne — iz tega nastane potopis"),
    "zdravje_intro": "Vsak vpiše svoje podatke; vidita jih oba (in delujejo tudi brez interneta). Ob težavi pokažita zdravniku kartico.",
    "izziv_jump": "📸 Poglejta foto izzive",
}

# --------------------------------------------------------------------------- postaje

LOCATIONS = [
    {
        "key": "vlak", "emoji": "🚂", "name": "Z vlakom v Ljubljano", "nav": "Vlak",
        "sub": "Maribor → Ljubljana, prvi del pustolovščine",
        "teaser": "Vlak, okno in dve uri za klepet, igro in prvi zapis v Zmajevo knjigo.",
        "intro": ("Pustolovščina se začne že na peronu. Vlak iz Maribora vaju v približno dveh urah pripelje v Ljubljano — "
                  "mimo vinogradov, rek in hribov. Sedita k oknu, vzemita malico in poglejta, kdo prvi opazi reko Savo."),
        "food": [
            ("Malica za pot", "sendvič, sadje in kaj sladkega — Maks naj izbere, kaj gre v nahrbtnik"),
            ("Voda", "polna steklenička za vsakega, da vama na poti ni treba iskati prodajalne"),
            ("Prigrizek za igro", "suho sadje ali krekerji, ki se ne drobijo — zraven lahko igrata »Vidim, vidim«"),
        ],
        "acts": [
            ("Igra »Vidim, vidim«", "izmenično izbirata predmete ali črke za oknom — zmaga, kdor prvi ugane"),
            ("Prvi zapis v Zmajevo knjigo", "Maks napiše tri stvari, ki se jih najbolj veseli v Ljubljani"),
        ],
        "fact": ("Proga proti Ljubljani je del stare Južne železnice, ki je v 19. stoletju povezala Dunaj s Trstom. "
                 "Pri Zidanem Mostu se reki Savinja in Sava stečeta — in proga potem dolgo sledi reki Savi."),
        "magda": "Zmaj Ljubljane čaka na koncu poti. Ko se pripeljeta, ga poiščita: v mestu je zmajev več, kot si mislita. Preštejeta jih!",
        "phrases": ["Slovenske železnice Maribor Ljubljana vlak", "Zidani Most Sava Savinja"],
    },
    {
        "key": "emonec", "emoji": "🏨", "name": "Hotel Emonec", "nav": "Hotel",
        "sub": "Kovčka odložita, nočitev v središču Ljubljane",
        "teaser": "Wolfova ulica 12: kovčka odložita, pa že lahko raziskujeta mesto — brez težke prtljage.",
        "intro": ("Hotel Emonec je v središču Ljubljane, približno 12 minut hoje od železniške postaje. Takoj ob prihodu odložita prtljago "
                  "(tudi če sobe še niso pripravljene, jo hotelsko osebje običajno shrani), nato pa lahko lahkotno odkrivata mesto. "
                  "Zvečer se vrneta, počijeta in se naslednje jutro odpravita v živalski vrt."),
        "food": [
            ("Zajtrk", "preverita, ali je zajtrk vključen — če je, naj bo velik, saj vaju čaka dolg dan v živalskem vrtu"),
            ("Večerja v bližini", "v središču je veliko izbire; Maks naj izbere, ali bo juha, testenine ali nekaj slovenskega"),
            ("Malica za jutri", "v nahrbtnik si pripravita sadje in vodo za živalski vrt"),
        ],
        "acts": [
            ("Odložita kovčka", "še pred sprehodom — in poglejta, kje so zajtrk, dvigalo in stopnice (zaradi pustolovščine!)"),
            ("Večerni sprehod", "kratek krog po razsvetljenem središču, nato zgodaj spat — jutri je velik dan"),
        ],
        "fact": ("Ime »Emonec« spominja na Emono — rimsko mesto, ki je pred skoraj 2000 leti stalo na območju današnje Ljubljane. "
                 "Ostanke rimskega zidu še vedno vidite v mestu."),
        "magda": "Pred spanjem naj Maks poišče na zemljevidu živalski vrt — in mami pove, katero žival se najbolj veseli. Spanje bo takrat prišlo kar samo.",
        "phrases": ["Hotel Emonec Ljubljana", "Emona rimsko mesto Ljubljana"],
    },
    {
        "key": "center", "emoji": "🏰", "name": "Ljubljana s Katjo", "nav": "Center",
        "sub": "Zmaji, mostovi, grad in sladoled z najboljšo družbo",
        "teaser": "Katja, zmajski most, grad nad mestom in kaj slastnega ob reki.",
        "intro": ("Prvi popoldan je za mesto in za prijateljico Katjo. Ljubljana je majhna in prijazna — vse zanimivo je znotraj "
                  "nekaj sto metrov: Tromostovje, Prešernov trg, Zmajski most, reka Ljubljanica in nad vsem grad. "
                  "Spodaj je več idej; izberita tiste, ki vama (in Katji) ustrezajo — ni treba vsega."),
        "food": [
            ("Sladoled ali topla čokolada", "ob Ljubljanici — Maks izbere okus, Katja in Ana pa poskusita po koščku"),
            ("Štruklji", "slovenska specialiteta — zavit testo z nadevom (sirovi, orehovi, tarhonja). Poskusita v kakšni gostilni"),
            ("Sezonski prigrizki na tržnici", "oktober je čas jabolk, kostanja in medu"),
        ],
        "acts": [
            ("Tromostovje in Prešernov trg", "osrednji točki mesta, kjer se večina stvari začne"),
            ("Zmajski most", "poiščita vse štiri zmaje"),
            ("Ljubljanski grad", "peš ali z vzpenjačo — razgled na celo mesto"),
        ],
        "fact": ("Zmaj je simbol Ljubljane. Po izročilu je v močvirju ob reki zmaja premagal Jazon, vodja Argonavtov, ki naj bi se "
                 "z zlatim runom vračal domov po Ljubljanici. Zato je zmaj na mestnem grbu, na mostu in tudi na gradu."),
        "magda": "Na Zmajskem mostu vsak izmed vas izbere svojega zmaja — in mu da ime. Potem ga iščite po vsem mestu.",
        "phrases": ["Ljubljana Dragon Bridge walking tour", "Ljubljanski grad vzpenjača"],
    },
    {
        "key": "zoo", "emoji": "🦁", "name": "Živalski vrt Ljubljana", "nav": "Živalski vrt",
        "sub": "Cel dan med slonom, žirafami, tigri in morskimi levi",
        "teaser": "Glavni dan: poglobljen načrt, 15 izzivov in veliko živali. Slon Ganga čaka!",
        "intro": ("Živalski vrt leži na južnem pobočju Rožnika, v gozdu in na travnikih, ki so del krajinskega parka. "
                  "Površine je okoli 19,6 hektara, poti pa je po objavljenih podatkih 5–6 km — dovolj za cel dan raziskovanja. "
                  "Spodaj je predlog poti od vhoda do izhoda, s krmljenji, igrišči, odmori in 15 izzivi za Zmajevo knjigo. "
                  "Malo načrta, veliko radovednosti!"),
        "food": [
            ("Sladoled in prigrizek v živalskem vrtu", "po objavljenih podatkih je v vrtu restavracija s sladoledom — idealen odmor po Mini ZOO"),
            ("Piknik z lastno malico", "klopi so pod drevesi; Maks naj izbere, katera žival ju bo gledala med malico"),
            ("Topla juha po obisku", "ko se zunaj ohladi, vroč napitek pomaga — oktobra zna biti ob pobočju hladno"),
        ],
        "acts": [
            ("Slonica Ganga", "poglejta, kako je velika — in kaj vse poje"),
            ("Morski levi", "poglejta trening in napajanje (po urniku)"),
            ("Mini ZOO", "tukaj se smeta živali nežno dotakniti — počepnita in počakata, da pride sama"),
        ],
        "fact": ("Živalski vrt Ljubljana je bil ustanovljen leta 1949 in je od leta 1951 na današnji lokaciji pod Rožnikom. "
                 "Slonica Ganga tam živi od leta 1977 in je najstarejša prebivalka vrta."),
        "magda": ("Za trenutek se ustavita pri kakšni živali, ki je najbolj mirna, in 2 minuti samo opazujta — brez telefona. "
                  "Kaj dela? Kaj bi počela, če bi bila ona? To je pogosto najlepši spomin dneva."),
        "phrases": ["Ljubljana Zoo Slovenia visit", "ZOO Ljubljana slon Ganga", "ZOO Ljubljana morski levi"],
    },
    {
        "key": "domov", "emoji": "🏠", "name": "Domov z zmajem", "nav": "Domov",
        "sub": "Povratek v Maribor in zadnji zapisi",
        "teaser": "Vlak domov, spominek in zadnja slika Zmajeve knjige.",
        "intro": ("Po živalskem vrtu se vrneta v središče po prtljago in na vlak. Za povratek izberita vlak glede na uro, ko "
                  "zapustita zoo (vozne rede preverita na potniski.sz.si). Med vožnjo naj Maks v zvezek napiše tri najboljše stvari "
                  "iz teh dveh dni, Ana pa tri, ki jih je Maks presenetil."),
        "food": [
            ("Malica za vlak", "sendvič ali sadje, če se vožnja zavleče"),
            ("Topla juha pred potjo", "če je še čas, v središču kaj toplega"),
        ],
        "acts": [
            ("Spominek za domov", "izberita skupaj — lahko je majhen zmaj, razglednica ali žival iz zoo"),
            ("Zmajev dnevnik", "vsak napiše svoje tri najboljše stvari dneva"),
        ],
        "fact": ("Slovenija je majhna država, a ima veliko različnih krajev: od Maribora na vzhodu do Ljubljane v sredini — "
                 "in to pot vlak prevozi v približno dveh urah."),
        "magda": "Ko prideta domov, najprej poiščita pet najboljših slik in jih izberita za Zmajevo knjigo. To je lepši nalogi kot pospravljanje kovčka.",
        "phrases": ["Slovenske železnice vlak", "Maribor Ljubljana vlak"],
    },
]

# --------------------------------------------------------------------------- zemljevidi
MAPS = {
    "vlak":   (46.0582, 14.5103, 14, "Železniška postaja Ljubljana, Trg osvobodilne fronte"),
    "emonec": (46.0508, 14.5050, 16, "Hotel Emonec, Wolfova ulica 12, Ljubljana"),
    "center": (46.0516, 14.5085, 15, "Prešernov trg, Ljubljana"),
    "zoo":    (46.0553, 14.4722, 16, "Živalski vrt Ljubljana, Večna pot 70"),
    "domov":  (46.0582, 14.5103, 14, "Železniška postaja Ljubljana, Trg osvobodilne fronte"),
}

# --------------------------------------------------------------------------- vodnik po postajah
GUIDE = {
    "vlak": {
        "key": "vlak",
        "sights": [
            {"name": "Peron in vlak", "desc": "Vlak vaju z mariborske postaje pripelje v Ljubljano v približno dveh urah. Preverita peron in uro na tabli ter sedeža pri oknu.",
             "tip": "Vozovnici kupita vnaprej na potniski.sz.si ali na blagajni; za otroka velja otroška cena.",
             "maps": "Železniška postaja Maribor"},
            {"name": "Železniška postaja Ljubljana", "desc": "Ob prihodu izstopita na glavni postaji; do Hotela Emonec je okoli 12 minut peš po središču.",
             "tip": "Ostanita skupaj in pojdita počasi — v zoo ju bo čakalo veliko hoje.",
             "maps": "Železniška postaja Ljubljana"},
        ],
        "practical": [
            "Vozni red in vozovnice: potniski.sz.si ali na blagajni — točno uro odhoda preverita nekaj dni pred potjo.",
            "Nahrbtnik za vsakega: voda, malica, polnilec, dežnik; kovčki naj imajo kolesca (do hotela je kratka pot peš).",
            "Peron preverita na tabli ali v obvestilih; do vlaka pridita pet minut prej.",
        ],
    },
    "emonec": {
        "key": "emonec",
        "sights": [
            {"name": "Hotel Emonec", "desc": "Hotel v središču mesta, Wolfova ulica 12. Od železniške postaje do hotela je okoli 12 minut hoje; do Prešernovega trga in reke Ljubljanice je le nekaj minut.",
             "tip": "Na recepciji vprašajta za shranjevanje prtljage, uro odjave in zajtrk.",
             "maps": "Hotel Emonec, Wolfova ulica 12, Ljubljana"},
            {"name": "Stolnica sv. Nikolaja", "desc": "Največja cerkev v mestu in v bližini hotela. Poglejta bronasta vrata s prizori iz zgodovine — izdelana so bila ob obisku papeža leta 1996.",
             "tip": "Kratek postanek je možen tudi, če se cerkev ravno ne odpre — vrata si lahko ogledata od zunaj.",
             "maps": "Stolnica sv. Nikolaja, Ljubljana"},
        ],
        "practical": [
            "Pred odhodom sporočita hotelu, kdaj prideta (da pripravijo prtljago in sobo).",
            "Zvečer: priprava nahrbtnika za zoo — malica, voda, dežnik, polnilec, zvezek za zapiske.",
            "Zajtrk je lahko dolg — da pridemo v zoo ob odprtju (ob 9.00), vstanita zgodaj.",
        ],
        "day_plan": [
            {"time": "Ob prihodu", "what": "Odložita kovčka v hotelu (če soba še ni pripravljena, prtljago shranijo) in lahkotno krenita v mesto."},
            {"time": "Zvečer", "what": "Večerja, večerni sprehod, nato zgodaj spat. Jutri vaju čaka živalski vrt!"},
        ],
    },
    "center": {
        "key": "center",
        "sights": [
            {"name": "Tromostovje in Prešernov trg", "desc": "Tromostovje, ki ga je oblikoval Jože Plečnik (okoli 1929–1932), je trojica mostov na enem mestu. Na Prešernovem trgu stoji kip pesnika Franceta Prešerna — verzi njegove Zdravljice so slovenska himna.",
             "tip": "Srečanje s Katjo je idealno na Prešernovem trgu — vsi ga poznajo.",
             "maps": "Tromostovje, Ljubljana", "yt": "Ljubljana Triple Bridge Plečnik"},
            {"name": "Zmajski most", "desc": "Most z zelenimi zmaji stoji ob reki Ljubljanici. Na vsakem koncu ga čuvata dva zmaja, skupaj štirje. Zmaj je simbol mesta in je tudi na mestnem grbu.",
             "tip": "Vsak naj si izbere svojega zmaja in mu da ime — potem ga iščita po vsem mestu.",
             "maps": "Zmajski most, Ljubljana", "yt": "Ljubljana Dragon Bridge"},
            {"name": "Ljubljanski grad", "desc": "Grad nad mestom je viden od povsod. Nanj se lahko povzpnete peš ali z vzpenjačo (Krekov trg); zgoraj je razgled na celo mesto, če je dan jasen — tudi na Kamniško-Savinjske Alpe.",
             "tip": "Če vaju čas zanima, poglejta, ali se na gradu odvijajo kakšne otroške delavnice — na gradu je tudi lutkovni muzej.",
             "maps": "Ljubljanski grad", "yt": "Ljubljana Castle funicular"},
            {"name": "Plečnikova tržnica", "desc": "Osrednja ljubljanska tržnica ob reki, delo arhitekta Plečnika. Dopoldne so stojnice polne sadja, medu, sira in oktobrskih dobrot.",
             "tip": "Tržnica je odprta predvsem dopoldne in ob nedeljah večinoma zaprta; popoldne so stojnice že redkejše.",
             "maps": "Osrednja tržnica Ljubljana, Plečnikove arkade"},
            {"name": "Hiša eksperimentov", "desc": "Muzej, kjer smeš vse poskusiti sam: zvok, svetloba, magneti, optične iluzije. Odličen za Maksa.",
             "tip": "Po zadnjih objavljenih podatkih je odprta torek–četrtek dopoldne (10.00–13.00) — pred obiskom preverita na spletu. Naslov: Trubarjeva cesta 39.",
             "maps": "Hiša eksperimentov, Trubarjeva cesta 39, Ljubljana", "yt": "Hiša eksperimentov Ljubljana"},
            {"name": "Tivoli", "desc": "Največji mestni park, nekaj minut od središča. Jeseni so drevesa zlata in rdeča; v parku je več igrišč in sprehajalnih poti.",
             "tip": "Če imata še energijo in si vzameta uro, je to idealen sprehod s Katjo.",
             "maps": "Park Tivoli, Ljubljana"},
        ],
        "practical": [
            "Središče je večinoma peš cona — vse, kar je zanimivo, je blizu: do vsega je 5–15 minut hoje.",
            "Vzpon na grad: peš po poti (približno 10–15 minut navkreber) ali z vzpenjačo — izberita glede na energijo.",
            "Urnike (grad, vzpenjača, Hiša eksperimentov) vedno preverita dan prej — oktobra so lahko skrajšani.",
            "Najboljši čas za sprehod po središču: popoldne, ko se mesto prižge v zlati svetlobi.",
        ],
        "day_plan": [
            {"time": "Popoldne", "what": "Srečanje s Katjo (npr. na Prešernovem trgu), skupen sprehod po Tromostovju in Zmajskem mostu; izberita še eno stvar: grad ali Hišo eksperimentov."},
            {"time": "Pozno popoldne", "what": "Sladoled ali topla čokolada ob Ljubljanici, nato počasi proti hotelu."},
            {"time": "Zvečer", "what": "Večerja v središču (Maks izbere), zgodaj nazaj v hotel."},
        ],
        "food_categories": [
            {"name": "Sladoled in slaščice ob reki", "emoji": "🍦",
             "intro": "Središče Ljubljane je polno slaščičarn in sladoledarn. Izberita kar tisto, ki ima najdaljšo vrsto otrok.",
             "places": [
                 {"name": "Sladoled blizu Ljubljanice", "desc": "V Google Zemljevidih poiščita »sladoled« v središču in izberita najbolje ocenjeno sladoledarno; oktobra so lahko okusi bolj jesenski (kostanj, jabolko, čokolada).",
                  "price": "€", "maps": "sladoled Ljubljana center"},
                 {"name": "Topla čokolada ali čaj", "desc": "Če je hladno, se ogrejeta ob topli čokoladi. V središču je več kavarn z bogatimi napitki.",
                  "price": "€", "maps": "topla čokolada Ljubljana center"},
             ]},
            {"name": "Kosilo in večerja v središču", "emoji": "🍽️",
             "intro": "Izberita kaj, kar bo všeč tudi Maksu — in poskusita vsaj eno slovensko jed.",
             "places": [
                 {"name": "Gostilna s štruklji", "desc": "V Googlu poiščita »štruklji Ljubljana« — več gostiln v središču jih ponuja. Naročita en sladki in en slani štrukelj in si ju razdelita.",
                  "price": "€€", "maps": "gostilna štruklji Ljubljana center"},
                 {"name": "Pica ali testenine", "desc": "Če Maks ne mara eksperimentov: v središču je dovolj dobrih piceric in italijanskih restavracij ob reki.",
                  "price": "€€", "maps": "pizzeria Ljubljana center"},
             ]},
        ],
    },
    "zoo": {
        "key": "zoo",
        "sights": [
            {"name": "Vhod in zemljevid", "desc": "Zoo je odprt vsak dan; oktobra po objavljenih podatkih od 9.00 do 18.00 (točno uro zadnjega vstopa preverita na zoo.si). Na vhodu vzemita zemljevid — Maks je »kapitan poti« in izbere prvo žival.",
             "tip": "Vstopnice lahko kupita tudi vnaprej na spletu (trgovina.zoo.si) in se izogneta vrsti.",
             "maps": "Živalski vrt Ljubljana, Večna pot 70"},
            {"name": "Slonica Ganga", "desc": "Azijska slonica Ganga živi v ljubljanskem živalskem vrtu že od leta 1977 — najstarejša je med prebivalci. Odrasel azijski slon poje na dan več deset kilogramov hrane.",
             "tip": "Opazujta, kako s hobotom pobira hrano — hobot ima neverjetno veliko mišic in je hkrati nos, roka in cev za pitje.",
             "maps": "Živalski vrt Ljubljana sloni", "yt": "ZOO Ljubljana slon Ganga"},
            {"name": "Žirafe", "desc": "Žirafe so najvišje kopenske živali. Jezik, s katerim objemajo vejice, je dolg tudi do 50 cm in temno modrikast, da se ne opeče na soncu.",
             "tip": "Ugibajta: koliko Maksov je visoka žirafa? Najprej ugibata, nato primerjata s sliko.",
             "maps": "Živalski vrt Ljubljana žirafe", "yt": "giraffe feeding zoo"},
            {"name": "Tigri in veliki mački", "desc": "V vrtu živijo sibirski tigri — največje mačke na svetu. Vsak tiger ima unikatne črte, kot človek prstni odtis.",
             "tip": "Če tigra ne vidita takoj, poiščita sledi: tace, praske na deblu, utrujen pogled mačk, ki spi na skali.",
             "maps": "Živalski vrt Ljubljana tigri", "yt": "Siberian tiger zoo"},
            {"name": "Morski levi", "desc": "Kalifornijski morski levi so zabavni: plavajo, se podijo in se učijo trikov. Za razliko od tjulnjev imajo majhne zunanje ušesne školjke.",
             "tip": "Po nekaterih virih je trening dvakrat dnevno (npr. okoli 11.00 in 17.00) — točno uro preverita na vhodu ali zoo.si.",
             "maps": "Živalski vrt Ljubljana morski levi", "yt": "California sea lion training zoo"},
            {"name": "Mini ZOO", "desc": "Prostor za otroke in manjše živali: koze, ovce in druge domače živali, ki jih smeš nežno pobožati. Pravilo: počepnita, počakata, da pride žival sama; ne hranita, ne lovita, ne dvigajta.",
             "tip": "Mini ZOO je pri ogradi guanak, nasproti jelenov (za vivarijem).",
             "maps": "Mini ZOO Živalski vrt Ljubljana"},
            {"name": "Volkovi, medvedi in domača divjad", "desc": "V slovenskih gozdovih živi več sto rjavih medvedov in tudi volkovi; v vrtu si lahko ogledata, kako velika je medvedja šapa. Ris je bil pri nas ponovno naseljen leta 1973.",
             "tip": "Živali so običajno najbolj aktivne zjutraj in pozno popoldne — opoldne pogosto počivajo.",
             "maps": "Živalski vrt Ljubljana medvedi"},
            {"name": "Rdeče pande, opice in drobne živali", "desc": "Rdeča panda ni v sorodu z velikim pando, je pa ena najbolj ljubkih živali. Kaj vse še živi v vrtu, ugotovita sama: na zemljevidu iščita opice, ptice in majhne sesalce.",
             "tip": "Živali se menjajo — če katere ni, poiščita naslednjo. Pomembno je, da hodita počasi in opazujeta.",
             "maps": "Živalski vrt Ljubljana"},
            {"name": "Vivarij in terariji", "desc": "Kače, kuščarji, žabe in druge plazilke in dvoživke. Tukaj je toplo in vlažno — dobro mesto za krajšo pavzo, če zunaj piha.",
             "tip": "Poiščita najmanjše in največje bitje in jima izberita imeni.",
             "maps": "Vivarij Živalski vrt Ljubljana"},
            {"name": "Igrišči in odmor", "desc": "V vrtu sta dve igrišči, med njima novejše z afriško temo. Tudi sladoled in prigrizek sta tam; ob lepem vremenu je odmor na travniku pravi zaklad.",
             "tip": "Odmor načrtujta za sredino poti, ko sta že malo utrujena — potem imata moč za drugi del.",
             "maps": "igrišče Živalski vrt Ljubljana"},
        ],
        "practical": [
            "Zoo je na pobočju Rožnika — poti so ponekod strme. Obujta udobne, nepremočljive čevlje, ki jih ne bo škoda zmočiti.",
            "Oktobra je lahko hladno in vlažno: vzemita jakno, kapo in nepremočljivo plast; dežnik je lahko v nahrbtniku.",
            "Živali spoštujemo: ne hranimo, ne kričimo, ne tolčemo po steklu. Živalim je potreben mir.",
            "Psi so dobrodošli s kupljeno vstopnico, vendar v Mini ZOO, ograjo Avstralije in na otroška igrišča ne smejo.",
            "Informacije: info@zoo.si, telefon +386 1 24 42 190. Urnik krmljenja in treningov je običajno objavljen ob vhodu in na zoo.si.",
        ],
        "day_plan": [
            {"time": "9.00", "what": "Prihod z avtobusom št. 18 (postaja »Živalski vrt«). Vzemita zemljevid, kupita vstopnici (ali jih že imata) in se slikata pod vhodom."},
            {"time": "9.30", "what": "Prvi del poti: slon Ganga, žirafe in tigri — najbolj »velike« živali, ko so še spočite in aktivne. Za vsako žival izpolnita izziv."},
            {"time": "11.00", "what": "Morski levi: trening ali napajanje — po objavljenem urniku. Poglejta, kako se levi učijo trikov."},
            {"time": "12.00", "what": "Odmor: malica ali sladoled. Poglejta zemljevid in izberita, kaj gresta gledat po kosilu."},
            {"time": "13.00", "what": "Mini ZOO: pobožajta koze in ovce po pravilih. Poiščita vivarij in igrišče — Maks izbere, kje se zadržita dlje."},
            {"time": "14.30", "what": "Druga polovica poti: volk, medved, rdeče pande, opice in ptice. Hodita počasi in opazujta — katera žival jima je najbolj smešna?"},
            {"time": "16.00", "what": "Zadnji postanek: trgovinica z darili (izberita en spominek) in zadnja slika pri izhodu. Nato avtobus nazaj v središče."},
        ],
        "food_categories": [
            {"name": "Prigrizek v živalskem vrtu", "emoji": "🍦",
             "intro": "Po objavljenih podatkih je v vrtu restavracija s sladoledom in prigrizki — dobra pavza sredi dneva.",
             "places": [
                 {"name": "Restavracija v živalskem vrtu", "desc": "Sladoled, topli napitki in preprosti obroki; urnik preverita ob prihodu.",
                  "price": "€", "maps": "Restavracija Živalski vrt Ljubljana"},
             ]},
        ],
    },
    "domov": {
        "key": "domov",
        "sights": [
            {"name": "Vlak domov", "desc": "Vlak iz Ljubljane v Maribor traja približno dve uri. Izberita odhod glede na čas, ko zapustita zoo, in pojdita na postajo vsaj 15 minut prej.",
             "tip": "Vozni red preverita na potniski.sz.si. Če si nista kupila povratne vozovnice, na blagajni ali v aplikaciji kupita novo.",
             "maps": "Železniška postaja Ljubljana"},
            {"name": "Spominek za Zmajevo knjigo", "desc": "Lahko je majhen zmaj, razglednica ali žival iz zoo. Izberita skupaj in ga prilepita v dnevnik.",
             "tip": "Vozovnici (vlak) sta tudi spomin — prilepita ju v knjigo!",
             "maps": "Ljubljana trgovina z darili center"},
        ],
        "practical": [
            "Pred vlakom preverita, ali imata vse stvari (telefon, polnilec, jakne, kovčka v hotelu). Ana naj preveri hotel.",
            "Če se vlak zamudi ali ga zamudita, povprašajta pri blagajni/informacijah Slovenskih železnic o naslednjem vlaku.",
        ],
    },
}

# --------------------------------------------------------------------------- dodatki (kje prespati, če dežuje)
EXTRAS = {
    "emonec": {
        "prespati": "Hotel Emonec, Wolfova ulica 12, Ljubljana (nočitev 15.–16. oktobra). Odjavo preverita v potrditvi rezervacije; prtljago smeta pustiti na recepciji, dokler ne odideta na vlak.",
        "dez": "Če dežuje: ostanita pod streho — počitek v sobi, kratek sprehod pod arkadami in zgodnja večerja v bližini.",
    },
    "center": {
        "dez": "Če dežuje: Hiša eksperimentov (če je odprta), muzej ali kavarna s toplo čokolado. Dežnika v nahrbtnik.",
    },
    "zoo": {
        "dez": "Če dežuje: zoo je deloma pod streho — vivarij in terariji, notranji prostori z živalmi; vzemita dežnik ali pelerino. Živali v dežju so pogosto bolj skrivnostne.",
    },
    "vlak": {"dez": "Če dežuje: pod streho vlaka je še bolje — igra in zapisek v zvezek."},
}

# --------------------------------------------------------------------------- osebne rubrike
RUBRICS = {
    "vlak": {
        "najlepsi_trenutek": "Ko vlak odpelje in oba pogledata skozi okno: kaj vidita prvo? Zapišita in preštejta, koliko sprememb pokrajine opazita na poti.",
        "ura_zase": "Dve uri v vlaku sta lep čas za pogovor: Ana vpraša Maksa, katero žival bi bil, če bi bil žival — in zakaj.",
        "mandala": "Narišita zmaja Ljubljane po svoje: kakšna barva, krila, rep? To je prvi zmaj Zmajeve knjige.",
    },
    "emonec": {
        "najlepsi_trenutek": "Ko odpreta vrata sobe: kdo prvi ugotovi, kaj je v omari ali na polici? Skupaj izberita stran postelje.",
        "ura_zase": "Pol ure počitka po prihodu: Maks nariše načrt jutrišnjega dne v zoo, Ana si v miru privošči čaj.",
        "mandala": "Narišita hotelsko sobo ali okno z razgledom — in poimenujta, kaj vidita skozi njega.",
    },
    "center": {
        "najlepsi_trenutek": "Ko se z reke zasvetijo prve luči in se odsevajo v vodi. Skupaj se ustavita in samo pogledata.",
        "ura_zase": "Ana in Katja si vzameta pol ure ob kavi ali čaju, Maks pa gre na kratko igro okoli (v bližini) — ali pa si naroči sladoled.",
        "mandala": "Narišita Zmajski most z vsemi štirimi zmaji — in vsakemu dajta ime.",
    },
    "zoo": {
        "najlepsi_trenutek": "Ko pri kateri živali oba obstojita in nista rekla ničesar. Zapišita, kaj je bilo to in zakaj si ga bosta zapomnila.",
        "ura_zase": "Odmor za dva: malica na klopci, pol ure brez telefona; vsak pove najlepšo žival do zdaj.",
        "mandala": "Vsak nariše svojo žival — tisto, ki jo je videl danes, ali pa novo: zmes dveh živali (npr. slon s pasovi tigra).",
    },
    "domov": {
        "najlepsi_trenutek": "Ko vlak odpelje iz Ljubljane in sta oba utrujena, a srečna. Zapišita eno stvar, ki je bila boljša, kot sta pričakovala.",
        "ura_zase": "V vlaku naj Ana zapiše tri stvari, ki jo je Maks presenetil; Maks pa tri, ki jih je naredila mama najbolje.",
        "mandala": "Maks nariše, kaj bo prvo povedal prijateljem, ko pride v šolo.",
    },
}

# --------------------------------------------------------------------------- foto izzivi (največ v zoo)
IZZIVI = {
    "vlak": [
        {"t": "foto", "x": "Ana in Maks skupaj na peronu v Mariboru, preden pride vlak.",
         "w": "Vsaka pustolovščina ima začetek — to je vajin »štart«. Na koncu dneva primerjata, kako sta bila videti zjutraj in zvečer (po zoo!).",
         "p": {"k": "zanimivost", "h": "Prvi vlaki v Ljubljano",
               "x": "Ljubljana je dobila železnico sredi 19. stoletja, ko so zgradili Južno železnico Dunaj–Trst — pred tem je potovanje do Dunaja trajalo več dni."}},
        {"t": "foto", "x": "Skozi okno: najlepši razgled, ki ga opazita na poti (vinogradi, reka ali hribi).",
         "w": "Proga pri Zidanem Mostu sledi reki Savi — zato je med vožnjo pogosto viden zelen rečni breg.",
         "p": {"k": "skrivnost", "h": "Skrivnost reke Save",
               "x": "Pri Zidanem Mostu se Savinja izliva v Savo. Poiščita ga na zemljevidu — in ugotovita, koliko rek je še v bližini."}},
        {"t": "video", "x": "10-sekundni video zvokov vlaka: kolesa na tirih, obvestila, korak. Ugibata, kje se ravno vozita.",
         "w": "Vsak kraj ima svoj zvok — in zvok vlaka je eden najbolj značilnih spominov na potovanje.",
         "p": {"k": "nagrada", "h": "Nagrada: malica po Maksovi izbiri",
               "x": "Maks izbere, kaj bosta pojedla med vožnjo (sadje, sendvič ali sladkarija) — in Ana prizna, da je izbral odlično."}},
        {"t": "foto", "x": "Lov na črko Z: poiščita tri napise z začetno črko Z (Zidani Most, ZOO, zmaj …).",
         "w": "Črka Z je zmajeva črka: Zidani Most, Zoo, Zmaj — poglejta, koliko jih najdeta in napišita seznam.",
         "p": {"k": "skrivnost", "h": "Skrivnost zmaja",
               "x": "V Ljubljani je zmajev več, kot si mislita: na mostu, na gradu in celo na mestnem grbu. Preštejta jih in zapišita število v Zmajevo knjigo!"}},
        {"t": "foto", "x": "Vozovnici (ali vozovnica in malica) kot trofeja — skupaj na mizi.",
         "w": "Vozovnica je prvi »predmet« v vajinem potopisu. Prilepita jo v zvezek: čez leta bo spomin na to pot.",
         "p": {"k": "zanimivost", "h": "Prva vozovnica",
               "x": "Vozovnice so včasih bile kartonaste, z dnevnim žigom. Danes jih imate v telefonu — a vozovnica na papirju je lepa trofeja."}},
    ],
    "emonec": [
        {"t": "foto", "x": "Kovčka pred vhodom Hotela Emonec — Ana in Maks za njima.",
         "w": "Dokaz, da sta prispela! Hotel je v središču mesta, na Wolfovi ulici 12.",
         "p": {"k": "zanimivost", "h": "Emona — rimsko mesto",
               "x": "Ime »Emonec« spominja na Emono, rimsko mesto na območju današnje Ljubljane. Staro je skoraj 2000 let. Ostanke rimskega zidu še vedno vidite v mestu.", "m": "Rimski zid Ljubljana"}},
        {"t": "foto", "x": "Pogled skozi hotelsko okno (ali s hodnika): kaj vidita od tam?",
         "w": "Ljubljana je polna zvonikov. V bližini hotela je stolnica sv. Nikolaja (okoli 350 m) — poiščita njen zvonik.",
         "p": {"k": "zanimivost", "h": "Vrata s prizori",
               "x": "Glavna bronasta vrata stolnice sv. Nikolaja so bila izdelana ob obisku papeža leta 1996 in prikazujejo prizore iz zgodovine. Poglejta jih, ko greta mimo.", "m": "Stolnica sv. Nikolaja Ljubljana"}},
        {"t": "foto", "x": "Zamenjava vlog: Maks je fotograf Ane, Ana fotografinja Maksa — ena slika pred hotelom.",
         "w": "Najboljše slike nastanejo, ko ju posname druga oseba. Zamenjata vlogi in naredita smešno pozo.",
         "p": {"k": "nagrada", "h": "Nagrada: fotograf dneva",
               "x": "Kdor je posnel boljšo sliko, dobi naslov »fotograf dneva« — in izbere večerjo."}},
        {"t": "video", "x": "Hotelska soba v 10 sekundah: Maks je turistični vodnik in predstavi sobo.",
         "w": "Hotelske sobe so kot male hiške. Pokažita, kaj vama je najbolj všeč.",
         "p": {"k": "nagrada", "h": "Nagrada: izbira postelje",
               "x": "Maks izbere, katero stran sobe (ali kateri sedež ob oknu) ima. Poštena delitev: jutri izbira Ana."}},
        {"t": "foto", "x": "Zadnja slika dneva: utrujena in nasmejana, pripravljena na spanje.",
         "w": "Včasih je najboljša slika tista, ko sta utrujena in srečna.",
         "p": {"k": "skrivnost", "h": "Jutranja skrivnost",
               "x": "Jutri vaju čaka slon s hobotom, ki ima neverjetno veliko mišic. Zgodaj spat — in zjutraj izveta več!"}},
    ],
    "center": [
        {"t": "foto", "x": "Ana, Maks in Katja skupaj — na Prešernovem trgu ali na Tromostovju.",
         "w": "Prva skupna slika s Katjo je »dokaz srečanja«. Poiščita zanimivo ozadje (kip, most ali reka).",
         "p": {"k": "zanimivost", "h": "Prešeren in Zdravljica",
               "x": "Na Prešernovem trgu stoji kip pesnika Franceta Prešerna. Njegova pesem Zdravljica je slovenska himna — pravzaprav njena sedma kitica.", "m": "Prešernov trg Ljubljana"}},
        {"t": "foto", "x": "Tromostovje: trije mostovi na enem mestu — poiščita najboljši kot za sliko.",
         "w": "Tromostovje je delo arhitekta Jožeta Plečnika (okoli 1929–1932): ob starem mostu je dodal še dva za pešce.",
         "p": {"k": "zanimivost", "h": "Zakaj trije?",
               "x": "Ob osrednjem mostu sta dodana dva ožja, za pešce — tako se mesto ni preveč razširilo, mostovi pa so postali slavni.", "m": "Tromostovje Ljubljana"}},
        {"t": "foto", "x": "Zmajski most: vsak izbere svojega zmaja in se slika z njim. Kako ga poimenujeta?",
         "w": "Na vsakem koncu mostu stojita dva zmaja, skupaj štirje. Zmaj je simbol mesta.",
         "p": {"k": "zanimivost", "h": "Zmaj Ljubljane",
               "x": "Po izročilu je zmaja v močvirju ob reki premagal Jazon, vodja Argonavtov, ki naj bi se z zlatim runom vračal po Ljubljanici. Zato je zmaj na mestnem grbu.", "m": "Zmajski most Ljubljana"}},
        {"t": "foto", "x": "Zmajski lov: najdita še vsaj tri druge zmaje v mestu (na grbu, kipu ali hiši).",
         "w": "Kdor dobro gleda, v Ljubljani zmajev ne manjka. Preštejta jih.",
         "p": {"k": "skrivnost", "h": "Zmajeva skrivnost",
               "x": "Zapišita število zmajev, ki sta jih našla. Jutri v zoo ugotovita, katera žival je zmaju najbolj podobna."}},
        {"t": "video", "x": "Panorama z gradu (ali kratka vožnja z vzpenjačo) — če se odločita za grad.",
         "w": "Pogled z gradu je najboljši razgled na mesto in strehe starega mestnega jedra.",
         "p": {"k": "zanimivost", "h": "Grad nad mestom",
               "x": "Ljubljanski grad stoji na vzpetini nad starim mestnim jedrom. Z razglednega stolpa vidita celo mesto in — ob jasnem dnevu — gore v daljavi.", "m": "Ljubljanski grad"}},
        {"t": "foto", "x": "Odsev v reki Ljubljanici — poglejta, kaj vse vidita v vodi (in naredita sliko).",
         "w": "Ljubljanica ima na svoji poti več imen (Pivka, Unica, Ljubljanica …) in so ji včasih rekli »reka sedmerih imen«.",
         "p": {"k": "skrivnost", "h": "Skrivnost reke",
               "x": "Del reke teče pod zemljo (kraške jame in ponori). Ko vidita Ljubljanico v mestu, je to le zadnji del njene poti."}},
        {"t": "foto", "x": "Sladoled ali topla čokolada s Katjo — trije kozarci/skodelice, vsak drugačen okus.",
         "w": "Kavarne in sladoledarne ob reki so pravi del mestnega življenja. Napitnine so pri nas dobrodošle, a prostovoljne.",
         "p": {"k": "nagrada", "h": "Nagrada: okus po Maksovi izbiri",
               "x": "Maks izbere nov okus (ali napitek), Katja in Ana poskusita po koščku — in vsak ugiba, kateri je Maksov izbor."}},
        {"t": "foto", "x": "Najbolj barvita stojnica na tržnici (sadje, zelenjava, med) — če greste dopoldne.",
         "w": "Plečnikova tržnica je delo istega arhitekta kot Tromostovje. Oktobra: jabolka, hruške, bučke in med.",
         "p": {"k": "zanimivost", "h": "Plečnikove arkade",
               "x": "Arhitekt Jože Plečnik je mesto oblikoval v več delih: mostovi, tržnica, park, knjižnica. Mnogi pravijo, da je Ljubljano »naredil po svoji meri«.", "m": "Osrednja tržnica Ljubljana"}},
        {"t": "foto", "x": "Hiša eksperimentov: slika Maksa pri svojem najljubšem eksperimentu (če je odprta).",
         "w": "V muzeju se vsi eksperimenti smejo poskusiti. Maks je »znanstvenik dneva«.",
         "p": {"k": "nagrada", "h": "Nagrada: znanstvenik dneva",
               "x": "Maks izbere eksperiment, ki ga pokaže Katji in Ani — razlaga naj bo kratka in zabavna.", "m": "Hiša eksperimentov Trubarjeva cesta 39 Ljubljana"}},
        {"t": "foto", "x": "Najbolj nenavadna stvar v mestu: vsak izbere in fotografira svojo — nato ugibajo, kaj je kdo izbral.",
         "w": "Najbolj nenavadne stvari so včasih najbolj zanimive. Poiščita kakšen čuden kip, napis ali balkon.",
         "p": {"k": "skrivnost", "h": "Skrivni kotiček",
               "x": "Vsak mesto skriva majhne skrivnosti — tiste, ki jih vidita le, če se ustavita. Danes sta jih našla vsaj tri."}},
    ],
    "zoo": [
        {"t": "foto", "x": "Ana in Maks pod vhodnim napisom ali pri vhodu v zoo.",
         "w": "Vhod je štart največjega dneva. Poglejta, kako so oblečeni — zvečer jim bosta morda drugačni (blatni, ampak srečni).",
         "p": {"k": "zanimivost", "h": "Zoo pod Rožnikom",
               "x": "Živalski vrt leži na južnem pobočju Rožnika, v naravnem gozdu in travnikih — del krajinskega parka Tivoli, Rožnik in Šišenski hrib.", "m": "Živalski vrt Ljubljana"}},
        {"t": "foto", "x": "Maks je »kapitan poti«: drži zemljevid zoo in pokaže, kam gresta prvo.",
         "w": "Vsak dober raziskovalec začne z zemljevidom. Označita tri živali, ki jih morata videti prvo.",
         "p": {"k": "nagrada", "h": "Nagrada: kapitan poti",
               "x": "Maks določi vrstni red prvih treh živali — Ana ga ne sme spreminjati (razen, če je res nujno)."}},
        {"t": "foto", "x": "Slonica Ganga: poiščita jo in naredita sliko z velikim slonom v ozadju.",
         "w": "Ganga živi v ljubljanskem zoo že od leta 1977 — skoraj petdeset let. To je dolgo!",
         "p": {"k": "zanimivost", "h": "Najstarejša prebivalka",
               "x": "Ganga je azijska slonica in najstarejša prebivalka ljubljanskega živalskega vrta. Slon z velikimi ušesi si ohlaja kri — ušesa so kot hladilnik!", "m": "Živalski vrt Ljubljana sloni"}},
        {"t": "video", "x": "10-sekundni video: slonov hobot v akciji (jedo, pije, se igra).",
         "w": "Hobot je nos, roka in cev za pitje hkrati — in ima neverjetno veliko mišic. Poglejta, kaj vse zna.",
         "p": {"k": "zanimivost", "h": "Hobot in hrana",
               "x": "Odrasel azijski slon poje na dan več deset kilogramov hrane — kolikor tehta Maksova šolska torba večkrat. Hobot jo vedno pobere sam."}},
        {"t": "foto", "x": "Žirafa: Maks stoji z dvignjeno roko poleg sebe — ugibajta, koliko Maksov je visoka žirafa.",
         "w": "Žirafa je najvišja kopenska žival. Poleg Maksa se zdi še višja!",
         "p": {"k": "skrivnost", "h": "Skrivnost modrega jezika",
               "x": "Jezik žirafe je dolg do 50 cm in temno modrikast — da se ne opeče na soncu, ko objema veje."}},
        {"t": "foto", "x": "Sibirski tiger: poiščita črte in slikajta oči — kje je tiger?",
         "w": "Črte so pri vsakem tigru drugačne, kot prstni odtis. Poglejta, če so res.",
         "p": {"k": "zanimivost", "h": "Največja mačka",
               "x": "Sibirski tiger je največja mačka na svetu. Njegova koža pod krznom je prav tako progasta."}},
        {"t": "video", "x": "Morski levi: kratek video plavanja ali treninga.",
         "w": "Morski levi se hitro učijo. Poglejta, kdaj je trening, in naredita video.",
         "p": {"k": "zanimivost", "h": "Ušesa ali ne",
               "x": "Morski levi imajo majhne zunanje ušesne školjke — tjulnji jih nimajo. Tako ju ločita med seboj."}},
        {"t": "foto", "x": "Mini ZOO: Maks nežno pobožja kozo ali ovco (počepnita in počakata).",
         "w": "V Mini ZOO se mirno počepneš in počakaš, da žival pride sama; ne hranimo, ne lovimo, ne dvigamo.",
         "p": {"k": "nagrada", "h": "Nagrada: varuh Mini ZOO",
               "x": "Maks postane »varuh Mini ZOO« — in mami pove, katero pravilo je najpomembnejše. Ana pove, katero ji je všeč."}},
        {"t": "foto", "x": "Selfi z alpako ali guanako — kdo se bolj smeji (ali kuka)?",
         "w": "Guanako je divji prednik lame; v Mini ZOO je pri njihovi ogradi.",
         "p": {"k": "zanimivost", "h": "Prednik lame",
               "x": "Guanako (iz Južne Amerike) je divji prednik domače lame. Ima krzno, ki je odlično za mraz — ravno prav za oktober."}},
        {"t": "foto", "x": "Medved ali volk: slikajta njegovo šapo ali oči — in primerjajta z roko.",
         "w": "V slovenskih gozdovih živi več sto rjavih medvedov in tudi volkovi. Tu jih vidita od blizu, na varnem.",
         "p": {"k": "zanimivost", "h": "Ris se je vrnil",
               "x": "Ris je bil pri nas v preteklosti iztrebljen, nato pa leta 1973 ponovno naseljen v kočevskih gozdovih."}},
        {"t": "foto", "x": "Rdeča panda: poiščita jo (če je) in slikajta njen rep.",
         "w": "Rdeča panda ni v sorodu z velikim pando — je njena lastna družina.",
         "p": {"k": "skrivnost", "h": "Skrivnost rdeče pande",
               "x": "Rdeča panda ima zelo dolg, progast rep — služi ji kot odeja v mrzlih nočeh in za ravnotežje na vejah."}},
        {"t": "foto", "x": "Najbolj smešna opica ali ptica: slikajta, kako jo gledata (in naredita enak obraz).",
         "w": "Žival ni nikoli smešna po naključju — le mi jo vidimo tako. Opazujta jo mirno in ugotovita, zakaj je tako videti.",
         "p": {"k": "nagrada", "h": "Nagrada: smešni obrazi",
               "x": "Vsak naredi obraz, kot ga ima izbrana žival — nato ugibata, katero žival je kdo upodobil."}},
        {"t": "foto", "x": "Vivarij ali terarij: najmanjša in največja žival, ki ju najdeta.",
         "w": "V vivariju je toplo in vlažno. Kače, kuščarji in žabe so mojstri skrivanja — poiščita jih!",
         "p": {"k": "skrivnost", "h": "Skrivnost kačjega jezika",
               "x": "Kača z jezikom »okuša« zrak, da ugotovi, kje je plen. Zato ima jezik razcepljen na dvoje."}},
        {"t": "foto", "x": "Sova ali orel: poiščita par oči, ki vaju opazujejo.",
         "w": "Sove lahko glavo obrnejo skoraj za 270 stopinj — a oči se skoraj ne premikajo.",
         "p": {"k": "zanimivost", "h": "Sovine oči",
               "x": "Sova ima oči nepremične, zato mora obračati vso glavo. Zato je tako vitka in prožna — kot cirkuški akrobat."}},
        {"t": "foto", "x": "Igrišče: Maks na igralu (poiščita tisto z afriško temo, če je odprto).",
         "w": "Igrišče je čas za gibanje in smeh. Maks naj izbere igro, ki jo igrata skupaj.",
         "p": {"k": "nagrada", "h": "Nagrada: igra po Maksovi izbiri",
               "x": "Maks izbere igro (npr. lovljenje, skrivalnice ali zmajska pustolovščina) — Ana jo igra z veseljem."}},
        {"t": "foto", "x": "Odmor: malica ali sladoled sredi vrta — slikata, kaj jesta in koga gledata zraven.",
         "w": "Odmor je pomemben del pustolovščine. Najboljše slike so tiste, ko si lačen in srečen.",
         "p": {"k": "nagrada", "h": "Nagrada: sladoled po izbiri",
               "x": "Maks izbere okus sladoleda — in Ana mu pove, kateri okus bi izbrala sama."}},
        {"t": "video", "x": "Zvoki zoo: 15 sekund posnetka (ptice, voda, opice) — in ugibata, katera žival je to.",
         "w": "Zoo ni samo za oči, ampak tudi za ušesa. Zaprita oči in poslušata.",
         "p": {"k": "skrivnost", "h": "Skrivnost zvokov",
               "x": "Vsaka žival ima svoj glas: sloni oddajajo nizke glasove, žirafe so večinoma tihe, morski levi lajajo. Kdo ima najlepši glas?"}},
        {"t": "video", "x": "TV novinar Maks: »Danes v ZOO Ljubljana …« — 20-sekundno poročilo iz zoo.",
         "w": "Novinar mora povedati, kaj se dogaja. Ana je kamerman — držita telefon vodoravno in govorita razločno.",
         "p": {"k": "nagrada", "h": "Nagrada: zvezda poročil",
               "x": "Maks postane »zvezda poročil« — Ana ga predstavi kot najboljšega novinarja pod Rožnikom."}},
        {"t": "foto", "x": "Skupna slika z živaljo, ki jima je najbolj ušla v srce (v ozadju, brez dotikanja!).",
         "w": "Vsak ima svojo najljubšo žival. Če sta različni, je še bolje — naredita dve sliki.",
         "p": {"k": "zanimivost", "h": "Najljubša žival",
               "x": "Strokovnjaki pravijo, da otroci žival, ki jo vidijo od blizu, pomnijo več let. Zato je dobro, da jo slikata skupaj."}},
        {"t": "foto", "x": "Trgovinica z darili: izberita en spominek za Zmajevo knjigo (in ga fotografirajta).",
         "w": "Spominek je trofeja pustolovščine. Izberita nekaj majhnega in uporabnega.",
         "p": {"k": "nagrada", "h": "Nagrada: spominek po izbiri",
               "x": "Maks izbere spominek — Ana ga plača, oba ga pokažeta doma babicam in prijateljem."}},
        {"t": "foto", "x": "Zadnja slika v zoo: Ana in Maks utrujena, a srečna ob izhodu.",
         "w": "Zadnja slika dneva je pogosto najlepša. Primerjata jo s tisto na vhodu zjutraj.",
         "p": {"k": "skrivnost", "h": "Zmajeva nagrada",
               "x": "Če sta opravila vsaj 10 izzivov v zoo, si zaslužita »zmajsko diplomo«. Izdelata jo doma in jo pokažeta vsem!"}},
    ],
    "domov": [
        {"t": "foto", "x": "Zadnja slika na postaji v Ljubljani: nahrbtnika, utrujena in nasmejana.",
         "w": "Vsaka pustolovščina ima konec — a Zmajeva knjiga ostane.",
         "p": {"k": "zanimivost", "h": "Slovenija v dveh urah",
               "x": "Z vlakom od Maribora do Ljubljane traja približno dve uri — Slovenija je majhna, a polna zanimivosti."}},
        {"t": "foto", "x": "Spominek, ki sta ga izbrala — pokažita ga v kameri.",
         "w": "Vsak spominek ima zgodbo. Povejta jo drug drugemu.",
         "p": {"k": "nagrada", "h": "Nagrada: spominek je zadolžen",
               "x": "Spominek je »varuh« zmajeve knjige: odloži ga na polico, kjer ga vidita vsak dan."}},
        {"t": "video", "x": "Maks pove v kamero tri najboljše stvari teh dveh dni (10–20 sekund).",
         "w": "Ko povemo na glas, si zapomnimo bolje. In Ana ima videopogovor za babice.",
         "p": {"k": "nagrada", "h": "Nagrada: Maksov govor",
               "x": "Ana posluša brez prekinjanja — potem vpraša eno vprašanje. Maks odgovori kot strokovnjak."}},
        {"t": "foto", "x": "V vlaku proti domu: kdo bo prvi zaspal? (po dovoljenju seveda).",
         "w": "Dvodnevna pustolovščina utrudi. Spanje v vlaku je del pustolovščine!",
         "p": {"k": "skrivnost", "h": "Zadnja skrivnost",
               "x": "Doma odpreta Zmajevo knjigo in izberita pet najlepših slik. Tista, ki jo izbereta oba, je naslovnica!"}},
    ],
}

# izbor izzivov (indeksi iz seznamov zgoraj) — manj izzivov na dan; največ ostane v živalskem vrtu.
# Dan 1 (vlak + hotel + center): 13, dan 2 (zoo + domov): 18. Spremeni seznam, če želiš kakšnega vrniti.
_KEEP = {"vlak": [0, 1, 3], "emonec": [0, 2, 4], "center": [0, 1, 2, 3, 4, 6, 8],
         "zoo": [0, 2, 3, 4, 5, 6, 7, 9, 11, 12, 14, 15, 17, 18, 20], "domov": [0, 2, 3]}
IZZIVI = {k: [v[i] for i in _KEEP[k]] if k in _KEEP else v for k, v in IZZIVI.items()}

# --------------------------------------------------------------------------- načrt poti
ITINERARY = {
    "intro": ("Dva dneva, ena noč. Prvi dan: vlak, hotel in Ljubljana s Katjo. Drugi dan: avtobus v živalski vrt in cel dan med živalmi. "
              "Povratni vlak izberita glede na uro, ko zapustita zoo. Ure so okvirne — vzemita si čas."),
    "days": [
        {"day": 1, "date": "čet, 15. okt", "region": "Ljubljana", "title": "Z vlakom v Ljubljano",
         "plan": ("Vlak iz Maribora (približno 2 uri). Ob prihodu odložita kovčka v Hotelu Emonec (Wolfova 12), "
                  "nato srečanje s Katjo: Prešernov trg, Tromostovje, Zmajski most, sladoled ali topla čokolada ob reki. "
                  "Večerja v središču in zgodaj spat.")},
        {"day": 2, "date": "pet, 16. okt", "region": "Živalski vrt", "title": "Cel dan v živalskem vrtu",
         "plan": ("Zajtrk, odjava in odhod z avtobusom št. 18 do postaje »Živalski vrt« (zoo odpre ob 9.00). Slon Ganga, žirafe, tigri, "
                  "morski levi, Mini ZOO, odmor in igrišče. Popoldne po prtljago v hotelu in vlak domov.")},
    ],
    "legs": [
        {"from": "Maribor", "to": "Ljubljana", "how": "Vlak (npr. InterCity Slovenija) z glavne postaje; vozni red in vozovnice na potniski.sz.si ali na blagajni",
         "duration": "približno 2 uri", "tip": "Vozovnici kupita vnaprej, sedeža ob oknu in majhen prigrizek v nahrbtniku."},
        {"from": "Železniška postaja Ljubljana", "to": "Hotel Emonec", "how": "peš po središču mesta",
         "duration": "okoli 12 min", "tip": "Kovčka na kolesih — pot je večinoma ravna."},
        {"from": "Hotel Emonec", "to": "Živalski vrt", "how": "avtobus št. 18 (smer Stožice) do postaje »Živalski vrt« — vstopita npr. na Bavarskem dvoru ali Konzorciju; ali peš okoli 25–35 min",
         "duration": "okoli 20–30 min", "tip": "Za plačilo vozovnice preverita aktualne možnosti (kartica Urbana ali brezstično plačilo) v aplikaciji Ljubljana Bus (LPP). Čez dan vozi približno vsakih 14 minut."},
        {"from": "Ljubljana", "to": "Maribor", "how": "vlak z glavne postaje; vozni red preverita na potniski.sz.si",
         "duration": "približno 2 uri", "tip": "Odhod izberita glede na uro, ko zapustita zoo — pridita na postajo 15 min prej."},
    ],
}

REGION_KEY = {"Ljubljana": "center", "Živalski vrt": "zoo"}

# --------------------------------------------------------------------------- Nujno
NUJNO_CALLS_HTML = """<section class="card-section nujno-calls" aria-labelledby="klic">
  <h2 id="klic">📞 Takoj pokliči</h2>
  <div class="call-grid">
    <a class="call-btn call-red" href="tel:112"><span class="c-num">112</span><span class="c-lbl">Nujna pomoč<br><small>reševalci, gasilci, policija</small></span></a>
    <a class="call-btn call-red" href="tel:113"><span class="c-num">113</span><span class="c-lbl">Policija</span></a>
    <a class="call-btn" href="tel:+38612442190"><span class="c-num">01 244 21 90</span><span class="c-lbl">Živalski vrt Ljubljana<br><small>informacije</small></span></a>
  </div>
  <p class="fine-note">Številka 112 deluje po vsej Evropi in je brezplačna. Povejta, kdo ste, kje ste (naslov ali znamenitost) in kaj se je zgodilo; ostanita na liniji, dokler vama ne rečejo, da lahko prekineta.</p>
</section>
"""

NUJNO_STEPS = [
    ("🧒", "Maks se izgubi v zoo",
     "Dogovor: Maks ostane točno tam, kjer je, in pokliče mamo ali pristopi k osebju zoo (uniforma). Ana pa ostane na mestu, kjer sta se videla zadnjič — in pokliče Maksa. Maks naj ima listek s telefonsko številko v žepu."),
    ("🏨", "Težava s hotelom",
     "Pokličita recepcijo (številko poglejta v potrditvi rezervacije). Prtljago smeta pustiti v hotelu še po odjavi — vprašajta ob prihodu."),
    ("🚂", "Zamuda ali zamujen vlak",
     "Povprašajta pri blagajni ali informacijah Slovenskih železnic o naslednjem vlaku; vozni red na potniski.sz.si."),
    ("🌧️", "Dež ali prehlad",
     "Zoo ima notranje prostore (vivarij, terariji); v središču Ljubljane so muzeji in kavarne. Preoblecita se v suho — tople nogavice so zlato."),
    ("🏥", "Zdravstvene težave",
     "Pokličita 112. Pri manjših težavah poiščita najbližjo lekarno (v središču jih je več). Kartico zdravstvenega zavarovanja imata v denarnici."),
    ("🧳", "Izgubljena stvar",
     "Pokličita hotel, zoo (+386 1 24 42 190) ali Slovenske železnice. Pogosto se najde — še posebej v vlaku, če takoj poveste kondukterju."),
]

NUJNO_NOTES_HTML = """<section class="card-section" aria-labelledby="zapiski">
  <h2 id="zapiski">📝 Najine številke (shranjeno samo v tem telefonu)</h2>
  <p class="cat-intro">Zapišita si, kar bi rada imela pri roki: hotel (telefon in naslov), Katjina številka, zavarovanje.</p>
  <textarea class="notes-box" data-save="nujno-zapiski" rows="7" placeholder="npr.
Hotel Emonec, Wolfova 12: tel. …
Katja: …
Maksova številka mame: …"></textarea>
</section>
"""

# --------------------------------------------------------------------------- Priprave (kontrolni seznam)
CHECKLIST = [
    ("📄 Pred odhodom", [
        "Vozovnici za vlak (Maribor ↔ Ljubljana) kupljeni ali shranjeni v telefonu",
        "Potrditev rezervacije v Hotelu Emonec (telefon, naslov, ura prihoda)",
        "Osebni izkaznici (ali potni listi) — obe",
        "Kartica zdravstvenega zavarovanja",
        "Dogovorjeno s Katjo: ura in kraj srečanja (npr. Prešernov trg)",
        "Vstopnici za zoo (po želji vnaprej na spletu) ali dovolj gotovine/kartica",
    ]),
    ("🎒 Nahrbtnik", [
        "Voda (obe steklenički) in malica za vlak",
        "Prigrizek za zoo: sadje, krekerji, malica za piknik",
        "Dežnik ali pelerina, kapa in rokavice za primer hladnega dne",
        "Telefon + polnilec + powerbank (veliko fotografiranja!)",
        "Zvezek ali Zmajev dnevnik in barvice/svinčnik",
        "Vrečke za smeti in robčki",
    ]),
    ("🧥 Obleka in obutev", [
        "Udobni, nepremočljivi čevlji (zoo ima ponekod strme poti)",
        "Plasti: majica, pulover, toplejša jakna",
        "Rezervne nogavice (za primer mokrote)",
        "Pižami in osnovna higiena za nočitev",
    ]),
    ("💊 Zdravje", [
        "Zdravila, ki jih Maks ali Ana redno jemljeta",
        "Obliži in robčki",
        "Sončna krema in kapa (če sije)",
    ]),
    ("🐉 Za pustolovščino", [
        "Dogovor: vsak dan vsaj 5 slik za Zmajevo knjigo",
        "Zapis imena in telefona mame/očeta na listku za Maksa (za vsak primer)",
        "Ideja: Maks izbere tri živali, ki jih mora videti",
        "Koledar: izberita en večer za skupno zgodbo",
    ]),
]

# --------------------------------------------------------------------------- Domov: besedila
WELCOME = [
    ("Pozdravljena, zmajska ekipa! Pred vama sta dva dneva, ki jih ne bosta pozabila: vlak, mesto z zmaji, prijateljica Katja in cel dan med živalmi."),
    ("Ta vodnik ni urnik, ki bi ga bilo treba prehiteti. Je vajin žepni spremljevalec: kaj in kje, s kratkimi zanimivostmi in veliko idejami."),
    ("Največ izzivov čaka v živalskem vrtu. Naložita fotografijo ali video, izziv se opravi, odkleni pa se zanimivost, skrivnost ali majhna nagrada. Iz tega nastane vajina Zmajeva knjiga."),
]

# --------------------------------------------------------------------------- ikone znamenitosti
_ICONS = {
    "Peron in vlak": "🚉", "Železniška postaja Ljubljana": "🚶", "Hotel Emonec": "🏨", "Stolnica sv. Nikolaja": "⛪",
    "Tromostovje in Prešernov trg": "🌉", "Zmajski most": "🐉", "Ljubljanski grad": "🏰", "Plečnikova tržnica": "🍎",
    "Hiša eksperimentov": "🔬", "Tivoli": "🌳", "Vhod in zemljevid": "🎟️", "Slonica Ganga": "🐘", "Žirafe": "🦒",
    "Tigri in veliki mački": "🐅", "Morski levi": "🦭", "Mini ZOO": "🐐", "Volkovi, medvedi in domača divjad": "🐺",
    "Rdeče pande, opice in drobne živali": "🐒", "Vivarij in terariji": "🐍", "Igrišči in odmor": "🛝",
    "Vlak domov": "🚂", "Spominek za Zmajevo knjigo": "🎁",
}
for _g in GUIDE.values():
    for _s in _g.get("sights", []):
        if _s["name"] in _ICONS:
            _s["icon"] = _ICONS[_s["name"]]

# --------------------------------------------------------------------------- povezave za nakup in rezervacije
from links import gdir, gsearch   # noqa: E402

SZ = "https://potniski.sz.si/"
LPP = "https://www.lpp.si/en"
ZOO_TICKETS = "https://trgovina.zoo.si/"
ZOO_HOURS = "https://www.zoo.si/odpiralni-cas"
CASTLE = "https://www.ljubljanskigrad.si/en/"
HE = "https://www.he.si/"
VISIT = "https://www.visitljubljana.com/en/"
HOTEL = "https://www.hotel-emonec.com/"
HOTEL_BOOKING = "https://www.booking.com/hotel/si/emonec.html"

LODGING = {
    "emonec": {
        "in": "2026-10-15", "out": "2026-10-16",
        "booked": ("Nastanitev je izbrana: Hotel Emonec, Wolfova ulica 12. Preverita potrditev rezervacije (ura prijave in odjave, zajtrk) "
                   "in pri recepciji vprašata, ali lahko prtljago odložita že ob prihodu in jo pustita še po odjavi."),
        "where": "Središče Ljubljane, okoli 12 minut hoje od železniške postaje in nekaj minut do Prešernovega trga.",
        "links": [("🏨 Hotel Emonec — uradna stran", HOTEL), ("🏨 Booking — stran hotela", HOTEL_BOOKING),
                  ("🚶 Pot od postaje do hotela (peš)", gdir("Ljubljana railway station", "Hotel Emonec, Wolfova ulica 12, Ljubljana", "walking"))],
    },
}

BOOK = {
    "vlak": [
        ("Vozovnice in vozni red — Slovenske železnice", SZ, "Vozovnici kupita vnaprej; za otroka velja otroška cena."),
        ("Vozni red Maribor → Ljubljana (Google Zemljevidi)", gdir("Maribor railway station", "Ljubljana railway station"), "Preveri odhode in peron."),
    ],
    "emonec": [
        ("Hotel Emonec — uradna stran", HOTEL, "Kontakt, prijava, zajtrk."),
        ("Booking — stran hotela", HOTEL_BOOKING, "Potrditev, ocene, podrobnosti."),
        ("Pot od postaje do hotela (Google, peš)", gdir("Ljubljana railway station", "Hotel Emonec, Wolfova ulica 12, Ljubljana", "walking"), "Okoli 12 minut hoje."),
    ],
    "center": [
        ("Ljubljanski grad — urnik, vstopnice, vzpenjača", CASTLE, "Preverita delovni čas in ceno vzpenjače."),
        ("Hiša eksperimentov — urnik in vstopnice", HE, "Po zadnjih podatkih: tor–čet 10–13, sob–ned 10–18; pon in pet zaprto — preverita!"),
        ("Turistična informacija Ljubljana — prireditve in nasveti", VISIT, "Kaj se dogaja v mestu."),
    ],
    "zoo": [
        ("Vstopnice za živalski vrt (spletna trgovina)", ZOO_TICKETS, "Vnaprej kupljena vstopnica prihrani čakanje."),
        ("Odpiralni čas in navodila", ZOO_HOURS, "Oktobra po objavljenih podatkih 9.00–18.00."),
        ("Avtobus št. 18 — LPP (vozni red, plačilo)", LPP, "Smer Stožice; postaja »Živalski vrt«."),
        ("Pot do zoo z avtobusom (Google Zemljevidi)", gdir("Bavarski dvor, Ljubljana", "Živalski vrt Ljubljana"), "Iz središča v približno 20 min."),
    ],
    "domov": [
        ("Vozni red Ljubljana → Maribor (Slovenske železnice)", SZ, "Izberita odhod glede na čas izhoda iz zoo."),
        ("Pot domov (Google Zemljevidi)", gdir("Ljubljana railway station", "Maribor railway station"), "Vozni red v telefonu."),
    ],
}

LEG_LINKS = {
    ("Maribor", "Ljubljana"): [("Slovenske železnice — vozovnice", SZ),
                               ("Vozni red (Google)", gdir("Maribor railway station", "Ljubljana railway station"))],
    ("Železniška postaja Ljubljana", "Hotel Emonec"): [
        ("Pot peš (Google)", gdir("Ljubljana railway station", "Hotel Emonec, Wolfova ulica 12, Ljubljana", "walking"))],
    ("Hotel Emonec", "Živalski vrt"): [
        ("LPP — avtobus 18", LPP), ("Vozni red (Google)", gdir("Bavarski dvor, Ljubljana", "Živalski vrt Ljubljana")),
        ("Vstopnice za zoo", ZOO_TICKETS)],
    ("Ljubljana", "Maribor"): [("Slovenske železnice — vozni red", SZ),
                               ("Vozni red (Google)", gdir("Ljubljana railway station", "Maribor railway station"))],
}

QUICKBUY = [
    ("🚆", "Vlak Maribor ↔ Ljubljana", [
        ("Slovenske železnice — vozovnice", SZ),
        ("Vozni red tja (Google)", gdir("Maribor railway station", "Ljubljana railway station")),
        ("Vozni red domov (Google)", gdir("Ljubljana railway station", "Maribor railway station"))]),
    ("🚌", "Avtobus v živalski vrt", [
        ("LPP — avtobus št. 18", LPP),
        ("Pot do zoo (Google)", gdir("Bavarski dvor, Ljubljana", "Živalski vrt Ljubljana"))]),
    ("🏨", "Hotel", [("Hotel Emonec — uradna stran", HOTEL), ("Booking — stran hotela", HOTEL_BOOKING)]),
    ("🎟️", "Vstopnice in urniki", [
        ("Živalski vrt — vstopnice", ZOO_TICKETS), ("Živalski vrt — odpiralni čas", ZOO_HOURS),
        ("Ljubljanski grad", CASTLE), ("Hiša eksperimentov", HE)]),
    ("🌐", "Mesto", [("Turistična informacija Ljubljana", VISIT)]),
]

FOOD_LINKS = [
    ("🍽️ Restavracije v bližini (Google Zemljevidi)", "https://www.google.com/maps/search/?api=1&query=restavracije+Ljubljana+center"),
    ("📞 Rezervacijo mize za 2 uredita po telefonu ali prek spletne strani lokala", None),
]

# --------------------------------------------------------------------------- zanimivosti, kviz, lov (Ljubljana)
FACTS = {
    "vlak": [
        "Slovenija ima približno 1.200 km železniških prog — in kar nekaj jih vodi mimo rek, kot je Sava.",
        "Preden pustita Maribor: ob Dravi raste najstarejša trta na svetu (nad 400 let) — po zapisu Guinnessove knjige rekordov.",
        "Ime postaje Zidani Most pomeni prav to: kamnit most. Tu se reki Savinja in Sava stečeta.",
        "Slovenija je med najbolj gozdnatimi državami Evrope: gozd pokriva okoli 60 % površine — iz vlaka ga vidita res veliko.",
    ],
    "emonec": [
        "Emona je bila rimsko mesto, ustanovljeno v prvih letih 1. stoletja na območju današnje Ljubljane; zid in ostanke lahko vidita še danes.",
        "Ljubljana je bila leta 2016 Zelena prestolnica Evrope — središče je večinoma brez avtomobilov.",
        "Ljubljana ima naziv Unescovo mesto književnosti (od leta 2015).",
        "Stolnica sv. Nikolaja, ki jo vidita blizu hotela, ima bronasta vrata iz leta 1996 s prizori iz zgodovine.",
    ],
    "center": [
        "Ljubljanski grad stoji na vzpetini okoli 376 m nad morjem; z razglednega stolpa vidita ob jasnem dnevu tudi Alpe.",
        "Zmajski most je bil zgrajen okoli leta 1901 in velja za eden prvih velikih armiranobetonskih obočnih mostov v mestu.",
        "Tromostovje ima dva stranska mostova za pešce, ki ju je dodal Jože Plečnik; osrednji most je starejši.",
        "Narodna in univerzitetna knjižnica (NUK) je Plečnikovo delo (okoli 1941) — poglejta velika stopnišča in svetilke.",
        "Ljubljanica ima več imen na svoji poti (Pivka, Unica …), zato ji pravijo tudi »reka sedmerih imen«.",
    ],
    "zoo": [
        "Ljubljanski živalski vrt je član evropskega združenja živalskih vrtov in akvarijev (EAZA).",
        "Sibirski tiger lahko v enem obroku poje več deset kilogramov mesa — pa vendar je večino dneva miren.",
        "Žirafe spijo zelo malo, pogosto manj kot dve uri na dan, v kratkih počitkih.",
        "Kalifornijski morski levi lahko plavajo okoli 40 km/h.",
        "Gepard v nekaj sekundah pospeši do skoraj 100 km/h — najhitrejša kopenska žival.",
        "Vrt združuje alpske, panonske in sredozemske živali — tako kot Slovenija sama.",
    ],
    "domov": [
        "Svetovni dan čebel (20. maja) je nastal na pobudo Slovenije — ker je čebelarstvo pri nas zelo staro.",
        "Najvišja gora Slovenije je Triglav (2.864 m) — na grbu in zastavi.",
        "Ko pridete domov, primerjajta prvi in zadnji posnetek dneva: kaj se je spremenilo? To je Zmajeva knjiga.",
    ],
}

QUIZ = {
    "ranks": [
        {"min": 0, "e": "🥚", "t": "Zmajevo jajce", "x": "Vse se začne z jajcem! Preberita zanimivosti in poskusita še enkrat."},
        {"min": 5, "e": "🐲", "t": "Mladi zmaj", "x": "Odlično — že veliko veš o živalih in Ljubljani!"},
        {"min": 9, "e": "🐉", "t": "Zmaj Ljubljane", "x": "Izvrstno! Poznata mesto in zoo kot pravi domačina."},
        {"min": 12, "e": "🏆", "t": "Zmajev mojster", "x": "Skoraj brez napake — lahko postaneta vodnika po Ljubljani!"},
    ],
    "questions": [
        {"q": "Katera žival je simbol Ljubljane?", "a": ["Zmaj", "Medved", "Lev"], "c": 0, "e": "Zmaj je na mestnem grbu, na gradu in na Zmajskem mostu."},
        {"q": "Kdo je po izročilu premagal zmaja v ljubljanskem močvirju?", "a": ["Herkul", "Jazon", "Odisej"], "c": 1, "e": "Jazon, vodja Argonavtov, ki se je z zlatim runom vračal domov."},
        {"q": "Koliko zmajev stoji na Zmajskem mostu?", "a": ["2", "4", "6"], "c": 1, "e": "Na vsakem koncu mostu sta po dva zmaja."},
        {"q": "Kdo je oblikoval Tromostovje?", "a": ["Jože Plečnik", "France Prešeren", "Ivan Cankar"], "c": 0, "e": "Arhitekt Jože Plečnik je dodal stranska mostova."},
        {"q": "Katera slonica živi v ljubljanskem zoo že od leta 1977?", "a": ["Jumbo", "Ganga", "Dumbo"], "c": 1, "e": "Ganga je najstarejša prebivalka vrta."},
        {"q": "Kako dolg je jezik žirafe?", "a": ["Okoli 10 cm", "Do okoli 50 cm", "Čez 2 m"], "c": 1, "e": "Do 50 cm in temno modrikast — da se ne opeče na soncu."},
        {"q": "Katera mačka je največja na svetu?", "a": ["Lev", "Sibirski tiger", "Gepard"], "c": 1, "e": "Sibirski tiger — in ima vsak tiger drugačne črte."},
        {"q": "Kaj imajo morski levi, tjulnji pa ne?", "a": ["Zunanje ušesne školjke", "Rep", "Krila"], "c": 0, "e": "To je najlažji način, da jih ločite."},
        {"q": "Rdeča panda je …", "a": ["Sorodnica velike pande", "Pripadnica lastne družine", "Vrsta medveda"], "c": 1, "e": "Rdeča panda pripada lastni družini — ni v sorodu z veliko pando."},
        {"q": "Katera pesem je slovenska himna (njena sedma kitica)?", "a": ["Zdravljica", "Lepa Vida", "Slovenija, od kod lepote tvoje"], "c": 0, "e": "Zdravljica, pesem Franceta Prešerna."},
        {"q": "Kje najdete najstarejšo trto na svetu?", "a": ["V Ljubljani", "V Mariboru", "Na Bledu"], "c": 1, "e": "V Mariboru, ob Dravi — več kot 400 let stara."},
        {"q": "Kako božate koze v Mini ZOO?", "a": ["Jih lovite", "Počepnete in počakate, da pridejo same", "Jih dvignete"], "c": 1, "e": "To je pravilo Mini ZOO: počepnite in počakajte."},
        {"q": "Kako se imenuje rimsko mesto na območju Ljubljane?", "a": ["Emona", "Celeia", "Poetovio"], "c": 0, "e": "Emona — po njej se imenuje tudi vaš hotel."},
        {"q": "Katera žival doseže v nekaj sekundah skoraj 100 km/h?", "a": ["Slon", "Gepard", "Žirafa"], "c": 1, "e": "Gepard je najhitrejša kopenska žival."},
    ],
}

LOV = [
    {"t": "Živali v zoo", "x": "Označita vsako žival, ki sta jo videla (na živo!).", "items": [
        {"id": "slon", "e": "🐘", "n": "Slon (Ganga)"}, {"id": "zirafa", "e": "🦒", "n": "Žirafa"}, {"id": "tiger", "e": "🐅", "n": "Tiger"},
        {"id": "levi", "e": "🦭", "n": "Morski lev"}, {"id": "medved", "e": "🐻", "n": "Rjavi medved"}, {"id": "volk", "e": "🐺", "n": "Volk"},
        {"id": "panda", "e": "🐼", "n": "Rdeča panda"}, {"id": "opica", "e": "🐒", "n": "Opica"}, {"id": "papiga", "e": "🦜", "n": "Papiga ali druga ptica"},
        {"id": "sova", "e": "🦉", "n": "Sova ali orel"}, {"id": "kaca", "e": "🐍", "n": "Kača ali kuščar"}, {"id": "koza", "e": "🐐", "n": "Koza ali ovca (Mini ZOO)"},
        {"id": "alpaka", "e": "🦙", "n": "Alpaka ali guanako"}, {"id": "gepard", "e": "🐆", "n": "Gepard ali leopard"}, {"id": "ris", "e": "🐈", "n": "Ris ali divja mačka"},
        {"id": "pelikan", "e": "🦩", "n": "Pelikan ali flamingo"},
    ]},
    {"t": "Zmaji in mesto", "items": [
        {"id": "zmaj_most", "e": "🐉", "n": "Zmaj na Zmajskem mostu"}, {"id": "zmaj_grb", "e": "🛡️", "n": "Zmaj na grbu ali gradu"},
        {"id": "tromostovje", "e": "🌉", "n": "Tromostovje"}, {"id": "preseren", "e": "🗿", "n": "Prešernov kip"},
        {"id": "ljubljanica", "e": "🌊", "n": "Reka Ljubljanica"}, {"id": "grad", "e": "🏰", "n": "Ljubljanski grad"},
        {"id": "trznica", "e": "🍎", "n": "Plečnikova tržnica"}, {"id": "sladoled", "e": "🍦", "n": "Sladoled ali čokolada"},
    ]},
    {"t": "Na poti", "items": [
        {"id": "vlak", "e": "🚂", "n": "Vlak Maribor–Ljubljana"}, {"id": "bus18", "e": "🚌", "n": "Avtobus št. 18"},
        {"id": "katja", "e": "👩", "n": "Srečanje s Katjo"}, {"id": "hotel", "e": "🏨", "n": "Hotel Emonec"},
        {"id": "zidani", "e": "🌉", "n": "Zidani Most iz vlaka"}, {"id": "megla", "e": "🌫️", "n": "Megla ob reki ali v mestu"},
    ]},
    {"t": "Števci", "items": [
        {"id": "c_zmaji", "e": "🐉", "n": "Zmaji, ki sta jih našla", "count": True},
        {"id": "c_zivali", "e": "📸", "n": "Živali, ki sta jih fotografirala", "count": True},
        {"id": "c_slike", "e": "🖼️", "n": "Fotografije za Zmajevo knjigo", "count": True},
    ]},
]

# --------------------------------------------------------------------------- Plan B za dež (Ljubljana)
RAIN = {
    "vlak": [
        ("Igre v vlaku", "Zmajev kviz in Zmajev lov v aplikaciji — brez zunanjega vremena", "Slovenske železnice vlak"),
    ],
    "emonec": [
        ("Narodni muzej Slovenije", "okoli 650 m od hotela: arheologija in zlata zgodovina Slovenije", "Narodni muzej Slovenije Ljubljana"),
        ("Mestni muzej Ljubljana", "zgodovina mesta in Emona (pod streho)", "Mestni muzej Ljubljana"),
        ("Stolnica sv. Nikolaja (notranjost)", "baročna notranjost, kratek postanek", "Stolnica sv. Nikolaja Ljubljana"),
    ],
    "center": [
        ("Prirodoslovni muzej Slovenije", "živali, minerali in dinozavri — super za Maksa", "Prirodoslovni muzej Slovenije Ljubljana"),
        ("Hiša eksperimentov", "vse se sme poskusiti (preverita urnik!)", "Hiša eksperimentov, Trubarjeva cesta 39, Ljubljana"),
        ("Mestni muzej Ljubljana", "zgodovina mesta pod streho", "Mestni muzej Ljubljana"),
        ("Topla čokolada v kavarni", "po sprehodu — in z Katjo klepet", "topla čokolada Ljubljana center"),
    ],
    "zoo": [
        ("Vivarij in terariji", "notranji prostori: kače, kuščarji, žabe", "Vivarij Živalski vrt Ljubljana"),
        ("Restavracija v zoo", "toplo kosilo in sladoled pod streho", "Restavracija Živalski vrt Ljubljana"),
        ("Pelerina + izzivi", "živali so ob dežju pogosto bolj skrivnostne — izzivi še vedno veljajo", "Živalski vrt Ljubljana"),
        ("Rezerva: Prirodoslovni muzej", "če dež postane premočan, se vrnita v mesto", "Prirodoslovni muzej Slovenije Ljubljana"),
    ],
    "domov": [
        ("Kavarna na postaji", "topel napitek pred vlakom", "kavarna železniška postaja Ljubljana"),
    ],
}
