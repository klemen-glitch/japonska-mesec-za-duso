# Potopis iz dnevnika in slik (po koncu potovanja)

Surovina:
- `trip_diary` — povzetki dneva (aplikacija ali Telegram), po dnevih in avtorjih
- `trip_uploads` + izzivi — slike s postajami in opisi (stran Potopisna knjiga)
- `trip_bookings` — kraji, nastanitve (kontekst)

Postopek (Claude, ob koncu potovanja):
1. Izvoz: `select day_iso, author, body from trip_diary where trip_id='japonska' and not deleted order by day_iso, created_at;`
2. Sinteza (prompt v `potopis_prompt.md`): topel, osebni slovenski potopis po dnevih, v ženski množini, z navedbo postaj in zanimivosti; ne izmišljaj dejstev, ki jih ni v zapisih ali vodniku.
3. Vstavitev: `insert into trip_diary (trip_id, day_iso, author, body, source) values ('japonska', '<datum>', 'Potopis', '<besedilo>', 'potopis');` (po dnevih ali eno besedilo) — pokaže se na straneh Dnevnik in Potopisna knjiga (natisni / PDF).
