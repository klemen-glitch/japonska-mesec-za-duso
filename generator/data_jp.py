# -*- coding: utf-8 -*-
"""Praktični podatki za potovanje Japonska: nastanitve (datumi se izračunajo iz načrta poti),
povezave za prevoz, vstopnice in hitre povezave. Cene namenoma niso navedene — preverite jih za svoje datume."""
from links import gdir, gsearch, klook, gyg, booking, airbnb, google_hotels

SMART_EX = "https://smart-ex.jp/en/"
EKINET = "https://www.eki-net.com/en/jreast-train-reservation/Top/Index"
JR_CENTRAL = "https://global.jr-central.co.jp/en/"
JR_WEST = "https://www.westjr.co.jp/global/en/"
NAVITIME = "https://japantravel.navitime.com/en/"
JORUDAN = "https://world.jorudan.co.jp/mln/en/"
SKYLINER = "https://www.keisei.co.jp/keisei/tetudou/skyliner/us/index.php"
NEX = "https://www.jreast.co.jp/e/nex/"
FUJIKYU = "https://www.fujikyu.co.jp/en/"
HIGHWAYBUS = "https://www.highwaybus.com/gp/index"
MEIKO = "https://www.meikobus.jp/en/"
KUMANO = "https://www.tb-kumano.jp/en/"
KOYASAN = "https://www.koyasan.or.jp/en/"
IYA_ONSEN = "https://www.iyaonsen.co.jp/en/"
KYOTO_TRAVEL = "https://kyoto.travel/en/"
OSAKA_INFO = "https://osaka-info.jp/en/"
MIYAJIMA_FERRY = "https://www.jr-miyajimaferry.co.jp/en/"
PEACE_MUSEUM = "https://hpmmuseum.jp/?lang=eng"

# --------------------------------------------------------------------------- nastanitve
LODGING = {
    "tokio": {
        "book": "Ueno, Tokyo", "air": "Taito-City--Tokyo--Japan",
        "where": "Ueno ali Asakusa — blizu Yanake, tržnice in ladjice; Skyliner z letališča Narita pripelje prav na postajo Keisei Ueno. Za več povezav in nakupov: Shinjuku ali postaja Tokio.",
        "cheaper": ("Najcenejše so poslovne verige (Toyoko Inn, APA, Sotetsu Fresa Inn, Super Hotel): majhne sobe, a čiste in ob postaji. "
                    "Za štiri osebe pa pogosto izide ceneje apartma z 2 spalnicama (Airbnb ali aparthotel) kot dve hotelski sobi — "
                    "izračunajte skupno ceno obeh možnosti. Za iste datume primerjajte Booking, Google Hotels in Airbnb."),
        "search": [
            "»Apartment, 2 bedrooms« v Uenu/Asakusi — na Airbnb »Entire home« z 2+ spalnicama, na Bookingu filter Apartments; do 10 min hoje do postaje.",
            "2 × »Twin Room« v isti stavbi (2 sobi, 4 odrasli) z brezplačnim preklicem — dve kopalnici, manj čakanja zjutraj.",
            "Aparthotel z družinskimi sobami za 4 (npr. MIMARU) — večje sobe s kuhinjico; preverite razpoložljivost za svoje datume.",
            "Hotel z oceno 8+ in največ 5–7 min hoje do metroja (linija Ginza) — vsak dan prihranite pot s kovčki.",
        ],
    },
    "kawaguchiko": {
        "book": "Kawaguchiko, Yamanashi", "air": "Fujikawaguchiko--Yamanashi--Japan",
        "where": "Ob jezeru Kawaguchi — severna obala (razgled na Fuji) ali okoli postaje Kawaguchiko za lažje povezave.",
        "cheaper": ("Sobe z razgledom na Fuji so dražje in jih zmanjka prve. Za eno noč je pogosto ugodna tatami soba (washitsu) za 4 osebe z večerjo (»half board«), "
                    "ker so cene v ryokanih navadno na osebo — primerjajte skupno ceno za vse štiri, ne cene sobe."),
        "search": [
            "»Japanese-style room (washitsu) for 4« ali »Quadruple Room« z razgledom na Fuji.",
            "Ryokan ali hotel z onsenom in večerjo (»dinner included«), do 10 min od postaje ali avtobusne postaje.",
            "Fotografije z balkona/okna: izberite »Mountain view« in preverite, ali razgled res vključuje Fuji.",
            "Brezplačen preklic — jesenski vikendi so polni; rezervirajte zdaj, odpovejte lahko kasneje.",
        ],
    },
    "minobusan": {
        "booked": ("Nastanitev je že rezervirana (šukubo Kakurinbo). Shranite potrditev in številko rezervacije v telefon in na papir. "
                   "Ob prihodu preverite uro prijave, uro večerje in jutranje molitve (točno po urniku) ter ali plačate na kraju samem (pogosto gotovina)."),
        "links": [("📍 Kakurinbo na zemljevidu", "https://www.google.com/maps/search/?api=1&query=Kakurinbo%20Minobu%20Yamanashi"),
                  ("🔎 Kuon-ji — uradna stran", "https://www.kuonji.jp/")],
    },
    "izu": {
        "book": "Shuzenji, Izu, Shizuoka", "air": "Izu--Shizuoka--Japan",
        "where": "Shuzenji (onsen mesto s starim središčem, bambusova pot, Momijirin) — ali obala Izukogen, če želite razgled na morje.",
        "cheaper": ("V ryokanih je cena običajno na osebo in vključuje večerjo kaiseki ter zajtrk — primerjajte skupno ceno za štiri, ne cene sobe. "
                    "Če je proračun napet: eno noč v ryokanu z zasebno kopeljo, dve noči v ugodnejšem hotelu z onsenom. "
                    "Spletna stran ryokana je včasih ugodnejša od platform — preverite pred potrditvijo."),
        "search": [
            "Ryokan v Shuzenjiju z zasebno kopeljo (»private open-air bath«); na Bookingu filter »Hot spring bath«.",
            "»Japanese-style room for 4« z 2 obrokoma (večerja + zajtrk) — običajno najbolje razmerje cena/doživetje.",
            "Hotel z onsenom do 10 min od postaje Shuzenji (ali s prevozom z avtobusa/postaje) — za preostali dve (cenejši) noči.",
            "Vila/apartma na obali Izu za 4 (Airbnb), če želite eno noč kuhati sami in imeti mir za pranje.",
        ],
    },
    "kumano": {
        "book": "Yunomine Onsen, Tanabe, Wakayama", "air": "Tanabe--Wakayama--Japan",
        "where": "Yunomine ali Kawayu Onsen (rečna kopel) za Hongu; Katsuura/Nachi za slap in morje. Ponudba je majhna — preverite razdalje do poti.",
        "cheaper": ("Minshuku in ryokani na Kumano Kodo imajo ceno na osebo z večerjo in zajtrkom; platforme ne bodo bistveno ceneje. "
                    "Turistični urad Tanabe (Kumano Travel) ima rezervacijski servis z angleško podporo — pogosto je lažje kot iskanje po platformah, še posebej za prevoz prtljage in bento za na pot."),
        "search": [
            "Minshuku/ryokan v Yunomine ali Kawayu z večerjo in zajtrkom — pri rezervaciji vprašajte za bento za na pot.",
            "Hotel v Katsuuri ob morju z onsenom (blizu Nachi) — za noči, ko ste ob slapu.",
            "Kumano Travel (Tanabe): nastanitve ob Kumano Kodo in prevoz prtljage med nočitvami (takuhaibin).",
            "Brezplačen preklic ali rezervacija prek urada — poti in vreme se lahko spremenijo.",
        ],
        "links": [("🥾 Kumano Travel (Tanabe) — nastanitve in rezervacije", KUMANO),
                  ("🚌 Meiko Bus — avtobusi po Kumano Kodo", MEIKO)],
    },
    "koyasan": {
        "book": "Koyasan, Wakayama", "air": "Koya--Wakayama--Japan",
        "where": "Glavna ulica Koya-san (med Senjuguchi in Daimon) — blizu Okunoina, Danjo Garan in avtobusov.",
        "cheaper": ("Šukubo (nočitev pri menihih) imajo fiksne cene na osebo z dvema vegetarijanskima obrokoma, zato platforma ne bo ceneje — "
                    "za to nočitev je smiselno gledati razpoložljivost neposredno pri združenju šukubo in turistični zvezi Koya-san. "
                    "Če je šukubo zaseden, ga ponovno preverite 1–2 tedna pred odhodom: odpovedi so pogoste."),
        "search": [
            "Šukubo za 15.–17. nov — poskusite znova prek združenja Koyasan Shukubo Association (odpovedi).",
            "Guest house ali hotel na gori (Booking: »Koyasan«), 2 sobi ali 1 tatami soba za 4.",
            "Rezervna možnost: ena noč v dolini (Gokurakubashi/Hashimoto) in dnevni obisk gore.",
            "Pri šukuboju zahtevajte tatami sobo za 4 s futoni in bližino vhoda v Okunoin.",
        ],
        "links": [("⛩️ Koyasan Tourist Association — nastanitve", KOYASAN),
                  ("🔎 Koyasan Shukubo Association — iskanje", gsearch("Koyasan Shukubo Association booking"))],
    },
    "iya": {
        "book": "Iya Valley, Miyoshi, Tokushima", "air": "Miyoshi--Tokushima--Japan",
        "where": "Dolina Iya — Hotel Iya Onsen (kopel ob reki, žičnica) ali tradicionalna slamnata hiša (kominka) v Higashi-Iya ali Nishi-Iya.",
        "cheaper": ("Nastanitev je v dolini malo in na odročnih krajih — rezervirajte čim prej in neposredno pri hotelu ali na Bookingu. "
                    "Večerjo naročite pri nastanitvi (v dolini restavracij skoraj ni), prevoz pa dogovorite vnaprej."),
        "search": [
            "Hotel Iya Onsen — uradna stran (rezervacija, prevoz, večerja).",
            "Kominka/slamnata hiša za 4 (Iya, Tokushima) na Bookingu ali Airbnb.",
            "Minshuku v Nishi-Iya blizu Kazurabashi z večerjo in zajtrkom.",
            "Vprašajte za prevoz s postaje Oboke ali taksi — lokalnih avtobusov je malo.",
        ],
        "links": [("♨️ Hotel Iya Onsen — uradna stran", IYA_ONSEN)],
    },
    "ine": {
        "book": "Ine, Kyoto, Japan", "air": "Ine--Kyoto--Japan",
        "where": "Ine — nepozabno je prespati kar v funayi (hiše nad vodo); nekaj nastanitev je v samem zalivu, ostale v bližnjih krajih.",
        "cheaper": ("Funaya imajo malo sob in jih zmanjka zelo zgodaj; cene so na osebo z večerjo (morski sadeži). "
                    "Če funaye ni, je dobra druga izbira minshuku v vasi ali hotel pri Amanohashidateju."),
        "search": [
            "Nastanitev v funayi (»Ine funaya stay«) — izberite sobo z razgledom na zaliv.",
            "Minshuku v Ine z večerjo (morski sadeži) in zajtrkom.",
            "Rezervirajte čim prej — ponudba je zelo majhna; brezplačen preklic.",
            "Rezerva: hotel/ryokan v Amanohashidateju s prevozom do Ine z avtobusom.",
        ],
    },
    "kyoto": {
        "book": "Kyoto Station, Kyoto", "air": "Kyoto--Japan",
        "where": "Ob postaji Kyoto (povezave), Shijo–Kawaramachi (hrana, Gion) ali Higashiyama (mirneje, bližje templjem).",
        "cheaper": ("November je vrhunec sezone, cene so lahko občutno višje od običajnih: rezervirajte zdaj z brezplačnim preklicem in kasneje primerjajte. "
                    "Za štiri osebe so machiya (cele tradicionalne hiše) pogosto ugodne na osebo. V Kyotu se plača tudi lokalni nastanitveni davek (v ceni ali na kraju samem) — preverite pri rezervaciji."),
        "search": [
            "Machiya — celotna hiša, 2 spalnici (Airbnb »Entire home« ali Booking »Homes«), blizu Higashiyame ali Giona.",
            "Hotel pri postaji Kyoto z oceno 8+ (vse povezave in kovčki) — dve twin sobi.",
            "Ryokan za 1 noč v Higashiyami/Gionu z večerjo kaiseki — za izkušnjo.",
            "Aparthotel z družinskimi sobami (npr. MIMARU Kyoto) — kuhinjica, pralni stroj, 4 postelje.",
        ],
    },
    "osaka": {
        "book": "Namba, Osaka", "air": "Osaka--Japan",
        "where": "Namba ali Shinsaibashi (hrana, Dotonbori; vlak Rapi:t na letališče Kansai gre prav iz Nambe) ali Umeda (povezave).",
        "cheaper": ("Osaka je običajno cenejša od Kyota. Za 5 noči je smiseln apartma s kuhinjico in pralnim strojem (pranje pred povratkom). "
                    "Primerjajte Booking, Airbnb in Google Hotels za iste datume; mestni davek se plača posebej."),
        "search": [
            "Apartment, 2 bedrooms, v Nambi/Shinsaibashiju (Airbnb ali Booking Apartments) — z pralnim strojem.",
            "Hotel ob postaji Nankai Namba (vlak Rapi:t do letališča Kansai 2. 12.), 2 twin sobi.",
            "Aparthotel (npr. Citadines, MIMARU) — prostorne sobe za 4.",
            "Hotel blizu Dotonbori ali Shinsaibashi z oceno 8+ — peš do večerij in tržnice Kuromon.",
        ],
    },
    "chichibu": {
        "book": "Chichibu, Saitama", "air": "Chichibu--Saitama--Japan", "optional": True,
        "where": "Chichibu je izlet iz Tokia (nazaj zvečer). Kdor želi mirno noč z onsenom, lahko prespi pri postaji Seibu-Chichibu.",
        "cheaper": "Ena noč v Chichibuju je običajno cenejša kot v Tokiu; med jesenskimi barvami in nočnim festivalom (začetek decembra) rezervirajte zgodaj.",
        "search": ["Hotel ali ryokan blizu postaje Seibu-Chichibu z onsenom, 2 sobi, brezplačen preklic."],
    },
    "nara": {
        "book": "Nara, Japan", "air": "Nara--Japan", "optional": True,
        "where": "Nara je izlet — kdor želi jutro v parku brez gneče, lahko doda eno noč blizu parka.",
        "cheaper": "Ena noč v Nari je običajno cenejša kot v Kyotu; primerjajte Booking in Google Hotels.",
        "search": ["Hotel ali ryokan blizu parka Nara (do 15 min peš), 2 sobi, brezplačen preklic."],
    },
    "hiroshima": {
        "book": "Miyajima, Hatsukaichi, Hiroshima", "air": "Miyajima--Hiroshima--Japan", "optional": True,
        "where": "Miyajima — ryokan na otoku za mirnejši večer (ko izletniki odidejo).",
        "cheaper": "Nočitve na otoku so dražje kot v Hiroshimi; preverite, ali se splača le za večer.",
        "search": ["Ryokan na Miyajimi z večerjo (če želite videti plavajočo torijo v mraku)."],
    },
}

# --------------------------------------------------------------------------- vstopnice in rezervacije po postajah
BOOK = {
    "tokio": [
        ("Vrta Rikugien in Hamarikyu — urnik, cene, večerna osvetlitev", "https://teien.tokyo-park.or.jp/en/rikugien/",
         "Vstopnina je ob vhodu; pred obiskom preverite urnik osvetlitve."),
        ("Ladjica po reki Sumidi — vozni red in vozovnice", "https://www.suijobus.co.jp/en/", "Tokyo Mizube Line: Hamarikyu ↔ Asakusa."),
        ("Pot z letališča — Skyliner (Keisei) do Uena", SKYLINER, "Vlak do postaje Keisei Ueno."),
    ],
    "kawaguchiko": [
        ("Fujikyu — Fuji Excursion, avtobusi in vozovnice", FUJIKYU, "Vlak in avtobus do jezera Kawaguchi; vozni redi."),
        ("Avtobus Shinjuku → Kawaguchiko (rezervacija)", HIGHWAYBUS, "Rezervirajte sedeže vnaprej."),
    ],
    "chichibu": [
        ("Vlak Seibu Laview — vozovnice (iskanje)", gsearch("Seibu Laview Ikebukuro Chichibu limited express ticket"), "Hitri vlak iz Ikebukura (okoli 80 min)."),
        ("Pot Tokio → Chichibu (Google Zemljevidi)", gdir("Ikebukuro Station", "Seibu-Chichibu Station"), "Vozni red in cena."),
        ("Svetišče Mitake — dostop (iskanje)", gsearch("Mitake shrine Ome Tokyo access hours"), "Dostop in obratovalni čas."),
    ],
    "izu": [
        ("Vlak Izuhakone (Mishima ↔ Shuzenji) — vozni red", gdir("Mishima Station", "Shuzenji Station"), "Povezava z Odorikom ali shinkansnom."),
        ("Niji no Sato — urnik osvetlitve (iskanje)", gsearch("Shuzenji Niji no Sato illumination hours"), "Vstopnina in ure za večerno osvetlitev."),
        ("Ladjica Dogashima — iskanje", gsearch("Dogashima cruise Nishiizu"), "Plovba skozi jame ob obali."),
    ],
    "minobusan": [("Tempelj Kuon-ji — uradna stran", "https://www.kuonji.jp/", "Informacije o templju in dostopu.")],
    "kumano": [
        ("Kumano Travel (Tanabe) — zemljevidi, nastanitve, rezervacije", KUMANO, "Uradni turistični urad za Kumano Kodo."),
        ("Meiko Bus — avtobusi po Kumano Kodo", MEIKO, "Vozni redi in vozovnice."),
    ],
    "koyasan": [
        ("Koyasan Tourist Association — dostop, nastanitve, dogodki", KOYASAN, "Uradna turistična zveza."),
        ("Vozovnica za Koya-san (Nankai, žičnica) — iskanje", klook("Koyasan"), "Paketi vlaka in žičnice."),
    ],
    "iya": [
        ("Hotel Iya Onsen — žičnica in kopel", IYA_ONSEN, "Uradna stran: rezervacije in prevoz."),
        ("Ladjica po soteski Oboke — iskanje", gsearch("Oboke Gorge sightseeing boat Miyoshi"), "Preverite delovni čas čolnov."),
    ],
    "ine": [("Ladjica po zalivu Ine — iskanje", gsearch("Ine Bay sightseeing boat Funaya"), "Plačilo običajno na pomolu.")],
    "kyoto": [
        ("Kyoto Travel — dogodki, osvetlitve, nasveti", KYOTO_TRAVEL, "Uradna turistična stran."),
        ("Osvetlitev templja Eikando — urnik in vstopnice", "https://www.eikando.or.jp/English/", "Večerna osvetlitev javorjev v novembru."),
        ("Čajna ceremonija — termini (Klook)", klook("Kyoto tea ceremony"), "Rezervirajte vnaprej za 4 osebe."),
        ("Čajna ceremonija — termini (GetYourGuide)", gyg("Kyoto tea ceremony"), "Primerjajte cene in ure."),
    ],
    "osaka": [
        ("Grad Osaka — urnik in vstopnice", "https://www.osakacastle.net/english/", "Vstopnice tudi ob vhodu."),
        ("Osaka Amazing Pass — vstopnice in prevoz", OSAKA_INFO, "Preverite, ali se vam izplača za vaš program."),
        ("Ladjica Tombori — iskanje", gsearch("Tombori River Cruise Osaka"), "Plovba po reki Dotonbori."),
    ],
    "nara": [("Todai-ji — uradna stran", "https://www.todaiji.or.jp/en/", "Ure in vstopnina.")],
    "hiroshima": [
        ("Shinkansen Osaka → Hiroshima (Smart EX)", SMART_EX, "Rezervacija sedežev in vozovnice v telefonu."),
        ("Feri na Miyajimo (JR Miyajima Ferry)", MIYAJIMA_FERRY, "Vozni red in cene."),
        ("Peace Memorial Museum — uradna stran", PEACE_MUSEUM, "Ure in vstopnina."),
    ],
}

# --------------------------------------------------------------------------- prevozi med postajami
LEG_LINKS = {
    ("Letališče (Haneda/Narita)", "Tokio"): [
        ("Skyliner (Keisei) — vozovnice", SKYLINER), ("Narita Express (JR East)", NEX),
        ("Vozni red (Google)", gdir("Narita International Airport", "Ueno Station"))],
    ("Tokio", "Chichibu (izlet)"): [
        ("Vozni red (Google)", gdir("Ikebukuro Station", "Seibu-Chichibu Station")),
        ("Seibu Laview — vozovnice", gsearch("Seibu Laview Ikebukuro Chichibu limited express ticket"))],
    ("Tokio", "Fuji – Kawaguchiko"): [
        ("Fuji Excursion / Fujikyu", FUJIKYU), ("Avtobus Shinjuku → Kawaguchiko", HIGHWAYBUS),
        ("Vozni red (Google)", gdir("Shinjuku Station", "Kawaguchiko Station"))],
    ("Fuji – Kawaguchiko", "Minobusan"): [
        ("Vozni red (Google)", gdir("Kawaguchiko Station", "Minobu Station")), ("Navitime", NAVITIME)],
    ("Minobusan", "Izu"): [
        ("Vozni red (Google)", gdir("Minobu Station", "Shuzenji Station")),
        ("Odoriko ekspres — vozovnice", gsearch("JR Odoriko limited express Izu ticket reservation"))],
    ("Izu", "Kumano Kodo"): [
        ("Smart EX — shinkansen do Nagoje", SMART_EX), ("JR Central — informacije (Wide View Nanki)", JR_CENTRAL),
        ("Vozni red (Google)", gdir("Shuzenji Station", "Kii-Katsuura Station"))],
    ("Kumano Kodo", "Koya-san"): [
        ("Vozni red (Google)", gdir("Kii-Katsuura Station", "Koyasan")), ("Koyasan Tourist Association — dostop", KOYASAN),
        ("Meiko Bus", MEIKO)],
    ("Koya-san", "Iya"): [
        ("Smart EX — shinkansen do Okayame", SMART_EX), ("Vozni red (Google)", gdir("Koyasan", "Oboke Station"))],
    ("Iya", "Ine"): [("Vozni red (Google)", gdir("Oboke Station", "Amanohashidate Station")), ("Navitime", NAVITIME)],
    ("Ine", "Kyoto"): [("Vozni red (Google)", gdir("Ine, Kyoto", "Kyoto Station")), ("Navitime", NAVITIME)],
    ("Kyoto", "Osaka"): [("Vozni red (Google)", gdir("Kyoto Station", "Osaka Station")), ("JR West — informacije", JR_WEST)],
    ("Osaka", "Nara (izlet)"): [("Vozni red (Google)", gdir("Osaka Namba Station", "Nara Station")), ("JR West", JR_WEST)],
    ("Osaka", "Hiroshima (izlet)"): [
        ("Smart EX — shinkansen Nozomi", SMART_EX), ("Vozni red (Google)", gdir("Shin-Osaka Station", "Hiroshima Station"))],
    ("Osaka", "Letališče Kansai (KIX)"): [
        ("Haruka (JR West)", JR_WEST), ("Rapi:t (Nankai) — iskanje vozovnic", gsearch("Nankai Rapi:t Namba Kansai Airport ticket")),
        ("Vozni red (Google)", gdir("Namba Station", "Kansai International Airport"))],
}

# --------------------------------------------------------------------------- hitre povezave (Priprave)
QUICKBUY = [
    ("🛂", "Pred prihodom", [
        ("Visit Japan Web — carina in priseljevanje (QR koda)", "https://vjw-lp.digital.go.jp/en/"),
        ("eSIM za Japonsko (Airalo)", "https://www.airalo.com/japan-esim"),
        ("Skyliner z letališča Narita (Keisei)", SKYLINER), ("Narita Express (JR East)", NEX)]),
    ("🚄", "Vlaki (kupi vozovnico, rezerviraj sedež)", [
        ("Smart EX — shinkansen (Tokaido/Sanyo)", SMART_EX), ("JR East — rezervacija (Eki-net)", EKINET),
        ("JR Central — informacije", JR_CENTRAL), ("JR West — Kansai/Haruka", JR_WEST),
        ("Navitime — vozni redi in cene", NAVITIME), ("Jorudan — iskanje povezav", JORUDAN)]),
    ("🚌", "Avtobusi", [
        ("Highway bus — rezervacija (Shinjuku ↔ Kawaguchiko in drugi)", HIGHWAYBUS),
        ("Fujikyu — Fuji", FUJIKYU), ("Meiko Bus — Kumano Kodo", MEIKO)]),
    ("🏨", "Nastanitve (4 osebe, 2 sobi)", [
        ("Booking.com — Japonska", booking("Japan", adults=4, rooms=2)),
        ("Airbnb — Japonska (2+ spalnici)", airbnb("Japan", adults=4)),
        ("Google Hotels — primerjava cen", google_hotels("Japan"))]),
    ("🎟️", "Vstopnice in doživetja", [
        ("Osaka Amazing Pass", OSAKA_INFO), ("Feri na Miyajimo", MIYAJIMA_FERRY),
        ("Peace Memorial Museum Hiroshima", PEACE_MUSEUM), ("teamLab — vstopnice", "https://www.teamlab.art/e/"),
        ("Ghibli muzej", "https://www.ghibli-museum.jp/en/"), ("Klook — izleti in vstopnice", klook("Japan")),
        ("GetYourGuide — izleti", gyg("Japan"))]),
    ("🧳", "Prtljaga in taksi", [
        ("Yamato (Kuro Neko) — pošiljanje kovčkov", "https://www.kuronekoyamato.co.jp/en/"),
        ("GO — taksi aplikacija", "https://go.goinc.jp/en")]),
    ("🌦️", "Vreme", [("Japonska meteorološka agencija", "https://www.jma.go.jp/jma/indexe.html")]),
]

FOOD_LINKS = [      # pri hrani: kje rezervirati mizo za 4
    ("🍽️ Tabelog — ocene in rezervacije", "https://tabelog.com/en/"),
    ("🍽️ TableCheck — spletna rezervacija", "https://www.tablecheck.com/en/japan/"),
    ("📞 Prosite recepcijo hotela, da pokliče in rezervira za 4 osebe", None),
]

DOZ_SEARCH = True     # pri doživetjih dodaj iskanje terminov (Klook, GetYourGuide)

# največja oddaljenost točk od središča postaje (km) — strožje za mesta, širše za pokrajine
GEO_RADIUS = {"tokio": 25, "chichibu": 40, "kawaguchiko": 20, "minobusan": 15, "izu": 35, "kumano": 40, "koyasan": 10,
              "iya": 30, "ine": 25, "nara": 10, "kyoto": 25, "osaka": 25, "hiroshima": 30}

# --------------------------------------------------------------------------- zanimivosti po postajah (previdno formulirane)
FACTS = {
    "tokio": [
        "Križišče Shibuya je eno najbolj obremenjenih prehodov za pešce na svetu: ob zeleni luči ga naenkrat prečka več sto ljudi, ob konicah tudi več tisoč.",
        "Tokijski pitni avtomati prodajajo tudi tople napitke v pločevinkah: rdeča oznaka pomeni toplo, modra hladno.",
        "Sensō-ji v Asakusi velja za najstarejši tempelj v Tokiu; po izročilu je nastal v 7. stoletju, ko sta ribiča v reki Sumidi našla kip boginje Kannon.",
        "Veleprodajna ribja tržnica Tsukiji se je leta 2018 preselila v Toyosu; zunanja tržnica Tsukiji (stojnice in lokali) pa še vedno deluje.",
        "Soseska Yanaka je večinoma preživela potres iz leta 1923 in bombardiranje v drugi svetovni vojni, zato ima še vedno vzdušje starega Tokia.",
    ],
    "chichibu": [
        "Nočni festival Chichibu (2.–3. december) velja za enega od treh največjih japonskih festivalov z okrašenimi vozovi, poleg Gion v Kyotu in Takayame.",
        "Romarska pot po Chichibuju povezuje 34 templjev, posvečenih boginji Kannon — krajša in mirnejša različica velikih romarskih poti.",
        "Soba (ajdovi rezanci) so tu domača jed: pokrajina ima hladno podnebje in kamnita tla, kjer ajda dobro uspeva.",
        "Pri kraju Nagatoro so po reki Arakawa naravne skalne terase (iwadatami), ki jih Japonci cenijo kot naravno znamenitost; po reki vozijo tudi čolni.",
    ],
    "kawaguchiko": [
        "Fuji je visok 3.776 m — najvišja gora Japonske. Od leta 2013 je na Unescovem seznamu svetovne dediščine kot kulturna krajina, ne kot naravna znamenitost.",
        "Okoli Fujija so pet jezer (Fuji Goko): Kawaguchi, Yamanaka, Sai, Shoji in Motosu. Kawaguchi je najlažje dostopno.",
        "Pagoda Chureito stoji na vrhu okoli 400 stopnic v parku Arakurayama Sengen; zgornji razgled je ena najbolj znanih japonskih razglednic.",
        "Hoto — debeli ploščati rezanci v miso juhi z bučo — so specialiteta pokrajine Yamanashi; po legendi so jed bojevnikov pod vodstvom Takede Shingena.",
    ],
    "minobusan": [
        "Pred gorskim templjem Kuon-ji vodi 287 stopnic, imenovanih Bodaitei — romarji jih premagajo kot del čiščenja duha.",
        "Menih Nichiren je na gori Minobu preživel približno 9 let (od 1274); tu je zapisal veliko svojih spisov, danes je Kuon-ji glavni tempelj njegove šole.",
        "V šukuboju vas običajno čaka tatami soba, vegetarijanska večerja (shojin ryori) in jutranja molitev ob zori; goste prosijo, naj molitev spoštujejo.",
    ],
    "izu": [
        "Polotok Izu je od leta 2018 Unescov geopark: ima vulkanske kraterje, vroče vrelce in obalo, nastalo iz lave.",
        "Shuzenji onsen po izročilu sega v leto 807, ko naj bi menih Kūkai z vajro udaril ob skalo in iz nje pritekla vroča voda.",
        "Pokrajina okoli Amagija slovi po pridelavi wasabija v kamnitih potokih; sveži wasabi, nariban na somoten rezek ribe, je povsem drugačen od tistega iz tube.",
        "Obala Jogasaki je nastala iz lave vulkana Omuro (pred približno 4.000 leti); čez zaliv jo povezuje viseči most Kadowaki.",
        "V Shimodi je po prihodu komodorja Perryja (1854) začel delovati prvi ameriški konzulat na Japonskem.",
    ],
    "kumano": [
        "Kumano Kodo in pot v Santiago de Compostela sta edini dve romarski poti na svetu s skupnim imenom in znakom »dvojni romar«, ki sta se pobratili leta 1998.",
        "Slap Nachi je z okoli 133 m najvišji neprekinjeni slap na Japonskem; kamen pod njim častijo kot svetega.",
        "Velika torija Oyunohara pred Hongu Taisha je visoka okoli 34 m — ena največjih na Japonskem.",
        "Kopel Tsuboyu v kraju Yunomine je edina kopel, ki je zaščitena kot del Unescove svetovne dediščine.",
        "Trinožni vran Yatagarasu je simbol Kumana; po izročilu je vodil prvega cesarja Jimmuja skozi gore — njegova podoba je tudi na grbu japonske nogometne zveze.",
    ],
    "koyasan": [
        "Koya-san je leta 816 ustanovil menih Kōbō Daishi (Kūkai), ustanovitelj japonskega budizma Shingon.",
        "Pokopališče Okunoin ima več kot 200.000 nagrobnikov — med cedrami vodi 2 km dolga pot do mavzoleja ustanovitelja.",
        "Po verovanju Kūkai ni umrl, ampak še vedno meditira v mavzoleju. Menihi mu dvakrat na dan prinesejo obrok.",
        "Na gori je več kot 100 templjev; približno polovica jih sprejema goste v šukuboju.",
        "Shojin ryori je vegetarijanska budistična kuhinja; sezamov tofu (goma-dofu) je specialiteta Koya-sana.",
    ],
    "iya": [
        "Viseči most Iya Kazurabashi je iz divje trte (sarunashi) in ga obnavljajo približno vsaka tri leta — ker trta sčasoma oslabi.",
        "Po legendi so se v dolini Iya skrivali preživeli poraženega klana Heike (Taira) po bitki leta 1185.",
        "Na pečini nad sotesko stoji kip »fantiča, ki lula« (Oshikko-kozo), ki spominja na otroke, ki so se včasih drznili poseči čez pečino.",
        "Soteska Oboke (reka Yoshino) je znana po ladjicah in raftingu; pokrajina Iya velja za eno najbolj odročnih na Japonskem.",
    ],
    "ine": [
        "V zalivu Ine stoji približno 230 hiš funaya — v pritličju je pristanišče za čolne, zgoraj pa stanovanje.",
        "Zaliv je zaščiten z otokom Aoshima, zato je voda zelo mirna; razlika med plimo in oseko je le okoli 50 cm.",
        "Vas je od leta 2005 zaščitena kot pomembno območje tradicionalnih stavb.",
        "Ribiška tradicija: zaradi mirne vode so hiše postavili tik ob rob zaliva, da se čolni zapeljejo kar v hišo.",
    ],
    "nara": [
        "V parku Nara živi okoli 1.200 jelenov, ki jih častijo kot božje glasnike svetišča Kasuga.",
        "Nara je bila prva stalna prestolnica Japonske (Heijō-kyō, 710–784).",
        "Veliki Buda v Todai-ji je visok okoli 15 m; stavba Daibutsuden velja za eno največjih lesenih zgradb na svetu.",
        "Jelene hranite samo z uradnimi piškoti (shika senbei), ki jih prodajajo v parku — drugih jedi jim ne dajajte.",
        "Svetišče Kasuga Taisha ima več kot 3.000 kamnitih in bronastih svetilk, ki jih dvakrat na leto prižgejo na festivalu Mantōrō.",
    ],
    "kyoto": [
        "Kyoto je bil prestolnica Japonske okoli 1.000 let (794–1868).",
        "Kyoto ima 17 objektov na Unescovem seznamu »Zgodovinski spomeniki starodavnega Kyota«.",
        "Svetišče Fushimi Inari ima okoli 10.000 torij; vsaka je dar podjetja ali posameznika.",
        "V nekaterih zasebnih ulicah Giona fotografiranje ni več dovoljeno — spoštujte znake, ki zaščitijo prebivalce in maiko.",
        "Jesenske barve (koyo) so v Kyotu običajno na vrhuncu od srede do konca novembra.",
        "Uji, južno od Kyota, je slavna po čaju: tamkajšnja matcha se pogosto šteje za najboljšo na Japonskem.",
    ],
    "osaka": [
        "Osaka ima vzdevek »kuhinja Japonske« (tenka no daidokoro) — nekoč je bila središče trgovine z rižem.",
        "Reklo kuidaore (»jej, dokler ne zbankrotiraš«) poznajo kot motto osaškega zadovoljevanja z jedjo.",
        "Takoyaki naj bi izumil Endō Tomekichi leta 1935 v Osaki, in sicer kot nadgradnjo jedi akashiyaki.",
        "Grad Osaka je vladar Toyotomi Hideyoshi začel graditi leta 1583; sedanji grad je rekonstrukcija iz 20. stoletja.",
        "Na tekočih stopnicah se v Osaki stoji na desni, v Tokiu na levi — zanimiv kulturni zaplet.",
    ],
    "hiroshima": [
        "Prva atomska bomba je padla 6. avgusta 1945; kupola Genbaku je na Unescovem seznamu od 1996.",
        "Spomenik otrokom (Children's Peace Monument) spominja na Sadako Sasaki in 1.000 papirnatih žerjavov.",
        "Plavajoča torija na Miyajimi je ena najbolj fotografiranih; sedanja stoji od leta 1875.",
        "Okonomiyaki po hirošimsko ima plasti: testo, zelje, meso in rezanci — drugače kot v Osaki, kjer se vse zmeša.",
        "Zaliv Hiroshima daje okoli 60 % japonskih ostrig; po pristanišču Miyajima jih nabirajo še danes.",
        "Plamen miru v parku gori od leta 1964 in bo gorel, dokler ne bo uničeno vse jedrsko orožje.",
    ],
}

QUIZ = {
    "ranks": [
        {"min": 0, "e": "🌱", "t": "Radovedni popotnik", "x": "Ni hudega — vsaka pot se začne z zanimivostjo. Poglejte postaje in poskusite znova!"},
        {"min": 6, "e": "🍵", "t": "Čajni učenec", "x": "Lepo znanje! Z vsako postajo ga bo več."},
        {"min": 10, "e": "⛩️", "t": "Romar", "x": "Odlično — Japonsko že precej poznate."},
        {"min": 14, "e": "🏆", "t": "Mojstrica Japonske", "x": "Popoln spoznavalec! Pripravljene ste na pot."},
    ],
    "questions": [
        {"q": "Kako visoka je gora Fuji?", "a": ["3.200 m", "3.776 m", "4.500 m"], "c": 1, "e": "Fuji je visok 3.776 m — najvišja gora Japonske."},
        {"q": "Kateri je najvišji neprekinjeni slap na Japonskem?", "a": ["Nachi", "Kegon", "Fukuroda"], "c": 0, "e": "Slap Nachi je visok okoli 133 m."},
        {"q": "Kdo je leta 816 ustanovil Koya-san?", "a": ["Nichiren", "Kōbō Daishi (Kūkai)", "Šogun Tokugawa"], "c": 1, "e": "Kūkai, ustanovitelj budizma Shingon, je izbral samoten gorski kraj."},
        {"q": "Koliko nagrobnikov je približno na pokopališču Okunoin?", "a": ["20.000", "200.000", "2 milijona"], "c": 1, "e": "Več kot 200.000 — med stoletnimi cedrami."},
        {"q": "Koliko približno torij ima svetišče Fushimi Inari v Kyotu?", "a": ["100", "1.000", "10.000"], "c": 2, "e": "Okoli 10.000 torij, vsaka je dar."},
        {"q": "Kako pogosto obnavljajo viseči most Iya Kazurabashi iz trte?", "a": ["Vsako leto", "Približno vsaka 3 leta", "Vsakih 50 let"], "c": 1, "e": "Trta s časom oslabi, zato jo menjajo okoli vsaka tri leta."},
        {"q": "Koliko jelenov živi v parku Nara?", "a": ["Okoli 12", "Okoli 120", "Okoli 1.200"], "c": 2, "e": "Okoli 1.200 jelenov — častijo jih kot božje glasnike."},
        {"q": "Kaj pomeni osaška reklo »kuidaore«?", "a": ["Jej do bankrota", "Spi do poldneva", "Hodi do jutra"], "c": 0, "e": "Osaka je »kuhinja Japonske«."},
        {"q": "Katera je bila prva stalna prestolnica Japonske?", "a": ["Kyoto", "Nara", "Osaka"], "c": 1, "e": "Nara (Heijō-kyō) od leta 710."},
        {"q": "Koliko časa je bil Kyoto prestolnica?", "a": ["Okoli 100 let", "Okoli 500 let", "Okoli 1.000 let"], "c": 2, "e": "Od leta 794 do 1868."},
        {"q": "Kaj pomeni »shinrin-yoku«?", "a": ["Gozdna kopel", "Čajna slovesnost", "Jutranji sprehod po mestu"], "c": 0, "e": "Pomirjajoče bivanje med drevesi — priznana praksa za zdravje."},
        {"q": "V kateri pokrajini so doma rezanci hoto v miso juhi?", "a": ["Hokkaido", "Yamanashi (Fuji)", "Okinawa"], "c": 1, "e": "Hoto je jed pokrajine Yamanashi pod goro Fuji."},
        {"q": "Koliko približno hiš funaya stoji v zalivu Ine?", "a": ["Okoli 30", "Okoli 230", "Okoli 2.300"], "c": 1, "e": "Okoli 230 hiš nad vodo."},
        {"q": "Kdaj se je ribja tržnica Tsukiji preselila v Toyosu?", "a": ["2008", "2018", "1998"], "c": 1, "e": "Leta 2018; zunanja tržnica Tsukiji ostaja."},
        {"q": "Približno kolikšen delež japonskih ostrig prihaja iz zaliva Hiroshima?", "a": ["Okoli 6 %", "Okoli 20 %", "Okoli 60 %"], "c": 2, "e": "Okoli 60 % — še posebej pozimi."},
    ],
}

LOV = [
    {"t": "Na ulici in na vlaku", "x": "Opazita in označita, kar vidita.", "items": [
        {"id": "torii", "e": "⛩️", "n": "Torija"}, {"id": "avtomat", "e": "🥤", "n": "Pitni avtomat s toplo pijačo"},
        {"id": "konbini", "e": "🍙", "n": "Onigiri iz konbinija"}, {"id": "shinkansen", "e": "🚄", "n": "Shinkansen"},
        {"id": "neko", "e": "🐱", "n": "Maneki-neko"}, {"id": "lanterna", "e": "🏮", "n": "Rdeča papirnata svetilka"},
        {"id": "neonka", "e": "🌃", "n": "Neonski napis ponoči"}, {"id": "vrsta", "e": "🧍", "n": "Mirno stoječa vrsta"},
    ]},
    {"t": "V templju in svetišču", "items": [
        {"id": "ema", "e": "🪵", "n": "Ema (lesena ploščica želja)"}, {"id": "omikuji", "e": "📜", "n": "Omikuji (listek sreče)"},
        {"id": "jizo", "e": "🧸", "n": "Kip Jizo z rdečo bibico"}, {"id": "zvon", "e": "🔔", "n": "Veliki zvon"},
        {"id": "temizu", "e": "💧", "n": "Čistilni vodnjak (temizuya)"}, {"id": "kitsune", "e": "🦊", "n": "Kamnita lisica (kitsune)"},
        {"id": "pagoda", "e": "🏯", "n": "Pagoda"}, {"id": "kamen", "e": "🪨", "n": "Kamnita svetilka"},
    ]},
    {"t": "Narava in jesen", "items": [
        {"id": "javor", "e": "🍁", "n": "Rdeč javor"}, {"id": "ginkgo", "e": "🍂", "n": "Zlata ginkgo"},
        {"id": "fuji", "e": "🗻", "n": "Gora Fuji"}, {"id": "jelen", "e": "🦌", "n": "Jelen v Nari"},
        {"id": "bambus", "e": "🎋", "n": "Bambusov gaj"}, {"id": "slap", "e": "🌊", "n": "Slap ali soteska"},
    ]},
    {"t": "Okusi", "items": [
        {"id": "matcha", "e": "🍵", "n": "Matcha"}, {"id": "sushi", "e": "🍣", "n": "Sushi"}, {"id": "ramen", "e": "🍜", "n": "Ramen ali soba"},
        {"id": "takoyaki", "e": "🐙", "n": "Takoyaki"}, {"id": "dango", "e": "🍡", "n": "Dango ali mochi"},
        {"id": "shojin", "e": "🥬", "n": "Shojin ryori (templjska kuhinja)"}, {"id": "hoto", "e": "🥣", "n": "Hoto (rezanci pod Fujijem)"},
        {"id": "okonomi", "e": "🥞", "n": "Okonomiyaki"},
    ]},
    {"t": "Doživetja", "items": [
        {"id": "onsen", "e": "♨️", "n": "Onsen"}, {"id": "tatami", "e": "🛏️", "n": "Spanje na tatamiju"},
        {"id": "yukata", "e": "👘", "n": "Yukata v ryokanu"}, {"id": "caj", "e": "🫖", "n": "Čajna slovesnost"},
        {"id": "bonsai", "e": "🌳", "n": "Bonsaj"}, {"id": "maiko", "e": "💃", "n": "Maiko ali geiko (ob sreči)"},
    ]},
    {"t": "Števci", "items": [
        {"id": "c_torii", "e": "⛩️", "n": "Torije, ki sta jih prehodili", "count": True},
        {"id": "c_avtomat", "e": "🥤", "n": "Pitni avtomati, ki sta jih naštele", "count": True},
        {"id": "c_slike", "e": "📸", "n": "Fotografije za knjigo", "count": True},
    ]},
]

# izbor izzivov (indeksi iz izzivi.json) — manj izzivov na dan: ena-dnevne postaje 2, ostale 3.
# Spremeni seznam, če želiš kakšnega vrniti; izzivi.json ostane poln.
IZZIVI_KEEP = {
    "tokio": [0, 2, 3], "chichibu": [0, 2], "kawaguchiko": [0, 1], "minobusan": [0, 1],
    "izu": [0, 1, 3], "kumano": [0, 1, 3], "koyasan": [0, 1, 2], "iya": [0, 1, 2], "ine": [0, 1, 2],
    "nara": [0, 1], "kyoto": [0, 1, 3], "osaka": [0, 1, 3], "hiroshima": [1, 3],
}
