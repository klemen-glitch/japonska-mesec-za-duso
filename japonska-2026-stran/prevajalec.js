/* ============================================================
   Prevajalec s kamero: kamera → OCR (japonščina, v telefonu) → prevod.
   - OCR: Tesseract.js (model jpn), slika ne zapusti telefona
   - Prevod: Google (neuradni dostop), rezerva MyMemory
   ============================================================ */
(function () {
  "use strict";

  var TESS_SRC = "https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js";
  var LANG_PATH = "https://cdn.jsdelivr.net/npm/@tesseract.js-data/jpn/4.0.0_best_int";

  function $(id) { return document.getElementById(id); }
  var el = {
    cam: $("tr-cam"), video: $("tr-video"), guide: $("tr-guide"), hint: $("tr-hint"),
    open: $("tr-open"), snap: $("tr-snap"), close: $("tr-close"), file: $("tr-file"), crop: $("tr-crop"),
    status: $("tr-status"), ja: $("tr-ja"), lang: $("tr-lang"), go: $("tr-go"), out: $("tr-out"),
    say: $("tr-say"), copy: $("tr-copy"), show: $("tr-show")
  };
  if (!el.open) return;

  var stream = null, worker = null, workerPromise = null, busy = false, lastTranslation = "";

  function status(msg, kind) {
    el.status.textContent = msg || "";
    el.status.className = "tr-status" + (kind ? " " + kind : "");
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function loadScript(src) {
    return new Promise(function (res, rej) {
      if (window.Tesseract) return res();
      var s = document.createElement("script");
      s.src = src; s.onload = res; s.onerror = function () { rej(new Error("script")); };
      document.head.appendChild(s);
    });
  }

  function getWorker() {
    if (workerPromise) return workerPromise;
    status("Nalagam prepoznavo japonščine (prvič ~2 MB) …");
    workerPromise = loadScript(TESS_SRC).then(function () {
      return window.Tesseract.createWorker("jpn", 1, {
        langPath: LANG_PATH,
        logger: function (m) {
          if (m && m.status === "recognizing text") status("Berem besedilo … " + Math.round(m.progress * 100) + " %");
        }
      });
    }).then(function (w) { worker = w; return w; })
      .catch(function (e) { workerPromise = null; throw e; });
    return workerPromise;
  }

  // ---- priprava slike ------------------------------------------------------
  function prepareCanvas(source, sw, sh, crop) {
    // crop = {x,y,w,h} v pikslih vira, ali null za celotno sliko
    var cx = crop ? crop.x : 0, cy = crop ? crop.y : 0;
    var cw = crop ? crop.w : sw, ch = crop ? crop.h : sh;
    var maxSide = Math.max(cw, ch);
    var scale = 1;
    if (maxSide > 1800) scale = 1800 / maxSide;
    else if (maxSide < 1000) scale = 1000 / maxSide;
    var c = document.createElement("canvas");
    c.width = Math.round(cw * scale); c.height = Math.round(ch * scale);
    var g = c.getContext("2d", { willReadFrequently: true });
    g.drawImage(source, cx, cy, cw, ch, 0, 0, c.width, c.height);
    var img = g.getImageData(0, 0, c.width, c.height), d = img.data, n = d.length, sum = 0, i;
    for (i = 0; i < n; i += 4) {
      var y = 0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2];
      d[i] = d[i + 1] = d[i + 2] = y; sum += y;
    }
    var mean = sum / (n / 4);
    var invert = mean < 110;          // svetlo besedilo na temnem ozadju
    var lo = 255, hi = 0;
    for (i = 0; i < n; i += 4) { var v = d[i]; if (v < lo) lo = v; if (v > hi) hi = v; }
    var span = Math.max(hi - lo, 1);
    for (i = 0; i < n; i += 4) {
      var s = (d[i] - lo) * 255 / span;
      if (invert) s = 255 - s;
      d[i] = d[i + 1] = d[i + 2] = s;
    }
    g.putImageData(img, 0, 0);
    return c;
  }

  function cleanJa(t) {
    return (t || "")
      .replace(/([　-鿿＀-￯])[ \t]+(?=[　-鿿＀-￯])/g, "$1")
      .replace(/[ \t]+\n/g, "\n").replace(/\n{3,}/g, "\n\n").trim();
  }

  // ---- prevod --------------------------------------------------------------
  function chunks(text, max) {
    var lines = text.split(/\n+/), out = [], cur = "";
    lines.forEach(function (ln) {
      ln = ln.trim(); if (!ln) return;
      if ((cur + "\n" + ln).length > max && cur) { out.push(cur); cur = ln; } else { cur = cur ? cur + "\n" + ln : ln; }
    });
    if (cur) out.push(cur);
    return out;
  }
  function viaGoogle(text, tl) {
    var url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=" + tl + "&dt=t&q=" + encodeURIComponent(text);
    return fetch(url).then(function (r) { if (!r.ok) throw new Error("g" + r.status); return r.json(); })
      .then(function (j) { return j[0].map(function (x) { return x[0]; }).join(""); });
  }
  function viaMyMemory(text, tl) {
    var url = "https://api.mymemory.translated.net/get?q=" + encodeURIComponent(text) + "&langpair=ja|" + tl;
    return fetch(url).then(function (r) { if (!r.ok) throw new Error("m" + r.status); return r.json(); })
      .then(function (j) {
        var t = j && j.responseData && j.responseData.translatedText;
        if (!t) throw new Error("m-empty");
        return t;
      });
  }
  function translate(text, tl) {
    text = (text || "").trim();
    if (!text) return Promise.resolve("");
    var parts = chunks(text, 1200);
    return Promise.all(parts.map(function (p) {
      return viaGoogle(p, tl).catch(function () {
        // MyMemory ima omejitev dolžine → razbij na krajše dele
        return Promise.all(chunks(p, 400).map(function (q) { return viaMyMemory(q, tl); })).then(function (a) { return a.join("\n"); });
      });
    })).then(function (a) { return a.join("\n"); });
  }

  function showTranslation(t) {
    lastTranslation = t || "";
    if (!t) { el.out.innerHTML = '<span class="tr-out-empty">Prevod se prikaže tukaj.</span>'; return; }
    el.out.innerHTML = esc(t).replace(/\n/g, "<br>");
  }

  function runTranslate() {
    var ja = el.ja.value.trim();
    if (!ja) { status("Najprej vnesite ali zajemite japonsko besedilo.", "warn"); return Promise.resolve(); }
    status("Prevajam …");
    el.go.disabled = true;
    return translate(ja, el.lang.value).then(function (t) {
      showTranslation(t);
      status(t ? "Pripravljeno ✓" : "Prevoda ni bilo mogoče pridobiti.", t ? "ok" : "warn");
    }).catch(function () {
      status("Prevod ni uspel — preverite internet in poskusite znova.", "warn");
    }).then(function () { el.go.disabled = false; });
  }

  // ---- OCR -----------------------------------------------------------------
  function processCanvas(canvas) {
    if (busy) return Promise.resolve();
    busy = true; el.snap.disabled = true;
    return getWorker().then(function (w) {
      status("Berem besedilo …");
      return w.recognize(canvas);
    }).then(function (res) {
      var text = cleanJa(res && res.data && res.data.text);
      el.ja.value = text;
      if (!text) {
        status("Besedila nisem našla. Pojdite bliže, dodajte svetlobo ali besedilo vtipkajte.", "warn");
        showTranslation("");
        return;
      }
      return runTranslate();
    }).catch(function () {
      status("Prepoznava ni uspela (potreben je internet za prvi zagon). Besedilo lahko vtipkate.", "warn");
    }).then(function () { busy = false; el.snap.disabled = false; });
  }

  // ---- kamera --------------------------------------------------------------
  function guideRect() {
    // okvir v odstotkih posnetka: širina 90 %, višina 46 %, nekoliko nad sredino
    return { x: 0.05, y: 0.27, w: 0.90, h: 0.46 };
  }
  function openCamera() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      status("Ta brskalnik ne omogoča kamere — uporabite »Slikaj ali izberi sliko«.", "warn"); return;
    }
    status("Odpiram kamero …");
    navigator.mediaDevices.getUserMedia({
      video: { facingMode: { ideal: "environment" }, width: { ideal: 1920 }, height: { ideal: 1080 } }, audio: false
    }).then(function (s) {
      stream = s;
      el.video.srcObject = s;
      el.video.setAttribute("playsinline", ""); el.video.muted = true;
      el.cam.hidden = false;
      el.video.onloadedmetadata = function () {
        if (el.video.videoWidth) el.cam.style.aspectRatio = el.video.videoWidth + " / " + el.video.videoHeight;
      };
      var p = el.video.play(); if (p && p.catch) p.catch(function () {});
      el.open.hidden = true; el.snap.hidden = false; el.close.hidden = false;
      status("");
      getWorker().then(function () { status("Pripravljeno — usmerite kamero v napis."); }).catch(function () {
        status("Prepoznave ni bilo mogoče naložiti (internet?). Besedilo lahko vtipkate.", "warn");
      });
    }).catch(function (e) {
      var denied = e && (e.name === "NotAllowedError" || e.name === "SecurityError");
      status(denied
        ? "Dostop do kamere ni dovoljen. Dovolite ga v nastavitvah ali uporabite »Slikaj ali izberi sliko«."
        : "Kamere ni bilo mogoče odpreti. Uporabite »Slikaj ali izberi sliko«.", "warn");
    });
  }
  function closeCamera() {
    if (stream) { stream.getTracks().forEach(function (t) { t.stop(); }); stream = null; }
    el.video.srcObject = null; el.cam.hidden = true;
    el.open.hidden = false; el.snap.hidden = true; el.close.hidden = true;
  }
  function snap() {
    var v = el.video, vw = v.videoWidth, vh = v.videoHeight;
    if (!vw || !vh) { status("Kamera se še pripravlja — počakajte trenutek.", "warn"); return; }
    var crop = null;
    if (el.crop.checked) {
      var r = guideRect();
      crop = { x: Math.round(vw * r.x), y: Math.round(vh * r.y), w: Math.round(vw * r.w), h: Math.round(vh * r.h) };
    }
    processCanvas(prepareCanvas(v, vw, vh, crop));
  }

  function fromFile(file) {
    if (!file) return;
    status("Odpiram sliko …");
    var url = URL.createObjectURL(file), img = new Image();
    img.onload = function () {
      var c = prepareCanvas(img, img.naturalWidth, img.naturalHeight, null);
      URL.revokeObjectURL(url);
      processCanvas(c);
    };
    img.onerror = function () { status("Slike ni bilo mogoče odpreti.", "warn"); };
    img.src = url;
  }

  // ---- večji prikaz, poslušanje, kopiranje --------------------------------
  var overlay = null;
  function showBig() {
    if (!lastTranslation) { status("Najprej prevedite besedilo.", "warn"); return; }
    if (!overlay) {
      overlay = document.createElement("div");
      overlay.className = "show-overlay"; overlay.hidden = true;
      overlay.innerHTML = '<div class="so-inner"><p class="so-sl"></p><p class="so-jp"></p>' +
        '<div class="so-btns"><button type="button" class="so-close">✕ Zapri</button></div></div>';
      document.body.appendChild(overlay);
      overlay.addEventListener("click", function () { overlay.hidden = true; document.body.style.overflow = ""; });
    }
    overlay.querySelector(".so-sl").textContent = el.ja.value.trim();
    var big = overlay.querySelector(".so-jp");
    big.textContent = lastTranslation; big.style.fontSize = "clamp(1.4rem, 6vw, 2.6rem)"; big.removeAttribute("lang");
    overlay.hidden = false; document.body.style.overflow = "hidden";
  }
  function sayJa() {
    var t = el.ja.value.trim();
    if (!t || !("speechSynthesis" in window)) { status("Poslušanje ni na voljo.", "warn"); return; }
    try {
      window.speechSynthesis.cancel();
      var u = new SpeechSynthesisUtterance(t); u.lang = "ja-JP"; u.rate = 0.85;
      var vs = window.speechSynthesis.getVoices() || [];
      for (var i = 0; i < vs.length; i++) { if ((vs[i].lang || "").toLowerCase().indexOf("ja") === 0) { u.voice = vs[i]; break; } }
      window.speechSynthesis.speak(u);
    } catch (e) {}
  }
  function copyOut() {
    if (!lastTranslation) { status("Ni česa kopirati.", "warn"); return; }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(lastTranslation).then(function () { status("Kopirano ✓", "ok"); },
        function () { status("Kopiranje ni uspelo.", "warn"); });
    }
  }

  // ---- povezave ------------------------------------------------------------
  el.open.addEventListener("click", openCamera);
  el.close.addEventListener("click", function () { closeCamera(); status(""); });
  el.snap.addEventListener("click", snap);
  el.file.addEventListener("change", function () { fromFile(el.file.files && el.file.files[0]); el.file.value = ""; });
  el.go.addEventListener("click", runTranslate);
  el.lang.addEventListener("change", function () { if (el.ja.value.trim()) runTranslate(); });
  el.ja.addEventListener("keydown", function (e) { if ((e.ctrlKey || e.metaKey) && e.key === "Enter") runTranslate(); });
  el.crop.addEventListener("change", function () { el.guide.hidden = !el.crop.checked; });
  el.say.addEventListener("click", sayJa);
  el.copy.addEventListener("click", copyOut);
  el.show.addEventListener("click", showBig);
  window.addEventListener("pagehide", closeCamera);
  document.addEventListener("visibilitychange", function () { if (document.hidden && stream) closeCamera(); });

  // za preizkušanje
  window.__tr = { processCanvas: processCanvas, translate: translate, prepareCanvas: prepareCanvas, cleanJa: cleanJa };
})();
