/* ============================================================
   Album — nalaganje fotografij/videov in gradnja izzivov.
   Shramba: bucket "trip_album" v Supabase; dostop prek PIN-a (RPC).
   Potovanje (id, postaje, ljudje) pride iz window.TRIP.
   ============================================================ */
(function () {
  "use strict";

  var SB_URL = "https://ayejgzzaykbopojiacgn.supabase.co";
  var SB_KEY = "sb_publishable_vgNDW0KMTwSPstN0PhwySQ_SDuOUzn3";
  var BUCKET = "trip_album";
  var TRIP = window.TRIP || { id: "", people: [], stations: [] };
  var STATIONS = (TRIP.stations || []).concat([{ k: "drugo", e: "✨", n: "Drugo" }]);
  var PEOPLE = TRIP.people || [];
  var T = TRIP.t || {};
  var T_LOCKED = T.locked || "Presenečenje te čaka — odklene se, ko naložite sliko ali video.";
  var T_EMPTY = T.empty || "Album je še prazen — naložite prvo fotografijo. 📸";
  var T_THANKS = T.thanks || "naloženih ✓ — hvala!";
  var T_MORE = T.more || "Odpri vodnik za to postajo →";
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

  // ---- seja (PIN iz vstopne strani) + ime ----------------------------------
  function session() {
    try { return JSON.parse(localStorage.getItem("trip_session") || "null"); } catch (e) { return null; }
  }
  function getPin() { var s = session(); return (s && s.pin) || ""; }
  var NAME_KEY = "album_name:" + TRIP.id;
  function getName() { try { return localStorage.getItem(NAME_KEY) || ""; } catch (e) { return ""; } }
  function setName(v) { try { localStorage.setItem(NAME_KEY, v); } catch (e) {} }
  function unlocked() { return !!getPin(); }

  function ensureReady() {
    // vrne true, če lahko nalagamo (PIN iz seje + ime)
    if (!unlocked()) { location.href = (TRIP.gate || "../index.html") + "?next=" + encodeURIComponent(TRIP.slug || ""); return false; }
    if (!getName()) {
      var who = window.prompt("Kdo nalaga? (" + PEOPLE.join(", ") + ")");
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
      row.innerHTML = '<span class="gate-lbl">🔒 Seja je potekla.</span>' +
        '<a class="gate-btn" href="' + (TRIP.gate || "../index.html") + '?next=' + encodeURIComponent(TRIP.slug || "") + '">Vnesi kodo</a>';
      el.appendChild(row);
    } else {
      row.innerHTML = '<span class="gate-lbl">Nalagaš kot:</span>';
      PEOPLE.forEach(function (nm) {
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
    var ck = "albumlist:" + TRIP.id;
    return sb.rpc("trip_album_list", { p_pin: getPin(), p_trip: TRIP.id })
      .then(function (r) {
        if (r && r.error && typeof tripAuthFail === "function" && tripAuthFail(r.error)) { tripReLogin(null); }
        if (r && !r.error && r.data) { try { localStorage.setItem(ck, JSON.stringify(r.data)); } catch (e) {} uploadsCache = r.data; }
        else {
          // brez povezave: zadnji znani seznam
          var c = null; try { c = JSON.parse(localStorage.getItem(ck) || "null"); } catch (e) {}
          uploadsCache = c || [];
        }
        return withPending();
      })
      .catch(function () {
        var c = null; try { c = JSON.parse(localStorage.getItem(ck) || "null"); } catch (e) {}
        uploadsCache = c || [];
        return withPending();
      });
  }

  // ---- čakalna vrsta (IndexedDB): slike, izbrane brez interneta -------------
  var QDB = null;
  function qdb() {
    if (QDB) return QDB;
    QDB = new Promise(function (res, rej) {
      if (!window.indexedDB) return rej(new Error("idb"));
      var rq = indexedDB.open("tripq", 1);
      rq.onupgradeneeded = function () { rq.result.createObjectStore("uploads", { keyPath: "id", autoIncrement: true }); };
      rq.onsuccess = function () { res(rq.result); };
      rq.onerror = function () { rej(rq.error); };
    });
    return QDB;
  }
  function qAll() {
    return qdb().then(function (db) {
      return new Promise(function (res) {
        var out = [], tx = db.transaction("uploads", "readonly"), cur = tx.objectStore("uploads").openCursor();
        cur.onsuccess = function () { var c = cur.result; if (c) { out.push(c.value); c.continue(); } else res(out); };
        cur.onerror = function () { res(out); };
      });
    }).catch(function () { return []; });
  }
  function qAdd(item) {
    return qdb().then(function (db) {
      return new Promise(function (res, rej) {
        var tx = db.transaction("uploads", "readwrite"); tx.objectStore("uploads").add(item);
        tx.oncomplete = function () { res(); }; tx.onerror = function () { rej(tx.error); };
      });
    });
  }
  function qDel(id) {
    return qdb().then(function (db) {
      return new Promise(function (res) {
        var tx = db.transaction("uploads", "readwrite"); tx.objectStore("uploads").delete(id);
        tx.oncomplete = function () { res(); }; tx.onerror = function () { res(); };
      });
    }).catch(function () {});
  }
  var pendingItems = [];
  function withPending() {
    return qAll().then(function (all) {
      pendingItems = all.filter(function (q) { return q.trip === TRIP.id; });
      pendingItems.forEach(function (q) {
        if (!q.url) q.url = URL.createObjectURL(q.blob);
        uploadsCache.push({ station: q.station, challenge_id: q.challenge || null, uploader: q.name, path: null, mime: q.mime, pending: true, _url: q.url });
      });
      return uploadsCache;
    });
  }
  function isNetFail(e) {
    var m = (e && (e.message || e.error || String(e))) || "";
    return !navigator.onLine || /fetch|network|load failed|timeout|offline/i.test(m);
  }
  var flushingQ = false;
  function flushQueue() {
    if (flushingQ || !navigator.onLine || !getPin()) return Promise.resolve();
    flushingQ = true;
    return qAll().then(function (all) {
      var mine = all.filter(function (q) { return q.trip === TRIP.id; }), ok = 0;
      function step(i) {
        if (i >= mine.length) return Promise.resolve();
        var q = mine[i];
        var path = TRIP.id + "/" + q.station + "/" + (q.challenge || "splosno") + "/" + uuid() + "." + q.ext;
        return sb.storage.from(BUCKET).upload(path, q.blob, { contentType: q.mime || undefined, upsert: false }).then(function (res) {
          if (res.error) throw res.error;
          return sb.rpc("trip_album_add", { p_pin: getPin(), p_trip: TRIP.id, p_station: q.station, p_challenge: q.challenge || null,
            p_uploader: q.name || null, p_path: path, p_mime: q.mime || null });
        }).then(function (r) {
          if (r && r.error) throw r.error;
          return qDel(q.id).then(function () { ok++; return step(i + 1); });
        }).catch(function (e) { if (isNetFail(e)) return Promise.resolve(); return step(i + 1); });
      }
      return step(0).then(function () { if (ok) return fetchUploads().then(rerenderAll); });
    }).then(function () { flushingQ = false; }, function () { flushingQ = false; });
  }
  window.addEventListener("online", function () { setTimeout(flushQueue, 800); });
  setTimeout(flushQueue, 3000);

  function uuid() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
      var r = Math.random() * 16 | 0; return (c === "x" ? r : (r & 3 | 8)).toString(16);
    });
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
    var total = files.length, ok = 0, idx = 0, queued = 0;
    function next() {
      if (idx >= files.length) {
        fetchUploads().then(function () { rerenderAll(); if (done) done(ok + queued); });
        return;
      }
      var file = files[idx++];
      if (statusEl) statusEl.textContent = "Nalagam " + idx + "/" + total + " …";
      var path = TRIP.id + "/" + station + "/" + (challengeId || "splosno") + "/" + uuid() + "." + extOf(file);
      sb.storage.from(BUCKET).upload(path, file, { contentType: file.type || undefined, upsert: false })
        .then(function (res) {
          if (res.error) throw res.error;
          return sb.rpc("trip_album_add", {
            p_pin: getPin(), p_trip: TRIP.id, p_station: station, p_challenge: challengeId || null,
            p_uploader: name || null, p_path: path, p_mime: file.type || null
          });
        })
        .then(function (r) { if (r && r.error) throw r.error; ok++; next(); })
        .catch(function (e) {
          console.warn("upload napaka", e);
          if (isNetFail(e)) {
            qAdd({ trip: TRIP.id, station: station, challenge: challengeId || null, name: name, mime: file.type || "", ext: extOf(file), blob: file })
              .then(function () { queued++; if (statusEl) statusEl.textContent = "📴 Brez povezave — slika čaka in se naloži sama (" + queued + ")."; next(); })
              .catch(function () { if (statusEl) statusEl.textContent = "Napaka pri eni datoteki — poskušam naprej …"; next(); });
            return;
          }
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
    var url = u.pending ? u._url : pub(u.path);
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
    if (u.pending) { var pt = document.createElement("span"); pt.className = "vtag pend"; pt.textContent = "⏳"; wrap.appendChild(pt); }
    return wrap;
  }

  // ---- tabla izzivov -------------------------------------------------------
  var KIND = {
    zanimivost: { ic: "💡", lbl: "Zanimivost" },
    skrivnost: { ic: "🔮", lbl: "Skrivnost" },
    nagrada: { ic: "🎁", lbl: "Nagrada" }
  };
  var openStations = {}; // postaje, ki jih je uporabnik odprl (ostanejo odprte ob osvežitvi tabele)

  function mapsUrl(q) {
    return "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(q);
  }

  function challengeCard(c, shots, scope) {
    var isDone = !!(shots && shots.length);
    var li = document.createElement("li");
    li.className = "izziv-card" + (isDone ? " done" : "");

    var head = document.createElement("div");
    head.className = "izziv-head";
    var mark = isDone ? "✅" : (c.t === "video" ? "🎥" : "📸");
    head.innerHTML = '<span class="izziv-mark">' + mark + "</span>" +
      '<span class="izziv-text">' + escapeHtml(c.x) + "</span>";
    li.appendChild(head);

    if (c.w) {
      var fine = document.createElement("details");
      fine.className = "izziv-fine";
      fine.innerHTML = "<summary>ℹ️ Drobni tisk: zakaj tu?</summary><p>" + escapeHtml(c.w) + "</p>";
      li.appendChild(fine);
    }

    if (c.p) {
      var k = KIND[c.p.k] || KIND.zanimivost;
      var sur = document.createElement("div");
      sur.className = "izziv-surprise " + (isDone ? "open" : "locked");
      if (isDone) {
        var html = '<div class="sur-head"><span class="sur-ic">' + k.ic + '</span><span><span class="sur-kind">' +
          k.lbl + " odklenjena</span><strong>" + escapeHtml(c.p.h) + "</strong></span></div>" +
          "<p>" + escapeHtml(c.p.x) + "</p>";
        if (c.p.m) {
          html += '<a class="pin-btn sur-pin" href="' + mapsUrl(c.p.m) + '" target="_blank" rel="noopener">📍 Pokaži na zemljevidu</a>';
        }
        sur.innerHTML = html;
      } else {
        sur.innerHTML = '<span class="sur-ic">🎁</span><span>' + escapeHtml(T_LOCKED) + '</span>';
      }
      li.appendChild(sur);
    }

    if (isDone) {
      var gal = document.createElement("div");
      gal.className = "izziv-shots";
      shots.forEach(function (u) { gal.appendChild(mediaEl(u, "album-thumb sm")); });
      li.appendChild(gal);
    }

    var act = document.createElement("div");
    act.className = "izziv-act";
    var st2 = document.createElement("span"); st2.className = "izziv-status";
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "pin-btn izziv-up";
    btn.textContent = isDone ? "➕ Dodaj še" : (c.t === "video" ? "🎥 Naloži video in opravi" : "📸 Naloži in opravi");
    btn.addEventListener("click", function () {
      pickAndUpload(c.s, c.id, st2, function () { st2.textContent = "Naloženo ✓"; });
    });
    act.appendChild(btn); act.appendChild(st2);
    li.appendChild(act);
    return li;
  }

  function renderBoards() {
    var dataEl = document.getElementById("izziv-data");
    var challenges = [];
    if (dataEl) { try { challenges = JSON.parse(dataEl.textContent); } catch (e) {} }
    var m = byChallenge();

    document.querySelectorAll(".izziv-board").forEach(function (board) {
      var scope = board.getAttribute("data-scope") || "all";
      var list = challenges.filter(function (c) { return scope === "all" || c.s === scope; });
      var totalDone = list.filter(function (c) { return m[c.id]; }).length;
      board.innerHTML = "";

      // skupni napredek
      var overall = document.getElementById("izziv-overall");
      if (scope === "all" && overall) {
        var pct = list.length ? Math.round(totalDone * 100 / list.length) : 0;
        overall.innerHTML = '<div class="ov-top"><strong>Opravljeno: ' + totalDone + " / " + list.length +
          " izzivov</strong><span>" + pct + ' %</span></div><div class="ov-bar"><i style="width:' + pct + '%"></i></div>';
        var fin = document.getElementById("izziv-final");
        if (fin) fin.hidden = !(list.length && totalDone === list.length);
      }

      if (scope !== "all") {
        var prog = document.createElement("p");
        prog.className = "izziv-progress";
        prog.textContent = "Opravljeno: " + totalDone + " / " + list.length + " izzivov";
        board.appendChild(prog);
        var ul = document.createElement("ul");
        ul.className = "izziv-items";
        var todo = list.filter(function (c) { return !m[c.id]; });
        var done = list.filter(function (c) { return m[c.id]; });
        todo.concat(done).forEach(function (c) { ul.appendChild(challengeCard(c, m[c.id], scope)); });
        board.appendChild(ul);
        return;
      }

      // razdelki po postajah (v vrstnem redu poti)
      var order = [], by = {};
      list.forEach(function (c) {
        if (!by[c.s]) { by[c.s] = { s: c.s, sn: c.sn, e: c.e, items: [] }; order.push(c.s); }
        by[c.s].items.push(c);
      });
      var firstOpen = null;
      order.forEach(function (k) {
        var g = by[k];
        var dn = g.items.filter(function (c) { return m[c.id]; }).length;
        if (firstOpen === null && dn < g.items.length) firstOpen = k;
      });
      order.forEach(function (k) {
        var g = by[k];
        var dn = g.items.filter(function (c) { return m[c.id]; }).length;
        var complete = dn === g.items.length;
        var det = document.createElement("details");
        det.className = "izziv-station" + (complete ? " complete" : "");
        det.setAttribute("data-st", k);
        if (openStations[k] !== undefined ? openStations[k] : (k === firstOpen)) det.open = true;
        var pct = Math.round(dn * 100 / g.items.length);
        det.innerHTML = '<summary><span class="st-emoji">' + g.e + '</span>' +
          '<span class="st-name">' + escapeHtml(g.sn) + (complete ? ' <em class="st-badge">🏅 Opravljeno</em>' : "") + "</span>" +
          '<span class="st-count">' + dn + "/" + g.items.length + '</span><span class="st-chev" aria-hidden="true">▶</span>' +
          '<span class="st-bar"><i style="width:' + pct + '%"></i></span></summary>';
        det.addEventListener("toggle", function () { openStations[k] = det.open; });
        var ul2 = document.createElement("ul");
        ul2.className = "izziv-items";
        var t2 = g.items.filter(function (c) { return !m[c.id]; });
        var d2 = g.items.filter(function (c) { return m[c.id]; });
        t2.concat(d2).forEach(function (c) { ul2.appendChild(challengeCard(c, m[c.id], scope)); });
        det.appendChild(ul2);
        var more = document.createElement("a");
        more.className = "st-more"; more.href = k + ".html"; more.textContent = T_MORE;
        det.appendChild(more);
        board.appendChild(det);
      });
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
        status.textContent = (n || 0) + " " + T_THANKS;
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
      gEl.innerHTML = '<p class="album-empty">' + escapeHtml(T_EMPTY) + '</p>';
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

  // ---- prenos celega albuma (.zip) ----------------------------------------
  function loadJsZip() {
    return new Promise(function (res, rej) {
      if (window.JSZip) return res();
      var s = document.createElement("script");
      s.src = "https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js";
      s.onload = res; s.onerror = rej;
      document.head.appendChild(s);
    });
  }
  function baseName(p) { var a = (p || "").split("/"); return a[a.length - 1]; }
  function safeFolder(k) {
    var n = (STNAME[k] || k || "drugo");
    return n.replace(/[^0-9A-Za-zČŠŽčšž _-]/g, "").trim() || "drugo";
  }

  function downloadAll(btn, status) {
    if (!uploadsCache || !uploadsCache.length) { if (status) status.textContent = "Album je še prazen."; return; }
    btn.disabled = true;
    var total = uploadsCache.length, ok = 0, i = 0, zip;
    if (status) status.textContent = "Pripravljam …";
    loadJsZip().then(function () {
      zip = new JSZip();
      function next() {
        if (i >= total) {
          if (status) status.textContent = "Pakiram " + ok + " datotek v .zip …";
          zip.generateAsync({ type: "blob" }).then(function (out) {
            var a = document.createElement("a");
            a.href = URL.createObjectURL(out);
            a.download = (TRIP.id || "potovanje") + "-album.zip";
            document.body.appendChild(a); a.click(); a.remove();
            if (status) status.textContent = "Preneseno ✓ (" + ok + " datotek)";
            btn.disabled = false;
          });
          return;
        }
        var u = uploadsCache[i++];
        if (u.pending) { next(); return; }
        if (status) status.textContent = "Pripravljam " + i + "/" + total + " …";
        fetch(pub(u.path)).then(function (r) { return r.blob(); }).then(function (blob) {
          zip.file(safeFolder(u.station) + "/" + baseName(u.path), blob);
          ok++; next();
        }).catch(function (e) { console.warn("skip", u.path, e); next(); });
      }
      next();
    }).catch(function () { if (status) status.textContent = "Napaka pri pripravi prenosa."; btn.disabled = false; });
  }

  function renderDownload() {
    var box = document.querySelector(".album-download");
    if (!box) return;
    box.innerHTML = "";
    if (!uploadsCache || !uploadsCache.length) return;
    var btn = document.createElement("button");
    btn.type = "button"; btn.className = "photo-button album-dl-btn";
    btn.textContent = "⬇️ Prenesi vse slike (.zip)";
    var status = document.createElement("span"); status.className = "album-status dl-status";
    btn.addEventListener("click", function () { downloadAll(btn, status); });
    box.appendChild(btn); box.appendChild(status);
  }

  function rerenderAll() { renderBoards(); renderGallery(); renderDownload(); }

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
