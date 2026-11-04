// Telegram bot za potovalne vodnike (Japonska, Ljubljana).
// Funkcija: trip-bot  (POST ?hook=1 = Telegram webhook, POST ?tick=1 = urnik iz pg_cron, GET = zdravje)
// Skrivnosti (žeton bota, skrivnost webhooka, skrivnost crona) so v tabeli trip_bot_config (brez dostopa prek API-ja).
// Ničesar ne pošlje, dokler v trip_bot_config ni vrstice bot_token.
import { createClient } from "npm:@supabase/supabase-js@2";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });

type Cfg = Record<string, string>;
let CFG: Cfg = {};

async function loadCfg(): Promise<Cfg> {
  const { data } = await db.from("trip_bot_config").select("key,value");
  const o: Cfg = {};
  (data || []).forEach((r: any) => { o[r.key] = r.value; });
  CFG = o;
  return o;
}

// ------------------------------------------------------------------ Telegram
async function tg(method: string, body: Record<string, unknown>) {
  const r = await fetch(`https://api.telegram.org/bot${CFG.bot_token}/${method}`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  });
  const j = await r.json().catch(() => ({}));
  if (!j.ok) console.log("tg napaka", method, JSON.stringify(j));
  return j;
}
const esc = (s: unknown) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
function send(chat_id: number, text: string, extra: Record<string, unknown> = {}) {
  return tg("sendMessage", { chat_id, text, parse_mode: "HTML", disable_web_page_preview: true, ...extra });
}
const urlBtn = (text: string, url: string) => ({ text, url });
const cbBtn = (text: string, data: string) => ({ text, callback_data: data });

// ------------------------------------------------------------------ pomožne funkcije
async function sha256(s: string): Promise<string> {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s.trim()));
  return Array.from(new Uint8Array(b)).map((x) => x.toString(16).padStart(2, "0")).join("");
}
function localNow(tz: string) {
  const parts = new Intl.DateTimeFormat("en-CA", { timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", hourCycle: "h23" }).formatToParts(new Date());
  const g = (t: string) => parts.find((p) => p.type === t)!.value;
  const iso = `${g("year")}-${g("month")}-${g("day")}`;
  const hh = parseInt(g("hour"), 10), mm = parseInt(g("minute"), 10);
  return { iso, hm: `${g("hour")}:${g("minute")}`, minutes: hh * 60 + mm };
}
function toMin(t: string) { const [h, m] = t.split(":"); return parseInt(h, 10) * 60 + parseInt(m, 10); }
function addDays(iso: string, n: number) { const d = new Date(iso + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); }
const MON = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "avg", "sep", "okt", "nov", "dec"];
const dlab = (iso: string) => { const p = iso.split("-"); return `${parseInt(p[2], 10)}. ${MON[parseInt(p[1], 10) - 1]}`; };

function wxEmoji(c: number) { return c === 0 ? "☀️" : c <= 2 ? "🌤️" : c === 3 ? "☁️" : c === 45 || c === 48 ? "🌫️" : c < 60 ? "🌦️" : c < 70 ? "🌧️" : c < 80 ? "🌨️" : c < 90 ? "🌦️" : "⛈️"; }
async function weather(lat: number | null, lon: number | null, iso: string) {
  if (lat == null || lon == null) return null;
  try {
    const r = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset&timezone=auto&forecast_days=7`);
    const j = await r.json();
    const i = j.daily.time.indexOf(iso);
    if (i < 0) return null;
    return { code: j.daily.weather_code[i], max: Math.round(j.daily.temperature_2m_max[i]), min: Math.round(j.daily.temperature_2m_min[i]), rain: j.daily.precipitation_probability_max[i], sr: j.daily.sunrise[i].slice(11, 16), ss: j.daily.sunset[i].slice(11, 16) };
  } catch { return null; }
}
function wxLine(w: any) { return w ? `${wxEmoji(w.code)} ${w.min}–${w.max} °C · 💧 ${w.rain ?? 0} % · 🌅 ${w.sr} · 🌇 ${w.ss}` : ""; }

// ------------------------------------------------------------------ podatki o potovanju
async function settingsFor(trip_id: string) {
  const { data } = await db.from("trip_bot_settings").select("*").eq("trip_id", trip_id).maybeSingle();
  return data;
}
async function tripInfo(trip_id: string) {
  const { data } = await db.from("trip_trips").select("id,slug,title,emoji").eq("id", trip_id).maybeSingle();
  return data;
}
async function allDays(trip_id: string) {
  const { data } = await db.from("trip_days").select("*").eq("trip_id", trip_id).order("day");
  return data || [];
}
function appUrl(trip: any, page = "index.html") { return `${CFG.app_base || ""}/${trip.slug}/${page}`; }

// besedila (dvojina za dva potnika, sicer ženska množina)
function words(people: string[]) {
  const dual = people.length === 2;
  return {
    dual,
    arrived: dual ? "Sta že prispela" : "Ste že prispele",
    you: dual ? "vama" : "vam",
    youNom: dual ? "vidva" : "vi",
    write: dual ? "napišita" : "napišite",
    plan: dual ? "Vajin načrt" : "Vaš načrt",
    ready: dual ? "Sta pripravljena?" : "Ste pripravljene?",
    please: dual ? "Odgovorita" : "Odgovorite",
    where: dual ? "kje sta bila, kaj sta videla" : "kje ste bile, kaj ste videle",
    know: dual ? "👍 Jasno, vemo za jutri" : "👍 Jasno, vemo za jutri",
  };
}

// ------------------------------------------------------------------ prijaznost in izzivi
const pick = <T,>(a: T[]): T => a[Math.floor(Math.random() * a.length)];
async function chStatus(trip_id: string, station: string) {
  const { data: ch } = await db.from("trip_challenges").select("id,kind,text").eq("trip_id", trip_id).eq("station", station);
  const { data: up } = await db.from("trip_uploads").select("challenge_id,uploader").eq("trip_id", trip_id).like("challenge_id", station + "-%");
  const num = (id: string) => parseInt(id.split("-").pop() || "0", 10);
  const list = (ch || []).sort((a: any, b: any) => num(a.id) - num(b.id));
  const done = new Set((up || []).map((u: any) => u.challenge_id));
  return { total: list.length, done: list.filter((c: any) => done.has(c.id)).length, left: list.filter((c: any) => !done.has(c.id)) };
}
const bar = (d: number, t: number) => t ? "🟩".repeat(d) + "⬜".repeat(Math.max(0, t - d)) : "";
const GREET = ["☀️ <b>Dobro jutro, junakinje!</b>", "🌸 <b>Dobro jutro, sončki!</b>", "☕ <b>Dobro jutro!</b> Upam, da ste se lepo naspale.", "🌞 <b>Hej, dobro jutro!</b> Nov dan, nova doživetja!"];
const GREET_DUAL = ["☀️ <b>Dobro jutro, pustolovca!</b>", "🐉 <b>Dobro jutro, zmajčka!</b>", "☕ <b>Dobro jutro!</b> Upam, da sta se lepo naspala."];

// ------------------------------------------------------------------ obvestila po urniku
async function claim(trip_id: string, kind: string, iso: string): Promise<boolean> {
  const { data, error } = await db.from("trip_bot_sent").insert({ trip_id, kind, day_iso: iso }).select();
  return !error && !!data && data.length > 0;
}
async function targets(s: any): Promise<number[]> {
  if (s.chat_id) return [Number(s.chat_id)];
  const { data } = await db.from("trip_bot_chats").select("chat_id").eq("trip_id", s.trip_id);
  return Array.from(new Set((data || []).map((r: any) => Number(r.chat_id)).filter((x: number) => x > 0)));
}

async function sendToAll(s: any, text: string, extra: Record<string, unknown> = {}) {
  const ids = await targets(s);
  for (const id of ids) await send(id, text, extra);
  return ids.length;
}

async function tick() {
  const { data: all } = await db.from("trip_bot_settings").select("*").eq("enabled", true);
  const out: string[] = [];
  for (const s of all || []) {
    const trip = await tripInfo(s.trip_id);
    if (!trip) continue;
    const now = localNow(s.tz);
    const days = await allDays(s.trip_id);
    if (!days.length) continue;
    const first = days[0].iso;
    const today = days.find((d: any) => d.iso === now.iso);
    const tomorrow = days.find((d: any) => d.iso === addDays(now.iso, 1));
    const prev = days.find((d: any) => d.iso === addDays(now.iso, -1));
    const W = words(s.people || []);
    const within = (hhmm: string, hours = 3) => now.minutes >= toMin(hhmm) && now.minutes < toMin(hhmm) + hours * 60;

    // dan pred začetkom
    if (now.iso === addDays(first, -1) && within(s.morning) && await claim(s.trip_id, "pretrip", now.iso)) {
      const d1 = days[0];
      const w = await weather(d1.lat, d1.lon, first);
      await sendToAll(s, `🧳 <b>Jutri se začne!</b>\n${trip.emoji} ${esc(trip.title)} — ${esc(d1.title)}\n${w ? wxLine(w) + "\n" : ""}\n✅ Preverite kontrolni seznam, polnilce in vozovnice.`, {
        reply_markup: { inline_keyboard: [[urlBtn("🎒 Priprave", appUrl(trip, "priprave.html"))], [urlBtn("📅 Načrt", appUrl(trip, "nacrt.html"))]] } });
      out.push(s.trip_id + ":pretrip");
    }
    if (!today) continue;

    // jutranje sporočilo
    if (within(s.morning) && await claim(s.trip_id, "morning", now.iso)) {
      const w = await weather(today.lat, today.lon, now.iso);
      let msg = `${pick(W.dual ? GREET_DUAL : GREET)}\nDan ${today.day} od ${days.length} — ${esc(today.station_name || today.region)}\n<b>${esc(today.title)}</b>\n${esc(today.plan)}\n${w ? "\n" + wxLine(w) : ""}`;
      { const cs = await chStatus(s.trip_id, today.station); if (cs.total) msg += `\n\n📸 <b>Izzivi tukaj: ${cs.total}</b> (opravljenih ${cs.done}). Za začetek: ${esc(cs.left[0]?.text || "vse so že narejeni, bravo!")}`; }
      if (w && w.rain >= 60) msg += `\n\n☔ <b>Napoved kaže dež.</b> V aplikaciji vklopite <i>dežni način</i> za Plan B.`;
      if (prev) {
        const { count } = await db.from("trip_diary").select("id", { count: "exact", head: true }).eq("trip_id", s.trip_id).eq("day_iso", prev.iso).eq("deleted", false);
        if (!count) msg += `\n\n✍️ Včeraj ni povzetka dneva. Pošljite /povzetek, če ga želite dopisati.`;
      }
      await sendToAll(s, msg, { reply_markup: { inline_keyboard: [[urlBtn("📖 Vodnik za danes", appUrl(trip, (today.station || "index") + ".html"))], [urlBtn("🧾 Rezervacije", appUrl(trip, "rezervacije.html"))]] } });
      out.push(s.trip_id + ":morning");
    }

    // prihod: ali ste prispele? (če se kraj spremeni glede na prejšnji dan)
    if ((!prev || prev.station !== today.station) && within(s.arrival, 6) && await claim(s.trip_id, "arrival", now.iso)) {
      await sendToAll(s, `📍 <b>${W.arrived} v ${esc(today.station_name || today.region)}?</b> 🎒 Upam, da je bila pot gladka!`, {
        reply_markup: { inline_keyboard: [[cbBtn("✅ Da, smo tu", "arr:yes:" + now.iso), cbBtn("⏳ Še ne", "arr:no:" + now.iso)], [cbBtn("❗ Težava", "arr:prob:" + now.iso)]] } });
      out.push(s.trip_id + ":arrival");
    }

    // ponovitev vprašanja o prihodu (če je bil odgovor »še ne«)
    {
      const { data: rr } = await db.from("trip_bot_sent").select("*").eq("trip_id", s.trip_id).eq("kind", "arrival_retry").eq("day_iso", now.iso).lte("sent_at", new Date().toISOString());
      if (rr && rr.length) {
        await db.from("trip_bot_sent").delete().eq("trip_id", s.trip_id).eq("kind", "arrival_retry").eq("day_iso", now.iso);
        await sendToAll(s, `📍 <b>${W.arrived} v ${esc(today.station_name || today.region)}?</b>`, {
          reply_markup: { inline_keyboard: [[cbBtn("✅ Da, smo tu", "arr:yes:" + now.iso), cbBtn("⏳ Še ne", "arr:no:" + now.iso)], [cbBtn("❗ Težava", "arr:prob:" + now.iso)]] } });
        out.push(s.trip_id + ":arrival2");
      }
    }

    // jutri: pregled in premik
    if (tomorrow && within(addMinutes(s.evening, -60)) && await claim(s.trip_id, "tomorrow", now.iso)) {
      const w = await weather(tomorrow.lat, tomorrow.lon, tomorrow.iso);
      let msg = `🌙 <b>Jutri</b> (${dlab(tomorrow.iso)}) — Dan ${tomorrow.day}: ${esc(tomorrow.title)}\n${esc(tomorrow.plan)}\n${w ? "\n" + wxLine(w) : ""}`;
      if (tomorrow.station !== today.station) {
        const { data: legs } = await db.from("trip_legs").select("*").eq("trip_id", s.trip_id);
        const leg = (legs || []).find((l: any) => l.from_r === today.region && l.to_r === tomorrow.region) || (legs || []).find((l: any) => l.to_r === tomorrow.region);
        if (leg) msg += `\n\n🚉 <b>Premik: ${esc(leg.from_r)} → ${esc(leg.to_r)}</b> (${esc(leg.dur)})\n${esc(leg.how)}\n💡 ${esc(leg.tip)}`;
      }
      if (w && w.rain >= 60) msg += `\n\n☔ Napoved kaže dež — pripravite Plan B.`;
      await sendToAll(s, msg, { reply_markup: { inline_keyboard: [[cbBtn(W.know, "pack:" + tomorrow.iso)], [urlBtn("🚉 Prevozi", appUrl(trip, "nacrt.html#prehodi"))]] } });
      out.push(s.trip_id + ":tomorrow");
    }

    // dopoldne: kako gre?
    if (within("10:30", 1.5) && await claim(s.trip_id, "checkin_am", now.iso)) {
      const q = W.dual
        ? pick(["👋 Hej, pustolovca! Kako vama gre? Gre vse po načrtu? 😊", "🐉 Kako je kaj? Sta že videla kaj lepega? Povejta mi!"])
        : pick(["👋 Hej, junakinje! Kako vam gre? Gre vse po načrtu? 😊", "🌸 Kako je kaj? Ste že videle kaj lepega danes? Povejte mi!", "😄 Dopoldanski pozdrav! Kako teče dan — po planu?"]);
      await sendToAll(s, q, { reply_markup: { inline_keyboard: [[cbBtn("🎉 Odlično!", "ci:ok:" + now.iso), cbBtn("😅 Malo zamika", "ci:slow:" + now.iso)], [cbBtn("🆘 Rabimo pomoč", "ci:help:" + now.iso)]] } });
      out.push(s.trip_id + ":checkin_am");
    }
    // popoldne: pokosilo + izzivi
    if (within("14:30", 1.5) && await claim(s.trip_id, "checkin_pm", now.iso)) {
      const cs = await chStatus(s.trip_id, today.station);
      let m = W.dual ? "🍜 Sta že kaj dobrega pojedla? Pošljita sliko!" : pick(["🍜 Ste že pojedle kaj dobrega? Vse me zanima!", "🥢 Popoldne je! Ste si privoščile kaj okusnega? 😋"]);
      if (cs.total) m += `\n\n📸 <b>Izzivi: ${cs.done}/${cs.total}</b> ${bar(cs.done, cs.total)}` + (cs.left.length ? `\nŠe čaka: ${esc(cs.left[0].text)}` : `\n🎉 Vsi izzivi na tej postaji so narejeni — bravo!`);
      await sendToAll(s, m, { reply_markup: { inline_keyboard: [[urlBtn("📸 Naloži slike", appUrl(trip, "nalozi.html")), urlBtn("🎯 Vsi izzivi", appUrl(trip, "izziv.html"))]] } });
      out.push(s.trip_id + ":checkin_pm");
    }
    // pozno popoldne: opomnik na izzive
    if (within("17:30", 1.5)) {
      const cs = await chStatus(s.trip_id, today.station);
      if (cs.left.length && await claim(s.trip_id, "challenge_push", now.iso)) {
        const list = cs.left.slice(0, 3).map((c: any) => `• ${esc(c.text)}`).join("\n");
        const m = (W.dual ? "🎯 <b>Izzivi dneva!</b> Sta jih že opravila? Še čakajo:" : pick(["🎯 <b>Izzivi dneva!</b> Ste jih že opravile? Še čakajo:", "📸 <b>Hej, izzivi!</b> Niste pozabile? Še čakajo:"])) + `\n${list}\n\nOpravljenih ${cs.done} od ${cs.total}. Ni treba vseh — a mi so popestritev spominov! 💛`;
        await sendToAll(s, m, { reply_markup: { inline_keyboard: [[cbBtn(W.dual ? "✅ Opravila sva" : "✅ Opravile smo", "ch:done:" + now.iso), cbBtn("⏭️ Danes ne", "ch:skip:" + now.iso)], [urlBtn("🎯 Izzivi", appUrl(trip, "izziv.html")), urlBtn("📸 Naloži", appUrl(trip, "nalozi.html"))]] } });
        out.push(s.trip_id + ":challenge_push");
      }
    }
    // navijanje za novo opravljene izzive
    {
      const { data: rec } = await db.from("trip_uploads").select("id,challenge_id,uploader,created_at").eq("trip_id", s.trip_id).not("challenge_id", "is", null).gte("created_at", new Date(Date.now() - 20 * 60000).toISOString());
      const fresh: any[] = [];
      for (const u of rec || []) { if (await claim(s.trip_id, "cheer", String(u.id))) fresh.push(u); }
      if (fresh.length) {
        const { data: chs } = await db.from("trip_challenges").select("id,text,station").eq("trip_id", s.trip_id);
        const seen = new Set<string>();
        const lines: string[] = [];
        for (const u of fresh) {
          if (seen.has(u.challenge_id)) continue; seen.add(u.challenge_id);
          const c = (chs || []).find((x: any) => x.id === u.challenge_id);
          if (c) lines.push(`${esc(u.uploader || "Nekdo")} — ${esc(c.text.slice(0, 80))}${c.text.length > 80 ? "…" : ""}`);
        }
        if (lines.length) {
          const cs = await chStatus(s.trip_id, today.station);
          await sendToAll(s, `🎉 <b>${pick(["Bravo", "Juhu", "Super", "Odlično"])}!</b> Nov izziv je opravljen:\n${lines.join("\n")}\n\n📸 ${cs.done}/${cs.total} ${bar(cs.done, cs.total)}` + (cs.total && !cs.left.length ? "\n🏆 Vsi izzivi te postaje so narejeni!" : ""));
          out.push(s.trip_id + ":cheer");
        }
      }
    }

    // večer: kdo piše povzetek (klik na ime = rezervacija zapisa za ta dan)
    if (within(s.evening, 2) && await claim(s.trip_id, "evening", now.iso)) {
      const cs = await chStatus(s.trip_id, today.station);
      const extra = cs.total ? `\n\n📸 Izzivi te postaje: <b>${cs.done}/${cs.total}</b> ${bar(cs.done, cs.total)}` + (cs.done === cs.total ? " 🏆 Bravo!" : cs.done ? " — lepo gre!" : " — jutri nadoknadite, če ste jih zamudile.") : "";
      await askWho(s, trip, today, eveningText(W, s.people || []) + extra);
      out.push(s.trip_id + ":evening");
    }
    // ponavljajoči opomniki, dokler nihče ne klikne na svoje ime in ni zapisa
    {
      const { count } = await db.from("trip_diary").select("id", { count: "exact", head: true }).eq("trip_id", s.trip_id).eq("day_iso", now.iso).eq("deleted", false).neq("source", "potopis");
      const { data: wr } = await db.from("trip_day_writer").select("*").eq("trip_id", s.trip_id).eq("day_iso", now.iso).maybeSingle();
      const since = now.minutes - toMin(s.evening);
      if (!count && since >= 0 && since < 300) {
        if (!wr) {
          const step = Math.floor(since / 40);   // opomnik vsakih 40 min (po 40, 80, 120 …)
          if (step >= 1 && await claim(s.trip_id, "diary_remind_" + step, now.iso)) {
            await askWho(s, trip, today, "⏰ <b>Dnevnika za danes še ni.</b> Klikni na svoje ime — kdor klikne, danes napiše vtise. (Nekaj stavkov zadostuje.)");
            out.push(s.trip_id + ":remind" + step);
          }
        } else if (since >= 60 && Date.now() - new Date(wr.claimed_at).getTime() > 40 * 60000) {
          const step = Math.floor((Date.now() - new Date(wr.claimed_at).getTime()) / (40 * 60000));
          if (await claim(s.trip_id, "writer_nudge_" + step, now.iso)) {
            await sendToAll(s, `✍️ ${esc(wr.person)}, čakamo na tvoj zapis za ${dlab(now.iso)}. Odgovori na zgornje sporočilo z vtisi (lahko v več sporočilih), na koncu pa /končano. Če ne moreš, napiši /zamenjaj.`);
            out.push(s.trip_id + ":nudge");
          }
        }
      }
    }
    // potopis: sestavi dneve s spremembami (zapisi ali slike)
    for (const d of days) {
      if (d.iso > now.iso || d.iso < addDays(now.iso, -3)) continue;
      try { if (await composeDay(s, d, false)) out.push(s.trip_id + ":story:" + d.iso); } catch (e) { console.log("compose napaka", String(e)); }
    }
  }
  return out;
}
function addMinutes(hhmm: string, n: number) { const m = toMin(hhmm) + n; const h = Math.floor(m / 60), mm = m % 60; return `${String(h).padStart(2, "0")}:${String(mm).padStart(2, "0")}`; }

function eveningText(W: any, people: string[]) {
  return W.dual
    ? "🌙 <b>Konec dneva!</b> Napišita, kako sta se danes imela: dogajanje in vtise. Klikni na svoje ime — kdor klikne, danes vpiše dnevnik. Iz zapisa (in slik) nastane potopis."
    : "🌙 <b>Konec dneva!</b> Napišite, kako ste se danes imele: dogajanje in vtise. Klikni na svoje ime (spodaj) — kdor klikne, danes vpiše dnevnik. Iz zapisa (in slik) nastane potopis.";
}
async function askWho(s: any, trip: any, day: any, text: string) {
  const people: string[] = s.people || [];
  const rows = [];
  for (let i = 0; i < people.length; i += 2) rows.push(people.slice(i, i + 2).map((p) => cbBtn("✍️ " + p, `who:${p}:${day.iso}`)));
  rows.push([urlBtn("📸 Naložite slike dneva", appUrl(trip, "nalozi.html")), urlBtn("✍️ Pišem v aplikaciji", appUrl(trip, "dnevnik.html"))]);
  await sendToAll(s, text, { reply_markup: { inline_keyboard: rows } });
}

// ------------------------------------------------------------------ AI (DeepSeek ali Anthropic)
function deepseekKey(): string {
  return CFG.deepseek_key || Deno.env.get("DEEPSEEK_API_KEY") || Deno.env.get("DEEPSEEK_KEY") || Deno.env.get("DEEPSEEK_API_TOKEN") || Deno.env.get("DEEPSEEK") || "";
}
function aiKey(): string { return deepseekKey() || CFG.anthropic_key || ""; }
async function aiCall(system: string, user: string): Promise<{ text: string; model: string }> {
  const ds = deepseekKey();
  if (ds) {
    const model = CFG.deepseek_model || "deepseek-chat";
    const r = await fetch("https://api.deepseek.com/chat/completions", {
      method: "POST", headers: { "content-type": "application/json", authorization: `Bearer ${ds}` },
      body: JSON.stringify({ model, max_tokens: 900, temperature: 0.5, messages: [{ role: "system", content: system }, { role: "user", content: user }] }),
    });
    const j = await r.json().catch(() => ({}));
    const text = (j.choices?.[0]?.message?.content || "").trim();
    if (!text) throw new Error("DeepSeek: " + JSON.stringify(j).slice(0, 200));
    return { text, model };
  }
  const model = CFG.anthropic_model || "claude-sonnet-5-5";
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST", headers: { "content-type": "application/json", "x-api-key": CFG.anthropic_key, "anthropic-version": "2023-06-01" },
    body: JSON.stringify({ model, max_tokens: 900, system, messages: [{ role: "user", content: user }] }),
  });
  const j = await r.json().catch(() => ({}));
  const text = (j.content?.[0]?.text || "").trim();
  if (!text) throw new Error("Anthropic: " + JSON.stringify(j).slice(0, 200));
  return { text, model };
}

// ------------------------------------------------------------------ potopis dneva (AI)
function dayOfTs(ts: string, tz: string) {
  return new Intl.DateTimeFormat("en-CA", { timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date(ts));
}
async function composeDay(s: any, day: any, announce: boolean): Promise<boolean> {
  const { data: ent } = await db.from("trip_diary").select("author,body,created_at,source").eq("trip_id", s.trip_id).eq("day_iso", day.iso).eq("deleted", false).neq("source", "potopis").order("created_at");
  const { data: ups } = await db.from("trip_uploads").select("path,uploader,created_at,mime").eq("trip_id", s.trip_id).gte("created_at", addDays(day.iso, -1) + "T00:00:00Z").lte("created_at", addDays(day.iso, 2) + "T00:00:00Z");
  const photos = (ups || []).filter((u: any) => dayOfTs(u.created_at, s.tz) === day.iso);
  const entries = ent || [];
  if (!entries.length && !photos.length) return false;
  const hasAI = !!aiKey();
  if (!entries.length && !hasAI) return false;   // brez zapisov in brez AI ni kaj sestaviti
  const lastChange = Math.max(0, ...entries.map((e: any) => +new Date(e.created_at)), ...photos.map((p: any) => +new Date(p.created_at)));
  if (!announce && Date.now() - lastChange < 8 * 60000) return false;   // počakaj, da nehajo pisati/nalagati
  const hash = await sha256(JSON.stringify([entries.map((e: any) => [e.author, e.body]), photos.length, hasAI]));
  const { data: cur } = await db.from("trip_story").select("src_hash").eq("trip_id", s.trip_id).eq("day_iso", day.iso).maybeSingle();
  if (cur && cur.src_hash === hash) return false;
  const trip = await tripInfo(s.trip_id);
  let body = "", model = "";
  const people: string[] = s.people || [];
  const dual = people.length === 2;
  if (hasAI) {
    const who = dual ? "dvojini (mi sva, midva, sva videla)" : "ženski množini (smo, smo videle, bile smo)";
    const sys = `Si urednik potopisa v slovenščini. Iz kratkih, nepopravljenih zapisov potnikov sestaviš zgodbo enega dne. Pravila: piši v prvi osebi ${who}; ohrani vsa dejstva, kraje, imena in občutke iz zapisov — NIČ si ne izmišljaj in ne dodajaj dogodkov, ki jih ni v zapisih; popravi slovnico in črkovanje, razporedi dogajanje smiselno in berljivo; topel, preprost ton, brez klišejev in pretiravanja; 80–250 besed, brez naslova, brez nabrajanja z alinejami, brez emojijev. Če so zapisov malo, bodi kratek. Če zapisov ni, napiši le 1–2 skromna stavka o dnevu na podlagi načrta in števila slik, brez izmišljenih doživetij.`;
    const user = `Potovanje: ${trip?.title}\nDan ${day.day}: ${day.title} (${day.station_name || day.region}), ${dlab(day.iso)}\nNačrt dneva: ${day.plan}\nŠtevilo fotografij, ki so jih naložile ta dan: ${photos.length}\n\nZapisi potnikov:\n` +
      (entries.length ? entries.map((e: any) => `[${e.author}] ${e.body}`).join("\n\n") : "(ni zapisov)");
    try { const r = await aiCall(sys, user); body = r.text; model = r.model; } catch (e) { console.log("AI napaka", String(e).slice(0, 300)); }
  }
  if (!body) {   // brez AI (ni ključa ali napaka): preprosta zložitev zapisov
    body = entries.length ? entries.map((e: any) => `${e.body.trim()} (${e.author})`).join("\n\n") : `Dan ${day.day}: ${day.title}. Naloženih je ${photos.length} fotografij.`;
    model = "brez-ai";
  }
  await db.from("trip_story").upsert({ trip_id: s.trip_id, day_iso: day.iso, body, src_hash: hash, entries: entries.length, photos: photos.length,
    photo_paths: photos.slice(0, 12).map((p: any) => p.path), model, updated_at: new Date().toISOString() });
  if (announce) await sendToAll(s, `📖 <b>Potopis — ${dlab(day.iso)}</b>\n\n${esc(body)}\n\n<i>${model === "brez-ai" ? "Zapisi brez urejanja." : "Besedilo je uredil AI iz vaših zapisov."} Vidite ga tudi v aplikaciji (Dnevnik).</i>`);
  return true;
}

// ------------------------------------------------------------------ pogovor (webhook)
async function chatTrip(chat_id: number, user_id: number): Promise<{ trip_id: string; s: any } | null> {
  const { data: gs } = await db.from("trip_bot_settings").select("*").eq("chat_id", chat_id).maybeSingle();
  if (gs) return { trip_id: gs.trip_id, s: gs };
  const { data: c } = await db.from("trip_bot_chats").select("trip_id").eq("chat_id", chat_id).eq("tg_user_id", user_id).maybeSingle();
  if (c && c.trip_id) { const s = await settingsFor(c.trip_id); return s ? { trip_id: c.trip_id, s } : null; }
  return null;
}
async function getState(chat_id: number, user_id: number) {
  const { data } = await db.from("trip_bot_chats").select("*").eq("chat_id", chat_id).eq("tg_user_id", user_id).maybeSingle();
  return data;
}
async function setState(chat_id: number, user_id: number, name: string, patch: Record<string, unknown>, trip_id?: string, person?: string) {
  const cur = await getState(chat_id, user_id);
  const state = { ...(cur?.state || {}), ...patch };
  await db.from("trip_bot_chats").upsert({ chat_id, tg_user_id: user_id, tg_name: name, trip_id: trip_id ?? cur?.trip_id ?? null, person: person ?? cur?.person ?? null, state }, { onConflict: "chat_id,tg_user_id" });
  return state;
}

const HELP = `<b>Ukazi</b>\n/danes — kaj je danes na vrsti\n/jutri — načrt za jutri\n/nastanitev — kje prespite\n/vreme — vreme v kraju\n/izzivi — kateri izzivi še čakajo\n/povzetek — vpiši dnevnik dneva\n/zamenjaj — če ne moreš pisati, naj piše druga\n/potopis — potopis današnjega dne\n/povezi KODA — poveži ta klepet s potovanjem\n/pomoc — ta seznam`;

async function handleLink(msg: any, code: string) {
  const chat = msg.chat.id, uid = msg.from.id;
  const st = await getState(chat, uid);
  const lockUntil = st?.state?.lockUntil ? Number(st.state.lockUntil) : 0;
  if (lockUntil > Date.now()) { await send(chat, "⏳ Preveč napačnih poskusov. Poskusite čez nekaj minut."); return; }
  if (!code) { await send(chat, "Pošljite: <code>/povezi KODA</code> (kodo potovanja imate v sporočilu)."); return; }
  const h = await sha256(code);
  const { data: acc } = await db.from("trip_access").select("trip_id").eq("pin_hash", h);
  // sporočilo s kodo poskusimo izbrisati
  tg("deleteMessage", { chat_id: chat, message_id: msg.message_id });
  if (!acc || !acc.length) {
    const fails = (Number(st?.state?.fails) || 0) + 1;
    await setState(chat, uid, msg.from.first_name || "", { fails, lockUntil: fails >= 5 ? Date.now() + 30 * 60000 : 0 });
    await send(chat, "❌ Napačna koda.");
    return;
  }
  await setState(chat, uid, msg.from.first_name || "", { fails: 0, lockUntil: 0 });
  if (acc.length === 1) return finishLink(msg, acc[0].trip_id);
  const rows = [];
  for (const a of acc) { const t = await tripInfo(a.trip_id); if (t) rows.push([cbBtn(`${t.emoji} ${t.title}`, "link:" + t.id)]); }
  await setState(chat, uid, msg.from.first_name || "", { link_ok: acc.map((a: any) => a.trip_id) });
  await send(chat, "Katero potovanje povežem s tem klepetom?", { reply_markup: { inline_keyboard: rows } });
}
async function finishLink(msg: any, trip_id: string) {
  const chat = msg.chat.id, uid = msg.from.id;
  const trip = await tripInfo(trip_id);
  if (!trip) return;
  const isGroup = msg.chat.type === "group" || msg.chat.type === "supergroup";
  if (isGroup) await db.from("trip_bot_settings").update({ chat_id: chat }).eq("trip_id", trip_id);
  await setState(chat, uid, msg.from.first_name || "", {}, trip_id);
  const s = await settingsFor(trip_id);
  const W = words(s?.people || []);
  await send(chat, `✅ <b>Povezano:</b> ${trip.emoji} ${esc(trip.title)}\n\nOd zdaj ${W.you} pošiljam jutranje načrte, pregled za jutri, vprašanje »${W.arrived.toLowerCase()}?« in večerni povzetek dneva.\n\n${HELP}`);
}

async function whoMenu(chat: number, s: any, day: any) {
  const people: string[] = s.people || [];
  const rows = [];
  for (let i = 0; i < people.length; i += 2) rows.push(people.slice(i, i + 2).map((p) => cbBtn("✍️ " + p, `who:${p}:${day.iso}`)));
  await send(chat, `📝 Kdo piše povzetek za <b>${dlab(day.iso)}</b> (dan ${day.day})?`, { reply_markup: { inline_keyboard: rows } });
}

async function handleCommand(msg: any, cmd: string, arg: string) {
  const chat = msg.chat.id, uid = msg.from.id;
  if (cmd === "/start" || cmd === "/pomoc") {
    const ct = await chatTrip(chat, uid);
    if (!ct) { await send(chat, "👋 Pozdravljeni! Sem pomočnik za potovanje.\nPovežite me z <code>/povezi KODA</code> (kodo potovanja imate v sporočilu).\nV skupini me dodajte kot člana in tam pošljite ukaz."); return; }
    await send(chat, HELP); return;
  }
  if (cmd === "/povezi") return handleLink(msg, arg);
  const ct = await chatTrip(chat, uid);
  if (!ct) { await send(chat, "Najprej me povežite: <code>/povezi KODA</code>"); return; }
  const trip = (await tripInfo(ct.trip_id))!;
  const s = ct.s;
  const now = localNow(s.tz);
  const days = await allDays(ct.trip_id);
  const today = days.find((d: any) => d.iso === now.iso);
  if (cmd === "/danes") {
    if (!today) { await send(chat, `Danes ni na seznamu potovanja (${dlab(now.iso)}). Začetek: ${dlab(days[0].iso)}.`); return; }
    const w = await weather(today.lat, today.lon, now.iso);
    await send(chat, `📅 <b>Dan ${today.day} od ${days.length}</b> — ${esc(today.station_name || today.region)}\n<b>${esc(today.title)}</b>\n${esc(today.plan)}\n${w ? "\n" + wxLine(w) : ""}`, {
      reply_markup: { inline_keyboard: [[urlBtn("📖 Vodnik", appUrl(trip, (today.station || "index") + ".html"))]] } });
    return;
  }
  if (cmd === "/jutri") {
    const t = days.find((d: any) => d.iso === addDays(now.iso, 1));
    if (!t) { await send(chat, "Jutri ni na seznamu potovanja."); return; }
    await send(chat, `🌙 <b>Jutri</b> — Dan ${t.day}: ${esc(t.title)}\n${esc(t.plan)}`, { reply_markup: { inline_keyboard: [[urlBtn("🚉 Prevozi", appUrl(trip, "nacrt.html#prehodi"))]] } });
    return;
  }
  if (cmd === "/vreme") {
    const d = today || days[0];
    const w = await weather(d.lat, d.lon, today ? now.iso : d.iso);
    await send(chat, w ? `${esc(d.station_name || d.region)}: ${wxLine(w)}` : "Vremenske napovedi trenutno ni mogoče dobiti.");
    return;
  }
  if (cmd === "/nastanitev") {
    const iso = today ? now.iso : (days[0]?.iso || now.iso);
    const { data } = await db.from("trip_bookings").select("*").eq("trip_id", ct.trip_id).eq("deleted", false).eq("kind", "nastanitev").order("date_from");
    const cur = (data || []).filter((b: any) => (!b.date_from || b.date_from <= iso) && (!b.date_to || b.date_to >= iso));
    const list = cur.length ? cur : (data || []).filter((b: any) => b.date_from && b.date_from >= iso).slice(0, 1);
    if (!list.length) { await send(chat, `Nastanitev še ni vpisana. Vpišite jo v aplikaciji (Moje rezervacije).`, { reply_markup: { inline_keyboard: [[urlBtn("🧾 Moje rezervacije", appUrl(trip, "rezervacije.html"))]] } }); return; }
    for (const b of list) {
      await send(chat, `🏨 <b>${esc(b.title)}</b>\n${b.date_from ? dlab(b.date_from) + (b.date_to ? " → " + dlab(b.date_to) : "") : ""}\n${b.address ? "📍 " + esc(b.address) + "\n" : ""}${b.address_local ? esc(b.address_local) + "\n" : ""}${b.phone ? "📞 " + esc(b.phone) + "\n" : ""}${b.conf ? "🔖 " + esc(b.conf) + "\n" : ""}${b.time_text ? "⏰ " + esc(b.time_text) : ""}`);
    }
    return;
  }
  if (cmd === "/povzetek") {
    const day = today || days[days.length - 1];
    await whoMenu(chat, s, day);
    return;
  }
  if (cmd === "/zamenjaj") {
    const day = today || days[days.length - 1];
    await db.from("trip_day_writer").delete().eq("trip_id", ct.trip_id).eq("day_iso", day.iso);
    await whoMenu(chat, s, day);
    return;
  }
  if (cmd === "/izzivi") {
    if (!today) { await send(chat, "Danes izzivov še ni na vrsti. 🙂"); return; }
    const cs = await chStatus(ct.trip_id, today.station);
    if (!cs.total) { await send(chat, "Za današnjo postajo izzivov ni — uživajte! 💛"); return; }
    await send(chat, `📸 <b>Izzivi (${esc(today.station_name || today.region)}): ${cs.done}/${cs.total}</b> ${bar(cs.done, cs.total)}\n` + (cs.left.length ? "Še čakajo:\n" + cs.left.map((c: any) => "• " + esc(c.text)).join("\n") : "🏆 Vsi so narejeni — bravo!"), { reply_markup: { inline_keyboard: [[urlBtn("📸 Naloži", appUrl(trip, "nalozi.html")), urlBtn("🎯 Izzivi", appUrl(trip, "izziv.html"))]] } });
    return;
  }
  if (cmd === "/potopis") {
    const day = today || days[days.length - 1];
    const { data: st } = await db.from("trip_story").select("body").eq("trip_id", ct.trip_id).eq("day_iso", day.iso).maybeSingle();
    await send(chat, st ? `📖 <b>Potopis — ${dlab(day.iso)}</b>\n\n${esc(st.body)}` : "Za ta dan potopisa še ni. Vpišite dnevnik (/povzetek) ali naložite slike.");
    return;
  }
  if (cmd === "/koncano" || cmd === "/končano") {
    const st = await getState(chat, uid);
    const dayIso = st?.state?.day as string | undefined;
    await setState(chat, uid, msg.from.first_name || "", { awaiting: null });
    await send(chat, "✅ Hvala! Zapis je shranjen v dnevniku. Sestavljam potopis dneva …");
    const dd = days.find((d: any) => d.iso === (dayIso || now.iso));
    if (dd) {
      try { await composeDay(s, dd, true); } catch (e) { console.log("compose napaka", String(e)); await send(chat, "Potopisa trenutno ni mogoče sestaviti; poskusim znova samodejno."); }
    }
    return;
  }
  await send(chat, HELP);
}

async function saveDiary(msg: any, st: any) {
  const chat = msg.chat.id;
  const body = (msg.text || msg.caption || "").trim();
  if (!body) return;
  await db.from("trip_diary").insert({ trip_id: st.trip_id, day_iso: st.state.day, author: st.state.person, body, source: "telegram" });
  await send(chat, `✅ Shranjeno, ${esc(st.state.person)}. Dodate lahko še (odgovorite na to sporočilo) ali pošljite /končano.`, {
    reply_to_message_id: msg.message_id, reply_markup: { force_reply: true, selective: true } });
}

async function onMessage(msg: any) {
  if (!msg.from || msg.from.is_bot) return;
  const chat = msg.chat.id, uid = msg.from.id;
  const text: string = msg.text || "";
  if (text.startsWith("/")) {
    const m = text.match(/^\/([A-Za-zČŠŽčšž_]+)(?:@\w+)?\s*(.*)$/s);
    if (m) { await handleCommand(msg, "/" + m[1].toLowerCase(), (m[2] || "").trim()); return; }
  }
  const st = await getState(chat, uid);
  const isReplyToBot = !!(msg.reply_to_message && msg.reply_to_message.from && msg.reply_to_message.from.is_bot);
  const isPrivate = msg.chat.type === "private";
  if (st?.state?.awaiting === "diary" && (isReplyToBot || isPrivate)) { await saveDiary(msg, st); return; }
  if (st?.state?.awaiting === "problem" && (isReplyToBot || isPrivate)) {
    const ct = await chatTrip(chat, uid);
    if (ct) {
      await sendToAll(ct.s, `❗ <b>Težava</b> (${esc(msg.from.first_name || "")}): ${esc(text)}`);
      await setState(chat, uid, msg.from.first_name || "", { awaiting: null });
    }
    return;
  }
  if (isPrivate) await send(chat, "Pošljite /pomoc za ukaze.");
}

async function onCallback(cq: any) {
  const data: string = cq.data || "";
  const msg = cq.message;
  if (!msg) { await tg("answerCallbackQuery", { callback_query_id: cq.id }); return; }
  const chat = msg.chat.id, uid = cq.from.id, name = cq.from.first_name || "";
  const [kind, a, b] = data.split(":");
  const ct = await chatTrip(chat, uid);

  if (kind === "link") {
    const st = await getState(chat, uid);
    const ok = st?.state?.link_ok as string[] | undefined;
    if (ok && ok.includes(a)) { await finishLink({ chat: msg.chat, from: cq.from, message_id: msg.message_id }, a); await setState(chat, uid, name, { link_ok: null }); }
    await tg("answerCallbackQuery", { callback_query_id: cq.id });
    return;
  }
  if (!ct) { await tg("answerCallbackQuery", { callback_query_id: cq.id, text: "Najprej /povezi KODA" }); return; }
  const s = ct.s;
  const W = words(s.people || []);

  if (kind === "who") {
    const person = a, day = b;
    const { data: wr } = await db.from("trip_day_writer").select("*").eq("trip_id", ct.trip_id).eq("day_iso", day).maybeSingle();
    if (wr && wr.person !== person) {
      const { count } = await db.from("trip_diary").select("id", { count: "exact", head: true }).eq("trip_id", ct.trip_id).eq("day_iso", day).eq("deleted", false).neq("source", "potopis");
      const stale = Date.now() - new Date(wr.claimed_at).getTime() > 3 * 3600000 && !count;
      if (!stale) { await tg("answerCallbackQuery", { callback_query_id: cq.id, text: `Danes že piše ${wr.person}.`, show_alert: true }); return; }
    }
    await db.from("trip_day_writer").upsert({ trip_id: ct.trip_id, day_iso: day, person, tg_user_id: uid, claimed_at: new Date().toISOString() });
    await tg("answerCallbackQuery", { callback_query_id: cq.id, text: `${person}, hvala!` });
    await tg("editMessageReplyMarkup", { chat_id: chat, message_id: msg.message_id, reply_markup: { inline_keyboard: [] } });
    await sendToAll(s, `✍️ <b>${esc(person)}</b> danes piše dnevnik za ${dlab(day)}. Hvala!`).catch(() => {});
    await setState(chat, uid, name, { awaiting: "diary", person, day }, ct.trip_id, person);
    await send(chat, `✍️ <a href="tg://user?id=${uid}">${esc(person)}</a>, napiši, kako ste se danes imele: dogajanje, vtise, kaj je bilo najlepše in kaj smešno. <b>Odgovori na to sporočilo</b> (lahko v več sporočilih; na koncu /končano). Iz tega bom sestavil potopis dneva.`, {
      reply_markup: { force_reply: true, selective: true, input_field_placeholder: "Danes smo …" } });
    return;
  }
  if (kind === "arr") {
    await tg("answerCallbackQuery", { callback_query_id: cq.id });
    await tg("editMessageReplyMarkup", { chat_id: chat, message_id: msg.message_id, reply_markup: { inline_keyboard: [] } });
    const trip = await tripInfo(ct.trip_id);
    if (a === "yes") {
      const { data } = await db.from("trip_bookings").select("*").eq("trip_id", ct.trip_id).eq("deleted", false).eq("kind", "nastanitev").lte("date_from", b).gte("date_to", b);
      const bk = (data || [])[0];
      if (bk) await send(chat, `✅ Odlično! Nastanitev:\n🏨 <b>${esc(bk.title)}</b>\n${bk.address ? "📍 " + esc(bk.address) + "\n" : ""}${bk.phone ? "📞 " + esc(bk.phone) + "\n" : ""}${bk.conf ? "🔖 " + esc(bk.conf) : ""}`);
      else await send(chat, "✅ Odlično! Nastanitve za ta dan še ni v aplikaciji — vpišite jo (Moje rezervacije), da bo vedno pri roki.", { reply_markup: { inline_keyboard: [[urlBtn("🧾 Moje rezervacije", appUrl(trip, "rezervacije.html"))]] } });
    } else if (a === "no") {
      await send(chat, "⏳ V redu. Če je kaj narobe z vlakom ali nastanitvijo, pošljite /nastanitev ali tapnite spodaj. Vprašam znova čez nekaj ur.", { reply_markup: { inline_keyboard: [[urlBtn("🚉 Prevozi", appUrl(trip, "nacrt.html#prehodi"))]] } });
      // ponovno vprašanje čez 2 uri (poberet ga bo tick)
      await db.from("trip_bot_sent").upsert({ trip_id: ct.trip_id, kind: "arrival_retry", day_iso: b, sent_at: new Date(Date.now() + 2 * 3600000).toISOString() });
    } else if (a === "prob") {
      await setState(chat, uid, name, { awaiting: "problem" });
      await send(chat, `❗ ${W.please} na to sporočilo in opišite težavo (kaj se je zgodilo, kje ste). Sporočilo bom poslal/-a vsem v skupini.`, { reply_markup: { force_reply: true, selective: true } });
    }
    return;
  }
  if (kind === "ci") {
    await tg("answerCallbackQuery", { callback_query_id: cq.id, text: "💛" });
    await tg("editMessageReplyMarkup", { chat_id: chat, message_id: msg.message_id, reply_markup: { inline_keyboard: [] } });
    if (a === "ok") await send(chat, pick(["🎉 Juhu, to je lepo slišati! Uživajte v vsakem koraku. 💛", "😍 Super! Naj bo cel dan tak. Ne pozabite na kakšno sliko!", "🥳 Odlično! Vesela sem z vami. Pošljite mi kaj lepega, ko utegnete!"]));
    else if (a === "slow") await send(chat, pick(["😅 Nič hudega, počasi je včasih najlepše! Če vam česa ne uspe, preskočite — nihče ne gleda ure. 💛", "🐢 Saj ni nujno vse! Izberite, kar vam je najbolj pri srcu, in uživajte."]));
    else if (a === "help") { await setState(chat, uid, name, { awaiting: "problem" }); await send(chat, `🤗 Seveda! ${W.please} na to sporočilo in povejte, kaj se dogaja — sporočilo bom poslal/-a vsem v skupini.`, { reply_markup: { force_reply: true, selective: true } }); }
    return;
  }
  if (kind === "ch") {
    await tg("answerCallbackQuery", { callback_query_id: cq.id, text: "💛" });
    await tg("editMessageReplyMarkup", { chat_id: chat, message_id: msg.message_id, reply_markup: { inline_keyboard: [] } });
    const trip = await tripInfo(ct.trip_id);
    if (a === "done") await send(chat, "🎉 Bravo! Če slik še niste naložile v album, jih dodajte — prav iz njih nastane vaša potopisna knjiga. 📖", { reply_markup: { inline_keyboard: [[urlBtn("📸 Naloži slike", appUrl(trip, "nalozi.html"))]] } });
    else await send(chat, pick(["💛 V redu, jutri je nov dan! Če se kaj ponudi, ne pozabite na sliko.", "😊 Nič hudega! Spomini so najpomembnejši — izzivi so samo bonus."]));
    return;
  }
  if (kind === "pack") {
    await tg("answerCallbackQuery", { callback_query_id: cq.id, text: "👍 Super!" });
    await tg("editMessageReplyMarkup", { chat_id: chat, message_id: msg.message_id, reply_markup: { inline_keyboard: [] } });
    return;
  }
  await tg("answerCallbackQuery", { callback_query_id: cq.id });
}

// ------------------------------------------------------------------ vstopna točka
Deno.serve(async (req) => {
  const url = new URL(req.url);
  const cfg = await loadCfg();
  if (req.method === "GET") return Response.json({ ok: true, configured: !!cfg.bot_token, ai: deepseekKey() ? "deepseek" : cfg.anthropic_key ? "anthropic" : "ni" });
  if (!cfg.bot_token) return Response.json({ ok: false, reason: "bot_token ni nastavljen" }, { status: 200 });

  if (url.searchParams.get("tick")) {
    if (req.headers.get("x-cron-secret") !== cfg.cron_secret) return new Response("forbidden", { status: 403 });
    try { return Response.json({ ok: true, sent: await tick() }); } catch (e) { console.log("tick napaka", e); return Response.json({ ok: false, error: String(e) }, { status: 500 }); }
  }
  if (url.searchParams.get("hook")) {
    if (req.headers.get("x-telegram-bot-api-secret-token") !== cfg.webhook_secret) return new Response("forbidden", { status: 403 });
    let update: any;
    try { update = await req.json(); } catch { return new Response("bad", { status: 400 }); }
    try {
      if (update.message) await onMessage(update.message);
      else if (update.callback_query) await onCallback(update.callback_query);
    } catch (e) { console.log("webhook napaka", e); }
    return new Response("ok");
  }
  return new Response("ni najdeno", { status: 404 });
});
