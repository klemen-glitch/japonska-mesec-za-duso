# Telegram bot — tehnične opombe

- Funkcija: Supabase Edge Function `trip-bot` (koda: `bot/trip-bot/index.ts`, `verify_jwt=false`).
  - `POST ?hook=1` — Telegram webhook (preverja glavo `x-telegram-bot-api-secret-token` = `trip_bot_config.webhook_secret`)
  - `POST ?tick=1` — urnik (pg_cron `trip_bot_tick`, vsakih 5 min, glava `x-cron-secret` = `cron_secret`)
  - `GET` — `{ok, configured}`
- Tabele (brez politik RLS; dostop le prek service role): `trip_bot_config`, `trip_bot_settings`, `trip_bot_chats`, `trip_bot_sent`, `trip_days`, `trip_legs`.
- Seed: `python3 generator/gen_bot_seed.py > generator/bot/seed.sql` (dnevi, prehodi, nastavitve; ob spremembi načrta ponovno poženi seed).
- Aktivacija (ko je žeton):
  1. `insert into trip_bot_config(key,value) values ('bot_token','<žeton>') on conflict (key) do update set value=excluded.value;`
  2. webhook: `curl https://api.telegram.org/bot<žeton>/setWebhook -d url='https://clpwjvcuvpnjtkxokkqh.supabase.co/functions/v1/trip-bot?hook=1' -d secret_token='<webhook_secret iz trip_bot_config>' -d 'allowed_updates=["message","callback_query"]'`
  3. ukazi: `setMyCommands` (danes, jutri, nastanitev, vreme, povzetek, povezi, pomoc)
  4. preveri `getWebhookInfo`; v skupini pošlji `/povezi <koda>`.
- Dedup obvestil: `trip_bot_sent (trip_id, kind, day_iso)`; za ponovno pošiljanje izbriši vrstico.
- Obstoječe funkcije `meta-webhook`, `telegram-*`, `intake`, `admin` in cron `dispatch-daily-recap`, `sanus-sync-meta-leads` so del CRM — ne spreminjati.

## Potopis dneva (od 3. 11. 2026)
- Večerno vprašanje ob 20.00 lokalnega časa; klik na ime = rezervacija zapisa (`trip_day_writer`), opomniki vsakih 40 min, dokler nihče ne klikne; `/zamenjaj`, `/potopis`, `/končano`.
- `composeDay()` sestavi zgodbo dneva v `trip_story` (po 8 min tišine ob novem zapisu ali novih slikah, ali takoj ob `/končano`). AI: Anthropic API, ključ v `trip_bot_config` (`anthropic_key`, neobvezno `anthropic_model`). Brez ključa se zapisi le zložijo (model `brez-ai`), samo slike brez zapisov pa ne ustvarijo ničesar.
- Aplikacija bere `trip_story_list` (Dnevnik, Potopisna knjiga).

## Prijazni pomočnik (od 4. 11. 2026)
- Urnik (lokalni čas postaje): 8.00 jutro (z izzivi), 10.30 »kako gre?« (gumbi), 14.30 kosilo + napredek izzivov, 17.30 opomnik na izzive (če jih kaj manjka), 20.00 večer + izbira pisca. Ob vsakem novem izzivu v albumu sporočilo z navijanjem.
- Izzivi so v tabeli `trip_challenges` (seed: `gen_bot_seed.py`; id = `<postaja>-<n>`, kot `trip_uploads.challenge_id`). Ukaz `/izzivi`.
- `trip_bot_sent.day_iso` je text (ne date), ker hrani tudi id fotografij (`kind = cheer`).
