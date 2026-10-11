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

/* Offline podpora (PWA): stran si telefon zapomni,
   da osnovne informacije delujejo tudi brez interneta. */
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("sw.js").catch(function () {
      /* če ne uspe, stran normalno deluje naprej */
    });
  });
}
