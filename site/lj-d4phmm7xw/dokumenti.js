/* ============================================================
   Potni listi in letalske karte (stran Nujno): slike/PDF se shranijo na strežnik (zaščiteno s kodo potovanja)
   in v telefon (IndexedDB), zato so na voljo tudi brez interneta. Vidijo jih vsi člani potovanja.
   ============================================================ */
(function () {
  "use strict";
  var hosts = { passport: document.getElementById("pot-host"), flight: document.getElementById("let-host") };
  if (!hosts.passport && !hosts.flight) return;
  var TRIP = window.TRIP || { id: "", people: [] };
  var PEOPLE = TRIP.people || [];
  var docs = [], cachedView = false;
  var DB = "tripdocs:" + TRIP.id;

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function myName() { try { return localStorage.getItem("album_name:" + TRIP.id) || ""; } catch (e) { return ""; } }
  function pin() { return window.TripData ? TripData.pin() : ""; }

  /* IndexedDB: predpomnilnik vsebine dokumentov */
  function idb() {
    return new Promise(function (res, rej) {
      if (!window.indexedDB) return rej();
      var r = indexedDB.open(DB, 1);
      r.onupgradeneeded = function () { r.result.createObjectStore("d"); };
      r.onsuccess = function () { res(r.result); };
      r.onerror = function () { rej(); };
    });
  }
  function idbGet(id) {
    return idb().then(function (db) { return new Promise(function (res) { var q = db.transaction("d").objectStore("d").get(id); q.onsuccess = function () { res(q.result || null); }; q.onerror = function () { res(null); }; }); }, function () { return null; });
  }
  function idbPut(id, v) { return idb().then(function (db) { db.transaction("d", "readwrite").objectStore("d").put(v, id); }, function () {}); }
  function idbDel(id) { return idb().then(function (db) { db.transaction("d", "readwrite").objectStore("d").delete(id); }, function () {}); }

  function getData(id) {
    return idbGet(id).then(function (c) {
      if (c) return c;
      return TripData.rpc("trip_doc_get", { p_pin: pin(), p_trip: TRIP.id, p_id: id }).then(function (r) {
        if (r.error) throw r.error;
        if (r.data) idbPut(id, r.data);
        return r.data;
      });
    });
  }

  function load() {
    return TripData.list("trip_docs_list", "docs").then(function (r) { docs = r.data || []; cachedView = !!r.cached; });
  }

  /* slika: pomanjšaj in stisni (potni list ostane čitljiv) */
  function shrink(file) {
    return new Promise(function (res, rej) {
      if (file.type === "application/pdf") {
        if (file.size > 1800000) return rej(new Error("PDF je prevelik (največ okoli 1,8 MB). Raje naložite sliko."));
        var fr = new FileReader(); fr.onload = function () { res(fr.result); }; fr.onerror = rej; fr.readAsDataURL(file); return;
      }
      if (!/^image\//.test(file.type)) return rej(new Error("Izberite sliko ali PDF."));
      var img = new Image(), url = URL.createObjectURL(file);
      img.onload = function () {
        var max = 1600, s = Math.min(1, max / Math.max(img.width, img.height));
        var c = document.createElement("canvas"); c.width = Math.round(img.width * s); c.height = Math.round(img.height * s);
        c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
        URL.revokeObjectURL(url);
        res(c.toDataURL("image/jpeg", 0.78));
      };
      img.onerror = function () { URL.revokeObjectURL(url); rej(new Error("Slike ni mogoče prebrati (HEIC? poskusite posnetek zaslona ali JPG).")); };
      img.src = url;
    });
  }

  function render() {
    ["passport", "flight"].forEach(function (kind) {
      var host = hosts[kind]; if (!host) return;
      var mine = docs.filter(function (d) { return d.kind === kind; });
      var h = "";
      if (cachedView) h += '<p class="buy-note sync-note">📴 Prikazana je shranjena kopija seznama.</p>';
      if (kind === "passport") {
        h += '<div class="doc-grid">' + PEOPLE.map(function (p) {
          var its = mine.filter(function (d) { return d.person === p; });
          return '<div class="doc-card"><h3>' + esc(p) + "</h3>" +
            (its.length ? its.map(rowHtml).join("") : '<p class="buy-note">Še ni slike.</p>') +
            '<button type="button" class="buy-btn alt doc-add" data-kind="passport" data-person="' + esc(p) + '">📷 Dodaj sliko potnega lista</button></div>';
        }).join("") + "</div>";
        h += '<p class="buy-note">🔒 Slike so shranjene na zaščitenem strežniku in vidne le članom tega potovanja (s skupno kodo); v telefon se shranijo za uporabo brez interneta. Zbrišete jih lahko kadarkoli (🗑️). Po potovanju jih zbrišite.</p>';
      } else {
        h += (mine.length ? mine.map(rowHtml).join("") : '<p class="buy-note">Še ni dodanih kart.</p>');
        h += '<div class="mf-row doc-flight-add"><label class="mf">Komu / kaj<select id="doc-fl-person"><option value="Vse">Vse</option>' +
          PEOPLE.map(function (p) { return "<option>" + esc(p) + "</option>"; }).join("") + '</select></label>' +
          '<label class="mf">Naslov<input id="doc-fl-title" type="text" placeholder="npr. Dunaj → Tokio, 3. 11."></label></div>' +
          '<button type="button" class="buy-btn doc-add" data-kind="flight">✈️ Dodaj letalsko karto (slika ali PDF)</button>';
      }
      h += '<p class="buy-note" id="doc-msg-' + kind + '" role="status"></p>';
      host.innerHTML = h;
    });
    document.querySelectorAll(".doc-add").forEach(function (b) { b.addEventListener("click", function () { pick(b); }); });
    document.querySelectorAll(".doc-view").forEach(function (b) { b.addEventListener("click", function () { view(b.getAttribute("data-id")); }); });
    document.querySelectorAll(".doc-del").forEach(function (b) { b.addEventListener("click", function () { del(b.getAttribute("data-id")); }); });
  }

  function rowHtml(d) {
    var label = d.kind === "flight" ? esc(d.title || "Karta") + " <small>(" + esc(d.person) + ")</small>" : esc(d.title || "Potni list");
    return '<div class="doc-row"><span>' + (d.mime === "application/pdf" ? "📄 " : "🖼️ ") + label + "</span>" +
      '<span><button type="button" class="buy-btn alt doc-view" data-id="' + esc(d.id) + '">Odpri</button> ' +
      '<button type="button" class="pin-btn doc-del" data-id="' + esc(d.id) + '" aria-label="Zbriši">🗑️</button></span></div>';
  }

  function msg(kind, t) { var e = document.getElementById("doc-msg-" + kind); if (e) e.textContent = t; }

  function pick(btn) {
    var kind = btn.getAttribute("data-kind");
    var person = kind === "passport" ? btn.getAttribute("data-person") : (document.getElementById("doc-fl-person") || {}).value || "Vse";
    var title = kind === "flight" ? ((document.getElementById("doc-fl-title") || {}).value || "").trim() : "Potni list";
    var inp = document.createElement("input");
    inp.type = "file"; inp.accept = kind === "flight" ? "image/*,application/pdf" : "image/*";
    inp.onchange = function () {
      var f = inp.files && inp.files[0]; if (!f) return;
      msg(kind, "Obdelujem in shranjujem …");
      shrink(f).then(function (data) {
        return TripData.rpc("trip_doc_add", { p_pin: pin(), p_trip: TRIP.id, p_kind: kind, p_person: person, p_title: title, p_mime: data.slice(5, data.indexOf(";")), p_data: data, p_by: myName() || person }).then(function (r) {
          if (r.error) throw r.error;
          idbPut(r.data, data);
        });
      }).then(function () { msg(kind, "✅ Shranjeno."); return refresh(); }).catch(function (e) {
        if (window.tripAuthFail && tripAuthFail(e)) { tripReLogin(hosts[kind], "Koda ni veljavna ali je seja potekla."); return; }
        msg(kind, e && e.message && !e.code ? e.message : (TripData.isNetErr(e) ? "Ni interneta — poskusite znova, ko bo povezava." : "Napaka pri shranjevanju (preveliko?)."));
      });
    };
    inp.click();
  }

  function view(id) {
    getData(id).then(function (data) {
      if (!data) throw new Error("ni");
      var ov = document.createElement("div");
      ov.className = "taxi-ov doc-ov";
      var pdf = data.indexOf("data:application/pdf") === 0;
      ov.innerHTML = '<div class="to-inner doc-inner">' + (pdf ? '<a class="buy-btn" target="_blank" rel="noopener" href="' + data + '">📄 Odpri PDF</a>' : '<img src="' + data + '" alt="Dokument" class="doc-img">') +
        '<div class="to-btns"><button type="button" class="buy-btn" data-close="1">✕ Zapri</button></div></div>';
      document.body.appendChild(ov); document.body.style.overflow = "hidden";
      ov.addEventListener("click", function (e) { if (e.target.getAttribute("data-close") || e.target === ov) { ov.parentNode.removeChild(ov); document.body.style.overflow = ""; } });
    }).catch(function () { alert("Dokumenta ni mogoče naložiti. Preverite internet (ali ga odprite enkrat z internetom, nato deluje tudi brez)."); });
  }

  function del(id) {
    if (!confirm("Zbrišem ta dokument za vse člane potovanja?")) return;
    TripData.rpc("trip_doc_delete", { p_pin: pin(), p_trip: TRIP.id, p_id: id }).then(function (r) {
      if (r.error) throw r.error; idbDel(id); return refresh();
    }).catch(function () { alert("Brisanje ni uspelo (internet?)."); });
  }

  function refresh() { return load().then(render).catch(function (e) {
    if (window.tripAuthFail && tripAuthFail(e)) { Object.keys(hosts).forEach(function (k) { if (hosts[k]) tripReLogin(hosts[k], "Koda ni veljavna ali je seja potekla."); }); return; }
    docs = []; cachedView = true; render(); }); }

  if (!window.TripData) { Object.keys(hosts).forEach(function (k) { if (hosts[k]) hosts[k].innerHTML = '<p class="buy-note">Naloži se, ko je internet na voljo.</p>'; }); return; }
  if (!pin()) { Object.keys(hosts).forEach(function (k) { if (hosts[k]) tripReLogin(hosts[k], "Seja je potekla."); }); return; }
  refresh().then(function () { docs.forEach(function (d) { idbGet(d.id).then(function (c) { if (!c && navigator.onLine) getData(d.id).catch(function () {}); }); }); });
})();
