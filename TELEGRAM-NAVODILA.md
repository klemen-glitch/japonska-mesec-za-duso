# Telegram pomočnik za potovanja — navodila (jutri, ~10 minut)

Vse je že pripravljeno (baza, funkcija `trip-bot`, urnik vsakih 5 minut). Manjka le Telegram bot, ki ga lahko naredi samo lastnik računa.

## 1. Naredi bota (BotFather)
1. V Telegramu odpri **@BotFather** → pošlji `/newbot`.
2. Ime: npr. `Potovanja — pomočnik`. Uporabniško ime: konča se z `bot`, npr. `klemen_potovanja_bot`.
3. BotFather ti pošlje **žeton** (izgleda kot `123456789:AA…`). Kopiraj ga.
4. Pošlji `/setprivacy` → izberi bota → **Disable** (da v skupini vidi odgovore; ni nujno, a pomaga).

## 2. Daj žeton Claudu
V pogovor z Claudom prilepi: `Telegram žeton: 123456789:AA…` — in nič več (Claude ga shrani v bazo, nastavi webhook in ukaze).
> Žeton je geslo bota. Ko je nastavljen, ga lahko pri BotFatherju kadar koli zamenjaš (`/revoke`).

## 3. Naredi skupine in poveži
- **Japonska:** naredi Telegram skupino (npr. »Japonska 2026«), dodaj Marjetico, Heleno, Ljubo, Magdo in bota. V skupino pošlji `/povezi 1195`.
- **Ljubljana:** skupina z Ano (in Maksom, če ima Telegram) ali kar zasebni klepet z botom: `/povezi 1638`.
Bot sam izbriše sporočilo s kodo in odgovori »Povezano«.

## Kaj bot počne
| Kdaj (lokalni čas kraja) | Kaj |
|---|---|
| dan pred začetkom, 8.00 | »Jutri se začne« + vreme + povezave na priprave |
| vsako jutro, 8.00 | načrt dneva, vreme, opozorilo za dež, opomnik za včerajšnji povzetek |
| 13.00 (prvi dan in ob menjavi kraja) | **»Ste že prispele?«** gumbi: ✅ Da · ⏳ Še ne (vpraša znova čez 2 uri) · ❗ Težava (sporočilo gre vsem). Ob »Da« pokaže nastanitev iz »Moje rezervacije« |
| 19.30 | pregled za jutri (+ premik, vozovnice) |
| 20.30 | **»Kdo napiše povzetek dneva?«** — gumbi z imeni (Magda, Marjetica, …). Izbrana odgovori na bota (lahko v več sporočilih), `/končano` |
| 22.00 | opomnik, če povzetka še ni |

Ukazi: `/danes` `/jutri` `/nastanitev` `/vreme` `/povzetek` `/povezi KODA` `/pomoc`.

Povzetki se shranijo v **Dnevnik** (aplikacija → Dnevnik) in so ob koncu surovina za potopis. Pišete lahko tudi kar v aplikaciji.

## Kaj ni vključeno / opozorila
- Bot ne vidi sporočil, ki niso odgovor nanj, če je »privacy« vklopljen — zato je vedno treba **odgovoriti** na sporočilo bota.
- Ure so nastavljene v tabeli `trip_bot_settings` (`morning`, `arrival`, `evening`); spremenimo na željo.
- Kodo potovanja sporoči samo članom skupine; bot jo sicer izbriše, a Telegram jo je za hip videl.
- Ne dotikaj se obstoječih funkcij `telegram-*`, `meta-webhook` v istem Supabase projektu — to je drug sistem (CRM).
