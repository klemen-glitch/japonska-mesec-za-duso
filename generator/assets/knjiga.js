/* ============================================================
   Potopisna knjiga: sestavi se iz fotografij v albumu (po postajah, z opisi izzivov), pripravljena za tisk / PDF.
   ============================================================ */
(function () {
  "use strict";
  var SB_URL = "https://ayejgzzaykbopojiacgn.supabase.co";
  var SB_KEY = "sb_publishable_vgNDW0KMTwSPstN0PhwySQ_SDuOUzn3";
  var BUCKET = "trip_album";
  var host = document.getElementById("book-host");
  if (!host || !window.supabase) return;
  var TRIP = window.TRIP || { id: "", people: [], stations: [] };
  var sb = window.supabase.createClient(SB_URL, SB_KEY);
  var HIDE_KEY = "book:hide:" + TRIP.id;
  var hidden = {};
  try { hidden = JSON.parse(localStorage.getItem(HIDE_KEY) || "{}"); } catch (e) { hidden = {}; }

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function session() { try { return JSON.parse(localStorage.getItem("trip_session") || "null"); } catch (e) { return null; } }
  function pin() { var s = session(); return (s && s.pin) || ""; }
  function pub(path) { return sb.storage.from(BUCKET).getPublicUrl(path).data.publicUrl; }
  function isVideo(m) { return (m || "").indexOf("video") === 0; }

  var challenges = {};
  try { JSON.parse(document.getElementById("izziv-data").textContent).forEach(function (c) { challenges[c.id] = c; }); } catch (e) {}

  function save() { try { localStorage.setItem(HIDE_KEY, JSON.stringify(hidden)); } catch (e) {} }

  function render(items) {
    var by = {};
    items.forEach(function (u) { (by[u.station || "drugo"] = by[u.station || "drugo"] || []).push(u); });
    var stations = (TRIP.stations || []).concat([{ k: "drugo", e: "✨", n: "Drugo" }]);
    var shown = items.filter(function (u) { return !hidden[u.path]; }).length;
    var html = '<div class="bk-toolbar no-print"><p><strong>' + shown + " od " + items.length + "</strong> fotografij je v knjigi. " +
      'Tapnite ✕ pri sliki, da jo izpustite; »Natisni« odpre tiskanje (izberite »Shrani kot PDF«).</p>' +
      '<button type="button" class="buy-btn" id="bk-print">🖨️ Natisni / shrani PDF</button> ' +
      '<button type="button" class="buy-btn alt" id="bk-reset">↩️ Vrni vse slike</button></div>';
    html += '<article class="bk-cover"><div class="bk-cover-e">📖</div><h1>' + esc(TRIP.title || "Potopisna knjiga") + "</h1>" +
      (TRIP.dates ? "<p>" + esc(TRIP.dates) + "</p>" : "") + "<p>" + esc((TRIP.people || []).join(", ")) + "</p></article>";
    var any = false;
    stations.forEach(function (s) {
      var arr = (by[s.k] || []).filter(function (u) { return true; });
      if (!arr.length) return;
      any = true;
      html += '<section class="bk-station"><h2>' + esc(s.e) + " " + esc(s.n) + "</h2><div class=\"bk-grid\">";
      arr.forEach(function (u) {
        var c = u.challenge_id ? challenges[u.challenge_id] : null;
        var off = !!hidden[u.path];
        html += '<figure class="bk-fig' + (off ? " off" : "") + '" data-p="' + esc(u.path) + '">' +
          '<button type="button" class="bk-x no-print" aria-label="' + (off ? "Vrni" : "Izpusti") + '">' + (off ? "↩" : "✕") + "</button>";
        if (isVideo(u.mime)) html += '<a class="bk-video" href="' + esc(pub(u.path)) + '" target="_blank" rel="noopener">🎥 Video (odpri)</a>';
        else html += '<img src="' + esc(pub(u.path)) + '" alt="' + esc(c ? c.x : s.n) + '" loading="lazy">';
        html += "<figcaption>" + (c ? "<strong>" + esc(c.x) + "</strong>" + (c.w ? "<span>" + esc(c.w) + "</span>" : "") : "") +
          (u.uploader ? '<em>— ' + esc(u.uploader) + "</em>" : "") + "</figcaption></figure>";
      });
      html += "</div></section>";
    });
    if (!any) html += '<p class="buy-note">Album je še prazen. Ko naložita fotografije, se tukaj sestavi knjiga.</p>';
    host.innerHTML = html;
    var pr = document.getElementById("bk-print"); if (pr) pr.addEventListener("click", function () { window.print(); });
    var rs = document.getElementById("bk-reset"); if (rs) rs.addEventListener("click", function () { hidden = {}; save(); render(items); });
    host.querySelectorAll(".bk-x").forEach(function (b) {
      b.addEventListener("click", function () {
        var p = b.closest(".bk-fig").getAttribute("data-p");
        if (hidden[p]) delete hidden[p]; else hidden[p] = 1;
        save(); render(items);
      });
    });
  }

  if (!pin()) { host.innerHTML = '<p class="buy-note">Seja je potekla. <a href="' + (TRIP.gate || "../index.html") + '?next=' + encodeURIComponent(TRIP.slug || "") + '">Vnesite kodo</a>.</p>'; return; }
  host.innerHTML = '<p class="buy-note">Nalagam album …</p>';
  sb.rpc("trip_album_list", { p_pin: pin(), p_trip: TRIP.id }).then(function (r) {
    if (r.error) throw r.error;
    render(r.data || []);
  }).catch(function () { host.innerHTML = '<p class="buy-note">Albuma ni mogoče naložiti. Preverite internet.</p>'; });
})();
