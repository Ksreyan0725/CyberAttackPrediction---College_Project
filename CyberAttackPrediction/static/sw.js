/**
 * CyberShield Service Worker v1.0
 * Handles offline fallback for mission-critical cyber defense data.
 */

const CACHE_NAME = 'cybershield-offline-cache-v1';
const OFFLINE_URL = '/offline.html';

// Assets that are necessary to render the offline page
const ASSETS_TO_CACHE = [
    OFFLINE_URL,
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Outfit:wght@700&display=swap'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[Service Worker] Caching offline fallback assets');
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
    // Force the waiting service worker to become active
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[Service Worker] Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    // Take control of all open pages immediately
    self.clients.claim();
});

self.addEventListener('fetch', (event) => {
    // We only want to handle navigation requests (GET for HTML documents)
    if (event.request.mode === 'navigate' || 
        (event.request.method === 'GET' && event.request.headers.get('accept').includes('text/html'))) {
        
        event.respondWith(
            fetch(event.request).catch(error => {
                // The fetch failed (server is off or network lost)
                console.log('[Service Worker] Fetch failed; returning offline page.', error);
                return caches.match(OFFLINE_URL);
            })
        );
    }
});
