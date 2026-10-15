# -*- coding: utf-8 -*-
"""Prevoz po postajah (Japonska): možnosti na kraju, kako od nastanitve do načrtovanih znamenitosti,
taksi, aplikacije in povezave. Cene so namenoma »okoli« (po objavljenih podatkih) — vedno jih preverite pri viru.

Struktura TRANSPORT[postaja]:
  from / from_label  izhodišče za Google Zemljevide (nastanitev ali glavna postaja)
  arrive             (od, do, besedilo) — kako priti do postaje (podrobnosti so tudi v Načrtu poti)
  intro              kratek povzetek (naveže se na bivanje)
  options            [(emoji, naslov, besedilo)]
  sights             besedilo za vsako znamenitost v vrstnem redu GUIDE[postaja]["sights"] ("" = izpusti)
  taxi               besedilo o taksiju
  apps               [(ime, besedilo, url)]
  links              [(oznaka, url)]
  tips               [besedilo]
"""
from links import gdir, gsearch
from data_jp import (SMART_EX, NAVITIME, JORUDAN, SKYLINER, NEX, FUJIKYU, HIGHWAYBUS, MEIKO, KUMANO, KOYASAN,
                     IYA_ONSEN, KYOTO_TRAVEL, OSAKA_INFO, MIYAJIMA_FERRY, JR_WEST, JR_CENTRAL)

GO_TAXI = "https://go.goinc.jp/en"
YAMATO = "https://www.kuronekoyamato.co.jp/en/"
ICOCA = "https://www.jr-odekake.net/icoca/"
TOKYO_METRO = "https://www.tokyometro.jp/en/"
SUIJOBUS = "https://www.suijobus.co.jp/en/"
TOKAI_BUS = "https://www.tokaibus.jp/"
KYOTO_BUS = "https://www2.city.kyoto.lg.jp/kotsu/webguide/en/"
OSAKA_METRO = "https://subway.osakametro.co.jp/en/"
HIRODEN = "https://www.hiroden.co.jp/en/"
HIROSHIMA_NAVI = "https://dive-hiroshima.com/en/"
KINTETSU = "https://www.kintetsu.co.jp/foreign/english/"
SEIBU = "https://www.seiburailway.jp/english/"
CHICHIBU_RAILWAY = "https://www.chichibu-railway.co.jp/"
SHIKOKU = "https://shikoku-tourism.com/en/"
INE_KANKO = "https://ine-kankou.jp/"
JNTO = "https://www.japan.travel/en/plan/getting-around/"

# Aplikacije, ki jih pokažemo pri vsaki postaji (poleg posebnih)
TRANSPORT_APPS = [
    ("Google Zemljevidi", "vozni redi, peron, cena in čas hoje; zemljevid območja shranite za uporabo brez povezave", "https://www.google.com/maps"),
    ("Japan Travel by NAVITIME", "iskalnik poti za vlake in avtobuse po vsej Japonski (angleško)", NAVITIME),
    ("GO — taksi", "naročilo taksija z naslovom v japonščini in plačilom v aplikaciji (v večjih mestih in turističnih krajih)", GO_TAXI),
    ("Suica / ICOCA", "prepaid kartica (tudi v Apple Wallet na iPhonu, če jo podpira vaš telefon): tapnete ob vstopu in izstopu, velja v vlakih, metroju in avtobusih", ICOCA),
]

TAXI_NOTE = ("Vrata se odprejo sama (ne dotikajte se jih). Napitnine ni. Naslov pokažite na zaslonu — "
             "v razdelku »Kartice za taksista« imate japonski zapis za najpogostejše cilje.")

TRANSPORT = {
    # ------------------------------------------------------------------ TOKIO
    "tokio": {
        "from": "Ueno Station, Tokyo", "from_label": "postaja Ueno (nastanitev v Uenu/Asakusi)",
        "arrive": ("Narita Airport", "Keisei Ueno Station, Tokyo",
                   "Z letališča Narita pripelje Skyliner (Keisei) do postaje Keisei Ueno v približno 40–45 minutah; cena enosmerne vozovnice je po objavljenih podatkih okoli 2.500 jenov in se ob nakupu vnaprej prek spleta nekoliko zniža. "
                   "Alternativa je Narita Express (JR) do postaj Tokio/Shinjuku. Z Hanede je do Uena okoli 40–60 minut (monorail ali Keikyu in nato JR/metro)."),
        "intro": "Tokio se najlažje prečka z vlaki in metrojem, nastanitev v Uenu pa je za vaš načrt idealna: tam se stikajo JR Yamanote, metro Ginza in Hibiya ter Skyliner. Taksi potrebujete le z velikimi kovčki, v dežju ali pozno zvečer.",
        "options": [
            ("🚇", "Metro in JR", "Enkratna vožnja stane po razdalji okoli 180–330 jenov. Najlažje je s kartico Suica/ICOCA: tapnete ob vstopu in ob izstopu, kartico pa dopolnite na avtomatih ali v Apple Wallet. JR Yamanote je krožna proga okoli središča — prava »hrbtenica« mesta."),
            ("🎫", "Dnevna vozovnica za metro", "Tokyo Subway Ticket (24, 48 ali 72 ur) za turiste je po objavljenih podatkih okoli 800, 1.200 ali 1.500 jenov, a velja le za metro (ne JR). Splača se šele, ko računate vsaj 4–5 voženj na dan — sicer je ceneje s Suico."),
            ("⛴️", "Ladjica po reki Sumidi", "Ladjice iz Asakuse proti Hamarikyuju in Odaibi so hkrati prevoz in doživetje; cena za Asakusa → Hamarikyu je po objavljenih podatkih okoli 1.000–1.500 jenov. Vozni red in vozovnice: spodaj."),
            ("🧳", "Kovčki naprej", "Če se selite iz hotela v hotel, pošljete kovčke prek Yamato (Kuro Neko) TA-Q-BIN: pri recepciji izpolnite obrazec, kovček pride naslednji dan; cena je odvisna od velikosti in razdalje (običajno nekaj tisoč jenov). Tako se v vlak odpravite le z nahrbtnikom."),
        ],
        "sights": [
            "JR Yamanote od Uena do postaje Komagome (okoli 10–12 min), nato okoli 7 min peš do vhoda.",
            "JR Yamanote do postaje Harajuku (okoli 25–30 min), vhod v svetišče je tik ob postaji. Pot vodi skozi gozd, računajte še 15–20 min hoje do svetišča.",
            "Najlažje peš: iz Uena v 15 min (po parku) ali z JR do postaje Nippori (2 postaji, okoli 5 min); Yanaka Ginza je 3 min od zahodnega izhoda.",
            "Metro Hibiya iz Uena do postaje Tsukiji (okoli 15–20 min) ali Tsukijishijo (Oedo); tržnica je tik zraven. Najbolj živahno je dopoldne.",
            "Metro Ginza iz Uena do Asakuse (okoli 5 min), pristanišče je 5 min peš od postaje. Ladjica pripelje tudi do Hamarikyuja.",
            "Najlepše z ladjico iz Asakuse (okoli 35–40 min); sicer JR do Shimbashija (okoli 15 min) in 12 min peš, ali metro Oedo do postaje Shiodome.",
            "Metro Ginza iz Uena do postaje Gaienmae (okoli 25 min, brez prestopanja), izhod za ginko je ob postaji. Zvečer in v jutranjem soncu je najlepše.",
            "Metro Chiyoda: Ueno → Nezu je enostavno prek postaje Nippori in nato 5 min hoje; ali peš skozi park Ueno okoli 20 min.",
        ],
        "taxi": ("Taksi se v Tokiu ustavi na dvignjeno roko ali pred postajo; rdeča lučka »空車« pomeni prost. Začetna cena je po objavljenih tarifah okoli 500 jenov za prvih nekaj sto metrov, nato se števec dviguje. "
                 "Pet kilometrov v središču običajno stane okoli 1.800–2.800 jenov; ponoči (22–5) je doplačilo okoli 20 %. Za štiri osebe je krajša vožnja pogosto ceneje kot štirje vozni listki."),
        "links": [("🚇 Tokyo Metro — vozovnice in proge", TOKYO_METRO), ("⛴️ Tokyo Cruise — ladjice po Sumidi", SUIJOBUS),
                  ("🛫 Skyliner Narita ↔ Ueno", SKYLINER), ("🚆 Narita Express (JR East)", NEX),
                  ("🧳 Yamato — pošiljanje kovčkov", YAMATO), ("🚕 GO — taksi", GO_TAXI)],
        "tips": ["Prvi dan si kupite kartico Suica/ICOCA ali jo dodajte v Apple Wallet, preden se zapeljete v mesto.",
                 "Na izhodih iz postaj poiščite številko izhoda (npr. »A4«) — v Google Zemljevidih je navedena; prihrani 10 minut iskanja.",
                 "Prometne konice (7.30–9.30 in 17–19) so zelo polne — s kovčki jih skušajte obiti."],
    },
    # ------------------------------------------------------------------ CHICHIBU
    "chichibu": {
        "from": "Seibu-Chichibu Station, Chichibu", "from_label": "postaja Seibu-Chichibu (izlet iz Tokia)",
        "arrive": ("Ikebukuro Station, Tokyo", "Seibu-Chichibu Station, Chichibu",
                   "Ekspres Seibu »Laview« vozi iz Ikebukura do Seibu-Chichibuja v okoli 80 minutah; skupaj z doplačilom za ekspres je cena po objavljenih podatkih okoli 1.500–2.000 jenov enosmerno. "
                   "Sedeži so rezervirani, zato kupite vozovnico vnaprej (spletno ali v avtomatu). Cenejša in počasnejša je vožnja z lokalnimi vlaki."),
        "intro": "Chichibu je izlet iz Tokia in se vrne zvečer. Trije »svetovi«: Chichibu mesto (svetišče, onsen), Nagatoro (reka, park Tsukinoishi, Hodosan) in gora Mitake na zahodu Tokia, ki je drugačen izlet. Najlažje je izbrati en dan za dva sveta.",
        "options": [
            ("🚆", "Seibu in Chichibu Railway", "Seibu vlak pripelje do Seibu-Chichibuja; za Nagatoro in Hodosan prestopite na lokalno linijo Chichibu Railway (nekaj minut hoje med postajama). Lokalne vožnje stanejo okoli 200–600 jenov; za več postankov vprašajte po dnevni vozovnici (»free pass«)."),
            ("🚌", "Avtobusi", "Lokalni avtobusi vozijo do svetišč in razgledišč, a redkeje. Pred odhodom preverite zadnji avtobus nazaj."),
            ("🚕", "Taksi", "Pred postajo stoji nekaj taksijev; za Hodosan ali Tsukinoishi je krajša vožnja ceneje kot čakanje na avtobus."),
        ],
        "sights": [
            "Mitake je na zahodu Tokia, ne v Chichibuju: JR Chuo in nato JR Ome Line do postaje Mitake (okoli 1,5–2 h iz Shinjuka), avtobus do spodnje postaje žičnice, nato vzpenjača. Drug dan kot Chichibu.",
            "Isti dan kot Mitake: od postaje Mitake peš ob reki Tama (okoli 20–30 min do muzeja Gyokudo in pivovarne Sawanoi).",
            "Vlak Chichibu Railway do postaje Nagatoro (okoli 30 min iz Chichibuja), od tam peš do pristanišča (okoli 10 min). Vožnja z ladjico po reki traja okoli 30 minut.",
            "Peš ali s taksijem od postaje Nagatoro (okoli 15–20 min hoje) — park je lepo osvetljen zvečer; preverite, do kdaj vozi zadnji vlak.",
            "Vlak do postaje Hodosan (okoli 4 postaje od Chichibuja) in nato okoli 10 min peš do spodnje postaje gondole; gondola traja okoli 5 minut.",
            "Svetišče Chichibu je okoli 10–12 min peš od postaje Seibu-Chichibu (ali 5 min od postaje Chichibu na lokalni progi). Nočni festival (3. 12.) je gneča — pridite zgodaj.",
            "Okutama je drugačna smer: JR Ome Line do postaje Okutama (okoli 2 uri iz Shinjuka) in nato avtobus do jezera/centra za obiskovalce.",
            "Onsen Matsuri no Yu je prav ob postaji Seibu-Chichibu — idealen za konec dneva pred vlakom domov (okoli 1.000 jenov, preverite).",
        ],
        "taxi": "Taksijev je malo — naročite ga prek nastanitve ali prek aplikacije GO, če je na voljo. Za ceno pogosto računajo okoli 700–1.000 jenov za prvih 2 km in nato po števcu; za Hodosan ali Tsukinoishi je to okoli 2.000–3.500 jenov, odvisno od izhodišča.",
        "links": [("🚆 Seibu — vozovnice in Laview", SEIBU), ("🚂 Chichibu Railway — vozni red in vozovnice", CHICHIBU_RAILWAY),
                  ("🧭 Pot Tokio → Chichibu (Google)", gdir("Ikebukuro Station", "Seibu-Chichibu Station"))],
        "tips": ["Dan si razdelita: Chichibu mesto + Nagatoro ali Mitake. Oba hkrati je preveč.",
                 "Zadnji vlak proti Tokiu preverite že zjutraj in si ga zapišite."],
    },
    # ------------------------------------------------------------------ IZU
    "izu": {
        "from": "Shuzenji Station, Izu, Shizuoka", "from_label": "postaja Shuzenji (nastanitev v Shuzenjiju)",
        "arrive": ("Minobu Station, Yamanashi", "Shuzenji Station, Izu, Shizuoka",
                   "Iz Minobuja z JR Minobu Line do Fujija, nato Tokaido do Mishime in z linijo Izuhakone Sunzu (Mishima → Shuzenji) v okoli 35 minutah; skupaj okoli 3–4 ure. "
                   "Alternativa za del poti je shinkansen »Kodama«. Celotno pot si nastavite v Google Zemljevidih na dan vožnje."),
        "intro": "Izu je velik polotok in tu javni prevoz ni zelo gost. Shuzenji je izhodišče za sprehode peš (onsen mesto, bambusova pot), za oddaljene točke (obala, slapovi, Dogashima) pa računajte na avtobuse ali sightseeing taksi. Ne poskušajte vsega — razporedite jih po dnevih.",
        "options": [
            ("🚆", "Izuhakone Sunzu Line", "Lokalna proga Mishima ↔ Shuzenji (okoli 35 min); cena okoli 600 jenov. Odličen priklop na shinkansen/JR v Mishimi."),
            ("🚌", "Tokai Bus", "Glavni avtobusni prevoznik na Izuju: linije Shuzenji ↔ Kawazu, Dogashima in Ito. Vožnje trajajo 40–90 minut in vozijo redko (nekaj na uro ali manj) — preverite urnik za povratek."),
            ("🚕", "Sightseeing taksi", "Pri postaji ali nastanitvi vprašajte po »kanko taksiju« (turistični taksi): fiksna cena na uro ali po poti; za štiri osebe je za oddaljene točke (Kawazu, Omuro, Jogasaki) pogosto smiselno. Rezervirajte dan prej."),
            ("🚲", "Peš po Shuzenjiju", "Staro središče, bambusova pot in svetišče so peš: okoli 15–25 minut med točkami. Od postaje Shuzenji do središča mesta vozi lokalni avtobus (okoli 6–10 minut)."),
        ],
        "sights": [
            "Od postaje Shuzenji z avtobusom do središča onsen mesta (okoli 10 min); od tam vse peš. Ob večerih je lepo osvetljeno.",
            "Avtobus od postaje Shuzenji do Niji no Sato (okoli 20–25 min, ni pogost); ali taksi okoli 15 min. Osvetlitev javorjev je zvečer — preverite zadnji avtobus nazaj.",
            "Obala Jogasaki je na vzhodni strani: z JR/Izukyu prek Ita in nato peš od postaje Jogasaki-kaigan (okoli 10 min do mostu Kadowaki). Skupaj okoli 1,5–2 h iz Shuzenjija.",
            "Avtobus Tokai Bus Shuzenji → Kawazu (okoli 1 h), nato lokalni avtobus do slapov (okoli 30 min). Za en dan: vozni red je ključen, ali taksi.",
            "Iz Shuzenjija z Izuhakone do postaje Izu-Nagaoka (okoli 12 min), nato avtobus ali taksi do vznožja žičnice; terasa Ao je na vrhu.",
            "Najlažje z lokalnim vlakom/avtobusom do Izukogena in nato avtobus do gore Omuro (okoli 20 min); vzpenjača do vrha.",
            "Izu Shaboten Zoo je ob Izukogenu (okoli 10 min z avtobusom od postaje Izukogen); kapibare so v toplih kopelih predvsem pozimi (okoli decembra, preverite).",
            "Ladjica med jamami Dogashime: Tokai Bus Shuzenji → Dogashima (okoli 1 h 20 min); plan za celo popoldne.",
        ],
        "taxi": "Taksi v Shuzenjiju stoji pred postajo, pogosto pa ga naročite prek nastanitve. Od postaje do središča mesta je okoli 1.000–1.500 jenov; za oddaljene točke (Kawazu, Omuro) je to več tisoč jenov, zato vprašajte za fiksno ceno ali turistični najem.",
        "links": [("🚌 Tokai Bus — vozni redi", TOKAI_BUS), ("🧭 Mishima → Shuzenji (Google)", gdir("Mishima Station", "Shuzenji Station")),
                  ("🔎 Izuhakone Sunzu Line (iskanje)", gsearch("Izuhakone Railway Sunzu Line timetable Mishima Shuzenji"))],
        "tips": ["Izberite 2–3 točke na dan; avtobusi na Izuju vozijo malo, čakanje je dolgo.",
                 "Večerja v ryokanu je običajno ob določeni uri (okoli 18.00) — upoštevajte jo pri načrtovanju povratka z izleta."],
    },
    # ------------------------------------------------------------------ KAWAGUCHIKO
    "kawaguchiko": {
        "from": "Kawaguchiko Station, Yamanashi", "from_label": "postaja Kawaguchiko (jezero Kawaguchi)",
        "arrive": ("Shinjuku Station, Tokyo", "Kawaguchiko Station, Yamanashi",
                   "Najhitreje z ekspresom »Fuji Excursion« iz Shinjuka (okoli 2 uri, na JR + Fujikyu). Alternativa je neposredni avtobus Highway Bus iz Shinjuka (Busta) v okoli 1 h 45 min–2 h; cena je po objavljenih podatkih okoli 2.000–2.500 jenov. Rezervirajte sedež vnaprej — ob koncih tedna in v jeseni so polni."),
        "intro": "Kawaguchiko je središče za Fuji; razgledov je veliko, a so razdalje med točkami velike. Z avtobusi na krožnih linijah okoli jezera (Red/Green/Blue Line) obiščete večino točk, pagoda Chureito pa je že na drugi strani, v Fujiyoshidi.",
        "options": [
            ("🚌", "Krožni avtobusi okoli jezera", "Fujikyu vozi krožne linije (rdeča, zelena, modra) okoli jezera. Dnevna vozovnica je po objavljenih podatkih okoli 1.500–2.000 jenov (preverite pri Fujikyu); pri 3+ vožnjah se splača."),
            ("🚆", "Fujikyu Line", "Vlak Kawaguchiko ↔ Otsuki ali Shimoyoshida (za Chureito); lokalne vožnje so ceneje kot avtobus."),
            ("🚕", "Taksi", "Kratke vožnje po jezeru stanejo okoli 1.500–3.000 jenov; za štiri osebe je to pogosto ceneje kot avtobusi, zlasti če avtobus zamudite."),
            ("🚲", "Kolo ali e-kolo", "Pri postaji ali jezeru izposojate kolesa; obhod jezera je okoli 20 km, zato e-kolo (okoli 2.000–3.000 jenov na dan, preverite). Dežuje pogosto in je mrzlo — samo za jasen dan."),
        ],
        "sights": [
            "Fujikyu Line do postaje Shimoyoshida (okoli 15 min, 400–500 jenov), nato okoli 15 min hoje in okoli 400 stopnic navzgor. Ob koncih tedna je gneča.",
            "Rdeča krožna linija ali taksi (okoli 15–20 min); park je ob severni obali jezera.",
            "Žičnica je 5 min peš od postaje Kawaguchiko; vožnja do vrha traja okoli 3 minute.",
            "Avtobus Fujikyu iz Kawaguchika (okoli 25–35 min, redko) ali taksi (okoli 20 min); ob koncu poti se vrnite z istim avtobusom, vozni red preverite.",
            "Zelena linija ali taksi (okoli 15 min) na severno obalo, kjer je koridor.",
            "Zelena ali modra linija (okoli 20–25 min); muzej je blizu severne obale. Odprto približno do 16.30, preverite pred odhodom.",
        ],
        "taxi": "Taksiji stojijo pred postajo; avtomobil lahko naročite tudi prek nastanitve. Vožnja do severne obale je okoli 1.500–2.500 jenov, do Chureita okoli 3.000–4.000. Zvečer in v megli je to varnejše in hitrejše od čakanja na avtobus.",
        "links": [("🚌 Fujikyu — avtobusi in vozovnice", FUJIKYU), ("🚌 Highway Bus — rezervacija Shinjuku → Kawaguchiko", HIGHWAYBUS),
                  ("🧭 Kawaguchiko → Chureito (Google)", gdir("Kawaguchiko Station", "Chureito Pagoda"))],
        "tips": ["Fuji je pogosto v oblakih do poldneva — razgled iščite zjutraj ali ob sončnem zahodu.",
                 "Za Chureito se obujte v udobne čevlje (stopnice) in pojdite zgodaj zjutraj."],
    },
    # ------------------------------------------------------------------ MINOBUSAN
    "minobusan": {
        "from": "Kakurinbo, Minobu", "from_label": "šukubo Kakurinbo",
        "arrive": ("Kawaguchiko Station, Yamanashi", "Minobu Station, Yamanashi",
                   "Iz Kawaguchika z avtobusom/vlakom do Fujija ali Kofuja in nato z JR Minobu Line do postaje Minobu (okoli 2–2,5 ure skupaj). Od postaje Minobu do templja Kuon-ji je okoli 15 minut z avtobusom ali taksijem."),
        "intro": "Minobu je majhno romarsko mestece in je za vas vezano na nastanitev v Kakurinbu — tempeljska vrata in jutranja molitev so peš. Največja zagata je prihod in odhod: avtobusi so redki, zato se dogovorite z nastanitvijo vnaprej.",
        "options": [
            ("🚌", "Avtobus s postaje Minobu", "Avtobus do Kuon-ji vozi približno ob prihodih vlakov, a ne pogosto; vozovnica je okoli 300–400 jenov. Zadnji avtobus preverite pred prihodom."),
            ("🚕", "Taksi", "Taksi s postaje Minobu do Kuon-ji je po objavljenih podatkih okoli 1.500–2.500 jenov (okoli 10–15 min). Na postaji jih ni vedno — naročite ga vnaprej (nastanitev ali taksi podjetje)."),
            ("🚠", "Vzpenjača", "Vzpenjača Minobusan Ropeway pelje s templja na vrh; cena je okoli 1.000 jenov v obe smeri (preverite). Ob vetru je lahko zaprta."),
            ("🚶", "Peš", "Tempeljski kompleks, vrata Sanmon in stari del so peš. Kamnita stopnica do glavne dvorane je dolga — računajte okoli 15–20 min počasne hoje."),
        ],
        "sights": [
            "Peš iz šukubo Kakurinbo, okoli 5–10 min.",
            "Spodnja postaja žičnice je ob templju (okoli 5 min peš); vožnja traja okoli 7 min.",
            "Velika vrata so na začetku tempeljske ceste, okoli 10 min od Kakurinba; za fotografijo pojdite zjutraj, ko je še tiho.",
            "Jutranja molitev je v tempeljski dvorani, pred zoro — nastanitev vas bo opozorila na uro. Peš.",
            "Staro mestece je prav pod templjem; hodite po tempeljski cesti navzdol, okoli 10–15 min.",
        ],
        "taxi": "Taksi iz Minobuja je omejen. Prosite Kakurinbo, da vam ob prihodu/odhodu pokliče taksi ali pove, ali ponujajo prevoz s postaje; ceno vprašajte pred vožnjo.",
        "links": [("🧭 Pot Kawaguchiko → Minobu (Google)", gdir("Kawaguchiko Station", "Minobu Station")), ("🔎 Tempelj Kuon-ji — uradna stran", "https://www.kuonji.jp/")],
        "tips": ["Prihod načrtujte pred temo; avtobusov zvečer ni.", "Za kovčke dogovorite v šukubo, ali jih lahko pustite do odhoda."],
    },
    # ------------------------------------------------------------------ KUMANO
    "kumano": {
        "from": "Hongu Taisha-mae, Tanabe, Wakayama", "from_label": "Hongu / Yunomine",
        "arrive": ("Mishima Station, Shizuoka", "Kii-Katsuura Station, Wakayama",
                   "Dolga vožnja: shinkansen do Nagoje in nato ekspres »Nanki« do Kii-Katsuure (skupaj okoli 6–7 ur). Od tam avtobus ali vlak do Nachi in nato prek Hongu. Pot si razdelite na dva dela in kupite vozovnice vnaprej (Smart EX za shinkansen)."),
        "intro": "Kumano Kodo je območje z redkimi avtobusi; na Yunomine in Kawayu se pride z avtobusom ali taksijem. Zaradi tega je najpomembnejša priprava urnik avtobusov in dogovori z nastanitvijo (prevoz s postaje, prtljaga, bento).",
        "options": [
            ("🚌", "Avtobusi Meiko in Ryujin", "Glavne povezave: Kii-Tanabe ↔ Hongu (okoli 2 uri), Hongu ↔ Yunomine/Kawayu (10–15 min), Shingu ↔ Hongu (okoli 1 h 15 min). Vozni red je omejen (nekaj vožnj na dan); preverite jih na dan prej. Cene so odvisne od razdalje; za Tanabe–Hongu okoli 2.000 jenov."),
            ("🚆", "JR Kisei Line", "Vlak Nanki Express (in lokalni vlaki) povezujejo Kii-Katsuuro in Shingu. Za Nachi je od postaje Kii-Katsuura še avtobus."),
            ("🧳", "Prevoz prtljage", "Turistični urad Tanabe (Kumano Travel) organizira prevoz prtljage med nastanitvami (»takuhaibin«); za pešačenje po Kodo je to najboljši prihranek."),
            ("🚕", "Taksi", "Taksi na območju je dražji in ga je treba naročiti vnaprej; nastanitev ga običajno uredi. Za slap Nachi, Daimonzaka in Hongu so točke pogosto dosegljive z avtobusom."),
        ],
        "sights": [
            "Od postaje Kii-Katsuura avtobus do Nachisan (okoli 30–35 min, okoli 700 jenov); pagoda je tik ob svetišču.",
            "Avtobus Kii-Katsuura → Nachi-no-taki-mae (okoli 25 min); slap je 2 min hoje od postaje.",
            "Daimonzaka: avtobus do postaje Daimonzaka (okoli 20 min iz Kii-Katsuure) in nato okoli 40 min hoje po kamniti poti do Nachija. Čevlji z dobrim oprijemom.",
            "Hongu Taisha: avtobus do postaje Hongu Taisha-mae; Oyunohara je okoli 10 min peš od svetišča (vsa pot je ravna).",
            "Yunomine: avtobus Hongu → Yunomine Onsen (okoli 10 min); Tsuboyu je v vasi, vstopnina okoli 800 jenov, 30 minut (rezervirajte pri blagajni).",
            "Ladjica po reki Kumano (Kawabune) vozi iz Hongu proti Shinguju: rezervirajte prek Kumano Travel (običajno več tisoč jenov, ura odhoda je odvisna od vode).",
            "Doro-kyo je oddaljen — avtobus Nara Kotsu iz Shingu ali taksi; težko dostopno s samo javnim prevozom: rezervirajte skupaj z nastanitvijo ali tur z lokalnim taksijem.",
            "Kawayu Onsen: avtobus Hongu → Kawayu (okoli 10–15 min). Sennin-buro (rečna kopel) je odprta le pozimi (običajno od decembra), preverite.",
        ],
        "taxi": "Taksiji so redki; v krajih se pogosto naroči prek nastanitve ali turističnega urada. Računajte okoli 700–800 jenov za prvih 2 km in nato po števcu; od Hongu do Yunomine približno 1.500–2.000 jenov.",
        "links": [("🥾 Kumano Travel — prevoz, prtljaga, rezervacije", KUMANO), ("🚌 Meiko Bus — vozni redi", MEIKO),
                  ("🧭 Kii-Katsuura → Nachisan (Google)", gdir("Kii-Katsuura Station", "Kumano Nachi Taisha"))],
        "tips": ["Preden greste, vprašajte nastanitev za zadnji avtobus ter ali nudijo prevoz s postaje.", "Kumano Kodo je lahko dolgo mokro — dobri čevlji in pelerina."],
    },
    # ------------------------------------------------------------------ KOYASAN
    "koyasan": {
        "from": "Senjuguchi, Koyasan, Wakayama", "from_label": "glavna ulica Koyasan",
        "arrive": ("Namba Station, Osaka", "Koyasan Station, Wakayama",
                   "Nankai iz Namb do Gokurakubashija (ekspres »Koya«, okoli 1 h 15 min–1 h 30 min), nato žičnica do Koya-sana (5 min) in avtobus do mesta. Za turiste je ugodna »Koyasan World Heritage Ticket« (vlak + žičnica + neomejeni avtobusi na gori); po objavljenih podatkih je okoli 3.500–4.500 jenov. Preverite aktualno ceno."),
        "intro": "Koyasan je mesto na gori, dolgo okoli 3 km. Glavna ulica poteka med Senjuguchijem in Daimonom, tempeljski kompleks Garan in Kongobu-ji sta blizu, Okunoin pa je 20–30 minut hoje ali nekaj postaj z avtobusom. Prevoz po gori so krajše vožnje z avtobusom.",
        "options": [
            ("🚌", "Avtobusi po gori", "Avtobusi Nankai Rinkan vozijo po glavni ulici in do Okunoina. Vozovnica je okoli 200–500 jenov po razdalji; dnevna vozovnica ali kombinirana vozovnica za turiste se splača, če greste več kot 3–4×. Zadnji avtobus vozi zgodaj zvečer."),
            ("🚠", "Žičnica", "Žičnica Gokurakubashi ↔ Koyasan traja okoli 5 minut in je vključena v vozovnico Nankai; v nasprotnem primeru je okoli 500 jenov."),
            ("🚶", "Peš", "Mesto je ravno: Garan, Kongobu-ji, Reihokan in glavna ulica so peš (10–20 min). Okunoin prehodite po poti ob pokopališču (okoli 2 km)."),
            ("🚕", "Taksi", "Taksijev je malo; stojijo ob postaji in v središču. Za zadnjo vožnjo ali prtljago jih vprašajte vnaprej."),
        ],
        "sights": [
            "Peš po glavni ulici do vhoda Ichinohashi in nato 2 km po poti med cedrami (okoli 30–40 min), ali avtobus do postaje Okunoin-mae (okoli 10 min) in 20 min hoje do mavzoleja.",
            "Peš iz središča okoli 10–15 min; avtobusna postaja Garan-mae.",
            "Kongobu-ji je ob glavni ulici (okoli 10 min peš od Senjuguchija); vstopnina okoli 1.000 jenov.",
            "Ostale nastanitve: poiščite v središču ali v dolini; šukubo so ob glavni ulici — peš do vsega.",
            "Večerni sprehod z menihom: zbirališče je v Ekoinu (blizu Okunoina), peš ali avtobus; običajno ob 20.00, preverite.",
            "Mavzolej je okoli 10 min peš vzhodno od središča.",
            "Reihokan je nasproti Garana, okoli 10 min peš.",
            "Daishi Kyokai je ob Garanu in Kongobu-ji, okoli 10 min peš.",
        ],
        "taxi": "Taksi iz postaje Koyasan do mesta je okoli 1.000–2.000 jenov; stojijo pri postaji in včasih pred tempeljskimi vrati. Naročilo prek nastanitve je najzanesljivejše.",
        "links": [("⛩️ Koyasan Tourist Association — dostop, avtobusi, dogodki", KOYASAN),
                  ("🔎 Koyasan World Heritage Ticket (iskanje)", gsearch("Koyasan World Heritage Ticket Nankai")),
                  ("🧭 Namba → Koyasan (Google)", gdir("Namba Station", "Koyasan Station"))],
        "tips": ["Zadnji avtobus preverite po zadnjem obisku Okunoina — zvečer je mesto zelo tiho.",
                 "Oblecite se v plasti: na gori je novembra občutno hladneje kot v Osaki."],
    },
    # ------------------------------------------------------------------ IYA
    "iya": {
        "from": "Oboke Station, Miyoshi, Tokushima", "from_label": "postaja Oboke",
        "arrive": ("Okayama Station", "Oboke Station, Miyoshi, Tokushima",
                   "Iz Okayame z ekspresom »Nanpu« po liniji Dosan do Oboke (okoli 1 h 45 min–2 h), od tam taksi/shuttle nastanitve. Dan prej preverite zadnji prevoz do hotela."),
        "intro": "Dolina Iya je odmaknjena: javnih avtobusov je malo in redki, zato je prevoz najdražji del tega kraja. Zato združite nastanitev s prevozom (shuttle), zjutraj dogovorite turistični taksi in računajte, da za oddaljene točke (Oku-Iya, Tsurugi) potrebujete cel dan.",
        "options": [
            ("🚕", "Taksi in shuttle", "Najzanesljivejši je shuttle nastanitve (vprašajte pri rezervaciji) ali taksi s postaje Oboke. Taksi do Kazurabashija je po objavljenih podatkih več tisoč jenov, do Oku-Iya pa precej več; za štiri osebe se strošek deli."),
            ("🚌", "Avtobusi", "Lokalni avtobusi vozijo po dolini redko (nekaj voženj na dan); v nekaterih smereh le ob delavnikih. Preverite jih pri turističnem uradu Miyoshi ali nastanitvi."),
            ("🚆", "JR Dosan Line", "Vlak ustavi na Oboke in Awa-Ikeda; do Kazurabashija je od tam še prevoz."),
            ("⛴️", "Ladjica po soteski Oboke", "Ladjica vozi ob postaji Oboke (okoli 30 min); cena je okoli 1.500 jenov, odpre se po vremenu."),
        ],
        "sights": [
            "Od postaje Oboke ali Awa-Ikeda s taksijem (okoli 30–40 min); vstopnina za most okoli 550 jenov. Z avtobusom le ob redkih odhodih.",
            "Pristanišče je v bližini postaje Oboke (okoli 10 min peš ali kratka vožnja s taksijem).",
            "Hotel Iya Onsen: hotelski vlak ob vzponu do kopeli ob reki je za goste. Od postaje Oboke je to okoli 30 min vožnje; prosite za shuttle.",
            "Hi-no-Ji in kipec dečka: vožnja po dolini okoli 40 min od Oboke; običajno v turističnem najemu skupaj z Ochiai.",
            "Ochiai: razgledišče nad vasjo, okoli 1 h iz Oboke z avtomobilom/taksijem; priporočeno z vodičem ali turističnim taksijem.",
            "Oku-Iya je najbolj oddaljen cilj (več kot 1 h od Oboke z avtom); samo taksi ali organiziran prevoz.",
            "Žičnica na Tsurugi je okoli 40–50 min z avtom od Oboke; samo taksi ali prevoz nastanitve.",
            "Lapis Oboke je prav ob postaji Oboke — odlično za čakanje na vlak, kopel za noge in prigrizek.",
        ],
        "taxi": "Taksi v dolini Iya je običajno treba naročiti vnaprej (nastanitev ali taksi iz Oboke). Dogovorite fiksno ceno za celo dolino: za poldnevni najem računajte okoli 15.000–25.000 jenov za skupino — štiri osebe si ga delijo.",
        "links": [("♨️ Hotel Iya Onsen — uradna stran (shuttle, rezervacija)", IYA_ONSEN), ("🏔️ Shikoku — turistične informacije", SHIKOKU),
                  ("🧭 Pot Okayama → Oboke (Google)", gdir("Okayama Station", "Oboke Station"))],
        "tips": ["Ne računajte na improviziran prevoz — vse dogovorite dan prej.", "Pred odhodom v oddaljeno dolino imejte nekaj gotovine."],
    },
    # ------------------------------------------------------------------ INE
    "ine": {
        "from": "Ine Bay, Kyoto", "from_label": "zaliv Ine (funaye)",
        "arrive": ("Amanohashidate Station, Miyazu, Kyoto", "Ine Bay Sightseeing Boat, Ine, Kyoto",
                   "Iz Kyota ali Osake z ekspresom »Hashidate« do Amanohashidateja (okoli 2–2,5 ure), nato avtobus Tango Kairiku do Ine (okoli 40 min, vozi redko). Zadnji avtobus preverite pred odhodom."),
        "intro": "Ine je ribiška vasica ob zalivu z eno glavno cesto: hodite peš ob funayah, čez zaliv pa ladjica. Za dan v Amanohashidate in nazaj računajte na avtobuse (redki) ali taksi; dobro načrtujte zadnji avtobus nazaj.",
        "options": [
            ("🚌", "Avtobus Amanohashidate ↔ Ine", "Vozi nekaj voženj na dan (okoli 40–50 min); vozovnica je po objavljenih podatkih okoli 700–900 jenov. Zadnji avtobus je zgodnji večer — preverite, preden greste."),
            ("⛴️", "Ladjica po zalivu", "Ine-wan Meguri traja okoli 25 minut; cena je okoli 1.000 jenov. Odhodi so ob ladijskem pristanišču."),
            ("🚲", "Kolo ali e-kolo", "V Ine in Amanohashidateju izposojajo kolesa; v Amanohashidateju so kolesa ob sipini dovoljena."),
            ("🚕", "Taksi", "Taksi v Ine je treba naročiti; iz Amanohashidateja je okoli 6.000–9.000 jenov (okoli 30–40 min)."),
        ],
        "sights": [
            "Pristanišče je v vasi (okoli 10–20 min peš od večine nastanitev). Odhodi so po urniku.",
            "Park Funaya no Sato je na vzhodni strani zaliva; peš ali kolo, okoli 15–25 min iz vasi.",
            "INE CAFE je v vasi, peš od večine nastanitev (okoli 10 min).",
            "Mukai Shuzo je ob cesti v vasi Hirata; peš okoli 15 min iz središča.",
            "Amanohashidate z avtobusom (okoli 40 min) do postaje Amanohashidate; Chion-ji je 5 min peš od postaje. Sipino prehodite ali prekolesarite (okoli 3,6 km).",
            "Kasamatsu Park je na drugi strani: žičnica/vlečnica ali ladjica prek ožine, nato razgledna terasa; vprašajte v informacijah.",
            "Nariai-ji je na hribu; avtobus je redek — taksi iz Amanohashidateja (okoli 30–40 min). Zvečer osvetljeno.",
            "Chie no Yu je ob postaji Amanohashidate, 5 min peš; odličen zaključek pred odhodom.",
        ],
        "taxi": "Taksi iz Ine je skoraj samo po naročilu. Prosite nastanitev, da ga pokliče, ali pokličite iz Amanohashidateja; vprašajte za ceno vnaprej in omejitev poti.",
        "links": [("🏘️ Ine — turistične informacije", INE_KANKO), ("🧭 Amanohashidate → Ine (Google)", gdir("Amanohashidate Station", "Ine Bay, Kyoto")),
                  ("🚌 Kyoto Tango — avtobus (iskanje)", gsearch("Tango Kairiku bus Amanohashidate Ine timetable"))],
        "tips": ["Vozni red avtobusa si zapišite ali posnemite zaslon — signal je lahko slab.", "V funayi so večerje ob fiksni uri, pridite pravočasno."],
    },
    # ------------------------------------------------------------------ KYOTO
    "kyoto": {
        "from": "Kyoto Station", "from_label": "postaja Kyoto (nastanitev ob postaji)",
        "arrive": ("Amanohashidate Station", "Kyoto Station",
                   "Iz Ine z avtobusom do Amanohashidateja in nato z ekspresom »Hashidate« do Kyota (okoli 2–2,5 ure). Prtljago po potrebi pošljite naprej z Yamato."),
        "intro": "Kyoto je velik in avtobusi so novembra zelo polni. Postaja Kyoto je odlično izhodišče: JR vodi do Arashiyame, Tofuku-ja in Nare, metro do središča, avtobusi do vzhodnih templjev. Za štiri osebe je taksi pogosto pametna izbira.",
        "options": [
            ("🚌", "Mestni avtobusi", "Enotna cena okoli 230 jenov za vožnjo; plačate s kartico ICOCA/Suica ali gotovino pri izstopu. Novembra so zelo polni — za Higashiyamo in Ginkaku-ji računajte na 45–60 min."),
            ("🚇", "Podzemna železnica", "Dve liniji (Karasuma in Tozai); vožnja okoli 220–360 jenov. Hitrejše od avtobusa do Keage, Nijo, Imperial Palace."),
            ("🚆", "JR in zasebne proge", "JR Sagano Line do Arashiyame (okoli 15 min, 240 jenov), JR Nara do Tofuku-ji (5 min), Keihan do Gion-Shijo, Hankyu do Kawaramachi."),
            ("🎫", "Dnevne vozovnice", "Kombinirane dnevne vozovnice za avtobus in podzemno so se v zadnjih letih spreminjale; preverite aktualno ponudbo v spodnji povezavi in primerjajte s ceno posameznih vožnj."),
            ("🚕", "Taksi", "Krajše vožnje v središču stanejo okoli 1.000–2.000 jenov, začetna cena je po objavljenih podatkih okoli 600–700 jenov. Za štiri osebe pogosto ceneje in hitreje kot avtobus."),
        ],
        "sights": [
            "Metro Karasuma do Karasuma Oike, nato Tozai do Keage in okoli 15 min peš do templja; ali avtobus 5 do postaje Nanzenji-Eikando-michi (okoli 30–40 min).",
            "JR Sagano Line do postaje Saga-Arashiyama (okoli 15 min, 240 jenov); Tenryu-ji je 5 min peš. Bambusov gozd tik zraven, zjutraj je najmirneje.",
            "Avtobus 5/17/100 do postaje Ginkakuji-michi (okoli 35–45 min) ali metro in nato avtobus; zaključek pri Filozofski poti je peš do Nanzenjija (okoli 30 min).",
            "Avtobus 50 ali 59 iz postaje Kyoto (okoli 40–45 min), ali taksi (okoli 25–30 min, okoli 3.000–4.000 jenov).",
            "JR Nara Line do postaje Tofukuji (1 postaja, okoli 3–5 min, 150 jenov), nato okoli 10 min peš; ali Keihan do Tofukuji.",
            "Gion: avtobus 206 ali metro/Keihan do Gion-Shijo (okoli 15–25 min). Gion Kaikan je v četrti Gion; zvečer pridite z vlakom/taksijem.",
            "Čajna ceremonija Camellia je v Ninenzaka (Higashiyama): avtobus do Kiyomizu-michi in okoli 10 min po strmi poti, ali taksi (rezervacija je obvezna; ura prihoda točna).",
            "Okochi Sanso je v Arashiyami, okoli 10 min peš od bambusovega gozda; pojdite v isti dan kot Tenryu-ji.",
        ],
        "taxi": "Taksi v Kyotu je dobra izbira za štiri osebe, zlasti za Ryoan-ji, Ginkaku-ji ali pozne večerje. Naročite prek aplikacije GO ali pred hotelom; MK Taxi in Yasaka so večja podjetja. Ob prometnih konicah novembra čakanje ni redko.",
        "links": [("🚌 Kyoto City Bus in podzemna — vozni redi in vozovnice", KYOTO_BUS), ("🍁 Kyoto Travel — osvetlitve, prevoz, nasveti", KYOTO_TRAVEL),
                  ("🚄 Smart EX — shinkansen", SMART_EX), ("🧭 Kyoto → Arashiyama (Google)", gdir("Kyoto Station", "Saga-Arashiyama Station")),
                  ("🧳 Yamato — kovčki naprej", YAMATO), ("🚕 GO — taksi", GO_TAXI)],
        "tips": ["Avtobusi novembra: pojdite zgodaj zjutraj ali izberite vlak/metro.", "Zadnji avtobusi iz severnih templjev (Ryoan-ji, Ginkaku-ji) odpeljejo zgodaj zvečer — za pot nazaj imejte rezervo ali taksi."],
    },
    # ------------------------------------------------------------------ OSAKA
    "osaka": {
        "from": "Namba Station, Osaka", "from_label": "postaja Namba",
        "arrive": ("Kyoto Station", "Namba Station, Osaka",
                   "Iz Kyota z JR »Special Rapid« do Osake (okoli 30 min), nato metro Midosuji do Namb (okoli 15 min). Shinkansen do Shin-Osake je hitrejši, a s prestopom ni bistveno. Prtljago lahko pošljete naprej z Yamato."),
        "intro": "Osaka ima gost javni prevoz in je cenejša od Kyota. Namba je odlično izhodišče: Dotonbori je 5–10 min peš, metro Midosuji pelje v Umedo in Shin-Osako, Nankai do letališča Kansai pa gre prav iz Namb.",
        "options": [
            ("🚇", "Osaka Metro", "Vožnje stanejo okoli 180–380 jenov po razdalji; ICOCA/Suica velja. Dnevna vozovnica za metro (npr. »Enjoy Eco Card«) je po objavljenih podatkih okoli 800 jenov čez teden in ceneje ob koncih tedna; preverite aktualno ceno."),
            ("🎫", "Osaka Amazing Pass", "Prevoz po metroju in avtobusih ter vstopnine v številne znamenitosti (npr. Umeda Sky Building); 1-dnevna je po objavljenih podatkih okoli 2.800–3.500 jenov. Splača se, če načrtujete 3+ vstopnine."),
            ("🚆", "JR in Nankai", "JR Loop Line obkroža središče; Nankai vozi iz Nambe do letališča Kansai (Rapi:t, okoli 40 min). Cena Rapi:ta je po objavljenih podatkih okoli 1.500 jenov z doplačilom za sedež."),
            ("🚕", "Taksi", "Krajše vožnje v središču Osake stanejo okoli 800–1.500 jenov; zvečer ceneje kot več prestopov. Naročilo prek GO ali pred postajo."),
        ],
        "sights": [
            "Metro Tanimachi ali Chuo do postaje Tanimachi 4-chome (okoli 15 min), nato 10 min peš do vrta Nishinomaru in gradu.",
            "Peš iz Namb okoli 5–10 min; ladjica Tombori vozi iz pristanišča ob mostu Ebisu.",
            "Kuromon je okoli 8 min peš od Namb ali 5 min od postaje Nipponbashi (Sennichimae).",
            "Metro Tanimachi do Shitennoji-mae Yuhigaoka (okoli 15 min); vhod v tempelj je 5 min peš.",
            "Keitakuen je v parku Tennoji; metro Midosuji Namba → Tennoji (okoli 10 min) in nato 5 min peš do vrta.",
            "Midosuji do Umede (okoli 10 min), nato okoli 10–15 min peš po podhodu do stolpnice; zvečer je razgled najlepši.",
            "Shinsekai: peš ali metro do postaje Ebisucho (6 min) ali Dobutsuen-mae; Tsutenkaku je v središču.",
            "Muzej bivanja: metro Sakaisuji do Tenjimbashisuji-rokuchome (okoli 15 min iz Namb), muzej je v istem poslopju.",
        ],
        "taxi": "Taksi v Osaki je poceni v primerjavi s Tokiem; krajša vožnja stane okoli 1.000–1.800 jenov. Naročite prek GO ali na postajališču. Dan pred odhodom na letališče si pripravite načrt (Rapi:t).",
        "links": [("🚇 Osaka Metro — vozovnice in proge", OSAKA_METRO), ("🎫 Osaka Amazing Pass (iskanje)", gsearch("Osaka Amazing Pass 1 day 2 day"))
                  , ("🌐 Osaka Info — prevoz in dogodki", OSAKA_INFO), ("🛫 Pot Namba → Kansai letališče (Google)", gdir("Namba Station", "Kansai International Airport")),
                  ("🧳 Yamato — kovčki na letališče", YAMATO), ("🚕 GO — taksi", GO_TAXI)],
        "tips": ["2. 12. načrtujte odhod na letališče vsaj 3 ure pred poletom (Rapi:t vozi na 30 min).",
                 "Pralni stroj v apartmaju + kovčki: pošljite jih na letališče z Yamato, če imate čas."],
    },
    # ------------------------------------------------------------------ NARA
    "nara": {
        "from": "Kintetsu Nara Station", "from_label": "postaja Kintetsu Nara",
        "arrive": ("Namba Station, Osaka", "Kintetsu Nara Station",
                   "Iz Osake (Namba/Kintetsu) z linijo Kintetsu Nara v okoli 40 minutah; iz Kyota z JR Miyakoji Rapid (okoli 45 min) ali Kintetsu (okoli 35–45 min). Cena je po objavljenih podatkih okoli 600–800 jenov."),
        "intro": "Nara je majhna in večino znamenitosti obiščete peš. Postaja Kintetsu Nara je ob parku; JR Nara je nekoliko dlje. Za ostale točke (Isuien, Nigatsu-do) je 10–25 minut hoje.",
        "options": [
            ("🚶", "Peš", "Vse znamenitosti so v krogu okoli 1,5 km: park, Todai-ji, Kasuga Taisha, Kofuku-ji. Vstopnine so ločene."),
            ("🚌", "Avtobusi Nara Kotsu", "Krožne linije povezujejo postaji JR/Kintetsu s parkom in Kasuga Taisha. Vožnja je po objavljenih podatkih okoli 220–250 jenov; plačate s kartico IC."),
            ("🚕", "Taksi", "Krajše vožnje od postaje do Todai-ji ali Kasuga stanejo okoli 1.000–1.500 jenov. Za štiri osebe je to enakovredno avtobusu."),
            ("🚲", "Kolo", "Izposoja koles pri postaji; po parku je kolo praktično, a ne med jeleni."),
        ],
        "sights": [
            "Peš iz Kintetsu Nara okoli 20–25 min, ali avtobus do Todaiji Daibutsuden.",
            "Park je tik ob Kintetsu Nara (5 min); jeleni se pasejo povsod. Pokupite si »shika senbei«.",
            "Kasuga Taisha je v gozdu na vzhodu parka (okoli 30 min peš od postaje ali avtobus).",
            "Isuien je 15 min peš od postaje, ob Todai-ji; vstopnina okoli 1.000–1.200 jenov.",
            "Nigatsu-do je na hribu nad Todai-ji (okoli 10 min peš od Todai-ji), zvečer osvetljen.",
            "Kofuku-ji je 3–5 min peš od Kintetsu Nara; pagoda je simbol mesta.",
        ],
        "taxi": "Taksi stoji pred postajama Kintetsu in JR. Za štiri osebe je to ugodno za pot do Kasuga Taisha ali nazaj na postajo po dolgem dnevu.",
        "links": [("🚆 Kintetsu — vozovnice in proge", KINTETSU), ("🧭 Osaka → Nara (Google)", gdir("Namba Station", "Kintetsu Nara Station"))],
        "tips": ["Jelenom ne dajajte hrane razen »senbei« iz stojnic; zaščitite torbe.", "Kovčke pustite v omarici na postaji Osaka/Namba."],
    },
    # ------------------------------------------------------------------ HIROSHIMA
    "hiroshima": {
        "from": "Hiroshima Station", "from_label": "postaja Hiroshima",
        "arrive": ("Shin-Osaka Station", "Hiroshima Station",
                   "Shinkansen »Nozomi« ali »Sakura« iz Shin-Osake do Hirošime traja okoli 1 h 25 min–1 h 35 min; enosmerna rezervirana vozovnica je po objavljenih podatkih okoli 10.000–11.000 jenov. Kupite jo prek Smart EX (QR vstop). Iz Namb do Shin-Osake je 15 min z metrojem."),
        "intro": "Hirošima ima lepo tramvajsko mrežo: s postaje Hiroshima do Peace Parka je okoli 15–20 minut. Miyajima je dodaten polovičen dan: vlak do Miyajimaguchija in ladjica. Dan načrtujte tako, da se vrnete pred zadnjim shinkansenom.",
        "options": [
            ("🚋", "Tramvaj Hiroden", "Enotna cena okoli 220 jenov za mestne proge; do Miyajima-guchi je okoli 330 jenov in 60–70 min. Plačate s kartico IC ali gotovino pri izstopu."),
            ("🚆", "JR Sanyo Line do Miyajimaguchija", "Vlak je hitrejši (okoli 25–30 min); nato ladjica (okoli 10 min). Obe ladji, JR in Matsudai, vozita pogosto."),
            ("🎫", "Miyajima – ladjica in taksa", "Ladjica JR do Miyajime je po objavljenih podatkih okoli 200 jenov; od oktobra 2023 se plača tudi turistična taksa za obisk otoka (100 jenov)."),
            ("🚕", "Taksi", "V Hirošimi je taksi ugoden za večje točke (Shukkeien, Muzej miru). Naročilo prek GO ali na postajališču."),
        ],
        "sights": [
            "Tramvaj št. 2 ali 6 od postaje Hiroshima do postaje Genbaku-Dome-mae (okoli 15–20 min, 220 jenov), nato 3 min do parka; park je ob muzeju.",
            "Muzej je v parku; od postaje Genbaku-Dome-mae je okoli 15 min peš, ali tramvaj do Hiroshima Peace Park.",
            "Kupola je ob postaji Genbaku-Dome-mae, 1 min peš od tramvaja.",
            "JR do Miyajimaguchija (okoli 25–30 min), nato ladjica (okoli 10 min) in od pristanišča okoli 10 min peš do torija.",
            "Dolina Momijidani je na Miyajimi; peš okoli 15–20 min od pristanišča ali shuttle. Jesenski barvni vrh je okoli sredine novembra do začetka decembra.",
            "Shukkeien je 10 min peš ali 5 min s tramvajem od postaje Hiroshima; vstopnina okoli 300 jenov (otroci manj).",
        ],
        "taxi": "Taksi pred postajo Hiroshima do Peace Parka stane okoli 1.500–2.000 jenov. Na Miyajimi ni taksijev, razen redkih; ostanite pri peš.",
        "links": [("🚄 Smart EX — shinkansen Osaka ↔ Hiroshima", SMART_EX), ("⛴️ Feri na Miyajimo (JR)", MIYAJIMA_FERRY),
                  ("🚋 Hiroden — tramvaj", HIRODEN), ("🌐 Hiroshima — turistične informacije", HIROSHIMA_NAVI)],
        "tips": ["Izlet Osaka–Hiroshima: odhod okoli 8.00, povratek pred 20.00; shinkansen izberite vnaprej.", "Ob plimi je torija v vodi, ob oseki lahko pridete bliže — preverite urnik plime."],
    },
}
