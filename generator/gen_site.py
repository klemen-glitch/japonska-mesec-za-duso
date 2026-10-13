# -*- coding: utf-8 -*-
"""Koren spletišča: vstopna stran s PIN-om, 404 preusmeritev, izklop starega service workerja.

Zagon: python3 gen_site.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.join(os.path.abspath(os.path.join(HERE, "..")), "site")
BASE = "/japonska-mesec-za-duso/"          # GitHub Pages pot (pri lastni domeni "/")
SB_URL = "https://ayejgzzaykbopojiacgn.supabase.co"
SB_KEY = "sb_publishable_vgNDW0KMTwSPstN0PhwySQ_SDuOUzn3"

GATE = r"""<!DOCTYPE html>
<html lang="sl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="robots" content="noindex,nofollow">
  <meta name="theme-color" content="#ffffff">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <title>Potovanja</title>
  <link rel="icon" href="__ICON__">
  <style>
    :root { --bg:#fff; --fg:#1d1d1f; --mute:#6e6e73; --line:#d2d2d7; --card:#f5f5f7; --acc:#0071e3; --err:#c0392b; }
    @media (prefers-color-scheme: dark) { :root { --bg:#000; --fg:#f5f5f7; --mute:#a1a1a6; --line:#3a3a3c; --card:#1c1c1e; --acc:#2997ff; --err:#ff6b5e; } }
    * { box-sizing: border-box; }
    html, body { margin:0; min-height:100%; background:var(--bg); color:var(--fg);
      font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",Roboto,Helvetica,Arial,sans-serif; -webkit-text-size-adjust:100%; }
    main { min-height:100vh; min-height:100dvh; display:flex; flex-direction:column; justify-content:center; align-items:center;
      padding:32px 20px calc(32px + env(safe-area-inset-bottom)); text-align:center; }
    .wrap { width:100%; max-width:380px; }
    .logo { font-size:56px; line-height:1; margin:0 0 14px; }
    h1 { font-size:28px; font-weight:700; letter-spacing:-.02em; margin:0 0 8px; }
    p.sub { margin:0 0 28px; color:var(--mute); font-size:17px; line-height:1.4; }
    form { display:flex; flex-direction:column; gap:12px; }
    input { font:inherit; font-size:26px; letter-spacing:.35em; text-align:center; padding:16px 12px; border-radius:14px;
      border:1px solid var(--line); background:var(--card); color:var(--fg); width:100%; outline:none; }
    input:focus { border-color:var(--acc); box-shadow:0 0 0 4px color-mix(in srgb, var(--acc) 22%, transparent); }
    input::placeholder { letter-spacing:.05em; font-size:17px; color:var(--mute); }
    button, .btn { font:inherit; font-size:17px; font-weight:600; padding:15px 18px; border-radius:14px; border:0; cursor:pointer;
      background:var(--acc); color:#fff; width:100%; display:block; text-decoration:none; }
    button:disabled { opacity:.55; }
    .btn.alt, button.alt { background:var(--card); color:var(--fg); border:1px solid var(--line); font-weight:500; }
    .msg { min-height:22px; margin:14px 0 0; font-size:15px; color:var(--mute); }
    .msg.err { color:var(--err); }
    .list { display:flex; flex-direction:column; gap:12px; margin:0 0 18px; text-align:left; }
    .trip { display:flex; align-items:center; gap:14px; padding:16px; border-radius:18px; background:var(--card);
      border:1px solid var(--line); color:var(--fg); text-decoration:none; }
    .trip .e { font-size:34px; }
    .trip b { display:block; font-size:18px; letter-spacing:-.01em; }
    .trip span.s { display:block; font-size:14px; color:var(--mute); margin-top:2px; }
    .trip .go { margin-left:auto; color:var(--mute); font-size:20px; }
    .foot { margin-top:26px; font-size:13px; color:var(--mute); }
    [hidden] { display:none !important; }
  </style>
</head>
<body>
<main>
  <div class="wrap">
    <div class="logo" aria-hidden="true">🧭</div>
    <h1 id="title">Potovanja</h1>
    <p class="sub" id="sub">Vpiši svojo kodo in odpri svoje potovanje.</p>

    <form id="f" autocomplete="off" novalidate>
      <input id="pin" type="password" inputmode="numeric" pattern="[0-9]*" maxlength="12" placeholder="koda"
             aria-label="Koda potovanja" autocomplete="off" autofocus>
      <button type="submit" id="go">Odpri</button>
    </form>

    <div id="chooser" hidden>
      <div class="list" id="list"></div>
      <button type="button" class="alt" id="other">Vpiši drugo kodo</button>
    </div>

    <p class="msg" id="msg" role="status" aria-live="polite"></p>
    <p class="foot">Vsako potovanje ima svojo kodo.</p>
  </div>
</main>
<script>
(function () {
  var SB = "__SB_URL__", KEY = "__SB_KEY__";
  var $ = function (id) { return document.getElementById(id); };
  var q = new URLSearchParams(location.search);
  var next = q.get("next") || "";
  var forceChoose = q.get("izpis") === "1";

  function readSession() { try { return JSON.parse(localStorage.getItem("trip_session") || "null"); } catch (e) { return null; } }
  function saveSession(s) { try { localStorage.setItem("trip_session", JSON.stringify(s)); } catch (e) {} }
  function clearSession() { try { localStorage.removeItem("trip_session"); } catch (e) {} }

  function say(t, err) { var m = $("msg"); m.textContent = t || ""; m.className = "msg" + (err ? " err" : ""); }

  function enter(pin) {
    return fetch(SB + "/rest/v1/rpc/trip_enter", {
      method: "POST",
      headers: { "apikey": KEY, "Authorization": "Bearer " + KEY, "Content-Type": "application/json" },
      body: JSON.stringify({ p_pin: pin })
    }).then(function (r) {
      return r.json().then(function (j) {
        if (!r.ok) { var e = new Error((j && j.message) || "napaka"); e.code = r.status; throw e; }
        return j;
      });
    });
  }

  function open(trip) { location.href = trip.slug + "/index.html"; }

  function showChooser(trips) {
    $("f").hidden = true; $("chooser").hidden = false;
    $("title").textContent = trips.length > 1 ? "Tvoja potovanja" : "Dobrodošli nazaj";
    $("sub").textContent = trips.length > 1 ? "Izberi potovanje." : "Potovanje je pripravljeno.";
    var list = $("list"); list.innerHTML = "";
    trips.forEach(function (t) {
      var a = document.createElement("a");
      a.className = "trip"; a.href = t.slug + "/index.html";
      a.innerHTML = '<span class="e"></span><span><b></b><span class="s"></span></span><span class="go">›</span>';
      a.querySelector(".e").textContent = t.emoji || "🧭";
      a.querySelector("b").textContent = t.title;
      a.querySelector(".s").textContent = t.subtitle || "";
      list.appendChild(a);
    });
  }

  function showForm(note) {
    $("chooser").hidden = true; $("f").hidden = false;
    $("title").textContent = "Potovanja";
    $("sub").textContent = "Vpiši svojo kodo in odpri svoje potovanje.";
    say(note || "", false);
    setTimeout(function () { $("pin").focus(); }, 50);
  }

  function route(trips) {
    var want = next && trips.filter(function (t) { return t.slug === next; })[0];
    if (want && !forceChoose) return open(want);
    if (trips.length === 1 && !forceChoose) return open(trips[0]);
    showChooser(trips);
  }

  $("f").addEventListener("submit", function (e) {
    e.preventDefault();
    var pin = $("pin").value.trim();
    if (!pin) { say("Vpiši kodo.", true); return; }
    $("go").disabled = true; say("Preverjam …");
    enter(pin).then(function (trips) {
      $("go").disabled = false;
      if (!trips.length) { $("pin").value = ""; say("Napačna koda. Poskusi znova.", true); return; }
      saveSession({ pin: pin, trips: trips, at: Date.now() });
      say("");
      forceChoose = false;
      route(trips);
    }).catch(function (err) {
      $("go").disabled = false;
      if (/prevec_poskusov/.test(err.message)) say("Preveč poskusov. Počakaj nekaj minut.", true);
      else say("Povezava ni uspela. Preveri internet.", true);
    });
  });

  $("other").addEventListener("click", function () { clearSession(); $("pin").value = ""; showForm(""); });

  // obstoječa seja: osveži seznam potovanj na strežniku (če je koda še veljavna)
  var s = readSession();
  if (s && s.pin && s.trips && s.trips.length) {
    say("");
    enter(s.pin).then(function (trips) {
      if (!trips.length) { clearSession(); showForm("Seja je potekla. Vpiši kodo."); return; }
      saveSession({ pin: s.pin, trips: trips, at: Date.now() });
      route(trips);
    }).catch(function () { route(s.trips); });   // brez povezave: uporabi shranjeno
  } else {
    showForm(q.get("old") ? "Naslov se je spremenil. Vpiši kodo za vstop." : "");
  }
})();
</script>
</body>
</html>
"""

NOT_FOUND = r"""<!DOCTYPE html>
<html lang="sl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><title>Preusmerjam …</title>
<script>
(function () {
  var base = "__BASE__";
  if (location.pathname.indexOf(base) !== 0) base = "/";
  location.replace(base + "index.html?old=1");
})();
</script></head>
<body style="font-family:-apple-system,Helvetica,Arial,sans-serif;text-align:center;padding:40px 20px">
<p>Preusmerjam na vstopno stran …</p>
<p><a href="__BASE__index.html">Če se nič ne zgodi, tapni tukaj.</a></p>
</body></html>
"""

KILL_SW = r"""/* Izklop starega service workerja (prejšnja različica spletišča je bila v korenu).
   Izbriše stare predpomnilnike in se odjavi; potovanja imajo svoje service workerje v svojih mapah. */
self.addEventListener("install", function () { self.skipWaiting(); });
self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys()
      .then(function (keys) { return Promise.all(keys.map(function (k) { return caches.delete(k); })); })
      .then(function () { return self.registration.unregister(); })
      .then(function () { return self.clients.matchAll({ type: "window" }); })
      .then(function (clients) { clients.forEach(function (c) { try { c.navigate(c.url); } catch (e) {} }); })
  );
});
self.addEventListener("fetch", function () { /* ne predpomni nič */ });
"""


def main():
    os.makedirs(SITE_DIR, exist_ok=True)
    icon = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%A7%AD%3C/text%3E%3C/svg%3E"
    gate = (GATE.replace("__SB_URL__", SB_URL).replace("__SB_KEY__", SB_KEY).replace("__ICON__", icon))
    with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(gate)
    with open(os.path.join(SITE_DIR, "404.html"), "w", encoding="utf-8") as f:
        f.write(NOT_FOUND.replace("__BASE__", BASE))
    with open(os.path.join(SITE_DIR, "sw.js"), "w", encoding="utf-8") as f:
        f.write(KILL_SW)
    open(os.path.join(SITE_DIR, ".nojekyll"), "a").close()
    print("site root written: index.html, 404.html, sw.js")


if __name__ == "__main__":
    main()
