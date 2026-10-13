/* Preprost service worker: shrani strani v predpomnilnik,
   da osnovne informacije delujejo tudi brez interneta.
   Ob spremembi strani povečaj številko različice spodaj. */

var CACHE_NAME = "japonska-2026-v16";

var PAGES = [
  "./",
  "./index.html",
  "./tokio.html",
  "./chichibu.html",
  "./kawaguchiko.html",
  "./minobusan.html",
  "./izu.html",
  "./kumano.html",
  "./koyasan.html",
  "./iya.html",
  "./ine.html",
  "./nara.html",
  "./kyoto.html",
  "./osaka.html",
  "./hiroshima.html",
  "./nasveti.html",
  "./nacrt.html",
  "./priprave.html",
  "./dozivetja.html",
  "./nalozi.html",
  "./izziv.html",
  "./nujno.html",
  "./style.css",
  "./app.js",
  "./album.js",
  "./manifest.json",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/apple-touch-icon.png",
  "./icons/favicon.svg"
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      return cache.addAll(PAGES);
    }).then(function () {
      return self.skipWaiting();
    })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.filter(function (k) { return k !== CACHE_NAME; })
            .map(function (k) { return caches.delete(k); })
      );
    }).then(function () {
      return self.clients.claim();
    })
  );
});

/* Strategija: najprej poskusi splet (da so novosti vedno vidne),
   če ni povezave, postrezi shranjeno različico.
   Za strani, CSS in JS obidemo brskalnikov predpomnilnik (cache: "reload"),
   da nikoli ne obtičimo na stari različici; slike se normalno predpomnijo. */
self.addEventListener("fetch", function (event) {
  if (event.request.method !== "GET") return;
  var url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return; // YouTube, zemljevidi ipd. pusti pri miru

  var isHTML = event.request.mode === "navigate" ||
               (event.request.headers.get("accept") || "").indexOf("text/html") !== -1;
  var fresh = isHTML || /\.(css|js|json)$/i.test(url.pathname);
  var req = fresh ? new Request(event.request.url, { cache: "reload" }) : event.request;

  event.respondWith(
    fetch(req)
      .then(function (response) {
        var copy = response.clone();
        caches.open(CACHE_NAME).then(function (cache) {
          cache.put(event.request, copy);
        });
        return response;
      })
      .catch(function () {
        return caches.match(event.request).then(function (cached) {
          return cached || caches.match("./index.html");
        });
      })
  );
});
