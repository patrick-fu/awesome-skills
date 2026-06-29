# Deploy & export

Ship the deck as a live URL, and export a static PDF to hand off.

## Vercel — query-routed SPA

The deck routes on `?scene=<id>&beat=<n>`. On static hosting a deep link or a manual refresh would 404, so add a catch-all rewrite to `index.html` — but **do not rewrite known static-asset paths**, otherwise a broken `/assets/font.ttf` resolves to HTML and the browser throws an OTS parsing error. Use the starter's `vercel.json` verbatim:

```json
{
  "cleanUrls": true,
  "trailingSlash": false,
  "headers": [
    { "source": "/fonts/(.*)", "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }] },
    { "source": "/assets/(.*)", "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }] }
  ],
  "rewrites": [
    { "source": "/((?!assets|fonts|_next|favicon\\.ico|sitemap\\.xml).*)", "destination": "/index.html" }
  ]
}
```

Put this in `vercel.json` at the project root (the starter already includes it), then `npx vercel --prod`. The free tier is plenty; redeploying the same project reuses the same URL (no new link to share).

## PDF export

`scripts/export-pdf.mjs` walks the deck and stitches one page per slide. It reads `window.__SLIDE_REGISTRY__` from the running app (single source — see `src/SlideRegistry.tsx`), so it covers every slide automatically — no second list to keep in sync.

1. Build and serve the deck: `npm run build && npm run preview` (default `http://localhost:4173`).
2. `npm run export:pdf -- --base http://localhost:4173 --out deck.pdf` (or `node scripts/export-pdf.mjs ...`).
   - `--compact` renders at 1280×720 instead of 1920×1080 (~50–70% smaller file).

It captures each slide's **final beat** with `?test=true` (a frozen frame), so the PDF matches what the harness verifies. Animations collapse to their final static state — expected for a PDF.

### Gotchas
- **Server must be up first.** The script visits the live app to read the registry. If the preview server isn't reachable it exits early with "Could not reach the preview server at <url>"; if the server is up but the registry is missing (forgot `exposeRegistryForTooling()`), it exits with "no window.__SLIDE_REGISTRY__".
- **Keep assets under `public/`.** Relative-path images/fonts render fine; absolute filesystem paths won't.
- **Big decks → big PDFs.** Each slide is a full 1920×1080 PNG. If the file is too large, re-run with `--compact`.
- **PDF clip matches the visual baseline.** Export and `tests/visual.spec.ts` both crop to `[data-slide-stage]`'s bounding box — letterbox chrome never appears, and the two outputs share a geometric origin.

## CJK font size (H-10 correction)

If the deck uses a heavy CJK font like `LXGW WenKai Lite` (20 MB+ TTF), **format conversion alone is not enough** to get it under budget.

> H-10: `ttf2woff2` only does **format conversion**, it does **not subset glyphs**. For a 20 MB
> CJK TTF, `npx ttf2woff2 < in.ttf > out.woff2` typically produces a **15–18 MB WOFF2**
> (–5% to –15%). To reach the < 1 MB target you **must use a subsetter**:
>
> - `glyphhanger --formats=woff2 --LATIN --subset=src/fonts/NotoSansSC.ttf` — scans the built
>   HTML and drops any glyph not actually rendered on a slide.
> - `pyftsubset src/fonts/NotoSansSC.ttf --text-file=used-chars.txt --flavor=woff2` — subset
>   against an explicit allow-list (great when content is script-generated).

Recommended CI step order:

```bash
# 1. (optional) discover actually-used glyphs from the built deck
glyphhanger ./dist/index.html --subset=./public/fonts/LXGWWenKaiLite-Regular.ttf --formats=woff2 --LATIN
# 2. or subset against a curated allow-list (deterministic, no build order dependency):
pyftsubset public/fonts/LXGWWenKaiLite-Regular.ttf   --text-file=content/used-chars.txt   --flavor=woff2   --output-file=public/fonts/LXGWWenKaiLite-Regular.subset.woff2
```

Run subsetting before `npm run build` in GitHub Actions, alongside `tsc` / `eslint` and the Playwright harness (Chromium only — see `tests/visual.spec.ts`). The starter ships `.github/workflows/harness.yml.example` as a starting point (it already includes npm + Playwright caches and an always-run artifact upload step).

## CI (optional)

The starter's `.github/workflows/harness.yml.example` — when renamed to `harness.yml` — installs Node 20.11 (matching `engines.node`), caches `~/.npm` and the Playwright Chromium binary (~300 MB), builds the deck, runs the Playwright harness, and uploads `playwright-report/`, `test-results/`, and the visual snapshot directory as a 14-day artifact even on failure.
