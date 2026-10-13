/* ============================================================
   TripData — skupni sloj za podatke potovanja (Supabase RPC, zaščiteno s kodo).
   Deluje tudi brez interneta: zadnji seznam se shrani v telefon, zapisi pa čakajo v vrsti in se
   samodejno pošljejo, ko je povezava spet na voljo.
   ============================================================ */
(function () {
  "use strict";
  var SB_URL = "https://ayejgzzaykbopojiacgn.supabase.co";
  var SB_KEY = "sb_publishable_vgNDW0KMTwSPstN0PhwySQ_SDuOUzn3";
  var TRIP = window.TRIP || {};
  var sb = null;

  function client() {
    if (!sb && window.supabase) sb = window.supabase.createClient(SB_URL, SB_KEY, { auth: { persistSession: false, autoRefreshToken: false } });
    return sb;
  }
  function session() { try { return JSON.parse(localStorage.getItem("trip_session") || "null"); } catch (e) { return null; } }
  function pin() { var s = session(); return (s && s.pin) || ""; }
  /* napaka omrežja = brez kode napake (strežnik vedno vrne kodo, npr. P0001) */
  function isNetErr(e) { return !e || !e.code; }
  function isAuthErr(e) { return !!e && /ni_dostopa/.test(e.message || ""); }

  function rpc(fn, args) {
    var c = client();
    if (!c) return Promise.resolve({ error: { message: "ni_odjemalca" } });
    return c.rpc(fn, args).then(function (r) { return r; }, function (e) { return { error: { message: String(e) } }; });
  }

  function ckey(name) { return "td:" + TRIP.id + ":" + name; }
  function readCache(name) { try { return JSON.parse(localStorage.getItem(ckey(name)) || "null"); } catch (e) { return null; } }
  function writeCache(name, data) { try { localStorage.setItem(ckey(name), JSON.stringify({ t: Date.now(), d: data })); } catch (e) {} }

  /* branje seznama: spletno, sicer shranjena različica */
  function list(fn, name) {
    return rpc(fn, { p_pin: pin(), p_trip: TRIP.id }).then(function (r) {
      if (r.error) {
        if (!isNetErr(r.error)) throw r.error;
        var c = readCache(name);
        if (c) return { data: c.d, cached: true, t: c.t };
        throw r.error;
      }
      writeCache(name, r.data);
      return { data: r.data, cached: false };
    });
  }

  /* čakalna vrsta zapisov */
  function qkey() { return "tdq:" + TRIP.id; }
  function getQ() { try { return JSON.parse(localStorage.getItem(qkey()) || "[]"); } catch (e) { return []; } }
  function setQ(q) { try { localStorage.setItem(qkey(), JSON.stringify(q)); } catch (e) {} notify(); }
  function pending() { return getQ().length; }
  function notify() { try { document.dispatchEvent(new CustomEvent("tripdata:queue", { detail: pending() })); } catch (e) {} }

  /* pisanje: takoj, sicer v vrsto. args brez p_pin/p_trip. */
  function write(fn, args, label) {
    var full = Object.assign({ p_pin: pin(), p_trip: TRIP.id }, args);
    return rpc(fn, full).then(function (r) {
      if (r.error) {
        if (!isNetErr(r.error)) throw r.error;
        var q = getQ(); q.push({ fn: fn, args: args, t: Date.now(), label: label || "" }); setQ(q);
        return { queued: true };
      }
      return { queued: false, data: r.data };
    });
  }

  var flushing = false;
  function flush() {
    if (flushing || !navigator.onLine || !getQ().length) return Promise.resolve(0);
    flushing = true;
    var done = 0;
    function next() {
      var q = getQ();
      if (!q.length) { flushing = false; return Promise.resolve(done); }
      var it = q[0];
      return rpc(it.fn, Object.assign({ p_pin: pin(), p_trip: TRIP.id }, it.args)).then(function (r) {
        if (r.error && (isNetErr(r.error) || isAuthErr(r.error))) { flushing = false; return done; }
        q.shift(); setQ(q); done++;                    // uspeh ali trajna napaka strežnika: odstrani iz vrste
        return next();
      });
    }
    return next().then(function (n) {
      if (n) { try { document.dispatchEvent(new CustomEvent("tripdata:synced", { detail: n })); } catch (e) {} }
      return n;
    });
  }

  window.addEventListener("online", function () { setTimeout(flush, 600); });
  document.addEventListener("visibilitychange", function () { if (!document.hidden) flush(); });
  setTimeout(flush, 2500);

  window.TripData = { client: client, pin: pin, rpc: rpc, list: list, write: write, flush: flush, pending: pending, getQ: getQ,
    readCache: readCache, writeCache: writeCache, isNetErr: isNetErr, isAuthErr: isAuthErr, TRIP: TRIP };
})();
