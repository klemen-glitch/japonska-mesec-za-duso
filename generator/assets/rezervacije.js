/* ============================================================
   Moje rezervacije (skupne za vse člane potovanja) in kartice za taksista.
   Podatki so v Supabase (zaščiteno s kodo); brez interneta se prikaže shranjen seznam, spremembe čakajo v vrsti.
   ============================================================ */
(function () {
  "use strict";
  var bookHost = document.getElementById("book-host"), taxiHost = document.getElementById("taxi-host");
  if (!bookHost && !taxiHost) return;
  var host = bookHost || taxiHost;
  if (!window.TripData) { host.innerHTML = '<p class="buy-note">Naloži se, ko je internet na voljo.</p>'; return; }
  var TRIP = window.TRIP || { id: "", people: [], stations: [] };
  var rows = [], cachedView = false, editing = null;
  var MON = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "avg", "sep", "okt", "nov", "dec"];
  var KINDS = { nastanitev: ["🏨", "Nastanitve"], prevoz: ["🚆", "Prevozi in vozovnice"], vstopnica: ["🎟️", "Vstopnice in doživetja"], drugo: ["📄", "Drugo"] };

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function jd(id) { var e = document.getElementById(id); if (!e) return null; try { return JSON.parse(e.textContent); } catch (x) { return null; } }
  function dshort(iso) { if (!iso) return ""; var p = iso.split("-"); return parseInt(p[2], 10) + ". " + MON[parseInt(p[1], 10) - 1]; }
  function range(a, b) { if (a && b && a !== b) return dshort(a) + " → " + dshort(b); return dshort(a || b); }
  function myName() { try { return localStorage.getItem("album_name:" + TRIP.id) || ""; } catch (e) { return ""; } }
  function gmaps(q) { return "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(q); }
  function stName(k) { var s = (TRIP.stations || []).filter(function (x) { return x.k === k; })[0]; return s ? s.e + " " + s.n : ""; }

  function merged() {
    var q = TripData.getQ(), out = rows.map(function (r) { return Object.assign({}, r); });
    q.forEach(function (it, i) {
      if (it.fn === "trip_book_delete") out = out.filter(function (r) { return r.id !== it.args.p_id; });
      else if (it.fn === "trip_book_save") {
        var d = it.args.p_data || {};
        if (it.args.p_id) out.forEach(function (r) { if (r.id === it.args.p_id) Object.assign(r, d, { pending: true }); });
        else out.push(Object.assign({ id: "q" + i, pending: true }, d));
      }
    });
    out.sort(function (a, b) { return (a.date_from || "9999").localeCompare(b.date_from || "9999"); });
    return out;
  }

  function load() { return TripData.list("trip_book_list", "book").then(function (r) { rows = r.data || []; cachedView = !!r.cached; }); }

  /* ---------------------------------------------------------------- REZERVACIJE */
  function card(r) {
    var k = KINDS[r.kind] || KINDS.drugo;
    var h = '<article class="bk-card"><div class="bk-top"><span class="bk-ic">' + k[0] + '</span><div><strong>' + (r.pending ? "⏳ " : "") + esc(r.title) + "</strong>" +
      '<span class="bk-meta">' + [r.station ? esc(stName(r.station)) : "", esc(range(r.date_from, r.date_to)), r.time_text ? "⏰ " + esc(r.time_text) : ""].filter(Boolean).join(" · ") + "</span></div></div>";
    if (r.address) h += '<p class="bk-line">📍 <a href="' + esc(gmaps(r.address)) + '" target="_blank" rel="noopener">' + esc(r.address) + "</a></p>";
    if (r.address_local) h += '<p class="bk-line bk-ja" lang="ja">' + esc(r.address_local) + "</p>";
    if (r.phone) h += '<p class="bk-line">📞 <a href="tel:' + esc(r.phone.replace(/[^+\d]/g, "")) + '">' + esc(r.phone) + "</a></p>";
    if (r.conf) h += '<p class="bk-line">🔖 <code>' + esc(r.conf) + '</code> <button type="button" class="bk-copy" data-copy="' + esc(r.conf) + '">Kopiraj</button></p>';
    if (r.url) h += '<p class="bk-line">🔗 <a href="' + esc(r.url) + '" target="_blank" rel="noopener">Povezava do rezervacije</a></p>';
    if (r.notes) h += '<p class="bk-line bk-notes">' + esc(r.notes).replace(/\n/g, "<br>") + "</p>";
    h += '<p class="bk-foot">' + (r.by ? "dodal/-a: " + esc(r.by) : "") + '<span><button type="button" class="bk-edit" data-id="' + esc(r.id) + '">✏️ Uredi</button> ' +
      '<button type="button" class="bk-del" data-id="' + esc(r.id) + '">🗑️</button></span></p></article>';
    return h;
  }

  function form(r) {
    r = r || {};
    var stOpts = '<option value="">— (ni vezano na postajo)</option>' + (TRIP.stations || []).map(function (s) {
      return '<option value="' + esc(s.k) + '"' + (r.station === s.k ? " selected" : "") + ">" + esc(s.e + " " + s.n) + "</option>";
    }).join("");
    var kOpts = Object.keys(KINDS).map(function (k) { return '<option value="' + k + '"' + ((r.kind || "nastanitev") === k ? " selected" : "") + ">" + KINDS[k][0] + " " + KINDS[k][1] + "</option>"; }).join("");
    function f(id, label, val, ph, type) {
      return '<label class="mf">' + label + '<input id="bf-' + id + '" type="' + (type || "text") + '" value="' + esc(val || "") + '" placeholder="' + esc(ph || "") + '"></label>';
    }
    return '<section class="card-section book-form" id="book-form"><h2>' + (r.id ? "✏️ Uredi rezervacijo" : "➕ Nova rezervacija") + "</h2>" +
      '<label class="mf">Vrsta<select id="bf-kind">' + kOpts + "</select></label>" +
      f("title", "Naziv *", r.title, "npr. Hotel Granvia Kyoto, vlak Nozomi 12:30") +
      '<label class="mf">Postaja<select id="bf-station">' + stOpts + "</select></label>" +
      '<div class="mf-row">' + f("from", "Od", r.date_from, "", "date") + f("to", "Do", r.date_to, "", "date") + "</div>" +
      f("time", "Ura / opomba za čas", r.time_text, "npr. prijava od 15.00") +
      f("address", "Naslov (latinica)", r.address, "ulica, mesto") +
      f("local", "Naslov v japonščini (za taksista)", r.address_local, "kopirajte iz potrditve") +
      f("phone", "Telefon", r.phone, "+81 …") + f("conf", "Številka potrditve", r.conf, "") + f("url", "Povezava", r.url, "https://…") +
      '<label class="mf">Opombe<textarea id="bf-notes" rows="3">' + esc(r.notes || "") + "</textarea></label>" +
      '<div class="mf-row"><button type="button" class="buy-btn" id="bf-save">Shrani</button>' + (r.id ? '<button type="button" class="buy-btn alt" id="bf-cancel">Prekliči</button>' : "") + '</div><p class="buy-note" id="bf-msg" role="status"></p></section>';
  }

  function renderBook() {
    var list = merged(), stays = jd("stays-data") || [];
    var html = "";
    if (cachedView || TripData.pending()) html += '<p class="buy-note sync-note">' + (cachedView ? "📴 Prikazan je shranjen seznam. " : "") + (TripData.pending() ? "⏳ " + TripData.pending() + " sprememb čaka na povezavo." : "") + "</p>";
    // predlogi iz načrta
    var sug = stays.filter(function (s) { return !list.some(function (r) { return r.kind === "nastanitev" && r.station === s.k; }); });
    if (sug.length) {
      html += '<section class="card-section"><h2>💡 Še niste vpisale</h2><p class="cat-intro">Tapnite za hiter vnos nastanitve (datumi so že vneseni).</p><div class="buy-row">' +
        sug.map(function (s) { return '<button type="button" class="buy-btn alt bk-sug" data-k="' + esc(s.k) + '">' + esc(s.e + " " + s.n + " · " + dshort(s.ci) + "–" + dshort(s.co)) + "</button>"; }).join("") + "</div></section>";
    }
    Object.keys(KINDS).forEach(function (k) {
      var items = list.filter(function (r) { return (r.kind || "drugo") === k; });
      if (!items.length) return;
      html += '<section class="card-section"><h2>' + KINDS[k][0] + " " + KINDS[k][1] + "</h2>" + items.map(card).join("") + "</section>";
    });
    if (!list.length) html += '<section class="card-section"><p>Še ni vpisanih rezervacij. Dodajte prvo spodaj — vse, kar vpišete, vidijo vsi člani potovanja.</p></section>';
    html += form(editing);
    host.innerHTML = html;
    bind();
  }

  function bind() {
    host.querySelectorAll(".bk-copy").forEach(function (b) {
      b.addEventListener("click", function () {
        var t = b.getAttribute("data-copy");
        if (navigator.clipboard) navigator.clipboard.writeText(t).then(function () { b.textContent = "Kopirano ✓"; }, function () {});
      });
    });
    host.querySelectorAll(".bk-edit").forEach(function (b) {
      b.addEventListener("click", function () {
        editing = merged().filter(function (r) { return r.id === b.getAttribute("data-id"); })[0] || null;
        renderBook();
        var f = document.getElementById("book-form"); if (f) f.scrollIntoView({ behavior: "smooth" });
      });
    });
    host.querySelectorAll(".bk-del").forEach(function (b) {
      b.addEventListener("click", function () {
        var id = b.getAttribute("data-id");
        if (!window.confirm("Izbrišem to rezervacijo?")) return;
        if (String(id).indexOf("q") === 0) return;           // še neposlana: ni mogoče brisati
        TripData.write("trip_book_delete", { p_id: id }, "izbris rezervacije").then(refresh);
      });
    });
    host.querySelectorAll(".bk-sug").forEach(function (b) {
      b.addEventListener("click", function () {
        var s = (jd("stays-data") || []).filter(function (x) { return x.k === b.getAttribute("data-k"); })[0];
        if (!s) return;
        editing = { kind: "nastanitev", title: "Nastanitev — " + s.n, station: s.k, date_from: s.ci, date_to: s.co };
        renderBook();
        var f = document.getElementById("book-form"); if (f) f.scrollIntoView({ behavior: "smooth" });
      });
    });
    var sv = document.getElementById("bf-save");
    if (sv) sv.addEventListener("click", save);
    var cn = document.getElementById("bf-cancel");
    if (cn) cn.addEventListener("click", function () { editing = null; renderBook(); });
  }

  function save() {
    function v(id) { var e = document.getElementById("bf-" + id); return e ? e.value.trim() : ""; }
    var msg = document.getElementById("bf-msg");
    if (!v("title")) { msg.textContent = "Vpišite naziv."; return; }
    var data = { kind: v("kind"), title: v("title"), station: v("station"), date_from: v("from"), date_to: v("to"), time_text: v("time"), address: v("address"),
      address_local: v("local"), phone: v("phone"), conf: v("conf"), url: v("url"), notes: v("notes"), by: myName() };
    msg.textContent = "Shranjujem …";
    var id = editing && editing.id && String(editing.id).indexOf("q") !== 0 ? editing.id : null;
    TripData.write("trip_book_save", { p_id: id, p_data: data }, "rezervacija: " + data.title).then(function () { editing = null; return refresh(); })
      .catch(function (e) {
        if (tripAuthFail(e)) { tripReLogin(host, "Koda ni veljavna ali je seja potekla."); return; }
        msg.textContent = "Napaka pri shranjevanju.";
      });
  }

  /* ---------------------------------------------------------------- TAKSI */
  var SPEAK_OK = "speechSynthesis" in window;
  function speak(t) {
    if (!SPEAK_OK) return;
    try { speechSynthesis.cancel(); var u = new SpeechSynthesisUtterance(t); u.lang = "ja-JP"; u.rate = 0.85; speechSynthesis.speak(u); } catch (e) {}
  }

  function overlay(o) {
    var phrases = (jd("taxi-phrases") || []);
    var ov = document.createElement("div");
    ov.className = "taxi-ov";
    ov.innerHTML = '<div class="to-inner"><p class="to-top" lang="ja">この住所までお願いします。</p><p class="to-ro">Kono jūsho made onegai shimasu.</p><p class="to-sl">Na ta naslov, prosim.</p>' +
      '<div class="to-addr" lang="ja">' + esc(o.ja || o.local || "") + '</div><div class="to-lat">' + esc(o.lat || "") + "</div>" +
      (o.phone ? '<p class="to-lat">📞 ' + esc(o.phone) + "</p>" : "") +
      '<div class="to-btns">' + (o.map ? '<a class="buy-btn alt" href="' + esc(o.map) + '" target="_blank" rel="noopener">📍 Zemljevid</a>' : "") +
      '<button type="button" class="buy-btn alt" data-say="1">🔊 Poslušaj</button><button type="button" class="buy-btn" data-close="1">✕ Zapri</button></div>' +
      '<details class="to-ph"><summary>🗣️ Še fraze za taksi</summary>' + phrases.map(function (p) {
        return '<div class="to-ph-row"><div lang="ja" class="to-ph-ja">' + esc(p.ja) + '</div><div class="to-ph-ro">' + esc(p.ro) + '</div><div>' + esc(p.sl) +
          '</div><button type="button" class="bk-copy" data-say-t="' + esc(p.ja) + '">🔊</button></div>';
      }).join("") + "</details></div>";
    document.body.appendChild(ov);
    document.body.style.overflow = "hidden";
    function close() { ov.parentNode.removeChild(ov); document.body.style.overflow = ""; }
    ov.addEventListener("click", function (e) {
      var t = e.target;
      if (t.getAttribute("data-close")) close();
      if (t.getAttribute("data-say")) speak("この住所までお願いします。" + (o.ja || o.local || ""));
      if (t.getAttribute("data-say-t")) speak(t.getAttribute("data-say-t"));
    });
  }

  function renderTaxi() {
    var list = merged().filter(function (r) { return r.kind === "nastanitev" && (r.address_local || r.address); });
    var dests = jd("taxi-dests") || [];
    var html = "";
    if (cachedView || TripData.pending()) html += '<p class="buy-note sync-note">' + (cachedView ? "📴 Prikazan je shranjen seznam. " : "") + "</p>";
    html += '<section class="card-section"><h2>🏨 Moje nastanitve</h2>';
    if (!list.length) html += '<p>Še ni naslovov. V <a href="rezervacije.html">Moje rezervacije</a> vpišite nastanitev z naslovom (po možnosti tudi v japonščini — kopirajte ga iz potrditve) in se bo pojavila tukaj.</p>';
    list.forEach(function (r, i) {
      html += '<button type="button" class="taxi-card" data-i="' + i + '"><span class="tc-t">' + esc(r.title) + '</span><span class="tc-ja" lang="ja">' + esc(r.address_local || "") +
        '</span><span class="tc-l">' + esc(r.address || "") + '</span><span class="tc-go">🚕 Pokaži taksistu</span></button>';
    });
    html += "</section>";
    html += '<section class="card-section"><h2>📍 Pogosti cilji</h2><p class="cat-intro">Postaje in letališča — tapnite in pokažite voznika.</p><div class="taxi-grid">' +
      dests.map(function (d, i) { return '<button type="button" class="taxi-card small" data-d="' + i + '"><span class="tc-ja" lang="ja">' + esc(d.ja) + '</span><span class="tc-t">' + esc(d.sl) + "</span></button>"; }).join("") + "</div></section>";
    host.innerHTML = html;
    host.querySelectorAll(".taxi-card[data-i]").forEach(function (b) {
      b.addEventListener("click", function () {
        var r = list[parseInt(b.getAttribute("data-i"), 10)];
        overlay({ ja: r.address_local, local: r.address_local, lat: r.address, phone: r.phone, map: r.address ? gmaps(r.address) : "" });
      });
    });
    host.querySelectorAll(".taxi-card[data-d]").forEach(function (b) {
      b.addEventListener("click", function () {
        var d = dests[parseInt(b.getAttribute("data-d"), 10)];
        overlay({ ja: d.ja, lat: d.lat || d.sl, map: gmaps(d.lat || d.sl) });
      });
    });
  }

  function render() { if (bookHost) renderBook(); else renderTaxi(); }
  function refresh() { return load().then(render).catch(handleErr); }
  function handleErr(e) {
    if (tripAuthFail(e)) { tripReLogin(host, "Koda ni veljavna ali je seja potekla."); return; }
    if (taxiHost) { rows = []; cachedView = true; render(); return; }       // taksi deluje tudi brez seznama (pogosti cilji)
    host.innerHTML = '<section class="card-section"><h2>⚠️ Rezervacij ni mogoče naložiti</h2><p>Preverite internetno povezavo. Ko enkrat naložite seznam, deluje tudi brez interneta.</p><p><button type="button" class="buy-btn" id="bk-retry">🔄 Poskusi znova</button></p></section>';
    document.getElementById("bk-retry").addEventListener("click", boot);
  }
  function boot() {
    if (!TripData.pin()) { tripReLogin(host, "Seja je potekla."); return; }
    host.innerHTML = '<p class="buy-note">Nalagam …</p>';
    refresh();
  }
  boot();
  document.addEventListener("tripdata:synced", refresh);
})();
