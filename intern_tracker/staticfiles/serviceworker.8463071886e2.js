const CACHE_NAME = 'internship-tracker-cache-v1';
const urlsToCache = [
  '/home/',
  '/admin/',
  '/intern/',
  '/static/favicon.ico',
  '/static/manifest.json',
  '/static/css/base_site.css',
  '/static/css/admin_site.css',
  '/static/css/intern_ui.css',
  '/static/js/base_site.js',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  '/static/screenshots/screenshot1.png',
  '/static/screenshots/screenshot2.png',
  '/static/screenshots/wide-screenshot.png',
  '/static/screenshots/narrow-screenshot.png',
  // Add other static files you want to cache
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});

self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (!cacheWhitelist.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

