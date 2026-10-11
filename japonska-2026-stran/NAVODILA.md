# Japonska 2026 — Naše potovanje · Navodila

Statična spletna stran — brez baze, brez backenda. Vse datoteke v tej mapi
so že pripravljene za objavo.

## 1. Dodajanje povezave do foto albuma

1. Ustvari deljen **Google Photos album** (v aplikaciji Google Photos:
   Albumi → Nov album → Deli → Pridobi povezavo) ali deljeno Google Drive mapo.
2. Odpri datoteko [app.js](app.js) in v prvo vrstico med narekovaje prilepi povezavo:

   ```js
   var PHOTO_ALBUM_URL = "https://photos.app.goo.gl/tvoja-povezava";
   ```

Dokler je povezava prazna, gumb »📸 Naše fotografije« na domači strani
samodejno nadomesti prijazno obvestilo.

## 2. Menjava YouTube videov

Vsaka podstran ima v razdelku »🎬 Videi za navdih« vgrajene videe.
Video zamenjaš tako, da v HTML datoteki (npr. `kyoto.html`) poiščeš vrstico:

```html
<iframe class="video-frame" src="https://www.youtube-nocookie.com/embed/KODA_VIDEA" ...>
```

in `KODA_VIDEA` zamenjaš s kodo drugega videa (to je tistih 11 znakov za
`watch?v=` v YouTube povezavi).

## 3. Objava na Vercel

Najlažje brez ukazne vrstice:

1. Pojdi na https://vercel.com in se prijavi (lahko z Google računom).
2. Izberi **Add New → Project → Deploy without Git** oz. na
   https://vercel.com/new povleci **celotno mapo `japonska-2026-stran`**.
3. Vercel ti v minuti vrne povezavo tipa `https://japonska-2026.vercel.app`.

Ob vsaki spremembi strani mapo preprosto povlečeš še enkrat (ali pa za
samodejno posodabljanje mapo povežeš z GitHubom).

## 4. Kako si prijateljice shranijo stran na telefon

Stran deluje kot aplikacija (PWA) — po prvem obisku dela tudi brez interneta
(videi seveda potrebujejo internet).

- **iPhone:** odpri povezavo v Safariju → gumb **Deli** (kvadratek s puščico) →
  **Dodaj na domači zaslon** (Add to Home Screen).
- **Android:** odpri povezavo v Chromu → meni s tremi pikami →
  **Dodaj na začetni zaslon**.

Na domačem zaslonu se pojavi ikona s torii vrati 🍁 in stran se odpira
kot prava aplikacija.

## 5. Kaj je v mapi

| Datoteka | Namen |
| --- | --- |
| `index.html` | domača stran s časovnico in karticami |
| `tokio.html` … `osaka.html` | vodniki devetih postaj (znamenitosti s pini, hrana po kategorijah, nasveti, videi) |
| `nasveti.html` | onsen bonton, denar, prevoz, november, japonske fraze |
| `style.css` | oblika (jesenske barve, velike pisave) |
| `app.js` | povezava do foto albuma + registracija offline podpore |
| `sw.js` | service worker za delovanje brez interneta |
| `manifest.json`, `icons/` | ikone in nastavitve za »aplikacijo« na telefonu |

## 6. Kako je zgrajen vodnik posamezne postaje

Vsaka stran lokacije ima razdelke v tem vrstnem redu:

1. **⛩️ Znamenitosti in doživetja** — vsaka s kratkim opisom, praktičnim
   nasvetom, gumbom »📍 Zemljevid« (odpre Google Maps s pinom) in
   gumbom »🎬 Video« (odpre YouTube iskanje za ta kraj).
2. **🗓️ Predlog enega lepega dne** — okviren načrt dneva.
3. **🍜 Hrana** — najprej »kaj poskusiti«, nato kategorije; dotik kategorije
   odpre seznam preverjenih restavracij s pini na zemljevid.
4. **🧭 Dobro je vedeti** — praktični nasveti (prevoz, rezervacije, gotovina).
5. **💡 Zanimivost** in **💛 Magdin trenutek**.
6. **🎬 Videi za navdih** — preverjeni vgrajeni YouTube videi.

Vsi podatki so statični (HTML) — restavracijo ali znamenitost urediš kar
v HTML datoteki te lokacije (poišči njeno ime).
