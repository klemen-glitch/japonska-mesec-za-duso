/* ============================================================
   Pogovorni prevajalnik (slovensko ↔ japonsko): govorite v telefon, prevod se prikaže veliko in se izgovori.
   - govor v besedilo: vgrajeno v brskalnik (Web Speech API)
   - prevod: Google (neuradni dostop), rezerva MyMemory — v prevajalsko storitev se pošlje samo besedilo
   - hitre fraze delujejo tudi brez interneta
   ============================================================ */
(function () {
  "use strict";
  var host = document.getElementById("pogovor");
  if (!host) return;

  function $(s) { return host.querySelector(s); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  var log = $("#pg-log"), live = $("#pg-live"), status = $("#pg-status"), txt = $("#pg-text");
  var rec = null, listening = null;

  function setStatus(t, kind) { status.textContent = t || ""; status.className = "pg-status" + (kind ? " " + kind : ""); }

  /* ---------------- prevod ---------------- */
  function parseGtx(j) {
    var segs = (j && j[0]) || [], out = "", roT = "", roS = "";
    segs.forEach(function (s) {
      if (s && s[0] != null) out += s[0];
      else if (s) { if (s[2]) roT = s[2]; if (s[3]) roS = s[3]; }
    });
    return { text: out, roT: roT, roS: roS };
  }
  function viaGoogle(text, sl, tl) {
    var url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" + sl + "&tl=" + tl + "&dt=t&dt=rm&q=" + encodeURIComponent(text);
    return fetch(url).then(function (r) { if (!r.ok) throw new Error("g" + r.status); return r.json(); }).then(parseGtx);
  }
  function viaMyMemory(text, sl, tl) {
    var url = "https://api.mymemory.translated.net/get?q=" + encodeURIComponent(text) + "&langpair=" + sl + "|" + tl;
    return fetch(url).then(function (r) { if (!r.ok) throw new Error("m" + r.status); return r.json(); }).then(function (j) {
      var t = j && j.responseData && j.responseData.translatedText;
      if (!t) throw new Error("m0");
      return { text: t, roT: "", roS: "" };
    });
  }
  function translate(text, sl, tl) {
    return viaGoogle(text, sl, tl).then(function (r) { if (!r.text) throw new Error("prazno"); return r; }).catch(function () { return viaMyMemory(text, sl, tl); });
  }

  /* ---------------- izgovor ---------------- */
  function speak(text, lang) {
    if (!("speechSynthesis" in window) || !text) return;
    try {
      speechSynthesis.cancel();
      var u = new SpeechSynthesisUtterance(text);
      u.lang = lang; u.rate = lang === "ja-JP" ? 0.85 : 0.95;
      var vs = speechSynthesis.getVoices() || [];
      for (var i = 0; i < vs.length; i++) { if ((vs[i].lang || "").toLowerCase().indexOf(lang.slice(0, 2).toLowerCase()) === 0) { u.voice = vs[i]; break; } }
      speechSynthesis.speak(u);
    } catch (e) {}
  }

  /* ---------------- mehurčki ---------------- */
  function big(text, ro, lang) {
    var ov = document.createElement("div");
    ov.className = "taxi-ov";
    ov.innerHTML = '<div class="to-inner"><div class="to-addr" lang="' + lang.slice(0, 2) + '">' + esc(text) + "</div>" + (ro ? '<div class="to-lat">' + esc(ro) + "</div>" : "") +
      '<div class="to-btns"><button type="button" class="buy-btn alt" data-s="1">🔊 Poslušaj</button><button type="button" class="buy-btn" data-c="1">✕ Zapri</button></div></div>';
    document.body.appendChild(ov); document.body.style.overflow = "hidden";
    ov.addEventListener("click", function (e) {
      if (e.target.getAttribute("data-c")) { ov.parentNode.removeChild(ov); document.body.style.overflow = ""; }
      if (e.target.getAttribute("data-s")) speak(text, lang);
    });
  }

  function bubble(o) {
    // o: {me: bool, src, out, ro, srcRo, outLang}
    var d = document.createElement("div");
    d.className = "pg-b " + (o.me ? "me" : "they");
    d.innerHTML = '<div class="pg-src">' + (o.me ? "🇸🇮 " : "🇯🇵 ") + esc(o.src) + (o.srcRo ? "<br><i>" + esc(o.srcRo) + "</i>" : "") + "</div>" +
      '<div class="pg-out" lang="' + o.outLang.slice(0, 2) + '">' + esc(o.out) + "</div>" + (o.ro ? '<div class="pg-ro">' + esc(o.ro) + "</div>" : "") +
      '<div class="pg-act"><button type="button" data-a="say">🔊</button><button type="button" data-a="big">🪪 Pokaži večje</button><button type="button" data-a="copy">📋</button></div>';
    d.querySelector('[data-a="say"]').addEventListener("click", function () { speak(o.out, o.outLang); });
    d.querySelector('[data-a="big"]').addEventListener("click", function () { big(o.out, o.ro, o.outLang); });
    d.querySelector('[data-a="copy"]').addEventListener("click", function () { if (navigator.clipboard) navigator.clipboard.writeText(o.out); });
    log.insertBefore(d, log.firstChild);
    if ($("#pg-auto").checked) speak(o.out, o.outLang);
    return d;
  }

  function run(text, dir) {
    text = (text || "").trim();
    if (!text) return;
    var sl = dir === "sl-ja" ? "sl" : "ja", tl = dir === "sl-ja" ? "ja" : "sl";
    setStatus("Prevajam …");
    translate(text, sl, tl).then(function (r) {
      setStatus("");
      bubble({ me: dir === "sl-ja", src: text, srcRo: dir === "ja-sl" ? r.roS : "", out: r.text, ro: dir === "sl-ja" ? r.roT : "", outLang: dir === "sl-ja" ? "ja-JP" : "sl-SI" });
    }).catch(function () {
      setStatus(navigator.onLine ? "Prevod ni uspel. Poskusite znova ali uporabite hitre fraze." : "📴 Brez interneta — uporabite hitre fraze spodaj.", "warn");
    });
  }

  /* ---------------- mikrofon ---------------- */
  function stopRec() { if (rec) { try { rec.stop(); } catch (e) {} } }
  function listen(btn) {
    if (!SR) { setStatus("Ta brskalnik ne podpira govora. Natipkajte besedilo ali uporabite mikrofon na tipkovnici (diktat).", "warn"); return; }
    if (listening) { stopRec(); return; }
    var lang = btn.getAttribute("data-lang"), dir = btn.getAttribute("data-dir");
    rec = new SR();
    rec.lang = lang; rec.interimResults = true; rec.continuous = false; rec.maxAlternatives = 1;
    var finalText = "";
    rec.onstart = function () { listening = btn; btn.classList.add("on"); live.textContent = ""; setStatus("🎤 Poslušam … govorite"); };
    rec.onresult = function (e) {
      var interim = "";
      for (var i = e.resultIndex; i < e.results.length; i++) {
        if (e.results[i].isFinal) finalText += e.results[i][0].transcript; else interim += e.results[i][0].transcript;
      }
      live.textContent = finalText + interim;
    };
    rec.onerror = function (e) {
      var m = e && e.error;
      if (m === "not-allowed" || m === "service-not-allowed") setStatus("Mikrofon ni dovoljen. Dovolite ga v nastavitvah brskalnika (ali uporabite tipkovnico).", "warn");
      else if (m === "no-speech") setStatus("Nič nisem slišal. Poskusite znova.", "warn");
      else if (m === "language-not-supported") setStatus("Ta jezik ni podprt za govor — natipkajte besedilo.", "warn");
      else if (m === "network") setStatus("Za prepoznavo govora je potreben internet.", "warn");
      else if (m !== "aborted") setStatus("Težava z mikrofonom (" + m + "). Natipkajte besedilo.", "warn");
    };
    rec.onend = function () {
      btn.classList.remove("on"); listening = null;
      var t = (live.textContent || "").trim(); live.textContent = "";
      if (t) run(t, dir);
      else if (!/Mikrofon|Nič|Težava|podprt|potreben/.test(status.textContent)) setStatus("");
    };
    try { rec.start(); } catch (e) { setStatus("Mikrofona ni mogoče zagnati. Natipkajte besedilo.", "warn"); }
  }

  host.querySelectorAll(".pg-mic").forEach(function (b) { b.addEventListener("click", function () { listen(b); }); });
  $("#pg-to-ja").addEventListener("click", function () { var t = txt.value; txt.value = ""; run(t, "sl-ja"); });
  $("#pg-to-sl").addEventListener("click", function () { var t = txt.value; txt.value = ""; run(t, "ja-sl"); });
  txt.addEventListener("keydown", function (e) { if (e.key === "Enter") { var t = txt.value; txt.value = ""; run(t, "sl-ja"); } });
  $("#pg-clear").addEventListener("click", function () { log.innerHTML = ""; setStatus(""); });

  // hitre fraze (delujejo brez interneta: japonščina je že pripravljena)
  var phrases = []; try { phrases = JSON.parse(document.getElementById("pg-phrases").textContent); } catch (e) {}
  var chips = $("#pg-chips");
  chips.innerHTML = phrases.map(function (p, i) { return '<button type="button" class="chip" data-i="' + i + '">' + esc(p.sl) + "</button>"; }).join("");
  chips.querySelectorAll(".chip").forEach(function (c) {
    c.addEventListener("click", function () {
      var p = phrases[parseInt(c.getAttribute("data-i"), 10)];
      bubble({ me: true, src: p.sl, out: p.ja, ro: p.ro, outLang: "ja-JP" });
    });
  });

  if (!SR) setStatus("ℹ️ Mikrofon v tem brskalniku ni na voljo — natipkajte besedilo ali uporabite hitre fraze.");
  if ("speechSynthesis" in window) { try { speechSynthesis.getVoices(); } catch (e) {} }
})();
