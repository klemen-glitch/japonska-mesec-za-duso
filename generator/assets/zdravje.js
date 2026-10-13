/* ============================================================
   Zdravstvena kartica (stran Nujno): vsak vpiše svoje podatke, vidijo jih vsi člani potovanja.
   Deluje tudi brez interneta (shranjena kopija), spremembe čakajo v vrsti.
   ============================================================ */
(function () {
  "use strict";
  var host = document.getElementById("zdravje-host");
  if (!host) return;
  if (!window.TripData) { host.innerHTML = '<p class="buy-note">Naloži se, ko je internet na voljo.</p>'; return; }
  var TRIP = window.TRIP || { id: "", people: [] };
  var PEOPLE = TRIP.people || [];
  var rows = {}, cachedView = false, current = "", editing = false;

  var FIELDS = [
    ["blood", "Krvna skupina", "血液型", "Blood type", "npr. A+"],
    ["allergies", "Alergije", "アレルギー", "Allergies", "zdravila, hrana, žuželke — ali »ni«"],
    ["meds", "Zdravila, ki jih jemlje", "服用中の薬", "Current medications", "ime + odmerek"],
    ["conditions", "Bolezni, stanja", "持病", "Medical conditions", "npr. sladkorna, tlak, srce"],
    ["birth", "Leto rojstva", "生年", "Year of birth", "npr. 1962"],
    ["insurer", "Zavarovalnica", "保険会社", "Insurance company", ""],
    ["policy", "Številka police", "保険証券番号", "Policy number", ""],
    ["assist", "Telefon zavarovalne asistence", "保険会社の緊急連絡先", "Insurance assistance phone", "+386 …"],
    ["contact", "Kontakt doma (ime + telefon)", "緊急連絡先", "Emergency contact (home)", "npr. Janez +386 …"],
    ["notes", "Druge pomembne informacije", "備考", "Other important notes", ""]
  ];

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function myName() { try { return localStorage.getItem("album_name:" + TRIP.id) || ""; } catch (e) { return ""; } }

  function merged() {
    var out = {};
    Object.keys(rows).forEach(function (p) { out[p] = Object.assign({}, rows[p]); });
    TripData.getQ().forEach(function (it) {
      if (it.fn === "trip_health_save") out[it.args.p_person] = Object.assign({}, it.args.p_data, { _pending: 1 });
    });
    return out;
  }
  function load() {
    return TripData.list("trip_health_list", "health").then(function (r) {
      rows = {}; (r.data || []).forEach(function (x) { rows[x.person] = x.data || {}; });
      cachedView = !!r.cached;
    });
  }

  function viewCard(p, d) {
    var filled = FIELDS.some(function (f) { return d[f[0]]; });
    var h = '<div class="hc"><h3>' + esc(p) + (d._pending ? " ⏳" : "") + "</h3>";
    if (!filled) h += '<p class="buy-note">Še ni vpisanih podatkov.</p>';
    else {
      h += '<dl class="hc-dl">' + FIELDS.map(function (f) { return d[f[0]] ? "<dt>" + f[1] + "</dt><dd>" + esc(d[f[0]]).replace(/\n/g, "<br>") + "</dd>" : ""; }).join("") + "</dl>";
    }
    h += '<div class="buy-row"><button type="button" class="buy-btn alt hc-edit">✏️ ' + (filled ? "Uredi" : "Vpiši") + '</button>' +
      (filled ? '<button type="button" class="buy-btn hc-show">🩺 Pokaži zdravniku</button>' : "") + "</div></div>";
    return h;
  }

  function editForm(p, d) {
    return '<div class="hc"><h3>✏️ ' + esc(p) + "</h3>" + FIELDS.map(function (f) {
      var big = f[0] === "meds" || f[0] === "conditions" || f[0] === "notes" || f[0] === "allergies";
      return '<label class="mf">' + f[1] + (big ? '<textarea id="hf-' + f[0] + '" rows="2" placeholder="' + esc(f[4]) + '">' + esc(d[f[0]] || "") + "</textarea>"
        : '<input id="hf-' + f[0] + '" type="text" value="' + esc(d[f[0]] || "") + '" placeholder="' + esc(f[4]) + '">') + "</label>";
    }).join("") + '<p class="buy-note">Podatke vidijo vsi člani potovanja (s skupno kodo). Vpišite le, kar je zares potrebno; najbolje v angleščini (ali latinici), da jih razume zdravnik.</p>' +
      '<div class="mf-row"><button type="button" class="buy-btn" id="hf-save">Shrani</button><button type="button" class="buy-btn alt" id="hf-cancel">Prekliči</button></div><p class="buy-note" id="hf-msg" role="status"></p></div>';
  }

  function render() {
    var all = merged();
    if (!current) current = (PEOPLE.indexOf(myName()) >= 0) ? myName() : PEOPLE[0] || "";
    var html = "";
    if (cachedView || TripData.pending()) html += '<p class="buy-note sync-note">' + (cachedView ? "📴 Prikazana je shranjena kopija. " : "") + (TripData.pending() ? "⏳ " + TripData.pending() + " sprememb čaka na povezavo." : "") + "</p>";
    html += '<div class="chip-row hc-tabs" role="tablist">' + PEOPLE.map(function (p) {
      var has = FIELDS.some(function (f) { return (all[p] || {})[f[0]]; });
      return '<button type="button" class="chip' + (p === current ? " on" : "") + '" data-p="' + esc(p) + '">' + (has ? "✅ " : "▫️ ") + esc(p) + "</button>";
    }).join("") + "</div>";
    html += editing ? editForm(current, all[current] || {}) : viewCard(current, all[current] || {});
    host.innerHTML = html;
    host.querySelectorAll(".hc-tabs .chip").forEach(function (b) {
      b.addEventListener("click", function () { current = b.getAttribute("data-p"); editing = false; render(); });
    });
    var ed = host.querySelector(".hc-edit"); if (ed) ed.addEventListener("click", function () { editing = true; render(); });
    var sh = host.querySelector(".hc-show"); if (sh) sh.addEventListener("click", function () { showDoctor(current, all[current] || {}); });
    var cn = document.getElementById("hf-cancel"); if (cn) cn.addEventListener("click", function () { editing = false; render(); });
    var sv = document.getElementById("hf-save"); if (sv) sv.addEventListener("click", save);
  }

  function save() {
    var data = {};
    FIELDS.forEach(function (f) { var e = document.getElementById("hf-" + f[0]); if (e && e.value.trim()) data[f[0]] = e.value.trim(); });
    var msg = document.getElementById("hf-msg"); msg.textContent = "Shranjujem …";
    TripData.write("trip_health_save", { p_person: current, p_data: data, p_by: myName() || current }, "zdravstvena kartica: " + current)
      .then(function () { editing = false; return refresh(); })
      .catch(function (e) {
        if (tripAuthFail(e)) { tripReLogin(host, "Koda ni veljavna ali je seja potekla."); return; }
        msg.textContent = "Napaka pri shranjevanju.";
      });
  }

  function showDoctor(p, d) {
    var ov = document.createElement("div");
    ov.className = "taxi-ov hc-ov";
    ov.innerHTML = '<div class="to-inner hc-doc"><p lang="ja" class="to-top">私は日本語が話せません。救急車を呼んでください。</p>' +
      '<p class="to-ro">I do not speak Japanese. Please call an ambulance (119) / Ne govorim japonsko.</p>' +
      '<table class="hc-table"><tr><th lang="ja">氏名</th><td><strong>' + esc(p) + '</strong><small>Name / Ime</small></td></tr>' +
      FIELDS.map(function (f) { return d[f[0]] ? '<tr><th lang="ja">' + f[2] + "</th><td>" + esc(d[f[0]]).replace(/\n/g, "<br>") + "<small>" + f[3] + " / " + f[1] + "</small></td></tr>" : ""; }).join("") +
      '</table><div class="to-btns"><button type="button" class="buy-btn" data-close="1">✕ Zapri</button></div></div>';
    document.body.appendChild(ov);
    document.body.style.overflow = "hidden";
    ov.addEventListener("click", function (e) {
      if (e.target.getAttribute("data-close")) { ov.parentNode.removeChild(ov); document.body.style.overflow = ""; }
    });
  }

  function refresh() { return load().then(render).catch(handleErr); }
  function handleErr(e) {
    if (tripAuthFail(e)) { tripReLogin(host, "Koda ni veljavna ali je seja potekla."); return; }
    rows = {}; cachedView = true; render();
  }
  function boot() {
    if (!TripData.pin()) { tripReLogin(host, "Seja je potekla."); return; }
    host.innerHTML = '<p class="buy-note">Nalagam …</p>';
    refresh();
  }
  boot();
  document.addEventListener("tripdata:synced", refresh);
})();
