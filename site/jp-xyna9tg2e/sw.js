/* Service worker potovanja: najprej splet (sveže), sicer predpomnilnik. */
var CACHE_NAME = "japonska-20";
var PAGES = ["./", "./index.html", "./nasveti.html", "./nacrt.html", "./priprave.html", "./dozivetja.html", "./nalozi.html", "./izziv.html", "./nujno.html", "./kako.html", "./prevajalec.html", "./kviz.html", "./lov.html", "./knjiga.html", "./stroski.html", "./tokio.html", "./chichibu.html", "./kawaguchiko.html", "./minobusan.html", "./izu.html", "./kumano.html", "./koyasan.html", "./iya.html", "./ine.html", "./nara.html", "./kyoto.html", "./osaka.html", "./hiroshima.html", "./style.css", "./app.js", "./album.js", "./fun.js", "./money.js", "./knjiga.js", "./manifest.json", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/apple-touch-icon.png", "./icons/favicon.svg", "./prevajalec.js"];

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
