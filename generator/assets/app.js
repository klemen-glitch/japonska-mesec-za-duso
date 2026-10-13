/* ============================================================
   Nastavitve strani (skupne vsem potovanjem; window.TRIP pride iz glave strani)
   ============================================================ */

/* Ključi v telefonu so ločeni po potovanju (prvo potovanje ostane brez predpone,
   da se ohrani že shranjeno). */
function SK(k) {
  var id = (window.TRIP && TRIP.id) || "";
  return (id && id !== "japonska") ? id + ":" + k : k;
}

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
    var key = SK("chk:" + cb.id);
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
        try { localStorage.removeItem(SK("chk:" + cb.id)); } catch (e) {}
      });
      update();
    });
  }
  update();
});

/* Zemljevidi kraja (Leaflet). Raven povečave sledi kontekstu:
   • »Kraj« (privzeto): prilagodi se točkam (znamenitosti, lokali) — raven mesta/kraja;
   • »Država«: kje v državi je kraj (TRIP.country).
   Pregledni zemljevid poti na domači strani se prilagodi vsem postajam (spodaj). */
document.addEventListener("DOMContentLoaded", function () {
  var els = document.querySelectorAll(".area-map[data-lat]");
  if (!els.length || typeof L === "undefined") return;
  var TRP = window.TRIP || {};
  var CTRY = TRP.country || { c: [46.15, 14.99], z: 7 };
  var PIN = TRP.color || "#9c2a3c";
  function esc(x) { return String(x).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function gUrl(q) { return "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(q); }

  els.forEach(function (el) {
    var lat = parseFloat(el.getAttribute("data-lat"));
    var lon = parseFloat(el.getAttribute("data-lon"));
    var z0 = parseInt(el.getAttribute("data-zoom"), 10) || 13;
    if (isNaN(lat) || isNaN(lon)) return;
    var sec = el.closest(".map-section") || el.parentNode;
    var pts = [];
    var pe = sec.querySelector("script.map-pts");
    if (pe) { try { pts = JSON.parse(pe.textContent); } catch (er) {} }
    try {
      var map = L.map(el, {
        zoomControl: true, attributionControl: true, scrollWheelZoom: false, doubleClickZoom: true,
        boxZoom: false, keyboard: false, touchZoom: false, dragging: !L.Browser.mobile, tap: true
      });
      L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 19, attribution: "© OpenStreetMap" }).addTo(map);

      var cityLayer = L.layerGroup();
      var latlngs = [];
      pts.forEach(function (p) {
        var food = p.t === "f";
        var icon = L.divIcon({
          className: "rm-wrap",
          html: '<span class="rm-pin' + (food ? " rm-food" : "") + '">' + (food ? "🍴" : p.n) + "</span>",
          iconSize: food ? [20, 20] : [24, 24], iconAnchor: food ? [10, 10] : [12, 12]
        });
        var mk = L.marker([p.lat, p.lon], { icon: icon, keyboard: false, riseOnHover: true });
        mk.bindPopup("<strong>" + esc(p.name) + '</strong><br><a href="' + gUrl(p.q) + '" target="_blank" rel="noopener">Odpri v Google Zemljevidih →</a>');
        cityLayer.addLayer(mk);
        if (!food) latlngs.push([p.lat, p.lon]);          // pogled določajo znamenitosti; lokali le dopolnijo
      });
      if (!latlngs.length) pts.forEach(function (p) { latlngs.push([p.lat, p.lon]); });
      // postaja sama (središče kraja), če ni drugih točk
      var home = L.circleMarker([lat, lon], { radius: 10, color: "#fff", weight: 3, fillColor: PIN, fillOpacity: 0.95 });

      var legend = sec.querySelector(".map-legend");
      function showCity() {
        if (legend) legend.hidden = false;
        map.eachLayer(function (l) { if (l === home || l === cityLayer) map.removeLayer(l); });
        if (pts.length) {
          cityLayer.addTo(map);
          if (latlngs.length > 1) map.fitBounds(latlngs, { padding: [30, 30], maxZoom: 16 });
          else map.setView(latlngs[0], 15);
        } else {
          home.addTo(map);
          map.setView([lat, lon], Math.max(z0, 12));
        }
      }
      function showCountry() {
        if (legend) legend.hidden = true;
        map.eachLayer(function (l) { if (l === cityLayer) map.removeLayer(l); });
        home.addTo(map);
        map.setView(CTRY.c, CTRY.z);
      }

      var btns = sec.querySelectorAll(".map-modes button");
      btns.forEach(function (b) {
        b.addEventListener("click", function () {
          btns.forEach(function (x) { x.classList.toggle("on", x === b); });
          if (b.getAttribute("data-mode") === "country") showCountry(); else showCity();
        });
      });

      showCity();
      // osveži velikost, ko je kontejner dokončno postavljen (in ponovno prilagodi pogled)
      setTimeout(function () {
        map.invalidateSize();
        var on = sec.querySelector(".map-modes button.on");
        if (!on || on.getAttribute("data-mode") !== "country") showCity();
      }, 250);
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
      " do odhoda</h2><p>" + ((window.TRIP && TRIP.t && TRIP.t.pre) ? TRIP.t.pre.replace("{date}", esc(days[0].date)) : ("Potovanje se začne " + esc(days[0].date) + ". Poglejte <a href=\"priprave.html\">priprave</a> in kontrolni seznam.")) + "</p>";
    if (diff === 1) html = html.replace("Še 1 dan do odhoda", "Jutri gremo!");
  } else {
    var aft = (window.TRIP && TRIP.after) || ["Mata ne — se še vidimo!", "Poglejte <a href=\"nalozi.html\">skupni album</a> in iz slik sestavite svojo potopisno knjigo."];
    html = '<div class="today-kicker">🌸 Potovanje je za vami</div><h2>' + esc(aft[0]) + '</h2><p>' + aft[1] + '</p>';
  }
  box.innerHTML = html;
  box.hidden = false;
  // vreme za današnjo (ali prvo) postajo
  var kk = cur ? cur.k : (diff > 0 ? days[0].k : "");
  var rdEl = document.getElementById("route-data");
  if (kk && rdEl) {
    try {
      JSON.parse(rdEl.textContent).forEach(function (st) {
        if (st.k !== kk) return;
        var w = document.createElement("div");
        w.className = "wx-box wx-compact"; w.hidden = true;
        w.setAttribute("data-lat", st.lat); w.setAttribute("data-lon", st.lon);
        w.setAttribute("data-compact", "1"); w.setAttribute("data-place", st.n);
        if (!cur && diff > 0) w.setAttribute("data-from", days[0].iso);
        box.appendChild(w); initWxBox(w);
      });
    } catch (er) {}
  }
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
    L.polyline(base, { color: (window.TRIP && TRIP.color) || "#9c2a3c", weight: 4, opacity: 0.85 }).addTo(map);
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
  function get(k) { try { return localStorage.getItem(SK("visited:" + k)) === "1"; } catch (e) { return false; } }
  function set(k, v) { try { if (v) localStorage.setItem(SK("visited:" + k), "1"); else localStorage.removeItem(SK("visited:" + k)); } catch (e) {} }

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
    var key = SK("note:" + t.getAttribute("data-save"));
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

  function markSeen() { try { localStorage.setItem(SK("tour_seen"), "1"); } catch (e) {} }

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
  try { seen = localStorage.getItem(SK("tour_seen")) === "1"; } catch (e) {}
  if (seen) return;
  b.hidden = false;
  var x = document.createElement("button");
  x.type = "button"; x.className = "tb-x"; x.setAttribute("aria-label", "Skrij"); x.textContent = "✕";
  x.addEventListener("click", function (e) {
    e.preventDefault(); e.stopPropagation();
    try { localStorage.setItem(SK("tour_seen"), "1"); } catch (er) {}
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

/* ============================================================
   Vreme (Open-Meteo, brez ključa), zanimivost dneva, pretvornik valut
   ============================================================ */
var WX_DAYS = ["ned", "pon", "tor", "sre", "čet", "pet", "sob"];
var WX_MON = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "avg", "sep", "okt", "nov", "dec"];

function wxCode(c) {
  if (c === 0) return ["☀️", "Jasno"];
  if (c === 1 || c === 2) return ["🌤️", "Delno oblačno"];
  if (c === 3) return ["☁️", "Oblačno"];
  if (c === 45 || c === 48) return ["🌫️", "Megla"];
  if (c >= 51 && c <= 57) return ["🌦️", "Rosenje"];
  if (c >= 61 && c <= 67) return ["🌧️", "Dež"];
  if (c >= 71 && c <= 77) return ["🌨️", "Sneg"];
  if (c >= 80 && c <= 82) return ["🌦️", "Plohe"];
  if (c === 85 || c === 86) return ["🌨️", "Snežne plohe"];
  if (c >= 95) return ["⛈️", "Nevihte"];
  return ["🌡️", "—"];
}

function wxFetch(url, cacheKey, maxAgeMin) {
  var cached = null;
  try { cached = JSON.parse(localStorage.getItem(cacheKey) || "null"); } catch (e) {}
  if (cached && Date.now() - cached.t < maxAgeMin * 60000) return Promise.resolve(cached.d);
  return fetch(url).then(function (r) { if (!r.ok) throw new Error("wx"); return r.json(); }).then(function (d) {
    try { localStorage.setItem(cacheKey, JSON.stringify({ t: Date.now(), d: d })); } catch (e) {}
    return d;
  }).catch(function (e) { if (cached) return cached.d; throw e; });
}

function wxHM(iso) { return (iso || "").slice(11, 16).replace(/^0/, ""); }

function wxTip(days) {
  if (!days.length) return "";
  var minT = Math.min.apply(null, days.map(function (d) { return d.min; }));
  var maxT = Math.max.apply(null, days.map(function (d) { return d.max; }));
  var rain = Math.max.apply(null, days.map(function (d) { return d.rain || 0; }));
  var fog = days.some(function (d) { return d.code === 45 || d.code === 48; });
  var tips = [];
  if (rain >= 50) tips.push("☔ Verjetnost dežja je visoka — dežnik ali pelerina v nahrbtnik, nepremočljivi čevlji.");
  else if (rain >= 25) tips.push("🌂 Možen je dež — majhen dežnik naj bo pri roki.");
  if (minT <= 5) tips.push("🧣 Hladna jutra — topla jakna, kapa in rokavice.");
  else if (minT <= 10) tips.push("🧥 Sveža jutra — plasti: majica, pulover, jakna.");
  if (maxT >= 24) tips.push("🧴 Toplo čez dan — lahka oblačila, voda in zaščita pred soncem.");
  if (fog) tips.push("🌫️ Jutranja megla je možna — za razglede počakajte, da se razkadi.");
  if (!tips.length) tips.push("😊 Vreme je prijazno — udobna oblačila v plasteh zadoščajo.");
  return tips.join(" ");
}

function initWxBox(el) {
  var lat = el.getAttribute("data-lat"), lon = el.getAttribute("data-lon");
  if (!lat || !lon || !window.fetch) return;
  var compact = el.getAttribute("data-compact") === "1";
  el.innerHTML = '<div class="wx-main"></div><div class="wx-hist-slot"></div>';
  var mainEl = el.querySelector(".wx-main"), histEl = el.querySelector(".wx-hist-slot");
  var stay = (el.getAttribute("data-stay") || "").split(",");
  var place = el.getAttribute("data-place") || "";
  var url = "https://api.open-meteo.com/v1/forecast?latitude=" + lat + "&longitude=" + lon +
    "&current=temperature_2m,weather_code&daily=weather_code,temperature_2m_max,temperature_2m_min," +
    "precipitation_probability_max,sunrise,sunset&timezone=auto&forecast_days=7";
  wxFetch(url, "wx:" + lat + "," + lon, 120).then(function (d) {
    var dl = d.daily, days = [];
    for (var i = 0; i < dl.time.length; i++) {
      days.push({ date: dl.time[i], code: dl.weather_code[i], max: dl.temperature_2m_max[i], min: dl.temperature_2m_min[i],
        rain: dl.precipitation_probability_max[i], sunrise: dl.sunrise[i], sunset: dl.sunset[i] });
    }
    var cur = wxCode(d.current.weather_code);
    var ttl = el.getAttribute("data-title");
    var html = (ttl ? "<h2>" + ttl + "</h2>" : "") + '<div class="wx-head"><span class="wx-ic">' + cur[0] + '</span><span class="wx-t">' + Math.round(d.current.temperature_2m) +
      '°C</span><span class="wx-d">' + (place ? place + " · " : "") + cur[1] + " zdaj</span></div>";
    var from = el.getAttribute("data-from"), start = 0;
    if (from) { for (var q = 0; q < days.length; q++) { if (days[q].date >= from) { start = q; break; } } }
    var shown = compact ? days.slice(start, start + 3) : days;
    html += '<div class="wx-days">' + shown.map(function (x) {
      var dt = new Date(x.date + "T12:00:00"), c = wxCode(x.code);
      return '<div class="wx-day"><b>' + WX_DAYS[dt.getDay()] + " " + dt.getDate() + ".</b><span class=\"wx-i\">" + c[0] + "</span><span>" +
        Math.round(x.min) + "–" + Math.round(x.max) + "°</span><i>" + (x.rain != null ? "💧" + x.rain + " %" : "") + "</i></div>";
    }).join("") + "</div>";
    var sd = compact ? shown[0] : days[0], sdt = new Date(sd.date + "T12:00:00");
    html += '<p class="wx-sun">🌅 ' + wxHM(sd.sunrise) + " · 🌇 " + wxHM(sd.sunset) + " (" + (sd === days[0] ? "danes" : sdt.getDate() + ". " + WX_MON[sdt.getMonth()]) + ")</p>";
    var rel = compact ? shown : days.slice(0, 5);
    html += '<p class="wx-tip">' + wxTip(rel) + "</p>";
    mainEl.innerHTML = html;
    el.hidden = false;
  }).catch(function () { /* brez interneta vreme ostane skrito */ });

  // podnebje: lani ob istem času (če je potovanje čez več kot 14 dni)
  if (!compact && stay.length === 2 && stay[0]) {
    var s = new Date(stay[0] + "T12:00:00"), e = new Date(stay[1] + "T12:00:00");
    var ahead = (s - new Date()) / 86400000;
    if (ahead > 14) {
      function sh(dt) { var c = new Date(dt); c.setFullYear(c.getFullYear() - 1); return c.toISOString().slice(0, 10); }
      var u2 = "https://archive-api.open-meteo.com/v1/archive?latitude=" + lat + "&longitude=" + lon + "&start_date=" + sh(s) +
        "&end_date=" + sh(new Date(e.getTime() - 86400000)) + "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto";
      wxFetch(u2, "wxh:" + lat + "," + lon + ":" + stay[0], 60 * 24 * 30).then(function (h) {
        var mx = h.daily.temperature_2m_max, mn = h.daily.temperature_2m_min, pr = h.daily.precipitation_sum;
        if (!mx || !mx.length) return;
        var avg = function (a) { return a.reduce(function (p, c) { return p + c; }, 0) / a.length; };
        var wet = pr.filter(function (v) { return v >= 1; }).length;
        var p = document.createElement("p");
        p.className = "wx-hist";
        p.innerHTML = "📊 Lani ob istem času (" + (s.getDate()) + ". " + WX_MON[s.getMonth()] + "–" + (new Date(e.getTime() - 86400000).getDate()) + ". " +
          WX_MON[new Date(e.getTime() - 86400000).getMonth()] + "): povprečno " + Math.round(avg(mn)) + "–" + Math.round(avg(mx)) +
          " °C, dež v " + wet + " od " + pr.length + " dni. Napoved za vaše dni bo na voljo 2 tedna pred odhodom.";
        histEl.appendChild(p);
        el.hidden = false;
      }).catch(function () {});
    }
  }
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".wx-box[data-lat]").forEach(initWxBox);

  /* Zanimivost dneva */
  var fe = document.getElementById("facts-data"), fbox = document.getElementById("fact-today");
  if (fe && fbox) {
    var facts = [];
    try { facts = JSON.parse(fe.textContent); } catch (e) {}
    if (facts.length) {
      var d0 = new Date(); var seed = d0.getFullYear() * 400 + d0.getMonth() * 31 + d0.getDate();
      var idx = seed % facts.length;
      function show() {
        var f = facts[idx];
        fbox.innerHTML = '<div class="ft-kicker">💡 Zanimivost dneva' + (f.s ? " · " + f.s : "") + '</div><p>' + f.t.replace(/[&<>]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]; }) +
          '</p><button type="button" class="ft-next">🔀 Še ena</button>';
        fbox.hidden = false;
        fbox.querySelector(".ft-next").addEventListener("click", function () { idx = (idx + 1 + Math.floor(Math.random() * (facts.length - 1))) % facts.length; show(); });
      }
      show();
    }
  }

  /* Pretvornik EUR ↔ JPY (ECB prek Frankfurterja; ob napaki shranjen ali okviren tečaj) */
  document.querySelectorAll(".fx-box").forEach(function (box) {
    var rate = 175, label = "okviren tečaj";
    try { var c = JSON.parse(localStorage.getItem("fx:EURJPY") || "null"); if (c) { rate = c.r; label = "tečaj z dne " + c.d; } } catch (e) {}
    var eur = box.querySelector(".fx-eur"), jpy = box.querySelector(".fx-jpy"), note = box.querySelector(".fx-note");
    function setNote() { note.textContent = "1 € = " + Math.round(rate * 100) / 100 + " ¥ (" + label + "). Banke in menjalnice imajo svoj tečaj in provizijo."; }
    function fromEur() { var v = parseFloat(String(eur.value).replace(",", ".")); jpy.value = isNaN(v) ? "" : Math.round(v * rate); }
    function fromJpy() { var v = parseFloat(String(jpy.value).replace(",", ".")); eur.value = isNaN(v) ? "" : (Math.round(v / rate * 100) / 100).toFixed(2); }
    eur.addEventListener("input", fromEur); jpy.addEventListener("input", fromJpy);
    setNote();
    if (window.fetch) {
      fetch("https://api.frankfurter.dev/v1/latest?base=EUR&symbols=JPY").then(function (r) { return r.json(); }).then(function (j) {
        if (j && j.rates && j.rates.JPY) {
          rate = j.rates.JPY; label = "tečaj ECB, " + j.date;
          try { localStorage.setItem("fx:EURJPY", JSON.stringify({ r: rate, d: j.date })); } catch (e) {}
          setNote(); if (eur.value) fromEur();
        }
      }).catch(function () {});
    }
  });
});
