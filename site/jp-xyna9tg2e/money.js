/* ============================================================
   Skupni stroški: vsi člani skupine vidijo isti seznam (shranjeno v Supabase, zaščiteno s kodo potovanja).
   Računanje po valutah (EUR in JPY ločeno), na koncu: kdo komu koliko. Zneski so v celih centih/jenih.
   ============================================================ */
(function () {
  "use strict";
  var SB_URL = "https://ayejgzzaykbopojiacgn.supabase.co";
  var SB_KEY = "sb_publishable_vgNDW0KMTwSPstN0PhwySQ_SDuOUzn3";
  var host = document.getElementById("money-host");
  if (!host || !window.supabase) return;
  var TRIP = window.TRIP || { id: "", people: [] };
  var PEOPLE = TRIP.people || [];
  var sb = window.supabase.createClient(SB_URL, SB_KEY);
  var rows = [];

  function session() { try { return JSON.parse(localStorage.getItem("trip_session") || "null"); } catch (e) { return null; } }
  function pin() { var s = session(); return (s && s.pin) || ""; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function minor(amount, cur) { return cur === "JPY" ? Math.round(amount) : Math.round(amount * 100); }
  function fmt(m, cur) {
    if (cur === "JPY") return Math.round(m).toLocaleString("sl-SI") + " ¥";
    return (m / 100).toLocaleString("sl-SI", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " €";
  }
  function myName() { try { return localStorage.getItem("album_name:" + TRIP.id) || ""; } catch (e) { return ""; } }
  function today() { var d = new Date(); return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2); }
  function rateJpy() { try { var c = JSON.parse(localStorage.getItem("fx:EURJPY") || "null"); if (c && c.r) return c.r; } catch (e) {} return 175; }

  function load() {
    return sb.rpc("trip_exp_list", { p_pin: pin(), p_trip: TRIP.id }).then(function (r) {
      if (r.error) throw r.error;
      rows = r.data || [];
    });
  }

  /* delitev: celi znesek (v centih/jenih) na enakovredne deleže, ostanek po abecedi */
  function shares(total, names) {
    var n = names.length, base = Math.floor(total / n), rem = total - base * n, out = {};
    names.slice().sort().forEach(function (nm, i) { out[nm] = base + (i < rem ? 1 : 0); });
    return out;
  }

  function balances(cur) {
    var net = {}; PEOPLE.forEach(function (p) { net[p] = 0; });
    var paidTotal = 0;
    rows.forEach(function (e) {
      if (e.currency !== cur) return;
      var tot = minor(parseFloat(e.amount), cur);
      paidTotal += tot;
      net[e.who] = (net[e.who] || 0) + tot;
      var sh = shares(tot, e.split);
      Object.keys(sh).forEach(function (nm) { net[nm] = (net[nm] || 0) - sh[nm]; });
    });
    return { net: net, total: paidTotal };
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
    var me = myName();
    var html = '<section class="card-section money-form"><h2>➕ Nov strošek</h2>' +
      '<label class="mf">Kdo je plačal?<select id="m-who">' + PEOPLE.map(function (p) { return '<option' + (p === me ? " selected" : "") + ">" + esc(p) + "</option>"; }).join("") + "</select></label>" +
      '<label class="mf">Kaj?<input id="m-what" type="text" maxlength="100" placeholder="npr. večerja, vlak, vstopnice"></label>' +
      '<div class="mf-row"><label class="mf">Znesek<input id="m-amt" type="number" inputmode="decimal" step="0.01" min="0" placeholder="0"></label>' +
      '<label class="mf">Valuta<select id="m-cur"><option value="JPY">¥ jeni</option><option value="EUR">€ evri</option></select></label></div>' +
      '<fieldset class="mf-split"><legend>Za koga? (delitev na enake dele)</legend>' +
      PEOPLE.map(function (p) { return '<label class="mf-chk"><input type="checkbox" value="' + esc(p) + '" checked> ' + esc(p) + "</label>"; }).join("") + "</fieldset>" +
      '<label class="mf">Datum<input id="m-day" type="date" value="' + today() + '"></label>' +
      '<button type="button" class="buy-btn" id="m-add">Dodaj strošek</button><p class="buy-note" id="m-msg" role="status"></p></section>';

    // stanje
    html += '<section class="card-section money-sum"><h2>⚖️ Kdo komu koliko</h2>';
    var any = false;
    ["JPY", "EUR"].forEach(function (cur) {
      var b = balances(cur);
      if (!b.total) return;
      any = true;
      var st = settle(b.net);
      html += '<h3 class="stay-sub">' + (cur === "JPY" ? "¥ Jeni" : "€ Evri") + " · skupaj porabljeno: " + fmt(b.total, cur) +
        (cur === "JPY" ? " (≈ " + fmt(Math.round(b.total / rateJpy() * 100), "EUR") + ")" : "") + "</h3>";
      if (!st.length) html += "<p>Vse je poravnano. ✅</p>";
      else html += '<ul class="settle">' + st.map(function (s) { return "<li><b>" + esc(s.from) + "</b> → <b>" + esc(s.to) + "</b>: " + fmt(s.amt, cur) + "</li>"; }).join("") + "</ul>";
      html += '<p class="buy-note">Plačali: ' + PEOPLE.map(function (p) {
        var paid = 0; rows.forEach(function (e) { if (e.currency === cur && e.who === p) paid += minor(parseFloat(e.amount), cur); });
        return esc(p) + " " + fmt(paid, cur);
      }).join(" · ") + "</p>";
    });
    if (!any) html += "<p>Še ni stroškov. Dodajte prvega zgoraj.</p>";
    html += "</section>";

    // seznam
    html += '<section class="card-section money-list"><h2>🧾 Vsi stroški</h2><ul class="exp-list">';
    rows.slice().reverse().forEach(function (e) {
      var cur = e.currency, tot = minor(parseFloat(e.amount), cur);
      html += '<li><div><strong>' + esc(e.what) + "</strong><span class=\"exp-meta\">" + esc(e.who) + " plačal/-a · za " +
        (e.split.length === PEOPLE.length ? "vse" : e.split.map(esc).join(", ")) + (e.day ? " · " + esc(e.day) : "") + '</span></div><div class="exp-r"><b>' +
        fmt(tot, cur) + '</b><button type="button" class="exp-del" data-id="' + esc(e.id) + '" aria-label="Izbriši">🗑️</button></div></li>';
    });
    if (!rows.length) html += "<li><em>Prazno.</em></li>";
    html += '</ul><p class="buy-note">Vsi člani skupine vidijo isti seznam. Brisanje označi strošek kot izbrisan (ostane v bazi, a se ne šteje). Zneski v jenih in evrih se računajo ločeno.</p>' +
      '<button type="button" class="chk-reset" id="m-refresh">🔄 Osveži</button></section>';

    host.innerHTML = html;
    document.getElementById("m-add").addEventListener("click", add);
    document.getElementById("m-refresh").addEventListener("click", function () { load().then(render); });
    host.querySelectorAll(".exp-del").forEach(function (b) {
      b.addEventListener("click", function () {
        if (!window.confirm("Izbrišem ta strošek?")) return;
        sb.rpc("trip_exp_delete", { p_pin: pin(), p_trip: TRIP.id, p_id: b.getAttribute("data-id") }).then(function () { return load(); }).then(render);
      });
    });
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
    sb.rpc("trip_exp_add", { p_pin: pin(), p_trip: TRIP.id, p_who: who, p_what: what, p_amount: amt, p_currency: cur, p_split: split, p_day: day })
      .then(function (r) { if (r.error) throw r.error; return load(); })
      .then(render)
      .catch(function () { msg.textContent = "Napaka pri shranjevanju. Preverite internet in poskusite znova."; });
  }

  if (!pin()) { host.innerHTML = '<p class="buy-note">Seja je potekla. <a href="' + (TRIP.gate || "../index.html") + '?next=' + encodeURIComponent(TRIP.slug || "") + '">Vnesite kodo</a>.</p>'; return; }
  load().then(render).catch(function () { host.innerHTML = '<p class="buy-note">Stroškov ni mogoče naložiti (brez povezave?). Poskusite znova.</p>'; });
  setInterval(function () { if (!document.hidden && !document.activeElement.closest(".money-form")) load().then(render).catch(function () {}); }, 45000);
})();
