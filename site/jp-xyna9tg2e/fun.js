/* ============================================================
   Kviz in zbiralni »lov« (shranjeno v telefonu; ključi so ločeni po potovanju prek SK()).
   ============================================================ */
(function () {
  "use strict";

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }
  function lsGet(k) { try { return localStorage.getItem(SK(k)); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(SK(k), v); } catch (e) {} }
  function shuffle(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }

  /* ---------------------------------------------------------- KVIZ */
  function initQuiz() {
    var stage = document.getElementById("quiz-stage"), dataEl = document.getElementById("quiz-data");
    if (!stage || !dataEl) return;
    var cfg = {}; try { cfg = JSON.parse(dataEl.textContent); } catch (e) { return; }
    var all = cfg.questions || [], ranks = cfg.ranks || [];
    var order, pos, score, locked;

    function best() { var b = parseInt(lsGet("quiz:best") || "0", 10); return isNaN(b) ? 0 : b; }

    function start() {
      order = shuffle(all.map(function (_, i) { return i; }));
      pos = 0; score = 0; locked = false;
      step();
    }

    function rankFor(s) {
      var r = ranks[0] || "";
      ranks.forEach(function (x) { if (s >= x.min) r = x; });
      return r;
    }

    function step() {
      if (pos >= order.length) return finish();
      var q = all[order[pos]];
      locked = false;
      var html = '<div class="qz-top"><span>Vprašanje ' + (pos + 1) + " / " + order.length + '</span><span>⭐ ' + score + '</span></div>' +
        '<div class="qz-bar"><i style="width:' + Math.round(pos * 100 / order.length) + '%"></i></div>' +
        '<h2 class="qz-q">' + esc(q.q) + "</h2><div class=\"qz-opts\">";
      q.a.forEach(function (o, i) { html += '<button type="button" class="qz-opt" data-i="' + i + '">' + esc(o) + "</button>"; });
      html += '</div><div class="qz-fb" aria-live="polite"></div>';
      stage.innerHTML = html;
      stage.querySelectorAll(".qz-opt").forEach(function (b) {
        b.addEventListener("click", function () { answer(q, parseInt(b.getAttribute("data-i"), 10)); });
      });
    }

    function answer(q, i) {
      if (locked) return;
      locked = true;
      var ok = i === q.c;
      if (ok) score++;
      stage.querySelectorAll(".qz-opt").forEach(function (b) {
        var bi = parseInt(b.getAttribute("data-i"), 10);
        b.disabled = true;
        if (bi === q.c) b.classList.add("right");
        else if (bi === i) b.classList.add("wrong");
      });
      var fb = stage.querySelector(".qz-fb");
      fb.innerHTML = '<p class="qz-res ' + (ok ? "ok" : "no") + '">' + (ok ? "✅ Pravilno!" : "❌ Ni čisto tako.") + "</p>" +
        (q.e ? "<p>" + esc(q.e) + "</p>" : "") +
        '<button type="button" class="qz-next">' + (pos + 1 >= order.length ? "Poglej rezultat →" : "Naprej →") + "</button>";
      fb.querySelector(".qz-next").addEventListener("click", function () { pos++; step(); });
      fb.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    function finish() {
      var b = best(), isBest = score > b;
      if (isBest) lsSet("quiz:best", String(score));
      var r = rankFor(score);
      stage.innerHTML = '<div class="qz-end"><div class="qz-emoji">' + esc((r && r.e) || "🏆") + '</div><h2>' + score + " / " + order.length +
        '</h2><p class="qz-rank">' + esc((r && r.t) || "") + '</p><p>' + esc((r && r.x) || "") + "</p>" +
        '<p class="qz-best">Najboljši rezultat: ' + Math.max(b, score) + " / " + all.length + (isBest ? " 🎉 nov rekord!" : "") +
        '</p><button type="button" class="qz-next">🔁 Igraj znova</button></div>';
      stage.querySelector(".qz-next").addEventListener("click", start);
    }

    var intro = document.getElementById("quiz-best");
    if (intro) { var bb = best(); intro.textContent = bb ? "Najboljši rezultat do zdaj: " + bb + " / " + all.length : ""; }
    start();
  }

  /* ---------------------------------------------------------- LOV (zbiralna lista) */
  function initLov() {
    var host = document.getElementById("lov-host"), dataEl = document.getElementById("lov-data");
    if (!host || !dataEl) return;
    var groups = []; try { groups = JSON.parse(dataEl.textContent); } catch (e) { return; }
    var state = {};
    try { state = JSON.parse(lsGet("lov") || "{}"); } catch (e) { state = {}; }
    var total = 0;
    groups.forEach(function (g) { g.items.forEach(function (it) { if (!it.count) total++; }); });

    function save() { lsSet("lov", JSON.stringify(state)); }
    function done() { var n = 0; groups.forEach(function (g) { g.items.forEach(function (it) { if (!it.count && state[it.id]) n++; }); }); return n; }

    function render() {
      var n = done(), pct = total ? Math.round(n * 100 / total) : 0;
      var html = '<div class="lov-prog"><div class="ov-top"><strong>Zbrano: ' + n + " / " + total + "</strong><span>" + pct +
        ' %</span></div><div class="ov-bar"><i style="width:' + pct + '%"></i></div>' +
        (n === total && total ? '<p class="lov-win">🏆 Vse zbrano! Odlično — pošljita sliko v album.</p>' : "") + "</div>";
      groups.forEach(function (g) {
        var gd = g.items.filter(function (it) { return !it.count && state[it.id]; }).length;
        var gt = g.items.filter(function (it) { return !it.count; }).length;
        html += '<section class="card-section lov-group"><h2>' + esc(g.t) + (gt ? ' <em class="lov-cnt">' + gd + "/" + gt + "</em>" : "") + "</h2>";
        if (g.x) html += '<p class="cat-intro">' + esc(g.x) + "</p>";
        html += '<div class="lov-grid">';
        g.items.forEach(function (it) {
          if (it.count) {
            var c = parseInt(state[it.id] || "0", 10) || 0;
            html += '<div class="lov-tile lov-count' + (c ? " on" : "") + '" data-id="' + esc(it.id) + '"><span class="lov-e">' + esc(it.e) +
              '</span><span class="lov-n">' + esc(it.n) + '</span><span class="lov-ctl"><button type="button" data-d="-1" aria-label="Manj">−</button><b>' + c +
              '</b><button type="button" data-d="1" aria-label="Več">+</button></span></div>';
          } else {
            var on = !!state[it.id];
            html += '<button type="button" class="lov-tile' + (on ? " on" : "") + '" data-id="' + esc(it.id) + '" aria-pressed="' + on + '"><span class="lov-e">' +
              esc(it.e) + '</span><span class="lov-n">' + esc(it.n) + "</span>" + (it.h ? '<span class="lov-h">' + esc(it.h) + "</span>" : "") +
              '<span class="lov-ok">' + (on ? "✓" : "") + "</span></button>";
          }
        });
        html += "</div></section>";
      });
      html += '<p class="lov-foot"><button type="button" class="chk-reset" id="lov-reset">Počisti vse</button></p>';
      host.innerHTML = html;
      host.querySelectorAll("button.lov-tile").forEach(function (b) {
        b.addEventListener("click", function () { var id = b.getAttribute("data-id"); state[id] = state[id] ? 0 : 1; save(); render(); });
      });
      host.querySelectorAll(".lov-count button").forEach(function (b) {
        b.addEventListener("click", function () {
          var id = b.closest(".lov-tile").getAttribute("data-id");
          var c = (parseInt(state[id] || "0", 10) || 0) + parseInt(b.getAttribute("data-d"), 10);
          state[id] = Math.max(0, c); save(); render();
        });
      });
      var rs = document.getElementById("lov-reset");
      if (rs) rs.addEventListener("click", function () { if (window.confirm("Res počistim vse oznake?")) { state = {}; save(); render(); } });
    }
    render();
  }

  function init() { initQuiz(); initLov(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
