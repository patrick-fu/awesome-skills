# Deploy & export

Ship the deck as a live URL, and export a static PDF to hand off.

## Vercel — query-routed SPA

The deck routes on `?scene=<id>&beat=<n>`. On static hosting a deep link or a manual refresh would 404, so add a catch-all rewrite to `index.html`:

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
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
- **Server must be up first.** The script visits the live app to read the registry; start the preview server before running it, or it exits with "No window.__SLIDE_REGISTRY__".
- **Keep assets under `public/`.** Relative-path images/fonts render fine; absolute filesystem paths won't.
- **Big decks → big PDFs.** Each slide is a full 1920×1080 PNG. If the file is too large, re-run with `--compact`.

## CI font compilation (optional)

If the deck uses a heavy CJK font like `LXGW WenKai Lite`, don't commit the big binary — compile a `woff2` on the fly in CI:

```bash
npx ttf2woff2 < public/fonts/LXGWWenKaiLite-Regular.ttf > public/fonts/LXGWWenKaiLite-Regular.woff2
```

Run it as a step before build in GitHub Actions, alongside `tsc` / `eslint` and the Playwright harness (Chromium only — see `tests/visual.spec.ts`). The starter ships `.github/workflows/harness.yml.example` as a starting point.
