# Potovalni vodniki 🧭

Več zasebnih potovalnih vodnikov (PWA) na enem naslovu. Vsako potovanje ima svojo kodo (PIN):
vstopna stran (`site/index.html`) kodo preveri na strežniku (Supabase) in odpre potovanje (ali več potovanj),
ki so prirejena tej kodi. Drugi potovanj ne vidijo.

- **Potovanja:** `site/<skrita-mapa>/` (HTML/CSS/JS, brez ogrodja)
  - `jp-xyna9tg2e/` — Japonska, Mesec za dušo (3. 11.–2. 12. 2026)
  - `lj-d4phmm7xw/` — Zmajeva pustolovščina, Ljubljana (15.–16. 10. 2026)
- **Vstopna stran in 404:** `site/index.html`, `site/404.html`, `site/sw.js` (izklop starega service workerja)
- **Generatorji:** `generator/`
  - `gen.py` — skupne predloge + potovanje Japonska
  - `gen_lj.py` + `lj_content.py` + `art_lj.py` — potovanje Ljubljana
  - `gen_site.py` — koren spletišča
  - `assets/` — skupni CSS/JS/ikone (kopirajo se v vsako potovanje; urejaj SAMO tukaj): `app.js` (osnova, vreme, zanimivost dneva, pretvornik), `fun.js` (kviz, lov), `money.js` (skupni stroški), `knjiga.js` (potopisna knjiga), `album.js`
  - `data_jp.py`, `lj_content.py` — vsebina (nastanitve, povezave, zanimivosti, kviz, lov); `links.py` — graditelji povezav; `geocode*.py` + `geocache.json` — koordinate znamenitosti

## Funkcije (povzetek)
Vreme, zanimivosti, kviz, lov, potopisna knjiga, skupni stroški (Japonska), dežni način (Plan B), koledar (.ics), delovanje brez interneta (service worker + čakalna vrsta), Moje rezervacije, kartice za taksista (Japonska), zdravstvena kartica (Nujno), dnevnik, pogovorni prevajalnik (Japonska), Telegram pomočnik (`generator/bot/`, navodila v `TELEGRAM-NAVODILA.md`), potopis (`generator/potopis/`).

## Objava
GitHub Pages objavi mapo `site/` (`.github/workflows/pages.yml`).

## Posodobitev vsebine
```
python3 generator/gen.py        # Japonska
python3 generator/gen_lj.py     # Ljubljana
python3 generator/gen_site.py   # koren
```

## Novo potovanje
1. Napiši `gen_<ime>.py` po vzoru `gen_lj.py` (nova vsebina, nastavitve `CFG`, `TXT`).
2. V Supabase dodaj vrstico v `trip_trips` in zgoščeno kodo v `trip_access` (ena koda lahko odpre več potovanj).
3. Poženi generator in objavi.
