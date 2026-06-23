# online-pdf

**A PDF toolbox that runs 100% in your browser — your file never leaves your device.**

No upload, no server, no account. Open the page, drop a PDF, done. Everything
(read, merge, OCR, signing…) happens locally in your browser via WebAssembly/JS.

👉 **Live:** https://gaoxifeng.github.io/online-pdf/

## Install as a Windows app (open PDFs by double-clicking)

online-pdf is a **PWA**, so you can install it like a native app and have it open
`.pdf` files straight from Explorer. Works in **Edge** or **Chrome** on Windows 10/11
(Chromium desktop only — not Firefox/Safari). It still runs 100% locally and works
offline; installing doesn't change the privacy model.

**1 · Install**

- **Edge:** open the [live site](https://gaoxifeng.github.io/online-pdf/) → click the
  **install icon** (a monitor with a down-arrow) at the right of the address bar, or
  **··· menu → Apps → Install this site as an app** → **Install**.
- **Chrome:** open the [live site](https://gaoxifeng.github.io/online-pdf/) → click the
  **install icon** in the address bar, or **⋮ menu → Cast, save, and share → Install
  page as app…** → **Install**.

Installing registers online-pdf as an **available** handler for `.pdf` (it now appears
under right-click **Open with**). It does **not** auto-become your default PDF app —
Windows keeps your current one until you change it (step 3).

**2 · Open a PDF with it**

Right-click any `.pdf` → **Open with → online-pdf**. The **first** time, Edge/Chrome show a
one-time prompt (“Open” / “Allow”) — accept it. The PDF opens straight in the reader.

**3 · (Optional) Make it the default for `.pdf`**

Right-click a `.pdf` → **Open with → Choose another app** → pick **online-pdf** → tick
**Always use this app to open .pdf files** → **OK**.
*(Or:* **Settings → Apps → Default apps**, find **online-pdf** or the **.pdf** type, set it.*)*

**Good to know**

- Opened PDFs land in the **View / Read** tool as tabs — drag in or **📂 Open** more, then
  switch tools (Merge, OCR, Sign…) as usual.
- Works **offline** after the first load — the app shell and libraries are cached by a
  service worker (`sw.js`). Your documents are never cached or uploaded.
- **Uninstalling** the app removes the `.pdf` association; Windows reverts to your previous
  default.
- Install from **one** browser only — installing in both Edge and Chrome creates two
  separate “online-pdf” entries in *Open with*.

## Tools

| Tool | What it does |
|------|--------------|
| **View / Read** | Read PDFs — **multiple open as tabs**, continuous scroll, zoom, jump to page, **find (`Ctrl+F`)**, select & copy text, full-screen (←/→ pages, +/− zoom, `f` full-screen) |
| **Merge** | Combine several PDFs into one |
| **Split** | Extract a page range, or split into single pages (`.zip`) |
| **Rotate** | Rotate selected pages 90 / 180 / 270° |
| **Watermark** | Diagonal text watermark on every page |
| **Page numbers** | Add page numbers (position + start value) |
| **Compress** | Shrink by rasterising pages to JPEG |
| **OCR** | Recognise text in a scanned PDF/image (English / 中文) |
| **Sign** | Draw or upload a signature, click on the page to place it |

## Why browser-only?

Most online PDF tools upload your file to their servers. For anything
confidential — contracts, IDs, medical records — that's a non-starter. Here the
file is read into memory in your browser and processed there; **nothing is ever
sent anywhere.** You can confirm it: open DevTools → Network, run any tool, and
you'll see zero upload requests for your document.

> Library code (pdf-lib, pdf.js, tesseract.js) loads from a public CDN like any
> website's JavaScript; the first OCR run downloads a language model (~10 MB).
> Your **document data** is never transmitted.

## Run / host it yourself

Static files — `index.html` plus the PWA bits (`manifest.webmanifest`, `sw.js`,
`icons/`) — no build step.

- **Locally:** serve over http (`python -m http.server`) and open
  `http://localhost:8000/`. Opening `index.html` as `file://` works for the tools but
  disables install/offline (a service worker needs http(s)).
- **GitHub Pages:** push to a repo → Settings → Pages → Branch `main` / root.
- **Anywhere:** drop the files on any static host (Netlify, Cloudflare Pages, S3…) — must
  be **HTTPS** for install + file association.

> Edited the app shell, `sw.js`, or icons? Bump `CACHE_VERSION` in `sw.js` so installed
> clients pick up the new build.

## Built with

[pdf-lib](https://github.com/Hopding/pdf-lib) (MIT) ·
[pdf.js](https://github.com/mozilla/pdf.js) (Apache-2.0) ·
[tesseract.js](https://github.com/naptha/tesseract.js) (Apache-2.0) ·
[signature_pad](https://github.com/szimek/signature_pad) (MIT) ·
[JSZip](https://github.com/Stuk/jszip) (MIT)

## License

MIT — see [LICENSE](LICENSE).
