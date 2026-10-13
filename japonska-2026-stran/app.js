/* ============================================================
   Japonska 2026 — nastavitve strani
   ============================================================ */

/* ▼▼▼ TUKAJ prilepi povezavo do deljenega Google Photos albuma
   ali Google Drive mape (med narekovaje). Primer:
   var PHOTO_ALBUM_URL = "https://photos.app.goo.gl/abc123";     */
var PHOTO_ALBUM_URL = "";

document.addEventListener("DOMContentLoaded", function () {
  var btn = document.getElementById("photo-link");
  if (btn) {
    if (PHOTO_ALBUM_URL) {
      btn.href = PHOTO_ALBUM_URL;
      btn.target = "_blank";
      btn.rel = "noopener";
    } else {
      // Dokler povezave še ni, gumb zamenjamo s prijaznim obvestilom.
      var note = document.createElement("p");
      note.className = "photo-note";
      note.textContent = "📸 Povezava do skupnega foto albuma bo dodana kmalu.";
      btn.replaceWith(note);
    }
  }
});

/* Meni: gumb odpre/zapre pregleden meni. */
document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.getElementById("menu-toggle");
  var menu = document.getElementById("main-menu");
  var backdrop = document.getElementById("menu-backdrop");
  if (!toggle || !menu) return;

  function setOpen(open) {
    menu.hidden = !open;
    if (backdrop) backdrop.hidden = !open;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.style.overflow = open ? "hidden" : "";
  }
  toggle.addEventListener("click", function (e) {
    e.stopPropagation();
    setOpen(menu.hidden);
  });
  if (backdrop) backdrop.addEventListener("click", function () { setOpen(false); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !menu.hidden) setOpen(false);
  });
  menu.addEventListener("click", function (e) { e.stopPropagation(); });
  document.addEventListener("click", function () {
    if (!menu.hidden) setOpen(false);
  });
});

/* Kontrolni seznam: obkljukano se shrani v telefon (localStorage). */
document.addEventListener("DOMContentLoaded", function () {
  var boxes = document.querySelectorAll('input[type="checkbox"][data-persist]');
  if (!boxes.length) return;
  var progress = document.getElementById("chk-progress");

  function update() {
    if (!progress) return;
    var done = 0;
    boxes.forEach(function (b) { if (b.checked) done++; });
    progress.textContent = "Urejeno: " + done + " / " + boxes.length;
  }

  boxes.forEach(function (cb) {
    var key = "chk:" + cb.id;
    try { if (localStorage.getItem(key) === "1") cb.checked = true; } catch (e) {}
    cb.addEventListener("change", function () {
      try { localStorage.setItem(key, cb.checked ? "1" : "0"); } catch (e) {}
      update();
    });
  });

  var reset = document.getElementById("chk-reset");
  if (reset) {
    reset.addEventListener("click", function () {
      boxes.forEach(function (cb) {
        cb.checked = false;
        try { localStorage.removeItem("chk:" + cb.id); } catch (e) {}
      });
      update();
    });
  }
  update();
});

/* Zemljevidi (Leaflet): statični predogled s pravo povečavo za vsak kraj.
   Za raziskovanje je tu gumb »Odpri na Google Zemljevidu«. */
document.addEventListener("DOMContentLoaded", function () {
  var els = document.querySelectorAll(".area-map[data-lat]");
  if (!els.length || typeof L === "undefined") return;
  /* Vsi zemljevidi kažejo celotno Japonsko z označbo kraja —
     da se vidi, kje v državi je. Za podrobnosti je gumb Google Zemljevid. */
  var JAPAN_VIEW = [37.9, 137.6];
  var JAPAN_ZOOM = 5;
  els.forEach(function (el) {
    var lat = parseFloat(el.getAttribute("data-lat"));
    var lon = parseFloat(el.getAttribute("data-lon"));
    if (isNaN(lat) || isNaN(lon)) return;
    try {
      var map = L.map(el, {
        center: JAPAN_VIEW, zoom: JAPAN_ZOOM,
        dragging: false, scrollWheelZoom: false, doubleClickZoom: false,
        boxZoom: false, keyboard: false, touchZoom: false,
        zoomControl: false, attributionControl: true
      });
      L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19, attribution: "© OpenStreetMap"
      }).addTo(map);
      L.circleMarker([lat, lon], {
        radius: 10, color: "#5e1a25", weight: 3,
        fillColor: "#c96a2a", fillOpacity: 0.95
      }).addTo(map);
      // osveži velikost, ko je kontejner dokončno postavljen
      setTimeout(function () { map.invalidateSize(); }, 200);
    } catch (e) { /* brez interneta zemljevid pač ostane prazen */ }
  });
});

/* ============================================================
   »Danes«: kateri dan poti je danes (po datumu v telefonu).
   Za preizkus: dodaj ?dan=2026-11-08 v naslov strani.
   ============================================================ */
document.addEventListener("DOMContentLoaded", function () {
  var box = document.getElementById("today");
  var dataEl = document.getElementById("trip-data");
  if (!dataEl) return;
  var days = [];
  try { days = JSON.parse(dataEl.textContent); } catch (e) { return; }
  if (!days.length) return;

  function pad(n) { return (n < 10 ? "0" : "") + n; }
  var q = (location.search.match(/dan=(\d{4}-\d{2}-\d{2})/) || [])[1];
  var now = new Date();
  var todayIso = q || (now.getFullYear() + "-" + pad(now.getMonth() + 1) + "-" + pad(now.getDate()));
  function toDate(iso) { var p = iso.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  var diff = Math.round((toDate(days[0].iso) - toDate(todayIso)) / 86400000);

  // označi današnji dan v načrtu poti
  document.querySelectorAll(".it-day[data-iso]").forEach(function (li) {
    if (li.getAttribute("data-iso") === todayIso) li.classList.add("is-today");
  });
  if (!box) return;

  var cur = null;
  days.forEach(function (d) { if (d.iso === todayIso) cur = d; });
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  var html = "";
  if (cur) {
    var link = cur.k ? '<a class="today-btn" href="' + cur.k + '.html">Odpri vodnik za ta kraj →</a>' : "";
    html = '<div class="today-kicker">📅 Danes · ' + esc(cur.date) + "</div>" +
      '<h2>Dan ' + cur.d + " od " + days.length + " — " + esc(cur.t) + "</h2>" +
      '<p class="today-region">' + esc(cur.r) + "</p><p>" + esc(cur.p) + "</p>" +
      '<div class="today-actions">' + link +
      '<a class="today-btn alt" href="izziv.html">📸 Foto izzivi</a>' +
      '<a class="today-btn alt" href="nujno.html">🆘 Nujno</a></div>';
  } else if (diff > 0) {
    html = '<div class="today-kicker">✈️ Odštevanje</div><h2>Še ' + diff + (diff === 1 ? " dan" : (diff === 2 ? " dni" : " dni")) +
      " do odhoda</h2><p>Potovanje se začne " + esc(days[0].date) + ". Poglejte <a href=\"priprave.html\">priprave</a> in kontrolni seznam.</p>";
  } else {
    html = '<div class="today-kicker">🌸 Potovanje je za vami</div><h2>Mata ne — se še vidimo!</h2>' +
      '<p>Poglejte <a href="nalozi.html">skupni album</a> in iz slik sestavite svojo potopisno knjigo.</p>';
  }
  box.innerHTML = html;
  box.hidden = false;
});

/* ============================================================
   Pregledni zemljevid poti (Leaflet): vseh 13 postaj po vrsti.
   ============================================================ */
document.addEventListener("DOMContentLoaded", function () {
  var el = document.getElementById("route-map");
  var dataEl = document.getElementById("route-data");
  if (!el || !dataEl || typeof L === "undefined") return;
  var st = [];
  try { st = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var map;
  try {
    map = L.map(el, {
      zoomControl: false, attributionControl: true, dragging: false, scrollWheelZoom: false,
      doubleClickZoom: false, boxZoom: false, keyboard: false, touchZoom: false
    });
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 19, attribution: "© OpenStreetMap" }).addTo(map);
    var byKey = {};
    st.forEach(function (s) { byKey[s.k] = s; });

    var base = st.filter(function (s) { return !s.day; }).map(function (s) { return [s.lat, s.lon]; });
    L.polyline(base, { color: "#9c2a3c", weight: 4, opacity: 0.85 }).addTo(map);
    st.forEach(function (s) {
      if (s.day && s.base && byKey[s.base]) {
        L.polyline([[byKey[s.base].lat, byKey[s.base].lon], [s.lat, s.lon]],
          { color: "#bd5f2c", weight: 3, opacity: 0.9, dashArray: "6 8" }).addTo(map);
      }
    });
    var pts = [];
    st.forEach(function (s) {
      pts.push([s.lat, s.lon]);
      var icon = L.divIcon({
        className: "rm-wrap",
        html: '<span class="rm-pin' + (s.day ? " rm-day" : "") + '">' + s.i + "</span>",
        iconSize: [22, 22], iconAnchor: [11, 11]
      });
      var m = L.marker([s.lat, s.lon], { icon: icon, keyboard: false }).addTo(map);
      m.bindPopup('<a href="' + s.k + '.html"><strong>' + s.i + ". " + s.e + " " + s.n + "</strong><br>Odpri vodnik →</a>");
    });
    map.fitBounds(pts, { padding: [22, 22] });
    setTimeout(function () { map.invalidateSize(); map.fitBounds(pts, { padding: [22, 22] }); }, 250);
  } catch (e) { /* brez interneta zemljevid ostane prazen */ }
});

/* ============================================================
   Obiskano: gumb na straneh postaj, oznake na domači strani.
   ============================================================ */
document.addEventListener("DOMContentLoaded", function () {
  function get(k) { try { return localStorage.getItem("visited:" + k) === "1"; } catch (e) { return false; } }
  function set(k, v) { try { if (v) localStorage.setItem("visited:" + k, "1"); else localStorage.removeItem("visited:" + k); } catch (e) {} }

  document.querySelectorAll(".visit-btn[data-visit]").forEach(function (b) {
    var k = b.getAttribute("data-visit");
    function paint() {
      var on = get(k);
      b.classList.toggle("on", on);
      b.textContent = on ? "✅ Obiskano" : "☐ Označi kot obiskano";
    }
    paint();
    b.addEventListener("click", function () { set(k, !get(k)); paint(); });
  });

  var tags = document.querySelectorAll("[data-visit-tag]");
  var n = 0;
  tags.forEach(function (t) {
    var on = get(t.getAttribute("data-visit-tag"));
    t.hidden = !on;
    if (on) n++;
  });
  var sum = document.getElementById("visit-sum");
  if (sum) sum.textContent = tags.length ? "✅ Obiskanih postaj: " + n + " / " + tags.length : "";
});

/* ============================================================
   Izgovorjava (🔊) in kartice »pokaži domačinu« čez cel zaslon.
   ============================================================ */
document.addEventListener("DOMContentLoaded", function () {
  var canSpeak = "speechSynthesis" in window && "SpeechSynthesisUtterance" in window;

  function say(text) {
    if (!canSpeak) return;
    try {
      window.speechSynthesis.cancel();
      var u = new SpeechSynthesisUtterance(text);
      u.lang = "ja-JP";
      u.rate = 0.85;
      var voices = window.speechSynthesis.getVoices() || [];
      for (var i = 0; i < voices.length; i++) {
        if ((voices[i].lang || "").toLowerCase().indexOf("ja") === 0) { u.voice = voices[i]; break; }
      }
      window.speechSynthesis.speak(u);
    } catch (e) {}
  }
  if (canSpeak) { try { window.speechSynthesis.getVoices(); } catch (e) {} }

  document.querySelectorAll(".say[data-say]").forEach(function (b) {
    if (!canSpeak) { b.hidden = true; return; }
    b.addEventListener("click", function () { say(b.getAttribute("data-say")); });
  });

  var cards = document.querySelectorAll(".show-card");
  if (!cards.length) return;
  var overlay = document.createElement("div");
  overlay.className = "show-overlay";
  overlay.hidden = true;
  overlay.innerHTML = '<div class="so-inner"><p class="so-sl"></p><p class="so-jp" lang="ja"></p><p class="so-ro"></p>' +
    '<div class="so-btns"><button type="button" class="so-say">🔊 Poslušaj</button>' +
    '<button type="button" class="so-close">✕ Zapri</button></div></div>';
  document.body.appendChild(overlay);
  var cur = "";
  function close() { overlay.hidden = true; document.body.style.overflow = ""; }
  overlay.querySelector(".so-close").addEventListener("click", function (e) { e.stopPropagation(); close(); });
  var sb = overlay.querySelector(".so-say");
  if (!canSpeak) sb.hidden = true;
  sb.addEventListener("click", function (e) { e.stopPropagation(); say(cur); });
  overlay.addEventListener("click", close);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !overlay.hidden) close(); });

  cards.forEach(function (c) {
    c.addEventListener("click", function () {
      cur = c.getAttribute("data-jp") || "";
      overlay.querySelector(".so-sl").textContent = c.getAttribute("data-sl") || "";
      overlay.querySelector(".so-jp").textContent = cur;
      overlay.querySelector(".so-ro").textContent = c.getAttribute("data-ro") || "";
      overlay.classList.toggle("red", c.classList.contains("red"));
      overlay.hidden = false;
      document.body.style.overflow = "hidden";
    });
  });
});

/* Zapiski, ki se shranijo v telefon (textarea[data-save]). */
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("textarea[data-save]").forEach(function (t) {
    var key = "note:" + t.getAttribute("data-save");
    try { var v = localStorage.getItem(key); if (v) t.value = v; } catch (e) {}
    t.addEventListener("input", function () { try { localStorage.setItem(key, t.value); } catch (e) {} });
  });
});

/* ============================================================
   Predstavitev (wizard): Naprej / Nazaj skozi vse funkcije.
   ============================================================ */
document.addEventListener("DOMContentLoaded", function () {
  var wiz = document.getElementById("wiz");
  if (!wiz) return;
  var steps = [].slice.call(wiz.querySelectorAll(".wiz-step"));
  var prev = document.getElementById("wiz-prev");
  var next = document.getElementById("wiz-next");
  var count = document.getElementById("wiz-count");
  var fill = document.getElementById("wiz-fill");
  var dots = document.getElementById("wiz-dots");
  var cur = 0, spotEl = null;

  steps.forEach(function (_, i) {
    var d = document.createElement("i");
    d.addEventListener("click", function () { go(i); });
    dots.appendChild(d);
  });
  dots.style.pointerEvents = "auto";

  function markSeen() { try { localStorage.setItem("tour_seen", "1"); } catch (e) {} }

  function go(i) {
    if (i < 0 || i >= steps.length) return;
    cur = i;
    steps.forEach(function (s, k) { s.hidden = k !== i; });
    count.textContent = (i + 1) + " / " + steps.length;
    fill.style.width = Math.round((i + 1) * 100 / steps.length) + "%";
    [].forEach.call(dots.children, function (d, k) { d.className = k === i ? "on" : (k < i ? "done" : ""); });
    prev.disabled = i === 0;
    var last = i === steps.length - 1;
    next.textContent = last ? "Končaj ✓" : "Naprej →";
    if (last) markSeen();
    if (spotEl) { spotEl.classList.remove("spot"); spotEl = null; }
    var sel = steps[i].getAttribute("data-spot");
    if (sel) { spotEl = document.querySelector(sel); if (spotEl) spotEl.classList.add("spot"); }
    try { history.replaceState(null, "", "#" + (i + 1)); } catch (e) {}
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  prev.addEventListener("click", function () { go(cur - 1); });
  next.addEventListener("click", function () {
    if (cur === steps.length - 1) { markSeen(); location.href = "index.html"; } else { go(cur + 1); }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") go(cur + 1);
    else if (e.key === "ArrowLeft") go(cur - 1);
  });
  var x0 = null;
  wiz.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  wiz.addEventListener("touchend", function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 70) go(dx < 0 ? cur + 1 : cur - 1);
  }, { passive: true });

  // demo: odklep presenečenja
  document.querySelectorAll('[data-demo="unlock"]').forEach(function (box) {
    var btn = box.querySelector(".demo-btn"), lock = box.querySelector(".demo-locked"),
        open = box.querySelector(".demo-open"), mark = box.querySelector(".demo-mark");
    var on = false;
    btn.addEventListener("click", function () {
      on = !on;
      lock.hidden = on; open.hidden = !on;
      mark.textContent = on ? "✅" : "📸";
      btn.textContent = on ? "↺ Ponastavi demo" : "▶ Preizkusi: naloži sliko";
    });
  });

  var h = parseInt((location.hash || "").replace("#", ""), 10);
  go(isNaN(h) ? 0 : Math.min(Math.max(h - 1, 0), steps.length - 1));
});

/* Pasica »Prvič tukaj?« na domači strani. */
document.addEventListener("DOMContentLoaded", function () {
  var b = document.getElementById("tour-banner");
  if (!b) return;
  var seen = false;
  try { seen = localStorage.getItem("tour_seen") === "1"; } catch (e) {}
  if (seen) return;
  b.hidden = false;
  var x = document.createElement("button");
  x.type = "button"; x.className = "tb-x"; x.setAttribute("aria-label", "Skrij"); x.textContent = "✕";
  x.addEventListener("click", function (e) {
    e.preventDefault(); e.stopPropagation();
    try { localStorage.setItem("tour_seen", "1"); } catch (er) {}
    b.hidden = true;
  });
  b.appendChild(x);
});

/* Offline podpora (PWA): stran si telefon zapomni,
   da osnovne informacije delujejo tudi brez interneta. */
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("sw.js").catch(function () {
      /* če ne uspe, stran normalno deluje naprej */
    });
  });
}
