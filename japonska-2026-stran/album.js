/* ============================================================
   Album — nalaganje fotografij/videov in gradnja izzivov.
   Shramba: ločen bucket "japonska_album" v Supabase.
   ============================================================ */
(function () {
  "use strict";

  var SB_URL = "https://ayejgzzaykbopojiacgn.supabase.co";
  var SB_KEY = "sb_publishable_vgNDW0KMTwSPstN0PhwySQ_SDuOUzn3";
  var BUCKET = "japonska_album";
  var TABLE = "japonska_album_uploads";
  var PIN = "1195";

  var STATIONS = [
    { k: "tokio", e: "🗼", n: "Tokio" },
    { k: "chichibu", e: "🌳", n: "Chichibu" },
    { k: "kawaguchiko", e: "🗻", n: "Fuji / Kawaguchiko" },
    { k: "minobusan", e: "🏯", n: "Minobusan" },
    { k: "izu", e: "🌊", n: "Izu" },
    { k: "kumano", e: "⛩️", n: "Kumano" },
    { k: "koyasan", e: "🏔️", n: "Koya-san" },
    { k: "iya", e: "🏞️", n: "Iya" },
    { k: "ine", e: "🎣", n: "Ine" },
    { k: "nara", e: "🦌", n: "Nara" },
    { k: "kyoto", e: "🍁", n: "Kyoto" },
    { k: "osaka", e: "🏙️", n: "Osaka" },
    { k: "hiroshima", e: "🕊️", n: "Hiroshima" }
  ];
  var STNAME = {};
  STATIONS.forEach(function (s) { STNAME[s.k] = s.e + " " + s.n; });

  if (!window.supabase) { return; } // knjižnica se ni naložila
  var sb = window.supabase.createClient(SB_URL, SB_KEY);

  var uploadsCache = null;

  function pub(path) {
    try { return sb.storage.from(BUCKET).getPublicUrl(path).data.publicUrl; }
    catch (e) { return SB_URL + "/storage/v1/object/public/" + BUCKET + "/" + path; }
  }
  function isVideo(mime) { return (mime || "").indexOf("video") === 0; }
  function extOf(file) {
    var m = (file.name || "").match(/\.([a-z0-9]+)$/i);
    if (m) return m[1].toLowerCase();
    if (isVideo(file.type)) return "mp4";
    return "jpg";
  }

  // ---- identiteta (koda + ime) --------------------------------------------
  function getName() { try { return localStorage.getItem("album_name") || ""; } catch (e) { return ""; } }
  function setName(v) { try { localStorage.setItem("album_name", v); } catch (e) {} }
  function unlocked() { try { return localStorage.getItem("album_pin_ok") === "1"; } catch (e) { return false; } }
  function setUnlocked() { try { localStorage.setItem("album_pin_ok", "1"); } catch (e) {} }

  function ensureReady() {
    // vrne true, če lahko nalagamo (koda + ime)
    if (!unlocked()) {
      var code = window.prompt("Za nalaganje vnesi kodo:");
      if (code === null) return false;
      if (code.trim() !== PIN) { alert("Napačna koda."); return false; }
      setUnlocked();
    }
    if (!getName()) {
      var who = window.prompt("Kdo nalaga? (Marjetica, Helena, Ljuba ali Magda)");
      if (who === null) return false;
      setName(who.trim() || "—");
    }
    renderGate();
    return true;
  }

  function renderGate() {
    var el = document.querySelector(".album-gate");
    if (!el) return;
    var name = getName();
    el.innerHTML = "";
    var row = document.createElement("div");
    row.className = "gate-row";
    if (!unlocked()) {
      row.innerHTML =
        '<span class="gate-lbl">🔒 Za nalaganje vnesi kodo:</span>' +
        '<input class="gate-pin" inputmode="numeric" placeholder="koda" maxlength="8">' +
        '<button class="gate-btn" type="button">Odkleni</button>';
      el.appendChild(row);
      var inp = row.querySelector(".gate-pin");
      var btn = row.querySelector(".gate-btn");
      function tryUnlock() {
        if (inp.value.trim() === PIN) { setUnlocked(); if (!getName()) ensureReady(); else renderGate(); }
        else { inp.value = ""; inp.placeholder = "napačna koda"; }
      }
      btn.addEventListener("click", tryUnlock);
      inp.addEventListener("keydown", function (e) { if (e.key === "Enter") tryUnlock(); });
    } else {
      row.innerHTML = '<span class="gate-lbl">Nalagaš kot:</span>';
      ["Marjetica", "Helena", "Ljuba", "Magda"].forEach(function (nm) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "gate-name" + (name === nm ? " on" : "");
        b.textContent = nm;
        b.addEventListener("click", function () { setName(nm); renderGate(); });
        row.appendChild(b);
      });
      el.appendChild(row);
    }
  }

  // ---- podatki -------------------------------------------------------------
  function fetchUploads() {
    return sb.from(TABLE).select("*").order("created_at", { ascending: true })
      .then(function (r) { uploadsCache = r.data || []; return uploadsCache; })
      .catch(function () { uploadsCache = []; return uploadsCache; });
  }
  function byChallenge() {
    var m = {};
    (uploadsCache || []).forEach(function (u) {
      if (!u.challenge_id) return;
      (m[u.challenge_id] = m[u.challenge_id] || []).push(u);
    });
    return m;
  }

  // ---- nalaganje -----------------------------------------------------------
  function uploadFiles(files, station, challengeId, statusEl, done) {
    if (!files || !files.length) { if (done) done(); return; }
    var name = getName();
    var total = files.length, ok = 0, idx = 0;
    function next() {
      if (idx >= files.length) {
        fetchUploads().then(function () { rerenderAll(); if (done) done(ok); });
        return;
      }
      var file = files[idx++];
      if (statusEl) statusEl.textContent = "Nalagam " + idx + "/" + total + " …";
      var path = station + "/" + (challengeId || "splosno") + "/" +
        Date.now() + "-" + Math.random().toString(36).slice(2, 8) + "." + extOf(file);
      sb.storage.from(BUCKET).upload(path, file, { contentType: file.type || undefined, upsert: false })
        .then(function (res) {
          if (res.error) throw res.error;
          return sb.from(TABLE).insert({
            station: station, challenge_id: challengeId || null,
            uploader: name || null, path: path, mime: file.type || null
          });
        })
        .then(function () { ok++; next(); })
        .catch(function (e) {
          console.warn("upload napaka", e);
          if (statusEl) statusEl.textContent = "Napaka pri eni datoteki — poskušam naprej …";
          next();
        });
    }
    next();
  }

  function pickAndUpload(station, challengeId, statusEl, done) {
    if (!ensureReady()) return;
    var input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*,video/*";
    input.multiple = true;
    input.addEventListener("change", function () {
      if (input.files && input.files.length) {
        uploadFiles(input.files, station, challengeId, statusEl, done);
      }
    });
    input.click();
  }

  // ---- izris medijev -------------------------------------------------------
  function mediaEl(u, cls) {
    var url = pub(u.path);
    var wrap = document.createElement("a");
    wrap.href = url; wrap.target = "_blank"; wrap.rel = "noopener";
    wrap.className = cls || "album-thumb";
    if (isVideo(u.mime)) {
      var v = document.createElement("video");
      v.src = url; v.muted = true; v.playsInline = true; v.preload = "metadata";
      wrap.appendChild(v);
      var tag = document.createElement("span"); tag.className = "vtag"; tag.textContent = "▶";
      wrap.appendChild(tag);
    } else {
      var img = document.createElement("img");
      img.src = url; img.loading = "lazy"; img.alt = "";
      wrap.appendChild(img);
    }
    return wrap;
  }

  // ---- tabla izzivov -------------------------------------------------------
  function renderBoards() {
    var dataEl = document.getElementById("izziv-data");
    var challenges = [];
    if (dataEl) { try { challenges = JSON.parse(dataEl.textContent); } catch (e) {} }
    var m = byChallenge();
    document.querySelectorAll(".izziv-board").forEach(function (board) {
      var scope = board.getAttribute("data-scope") || "all";
      var list = challenges.filter(function (c) { return scope === "all" || c.s === scope; });
      var todo = list.filter(function (c) { return !m[c.id]; });
      var done = list.filter(function (c) { return m[c.id]; });

      board.innerHTML = "";
      var prog = document.createElement("p");
      prog.className = "izziv-progress";
      prog.textContent = "Opravljeno: " + done.length + " / " + list.length + " izzivov";
      board.appendChild(prog);

      var ul = document.createElement("ul");
      ul.className = "izziv-items";
      todo.concat(done).forEach(function (c) {
        var isDone = !!m[c.id];
        var li = document.createElement("li");
        li.className = "izziv-item" + (isDone ? " done" : "");

        var head = document.createElement("div");
        head.className = "izziv-head";
        var mark = isDone ? "✅" : (c.t === "video" ? "🎥" : "📸");
        var st = scope === "all" ? ('<span class="izziv-st">' + (STNAME[c.s] || "") + "</span>") : "";
        head.innerHTML = '<span class="izziv-mark">' + mark + "</span>" +
          '<span class="izziv-text">' + st + escapeHtml(c.x) + "</span>";
        li.appendChild(head);

        if (isDone) {
          var gal = document.createElement("div");
          gal.className = "izziv-shots";
          m[c.id].forEach(function (u) { gal.appendChild(mediaEl(u, "album-thumb sm")); });
          li.appendChild(gal);
        }

        var act = document.createElement("div");
        act.className = "izziv-act";
        var st2 = document.createElement("span"); st2.className = "izziv-status";
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "pin-btn izziv-up";
        btn.textContent = isDone ? "➕ Dodaj še" : "📸 Naloži in opravi";
        btn.addEventListener("click", function () {
          pickAndUpload(c.s, c.id, st2, function () { st2.textContent = "Naloženo ✓"; });
        });
        act.appendChild(btn); act.appendChild(st2);
        li.appendChild(act);

        ul.appendChild(li);
      });
      board.appendChild(ul);
    });
  }

  // ---- splošni nalagalnik (stran Naloži) -----------------------------------
  function renderUploader() {
    var box = document.querySelector(".album-upload");
    if (!box) return;
    box.innerHTML = "";
    var sel = document.createElement("select");
    sel.className = "album-select";
    STATIONS.forEach(function (s) {
      var o = document.createElement("option"); o.value = s.k; o.textContent = s.e + " " + s.n; sel.appendChild(o);
    });
    var btn = document.createElement("button");
    btn.type = "button"; btn.className = "photo-button album-big-btn";
    btn.textContent = "📷 Izberi fotografije ali video";
    var status = document.createElement("p"); status.className = "album-status";
    btn.addEventListener("click", function () {
      pickAndUpload(sel.value, null, status, function (n) {
        status.textContent = (n || 0) + " naloženih ✓ — hvala!";
      });
    });
    var lbl = document.createElement("label"); lbl.className = "album-field";
    lbl.innerHTML = "<span>Katera postaja?</span>";
    lbl.appendChild(sel);
    box.appendChild(lbl);
    box.appendChild(btn);
    box.appendChild(status);
  }

  // ---- galerija ------------------------------------------------------------
  function renderGallery() {
    var gEl = document.querySelector(".album-gallery");
    if (!gEl) return;
    gEl.innerHTML = "";
    if (!uploadsCache || !uploadsCache.length) {
      gEl.innerHTML = '<p class="album-empty">Album je še prazen — naložite prvo fotografijo. 📸</p>';
      return;
    }
    var bySt = {};
    uploadsCache.forEach(function (u) { (bySt[u.station || "drugo"] = bySt[u.station || "drugo"] || []).push(u); });
    STATIONS.forEach(function (s) {
      var arr = bySt[s.k];
      if (!arr || !arr.length) return;
      var h = document.createElement("h3"); h.className = "album-st-h"; h.textContent = s.e + " " + s.n + " (" + arr.length + ")";
      gEl.appendChild(h);
      var grid = document.createElement("div"); grid.className = "album-grid";
      arr.slice().reverse().forEach(function (u) { grid.appendChild(mediaEl(u, "album-thumb")); });
      gEl.appendChild(grid);
    });
  }

  function rerenderAll() { renderBoards(); renderGallery(); }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function init() {
    renderGate();
    renderUploader();
    if (document.querySelector(".izziv-board") || document.querySelector(".album-gallery")) {
      fetchUploads().then(rerenderAll);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else { init(); }
})();
