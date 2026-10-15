# -*- coding: utf-8 -*-
"""Prevoz po postajah (Ljubljana — Zmajeva pustolovščina). Enaka struktura kot transport_jp.py.
Cene so »okoli« (po objavljenih podatkih) — preverita jih pri viru. Naslavljanje v dvojini."""
from links import gdir, gsearch

SZ = "https://potniski.sz.si/"
LPP = "https://www.lpp.si/en"
CASTLE_GETTING = "https://www.ljubljanskigrad.si/en/visit/getting-to-the-castle/"
VISIT_GETTING = "https://www.visitljubljana.com/en/visitors/getting-around/"
TAXI_LJ = "https://www.taxi-ljubljana.si/"
BOLT = "https://bolt.eu/en-si/"
ZOO = "https://www.zoo.si/en/"
ZOO_HOURS = "https://www.zoo.si/odpiralni-cas"

TRANSPORT_APPS = [
    ("Google Zemljevidi", "vozni red avtobusa in vlaka, čas hoje; zemljevid mesta shranita za uporabo brez povezave", "https://www.google.com/maps"),
    ("Ljubljana Bus (LPP)", "aplikacija mestnega avtobusa: kdaj pride št. 18, kje je postaja in plačilo (po objavljenih podatkih)", LPP),
    ("Bolt", "naročilo prevoza, če je v vaši aplikaciji na voljo (preverita ceno pred potrditvijo)", BOLT),
]

TRANSPORT = {
    # ------------------------------------------------------------------ VLAK
    "vlak": {
        "from": "Železniška postaja Ljubljana", "from_label": "železniška postaja Ljubljana",
        "arrive": ("Maribor railway station", "Ljubljana railway station",
                   "Vlak iz Maribora v Ljubljano vozi približno dve uri. Vozovnici kupita vnaprej (SŽ, blagajna ali avtomat); cena za odraslega je po objavljenih podatkih okoli 10–14 € v eno smer, otroška cena je nižja. Točno uro odhoda in peron preverita na dan potovanja."),
        "intro": "Od mariborske postaje do ljubljanske vaju čaka dve uri vožnje. Na ljubljanski postaji izstopita na glavnem peronu in nato kratek sprehod do hotela — kovčka na kolesih sta primerna za gladko pot.",
        "options": [
            ("🚆", "Vlak (SŽ)", "Slovenske železnice: spletna trgovina, avtomati in blagajna. InterCity vlaki so hitrejši, a morda dražji; sedež v 2. razredu je običajno dovolj udoben. Vprašajta za družinsko ali otroško ceno."),
            ("🧳", "Prtljaga", "Na ljubljanski postaji so omarice za prtljago (po objavljenih podatkih) — preverita, ali so odprte, če bi potrebovala prtljago prihraniti pred odjavo iz hotela."),
            ("🚕", "Taksi s postaje", "Taksi do hotela je kratka vožnja (okoli 5 min); cena po objavljenih podatkih okoli 5–8 €. Peš je okoli 12 min po ravni poti."),
        ],
        "sights": [
            "Na peronu pred odhodom preverita številko vagona; vlak ima na tabli oznako smeri (Ljubljana).",
            "Postajo si lahko ogledata v nekaj minutah; pot do hotela vodi po Slovenski cesti proti središču, peš okoli 12 min.",
        ],
        "taxi": "Pred postajo stojijo taksiji; vožnja do Hotela Emonec je kratka in po objavljenih podatkih stane okoli 5–8 €. Če vaju utrudi vroč dan ali dež, je to dobra izbira. Aplikaciji Bolt ali Taxi Ljubljana pokažeta ceno vnaprej.",
        "links": [("🚆 Slovenske železnice — vozovnice in vozni red", SZ),
                  ("🧭 Vozni red Maribor → Ljubljana (Google)", gdir("Maribor railway station", "Ljubljana railway station")),
                  ("🚶 Pot postaja → hotel (peš)", gdir("Ljubljana railway station", "Hotel Emonec, Wolfova ulica 12, Ljubljana", "walking"))],
        "tips": ["Na postaji kupita vodo in prigrizek, pred vlakom.", "Prtljago držita skupaj; Maks lahko vleče svoj kovček in je zmagovalec poti."],
    },
    # ------------------------------------------------------------------ EMONEC
    "emonec": {
        "from": "Hotel Emonec, Wolfova ulica 12, Ljubljana", "from_label": "Hotel Emonec (Wolfova ulica 12)",
        "arrive": ("Ljubljana railway station", "Hotel Emonec, Wolfova ulica 12, Ljubljana",
                   "Od železniške postaje do hotela je okoli 12 minut hoje po središču mesta; pot je večinoma ravna. S taksijem je to kratka vožnja (okoli 5–8 € po objavljenih podatkih)."),
        "intro": "Hotel Emonec je v samem središču: skoraj vse, kar sta načrtovala v mestu, je peš v 5–15 minutah. Javni prevoz potrebujeta predvsem za zoo (avtobus št. 18) in če bi bila utrujena ali bi deževalo.",
        "options": [
            ("🚶", "Peš", "Središče Ljubljane je večinoma peš cona. Od hotela do Prešernovega trga je nekaj minut, do Tromostovja podobno, do Ljubljanskega gradu okoli 15–20 minut z vzponom (ali z vzpenjačo)."),
            ("🚌", "Mestni avtobus LPP", "Enotna vožnja je po objavljenih podatkih okoli 1,30 €; plačilo po tem, kar ponuja aplikacija Ljubljana Bus ali kartica Urbana — preverita pred vožnjo. Za otroka veljajo posebni pogoji."),
            ("🚕", "Taksi", "V centru je kratka vožnja po objavljenih podatkih okoli 6–10 €; bolj plačljiva je, ko je mrzlo ali mokro. Telefonsko številko taksija vama pove recepcija."),
            ("🚲", "Kolesa in Kavalir", "BicikeLJ je mestna izposoja koles (registracija v aplikaciji, za odrasle). Po pešcih si lahko v središču pomagata s brezplačnim električnim vozilom Kavalir — po objavljenih podatkih vozi po starem mestu; preverita, če deluje v času vajinega obiska."),
        ],
        "sights": [
            "",
            "Peš okoli 5 min od hotela; Stolnica je v starem mestu, ob tržnici in reki.",
        ],
        "taxi": "Taksi do zoo vaju stane po objavljenih podatkih okoli 8–12 € (okoli 10–15 min); to je pogosto hitrejše od avtobusa. Pokličita hotel, če ne najdeta prostega vozila, in prosita, naj ga ukaže.",
        "links": [("🏨 Hotel Emonec — uradna stran", "https://www.hotel-emonec.com/"), ("🚕 Taxi Ljubljana", TAXI_LJ),
                  ("🚌 LPP — avtobus in vozovnice", LPP), ("🏙️ Visit Ljubljana — prevoz po mestu", VISIT_GETTING)],
        "tips": ["Pred odjavo vprašajta recepcijo, če smeta prtljago pustiti do odhoda na vlak.", "Vnaprej si zapišita uro odhoda vlaka domov (prva stvar v dnevu)."],
    },
    # ------------------------------------------------------------------ CENTER
    "center": {
        "from": "Hotel Emonec, Wolfova ulica 12, Ljubljana", "from_label": "Hotel Emonec",
        "arrive": ("Hotel Emonec, Wolfova ulica 12, Ljubljana", "Tromostovje, Ljubljana",
                   "Vse točke so v krogu 5–20 minut hoje od hotela; samo Tivoli in Ljubljanski grad zahtevata nekaj več poti. Pot po starem mestu je lepa tudi z dežnikom."),
        "intro": "Središče Ljubljane je kot narejeno za pešce. Z Emonca do Prešernovega trga, Tromostovja in Zmajskega mostu hodita v nekaj minutah; do Tivolija je okoli 15–20 minut; do gradu pa se povzpneta peš ali z vzpenjačo s Krekovega trga.",
        "options": [
            ("🚶", "Peš", "Pešpot po starem mestu je ravna in prijetna za otroka. Kavarne in klopi so na vsakih nekaj sto metrov, zato naredita počitek, ko je treba."),
            ("🚠", "Vzpenjača na grad", "Vzpenjača vozi s Krekovega trga na Ljubljanski grad in traja okoli minute; cena je po objavljenih podatkih nekaj evrov na odraslega (otroška cena nižja) — točno ceno in urnik preverita na strani gradu. Pešpot navzgor je prijetna, a strma (okoli 15–20 min)."),
            ("🚌", "Avtobus", "Za Tivoli ali Hišo eksperimentov avtobusa ne potrebujeta; avtobus št. 18 bosta potrebovala le za zoo."),
            ("🚕", "Taksi", "Če sta po več urah hoje utrujena, je taksi ugoden: po objavljenih podatkih okoli 6–10 € za krajšo vožnjo po mestu."),
        ],
        "sights": [
            "Peš iz hotela okoli 5–8 min proti reki Ljubljanici. Katja vaju lahko čaka pri Prešernovem spomeniku.",
            "Zmajski most je okoli 8–10 min peš od hotela (po Čopovi/Miklošičevi smeri), ob reki.",
            "Do Krekovega trga je okoli 10 min peš; vzpenjača na grad traja okoli minuto. Za pešpot računajta 15–20 min z vzponom.",
            "Tržnica je ob Ljubljanici, okoli 5–8 min peš od hotela. Najbolj živahna je dopoldne.",
            "Hiša eksperimentov (Trubarjeva 39) je okoli 10–15 min peš od hotela. Odprto po zadnjih podatkih tor–čet 10–13 in sob–ned 10–18 — preverita pred obiskom.",
            "Tivoli je okoli 15–20 min peš od hotela po Čopovi ulici in nato podvozu; sprehajalna pot v parku je ravna.",
        ],
        "taxi": "Za center taksija skoraj ne potrebujeta. Uporabita ga, ko sta utrujena po sprehodu proti gradu ali Tivoliju; po objavljenih podatkih je krajša vožnja okoli 6–10 €. Poleg aplikacije Bolt lahko naročita prek hotela.",
        "links": [("🏰 Ljubljanski grad — kako do gradu, vzpenjača", CASTLE_GETTING), ("🧪 Hiša eksperimentov — urnik in vstopnice", "https://www.he.si/"),
                  ("🏙️ Visit Ljubljana — prevoz in zemljevid", VISIT_GETTING), ("🧭 Hotel → Ljubljanski grad (Google, peš)", gdir("Hotel Emonec, Wolfova ulica 12, Ljubljana", "Ljubljanski grad", "walking"))],
        "tips": ["Pot do gradu navzgor je strma — vzpenjača prihrani energijo za zoo naslednji dan.", "Na tržnici kupita malico za piknik pri reki."],
    },
    # ------------------------------------------------------------------ ZOO
    "zoo": {
        "from": "Hotel Emonec, Wolfova ulica 12, Ljubljana", "from_label": "Hotel Emonec",
        "arrive": ("Hotel Emonec, Wolfova ulica 12, Ljubljana", "Živalski vrt Ljubljana, Večna pot 70",
                   "Z avtobusom št. 18 (smer Stožice) do postaje »Živalski vrt« je okoli 20–30 minut skupaj s hojo do postaje; vstopita lahko npr. na Bavarskem dvoru ali Konzorciju. Čez dan vozi po objavljenih podatkih približno vsakih 14 minut. Alternativa je taksi (okoli 10–15 min) ali peš okoli 25–35 min."),
        "intro": "Zoo je na pobočju Rožnika nad središčem. Najlažje pridete tja z avtobusom št. 18 ali s taksijem; po vrtu se premikata peš, zato si privoščita počitek. V vrtu so vzponi in poti med živalmi — vzemita udobne čevlje in nekaj prigrizka.",
        "options": [
            ("🚌", "Avtobus št. 18", "Najboljša javna povezava: vozi iz središča do postaje »Živalski vrt« (smer Stožice), vožnja okoli 15–20 minut. Vozovnica je po objavljenih podatkih okoli 1,30 € na odraslega; plačilo preverita v aplikaciji Ljubljana Bus (LPP) ali na avtomatu."),
            ("🚕", "Taksi", "Iz hotela je to okoli 10–15 minut vožnje; cena po objavljenih podatkih okoli 8–12 €. Povratek iz zoo je včasih težji (taksijev pred vhodom ni vedno) — naročita ga prek Bolta ali hotela."),
            ("🚶", "Peš", "Peš od hotela je okoli 25–35 minut, deloma v klanec; za otroka z energijo je to del pustolovščine, a pomislita, koliko moči bo ostalo za sam obisk."),
        ],
        "sights": [
            "Vhod je na Večni poti 70; z avtobusom izstopita na postaji »Živalski vrt«, od tam je do blagajne le nekaj minut hoje. Vstopnice po objavljenih podatkih tudi na trgovina.zoo.si.",
            "", "", "", "", "", "", "", "", "",
        ],
        "within": "Znotraj vrta se premikata peš po označenih poteh; zemljevid vzemita na vhodu. Vrt je razporejen po pobočju, zato predvidevajta tudi počitke (klopi, igrišči). Velja vzorec: najprej velike živali (sloni, žirafe), potem majhne, nazadnje igrišče.",
        "taxi": "Za povratek iz zoo: naročita Bolt ali pokličeta taksi ob izhodu in počakata pri vhodu. Če sta utrujena in ura pritiska zaradi vlaka, je to varnejša izbira od avtobusa. Cena je po objavljenih podatkih okoli 8–12 € do središča.",
        "links": [("🎟️ Vstopnice za zoo (spletna trgovina)", "https://trgovina.zoo.si/"), ("🕘 Zoo — odpiralni čas", ZOO_HOURS),
                  ("🚌 LPP — avtobus št. 18", LPP), ("🧭 Hotel → zoo (Google, javni prevoz)", gdir("Bavarski dvor, Ljubljana", "Živalski vrt Ljubljana"))],
        "tips": ["Povratek iz zoo načrtujta z rezervo: vlak domov lovita ob uri, ki jo imata v karti.", "Če dežuje, vzemita pelerino — živali v dežju so pogosto bolj skrivnostne."],
    },
    # ------------------------------------------------------------------ DOMOV
    "domov": {
        "from": "Železniška postaja Ljubljana", "from_label": "železniška postaja Ljubljana",
        "arrive": ("Živalski vrt Ljubljana, Večna pot 70", "Ljubljana railway station",
                   "Iz zoo: avtobus št. 18 proti središču (okoli 15–20 min) in od Bavarskega dvora še okoli 10–15 min peš do postaje; ali taksi (okoli 10–15 min). Na postajo pridita vsaj 15 minut pred odhodom."),
        "intro": "Povratek načrtujta od konca: najprej ura odhoda vlaka, potem čas za prtljago in pot do postaje, nato odhod iz zoo. Prtljago vzemita iz hotela po odjavi, če sta jo pustila na recepciji.",
        "options": [
            ("🚆", "Vlak (SŽ)", "Vozovnico kupita vnaprej (če nista kupila povratne) na potniski.sz.si ali na blagajni; cena je po objavljenih podatkih podobna kot v obratno smer. Ura odhoda: preverita na dan potovanja."),
            ("🚕", "Taksi do postaje", "Če se vama mudi, je taksi najpreprostejši; po objavljenih podatkih okoli 8–12 € iz zoo ali 5–8 € iz središča."),
            ("🚌", "Avtobus št. 18", "Z zoo v središče; nato peš do postaje (okoli 10–15 min). Dodajta čas za čakanje (vozi približno vsakih 14 minut)."),
        ],
        "sights": [
            "Na postaji počakajta pri tabli odhodov; peron se pogosto pokaže tik pred odhodom. Vstopita 5–10 min pred odhodom.",
            "Spominek za Zmajevo knjigo najdeta v trgovinicah z darili v starem mestu (peš nekaj minut od hotela) ali v trgovini zoo; vlak pa je že tudi sam spomin.",
        ],
        "taxi": "Zadnji kilometer do postaje: kratek taksi je smiseln, če sta utrujena ali se vama mudi. Iz središča je to okoli 5–8 €, iz zoo okoli 8–12 € (po objavljenih podatkih).",
        "links": [("🚆 Vozni red Ljubljana → Maribor (SŽ)", SZ), ("🧭 Pot domov (Google)", gdir("Ljubljana railway station", "Maribor railway station")),
                  ("🚕 Taxi Ljubljana", TAXI_LJ)],
        "tips": ["Na vlak pridita z rezervo — raje počakata na peronu in Maks nariše zmaja.", "Vozovnici prilepita v Zmajevo knjigo za spomin."],
    },
}
