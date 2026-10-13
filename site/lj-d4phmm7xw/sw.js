/* Service worker potovanja: najprej splet (sveže), sicer predpomnilnik. */
var CACHE_NAME = "ljubljana-19";
var PAGES = ["./", "./index.html", "./nacrt.html", "./priprave.html", "./nalozi.html", "./izziv.html", "./nujno.html", "./kako.html", "./vlak.html", "./emonec.html", "./center.html", "./zoo.html", "./domov.html", "./style.css", "./app.js", "./album.js", "./manifest.json", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/apple-touch-icon.png", "./icons/favicon.svg"];

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
      return Promise.all(keys.filter(function (k) { return k !== CACHE_NAME; }).map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (event) {
  if (event.request.method !== "GET") return;
  var url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;
  var isHTML = event.request.mode === "navigate" ||
               (event.request.headers.get("accept") || "").indexOf("text/html") !== -1;
  var fresh = isHTML || /\.(css|js|json)$/i.test(url.pathname);
  var req = fresh ? new Request(event.request.url, { cache: "reload" }) : event.request;
  event.respondWith(
    fetch(req).then(function (response) {
      var copy = response.clone();
      caches.open(CACHE_NAME).then(function (cache) { cache.put(event.request, copy); });
      return response;
    }).catch(function () {
      return caches.match(event.request).then(function (cached) { return cached || caches.match("./index.html"); });
    })
  );
});
