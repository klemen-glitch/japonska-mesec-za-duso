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

/* Offline podpora (PWA): stran si telefon zapomni,
   da osnovne informacije delujejo tudi brez interneta. */
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("sw.js").catch(function () {
      /* če ne uspe, stran normalno deluje naprej */
    });
  });
}
