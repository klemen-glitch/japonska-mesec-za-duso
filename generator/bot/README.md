# Telegram bot — tehnične opombe

- Funkcija: Supabase Edge Function `trip-bot` (koda: `bot/trip-bot/index.ts`, `verify_jwt=false`).
  - `POST ?hook=1` — Telegram webhook (preverja glavo `x-telegram-bot-api-secret-token` = `trip_bot_config.webhook_secret`)
  - `POST ?tick=1` — urnik (pg_cron `trip_bot_tick`, vsakih 5 min, glava `x-cron-secret` = `cron_secret`)
  - `GET` — `{ok, configured}`
- Tabele (brez politik RLS; dostop le prek service role): `trip_bot_config`, `trip_bot_settings`, `trip_bot_chats`, `trip_bot_sent`, `trip_days`, `trip_legs`.
- Seed: `python3 generator/gen_bot_seed.py > generator/bot/seed.sql` (dnevi, prehodi, nastavitve; ob spremembi načrta ponovno poženi seed).
- Aktivacija (ko je žeton):
  1. `insert into trip_bot_config(key,value) values ('bot_token','<žeton>') on conflict (key) do update set value=excluded.value;`
  2. webhook: `curl https://api.telegram.org/bot<žeton>/setWebhook -d url='https://ayejgzzaykbopojiacgn.supabase.co/functions/v1/trip-bot?hook=1' -d secret_token='<webhook_secret iz trip_bot_config>' -d 'allowed_updates=["message","callback_query"]'`
  3. ukazi: `setMyCommands` (danes, jutri, nastanitev, vreme, povzetek, povezi, pomoc)
  4. preveri `getWebhookInfo`; v skupini pošlji `/povezi <koda>`.
- Dedup obvestil: `trip_bot_sent (trip_id, kind, day_iso)`; za ponovno pošiljanje izbriši vrstico.
- Obstoječe funkcije `meta-webhook`, `telegram-*`, `intake`, `admin` in cron `dispatch-daily-recap`, `sanus-sync-meta-leads` so del CRM — ne spreminjati.
