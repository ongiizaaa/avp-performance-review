// AVP Performance Review service worker. Version __VERSION__
// Pages: network first, so a new Netlify deploy shows up on the next open; cached copy when offline.
// Versioned libraries and fonts: cache first.
const CACHE = "avp-pr-__VERSION__";
const SHELL = ["./", "./index.html", "./manifest.webmanifest", "./lib/xlsx-0.18.5.full.min.js", "./lib/jszip-3.10.1.min.js",
  "./icons/icon-192.png", "./icons/icon-512.png", "./icons/favicon-32.png"];
self.addEventListener("install", (e) => { e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL))); self.skipWaiting(); });
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
const put = (req, res) => { if (res && (res.ok || res.type === "opaque")) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); } return res; };
self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  const cacheFirst = url.pathname.includes("/lib/") || /fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);
  if (cacheFirst) { e.respondWith(caches.match(req).then((hit) => hit || fetch(req).then((res) => put(req, res)))); return; }
  if (url.origin !== self.location.origin) return;
  e.respondWith(fetch(req).then((res) => put(req, res)).catch(() => caches.match(req).then((hit) => hit || caches.match("./index.html"))));
});
