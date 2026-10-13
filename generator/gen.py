#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator strani 'Japonska 2026 — Naše potovanje'.
Iz podatkov spodaj ustvari index.html + 9 podstrani lokacij.
Videe bere iz videos.json (če obstaja) v isti mapi kot ta skripta."""

import json
import os
import re
import html
import urllib.parse

import art
import links as L
import data_jp as JP

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
SITE_DIR = os.path.join(REPO, "site")
ASSETS_DIR = os.path.join(HERE, "assets")

# Nastavitve potovanja (za drugo potovanje jih prepiše gen_<potovanje>.py)
CFG = {
    "id": "japonska",
    "slug": "jp-xyna9tg2e",
    "title": "Japonska — Mesec za dušo",
    "short": "Mesec za dušo",
    "brand": "🍁 Mesec za dušo",
    "theme": "#7b2230",
    "desc": "Potovalni vodnik: Japonska, 3. november – 2. december 2026, Tokio → Osaka.",
    "people": ["Marjetica", "Helena", "Ljuba", "Magda"],
    # kontekst zemljevidov: pogled »država« (središče, povečava) in največja oddaljenost točk od postaje (km)
    "country": {"name": "Japonska", "c": [37.9, 137.6], "z": 5},
    "geo_radius_km": 60,
}

# Besedila, ki se razlikujejo po potovanju
TXT = {
    "loc_title": "{name} · Japonska 2026",
    "loc_desc": "{name}: znamenitosti, hrana in nasveti — vodnik Japonska 2026.",
    "magda": "💛 Magdin trenutek",
    "diary": "📖 Magdin dnevnik",
    "diary_hint": "Prostor za vaše vtise, skice in najlepši spomin s te postaje.",
    "nalozi_title": "Naloži fotografije · Japonska — Mesec za dušo",
    "izziv_title": "Foto izzivi · Japonska — Mesec za dušo",
    "izziv_hero": ("Skupaj gradimo album", "Foto izzivi", "Za Marjetico, Heleno, Ljubo in Magdo"),
    "izziv_idea": ("Mesec dni bo minil hitro. Zato za vsako postajo ujamete nekaj slik — ne le razglednic, ampak "
                   "<strong>vas na teh krajih</strong>: skupaj, v tišini, ob hrani, med smehom. Iz teh slik in tega načrta "
                   "bo po vrnitvi nastala <strong>vaša potopisna knjiga</strong>."),
    "izziv_final": ("Zadnje presenečenje: izberite <strong>najljubšo sliko vsake postaje</strong> in jo uvrstite v potopisno "
                    "knjigo — prva slika (Meiji Jingu) in zadnja (Miyajima) bosta ob straneh, vmes pa vaš mesec Japonske. "
                    "Z gumbom »Prenesi vse slike« na strani Naloži dobite cel album z enim klikom."),
    "izziv_final_title": "🏆 Vse izzive ste opravile!",
    "nalozi_note": "Izberite postajo in naložite slike ali videe. Vse pristane v spodnjem skupnem albumu.",
    "nalozi_hero": ("📤", "Vaše fotografije in videi", "Naloži fotografije",
                    "Izberite postajo in naložite slike ali videe kar s telefona"),
    "izziv_how": [
        ("Izberi izziv", "pri vsaki postaji jih je nekaj. Odpri postajo in poglej, kaj te čaka."),
        ("Naloži fotografijo ali video", "kar s telefona. Prvič te vprašamo le, kdo nalaga."),
        ("Odkleni presenečenje", "zanimivost, skrivnost ali nagrada. Opravljeni izziv pade na dno in pokaže sličico."),
    ],
    "nacrt_title": "Načrt poti — Japonska, Mesec za dušo",
    "nacrt_desc": "30-dnevni načrt poti po Japonski: dan za dnem in prehodi med kraji, 3. 11.–2. 12. 2026.",
    "nacrt_hero": ("🗺️", "Hrbtenica potovanja", "Načrt poti — 30 dni", "Dan za dnem, od Tokia do Osake", "nacrt"),
    "kako_title": "Kako uporabljati · Japonska — Mesec za dušo",
    "izziv_why": "Zakaj to počnemo?",
    "izzivi_intro": ("Naložite fotografijo (ali video) za izziv — takoj se označi kot opravljen in se spodaj pokaže sličica. "
                     "Iz tega nastane vaš skupni album."),
    "izziv_fine": ("Drobni tisk: vsak izziv ima pod seboj »drobni tisk« — zakaj se slikate prav tam in kaj je ta kraj. "
                   "Presenečenja so zanimivosti, legende in majhne nagrade (nobenih izmišljenih kuponov — le pravi predlogi in kraji)."),
    "izziv_intro_desc": "Vsi foto izzivi potovanja — naložite sliko in izziv je opravljen.",
    "album_title": "📸 Naš album",
    "izziv_jump": "📸 Poglej foto izzive",
    "izziv_stations_note": "Odpri vodnik za to postajo →",
}

OUT = os.path.join(SITE_DIR, CFG["slug"])

# Verzija gradnje — doda se v naslov CSS/JS (?v=BUILD), da brskalnik vedno
# naloži svežo različico. Ob vsaki spremembi povečaj.
BUILD = "19"

# ----------------------------------------------------------------------------
# VSEBINA
# ----------------------------------------------------------------------------

LOCATIONS = [
    {
        "key": "tokio", "emoji": "🗼", "name": "Tokio", "nav": "Tokio",
        "sub": "Mesto, ki zna biti tudi tiho",
        "teaser": "Velemesto, ki zna biti tiho: stari vrtovi, jutranja svetišča in najboljši sushi zajtrk.",
        "intro": "Največje mesto na svetu vas bo presenetilo s tem, kako mirno zna biti. Med nebotičniki se skrivajo stare soseske, tihi vrtovi in svetišča, kjer zjutraj slišite le ptice in škripanje gramoza pod nogami. Tokio je najlepši počasi — ena soseska na dan, vmes pa dobra kava in še boljši sushi.",
        "food": [
            ("Sushi na trgu Tsukiji", "zgodaj zjutraj, ko je riba najbolj sveža — zajtrk, ki ga ne boste pozabile"),
            ("Wagyu govedina", "slavna japonska govedina, ki se dobesedno topi v ustih"),
            ("Matcha sladice v Yanaki", "zeleni čaj v obliki sladoleda, tort in piškotov v stari soseski"),
            ("Kaiseki večerja", "več majhnih, prekrasnih hodov — idealno za skupino, ki rada poskusi vse"),
            ("Topla soba juha", "ajdovi rezanci v vroči juhi, prava jesenska večerja"),
        ],
        "acts": [
            ("Sprehod po Yanaki", "stara soseska z lesenimi hišami, malimi trgovinicami in mačkami na vsakem vogalu — Tokio, kakršen je bil nekoč"),
            ("Vrt Rikugien zgodaj zjutraj", "krajinski vrt iz 17. stoletja; jeseni ves v rdečem in zlatem, s skodelico matche v čajni hišici ob jezeru"),
            ("Meiji Jingu ob osmih zjutraj", "veliko svetišče sredi gozda, ko je še mirno in skoraj brez ljudi"),
            ("Ladjica po reki Sumida", "mesto z vode — brez hoje, z lepimi pogledi na mostove in nebotičnike"),
        ],
        "fact": "V Tokiu je več restavracij z Michelinovimi zvezdicami kot v katerem koli drugem mestu na svetu — a nekatere najboljše jedi najdete v majhnih lokalih s komaj šestimi sedeži in brez napisa na vratih.",
        "magda": "V vrtu Rikugien si poiščite klopco ob jezeru in naročite skodelico matche. Nikamor se ne mudi. Opazujte odseve javorjev v vodi in pustite, da veliko mesto za pol ure počaka na vas.",
        "phrases": ["Tokyo Yanaka walking tour", "Rikugien Garden autumn"],
    },
    {
        "key": "chichibu", "emoji": "🌳", "name": "Chichibu", "nav": "Chichibu",
        "daytrip": True, "base": "Tokia",
        "sub": "Enodnevni pobeg v gore iz Tokia",
        "teaser": "Enodnevni izlet iz Tokia: gozdna kopel med cedrami, svetišča in ročni soba rezanci.",
        "intro": "Za en dan pobegnemo iz Tokia v gore. Samo dobri uri in pol vožnje stran se svet popolnoma spremeni: strme zelene gore, stoletne cedre in potoki s kristalno čisto vodo. Narodni park Chichibu–Tama–Kai je kraj, kamor Japonci pridejo dihat. Zjutraj z vlakom tja, zvečer nazaj v Tokio — vmes pa en sam počasen dan.",
        "food": [
            ("Soba rezanci", "Chichibu je znan po ajdovih rezancih — tu jih še vedno delajo ročno"),
            ("Sezonske gozdne jedi", "gobe in kostanj, ki jih jeseni ponudijo v lokalnih gostilnah"),
            ("Bento malica", "lepo zložena škatlica dobrot za postanek ob potoku"),
        ],
        "acts": [
            ("Ena lahka gozdna pot", "izberemo eno samo, položno pot — brez naglice in brez štetja kilometrov"),
            ("Shinrin-yoku — gozdna kopel", "sedenje ob potoku, globoko dihanje, poslušanje gozda; to je vse in ravno zato deluje"),
            ("Svetišče Mitake", "staro gorsko svetišče; s klopce se lepo opazuje romarje na stopnicah"),
        ],
        "fact": "Shinrin-yoku (»gozdna kopel«) je na Japonskem uradno priznana zdravstvena praksa — raziskave kažejo, da že 20 minut med drevesi občutno zniža stresne hormone.",
        "magda": "Ob potoku se ustavite, zaprite oči in pet minut samo poslušajte: vodo, veter, ptice. Temu Japonci pravijo gozdna kopel — in po njej boste natanko razumele, zakaj.",
        "phrases": ["Chichibu Tama Kai national park autumn", "Mitake shrine Japan"],
    },
    {
        "key": "kawaguchiko", "emoji": "🗻", "name": "Kawaguchiko & gora Fuji", "nav": "Fuji",
        "sub": "Zrcalna jezera pod goro Fuji",
        "teaser": "Gora Fuji nad mirnim jezerom, pagoda Chureito in jesenski drevored javorjev.",
        "intro": "Za eno noč se ustavimo pod najslavnejšo goro na svetu. Ob jezeru Kawaguchi se ob jasnem jutru gora Fuji zrcali v mirni vodi, pozno popoldne pa se za pagodo Chureito prižge najlepša razglednica Japonske. November je eden najboljših mesecev za jasne poglede na Fuji — zrak je čist, vrh pa že zasnežen.",
        "food": [
            ("Hoto rezanci", "debeli ploščati rezanci v gosti miso juhi z bučo in zelenjavo — glavna jed Yamanašija in topla jesenska večerja"),
            ("Yoshida udon", "žilavi udon rezanci, lokalna posebnost izpod Fujija"),
            ("Sladice z motivom Fujija", "od mochija do sladoleda — vse v obliki slavne gore"),
        ],
        "acts": [
            ("Pagoda Chureito", "slavni razgled: petstopenjska pagoda z goro Fuji v ozadju, jeseni uokvirjena z javorji"),
            ("Obala Oishi Park", "sprehajalna pot ob jezeru z neposrednim pogledom na Fuji in polji cvetja"),
            ("Vožnja ob jezeru Kawaguchi", "ladjica ali gondola Kachi Kachi za razglede na goro"),
        ],
        "fact": "Gora Fuji (3.776 m) je najvišja gora Japonske in sveti simbol dežele — najlepše jo vidite pozno jeseni in pozimi, ko je zrak najbolj čist in vrh že pokrit s snegom.",
        "magda": "Zjutraj vstanite zgodaj in pojdite k jezeru, preden se megla dvigne. Če je gladina mirna, boste videle dve gori Fuji — eno na nebu in eno v vodi. Tega trenutka ne hitite fotografirati.",
        "phrases": ["Chureito Pagoda Fuji autumn", "Lake Kawaguchi Mount Fuji morning"],
    },
    {
        "key": "minobusan", "emoji": "🏯", "name": "Minobusan", "nav": "Minobu",
        "sub": "Noč pri menihih na gori Minobu",
        "teaser": "Tempeljska nočitev pri menihih (šukubo Kakurinbo) in gorski tempelj Kuon-ji.",
        "intro": "Na gori Minobu stoji Kuon-ji, osrednji tempelj budistične šole Nichiren, obkrožen s starodavnimi cedrami in jeseni z žarečimi javorji. Tu prenočimo pri menihih v šukuboju Kakurinbo (že rezervirano) — z vegetarijansko večerjo in jutranjim mirom. Umirjen, oduhovljen postanek na poti proti jugu.",
        "food": [
            ("Shojin ryori", "vegetarijanska meniška večerja, pripravljena v templju — del izkušnje prenočitve"),
            ("Minobu manju", "parjeni polnjeni kolački, stara sladica romarjev"),
            ("Yuba (tofujeva koža)", "nežna specialiteta tempeljske kuhinje"),
        ],
        "acts": [
            ("Tempelj Kuon-ji", "mogočni gorski tempelj; do glavne dvorane vodi 287 strmih stopnic ali udobna vzpenjača"),
            ("Vzpenjača na vrh Minobu", "razgled na okoliške gore, ob jasnem dnevu celo na Fuji"),
            ("Jutranja molitev v templju", "tiho prisostvovanje obredu menihov ob svitu"),
        ],
        "fact": "Šukubo (prenočitev v templju) je na gori Minobu tradicija že stoletja — romarji so tu prenočevali na poti h grobu meniha Nichirena, ki je na tej gori preživel svoja zadnja leta.",
        "magda": "Po meniški večerji stopite ven v tišino gorske noči. Ni televizije, ni hrupa — le zvonovi, cedre in zvezde. Dovolite si, da za eno noč čisto upočasnite.",
        "phrases": ["Minobusan Kuonji temple autumn", "Kakurinbo shukubo Minobu"],
    },
    {
        "key": "izu", "emoji": "🌊", "name": "Izu polotok", "nav": "Izu",
        "sub": "Morje, vulkani in topli vrelci",
        "teaser": "Obala iz lave, polja pravega wasabija in onsen z razgledom na morje.",
        "intro": "Polotok vulkanskega izvora, kjer se gore spuščajo naravnost v Tihi ocean. Izu je znan po svežih ribah, poljih pravega wasabija in predvsem po onsenih — toplih vrelcih, ki izvirajo iz globin polotoka. Tu se potovanje prvič zares upočasni.",
        "food": [
            ("Sveži morski sadeži", "Izu živi od ribolova — riba pride na krožnik še isti dan"),
            ("Wasabi soba", "pravi wasabi raste prav tu; sveže nariban je čisto drugačen od tistega iz tube"),
            ("Sladoled iz sladkega krompirja", "nenavadno, a slastno — lokalna posebnost"),
        ],
        "acts": [
            ("Obala Jogasaki", "počasen sprehod po stezici ob klifih iz lave — pogledi na modrino brez konca"),
            ("Zasebni onsen v ryokanu", "topel vrelec samo za nas, z razgledom na morje — vrhunec dneva"),
            ("Shuzenji", "mali bambusov gozdiček, rdeči mostovi in čajna hiša v starem zdraviliškem mestecu"),
            ("Sončni zahod brez načrta", "en večer brez programa — samo klopca, ocean in nebo v jesenskih barvah"),
        ],
        "fact": "Izu je poln naravnih vročih vrelcev, ki izvirajo neposredno iz vulkanske preteklosti polotoka — nekateri ryokani imajo tople bazene tik ob morju.",
        "magda": "Zvečer, ko se stemni, stopite še enkrat v onsen pod odprtim nebom. Topla voda, hladen zrak, šumenje morja — to je trenutek, zaradi katerega se gre na Japonsko.",
        "phrases": ["Izu peninsula Jogasaki coast", "Shuzenji bamboo forest"],
    },
    {
        "key": "kumano", "emoji": "⛩️", "name": "Kumano Kodo", "nav": "Kumano",
        "sub": "Pot, po kateri romarji hodijo že tisoč let",
        "teaser": "Starodavna romarska pot pod tisočletnimi cedrami — sestra Camina de Santiago.",
        "intro": "Skozi gozdove polotoka Kii se že več kot tisoč let vijejo romarske poti Kumano Kodo. Po kamnitih stopnicah, med mahom in meglicami, so hodili cesarji in kmetje — vsi z istim namenom: umiriti misli. Ni treba prehoditi cele poti; dovolj je en lep, položen odsek.",
        "food": [
            ("Gorski čaj", "lokalni čaj, ki greje na postankih ob poti"),
            ("Umeboshi", "kisla slivka, ki so jo romarji od nekdaj nosili s seboj za moč"),
            ("Shojin ryori", "preprosta tempeljska vegetarijanska kuhinja — lahka in okusna"),
        ],
        "acts": [
            ("Krajši odsek romarske poti", "izberemo najlepši, položen del stare poti — kamnite stopnice, mah in tišina"),
            ("Kumano Hongu Taisha", "eno od treh velikih svetišč Kumana; v bližini stojijo največja torii vrata na svetu"),
            ("Počitek ob starodavnih cedrah", "drevesa, stara več sto let — najboljši kraj za malico in globok vdih"),
        ],
        "fact": "Kumano Kodo je ena od samo dveh romarskih poti na svetu na UNESCO seznamu svetovne dediščine — druga je Camino de Santiago v Španiji. Poti sta uradno »pobrateni«: kdor prehodi obe, prejme posebno dvojno romarsko spričevalo.",
        "magda": "Ko pridete do zares stare cedre, se ustavite in položite dlan na njeno deblo. To drevo je stalo tu že, ko so mimo hodili cesarji — in stalo bo še dolgo po nas. Lep kraj za tiho misel ali željo.",
        "phrases": ["Kumano Kodo pilgrimage walk", "Kumano Hongu Taisha"],
    },
    {
        "key": "koyasan", "emoji": "🏔️", "name": "Koya-san", "nav": "Koya-san",
        "sub": "Sveta gora tisočih templjev",
        "teaser": "Mistični Okunoin med cedrami, velika pagoda in sveti mir gore.",
        "intro": "Visoko v gorah leži Koya-san, sveto mesto s stotimi templji, ki ga je pred 1.200 leti ustanovil menih Kobo Daishi. Nočitev pri menihih je žal zasedena, a gora ostane eno najmočnejših doživetij poti — zlasti večerni sprehod med lučkami Okunoina in jutranji mir med cedrami. Ostanemo lahko tudi le eno noč.",
        "food": [
            ("Shojin ryori", "budistična vegetarijanska kuhinja — tudi za kosilo v mestnih templjih, nežna in okusna"),
            ("Sezamov tofu (goma-dofu)", "svilnata posebnost Koya-sana; take drugje ne najdete"),
        ],
        "acts": [
            ("Okunoin zvečer", "sprehod med tisoči kamnitih lantern in stoletnimi cedrami — eden najbolj mističnih krajev Japonske"),
            ("Danjo Garan in pagoda Konpon Daito", "sveti tempeljski kompleks z mogočno cinobrasto pagodo"),
            ("Tempelj Kongobu-ji", "največji kamniti vrt na Japonskem (Banryutei) in lepo poslikane dvorane"),
        ],
        "fact": "Okunoin je največje pokopališče na Japonskem — več kot 200.000 nagrobnikov med starodavnimi cedrami. Menihi verjamejo, da Kobo Daishi v svojem mavzoleju neprekinjeno meditira že več kot 1.200 let, zato mu vsak dan še vedno prinašajo obroke.",
        "magda": "Na večernem sprehodu skozi Okunoin hodite čisto počasi, čisto na koncu skupine. Lanterne, meglice med cedrami, vonj kadila — tega trenutka ne fotografirajte takoj; najprej ga samo doživite.",
        "phrases": ["Koyasan Okunoin cemetery walk", "shukubo temple stay Japan"],
    },
    {
        "key": "iya", "emoji": "🏞️", "name": "Shikoku — dolina Iya", "nav": "Iya",
        "sub": "Skrita dolina visečih mostov",
        "teaser": "Skrita dolina z visečimi mostovi iz trte in smaragdno reko globoko spodaj.",
        "intro": "Globoko na otoku Shikoku se skriva dolina Iya — eden najbolj odročnih in najlepših kotičkov Japonske. Strme gozdnate stene, smaragdna reka globoko spodaj in viseči mostovi iz trte, ki so nekoč skrivali begunce pred zasledovalci. Novembra dolina zažari v rdeči in zlati.",
        "food": [
            ("Ajdova soba", "dolina Iya je znana po ajdi — rezanci so tu gostejši in bolj rustikalni"),
            ("Pečen piščanec", "lokalna specialiteta z gorskih kmetij"),
            ("Gorska zelenjava (sansai)", "divje rastline iz okoliških gozdov, pripravljene na sto načinov"),
        ],
        "acts": [
            ("Most Kazurabashi", "prečkanje visečega mostu iz trte — počasi, korak za korakom, z dobro oprijetimi rokami in smehom"),
            ("Vožnja po dolini", "razgledi na jesenske barve, sotesko Oboke in smaragdno reko"),
            ("Male gorske vasice", "hiške na strminah, kjer se zdi, da se je čas ustavil"),
        ],
        "fact": "Viseči mostovi v dolini Iya so spleteni iz gorske trte in jih po stari tradiciji redno obnavljajo. Pravijo, da so jih nekoč gradili prav zato, da bi jih ob nevarnosti lahko hitro prerezali in ustavili zasledovalce.",
        "magda": "Na sredini mostu Kazurabashi se ustavite — trdno se držite ograje! — in poglejte navzdol na smaragdno reko. Srce bo malo pospešilo, smeh na drugi strani pa bo toliko slajši.",
        "phrases": ["Iya Valley vine bridge", "Shikoku Iya Valley autumn"],
    },
    {
        "key": "ine", "emoji": "🎣", "name": "Ine", "nav": "Ine",
        "sub": "Ribiška vasica, ki ji pravijo Benetke Japonske",
        "teaser": "»Benetke Japonske« — hiške s čolni tik nad vodo in najbolj svež sašimi.",
        "intro": "Ob mirnem zalivu na severu prefekture Kyoto stoji vasica Ine, kjer hiše ne stojijo ob morju, ampak na njem. V pritličju čoln, v nadstropju dnevna soba — tako tu živijo že stoletja. Ura vožnje s čolnom po zalivu in počasno kosilo iz ravnokar ujetih rib: to je Ine.",
        "food": [
            ("Sushi in sašimi", "riba pride naravnost iz zaliva pred hišo — bolj sveže ne gre"),
            ("Lokalni sake", "vaška pivovarna slovi po rdečkastem sakeju in eni redkih žensk mojstric sakeja na Japonskem"),
        ],
        "acts": [
            ("Vožnja s čolnom po zalivu", "pogled na funaye z vode — najlepši način, da vidite vas"),
            ("Sprehod ob zalivu", "počasna pot mimo hiš, ribičev in galebov"),
            ("Fotografiranje funay", "tradicionalne hiše nad vodo so ena najbolj fotogeničnih podob Japonske"),
        ],
        "fact": "Ine slovi po funayah — hišah, ki imajo pritličje tik nad vodo kot »garažo« za čoln, zgoraj pa bivalne prostore. Ob zalivu jih stoji okoli 230, zato vasici pravijo tudi »Benetke Japonske«.",
        "magda": "Poiščite kavarnico z okni tik nad vodo, naročite kavo in samo glejte: čolne, galebe, gladino zaliva. V Ine se ne pride česa »početi« — sem se pride biti.",
        "phrases": ["Ine funaya boat houses", "Ine fishing village Japan"],
    },
    {
        "key": "nara", "emoji": "🦌", "name": "Nara", "nav": "Nara",
        "daytrip": True, "base": "Kjota ali Osake",
        "sub": "Prva prestolnica in njeni jeleni",
        "teaser": "Veliki Buda, prijazni jeleni in zlati javorji v parku Nara.",
        "intro": "Enodnevni izlet v Naro, prvo stalno prestolnico Japonske. V ogromnem parku se med zlatimi javorji sprehajajo krotki jeleni, v templju Todai-ji pa domuje eden največjih bronastih Bud na svetu. Vse je na dosegu počasnega sprehoda — izlet naredimo na poti v Kyoto ali kot dan iz Osake.",
        "food": [
            ("Kakinoha-zushi", "sushi, zavit v liste kakija — stara narska posebnost za na pot"),
            ("Mochi iz Nakatanida", "sloviti hitri tolkači riževega mochija — predstava in sladica hkrati"),
            ("Čaj in wagashi", "mirno kosilo v čajnici ob vrtu"),
        ],
        "acts": [
            ("Tempelj Todai-ji in Veliki Buda", "ena največjih lesenih zgradb na svetu s 15-metrskim bronastim Budo"),
            ("Park Nara in jeleni", "stotine krotkih jelenov, ki se priklonijo za priboljšek — čarobno za vse"),
            ("Svetišče Kasuga Taisha", "pot med tisočimi kamnitimi in bronastimi lučmi skozi gozd"),
            ("Vrt Isuien", "miren krajinski vrt z razgledom na gore — manj znan biser"),
        ],
        "fact": "Naro so pred Kjotom za nekaj desetletij postavili za prestolnico (710–784). Jeleni v parku so po šintoistični veri sveti glasniki bogov, zato jih varujejo že več kot tisoč let.",
        "magda": "Kupite nekaj jelenjih piškotov (shika senbei) in se umaknite stran od gneče. Ko se vam jelen mirno prikloni, se morate le nasmehniti — to je trenutek, ki ga odnesete domov.",
        "phrases": ["Nara Todaiji deer park autumn", "Kasuga Taisha Nara"],
    },
    {
        "key": "kyoto", "emoji": "🍁", "name": "Kyoto", "nav": "Kyoto",
        "sub": "Tisočletna prestolnica v jesenskih barvah",
        "teaser": "Templji, zen vrtovi in čajne hiše na vrhuncu jesenskega obarvanja.",
        "intro": "Tisoč let je bil Kyoto prestolnica Japonske in vse to se še danes čuti: templji, čajne hiše, gejše, vrtovi. Novembra je mesto na vrhuncu momiji — jesenskega obarvanja javorjev — zato bo to eden od vrhuncev potovanja. Skrivnost je vstati zgodaj: ob sedmih zjutraj so tudi najbolj znameniti kraji skoraj prazni.",
        "food": [
            ("Kaiseki", "vrhunec japonske kuhinje — večerja kot umetniška razstava"),
            ("Matcha v vseh oblikah", "sladoled, torte, čaj — Kyoto je prestolnica zelenega čaja"),
            ("Yudofu", "nežen kuhan tofu, specialiteta tempeljskih restavracij — popoln za hladen dan"),
        ],
        "acts": [
            ("Zen vrtovi zgodaj zjutraj", "Ryoan-ji in Ginkaku-ji ob odprtju, ko je gramoz sveže pograbljen in ljudi še ni"),
            ("Bambusov gozd Arashiyama", "pred deveto uro, preden pridejo množice — takrat je zares čaroben"),
            ("Čajna ceremonija", "ura miru in lepote — spoznamo, zakaj je skodelica čaja lahko obred"),
        ],
        "fact": "Kyoto ima več kot 1.600 budističnih templjev in okoli 400 šintoističnih svetišč — mesto je bilo prestolnica Japonske več kot tisoč let, preden je to vlogo prevzel Tokio.",
        "magda": "V templju Ryoan-ji sedite na leseno verando pred kamnitim vrtom in ostanite vsaj deset minut — tudi ko se vam bo zdelo, da ste »že videle«. Ravno takrat se zgodi tisto pravo.",
        "phrases": ["Kyoto autumn colors", "Arashiyama bamboo grove early morning"],
    },
    {
        "key": "osaka", "emoji": "🏙️", "name": "Osaka", "nav": "Osaka",
        "sub": "Kuhinja Japonske",
        "teaser": "Kuhinja Japonske za vesel zaključek: takoyaki, neonske luči in nazdravljanje.",
        "intro": "Za konec — mesto, ki se rado smeji in še raje jé. Osaka je neuradna »kuhinja Japonske«: tu se ne sprašuje, kje bi jedli, ampak kaj bomo pojedle najprej. Popoln kraj za zadnje večere, nazdravljanje in nakup spominkov.",
        "food": [
            ("Takoyaki", "vroče kroglice s hobotnico, ki se jih jé kar na ulici"),
            ("Okonomiyaki", "»japonska pica« — slastna palačinka z zeljem, ki jo spečejo pred vami"),
            ("Ulica Dotonbori", "gastronomska ulica, kjer se večerja kar med sprehodom — od stojnice do stojnice"),
        ],
        "acts": [
            ("Večerni sprehod ob Dotonboriju", "neonske luči, ki se zrcalijo v kanalu — Osaka v najboljši izdaji"),
            ("Grad Osaka", "mogočen grad sredi parka; jeseni ga obdajo zlati ginki"),
            ("Tržnica Kuromon", "»kuhinja Osake« — pokrita tržnica za pokušanje in nakup spominkov"),
        ],
        "fact": "Osaki že stoletja pravijo »Tenka no Daidokoro« — kuhinja dežele. Mesto je obogatelo s trgovino z rižem in hrano, domačini pa še danes radi rečejo »kuidaore«: jej, dokler ne padeš.",
        "magda": "Zadnji večer se ustavite na mostu sredi Dotonborija, naročite vsaka svoj takoyaki in nazdravite: kanpai! Mesec dni Japonske — to je treba proslaviti.",
        "phrases": ["Osaka Dotonbori night walk", "Osaka street food"],
    },
    {
        "key": "hiroshima", "emoji": "🕊️", "name": "Hiroshima", "nav": "Hiroshima",
        "daytrip": True, "base": "Osake",
        "sub": "Mesto miru in plavajoči torii",
        "teaser": "Park miru, pretresljiv muzej in plavajoča torija svetišča Itsukušima na otoku Miyajima.",
        "intro": "Enodnevni izlet za tiste, ki želijo. Hiroshima je mesto, ki je iz najhujše tragedije zraslo v simbol miru — Park miru in muzej sta ganljiva in pomembna. V bližini pa na otoku Miyajima nad morjem lebdi ena najlepših podob Japonske: velika rdeča torija svetišča Itsukušima.",
        "food": [
            ("Hiroshimski okonomiyaki", "plastna različica s testeninami yakisoba — drugačna in slastnejša od osaške"),
            ("Ostrige (kaki)", "Hiroshima slovi po ostrigah; jeseni so na vrhuncu — na žaru ali ocvrte"),
            ("Momiji manju", "kolački v obliki javorjevega lista z nadevom — sladek spominek z Miyajime"),
        ],
        "acts": [
            ("Park miru in muzej", "spomenik žrtvam in pretresljiv muzej — pomemben, a težak obisk"),
            ("Atomska kupola (A-Bomb Dome)", "ostanek stavbe pod epicentrom, UNESCO spomenik miru"),
            ("Otok Miyajima in plavajoči torii", "trajekt na otok z veliko rdečo torijo, ki ob plimi lebdi nad morjem; jeseni žari dolina Momijidani"),
        ],
        "fact": "Velika torija svetišča Itsukušima na Miyajimi stoji v morju že od 12. stoletja; ob plimi se zdi, da plava na vodi. Otok je skupaj s Parkom miru na UNESCO seznamu svetovne dediščine.",
        "magda": "Po obisku muzeja si vzemite čas na Miyajimi. Stopite do torije ob oseki, poslušajte morje in pustite, da težo dneva nadomesti mir. Oboje je del iste zgodbe.",
        "phrases": ["Hiroshima Peace Memorial Park", "Miyajima floating torii autumn"],
    },
]

# ----------------------------------------------------------------------------
# VIDEI (iz workflowa; videos.json = [{key, name, videos:[{id,title,channel}]}])
# ----------------------------------------------------------------------------

VIDEOS = {}
vpath = os.path.join(HERE, "videos.json")
if os.path.exists(vpath):
    with open(vpath, encoding="utf-8") as f:
        for entry in json.load(f):
            VIDEOS[entry["key"]] = entry.get("videos", [])

# Vodniški podatki iz raziskave (guide.json = [{key, sights, practical,
# day_plan, food_categories, extra_videos}])
GUIDE = {}
gpath = os.path.join(HERE, "guide.json")
if os.path.exists(gpath):
    with open(gpath, encoding="utf-8") as f:
        for entry in json.load(f):
            GUIDE[entry["key"]] = entry

# Število noči na postajo (prenočitvene baze; enodnevni izleti so posebej označeni)
DAYS = {
    "tokio": "4 noči", "kawaguchiko": "1 noč", "minobusan": "1 noč pri menihih",
    "izu": "3 noči", "kumano": "3 noči", "koyasan": "1–2 noči", "iya": "3 noči",
    "ine": "2 noči", "kyoto": "5 noči", "osaka": "5 noči",
}


def stop_label(loc):
    """Oznaka postaje: baza z nočmi, ali enodnevni izlet."""
    if loc.get("daytrip"):
        return f"Enodnevni izlet iz {loc['base']}"
    if DAYS.get(loc["key"]):
        return DAYS[loc["key"]]
    return ""


def _load_json(name, default):
    p = os.path.join(HERE, name)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return default


# Osebne rubrike po lokacijah (rubrics.json = {key: {najlepsi_trenutek, ura_zase, mandala}})
RUBRICS = _load_json("rubrics.json", {})
# Načrt poti (itinerary.json = {intro, days:[...], legs:[...]})
ITINERARY = _load_json("itinerary.json", {})
# Praktična poglavja (practical.json = {pred-odhodom, denar, prevoz})
PRACTICAL = _load_json("practical.json", {})
# Doživetja (dozivetja.json = {intro, categories:[...]})
DOZIVETJA = _load_json("dozivetja.json", {})
# Dodatki po lokacijah (extras.json = {key: {prespati, dez}})
EXTRAS = _load_json("extras.json", {})
# Foto/video izzivi za album (izzivi.json = {key: [{t, x}, ...]})
IZZIVI = _load_json("izzivi.json", {})

# Praktični podatki: nastanitve, vstopnice, povezave za prevoz (data_jp.py; za drugo potovanje jih prepiše gen_<ime>.py)
LODGING = JP.LODGING
BOOK = JP.BOOK
LEG_LINKS = JP.LEG_LINKS
QUICKBUY = JP.QUICKBUY
DOZ_SEARCH = JP.DOZ_SEARCH
FOOD_LINKS = JP.FOOD_LINKS

_SL_MON = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "avg", "sep", "okt", "nov", "dec"]


def sl_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d}. {_SL_MON[m - 1]}"


# Koordinate znamenitosti/lokalov (geocode.py → geocache.json)
GEO = _load_json("geocache.json", {})

_GENERIC = {"cafe", "restaurant", "shop", "house", "honten", "store", "market", "sushi", "ramen", "udon", "soba",
            "tempura", "noodle", "noodles", "kitchen", "bakery", "main", "branch", "hotel"}


def _dist_km(a_lat, a_lon, b_lat, b_lon):
    import math
    r = 6371.0
    p1, p2 = math.radians(a_lat), math.radians(b_lat)
    dp, dl = p2 - p1, math.radians(b_lon - a_lon)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def _geo_ok(q, key, food):
    """Koordinate iz predpomnilnika, če so verjetno prave (blizu postaje, ime se ujema)."""
    g = GEO.get(q)
    m = MAPS.get(key)
    if not g or not m:
        return None
    if _dist_km(m[0], m[1], g["lat"], g["lon"]) > CFG.get("geo_radius_km", 60):
        return None
    broad = g.get("cls") in ("boundary", "place") and g.get("via", q) != q
    if broad or (food and g.get("cls") in ("boundary", "place")):
        return None
    if food:
        first = q.split(",")[0].lower()
        toks = [t for t in re.findall(r"[a-z0-9]+", first) if len(t) >= 4 and t not in _GENERIC]
        if toks and not any(t in (g.get("name", "") or "").lower() for t in toks):
            return None
    return g


def map_points(key):
    """Točke za zemljevid kraja: oštevilčene znamenitosti (s) in lokali s hrano (f)."""
    pts, sight_no = [], {}
    guide = GUIDE.get(key, {})
    n = 0
    for sg in guide.get("sights", []):
        g = _geo_ok(sg.get("maps", ""), key, False)
        if g:
            n += 1
            sight_no[sg["name"]] = n
            pts.append({"t": "s", "n": n, "name": sg["name"], "lat": round(g["lat"], 5), "lon": round(g["lon"], 5),
                        "q": sg["maps"]})
    for c in guide.get("food_categories", []):
        for pl in c.get("places", []):
            g = _geo_ok(pl.get("maps", ""), key, True)
            if g:
                pts.append({"t": "f", "name": pl["name"], "lat": round(g["lat"], 5), "lon": round(g["lon"], 5),
                            "q": pl["maps"]})
    return pts, sight_no


# Zemljevidi: središče (lat, lon), stopnja povečave (zoom) in iskalni niz za Google Maps.
# Zoom: ~11–12 = regija/večje mesto, 13 = mesto/kraj, 14 = ožji kraj/vas.
MAPS = {
    "tokio":       (35.712, 139.775, 12, "Ueno, Taito, Tokyo"),
    "chichibu":    (35.991, 139.085, 13, "Chichibu, Saitama"),
    "kawaguchiko": (35.517, 138.764, 13, "Lake Kawaguchi, Fujikawaguchiko"),
    "minobusan":   (35.404, 138.437, 14, "Kuonji Temple, Minobu, Yamanashi"),
    "izu":         (34.973, 138.925, 13, "Shuzenji, Izu, Shizuoka"),
    "kumano":      (33.668, 135.890, 12, "Kumano Nachi Taisha, Wakayama"),
    "koyasan":     (34.213, 135.584, 14, "Koyasan, Koya, Wakayama"),
    "iya":         (33.900, 133.840, 12, "Iya Valley, Miyoshi, Tokushima"),
    "ine":         (35.682, 135.287, 14, "Ine no Funaya, Kyoto"),
    "nara":        (34.685, 135.843, 14, "Nara Park, Nara"),
    "kyoto":       (35.011, 135.768, 12, "Kyoto, Japan"),
    "osaka":       (34.669, 135.501, 13, "Dotonbori, Osaka"),
    "hiroshima":   (34.393, 132.459, 12, "Hiroshima Peace Memorial Park"),
}

# Fotografije (neobvezno): če obstaja japonska-2026-stran/images/<key>.(jpg|jpeg|png|webp),
# se uporabi kot naslovna slika; sicer ostane risana SVG ilustracija.
_PHOTO_EXTS = ("jpg", "jpeg", "png", "webp")


def photo_for(key):
    for ext in _PHOTO_EXTS:
        rel = f"images/{key}.{ext}"
        if os.path.exists(os.path.join(OUT, rel)):
            return rel
    return None


def banner_html(key, svg, alt, extra_cls=""):
    """Naslovni pas: fotografija, če obstaja, sicer risana ilustracija."""
    cls = "scene-banner" + (f" {extra_cls}" if extra_cls else "")
    photo = photo_for(key)
    if photo:
        return (f'<div class="{cls}"><img class="photo-banner" src="{esc(photo)}" '
                f'alt="{esc(alt)}" loading="eager" decoding="async"></div>')
    return f'<div class="{cls}">{svg}</div>'


def card_media(key, svg):
    """Sličica na kartici: optimizirana foto sličica, če obstaja, sicer SVG."""
    thumb = os.path.join(OUT, "images", "thumbs", f"{key}.jpg")
    if os.path.exists(thumb):
        return (f'<img class="card-photo" src="images/thumbs/{key}.jpg" '
                f'alt="" loading="lazy" decoding="async">')
    return svg

# ----------------------------------------------------------------------------
# PREDLOGE
# ----------------------------------------------------------------------------

def esc(s):
    return html.escape(str(s), quote=True)


def trip_boot():
    """Nastavitve potovanja za JS + zaščita: brez PIN-a vrne na vstopno stran."""
    t = {"id": CFG["id"], "slug": CFG["slug"], "people": CFG["people"], "gate": "../index.html",
         "after": CFG.get("after"), "t": CFG.get("t"), "color": CFG.get("pin"), "country": CFG.get("country"),
         "stations": [{"k": l["key"], "e": l["emoji"], "n": l["nav"]} for l in LOCATIONS]}
    guard = ('(function(){try{var s=JSON.parse(localStorage.getItem("trip_session")||"null");'
             'var ok=s&&s.trips&&s.trips.some(function(t){return t.slug===TRIP.slug});'
             'if(!ok){location.replace(TRIP.gate+"?next="+encodeURIComponent(TRIP.slug));}}catch(e){}})();')
    return "  <script>window.TRIP=" + json.dumps(t, ensure_ascii=False) + ";" + guard + "</script>\n"


def head(title, desc, with_map=False, with_album=False):
    leaflet = ""
    if with_map:
        leaflet = (
            '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">\n'
            '  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>\n'
        )
    album = ""
    if with_album:
        album = (
            '  <script defer src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n'
            f'  <script defer src="album.js?v={BUILD}"></script>\n'
        )
    return f"""<!DOCTYPE html>
<html lang="sl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <meta name="robots" content="noindex,nofollow">
  <meta name="theme-color" content="{CFG['theme']}">
{trip_boot()}  <link rel="stylesheet" href="style.css?v={BUILD}">
{CFG.get("css", "")}
{leaflet}{album}  <link rel="manifest" href="manifest.json">
  <link rel="icon" href="icons/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
</head>
<body>
"""


NAV_PRIMARY = [
    ("index.html", "index", "🏠", "Domov"),
    ("kako.html", "kako", "🎓", "Kako uporabljati"),
    ("nacrt.html", "nacrt", "🗺️", "Načrt poti"),
    ("izziv.html", "izziv", "📸", "Izzivi"),
    ("nalozi.html", "nalozi", "📤", "Naloži fotografije"),
    ("dozivetja.html", "dozivetja", "🎨", "Doživetja"),
    ("priprave.html", "priprave", "🎒", "Priprave"),
    ("prevajalec.html", "prevajalec", "🔍", "Prevajalec s kamero"),
    ("nasveti.html", "nasveti", "💡", "Nasveti in kartice"),
    ("nujno.html", "nujno", "🆘", "Nujno"),
]
STATIONS_LABEL = "Postaje potovanja"


def nav(current_key):
    def cur(key):
        return ' aria-current="page"' if current_key == key else ""

    primary = list(NAV_PRIMARY) + [("../index.html?izpis=1", "gate", "🔑", "Zamenjaj potovanje")]
    prim = "\n".join(
        f'        <a href="{h}"{cur(k)}><span class="mi-emoji" aria-hidden="true">{e}</span>{esc(l)}</a>'
        for (h, k, e, l) in primary)
    stations = "\n".join(
        f'        <a href="{loc["key"]}.html"{cur(loc["key"])}>'
        f'<span class="mi-emoji" aria-hidden="true">{loc["emoji"]}</span>{esc(loc["nav"])}</a>'
        for loc in LOCATIONS)

    # trenutna stran za oznako v gumbu
    here = "Domov"
    for h, k, e, l in primary:
        if k == current_key:
            here = l
    for loc in LOCATIONS:
        if loc["key"] == current_key:
            here = loc["nav"]

    return f'''<header class="site-header">
  <div class="nav-inner">
    <a class="brand" href="index.html">{esc(CFG["brand"])}</a>
    <button class="menu-toggle" id="menu-toggle" aria-expanded="false" aria-controls="main-menu">
      <span class="mt-ico" aria-hidden="true">☰</span> Meni
    </button>
  </div>
  <nav class="main-menu" id="main-menu" aria-label="Glavni meni" hidden>
    <div class="menu-inner">
      <div class="menu-primary">
{prim}
      </div>
      <p class="menu-label">{STATIONS_LABEL}</p>
      <div class="menu-stations">
{stations}
      </div>
    </div>
  </nav>
</header>
<div class="menu-backdrop" id="menu-backdrop" hidden></div>
'''


def make_footer(l1, l2):
    return f"""<footer>
  <p>{l1}</p>
  <p>{l2}</p>
  <p><a href="kako.html">🎓 Kako uporabljati to stran</a> · <a href="../index.html?izpis=1">🔑 Zamenjaj potovanje</a></p>
</footer>
<script src="app.js?v={BUILD}"></script>
</body>
</html>
"""


FOOTER = make_footer("🍁 Japonska — Mesec za dušo · 3. november – 2. december 2026 · Tokio → Osaka",
                     "Z ljubeznijo pripravljeno za Magdo in prijateljice")


def yt_search_url(phrase):
    return "https://www.youtube.com/results?search_query=" + urllib.parse.quote(phrase)


def maps_url(query):
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(query)


# Samodejna ikonica za znamenitost glede na ime/opis (po ključnih besedah).
SIGHT_ICONS = [
    (("onsen", "vroč", "termaln", "kopel", "vrelc", "kopališč"), "♨️"),
    (("torii", "svetišč", "šinto", "jinja", "taisha"), "⛩️"),
    (("tempelj", "templ", "pagod", "budist", "šukubo", "shukubo", "mavzolej", "okunoin", "-ji ", "-in "), "🏯"),
    (("pokopališč", "nagrobni"), "🕯️"),
    (("vrt", "javor", "momiji", "park", "drevored", "gink", "bambus"), "🍁"),
    (("ladjic", "ladja", "čoln", "barka", "zaliv", "vožnja po", "cruise", "reki", "soteska"), "⛵"),
    (("most", "bridge", "kazurabashi"), "🌉"),
    (("tržnic", "trg ", "market", "kuromon", "nishiki", "tsukiji", "stojnic"), "🍢"),
    (("čajnic", "čajn", "matcha", "matcho", "čaj"), "🍵"),
    (("grad", "castle"), "🏯"),
    (("razgled", "panoram", "stolp", "vzpenjač", "sedežnic", "ropeway", "sky"), "🌄"),
    (("muzej", "galerij"), "🏛️"),
    (("obal", "morj", "plaž", "klif", "coast"), "🌊"),
    (("gozd", "cedr", "pohod", "sprehod", "pot ", "poti"), "🌲"),
    (("sake", "pivovarn", "vinar"), "🍶"),
    (("vas", "funaya", "sosesk", "ulic", "četrt", "mesto"), "🏘️"),
]


def sight_icon(name, desc=""):
    text = (name + " " + desc).lower()
    for keys, icon in SIGHT_ICONS:
        if any(k in text for k in keys):
            return icon
    return "📍"


PLAN_ICONS = {"Zjutraj": "🌅", "Dopoldne": "🌤️", "Popoldne": "🍂", "Zvečer": "🌙"}


def count_label(n):
    if n == 1:
        return "1 predlog"
    if n == 2:
        return "2 predloga"
    if n in (3, 4):
        return f"{n} predlogi"
    return f"{n} predlogov"


def sights_section(g):
    sights = g.get("sights", [])
    if not sights:
        return ""
    parts = ['<section class="card-section" aria-labelledby="znamenitosti">',
             f'  <h2 id="znamenitosti">{TXT.get("sights_h", "⛩️ Znamenitosti in doživetja")}</h2>']
    for s in sights:
        icon = s.get("icon") or sight_icon(s["name"], s.get("desc", ""))
        no = map_points(g.get("key", ""))[1].get(s["name"])
        badge = f'<span class="sight-no" title="Številka na zemljevidu">{no}</span>' if no else ""
        parts.append('  <article class="sight">')
        parts.append(f'    <h3><span class="sight-icon" aria-hidden="true">{icon}</span>{esc(s["name"])}{badge}</h3>')
        parts.append(f"    <p>{esc(s['desc'])}</p>")
        if s.get("tip"):
            parts.append(f'    <p class="sight-tip">💡 {esc(s["tip"])}</p>')
        parts.append('    <div class="action-row">')
        if s.get("maps"):
            parts.append(f'      <a class="pin-btn" href="{maps_url(s["maps"])}" target="_blank" rel="noopener">📍 Zemljevid</a>')
        if s.get("yt"):
            parts.append(f'      <a class="vid-btn" href="{yt_search_url(s["yt"])}" target="_blank" rel="noopener">🎬 Video</a>')
        parts.append("    </div>")
        parts.append("  </article>")
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def _clock_icon(t):
    """Ikona za uro v obliki »9.00« ali »13.30« (jutro/poldne/popoldne/večer)."""
    m = re.match(r"(\d{1,2})", t or "")
    if not m:
        return "•"
    h = int(m.group(1))
    return "🌅" if h < 11 else "🍽️" if h < 14 else "🍂" if h < 18 else "🌙"


def day_plan_section(g):
    plan = g.get("day_plan", [])
    if not plan:
        return ""
    parts = ['<section class="card-section" aria-labelledby="dan">',
             '  <h2 id="dan">🗓️ Predlog enega lepega dne</h2>',
             '  <ul class="plan-list">']
    for p in plan:
        ic = PLAN_ICONS.get(p["time"]) or _clock_icon(p["time"])
        parts.append(f'    <li><span class="plan-time"><span class="plan-ic" aria-hidden="true">{ic}</span> {esc(p["time"])}</span>'
                     f'<span>{esc(p["what"])}</span></li>')
    parts.append("  </ul>\n</section>")
    return "\n".join(parts) + "\n"


def food_section(loc, g):
    parts = ['<section class="card-section" aria-labelledby="hrana">',
             '  <h2 id="hrana">🍜 Hrana — kaj in kje jesti</h2>',
             '  <h3 style="margin:0 0 0.3rem; font-size:1.1rem;">Kaj poskusiti</h3>',
             '  <ul class="nice-list">']
    for name, desc in loc["food"]:
        parts.append(f"    <li><strong>{esc(name)}</strong> — {esc(desc)}</li>")
    parts.append("  </ul>")
    cats = g.get("food_categories", [])
    if cats:
        parts.append('  <h3 style="margin:1.2rem 0 0.3rem; font-size:1.1rem;">Kje jesti — izberite kategorijo</h3>')
        parts.append('  <p class="cat-intro">Dotaknite se kategorije in odprl se bo seznam preverjenih predlogov s povezavo na zemljevid.</p>')
        if FOOD_LINKS:
            parts.append('  <div class="buy-row">' + "".join(
                _btn(lbl, url, "buy-btn alt") if url else f'<span class="buy-note">{esc(lbl)}</span>'
                for lbl, url in FOOD_LINKS) + "</div>")
        for c in cats:
            places = c.get("places", [])
            if not places:
                continue
            parts.append('  <details class="food-cat">')
            parts.append(f'    <summary><span class="cat-emoji" aria-hidden="true">{c.get("emoji", "🍽️")}</span>'
                         f'<span class="cat-name">{esc(c["name"])}</span>'
                         f'<span class="cat-count">{count_label(len(places))}</span><span class="chev" aria-hidden="true">▶</span></summary>')
            parts.append('    <div class="cat-body">')
            if c.get("intro"):
                parts.append(f'      <p class="cat-intro">{esc(c["intro"])}</p>')
            for p in places:
                parts.append('      <div class="place">')
                parts.append(f'        <div class="place-head"><strong>{esc(p["name"])}</strong>'
                             f'<span class="price">{esc(p.get("price", "€€"))}</span></div>')
                parts.append(f"        <p>{esc(p['desc'])}</p>")
                if p.get("maps"):
                    parts.append(f'        <a class="pin-btn" href="{maps_url(p["maps"])}" target="_blank" rel="noopener">📍 Zemljevid</a>')
                parts.append("      </div>")
            parts.append("    </div>\n  </details>")
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def practical_section(g):
    tips = g.get("practical", [])
    if not tips:
        return ""
    parts = ['<section class="card-section" aria-labelledby="prakticno">',
             '  <h2 id="prakticno">🧭 Dobro je vedeti</h2>',
             '  <ul class="nice-list">']
    for t in tips:
        parts.append(f"    <li>{esc(t)}</li>")
    parts.append("  </ul>\n</section>")
    return "\n".join(parts) + "\n"


def map_section(key):
    """Zemljevid kraja: privzeto na ravni mesta/kraja (z oštevilčenimi znamenitostmi in lokali);
    gumb »država« pokaže, kje v državi je kraj. Povečava se prilagodi točkam (fitBounds v app.js)."""
    m = MAPS.get(key)
    if not m:
        return ""
    lat, lon, zoom, q = m
    pts, _ = map_points(key)
    ctry = (CFG.get("country") or {}).get("name", "država")
    legend = ""
    if pts:
        legend = ('  <p class="map-legend"><span class="rm-pin rm-inline">1</span> znamenitosti (po vrsti v seznamu) '
                  '&nbsp; <span class="rm-pin rm-food rm-inline">🍴</span> hrana. Tapnite oznako za povezavo.</p>\n')
    return (f'<section class="card-section map-section" aria-labelledby="zemljevid">\n'
            f'  <h2 id="zemljevid">🗺️ Zemljevid kraja</h2>\n'
            f'  <div class="map-modes" role="group" aria-label="Pogled zemljevida">'
            f'<button type="button" class="on" data-mode="city">📍 Kraj</button>'
            f'<button type="button" data-mode="country">🌏 {esc(ctry)}</button></div>\n'
            f'  <div class="area-map" data-lat="{lat}" data-lon="{lon}" data-zoom="{zoom}" '
            f'role="img" aria-label="Zemljevid — {esc(q)}"></div>\n'
            f'{legend}'
            f'  <script type="application/json" class="map-pts">{json.dumps(pts, ensure_ascii=False)}</script>\n'
            f'  <a class="pin-btn map-open" href="{maps_url(q)}" target="_blank" rel="noopener">'
            f'📍 Odpri na Google Zemljevidu</a>\n</section>\n')


def _challenge_data(key):
    loc = next((l for l in LOCATIONS if l["key"] == key), None)
    out = []
    for i, it in enumerate(IZZIVI.get(key, [])):
        out.append({"id": f"{key}-{i}", "t": it.get("t", "foto"), "x": it["x"],
                    "w": it.get("w", ""), "p": it.get("p"),
                    "s": key, "sn": loc["nav"] if loc else key,
                    "e": loc["emoji"] if loc else "📍"})
    return out


def izzivi_section(key):
    items = IZZIVI.get(key, [])
    if not items:
        return ""
    data = json.dumps(_challenge_data(key), ensure_ascii=False)
    return (
        '<section class="card-section izzivi" aria-labelledby="izzivi">\n'
        '  <h2 id="izzivi">📸 Foto izzivi za album</h2>\n'
        f'  <p class="cat-intro">{TXT["izzivi_intro"]} <a href="izziv.html">Vsi izzivi na enem mestu →</a></p>\n'
        '  <div class="album-gate"></div>\n'
        f'  <div class="izziv-board" data-scope="{key}"></div>\n'
        f'  <script type="application/json" id="izziv-data">{data}</script>\n'
        '</section>\n')


def stay_dates(key):
    """(prihod, odhod) iz načrta poti: od prvega dne postaje do dneva po zadnjem; lahko prepiše »in«/»out«."""
    ent = LODGING.get(key, {})
    if ent.get("in") and ent.get("out"):
        return ent["in"], ent["out"]
    days = [d for d in ITINERARY.get("days", [])
            if REGION_KEY.get(d["region"]) == key and d["region"] != "Odhod" and key not in DAYTRIP_BASE]
    if not days:
        return None
    ci = day_iso(days[0]["day"])
    co = (_dt.date.fromisoformat(day_iso(days[-1]["day"])) + _dt.timedelta(days=1)).isoformat()
    return ci, co


def _btn(label, url, cls="buy-btn"):
    return f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener">{label}</a>'


def stay_section(key):
    e = EXTRAS.get(key, {})
    lod = LODGING.get(key)
    if not e.get("prespati") and not lod:
        return ""
    parts = ['<section class="card-section stay-section" aria-labelledby="prespati">',
             '  <h2 id="prespati">🏡 Kje prespati</h2>']
    if e.get("prespati"):
        parts.append(f'  <p>{esc(e["prespati"])}</p>')
    if lod:
        adults = len(CFG["people"])
        rooms = lod.get("rooms", max(1, adults // 2))
        dates = stay_dates(key)
        parts.append('  <div class="stay-box">')
        if lod.get("optional"):
            parts.append('    <p class="stay-dates">Neobvezno: dodatna noč (če jo želite)</p>')
        elif dates:
            ci, co = dates
            parts.append(f'    <p class="stay-dates">📅 <strong>{sl_date(ci)} → {sl_date(co)}</strong> · {L.nights(ci, co)} '
                         f'{"noč" if L.nights(ci, co) == 1 else ("noči" if L.nights(ci, co) == 2 else "noči")}'
                         f' · {adults} {"osebi" if adults == 2 else "osebe"} · {rooms} {"soba" if rooms == 1 else "sobi"}</p>')
        else:
            ci = co = None
        if not dates or lod.get("optional"):
            ci = co = None
        if lod.get("booked"):
            parts.append(f'    <p class="stay-booked">✅ {esc(lod["booked"])}</p>')
        elif lod.get("book"):
            q = lod["book"]
            parts.append('    <div class="buy-row">')
            parts.append("      " + _btn("🏨 Booking.com", L.booking(q, ci, co, adults, rooms)))
            if lod.get("air"):
                parts.append("      " + _btn("🏠 Airbnb (2+ spalnici)", L.airbnb(lod["air"], ci, co, adults)))
            parts.append("      " + _btn("🔎 Google Hotels (primerjava)", L.google_hotels(q, ci, co, adults)))
            parts.append("    </div>")
            note = (f"Datumi, {adults} osebe in {rooms} sobi so že vneseni; Booking je filtriran na brezplačen preklic in oceno 8+."
                    if ci else "Datume vnesite sami; Booking je filtriran na brezplačen preklic in oceno 8+.")
            parts.append(f'    <p class="buy-note">{esc(note)} Preverite končno ceno z davki in pogoje preklica.</p>')
        if lod.get("where"):
            parts.append(f'    <h3 class="stay-sub">📍 Kje iskati</h3>\n    <p>{esc(lod["where"])}</p>')
        if lod.get("cheaper"):
            parts.append(f'    <h3 class="stay-sub">💶 Kje je ceneje</h3>\n    <p>{esc(lod["cheaper"])}</p>')
        if lod.get("search"):
            n = len(lod["search"])
            parts.append(f'    <h3 class="stay-sub">🔍 Kaj poiščite ({"4 najboljše možnosti" if n >= 4 else "predlogi"})</h3>')
            parts.append('    <ol class="stay-search">')
            for it in lod["search"]:
                parts.append(f"      <li>{esc(it)}</li>")
            parts.append("    </ol>")
        if lod.get("links"):
            parts.append('    <div class="buy-row">')
            for lbl, url in lod["links"]:
                parts.append("      " + _btn(lbl, url, "buy-btn alt"))
            parts.append("    </div>")
        parts.append("  </div>")
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def book_section(key):
    items = BOOK.get(key)
    if not items:
        return ""
    parts = ['<section class="card-section book-section" aria-labelledby="karte">',
             '  <h2 id="karte">🎟️ Karte, prevoz in rezervacije</h2>',
             '  <p class="cat-intro">Uradne in preverjene strani: tapnite in rezervirajte ali preverite urnik.</p>',
             '  <ul class="book-list">']
    for it in items:
        label, url = it[0], it[1]
        note = it[2] if len(it) > 2 else ""
        parts.append(f'    <li>{_btn(esc(label) + " →", url, "buy-btn alt")}'
                     + (f'<span class="book-note">{esc(note)}</span>' if note else "") + "</li>")
    parts.append("  </ul>\n</section>")
    return "\n".join(parts) + "\n"


def quickbuy_section():
    if not QUICKBUY:
        return ""
    parts = ['<h2 class="chapter-title" id="povezave">🔗 Kupi in rezerviraj</h2>',
             '<p class="chapter-sub">Neposredne povezave — tapnite in kupite, rezervirajte ali preverite vozni red</p>',
             '<section class="card-section quickbuy" aria-labelledby="povezave">']
    for emoji, title, items in QUICKBUY:
        parts.append(f'  <h3 class="stay-sub">{emoji} {esc(title)}</h3>\n  <div class="buy-row">')
        for lbl, url in items:
            parts.append("    " + _btn(esc(lbl) + " →", url, "buy-btn alt"))
        parts.append("  </div>")
    parts.append('  <p class="buy-note">Povezave vodijo na uradne strani ali iskanja; cene in razpoložljivost so vedno aktualne šele tam.</p>')
    parts.append("</section>")
    return "\n".join(parts) + "\n"


RUBRIC_META = [
    ("najlepsi_trenutek", "🍁 Najlepši trenutek dneva", "rubric-moment"),
    ("ura_zase", "☕ Vzemi si uro zase", "rubric-hour"),
    ("mandala", "🎨 Navdih za mandalo", "rubric-mandala"),
]


def rubric_section(key):
    r = RUBRICS.get(key) or {}
    e = EXTRAS.get(key, {})
    if not r and not e.get("dez"):
        return ""
    parts = ['<section class="rubric-wrap" aria-label="Osebne rubrike">']
    for field, title, cls in RUBRIC_META:
        if r.get(field):
            parts.append(f'  <div class="card-section rubric {cls}">')
            parts.append(f'    <h2>{title}</h2>')
            parts.append(f'    <p>{esc(r[field])}</p>')
            parts.append('  </div>')
    if e.get("dez"):
        parts.append('  <div class="card-section rubric rubric-rain">')
        parts.append('    <h2>☔ Če dežuje</h2>')
        parts.append(f'    <p>{esc(e["dez"])}</p>')
        parts.append('  </div>')
    parts.append('  <div class="card-section diary">')
    parts.append(f'    <h2>{TXT["diary"]}</h2>')
    parts.append(f'    <p class="diary-hint">{TXT["diary_hint"]}</p>')
    parts.append('    <div class="diary-lines" aria-hidden="true"></div>')
    parts.append('  </div>')
    parts.append('</section>')
    return "\n".join(parts) + "\n"


def videos_section(loc):
    vids = list(VIDEOS.get(loc["key"], []))
    for ev in GUIDE.get(loc["key"], {}).get("extra_videos", []):
        if ev.get("id") and ev["id"] not in {v["id"] for v in vids}:
            vids.append(ev)
    parts = ['<section class="card-section" aria-labelledby="videi">', '  <h2 id="videi">🎬 Videi za navdih</h2>']
    if vids:
        parts.append('  <div class="video-grid">')
        for v in vids[:6]:
            vid = esc(v["id"])
            title = esc(v.get("title", "YouTube video"))
            channel = esc(v.get("channel", ""))
            cap = f"{title}" + (f" · {channel}" if channel else "")
            if v.get("sight"):
                cap = f"<strong>{esc(v['sight'])}</strong> · " + cap
            parts.append("    <figure>")
            parts.append(f'      <!-- Video zamenjaš tako, da spremeniš kodo za "embed/" v spodnji vrstici -->')
            parts.append(
                f'      <iframe class="video-frame" src="https://www.youtube-nocookie.com/embed/{vid}" '
                f'title="{title}" loading="lazy" allowfullscreen '
                f'allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe>'
            )
            parts.append(f"      <figcaption>{cap}</figcaption>")
            parts.append("    </figure>")
        parts.append("  </div>")
    else:
        parts.append('  <p>Videe za ta kraj dodamo v kratkem. Do takrat si jih lahko ogledate prek spodnjih povezav. 🙂</p>')
    links = " · ".join(
        f'<a href="{yt_search_url(p)}" target="_blank" rel="noopener">»{esc(p)}«</a>' for p in loc["phrases"]
    )
    parts.append(f'  <p class="video-more">Več videov na YouTube: {links}</p>')
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def location_page(i, loc):
    prev_loc = LOCATIONS[i - 1] if i > 0 else None
    next_loc = LOCATIONS[i + 1] if i < len(LOCATIONS) - 1 else None

    g = GUIDE.get(loc["key"], {})
    kicker = f"Postaja {i + 1} od {len(LOCATIONS)}"
    lbl = stop_label(loc)
    if lbl:
        kicker += f" · {lbl}"

    out = head(TXT["loc_title"].format(name=loc["name"]),
               TXT["loc_desc"].format(name=loc["name"]),
               with_map=True, with_album=True)
    out += nav(loc["key"])
    out += "<main>\n"

    out += f"""<section class="loc-hero">
  {banner_html(loc['key'], art.location_scene(loc['key']), loc['name'])}
  <p class="kicker">{loc['emoji']} {kicker}</p>
  <h1>{esc(loc['name'])}</h1>
  <p class="loc-sub">{esc(loc['sub'])}</p>
  <p class="loc-intro">{esc(loc['intro'])}</p>
  <p class="visit-wrap"><button type="button" class="visit-btn" data-visit="{loc['key']}">☐ Označi kot obiskano</button></p>
</section>
"""

    if g.get("sights"):
        out += sights_section(g)
    else:
        out += '<section class="card-section" aria-labelledby="poceti">\n  <h2 id="poceti">🚶‍♀️ Kaj je dobro početi tukaj</h2>\n  <ul class="nice-list">\n'
        for name, desc in loc["acts"]:
            out += f"    <li><strong>{esc(name)}</strong> — {esc(desc)}</li>\n"
        out += "  </ul>\n</section>\n"

    out += map_section(loc["key"])
    out += day_plan_section(g)
    out += izzivi_section(loc["key"])
    out += food_section(loc, g)
    out += practical_section(g)
    out += stay_section(loc["key"])
    out += book_section(loc["key"])

    out += f"""<section class="card-section fact-section" aria-labelledby="zanimivost">
  <h2 id="zanimivost">💡 Zanimivost</h2>
  <p>{esc(loc['fact'])}</p>
</section>
<section class="card-section magda-section" aria-labelledby="magda">
  <h2 id="magda">{TXT["magda"]}</h2>
  <p>{esc(loc['magda'])}</p>
</section>
"""

    out += rubric_section(loc["key"])

    out += videos_section(loc)

    out += '<div class="back-row"><a class="back-button" href="index.html">🏠 Nazaj na pregled</a></div>\n'
    out += '<nav class="pager" aria-label="Prejšnja in naslednja postaja">\n'
    if prev_loc:
        out += (f'  <a class="prev" href="{prev_loc["key"]}.html"><span class="pager-label">← Prejšnja postaja</span>'
                f'{prev_loc["emoji"]} {esc(prev_loc["name"])}</a>\n')
    else:
        out += '  <span class="spacer"></span>\n'
    if next_loc:
        out += (f'  <a class="next" href="{next_loc["key"]}.html"><span class="pager-label">Naslednja postaja →</span>'
                f'{next_loc["emoji"]} {esc(next_loc["name"])}</a>\n')
    else:
        out += '  <span class="spacer"></span>\n'
    out += "</nav>\n</main>\n"
    out += FOOTER
    return out


NASVETI = [
    ("♨️ Onsen bonton", [
        ("Najprej umivanje", "pred vstopom v vodo se vedno temeljito umijete sede pri tuših — šele čiste stopite v bazen"),
        ("Brez kopalk", "v onsen se gre brez kopalk; majhno brisačko lahko nesete s seboj, a je nikoli ne namočite v vodo"),
        ("Speti lasje", "daljše lase spnite, da se ne dotikajo vode"),
        ("Počasi in tiho", "onsen je prostor miru — tihi pogovori so v redu, čofotanje ne"),
        ("Pijte vodo", "pred kopanjem in po njem popijte kozarec vode; vroča voda kar pošteno »vzame«"),
    ]),
    ("🙏 Splošni bonton", [
        ("Čevlji", "kjer je pred vhodom stopnička in copati, se sezujete — v ryokanih, templjih in mnogih restavracijah"),
        ("Napitnin ni", "na Japonskem se napitnin ne daje — hvaležnost pokažete z nasmehom in »gochisosama deshita« po jedi"),
        ("Tišina na vlakih", "na vlakih se govori tiho, telefoni so na tiho in klicev ni"),
        ("Smeti", "javnih košev skoraj ni — imejte s seboj vrečko in smeti odnesite do nastanitve"),
        ("Vrsta", "Japonci se povsod mirno postavijo v vrsto — na peronu, pred restavracijo, na avtobusu"),
    ]),
    ("⛩️ V templju in svetišču", [
        ("Pred vhodom", "pri torijih se rahlo priklonite; po sredini poti hodijo bogovi, zato stopajte malce ob strani"),
        ("Očiščenje", "pri kamnitem koritu (temizuya) si z zajemalko sperite roke, preden vstopite"),
        ("Fotografiranje", "spoštujte napise — ponekod fotografiranje ni dovoljeno, zlasti v notranjosti"),
        ("Tišina", "govorite tiho; to so kraji molitve in miru, ne le znamenitosti"),
    ]),
]

FRAZE = [
    ("Dober dan", "Konnichiwa", "kon-ni-či-va", "こんにちは"),
    ("Dobro jutro", "Ohayō gozaimasu", "o-ha-jo go-zai-mas", "おはようございます"),
    ("Dober večer", "Konbanwa", "kon-ban-va", "こんばんは"),
    ("Hvala lepa", "Arigatō gozaimasu", "a-ri-ga-to go-zai-mas", "ありがとうございます"),
    ("Prosim", "Onegai shimasu", "o-ne-gai ši-mas", "お願いします"),
    ("Oprostite", "Sumimasen", "su-mi-ma-sen", "すみません"),
    ("Da / Ne", "Hai / Iie", "haj / i-je", "はい、いいえ"),
    ("Koliko stane?", "Ikura desu ka?", "i-ku-ra des ka", "いくらですか"),
    ("Račun, prosim", "Okaikei onegai shimasu", "o-kai-kej o-ne-gai ši-mas", "お会計お願いします"),
    ("Kje je stranišče?", "Toire wa doko desu ka?", "to-i-re va do-ko des ka", "トイレはどこですか"),
    ("Zelo okusno!", "Oishii!", "oj-ši", "おいしい"),
    ("Dober tek (pred jedjo)", "Itadakimasu", "i-ta-da-ki-mas", "いただきます"),
    ("Hvala za pogostitev (po jedi)", "Gochisōsama deshita", "go-či-so-sa-ma deš-ta", "ごちそうさまでした"),
    ("Na zdravje!", "Kanpai!", "kan-paj", "乾杯"),
    ("Ne razumem", "Wakarimasen", "va-ka-ri-ma-sen", "わかりません"),
    ("Nasvidenje", "Sayōnara", "sa-jo-na-ra", "さようなら"),
]

# Kartice »pokaži domačinu«: (emoji, slovensko, japonsko, romaji)
SHOW_CARDS = [
    ("🥬", "Smo vegetarijanke", "私たちはベジタリアンです。肉、魚、かつおだしは食べられません。",
     "Watashitachi wa bejitarian desu. Niku, sakana, katsuo-dashi wa taberaremasen."),
    ("🍽️", "Ali je v tem meso ali riba?", "この料理に肉や魚は入っていますか？",
     "Kono ryōri ni niku ya sakana wa haitte imasu ka?"),
    ("🚄", "Ali ta vlak pelje v …? (pokažite ime kraja)", "この電車は＿＿＿に行きますか？",
     "Kono densha wa ___ ni ikimasu ka?"),
    ("🔢", "Kateri peron?", "何番線ですか？", "Nan-ban-sen desu ka?"),
    ("💳", "Ali lahko plačam s kartico?", "カードは使えますか？", "Kādo wa tsukaemasu ka?"),
    ("🧾", "Račun, prosim", "お会計をお願いします。", "Okaikei o onegai shimasu."),
    ("💧", "Vodo, prosim", "お水をください。", "Omizu o kudasai."),
    ("🚻", "Kje je stranišče?", "トイレはどこですか？", "Toire wa doko desu ka?"),
    ("🗺️", "Pokažite mi na zemljevidu, prosim", "地図で教えてください。", "Chizu de oshiete kudasai."),
    ("🗣️", "Ne govorim japonsko. Ali razumete angleško?", "日本語は話せません。英語は分かりますか？",
     "Nihongo wa hanasemasen. Eigo wa wakarimasu ka?"),
    ("📦", "Kovčke bi poslala v naslednji hotel", "荷物を次のホテルに送りたいです。",
     "Nimotsu o tsugi no hoteru ni okuritai desu."),
]

# Alergije: (slovensko, japonska beseda)
ALERGENI = [
    ("Oreščke", "ナッツ"), ("Jajca", "卵"), ("Mleko in mlečne izdelke", "乳製品"),
    ("Pšenico (gluten)", "小麦"), ("Sojo", "大豆"), ("Ribe", "魚"),
    ("Rake in školjke", "甲殻類・貝類"), ("Sezam", "ごま"),
]

# Nujne kartice (stran Nujno)
NUJNO_CARDS = [
    ("🆘", "Pomagajte mi, prosim", "助けてください！", "Tasukete kudasai!"),
    ("🚑", "Poklicite rešilca", "救急車を呼んでください。", "Kyūkyūsha o yonde kudasai."),
    ("👩‍⚕️", "Potrebujem zdravnika", "医者が必要です。", "Isha ga hitsuyō desu."),
    ("👮", "Poklicite policijo", "警察を呼んでください。", "Keisatsu o yonde kudasai."),
    ("🛂", "Izgubila sem potni list", "パスポートをなくしました。", "Pasupōto o nakushimashita."),
    ("📱", "Izgubila sem telefon ali denarnico", "携帯電話か財布をなくしました。",
     "Keitai denwa ka saifu o nakushimashita."),
]


def _show_card(e, sl, jp, ro, cls=""):
    return (f'<button type="button" class="show-card {cls}" data-sl="{esc(sl)}" data-jp="{esc(jp)}" '
            f'data-ro="{esc(ro)}"><span class="sc-emoji" aria-hidden="true">{e}</span>'
            f'<span class="sc-sl">{esc(sl)}</span><span class="sc-jp" lang="ja">{esc(jp)}</span></button>')


def nasveti_page():
    out = head("Nasveti, fraze in kartice · Japonska 2026",
               "Kartice za pokazati domačinom, japonske fraze z izgovorjavo, onsen bonton in praktični nasveti.")
    out += nav("nasveti")
    out += "<main>\n"
    out += _page_hero("💡", "Za vsak dan potovanja", "Nasveti, fraze in kartice",
                      "Pokažite zaslon domačinu — ni treba nič govoriti")
    out += '<nav class="chip-row" aria-label="Vsebina">\n'
    for href, lab in [("#kartice", "🪪 Kartice"), ("#alergije", "⚠️ Alergije"),
                      ("#fraze", "🗣️ Fraze"), ("#bonton", "🙏 Bonton")]:
        out += f'  <a class="chip" href="{href}">{lab}</a>\n'
    out += "</nav>\n"

    out += '<section class="card-section" id="kartice" aria-labelledby="kartice-h">\n'
    out += '  <h2 id="kartice-h">🪪 Pokaži domačinu</h2>\n'
    out += '  <p class="cat-intro">Tapnite kartico — odpre se čez cel zaslon z velikim japonskim besedilom. Pokažite telefon natakarju, osebju na postaji ali v hotelu.</p>\n'
    out += '  <div class="show-grid">\n'
    for e, sl, jp, ro in SHOW_CARDS:
        out += "    " + _show_card(e, sl, jp, ro) + "\n"
    out += "  </div>\n</section>\n"

    out += '<section class="card-section" id="alergije" aria-labelledby="alergije-h">\n'
    out += '  <h2 id="alergije-h">⚠️ Imam alergijo na …</h2>\n'
    out += '  <p class="cat-intro">Izberite, na kaj ste alergične — prikaže se poln stavek v japonščini.</p>\n'
    out += '  <div class="allergy-chips">\n'
    for sl, jp in ALERGENI:
        full = f"私は{jp}にアレルギーがあります。"
        ro = "Watashi wa ___ ni arerugī ga arimasu."
        out += "    " + _show_card("⚠️", f"Imam alergijo na: {sl.lower()}", full, ro, "chip-card") + "\n"
    out += "  </div>\n</section>\n"

    out += '<section class="card-section" id="fraze" aria-labelledby="fraze-h">\n  <h2 id="fraze-h">🗣️ Uporabne japonske fraze</h2>\n'
    out += '  <p class="cat-intro">Tapnite 🔊 in telefon izgovori frazo po japonsko.</p>\n  <ul class="phrase-list">\n'
    for sl, ro, izg, kana in FRAZE:
        out += (f'    <li><span class="sl">{esc(sl)}</span>'
                f'<span class="jp">{esc(ro)}</span>'
                f'<span class="kana" lang="ja">{esc(kana)}</span>'
                f'<span class="izg">({esc(izg)})</span>'
                f'<button type="button" class="say" data-say="{esc(kana)}" aria-label="Poslušaj izgovorjavo">🔊</button></li>\n')
    out += "  </ul>\n</section>\n"

    out += '<h2 class="chapter-title" id="bonton">🙏 Bonton</h2>\n'
    for title, items in NASVETI:
        sec_id = title.split(" ", 1)[1].lower().replace(" ", "-")
        out += f'<section class="card-section" aria-labelledby="{esc(sec_id)}">\n  <h2 id="{esc(sec_id)}">{esc(title)}</h2>\n  <ul class="nice-list">\n'
        for name, desc in items:
            out += f"    <li><strong>{esc(name)}</strong> — {esc(desc)}</li>\n"
        out += "  </ul>\n</section>\n"
    out += '<div class="back-row"><a class="back-button" href="nujno.html">🆘 Nujne informacije</a></div>\n'
    out += "</main>\n"
    out += FOOTER
    return out


NUJNO_CALLS_HTML = """<section class="card-section nujno-calls" aria-labelledby="klic">
  <h2 id="klic">📞 Takoj pokliči</h2>
  <div class="call-grid">
    <a class="call-btn call-red" href="tel:110"><span class="c-num">110</span><span class="c-lbl">Policija</span></a>
    <a class="call-btn call-red" href="tel:119"><span class="c-num">119</span><span class="c-lbl">Rešilec in gasilci</span></a>
    <a class="call-btn" href="tel:+81-50-3816-2787"><span class="c-num">050-3816-2787</span><span class="c-lbl">Japan Visitor Hotline<br><small>24 ur na dan, angleško</small></span></a>
    <a class="call-btn" href="tel:+81355706275"><span class="c-num">+81 3 5570 6275</span><span class="c-lbl">Veleposlaništvo RS v Tokiu</span></a>
  </div>
  <p class="fine-note">Na 119 povejte »Kyūkyū desu« (rešilec) ali »Kaji desu« (požar), nato naslov ali bližnji znak. Evropska številka 112 na Japonskem ni uradna številka — kličite 110 ali 119. Za Japan Visitor Hotline iz tujine: +81-50-3816-2787.</p>
</section>
"""

NUJNO_EMBASSY_HTML = """<section class="card-section" aria-labelledby="ambasada">
  <h2 id="ambasada">🇸🇮 Veleposlaništvo Republike Slovenije v Tokiu</h2>
  <p class="addr">7 Chome-14-12 Minamiaoyama, Minato-ku, Tokyo 107-0062<br>Telefon: <a href="tel:+81355706275">+81 3 5570 6275</a></p>
  <a class="pin-btn" href="https://www.google.com/maps/search/?api=1&query=Embassy%20of%20Slovenia%2C%20Minamiaoyama%2C%20Minato%2C%20Tokyo" target="_blank" rel="noopener">📍 Pokaži na zemljevidu</a>
  <p class="fine-note">Veleposlaništvo pomaga ob izgubi ali tatvini potnega lista in v hudih težavah. Pred odhodom preverite, ali so podatki še aktualni (gov.si → Japonska → predstavništva).</p>
</section>
"""

NUJNO_NOTES_HTML = """<section class="card-section" aria-labelledby="zapiski">
  <h2 id="zapiski">📝 Moje številke (shranjeno samo v tem telefonu)</h2>
  <p class="cat-intro">Zapišite si, kar bi rade imele pri roki: zavarovalna asistenca in številka police, banka (blokada kartice), naslov hotela.</p>
  <textarea class="notes-box" data-save="nujno-zapiski" rows="7" placeholder="npr.
Zavarovanje: tel … / polica …
Banka: blokada kartice …
Hotel (naslov in tel.): …"></textarea>
</section>
"""

NUJNO_STEPS = [
    ("💳", "Izgubljena ali ukradena kartica",
     "Takoj jo zamrznite v aplikaciji banke ali Revoluta (»Freeze«). Nato pokličite številko za blokado, ki jo imate shranjeno. Gotovino in drugo kartico imejte vedno ločeno."),
    ("📱", "Izgubljen ali ukraden telefon",
     "Z druge naprave poiščite telefon (Najdi / Najdi napravo) in ga zaklenite. Blokirajte SIM pri operaterju, spremenite gesla in prijavite izgubo na policijski postaji (koban) — dobite potrdilo za zavarovanje."),
    ("🛂", "Izgubljen potni list",
     "Prijavite izgubo policiji (koban) in zahtevajte potrdilo. Nato pokličite veleposlaništvo RS v Tokiu. Fotografijo potnega lista imejte vedno v telefonu."),
    ("🏥", "Zdravstvene težave",
     "Pokličite 119 (rešilec) ali prosite recepcijo hotela za pomoč pri iskanju zdravnika. Pokličite zavarovalno asistenco in shranite vse račune. Japan Visitor Hotline pomaga v angleščini."),
    ("🌏", "Potres",
     "Ostanite mirne, zaščitite glavo (pod mizo ali ob steno), izogibajte se steklu in sledite navodilom osebja. Ob obali ob opozorilu na cunami takoj na višje. Naložite aplikacijo »Safety tips« (JNTO) — opozorila v več jezikih."),
    ("🧳", "Izgubljena stvar",
     "Vprašajte osebje na postaji ali v taksi podjetju, nato koban. Japonska je znana po vračanju izgubljenih stvari — pogosto se najdejo."),
]


def nujno_page():
    out = head("Nujno · Japonska — Mesec za dušo",
               "Nujne številke, veleposlaništvo, kaj storiti ob izgubi kartice ali telefona, in kartice za pomoč v japonščini.")
    out += nav("nujno")
    out += "<main>\n"
    out += _page_hero("🆘", "Mir v žepu", "Nujne informacije",
                      "Upamo, da je ne boste potrebovale — a dobro je, da je tu")
    out += NUJNO_CALLS_HTML
    out += NUJNO_EMBASSY_HTML

    out += '<section class="card-section" aria-labelledby="tezava">\n  <h2 id="tezava">🧭 Kaj storiti ob težavi</h2>\n'
    for e, h, t in NUJNO_STEPS:
        out += (f'  <details class="step-box"><summary><span class="sb-e">{e}</span>{esc(h)}</summary>'
                f'<p>{esc(t)}</p></details>\n')
    out += "</section>\n"

    out += '<section class="card-section" aria-labelledby="povej">\n  <h2 id="povej">🗣️ Povej po japonsko (pokaži zaslon)</h2>\n  <div class="show-grid">\n'
    for e, sl, jp, ro in NUJNO_CARDS:
        out += "    " + _show_card(e, sl, jp, ro, "red") + "\n"
    out += "  </div>\n</section>\n"

    out += NUJNO_NOTES_HTML
    out += '<div class="back-row"><a class="back-button" href="index.html">🏠 Nazaj na pregled</a></div>\n'
    out += "</main>\n" + FOOTER
    return out


def _page_hero(emoji, kicker, title, subtitle, photo_key=None):
    banner = ""
    if photo_key and photo_for(photo_key):
        banner = "  " + banner_html(photo_key, "", title) + "\n"
    return f"""<section class="loc-hero">
{banner}  <div class="loc-emoji" aria-hidden="true">{emoji}</div>
  <p class="kicker">{esc(kicker)}</p>
  <h1>{esc(title)}</h1>
  <p class="loc-sub">{esc(subtitle)}</p>
</section>
"""


def practical_block(data):
    """En razdelek praktičnega poglavja (PRACTICAL[key])."""
    out = ""
    if data.get("intro"):
        out += f'<p class="intro-note">{esc(data["intro"])}</p>\n'
    for sec in data.get("sections", []):
        sid = esc(sec["heading"].lower().replace(" ", "-"))
        out += f'<section class="card-section" aria-labelledby="{sid}">\n'
        out += f'  <h2 id="{sid}">{sec.get("emoji", "")} {esc(sec["heading"])}</h2>\n'
        out += '  <ul class="nice-list">\n'
        for it in sec.get("items", []):
            out += f'    <li><strong>{esc(it["name"])}</strong> — {esc(it["text"])}</li>\n'
        out += "  </ul>\n</section>\n"
    return out


def _leg_links(lg):
    items = LEG_LINKS.get((lg["from"], lg["to"]))
    if not items:
        return ""
    return ('    <div class="buy-row">' + "".join(_btn(esc(lbl), url, "buy-btn alt") for lbl, url in items) + "</div>\n")


def nacrt_page():
    it = ITINERARY
    out = head(TXT["nacrt_title"], TXT["nacrt_desc"])
    out += nav("nacrt")
    out += "<main>\n"
    out += _page_hero(*TXT["nacrt_hero"])
    out += '<section class="today-card" id="today" hidden aria-live="polite"></section>\n'
    out += trip_script()
    if it.get("intro"):
        out += f'<p class="intro-note">{esc(it["intro"])}</p>\n'

    # dnevi, grupirani po regiji
    out += '<section class="card-section" aria-labelledby="dnevi">\n  <h2 id="dnevi">📅 Dan za dnem</h2>\n'
    out += '  <ol class="itinerary">\n'
    prev_region = None
    for d in it.get("days", []):
        new = d["region"] != prev_region
        prev_region = d["region"]
        reg = f'<span class="it-region">{esc(d["region"])}</span>' if new else ""
        out += (f'    <li class="it-day{" it-new" if new else ""}" data-iso="{day_iso(d["day"])}">\n'
                f'      <span class="it-num"><span class="it-daynum">Dan {d["day"]}</span>'
                f'<span class="it-date">{esc(d["date"])}</span></span>\n'
                f'      <span class="it-body">{reg}<strong>{esc(d["title"])}</strong>'
                f'<span class="it-plan">{esc(d["plan"])}</span></span>\n'
                f'    </li>\n')
    out += "  </ol>\n</section>\n"

    # prehodi
    legs = it.get("legs", [])
    if legs:
        out += '<section class="card-section" aria-labelledby="prehodi">\n  <h2 id="prehodi">🚉 Prehodi med kraji</h2>\n'
        out += '  <p class="cat-intro">Okvirni prevozi in časi — točne vozne rede preverite bliže odhodu.</p>\n'
        for lg in legs:
            out += ('  <div class="leg">\n'
                    f'    <div class="leg-head"><strong>{esc(lg["from"])}</strong> <span class="leg-arrow">→</span> <strong>{esc(lg["to"])}</strong>'
                    f'<span class="leg-dur">🕒 {esc(lg["duration"])}</span></div>\n'
                    f'    <p class="leg-how">{esc(lg["how"])}</p>\n'
                    f'    <p class="leg-tip">💡 {esc(lg["tip"])}</p>\n'
                    + _leg_links(lg) +
                    '  </div>\n')
        out += "</section>\n"

    out += '<div class="back-row"><a class="back-button" href="index.html">🏠 Nazaj na pregled</a></div>\n'
    out += "</main>\n" + FOOTER
    return out


CHECKLIST = [
    ("📄 Dokumenti in rezervacije", [
        "Potni list (velja do konca poti) + fotografije/kopije v oblaku",
        "Potovalno zavarovanje in številka za pomoč",
        "Potrdila o nastanitvah, vlakih in delavnicah v telefonu",
        "Vozovnice / rezervacije za daljše etape",
    ]),
    ("💳 Denar", [
        "Nekaj jenov v gotovini za prvi dan",
        "Dve kartici (npr. Revolut + banka), banka obveščena o potovanju",
        "Revolut naložen z evri",
        "Majhna denarnica za kovance",
    ]),
    ("📱 Telefon in elektrika", [
        "eSIM kupljen (aktivacija ob prihodu) ali žepni WiFi",
        "Aplikacije: Google Maps, Prevajalnik (offline japonščina), Japan Travel",
        "Adapterji tip A (2–3) in razdelilka",
        "Powerbank in kabli",
    ]),
    ("🧣 Obleka in obutev", [
        "Oblačila po plasteh za jesen",
        "Toplejša jakna, kapa in šal za gore (Koya-san, Iya)",
        "Zložljiv dežnik",
        "Udobni, prehojeni čevlji (ki se hitro sezuvajo)",
        "Tople nogavice brez lukenj (tatami, templji)",
    ]),
    ("💊 Zdravje in higiena", [
        "Redna zdravila v originalni embalaži (z imenom učinkovine)",
        "Proti prehladu, bolečini in za želodec",
        "Obliži za žulje",
        "Osebna higiena in kar potrebujete čez dan",
    ]),
    ("🎨 Za dušo", [
        "Skicirni blok in svinčniki/barve (za mandale in skice)",
        "Prostor v kovčku za spominke (papir, čaj, keramika)",
        "Knjiga ali dnevnik za večere",
    ]),
    ("🏠 Zadnji dan doma", [
        "Napolnite vse naprave in powerbank",
        "Preverite vremensko napoved in dokončno spakirajte plasti",
        "Shranite vse potrdila tudi brez interneta (posnetki zaslona)",
        "Doma poskrbite za rastline/pošto/ključe",
    ]),
]


def checklist_section():
    parts = ['<h2 class="chapter-title" id="seznam">✅ Kontrolni seznam za odhod</h2>',
             '<p class="chapter-sub">Obkljukajte — telefon si zapomni, kaj je urejeno</p>',
             '<section class="card-section checklist" aria-labelledby="seznam">',
             '  <p class="chk-progress" id="chk-progress" aria-live="polite"></p>']
    n = 0
    for cat, items in CHECKLIST:
        parts.append(f'  <h3 class="chk-cat">{esc(cat)}</h3>')
        parts.append('  <ul class="chk-list">')
        for it in items:
            cid = f"chk-{n}"
            n += 1
            parts.append(f'    <li><label><input type="checkbox" data-persist id="{cid}"> '
                         f'<span>{esc(it)}</span></label></li>')
        parts.append('  </ul>')
    parts.append('  <button type="button" class="chk-reset" id="chk-reset">Počisti vse kljukice</button>')
    parts.append('</section>')
    return "\n".join(parts) + "\n"


def priprave_page():
    out = head("Priprave — Japonska, Mesec za dušo",
               "Praktični vodnik: pred odhodom, denar, vlaki in prevoz, okvirni stroški in kontrolni seznam.")
    out += nav("priprave")
    out += "<main>\n"
    out += _page_hero("🎒", "Da bo vse gladko", "Priprave",
                      "Pred odhodom · denar · vlaki · stroški · seznam", "priprave")
    # hitri skok
    order = ["pred-odhodom", "denar", "prevoz", "stroski"]
    out += '<nav class="chip-row" aria-label="Vsebina">\n'
    for k in order:
        d = PRACTICAL.get(k)
        if d:
            out += f'  <a class="chip" href="#{k}">{d.get("emoji","")} {esc(d["title"])}</a>\n'
    out += '  <a class="chip" href="#povezave">🔗 Kupi in rezerviraj</a>\n'
    out += '  <a class="chip" href="#seznam">✅ Kontrolni seznam</a>\n'
    out += "</nav>\n"
    out += quickbuy_section()
    for k in order:
        d = PRACTICAL.get(k)
        if not d:
            continue
        out += f'<h2 class="chapter-title" id="{k}">{d.get("emoji","")} {esc(d["title"])}</h2>\n'
        out += f'<p class="chapter-sub">{esc(d.get("subtitle",""))}</p>\n'
        out += practical_block(d)
    out += checklist_section()
    out += '<div class="back-row"><a class="back-button" href="nasveti.html">💡 Naprej: bonton in fraze</a></div>\n'
    out += "</main>\n" + FOOTER
    return out


def dozivetja_page():
    dz = DOZIVETJA
    out = head("Doživetja za dušo — Japonska, Mesec za dušo",
               "Kuharske delavnice, čajne hiše, zen vrtovi in ustvarjanje ter nakup po Japonski.")
    out += nav("dozivetja")
    out += "<main>\n"
    out += _page_hero("🎨", "Za dušo in roke", "Doživetja za dušo",
                      "Kuhanje · čaj · zen vrtovi · ustvarjanje", "dozivetja")
    if dz.get("intro"):
        out += f'<p class="intro-note">{esc(dz["intro"])}</p>\n'
    for c in dz.get("categories", []):
        cid = esc(c["name"].lower().replace(" ", "-"))
        out += f'<section class="card-section" aria-labelledby="{cid}">\n'
        out += f'  <h2 id="{cid}">{c.get("emoji","")} {esc(c["name"])}</h2>\n'
        if c.get("intro"):
            out += f'  <p class="cat-intro">{esc(c["intro"])}</p>\n'
        for p in c.get("items", []):
            out += '  <div class="place">\n'
            out += (f'    <div class="place-head"><strong>{esc(p["name"])}</strong>'
                    f'<span class="place-city">{esc(p.get("city",""))}</span></div>\n')
            out += f'    <p>{esc(p["desc"])}</p>\n'
            if p.get("booking"):
                out += f'    <p class="booking">📝 {esc(p["booking"])}</p>\n'
            if p.get("maps"):
                out += f'    <a class="pin-btn" href="{maps_url(p["maps"])}" target="_blank" rel="noopener">📍 Zemljevid</a>\n'
            if DOZ_SEARCH:
                qn = f'{p["name"]} {p.get("city", "")}'.strip()
                out += ('    <div class="buy-row">' + _btn("🔎 Termini (Klook)", L.klook(qn), "buy-btn alt")
                        + _btn("🔎 Termini (GetYourGuide)", L.gyg(qn), "buy-btn alt")
                        + _btn("🔎 Google", L.gsearch(qn + " booking"), "buy-btn alt") + "</div>\n")
            out += "  </div>\n"
        out += "</section>\n"
    out += '<div class="back-row"><a class="back-button" href="index.html">🏠 Nazaj na pregled</a></div>\n'
    out += "</main>\n" + FOOTER
    return out


def _all_challenge_data():
    out = []
    for loc in LOCATIONS:
        out.extend(_challenge_data(loc["key"]))
    return out


def nalozi_page():
    out = head(TXT["nalozi_title"],
               "Naložite fotografije in videe s telefona v skupni album potovanja.",
               with_album=True)
    out += nav("nalozi")
    out += "<main>\n"
    out += _page_hero(*TXT["nalozi_hero"])
    out += f'<p class="intro-note">{TXT["nalozi_note"]}</p>\n'
    out += '<div class="album-gate"></div>\n'
    out += '<section class="card-section album-upload"></section>\n'
    out += f'<h2 class="section-title">{TXT["album_title"]}</h2>\n'
    out += '<div class="album-download"></div>\n'
    out += '<div class="album-gallery"></div>\n'
    out += f'<div class="back-row"><a class="back-button" href="izziv.html">{TXT["izziv_jump"]}</a></div>\n'
    out += "</main>\n" + FOOTER
    return out


def izziv_page():
    data = json.dumps(_all_challenge_data(), ensure_ascii=False)
    out = head(TXT["izziv_title"],
               TXT["izziv_intro_desc"],
               with_album=True)
    out += nav("izziv")
    out += "<main>\n"
    out += _page_hero("📸", *TXT["izziv_hero"])

    how = "".join(f'    <li><span class="how-n">{n}</span><span><strong>{esc(b)}</strong> — {esc(t)}</span></li>\n'
                  for n, (b, t) in enumerate(TXT["izziv_how"], 1))
    out += (f'''<section class="card-section izziv-how" aria-labelledby="kako">
  <h2 id="kako">Kako deluje</h2>
  <ol class="how-steps">
{how}  </ol>
</section>
<section class="card-section izziv-idea" aria-labelledby="ideja">
  <h2 id="ideja">{TXT["izziv_why"]}</h2>
  <p>{TXT["izziv_idea"]}</p>
  <p class="fine">{TXT["izziv_fine"]}</p>
</section>
''')
    out += '<div class="album-gate"></div>\n'
    out += '<section class="izziv-overall" id="izziv-overall"></section>\n'
    out += '<div class="izziv-board izziv-stations" data-scope="all"></div>\n'
    out += ('<section class="card-section izziv-final" id="izziv-final" hidden>'
            f'<h2>{TXT["izziv_final_title"]}</h2>'
            f'<p>{TXT["izziv_final"]}</p>'
            '<p><a class="back-button" href="nalozi.html">⬇️ Pojdi na album</a></p></section>\n')
    out += f'<script type="application/json" id="izziv-data">{data}</script>\n'
    out += '<div class="back-row"><a class="back-button" href="nalozi.html">📤 Naloži fotografije</a></div>\n'
    out += "</main>\n" + FOOTER
    return out


import datetime as _dt

TRIP_START = _dt.date(2026, 11, 3)

REGION_KEY = {
    "Tokio": "tokio", "Chichibu (izlet)": "chichibu", "Fuji – Kawaguchiko": "kawaguchiko",
    "Minobusan": "minobusan", "Izu": "izu", "Kumano Kodo": "kumano", "Koya-san": "koyasan",
    "Iya": "iya", "Ine": "ine", "Kyoto": "kyoto", "Osaka": "osaka",
    "Nara (izlet)": "nara", "Hiroshima (izlet)": "hiroshima", "Odhod": "osaka",
}
DAYTRIP_BASE = {"chichibu": "tokio", "nara": "kyoto", "hiroshima": "osaka"}


def day_iso(day):
    return (TRIP_START + _dt.timedelta(days=int(day) - 1)).isoformat()


def trip_script():
    """JSON z vsemi dnevi poti (za »Danes« in označitev v načrtu)."""
    rows = []
    for d in ITINERARY.get("days", []):
        rows.append({"d": d["day"], "iso": day_iso(d["day"]), "date": d["date"], "r": d["region"],
                     "t": d["title"], "p": d["plan"], "k": REGION_KEY.get(d["region"], "")})
    return ('<script type="application/json" id="trip-data">'
            + json.dumps(rows, ensure_ascii=False) + "</script>\n")


def route_script():
    """JSON s postajami in koordinatami (za pregledni zemljevid poti)."""
    rows = []
    for i, loc in enumerate(LOCATIONS):
        m = MAPS.get(loc["key"])
        if not m:
            continue
        rows.append({"k": loc["key"], "n": loc["nav"], "e": loc["emoji"], "i": i + 1,
                     "lat": m[0], "lon": m[1], "day": bool(loc.get("daytrip")),
                     "base": DAYTRIP_BASE.get(loc["key"], "")})
    return ('<script type="application/json" id="route-data">'
            + json.dumps(rows, ensure_ascii=False) + "</script>\n")


QUICK_LINKS = [
    ("nacrt.html", "🗺️", "Načrt poti", "30 dni, dan za dnem"),
    ("izziv.html", "📸", "Foto izzivi", "52 izzivov in presenečenja"),
    ("nalozi.html", "📤", "Naloži fotografije", "album iz vaših telefonov"),
    ("dozivetja.html", "🎨", "Doživetja", "delavnice, čaj, vrtovi"),
    ("priprave.html", "🎒", "Priprave", "denar, vlaki, pakiranje"),
    ("priprave.html#povezave", "🔗", "Kupi in rezerviraj", "vlaki, nastanitve, vstopnice"),
    ("nacrt.html#prehodi", "🚄", "Prevozi in vozovnice", "povezave za nakup"),
    ("nasveti.html#kartice", "🪪", "Kartice za domačine", "pokažite zaslon"),
    ("nasveti.html#fraze", "🗣️", "Fraze", "z izgovorjavo 🔊"),
    ("prevajalec.html", "🔍", "Prevajalec s kamero", "japonski napis → slovensko"),
    ("nujno.html", "🆘", "Nujno", "110, 119, veleposlaništvo"),
    ("kako.html", "🎓", "Kako uporabljati", "predstavitev vseh funkcij"),
]


def index_page():
    out = head(
        "Japonska — Mesec za dušo",
        "Potovalni vodnik za Magdo in prijateljice: Japonska, 3. november – 2. december 2026, Tokio → Osaka.",
        with_map=True,
    )
    out += nav("index")
    out += "<main>\n"
    out += f"""<section class="hero">
  {banner_html("hero", art.home_scene(), "Japonska — Mesec za dušo", "home-banner")}
  <p class="leaves" aria-hidden="true">🍁 🍂 🍁</p>
  <h1>Japonska<br><span class="h1-sub">Mesec za dušo</span></h1>
  <p class="dates">3. november – 2. december 2026 · Tokio → Osaka</p>
  <p class="tagline">Potovalni vodnik za Marjetico, Heleno, Ljubo in Magdo — vaš žepni spremljevalec: načrt dneva, znamenitosti, hrana, foto izzivi in nujne informacije.</p>
  <a class="photo-button" href="nalozi.html">📸 Naš album — naloži fotografije</a>
</section>
<a class="tour-banner" id="tour-banner" href="kako.html" hidden><span class="tb-e">🎓</span><span class="tb-t"><strong>Prvič tukaj?</strong> Poglej kratko predstavitev (2 minuti) →</span></a>
<section class="today-card" id="today" hidden aria-live="polite"></section>
"""
    out += '<nav class="quick-links" aria-label="Glavna poglavja">\n'
    for href, e, t, d in QUICK_LINKS:
        out += (f'  <a href="{href}"><span class="ql-emoji" aria-hidden="true">{e}</span>'
                f'<span class="ql-t">{esc(t)}</span><span class="ql-d">{esc(d)}</span></a>\n')
    out += "</nav>\n"

    out += """<section class="card-section map-route-sec" aria-labelledby="pot">
  <h2 id="pot">🗺️ Naša pot</h2>
  <div class="route-map" id="route-map" role="img" aria-label="Zemljevid poti po Japonski od Tokia do Osake"></div>
  <p class="map-legend"><span class="lg-line"></span> nočitvene postaje po vrsti &nbsp; <span class="lg-dash"></span> enodnevni izleti. Tapnite številko za vodnik.</p>
  <ol class="route-list">
""" + "\n".join(
        f'    <li><a href="{loc["key"]}.html"><span class="rl-n{" rl-day" if loc.get("daytrip") else ""}">{i + 1}</span>'
        f'<span class="rl-t">{loc["emoji"]} {esc(loc["nav"])}</span></a></li>'
        for i, loc in enumerate(LOCATIONS)) + """
  </ol>
  <p class="visit-sum" id="visit-sum"></p>
</section>
"""
    out += """<section class="welcome card-section" aria-labelledby="welcome">
  <h2 id="welcome">👋 Dobrodošle</h2>
  <p>Pred vami je mesec, kakršnega si privoščimo enkrat v življenju — cel november na Japonskem, v času, ko se javorji obarvajo v najlepše rdeče in zlato. Ta vodnik ni seznam, ki bi ga bilo treba prehiteti; je vaš tihi spremljevalec.</p>
  <p>Potujte počasi. Ena znamenitost dopoldne, ena popoldne, vmes skodelica čaja. Ustavite se, kjer je lepo, in tam ostanite dlje, kot se zdi potrebno. Japonska najlepše nagradi tiste, ki se ji ne mudi.</p>
  <p>Na vsaki postaji boste našle znamenitosti z zemljevidi, kje in kaj jesti, kdaj je kraj najlepši, kje si vzeti uro zase — in prostor za svoje zapiske.</p>
  <p>Čaka vas tudi <strong>52 foto izzivov</strong> z majhnimi presenečenji: naložite sliko s telefona, izziv se opravi, odklene pa se zanimivost, skrivnost ali nagrada. Iz tega bo nastala vaša potopisna knjiga. Marjetica, Helena, Ljuba in Magda: fotoaparati pripravljeni! 🍁</p>
</section>
"""
    out += '<h2 class="section-title">Naše postaje</h2>\n<ul class="cards">\n'
    for i, loc in enumerate(LOCATIONS):
        stop = f"Postaja {i + 1}"
        lbl = stop_label(loc)
        if lbl:
            stop += f" · {lbl}"
        out += f"""  <li>
    <a href="{loc['key']}.html">
      <span class="card-scene">{card_media(loc['key'], art.location_scene(loc['key']))}</span>
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
    out += """<div class="back-row">
  <a class="back-button" href="nujno.html">🆘 Nujne informacije</a>
</div>
"""
    out += trip_script() + route_script()
    out += "</main>\n"
    out += FOOTER
    return out


def _wiz_steps():
    """Koraki wizarda: (emoji, naslov, [odstavki], demo_html, (href, oznaka) ali None, spot_selector)."""
    demo_menu = ('<div class="demo-bar"><span>🍁 Mesec za dušo</span><span class="demo-pill">☰ Meni</span></div>'
                 '<ul class="demo-list"><li>🏠 Domov</li><li>🗺️ Načrt poti</li><li>📸 Izzivi</li>'
                 '<li>📤 Naloži fotografije</li><li>🆘 Nujno</li><li class="demo-more">… in vseh 13 postaj</li></ul>')
    demo_today = ('<div class="today-card demo-today"><div class="today-kicker">📅 Danes · 9. nov</div>'
                  '<h2>Dan 7 od 30 — Na polotok Izu</h2><p class="today-region">Izu</p>'
                  '<p>Jutranja molitev, nato proti morju. Zvečer prvi onsen z razgledom.</p></div>')
    demo_station = ('<div class="demo-chips"><span>⛩️ Znamenitosti</span><span>📍 Zemljevid</span><span>🎬 Videi</span>'
                    '<span>🍜 Hrana</span><span>🗓️ Predlog dneva</span><span>🏡 Kje prespati</span>'
                    '<span>☔ Če dežuje</span><span>🍁 Najlepši trenutek</span><span>☕ Ura zase</span>'
                    '<span>🎨 Mandala</span><span>📖 Dnevnik</span><span>📸 Izzivi</span></div>')
    demo_food = ('<details class="food-cat" open><summary><span class="cat-emoji" aria-hidden="true">🍣</span>'
                 '<span class="cat-name">Sushi in sveže ribe</span><span class="cat-count">3 predlogi</span>'
                 '<span class="chev" aria-hidden="true">▶</span></summary><div class="cat-body">'
                 '<div class="place"><div class="place-head"><strong>Primer restavracije</strong><span class="price">€€</span></div>'
                 '<p>Kaj naročiti in zakaj je lokal poseben.</p><span class="pin-btn">📍 Zemljevid</span></div></div></details>'
                 '<p class="demo-hint">Tapnite naslov kategorije, da jo odprete ali zaprete.</p>')
    demo_izziv = ('<div class="demo-izziv" data-demo="unlock">'
                  '<div class="izziv-head"><span class="izziv-mark demo-mark">📸</span>'
                  '<span class="izziv-text">Vse štiri pod velikimi torii svetišča Meiji Jingu.</span></div>'
                  '<div class="izziv-surprise locked demo-locked"><span class="sur-ic">🎁</span>'
                  '<span>Presenečenje te čaka — odklene se, ko naložite sliko ali video.</span></div>'
                  '<div class="izziv-surprise open demo-open" hidden><div class="sur-head"><span class="sur-ic">💡</span>'
                  '<span><span class="sur-kind">Zanimivost odklenjena</span><strong>Gozd, ki ga je zasadil človek</strong></span></div>'
                  '<p>Gozd Meiji Jingu ni naraven: zasadili so ga okoli 1915–1920, danes je videti kot pragozd.</p></div>'
                  '<button type="button" class="pin-btn demo-btn">▶ Preizkusi: naloži sliko</button></div>')
    demo_upload = ('<div class="gate-row"><span class="gate-lbl">Nalagaš kot:</span>'
                   '<span class="gate-name">Marjetica</span><span class="gate-name on">Helena</span>'
                   '<span class="gate-name">Ljuba</span><span class="gate-name">Magda</span></div>'
                   '<div class="demo-upload"><span class="demo-select">🗼 Tokio ▾</span>'
                   '<span class="demo-bigbtn">📷 Izberi fotografije ali video</span></div>')
    demo_cards = ('<button type="button" class="show-card" data-sl="Smo vegetarijanke" '
                  'data-jp="私たちはベジタリアンです。肉、魚、かつおだしは食べられません。" '
                  'data-ro="Watashitachi wa bejitarian desu. Niku, sakana, katsuo-dashi wa taberaremasen.">'
                  '<span class="sc-emoji" aria-hidden="true">🥬</span><span class="sc-sl">Smo vegetarijanke</span>'
                  '<span class="sc-jp" lang="ja">私たちはベジタリアンです。</span></button>'
                  '<p class="demo-hint">Poskusite: tapnite kartico zgoraj.</p>')
    demo_nujno = ('<div class="call-grid demo-calls"><div class="call-btn call-red"><span class="c-num">110</span><span class="c-lbl">Policija</span></div>'
                  '<div class="call-btn call-red"><span class="c-num">119</span><span class="c-lbl">Rešilec</span></div></div>')
    demo_lens = ('<div class="demo-lens"><div class="demo-lens-cam"><span>出口</span><span>営業時間 9:00〜17:00</span></div>'
                 '<div class="demo-lens-arrow">⬇</div><div class="demo-lens-out">Izhod<br>Delovni čas 9.00–17.00</div></div>')
    demo_install = ('<div class="demo-install"><div><strong>🍎 iPhone (Safari)</strong><br>Deli ⬆️ → »Dodaj na začetni zaslon«</div>'
                    '<div><strong>🤖 Android (Chrome)</strong><br>Meni ⋮ → »Dodaj na začetni zaslon«</div></div>')

    return [
        ("🍁", "Dobrodošle!", [
            "To je vaš žepni vodnik za potovanje po Japonski (3. november – 2. december 2026): načrt dneva, znamenitosti, hrana, foto izzivi in nujne informacije.",
            "Predstavitev traja približno dve minuti. Tapnite »Naprej« in videle boste vse, kar zna ta stran."], "", None, ""),
        ("☰", "Meni — vse na enem mestu", [
            "Gumb »Meni« zgoraj desno odpre pregleden meni: glavne strani in vseh 13 postaj. Je na vsaki strani."],
         demo_menu, None, ".menu-toggle"),
        ("📅", "Danes — kaj je na vrsti", [
            "Med potovanjem domača stran sama pokaže, kateri dan poti je danes: kje ste, kaj je v načrtu, in bližnjice do vodnika, izzivov in nujnih informacij.",
            "Pred odhodom kaže odštevanje, po potovanju pa pozdrav."], demo_today, None, ""),
        ("🗺️", "Načrt poti in pregledni zemljevid", [
            "Načrt poti ima vseh 30 dni z datumi in prehode med kraji (vlak, avtobus, kovčki). Današnji dan je označen.",
            "Na domači strani je zemljevid cele poti s 13 postajami po vrsti — nočitve in enodnevni izleti."],
         "", ("nacrt.html", "Odpri načrt poti →"), ""),
        ("⛩️", "Postaje — celoten vodnik za vsak kraj", [
            "Vsaka postaja ima znamenitosti z zemljevidom in videi, hrano, predlog dneva, nasvet kje prespati in kaj početi ob dežju, pa tudi osebne rubrike: najlepši trenutek dneva, ura zase in navdih za mandalo."],
         demo_station, ("tokio.html", "Poglej primer: Tokio →"), ""),
        ("🍜", "Hrana po kategorijah", [
            "Hrana je razdeljena po kategorijah (sushi, rezanci, sladice …). Kategorijo odprete s tapom in dobite restavracije s ceno in pinom na zemljevidu."],
         demo_food, None, ""),
        ("✅", "Obiskano", [
            "Na vsaki postaji je gumb »Označi kot obiskano«. Kar označite, ostane shranjeno v vašem telefonu, na domači strani pa se pokaže, koliko postaj ste že obiskale."],
         "", None, ""),
        ("📸", "Foto izzivi in presenečenja", [
            "Za vsako postajo je nekaj foto izzivov — večinoma slike, kjer vas ujame ena od vas. Pod vsakim je »drobni tisk«: zakaj se slikate tam.",
            "Ko za izziv naložite sliko, se opravi, pade na dno razdelka in odklene presenečenje: zanimivost, skrivnost ali majhna nagrada. Preizkusite spodaj!"],
         demo_izziv, ("izziv.html", "Odpri vse izzive →"), ""),
        ("📤", "Naloži fotografije", [
            "Fotografije in videe naložite kar s telefona. Prvič vnesete skupno kodo (jo imate v sporočilu) in izberete, kdo ste. Nato izberete postajo in slike.",
            "Vse pristane v skupnem albumu, ki ga vidite vse štiri. Na koncu potovanja ga z enim klikom prenesete kot .zip."],
         demo_upload, ("nalozi.html", "Odpri album →"), ""),
        ("🪪", "Kartice za domačine", [
            "Kartice »Smo vegetarijanke«, »Imam alergijo na …«, »Kateri peron?« in druge odprejo velik japonski zapis čez cel zaslon. Pokažete telefon, ni treba nič govoriti."],
         demo_cards, ("nasveti.html#kartice", "Vse kartice →"), ""),
        ("🔊", "Japonske fraze z izgovorjavo", [
            "Pri frazah je gumb 🔊: telefon jo izgovori po japonsko. Zraven so japonski zapis, izgovorjava po slovensko in pomen."],
         "", ("nasveti.html#fraze", "Odpri fraze →"), ""),
        ("🔍", "Prevajalec s kamero", [
            "Kot Google Lens: odprete kamero, napis postavite v okvir in tapnete »Prevedi«. Telefon prebere japonsko besedilo in ga prevede v slovenščino (ali angleščino).",
            "Prepoznano besedilo lahko popravite, poslušate ali pokažete večje. Dobro deluje pri tablah, jedilnikih in vozovnicah."],
         demo_lens, ("prevajalec.html", "Odpri prevajalec →"), ""),
        ("🆘", "Nujno — mir v žepu", [
            "Posebna stran s 110, 119, številko Japan Visitor Hotline, veleposlaništvom RS v Tokiu in koraki ob izgubi kartice, telefona ali potnega lista. Upamo, da je ne boste potrebovale."],
         demo_nujno, ("nujno.html", "Odpri nujne informacije →"), ""),
        ("🎒", "Priprave in doživetja", [
            "Priprave: pakiranje, eSIM, denar, vlaki, okvirni stroški in kontrolni seznam za odhod (obkljukate, telefon si zapomni).",
            "Doživetja: kuharske delavnice, čajne hiše, zen vrtovi in nakup za ustvarjalne duše."],
         "", ("priprave.html", "Odpri priprave →"), ""),
        ("📲", "Dodajte stran na domači zaslon", [
            "Da bo stran kot prava aplikacija (ikona na zaslonu, odpira se čez cel zaslon). Ob prvem odprtju z domačega zaslona boste kodo vnesle še enkrat."],
         demo_install, None, ""),
        ("🌸", "Pripravljene!", [
            "To je vse. Stran lahko to predstavitev kadar koli ponovite — v meniju poiščite »Kako uporabljati«. Lepo pot, Marjetica, Helena, Ljuba in Magda!"],
         "", ("index.html", "Na domačo stran →"), ""),
    ]


def kako_page():
    steps = _wiz_steps()
    out = head(TXT["kako_title"],
               "Kratka predstavitev vseh funkcij vodnika: korak za korakom z demo primeri.",
               with_album=False)
    out += nav("kako")
    out += "<main>\n"
    out += '<section class="wiz" id="wiz" aria-label="Predstavitev">\n'
    out += ('  <div class="wiz-top"><span class="wiz-count" id="wiz-count"></span>'
            '<a class="wiz-skip" href="index.html">Preskoči →</a></div>\n'
            '  <div class="wiz-bar"><i id="wiz-fill"></i></div>\n  <div class="wiz-stage">\n')
    for i, (e, t, paras, demo, link, spot) in enumerate(steps):
        out += f'    <article class="wiz-step" data-spot="{esc(spot)}"{" hidden" if i else ""}>\n'
        out += f'      <div class="wiz-emoji" aria-hidden="true">{e}</div>\n      <h2>{esc(t)}</h2>\n'
        for ptxt in paras:
            out += f'      <p>{esc(ptxt)}</p>\n'
        if demo:
            out += f'      <div class="wiz-demo">{demo}</div>\n'
        if link:
            out += f'      <a class="wiz-link" href="{link[0]}">{esc(link[1])}</a>\n'
        out += "    </article>\n"
    out += '  </div>\n'
    out += ('  <div class="wiz-nav"><button type="button" class="wiz-btn wiz-prev" id="wiz-prev">← Nazaj</button>'
            '<div class="wiz-dots" id="wiz-dots" aria-hidden="true"></div>'
            '<button type="button" class="wiz-btn wiz-next" id="wiz-next">Naprej →</button></div>\n')
    out += "</section>\n</main>\n" + FOOTER
    return out


def prevajalec_page():
    out = head("Prevajalec s kamero · Japonska — Mesec za dušo",
               "Usmerite kamero proti japonskemu besedilu in dobite prevod v slovenščino.")
    out += nav("prevajalec")
    out += "<main>\n"
    out += _page_hero("🔍", "Kot Google Lens", "Prevajalec s kamero",
                      "Usmerite telefon proti japonskemu napisu — prevod se prikaže pod njim")

    out += """<section class="card-section tr-card" aria-labelledby="tr-kamera">
  <h2 id="tr-kamera">📷 Kamera</h2>
  <div class="tr-cam" id="tr-cam" hidden>
    <video id="tr-video" playsinline muted autoplay></video>
    <div class="tr-guide" id="tr-guide" aria-hidden="true"></div>
  </div>
  <p class="tr-hint" id="tr-hint">Napis postavite v okvir, držite telefon mirno in tapnite »Prevedi«.</p>
  <div class="tr-actions">
    <button type="button" class="tr-btn tr-primary" id="tr-open">📷 Odpri kamero</button>
    <button type="button" class="tr-btn tr-primary" id="tr-snap" hidden>📸 Prevedi</button>
    <button type="button" class="tr-btn" id="tr-close" hidden>✕ Zapri kamero</button>
  </div>
  <div class="tr-actions">
    <label class="tr-btn tr-file">🖼️ Slikaj ali izberi sliko<input type="file" id="tr-file" accept="image/*" capture="environment" hidden></label>
    <label class="tr-check"><input type="checkbox" id="tr-crop" checked> Prevedi samo okvir</label>
  </div>
  <p class="tr-status" id="tr-status" role="status" aria-live="polite"></p>
</section>

<section class="card-section tr-card" aria-labelledby="tr-rezultat">
  <h2 id="tr-rezultat">📝 Besedilo in prevod</h2>
  <label class="tr-lbl" for="tr-ja">Prepoznano japonsko besedilo <span>(lahko ga popravite ali vtipkate/prilepite svoje)</span></label>
  <textarea id="tr-ja" class="tr-ja" lang="ja" rows="4" placeholder="Tukaj se prikaže prepoznano besedilo …"></textarea>
  <div class="tr-row">
    <label class="tr-sel">Prevedi v
      <select id="tr-lang"><option value="sl">slovenščino</option><option value="en">angleščino</option></select>
    </label>
    <button type="button" class="tr-btn tr-primary" id="tr-go">🔁 Prevedi</button>
  </div>
  <div class="tr-out" id="tr-out" aria-live="polite"><span class="tr-out-empty">Prevod se prikaže tukaj.</span></div>
  <div class="tr-actions">
    <button type="button" class="tr-btn" id="tr-say">🔊 Poslušaj japonsko</button>
    <button type="button" class="tr-btn" id="tr-copy">📋 Kopiraj prevod</button>
    <button type="button" class="tr-btn" id="tr-show">🪪 Pokaži večje</button>
  </div>
</section>

<section class="card-section" aria-labelledby="tr-nasveti">
  <h2 id="tr-nasveti">💡 Za boljši rezultat</h2>
  <ul class="nice-list">
    <li><strong>Dobra svetloba</strong> — brez sence in bleščanja; ponoči pomaga svetilka telefona.</li>
    <li><strong>Blizu in ravno</strong> — telefon vzporedno z napisom, besedilo naj zapolni okvir.</li>
    <li><strong>Natisnjeno besedilo</strong> — table, jedilniki, vozovnice. Rokopis in napisi v umetniških pisavah so težji.</li>
    <li><strong>Navpično besedilo</strong> (pogosto na templjih) prebere slabše — poskusite ga zasukati ali vtipkati.</li>
    <li><strong>Hrana</strong> — pri jedilnikih prevod pomaga razumeti sestavine; pri alergijah pokažite raje kartico »Imam alergijo na …«.</li>
  </ul>
</section>

<section class="card-section tr-alt" aria-labelledby="tr-google">
  <h2 id="tr-google">🔎 Za najboljši prevod</h2>
  <p class="cat-intro">Za zahtevnejše napise (rokopis, navpično besedilo, žive slike) uporabite aplikacijo Google, ki je v tem še boljša.</p>
  <div class="tr-actions">
    <a class="tr-btn" href="https://translate.google.com/?sl=ja&tl=sl&op=images" target="_blank" rel="noopener">Google Prevajalnik — slika</a>
    <a class="tr-btn" href="https://lens.google.com/" target="_blank" rel="noopener">Google Lens</a>
  </div>
  <p class="fine-note">Zasebnost: slika se obdela v vašem telefonu; prevajalski storitvi se pošlje le prepoznano besedilo (brez slike). Prvič se prenese majhna datoteka za prepoznavo japonščine (~2 MB), zato je potreben internet. Prevodi so strojni — pri pomembnih stvareh (zdravje, alergije, plačila) preverite z osebjem.</p>
</section>
"""
    out += '<div class="back-row"><a class="back-button" href="nasveti.html#kartice">🪪 Kartice za domačine</a></div>\n'
    out += "</main>\n" + FOOTER
    out = out.replace("</body>", f'<script src="prevajalec.js?v={BUILD}"></script>\n</body>', 1)
    return out


# ----------------------------------------------------------------------------
# GRADNJA
# ----------------------------------------------------------------------------

import shutil

SW_TEMPLATE = """/* Service worker potovanja: najprej splet (sveže), sicer predpomnilnik. */
var CACHE_NAME = "__CACHE__";
var PAGES = __PAGES__;

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      return Promise.all(PAGES.map(function (u) { return cache.add(u).catch(function () {}); }));
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE_NAME; }).map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (event) {
  if (event.request.method !== "GET") return;
  var url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;
  var isHTML = event.request.mode === "navigate" ||
               (event.request.headers.get("accept") || "").indexOf("text/html") !== -1;
  var fresh = isHTML || /\\.(css|js|json)$/i.test(url.pathname);
  var req = fresh ? new Request(event.request.url, { cache: "reload" }) : event.request;
  event.respondWith(
    fetch(req).then(function (response) {
      var copy = response.clone();
      caches.open(CACHE_NAME).then(function (cache) { cache.put(event.request, copy); });
      return response;
    }).catch(function () {
      return caches.match(event.request).then(function (cached) { return cached || caches.match("./index.html"); });
    })
  );
});
"""


def write_pwa(pages):
    """manifest.json in sw.js za to potovanje (v mapi potovanja)."""
    manifest = {
        "name": CFG["title"], "short_name": CFG["short"], "description": CFG["desc"], "lang": "sl",
        "start_url": "./index.html", "scope": "../", "display": "standalone",
        "background_color": "#ffffff", "theme_color": CFG["theme"],
        "icons": [{"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"}],
    }
    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    listing = ["./"] + [f"./{p}" for p in pages] + ["./style.css", "./app.js", "./album.js", "./manifest.json",
                                                     "./icons/icon-192.png", "./icons/icon-512.png",
                                                     "./icons/apple-touch-icon.png", "./icons/favicon.svg"]
    if os.path.exists(os.path.join(OUT, "prevajalec.js")):
        listing.append("./prevajalec.js")
    sw = (SW_TEMPLATE.replace("__CACHE__", f"{CFG['id']}-{BUILD}")
          .replace("__PAGES__", json.dumps(listing, ensure_ascii=False)))
    with open(os.path.join(OUT, "sw.js"), "w", encoding="utf-8") as f:
        f.write(sw)


def copy_assets(extra_files=()):
    """Skupne datoteke (CSS/JS/ikone) iz generator/assets v mapo potovanja."""
    os.makedirs(OUT, exist_ok=True)
    for name in ["style.css", "app.js", "album.js"] + list(extra_files):
        shutil.copy2(os.path.join(ASSETS_DIR, name), os.path.join(OUT, name))
    icons_out = os.path.join(OUT, "icons")
    os.makedirs(icons_out, exist_ok=True)
    for name in os.listdir(os.path.join(ASSETS_DIR, "icons")):
        dst = os.path.join(icons_out, name)
        if not os.path.exists(dst) or CFG.get("overwrite_icons", True):
            shutil.copy2(os.path.join(ASSETS_DIR, "icons", name), dst)


def write_pages(builders):
    written = []
    for name, builder in builders:
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(builder())
        written.append(name)
        print(f"written {name}")
    return written


def build():
    """Gradnja potovanja Japonska (privzeto)."""
    os.makedirs(OUT, exist_ok=True)
    copy_assets(["prevajalec.js"])
    pages = write_pages([("index.html", index_page), ("nasveti.html", nasveti_page),
                         ("nacrt.html", nacrt_page), ("priprave.html", priprave_page),
                         ("dozivetja.html", dozivetja_page), ("nalozi.html", nalozi_page),
                         ("izziv.html", izziv_page), ("nujno.html", nujno_page),
                         ("kako.html", kako_page), ("prevajalec.html", prevajalec_page)])
    for i, loc in enumerate(LOCATIONS):
        name = f"{loc['key']}.html"
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(location_page(i, loc))
        pages.append(name)
        print(f"written {name}")
    write_pwa(pages)
    n_vids = sum(len(v) for v in VIDEOS.values())
    print(f"done — embedded videos: {n_vids}")


if __name__ == "__main__":
    build()
