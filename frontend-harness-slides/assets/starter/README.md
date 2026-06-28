# Frontend Harness Slides — starter

A minimal, runnable React + Vite slide deck wired to the Playwright harness. Copy this folder to start a deck, then:

```bash
npm install
npm run dev          # author at http://localhost:5173
npm run build        # type-check + production build
npm test             # run the harness (auditor + visual) against the preview build
```

## How it fits together

- `src/SlideRegistry.tsx` — one array owns slide order; each entry's `id` is its route and its snapshot name.
- `src/SlideDeck.tsx` — the beat controller. State lives in the URL: `?scene=<id>&beat=<n>`; `&test=true` locks the frame for the harness.
- `src/components/SlideStage.tsx` — the absolute 16:9 stage. Carries `data-slide-stage` / `data-slide-id` / `data-beat` for the harness.
- `src/theme/` — `ThemeProvider` maps tokens to CSS variables; `themes.ts` holds the look.
- `tests/` — `auditor.spec.ts` (structure) and `visual.spec.ts` (pixels), both reading the live registry.
- `harness/freeze.mjs` — the single freeze mechanism, shared by the visual spec and the PDF export.

## First run

`auditor.spec.ts` passes immediately. `visual.spec.ts` needs a baseline on first run:

```bash
npm run test:update   # seed snapshots, then commit tests/**/__screenshots__ (the *-snapshots dirs)
```

After that, `npm test` is green; a failing visual diff means a real, reviewable change — re-baseline intended diffs with `npm run test:update`.

## Port & reproducibility

- The harness serves the production preview on **4173**. If that port is busy (e.g. another Vite app), shift everything with `PORT=4180 npm test` — `vite preview` and the Playwright specs read the same `PORT`. A busy port fails fast with a clear "Port is in use" error rather than silently testing the wrong app.
- `package-lock.json` is committed so installs are reproducible; CI uses `npm ci`.

## Export & deploy

- PDF: `npm run build && npm run preview`, then in another shell `npm run export:pdf` (add `--compact` for a smaller file).
- Vercel: `vercel.json` is included for query-routed deep links — `npx vercel --prod`.

See the parent skill's `references/` for theming, fonts, humanizer copy, and deploy details.
