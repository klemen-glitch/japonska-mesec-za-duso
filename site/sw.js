/* Izklop starega service workerja (prejšnja različica spletišča je bila v korenu).
   Izbriše stare predpomnilnike in se odjavi; potovanja imajo svoje service workerje v svojih mapah. */
self.addEventListener("install", function () { self.skipWaiting(); });
self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys()
      .then(function (keys) { return Promise.all(keys.map(function (k) { return caches.delete(k); })); })
      .then(function () { return self.registration.unregister(); })
      .then(function () { return self.clients.matchAll({ type: "window" }); })
      .then(function (clients) { clients.forEach(function (c) { try { c.navigate(c.url); } catch (e) {} }); })
  );
});
self.addEventListener("fetch", function () { /* ne predpomni nič */ });
