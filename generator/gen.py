#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator strani 'Japonska 2026 — Naše potovanje'.
Iz podatkov spodaj ustvari index.html + 9 podstrani lokacij.
Videe bere iz videos.json (če obstaja) v isti mapi kot ta skripta."""

import json
import os
import html
import urllib.parse

import art

OUT = "/Users/klemenlorber/Library/Mobile Documents/com~apple~CloudDocs/Japonska/japonska-2026-stran"
HERE = os.path.dirname(os.path.abspath(__file__))

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

# Zemljevidi: središče (lat, lon), polovica razpona v stopinjah, in iskalni niz za Google Maps.
MAPS = {
    "tokio":       (35.715, 139.775, 0.030, "Ueno, Taito, Tokyo"),
    "chichibu":    (35.990, 139.085, 0.045, "Chichibu, Saitama"),
    "kawaguchiko": (35.517, 138.764, 0.045, "Lake Kawaguchi, Fujikawaguchiko"),
    "minobusan":   (35.404, 138.437, 0.022, "Kuonji Temple, Minobu, Yamanashi"),
    "izu":         (34.973, 138.925, 0.035, "Shuzenji, Izu, Shizuoka"),
    "kumano":      (33.668, 135.890, 0.055, "Kumano Nachi Taisha, Wakayama"),
    "koyasan":     (34.213, 135.584, 0.022, "Koyasan, Koya, Wakayama"),
    "iya":         (33.900, 133.840, 0.065, "Iya Valley, Miyoshi, Tokushima"),
    "ine":         (35.682, 135.287, 0.022, "Ine no Funaya, Kyoto"),
    "nara":        (34.685, 135.843, 0.025, "Nara Park, Nara"),
    "kyoto":       (35.005, 135.770, 0.055, "Kyoto, Japan"),
    "osaka":       (34.669, 135.501, 0.028, "Dotonbori, Osaka"),
    "hiroshima":   (34.395, 132.455, 0.055, "Hiroshima Peace Memorial Park"),
}

# ----------------------------------------------------------------------------
# PREDLOGE
# ----------------------------------------------------------------------------

def esc(s):
    return html.escape(str(s), quote=True)


def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="sl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <meta name="theme-color" content="#7b2230">
  <link rel="stylesheet" href="style.css">
  <link rel="manifest" href="manifest.json">
  <link rel="icon" href="icons/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
</head>
<body>
"""


def nav(current_key):
    def link(href, key, label):
        cur = ' aria-current="page"' if current_key == key else ""
        return f'<a href="{href}"{cur}>{label}</a>'

    links = [link("index.html", "index", "🏠 Domov"),
             link("nacrt.html", "nacrt", "🗺️ Načrt poti")]
    for loc in LOCATIONS:
        links.append(link(f'{loc["key"]}.html', loc["key"], f'{loc["emoji"]} {esc(loc["nav"])}'))
    links.append(link("dozivetja.html", "dozivetja", "🎨 Doživetja"))
    links.append(link("priprave.html", "priprave", "🎒 Priprave"))
    links.append(link("nasveti.html", "nasveti", "💡 Nasveti"))
    return (
        '<header class="site-header">\n'
        '  <a class="brand" href="index.html">🍁 Japonska — Mesec za dušo</a>\n'
        '  <nav class="topnav" aria-label="Meni">\n    '
        + "\n    ".join(links)
        + "\n  </nav>\n</header>\n"
    )


FOOTER = """<footer>
  <p>🍁 Japonska — Mesec za dušo · 3. november – 2. december 2026 · Tokio → Osaka</p>
  <p>Z ljubeznijo pripravljeno za Magdo in prijateljice</p>
</footer>
<script src="app.js"></script>
</body>
</html>
"""


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
             '  <h2 id="znamenitosti">⛩️ Znamenitosti in doživetja</h2>']
    for s in sights:
        icon = sight_icon(s["name"], s.get("desc", ""))
        parts.append('  <article class="sight">')
        parts.append(f'    <h3><span class="sight-icon" aria-hidden="true">{icon}</span>{esc(s["name"])}</h3>')
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


def day_plan_section(g):
    plan = g.get("day_plan", [])
    if not plan:
        return ""
    parts = ['<section class="card-section" aria-labelledby="dan">',
             '  <h2 id="dan">🗓️ Predlog enega lepega dne</h2>',
             '  <ul class="plan-list">']
    for p in plan:
        ic = PLAN_ICONS.get(p["time"], "•")
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
    m = MAPS.get(key)
    if not m:
        return ""
    lat, lon, span, q = m
    spanx = span / 0.72  # rahlo širši razpon zaradi geografske širine
    bbox = f"{lon - spanx:.4f},{lat - span:.4f},{lon + spanx:.4f},{lat + span:.4f}"
    osm = (f"https://www.openstreetmap.org/export/embed.html?bbox={bbox}"
           f"&layer=mapnik&marker={lat:.4f},{lon:.4f}")
    return (f'<section class="card-section map-section" aria-labelledby="zemljevid">\n'
            f'  <h2 id="zemljevid">🗺️ Zemljevid kraja</h2>\n'
            f'  <iframe class="area-map" src="{esc(osm)}" loading="lazy" '
            f'title="Zemljevid — {esc(q)}"></iframe>\n'
            f'  <a class="pin-btn map-open" href="{maps_url(q)}" target="_blank" rel="noopener">'
            f'📍 Odpri na Google Zemljevidu</a>\n</section>\n')


def stay_section(key):
    e = EXTRAS.get(key, {})
    if not e.get("prespati"):
        return ""
    return (f'<section class="card-section stay-section" aria-labelledby="prespati">\n'
            f'  <h2 id="prespati">🏡 Kje prespati</h2>\n'
            f'  <p>{esc(e["prespati"])}</p>\n</section>\n')


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
    parts.append('    <h2>📖 Magdin dnevnik</h2>')
    parts.append('    <p class="diary-hint">Prostor za vaše vtise, skice in najlepši spomin s te postaje.</p>')
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

    out = head(f"{loc['name']} · Japonska 2026", f"{loc['name']}: znamenitosti, hrana in nasveti — vodnik Japonska 2026.")
    out += nav(loc["key"])
    out += "<main>\n"

    out += f"""<section class="loc-hero">
  <div class="scene-banner">{art.location_scene(loc['key'])}</div>
  <p class="kicker">{loc['emoji']} {kicker}</p>
  <h1>{esc(loc['name'])}</h1>
  <p class="loc-sub">{esc(loc['sub'])}</p>
  <p class="loc-intro">{esc(loc['intro'])}</p>
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
    out += food_section(loc, g)
    out += practical_section(g)
    out += stay_section(loc["key"])

    out += f"""<section class="card-section fact-section" aria-labelledby="zanimivost">
  <h2 id="zanimivost">💡 Zanimivost</h2>
  <p>{esc(loc['fact'])}</p>
</section>
<section class="card-section magda-section" aria-labelledby="magda">
  <h2 id="magda">💛 Magdin trenutek</h2>
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
    ("Dober dan", "Konnichiwa", "kon-ni-či-va"),
    ("Dobro jutro", "Ohayō gozaimasu", "o-ha-jo go-zai-mas"),
    ("Dober večer", "Konbanwa", "kon-ban-va"),
    ("Hvala lepa", "Arigatō gozaimasu", "a-ri-ga-to go-zai-mas"),
    ("Prosim", "Onegai shimasu", "o-ne-gai ši-mas"),
    ("Oprostite", "Sumimasen", "su-mi-ma-sen"),
    ("Da / Ne", "Hai / Iie", "haj / i-je"),
    ("Koliko stane?", "Ikura desu ka?", "i-ku-ra des ka"),
    ("Račun, prosim", "Okaikei onegai shimasu", "o-kai-kej o-ne-gai ši-mas"),
    ("Kje je stranišče?", "Toire wa doko desu ka?", "to-i-re va do-ko des ka"),
    ("Zelo okusno!", "Oishii!", "oj-ši"),
    ("Dober tek (pred jedjo)", "Itadakimasu", "i-ta-da-ki-mas"),
    ("Hvala za pogostitev (po jedi)", "Gochisōsama deshita", "go-či-so-sa-ma deš-ta"),
    ("Na zdravje!", "Kanpai!", "kan-paj"),
    ("Ne razumem", "Wakarimasen", "va-ka-ri-ma-sen"),
    ("Nasvidenje", "Sayōnara", "sa-jo-na-ra"),
]


def nasveti_page():
    out = head("Nasveti in fraze · Japonska 2026",
               "Praktični nasveti za Japonsko: onsen bonton, denar, prevoz, november in uporabne japonske fraze.")
    out += nav("nasveti")
    out += "<main>\n"
    out += """<section class="loc-hero">
  <div class="loc-emoji" aria-hidden="true">💡</div>
  <p class="kicker">Za vsak dan potovanja</p>
  <h1>Nasveti in fraze</h1>
  <p class="loc-sub">Majhne stvari, ki naredijo potovanje gladko</p>
</section>
"""
    for title, items in NASVETI:
        sec_id = title.split(" ", 1)[1].lower().replace(" ", "-")
        out += f'<section class="card-section" aria-labelledby="{esc(sec_id)}">\n  <h2 id="{esc(sec_id)}">{esc(title)}</h2>\n  <ul class="nice-list">\n'
        for name, desc in items:
            out += f"    <li><strong>{esc(name)}</strong> — {esc(desc)}</li>\n"
        out += "  </ul>\n</section>\n"

    out += '<section class="card-section" aria-labelledby="fraze">\n  <h2 id="fraze">🗣️ Uporabne japonske fraze</h2>\n  <ul class="phrase-list">\n'
    for sl, jp, izg in FRAZE:
        out += (f'    <li><span class="sl">{esc(sl)}</span>'
                f'<span class="jp">{esc(jp)}</span>'
                f'<span class="izg">({esc(izg)})</span></li>\n')
    out += "  </ul>\n</section>\n"
    out += '<div class="back-row"><a class="back-button" href="index.html">🏠 Nazaj na pregled</a></div>\n'
    out += "</main>\n"
    out += FOOTER
    return out


def _page_hero(emoji, kicker, title, subtitle):
    return f"""<section class="loc-hero">
  <div class="loc-emoji" aria-hidden="true">{emoji}</div>
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


def nacrt_page():
    it = ITINERARY
    out = head("Načrt poti — Japonska, Mesec za dušo",
               "30-dnevni načrt poti po Japonski: dan za dnem in prehodi med kraji, 3. 11.–2. 12. 2026.")
    out += nav("nacrt")
    out += "<main>\n"
    out += _page_hero("🗺️", "Hrbtenica potovanja", "Načrt poti — 30 dni",
                      "Dan za dnem, od Tokia do Osake")
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
        out += (f'    <li class="it-day{" it-new" if new else ""}">\n'
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
                      "Pred odhodom · denar · vlaki · stroški · seznam")
    # hitri skok
    order = ["pred-odhodom", "denar", "prevoz", "stroski"]
    out += '<nav class="chip-row" aria-label="Vsebina">\n'
    for k in order:
        d = PRACTICAL.get(k)
        if d:
            out += f'  <a class="chip" href="#{k}">{d.get("emoji","")} {esc(d["title"])}</a>\n'
    out += '  <a class="chip" href="#seznam">✅ Kontrolni seznam</a>\n'
    out += "</nav>\n"
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
                      "Kuhanje · čaj · zen vrtovi · ustvarjanje")
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
            out += "  </div>\n"
        out += "</section>\n"
    out += '<div class="back-row"><a class="back-button" href="index.html">🏠 Nazaj na pregled</a></div>\n'
    out += "</main>\n" + FOOTER
    return out


def index_page():
    out = head(
        "Japonska — Mesec za dušo",
        "Potovalni vodnik za Magdo in prijateljice: Japonska, 3. november – 2. december 2026, Tokio → Osaka.",
    )
    out += nav("index")
    out += "<main>\n"
    out += f"""<section class="hero">
  <div class="scene-banner home-banner">{art.home_scene()}</div>
  <p class="leaves" aria-hidden="true">🍁 🍂 🍁</p>
  <h1>Japonska<br><span class="h1-sub">Mesec za dušo</span></h1>
  <p class="dates">3. november – 2. december 2026 · Tokio → Osaka</p>
  <p class="tagline">Potovalni vodnik za Magdo in prijateljice — vaš žepni spremljevalec: za vsako postajo znamenitosti z zemljevidi, preverjene restavracije, osebne rubrike, nasveti in videi.</p>
  <!-- Povezavo do foto albuma vpišeš v datoteki app.js (PHOTO_ALBUM_URL) -->
  <a id="photo-link" class="photo-button" href="#">📸 Naše fotografije</a>
</section>
<nav class="quick-links" aria-label="Glavna poglavja">
  <a href="nacrt.html"><span class="ql-emoji" aria-hidden="true">🗺️</span><span class="ql-t">Načrt poti</span><span class="ql-d">30 dni, dan za dnem</span></a>
  <a href="dozivetja.html"><span class="ql-emoji" aria-hidden="true">🎨</span><span class="ql-t">Doživetja</span><span class="ql-d">delavnice, čaj, vrtovi</span></a>
  <a href="priprave.html"><span class="ql-emoji" aria-hidden="true">🎒</span><span class="ql-t">Priprave</span><span class="ql-d">denar, vlaki, pakiranje</span></a>
  <a href="nasveti.html"><span class="ql-emoji" aria-hidden="true">💡</span><span class="ql-t">Nasveti</span><span class="ql-d">bonton in fraze</span></a>
</nav>
"""
    out += """<section class="welcome card-section" aria-labelledby="welcome">
  <h2 id="welcome">👋 Dobrodošle</h2>
  <p>Pred vami je mesec, kakršnega si privoščimo enkrat v življenju — cel november na Japonskem, v času, ko se javorji obarvajo v najlepše rdeče in zlato. Ta vodnik ni seznam, ki bi ga bilo treba prehiteti; je vaš tihi spremljevalec.</p>
  <p>Potujte počasi. Ena znamenitost dopoldne, ena popoldne, vmes skodelica čaja. Ustavite se, kjer je lepo, in tam ostanite dlje, kot se zdi potrebno. Japonska najlepše nagradi tiste, ki se ji ne mudi.</p>
  <p>Na vsaki postaji boste našle znamenitosti z zemljevidi, kje in kaj jesti, kdaj je kraj najlepši, kje si vzeti uro zase — in prostor za svoje zapiske. Lepo pot, drage naše. 🍁</p>
</section>
"""
    out += '<ul class="route" aria-label="Pot potovanja">\n'
    route_items = []
    for loc in LOCATIONS:
        route_items.append(f"  <li>{loc['emoji']} {esc(loc['nav'])}</li>")
    out += '\n  <li class="arrow" aria-hidden="true">→</li>\n'.join(route_items) + "\n</ul>\n"

    out += '<h2 class="section-title">Naše postaje</h2>\n<ul class="cards">\n'
    for i, loc in enumerate(LOCATIONS):
        stop = f"Postaja {i + 1}"
        lbl = stop_label(loc)
        if lbl:
            stop += f" · {lbl}"
        out += f"""  <li>
    <a href="{loc['key']}.html">
      <span class="card-scene">{art.location_scene(loc['key'])}</span>
      <span class="card-body">
        <span class="stop-num">{stop}</span>
        <span class="card-title">{loc['emoji']} {esc(loc['name'])}</span>
        <span class="card-teaser">{esc(loc['teaser'])}</span>
        <span class="card-more">Odpri vodnik →</span>
      </span>
    </a>
  </li>
"""
    out += "</ul>\n"
    out += """<div class="back-row">
  <a class="back-button" href="nasveti.html">💡 Nasveti in japonske fraze</a>
</div>
</main>
"""
    out += FOOTER
    return out


# ----------------------------------------------------------------------------

os.makedirs(OUT, exist_ok=True)

with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_page())
print("written index.html")

with open(os.path.join(OUT, "nasveti.html"), "w", encoding="utf-8") as f:
    f.write(nasveti_page())
print("written nasveti.html")

for name, builder in [("nacrt.html", nacrt_page),
                      ("priprave.html", priprave_page),
                      ("dozivetja.html", dozivetja_page)]:
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(builder())
    print(f"written {name}")

for i, loc in enumerate(LOCATIONS):
    with open(os.path.join(OUT, f"{loc['key']}.html"), "w", encoding="utf-8") as f:
        f.write(location_page(i, loc))
    print(f"written {loc['key']}.html")

n_vids = sum(len(v) for v in VIDEOS.values())
print(f"done — embedded videos: {n_vids}")
