/* ============================================================
   Skupni stroški: vsi člani skupine vidijo isti seznam (Supabase, zaščiteno s kodo potovanja).
   Deluje tudi brez interneta (shranjen seznam + čakalna vrsta). Računanje po valutah (EUR in JPY ločeno);
   zneski so v celih centih/jenih.
   ============================================================ */
(function () {
  "use strict";
  var host = document.getElementById("money-host");
  if (!host) return;
  if (!window.TripData) { host.innerHTML = '<p class="buy-note">Naloži se, ko je internet na voljo.</p>'; return; }
  var TRIP = window.TRIP || { id: "", people: [] };
  var PEOPLE = TRIP.people || [];
  var rows = [], cachedView = false;

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function minor(amount, cur) { return cur === "JPY" ? Math.round(amount) : Math.round(amount * 100); }
  function fmt(m, cur) {
    if (cur === "JPY") return Math.round(m).toLocaleString("sl-SI") + " ¥";
    return (m / 100).toLocaleString("sl-SI", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " €";
  }
  function myName() { try { return localStorage.getItem("album_name:" + TRIP.id) || ""; } catch (e) { return ""; } }
  function today() { var d = new Date(); return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2); }
  function rateJpy() { try { var c = JSON.parse(localStorage.getItem("fx:EURJPY") || "null"); if (c && c.r) return c.r; } catch (e) {} return 175; }

  /* seznam = strežnik + še neposlani zapisi iz vrste (označeni ⏳); izbrisani iz vrste se skrijejo */
  function merged() {
    var q = TripData.getQ(), gone = {}, out = rows.slice();
    q.forEach(function (it) { if (it.fn === "trip_exp_delete") gone[it.args.p_id] = 1; });
    out = out.filter(function (e) { return !gone[e.id]; });
    q.forEach(function (it, i) {
      if (it.fn !== "trip_exp_add") return;
      var a = it.args;
      out.push({ id: "q" + i, who: a.p_who, what: a.p_what, amount: a.p_amount, currency: a.p_currency, split: a.p_split, day: a.p_day, pending: true });
    });
    return out;
  }

  function load() {
    return TripData.list("trip_exp_list", "exp").then(function (r) { rows = r.data || []; cachedView = !!r.cached; });
  }

  function shares(total, names) {
    var n = names.length, base = Math.floor(total / n), rem = total - base * n, out = {};
    names.slice().sort().forEach(function (nm, i) { out[nm] = base + (i < rem ? 1 : 0); });
    return out;
  }
  function balances(list, cur) {
    var net = {}; PEOPLE.forEach(function (p) { net[p] = 0; });
    var total = 0;
    list.forEach(function (e) {
      if (e.currency !== cur) return;
      var tot = minor(parseFloat(e.amount), cur);
      total += tot;
      net[e.who] = (net[e.who] || 0) + tot;
      var sh = shares(tot, e.split);
      Object.keys(sh).forEach(function (nm) { net[nm] = (net[nm] || 0) - sh[nm]; });
    });
    return { net: net, total: total };
  }
  function settle(net) {
    var cr = [], db = [], out = [];
    Object.keys(net).forEach(function (k) { if (net[k] > 0) cr.push([k, net[k]]); else if (net[k] < 0) db.push([k, -net[k]]); });
    cr.sort(function (a, b) { return b[1] - a[1]; }); db.sort(function (a, b) { return b[1] - a[1]; });
    var i = 0, j = 0;
    while (i < db.length && j < cr.length) {
      var x = Math.min(db[i][1], cr[j][1]);
      if (x > 0) out.push({ from: db[i][0], to: cr[j][0], amt: x });
      db[i][1] -= x; cr[j][1] -= x;
      if (db[i][1] === 0) i++;
      if (cr[j][1] === 0) j++;
    }
    return out;
  }

  function render() {
    var list = merged(), me = myName();
    var html = "";
    if (cachedView || TripData.pending()) {
      html += '<p class="buy-note sync-note">' + (cachedView ? "📴 Prikazan je shranjen seznam. " : "") +
        (TripData.pending() ? "⏳ " + TripData.pending() + " zapisov čaka na povezavo." : "") + "</p>";
    }
    html += '<section class="card-section money-form"><h2>➕ Nov strošek</h2>' +
      '<label class="mf">Kdo je plačal?<select id="m-who">' + PEOPLE.map(function (p) { return '<option' + (p === me ? " selected" : "") + ">" + esc(p) + "</option>"; }).join("") + "</select></label>" +
      '<label class="mf">Kaj?<input id="m-what" type="text" maxlength="100" placeholder="npr. večerja, vlak, vstopnice"></label>' +
      '<div class="mf-row"><label class="mf">Znesek<input id="m-amt" type="number" inputmode="decimal" step="0.01" min="0" placeholder="0"></label>' +
      '<label class="mf">Valuta<select id="m-cur"><option value="JPY">¥ jeni</option><option value="EUR">€ evri</option></select></label></div>' +
      '<fieldset class="mf-split"><legend>Za koga? (delitev na enake dele)</legend>' +
      PEOPLE.map(function (p) { return '<label class="mf-chk"><input type="checkbox" value="' + esc(p) + '" checked> ' + esc(p) + "</label>"; }).join("") + "</fieldset>" +
      '<label class="mf">Datum<input id="m-day" type="date" value="' + today() + '"></label>' +
      '<button type="button" class="buy-btn" id="m-add">Dodaj strošek</button><p class="buy-note" id="m-msg" role="status"></p></section>';

    html += '<section class="card-section money-sum"><h2>⚖️ Kdo komu koliko</h2>';
    var any = false;
    ["JPY", "EUR"].forEach(function (cur) {
      var b = balances(list, cur);
      if (!b.total) return;
      any = true;
      var st = settle(b.net);
      html += '<h3 class="stay-sub">' + (cur === "JPY" ? "¥ Jeni" : "€ Evri") + " · skupaj porabljeno: " + fmt(b.total, cur) +
        (cur === "JPY" ? " (≈ " + fmt(Math.round(b.total / rateJpy() * 100), "EUR") + ")" : "") + "</h3>";
      if (!st.length) html += "<p>Vse je poravnano. ✅</p>";
      else html += '<ul class="settle">' + st.map(function (s) { return "<li><b>" + esc(s.from) + "</b> → <b>" + esc(s.to) + "</b>: " + fmt(s.amt, cur) + "</li>"; }).join("") + "</ul>";
      html += '<p class="buy-note">Plačali: ' + PEOPLE.map(function (p) {
        var paid = 0; list.forEach(function (e) { if (e.currency === cur && e.who === p) paid += minor(parseFloat(e.amount), cur); });
        return esc(p) + " " + fmt(paid, cur);
      }).join(" · ") + "</p>";
    });
    if (!any) html += "<p>Še ni stroškov. Dodajte prvega zgoraj.</p>";
    html += "</section>";

    html += '<section class="card-section money-list"><h2>🧾 Vsi stroški</h2><ul class="exp-list">';
    list.slice().reverse().forEach(function (e) {
      var cur = e.currency, tot = minor(parseFloat(e.amount), cur);
      html += '<li><div><strong>' + (e.pending ? "⏳ " : "") + esc(e.what) + "</strong><span class=\"exp-meta\">" + esc(e.who) + " plačal/-a · za " +
        (e.split.length === PEOPLE.length ? "vse" : e.split.map(esc).join(", ")) + (e.day ? " · " + esc(e.day) : "") + '</span></div><div class="exp-r"><b>' +
        fmt(tot, cur) + "</b>" + (e.pending ? "" : '<button type="button" class="exp-del" data-id="' + esc(e.id) + '" aria-label="Izbriši">🗑️</button>') + "</div></li>";
    });
    if (!list.length) html += "<li><em>Prazno.</em></li>";
    html += '</ul><p class="buy-note">Vsi člani skupine vidijo isti seznam. Brisanje označi strošek kot izbrisan. Brez interneta se zapisi shranijo in pošljejo sami.</p>' +
      '<button type="button" class="chk-reset" id="m-refresh">🔄 Osveži</button></section>';

    host.innerHTML = html;
    document.getElementById("m-add").addEventListener("click", add);
    document.getElementById("m-refresh").addEventListener("click", function () { refresh(); });
    host.querySelectorAll(".exp-del").forEach(function (b) {
      b.addEventListener("click", function () {
        if (!window.confirm("Izbrišem ta strošek?")) return;
        TripData.write("trip_exp_delete", { p_id: b.getAttribute("data-id") }, "izbris stroška").then(function () { return refresh(); });
      });
    });
  }

  function refresh() { return load().then(render).catch(handleErr); }

  function handleErr(e) {
    if (tripAuthFail(e)) { tripReLogin(host, "Koda ni veljavna ali je seja potekla."); return; }
    var busy = e && /prevec_poskusov/.test(e.message || "");
    host.innerHTML = '<section class="card-section"><h2>⚠️ Stroškov ni mogoče naložiti</h2><p>' +
      (busy ? "Preveč poskusov — počakajte nekaj minut." : "Preverite internetno povezavo. Ko enkrat naložite seznam, deluje tudi brez interneta.") +
      '</p><p><button type="button" class="buy-btn" id="m-retry">🔄 Poskusi znova</button></p></section>';
    document.getElementById("m-retry").addEventListener("click", boot);
  }

  function add() {
    var msg = document.getElementById("m-msg");
    var who = document.getElementById("m-who").value, what = document.getElementById("m-what").value.trim();
    var amt = parseFloat(String(document.getElementById("m-amt").value).replace(",", "."));
    var cur = document.getElementById("m-cur").value, day = document.getElementById("m-day").value || null;
    var split = [].slice.call(host.querySelectorAll(".mf-split input:checked")).map(function (i) { return i.value; });
    if (!what) { msg.textContent = "Vpišite, kaj je bilo plačano."; return; }
    if (isNaN(amt) || amt <= 0) { msg.textContent = "Vpišite znesek."; return; }
    if (!split.length) { msg.textContent = "Izberite vsaj eno osebo."; return; }
    msg.textContent = "Shranjujem …";
    TripData.write("trip_exp_add", { p_who: who, p_what: what, p_amount: amt, p_currency: cur, p_split: split, p_day: day }, "strošek: " + what)
      .then(function () { return refresh(); })
      .catch(function (e) {
        if (tripAuthFail(e)) { tripReLogin(host, "Koda ni veljavna ali je seja potekla."); return; }
        msg.textContent = "Napaka pri shranjevanju. Poskusite znova.";
      });
  }

  function boot() {
    if (!TripData.pin()) { tripReLogin(host, "Seja je potekla."); return; }
    host.innerHTML = '<p class="buy-note">Nalagam stroške …</p>';
    refresh();
  }
  boot();
  document.addEventListener("tripdata:synced", function () { refresh(); });
  document.addEventListener("tripdata:queue", function () { if (document.querySelector(".sync-note")) render(); });
  setInterval(function () {
    if (!document.hidden && navigator.onLine && !(document.activeElement && document.activeElement.closest && document.activeElement.closest(".money-form"))) refresh();
  }, 45000);
})();
