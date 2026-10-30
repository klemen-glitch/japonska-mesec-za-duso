/* Service worker potovanja: aplikacija deluje tudi brez interneta.
   - strani, skripte, slogi: najprej splet (največ 3,5 s), sicer shranjena različica
   - slike, ikone: shranjene (stale-while-revalidate)
   - knjižnice (Leaflet, supabase-js …), zemljevidne ploščice in album slike: shranjene ob prvi uporabi
   - »Pripravi za brez interneta«: sporočilo {type:"precache-all"} naloži vse naenkrat */
var CACHE_NAME = "japonska-25";
var RT = "rt-1";
var PAGES = ["./", "./index.html", "./nasveti.html", "./nacrt.html", "./priprave.html", "./dozivetja.html", "./nalozi.html", "./izziv.html", "./nujno.html", "./kako.html", "./prevajalec.html", "./kviz.html", "./lov.html", "./knjiga.html", "./stroski.html", "./rezervacije.html", "./taksi.html", "./dnevnik.html", "./tokio.html", "./chichibu.html", "./kawaguchiko.html", "./minobusan.html", "./izu.html", "./kumano.html", "./koyasan.html", "./iya.html", "./ine.html", "./nara.html", "./kyoto.html", "./osaka.html", "./hiroshima.html", "./album.js", "./app.js", "./data.js", "./dnevnik.js", "./dokumenti.js", "./fun.js", "./knjiga.js", "./money.js", "./pogovor.js", "./prevajalec.js", "./rezervacije.js", "./zdravje.js", "./style.css", "./manifest.json", "./potovanje.ics", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/apple-touch-icon.png", "./icons/favicon.svg"];
var ASSETS = ["./images/chichibu.jpg", "./images/dozivetja.jpg", "./images/hero.jpg", "./images/hiroshima.jpg", "./images/ine.jpg", "./images/iya.jpg", "./images/izu.jpg", "./images/kawaguchiko.jpg", "./images/koyasan.jpg", "./images/kumano.jpg", "./images/kyoto.jpg", "./images/minobusan.jpg", "./images/nacrt.jpg", "./images/nara.jpg", "./images/osaka.jpg", "./images/priprave.jpg", "./images/tokio.jpg", "./images/thumbs/chichibu.jpg", "./images/thumbs/hiroshima.jpg", "./images/thumbs/ine.jpg", "./images/thumbs/iya.jpg", "./images/thumbs/izu.jpg", "./images/thumbs/kawaguchiko.jpg", "./images/thumbs/koyasan.jpg", "./images/thumbs/kumano.jpg", "./images/thumbs/kyoto.jpg", "./images/thumbs/minobusan.jpg", "./images/thumbs/nara.jpg", "./images/thumbs/osaka.jpg", "./images/thumbs/tokio.jpg"];
var CDN = ["https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css", "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js", "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2", "https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"];

function trim(cache, max) {
  cache.keys().then(function (keys) {
    if (keys.length > max) return Promise.all(keys.slice(0, keys.length - max).map(function (k) { return cache.delete(k); }));
  });
}
function putRT(req, res, max) {
  if (res && (res.ok || res.type === "opaque")) {
    var copy = res.clone();
    caches.open(RT).then(function (c) { c.put(req, copy).then(function () { if (max) trim(c, max); }); });
  }
  return res;
}
function cacheFirst(req, max) {
  return caches.match(req).then(function (hit) {
    return hit || fetch(req).then(function (res) { return putRT(req, res, max); });
  });
}
function swr(req, max) {
  return caches.match(req).then(function (hit) {
    var net = fetch(req).then(function (res) { return putRT(req, res, max); }).catch(function () { return hit; });
    return hit || net;
  });
}
function networkFirst(event) {
  var fresh = new Request(event.request.url, { cache: "reload" });
  var net = fetch(fresh).then(function (res) {
    var copy = res.clone();
    if (res.ok) caches.open(CACHE_NAME).then(function (c) { c.put(event.request, copy); });
    return res;
  });
  var timeout = new Promise(function (_, rej) { setTimeout(rej, 3500); });
  return Promise.race([net, timeout]).catch(function () {
    return caches.match(event.request, { ignoreSearch: true }).then(function (c) {
      return c || net.catch(function () { return caches.match("./index.html"); });
    });
  });
}

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      return Promise.all(PAGES.map(function (u) { return cache.add(u).catch(function () {}); }));
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE_NAME && k !== RT; }).map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (event) {
  var req = event.request;
  if (req.method !== "GET") return;
  var url = new URL(req.url);
  if (url.origin === self.location.origin) {
    var isHTML = req.mode === "navigate" || (req.headers.get("accept") || "").indexOf("text/html") !== -1;
    if (isHTML || /\.(css|js|json|ics)$/i.test(url.pathname)) { event.respondWith(networkFirst(event)); return; }
    event.respondWith(swr(req, 400));
    return;
  }
  var h = url.hostname;
  if (/\.supabase\.co$/.test(h)) {
    if (url.pathname.indexOf("/storage/v1/object/public/") === 0) event.respondWith(cacheFirst(req, 400));
    return;                                   // API (rpc) gre vedno na splet
  }
  if (/tile\.openstreetmap\.org$/.test(h)) { event.respondWith(swr(req, 600)); return; }
  if (/cdnjs\.cloudflare\.com$|cdn\.jsdelivr\.net$|unpkg\.com$/.test(h)) { event.respondWith(cacheFirst(req, 0)); return; }
});

self.addEventListener("message", function (event) {
  var d = event.data || {};
  if (d.type !== "precache-all") return;
  var jobs = [];
  PAGES.forEach(function (u) { jobs.push({ u: u, page: true }); });
  ASSETS.forEach(function (u) { jobs.push({ u: u }); });
  CDN.forEach(function (u) { jobs.push({ u: u, cdn: true }); });
  var done = 0, fail = 0, total = jobs.length, idx = 0;
  function notify(fin) {
    self.clients.matchAll().then(function (cs) {
      cs.forEach(function (c) { c.postMessage({ type: fin ? "precache-done" : "precache-progress", done: done, total: total, fail: fail }); });
    });
  }
  function worker(pa, pr) {
    if (idx >= jobs.length) return Promise.resolve();
    var j = jobs[idx++];
    var cache = j.page ? pa : pr;
    var rq = j.cdn ? new Request(j.u, { mode: "no-cors" }) : new Request(j.u, { cache: j.page ? "reload" : "default" });
    return fetch(rq).then(function (r) {
      if (r && (r.ok || r.type === "opaque")) return cache.put(j.u, r);
      fail++;
    }).catch(function () { fail++; }).then(function () {
      done++; if (done % 4 === 0) notify(false);
      return worker(pa, pr);
    });
  }
  event.waitUntil(caches.open(CACHE_NAME).then(function (pa) {
    return caches.open(RT).then(function (pr) { return Promise.all([worker(pa, pr), worker(pa, pr), worker(pa, pr), worker(pa, pr)]); });
  }).then(function () { notify(true); }));
});
