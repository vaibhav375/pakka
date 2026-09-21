/* Enough of a service worker to make the app installable, which is what puts
   Pakka in the Android share sheet next to every other app.

   Network first, cache second. The rules are the whole product and a stale
   copy of them is worse than a slow one, so a working network always wins and
   the cache is there for the times there is none. */
/* The cache name carries the build. It used to be a fixed string, which meant
   install() ran once and never again, so anyone who had installed the app
   could stay pinned to the files from whatever day they installed it. Changing
   the name on every deploy is what makes a new version take. */
const SHELL = 'pakka-f2cf9cf';
const FILES = ['./', './index.html', './styles.css', './app.js',
               './rules.generated.js', './config.js', './scene.js',
               './manifest.webmanifest', './icon-192.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(SHELL).then((c) => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys()
    .then((keys) => Promise.all(keys.filter((k) => k !== SHELL).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request)
      .then((res) => {
        const copy = res.clone();
        caches.open(SHELL).then((c) => c.put(e.request, copy)).catch(() => {});
        return res;
      })
      .catch(() => caches.match(e.request).then((hit) => hit || caches.match('./index.html')))
  );
});
