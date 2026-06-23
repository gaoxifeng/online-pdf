/* online-pdf — service worker
 * Makes the app installable and fully usable offline, so a PDF you double-click
 * (via the Windows file association) opens even with no network. No document
 * data is ever cached or transmitted — only the app shell and library code.
 *
 * Bump CACHE_VERSION whenever index.html / sw.js / icons change so clients
 * pick up the new build.
 */
"use strict";

const CACHE_VERSION = "v1";
const APP_CACHE = "onlinepdf-app-" + CACHE_VERSION;
const RUNTIME_CACHE = "onlinepdf-runtime-" + CACHE_VERSION;

// Same-origin app shell — must succeed for install to complete.
const APP_SHELL = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/maskable-512.png",
  "./icons/icon-256.png",
  "./icons/apple-touch-icon.png",
  "./icons/favicon-32.png",
  "./icons/favicon.ico",
];

// CDN libraries — precached best-effort so the tools work offline. A CDN hiccup
// here must NOT fail the install; the page loads these with crossorigin, so the
// fetch handler also caches them (as CORS) on first online use as a backstop.
const CDN_LIBS = [
  "https://cdn.jsdelivr.net/npm/pdf-lib@1.17.1/dist/pdf-lib.min.js",
  "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js",
  "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js",
  "https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js",
  "https://cdn.jsdelivr.net/npm/signature_pad@4.1.7/dist/signature_pad.umd.min.js",
  "https://cdn.jsdelivr.net/npm/tesseract.js@5.1.1/dist/tesseract.min.js",
];

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(APP_CACHE);
    await cache.addAll(APP_SHELL);                       // required
    await Promise.allSettled(                            // best-effort
      CDN_LIBS.map(async (url) => {
        try {
          const res = await fetch(url, { mode: "cors", cache: "no-cache" });
          if (res && res.ok) await cache.put(url, res.clone());
        } catch (e) { /* offline-or-blocked during install: fine */ }
      })
    );
    // No skipWaiting(): an UPDATED worker waits until every tab closes, so we
    // never swap the worker (and purge caches) under an in-progress OCR/merge.
    // The very first install still activates immediately (nothing to replace).
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(
      keys.filter((k) => k !== APP_CACHE && k !== RUNTIME_CACHE).map((k) => caches.delete(k))
    );
    await self.clients.claim();
  })());
});

// Allow the page to trigger an immediate update.
self.addEventListener("message", (event) => {
  if (event.data === "SKIP_WAITING") self.skipWaiting();
});

function cacheable(res) {
  return res && res.ok && (res.type === "basic" || res.type === "cors");
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;                      // never cache uploads/posts

  // App navigations: network-first (so updates land), fall back to cached shell.
  // On success, refresh the cached shell so the offline copy self-heals even if
  // CACHE_VERSION wasn't bumped.
  if (req.mode === "navigate") {
    event.respondWith((async () => {
      try {
        const res = await fetch(req);
        if (res && res.ok && res.type === "basic") {
          const copy = res.clone();
          caches.open(APP_CACHE)
            .then((c) => Promise.all([c.put("./", copy.clone()), c.put("./index.html", copy)]))
            .catch(() => {});
        }
        return res;
      } catch (e) {
        const cache = await caches.open(APP_CACHE);
        return (await cache.match("./index.html")) ||
               (await cache.match("./")) ||
               Response.error();
      }
    })());
    return;
  }

  // Everything else (scripts, icons, wasm, OCR models): stale-while-revalidate.
  event.respondWith((async () => {
    const cached = await caches.match(req);
    const fetching = fetch(req).then((res) => {
      if (cacheable(res)) {
        const copy = res.clone();
        caches.open(RUNTIME_CACHE).then((c) => c.put(req, copy)).catch(() => {});
      }
      return res;
    }).catch(() => null);
    return cached || (await fetching) || Response.error();
  })());
});
