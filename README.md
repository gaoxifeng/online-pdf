# online-pdf

**A PDF toolbox that runs 100% in your browser — your file never leaves your device.**

No upload, no server, no account. Open the page, drop a PDF, done. Everything
(merge, OCR, signing…) happens locally in your browser via WebAssembly/JS.

👉 **Live:** https://gaoxifeng.github.io/online-pdf/

## Tools

| Tool | What it does |
|------|--------------|
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

It's a single static `index.html` — no build step.

- **Locally:** open `index.html` in a browser (or `python -m http.server`).
- **GitHub Pages:** push to a repo → Settings → Pages → Branch `main` / root.
- **Anywhere:** drop the file on any static host (Netlify, Cloudflare Pages, S3…).

## Built with

[pdf-lib](https://github.com/Hopding/pdf-lib) (MIT) ·
[pdf.js](https://github.com/mozilla/pdf.js) (Apache-2.0) ·
[tesseract.js](https://github.com/naptha/tesseract.js) (Apache-2.0) ·
[signature_pad](https://github.com/szimek/signature_pad) (MIT) ·
[JSZip](https://github.com/Stuk/jszip) (MIT)

## License

MIT — see [LICENSE](LICENSE).
