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
