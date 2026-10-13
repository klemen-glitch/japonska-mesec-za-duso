/* ============================================================
   Skupni dnevnik potovanja: povzetki dneva (napišejo jih v aplikaciji ali v Telegramu).
   Iz teh besedil se na koncu sestavi potopis.
   ============================================================ */
(function () {
  "use strict";
  var host = document.getElementById("diary-host");
  if (!host) return;
  if (!window.TripData) { host.innerHTML = '<p class="buy-note">Naloži se, ko je internet na voljo.</p>'; return; }
  var TRIP = window.TRIP || { id: "", people: [], days: [], stations: [] };
  var PEOPLE = TRIP.people || [], DAYS = TRIP.days || [];
  var rows = [], cachedView = false;
  var MON = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "avg", "sep", "okt", "nov", "dec"];

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function dlabel(iso) { var p = iso.split("-"); return parseInt(p[2], 10) + ". " + MON[parseInt(p[1], 10) - 1]; }
  function myName() { try { return localStorage.getItem("album_name:" + TRIP.id) || ""; } catch (e) { return ""; } }
  function todayIso() { return (typeof tripToday === "function") ? tripToday() : new Date().toISOString().slice(0, 10); }
  function station(k) { var s = (TRIP.stations || []).filter(function (x) { return x.k === k; })[0]; return s ? s.e + " " + s.n : ""; }

  function merged() {
    var q = TripData.getQ(), out = rows.slice();
    q.forEach(function (it, i) {
      if (it.fn === "trip_diary_delete") out = out.filter(function (r) { return r.id !== it.args.p_id; });
      else if (it.fn === "trip_diary_add") out.push({ id: "q" + i, day: it.args.p_day, author: it.args.p_author, body: it.args.p_body, source: "app", pending: true });
    });
    return out;
  }
  function load() { return TripData.list("trip_diary_list", "diary").then(function (r) { rows = r.data || []; cachedView = !!r.cached; }); }

  function render() {
    var list = merged(), t = todayIso(), me = myName();
    var html = "";
    if (cachedView || TripData.pending()) html += '<p class="buy-note sync-note">' + (cachedView ? "📴 Prikazan je shranjen dnevnik. " : "") + (TripData.pending() ? "⏳ " + TripData.pending() + " zapisov čaka na povezavo." : "") + "</p>";

    // potopis (sestavljen besedilni povzetek), če obstaja
    var pot = list.filter(function (r) { return r.source === "potopis"; });
    if (pot.length) {
      html += '<section class="card-section potopis"><h2>📖 Potopis</h2>' + pot.map(function (r) { return "<p>" + esc(r.body).replace(/\n/g, "<br>") + "</p>"; }).join("") + "</section>";
    }

    // obrazec
    var dayOpts = DAYS.filter(function (d) { return d.iso <= t; }).slice(-8).reverse().map(function (d) {
      return '<option value="' + d.iso + '"' + (d.iso === t ? " selected" : "") + ">Dan " + d.d + " · " + dlabel(d.iso) + " · " + esc(station(d.k)) + "</option>";
    }).join("");
    if (!dayOpts) dayOpts = DAYS.map(function (d) { return '<option value="' + d.iso + '">Dan ' + d.d + " · " + dlabel(d.iso) + "</option>"; }).join("");
    html += '<section class="card-section diary-form"><h2>✍️ Povzetek dneva</h2><p class="cat-intro">Kaj se je zgodilo danes? Nekaj stavkov zadostuje: kje ste bile, kaj ste videle, kaj je bilo najlepše in kaj smešno. Iz teh zapisov nastane potopis.</p>' +
      '<label class="mf">Kdo piše?<select id="df-who">' + PEOPLE.map(function (p) { return '<option' + (p === me ? " selected" : "") + ">" + esc(p) + "</option>"; }).join("") + "</select></label>" +
      '<label class="mf">Za kateri dan?<select id="df-day">' + dayOpts + "</select></label>" +
      '<label class="mf">Povzetek<textarea id="df-text" rows="6" placeholder="Danes smo …"></textarea></label>' +
      '<button type="button" class="buy-btn" id="df-save">Shrani povzetek</button><p class="buy-note" id="df-msg" role="status"></p></section>';

    // seznam po dnevih
    var byDay = {};
    list.filter(function (r) { return r.source !== "potopis"; }).forEach(function (r) { (byDay[r.day] = byDay[r.day] || []).push(r); });
    var keys = Object.keys(byDay).sort().reverse();
    html += '<section class="card-section"><h2>📚 Zapisano</h2>';
    if (!keys.length) html += "<p>Še ni zapisov.</p>";
    keys.forEach(function (day) {
      var dd = DAYS.filter(function (d) { return d.iso === day; })[0];
      html += '<h3 class="stay-sub">' + (dd ? "Dan " + dd.d + " · " : "") + dlabel(day) + (dd ? " · " + esc(station(dd.k)) : "") + "</h3>";
      byDay[day].forEach(function (r) {
        html += '<article class="diary-entry"><p>' + (r.pending ? "⏳ " : "") + esc(r.body).replace(/\n/g, "<br>") + '</p><p class="bk-foot">— ' + esc(r.author) +
          (r.source === "telegram" ? " · 📱 Telegram" : "") + (r.pending ? "" : ' <button type="button" class="bk-del df-del" data-id="' + esc(r.id) + '">🗑️</button>') + "</p></article>";
      });
    });
    html += "</section>";
    host.innerHTML = html;
    document.getElementById("df-save").addEventListener("click", save);
    host.querySelectorAll(".df-del").forEach(function (b) {
      b.addEventListener("click", function () {
        if (!window.confirm("Izbrišem ta zapis?")) return;
        TripData.write("trip_diary_delete", { p_id: b.getAttribute("data-id") }, "izbris zapisa").then(refresh);
      });
    });
  }

  function save() {
    var msg = document.getElementById("df-msg"), body = document.getElementById("df-text").value.trim();
    if (!body) { msg.textContent = "Napišite nekaj besed."; return; }
    msg.textContent = "Shranjujem …";
    TripData.write("trip_diary_add", { p_day: document.getElementById("df-day").value, p_author: document.getElementById("df-who").value, p_body: body }, "dnevnik")
      .then(function () { try { localStorage.setItem("album_name:" + TRIP.id, document.getElementById("df-who").value); } catch (e) {} return refresh(); })
      .catch(function (e) {
        if (tripAuthFail(e)) { tripReLogin(host, "Koda ni veljavna ali je seja potekla."); return; }
        msg.textContent = "Napaka pri shranjevanju.";
      });
  }

  function refresh() { return load().then(render).catch(handleErr); }
  function handleErr(e) {
    if (tripAuthFail(e)) { tripReLogin(host, "Koda ni veljavna ali je seja potekla."); return; }
    host.innerHTML = '<section class="card-section"><h2>⚠️ Dnevnika ni mogoče naložiti</h2><p>Preverite internetno povezavo.</p><p><button type="button" class="buy-btn" id="df-retry">🔄 Poskusi znova</button></p></section>';
    document.getElementById("df-retry").addEventListener("click", boot);
  }
  function boot() {
    if (!TripData.pin()) { tripReLogin(host, "Seja je potekla."); return; }
    host.innerHTML = '<p class="buy-note">Nalagam …</p>';
    refresh();
  }
  boot();
  document.addEventListener("tripdata:synced", refresh);
})();
