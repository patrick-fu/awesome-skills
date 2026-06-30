# Frontend Harness Slides Starter

This is the runnable deck project copied by the skill. It is intentionally a
small React/Vite app plus a Playwright harness, not a single HTML file.

## First Run

```bash
npm install
npx playwright install chromium
npm run dev
```

Open `http://localhost:5173`.

For the first visual baseline:

```bash
npm run test:update
npm test
```

Commit the generated files under `tests/snapshots/` after reviewing them. Future
test runs compare against those baselines.

## Project Map

```text
src/
├── main.tsx                    # exposes registry, renders SlideDeck
├── SlideDeck.tsx               # scene/beat URL state and navigation
├── SlideRegistry.tsx           # one array owns order and stable ids
├── components/
│   ├── SlideStage.tsx          # fixed 1920x1080 stage
│   └── SandboxIsolator.tsx     # isolates embedded interactive widgets
├── scenes/
│   ├── CoverScene.tsx
│   └── HarnessScene.tsx
└── theme/
    ├── ThemeProvider.tsx
    └── themes.ts

tests/
├── auditor.spec.ts             # structural and overflow audit
└── visual.spec.ts              # frozen visual snapshots

harness/freeze.mjs              # shared animation/media freeze logic
scripts/export-pdf.mjs          # PDF export from the running app
```

## Add A Scene

1. Create `src/scenes/MyScene.tsx`.
2. Export a component that accepts `SceneProps`.
3. Import it in `src/SlideRegistry.tsx`.
4. Add an entry with a stable kebab-case `id`, a human `title`, the component,
   and `totalBeats`.

Example registry entry:

```ts
{ id: 'product-demo', title: 'Product demo', component: ProductDemoScene, totalBeats: 2 }
```

`totalBeats` is the last beat index. A scene with `totalBeats: 2` has beats `0`,
`1`, and `2`.

## Navigation

| Key | Action |
|---|---|
| `ArrowRight`, `Space`, `PageDown`, `Enter`, `j`, `ArrowDown` | Next beat |
| `ArrowLeft`, `PageUp`, `Backspace`, `k`, `ArrowUp` | Previous beat |
| `Home` | First scene, beat 0 |
| `End` | Last scene, final beat |
| `1` to `9`, `0` | Jump to scenes 1 to 10 |
| `f` / `F` / `F11` | Toggle browser fullscreen |

Editable fields are allowed to keep their keyboard input. Wrap custom editors,
playgrounds, or embedded interactive regions in `SandboxIsolator`.

## Commands

| Command | Purpose |
|---|---|
| `npm run dev` | Author locally with Vite. |
| `npm run build` | Type-check and production build. |
| `npm run preview` | Serve `dist/` locally, default `http://localhost:4173`. |
| `npm run auditor` | Run `auditor.spec.ts`. |
| `npm run visual` | Run `visual.spec.ts`. |
| `npm test` | Run all Playwright tests. |
| `npm run test:update` | Update all snapshots for intentional visual changes. |
| `npm run test:visual:update` | Update visual snapshots only. |
| `npm run test:ci` | CI-oriented Playwright run. |
| `npm run export:pdf` | Export PDF from a running preview server. |

If the preview port is busy, pass a shared `PORT`:

```bash
PORT=4180 npm test
PORT=4180 npm run export:pdf -- --base http://localhost:4180
```

## Export PDF

The exporter reads `window.__SLIDE_REGISTRY__` from the running app and captures
each scene at its final beat.

```bash
npm run build
npm run preview
npm run export:pdf -- --base http://localhost:4173 --out deck.pdf
```

Use `--compact` for a smaller 1280x720 export.

## CI

`.github/workflows/harness.yml` is included as a ready GitHub Actions workflow.
It installs dependencies, installs Playwright Chromium, builds the app, runs the
harness, and uploads failure artifacts.

## Important Contracts

- Keep `exposeRegistryForTooling()` in `src/main.tsx`.
- Keep all slide content inside `[data-slide-stage]`.
- Do not use responsive breakpoints inside scene content.
- Keep scene `id` values stable after baselines are created.
- Update snapshots only when the visual change is intentional.
