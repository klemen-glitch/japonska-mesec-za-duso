/* Dnevnik na strani postaje: zapis za dan na tej postaji (isti skupni dnevnik kot stran Dnevnik). */
(function () {
  "use strict";
  var box = document.querySelector(".diary[data-station]");
  if (!box || !window.TripData) return;
  var TRIP = window.TRIP || { id: "", people: [], days: [] };
  var key = box.getAttribute("data-station");
  var DAYS = (TRIP.days || []).filter(function (d) { return d.k === key; });
  var host = box.querySelector(".diary-live");
  if (!host) return;
  var rows = [], cached = false;
  var MON = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "avg", "sep", "okt", "nov", "dec"];

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function dl(iso) { var p = iso.split("-"); return parseInt(p[2], 10) + ". " + MON[parseInt(p[1], 10) - 1]; }
  function me() { try { return localStorage.getItem("album_name:" + TRIP.id) || ""; } catch (e) { return ""; } }
  function today() { return (typeof tripToday === "function") ? tripToday() : new Date().toISOString().slice(0, 10); }
  function isos() { return DAYS.map(function (d) { return d.iso; }); }

  function merged() {
    var out = rows.slice();
    TripData.getQ().forEach(function (it, i) {
      if (it.fn === "trip_diary_delete") out = out.filter(function (r) { return r.id !== it.args.p_id; });
      else if (it.fn === "trip_diary_add") out.push({ id: "q" + i, day: it.args.p_day, author: it.args.p_author, body: it.args.p_body, pending: true, source: "app" });
    });
    return out.filter(function (r) { return r.source !== "potopis" && isos().indexOf(r.day) >= 0; });
  }

  function render() {
    var list = merged(), t = today(), sel = isos().indexOf(t) >= 0 ? t : (isos()[0] || t), people = TRIP.people || [], m = me();
    var h = "";
    if (cached) h += '<p class="buy-note sync-note">📴 Prikazana je shranjena kopija.</p>';
    h += '<label class="mf">Kdo piše?<select id="dl-who">' + people.map(function (p) { return "<option" + (p === m ? " selected" : "") + ">" + esc(p) + "</option>"; }).join("") + "</select></label>";
    if (DAYS.length > 1) h += '<label class="mf">Dan<select id="dl-day">' + DAYS.map(function (d) { return '<option value="' + d.iso + '"' + (d.iso === sel ? " selected" : "") + ">Dan " + d.d + " · " + dl(d.iso) + "</option>"; }).join("") + "</select></label>";
    h += '<label class="mf">Vaši vtisi<textarea id="dl-text" rows="4" placeholder="Kaj ste videle, kaj je bilo najlepše, kaj smešno …"></textarea></label>' +
      '<button type="button" class="buy-btn" id="dl-save">Shrani v dnevnik</button><p class="buy-note" id="dl-msg" role="status"></p>';
    list.forEach(function (r) {
      h += '<article class="diary-entry"><p>' + (r.pending ? "⏳ " : "") + esc(r.body).replace(/\n/g, "<br>") + '</p><p class="bk-foot">— ' + esc(r.author) + " · " + dl(r.day) + "</p></article>";
    });
    host.innerHTML = h;
    document.getElementById("dl-save").addEventListener("click", save);
  }

  function save() {
    var msg = document.getElementById("dl-msg"), body = document.getElementById("dl-text").value.trim();
    if (!body) { msg.textContent = "Napišite nekaj besed."; return; }
    var who = document.getElementById("dl-who").value, dayEl = document.getElementById("dl-day");
    var day = dayEl ? dayEl.value : (isos().indexOf(today()) >= 0 ? today() : isos()[0]);
    if (!day) { msg.textContent = "Za to postajo ni določenega dne."; return; }
    msg.textContent = "Shranjujem …";
    TripData.write("trip_diary_add", { p_day: day, p_author: who, p_body: body }, "dnevnik")
      .then(function () { try { localStorage.setItem("album_name:" + TRIP.id, who); } catch (e) {} return refresh(); })
      .catch(function (e) {
        if (window.tripAuthFail && tripAuthFail(e)) { tripReLogin(host, "Koda ni veljavna ali je seja potekla."); return; }
        msg.textContent = "Napaka pri shranjevanju.";
      });
  }

  function refresh() {
    return TripData.list("trip_diary_list", "diary").then(function (r) { rows = r.data || []; cached = !!r.cached; render(); }).catch(function (e) {
      if (window.tripAuthFail && tripAuthFail(e)) { tripReLogin(host, "Seja je potekla."); return; }
      rows = []; cached = true; render();
    });
  }
  if (!TripData.pin()) { tripReLogin(host, "Seja je potekla."); return; }
  box.querySelector(".diary-lines") && box.querySelector(".diary-lines").remove();
  refresh();
  document.addEventListener("tripdata:synced", refresh);
})();
