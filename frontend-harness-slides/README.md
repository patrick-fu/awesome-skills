# Frontend Harness Slides

Build HTML slides that an agent can keep changing without quietly breaking
unrelated frames.

Single-file HTML is often enough for a quick first draft. The difficult part is
what happens after the first version: the user asks to change wording, add a
section, tune an animation, swap screenshots, tighten a dense page, or remove a
slide. Without structure and regression checks, one edit can damage another page
and nobody notices until review.

`frontend-harness-slides` solves that problem by starting from a real React/Vite
project guarded by Playwright:

- **Registry**: one array owns scene order, so insertions and removals do not
  cause filename or snapshot churn.
- **Fixed stage**: every scene is authored in a 1920x1080 canvas and scaled as a
  whole, so the layout does not reflow per device.
- **Beat URLs**: every scene state is addressable with `?scene=<id>&beat=<n>`.
- **Auditor**: checks that requested frames render correctly and that visible
  content does not collapse or escape the stage.
- **Visual regression**: freezes animation and compares every scene/beat against
  baselines.
- **PDF export**: captures the same stage geometry the harness checks.

## Quick Start

```bash
cp -r ~/.agents/skills/frontend-harness-slides/assets/starter ./my-deck
cd ./my-deck
npm install
npx playwright install chromium
npm run dev
```

First baseline and full check:

```bash
npm run test:update
npm test
```

## How The Starter Is Organized

```text
starter/
├── src/
│   ├── main.tsx                    # exposes registry, renders SlideDeck
│   ├── SlideDeck.tsx               # URL state, beats, keyboard navigation
│   ├── SlideRegistry.tsx           # scene order and stable ids
│   ├── components/
│   │   ├── SlideStage.tsx          # fixed 1920x1080 stage
│   │   └── SandboxIsolator.tsx     # event isolation for interactive regions
│   ├── scenes/
│   │   ├── CoverScene.tsx
│   │   └── HarnessScene.tsx
│   └── theme/
│       ├── ThemeProvider.tsx
│       └── themes.ts
├── tests/
│   ├── auditor.spec.ts             # structure and layout health
│   └── visual.spec.ts              # frozen visual snapshots
├── harness/freeze.mjs              # shared freeze logic
├── scripts/export-pdf.mjs          # PDF export from the running app
├── playwright.config.ts
└── package.json
```

To add a scene, create a component in `src/scenes/` and register it in
`src/SlideRegistry.tsx` with a stable kebab-case `id`.

## Commands

| Command | Purpose |
|---|---|
| `npm run dev` | Vite dev server for authoring. |
| `npm run build` | Type-check and production build. |
| `npm run preview` | Serve the built `dist/` folder. |
| `npm run auditor` | Run structural/layout audit only. |
| `npm run visual` | Run visual snapshot comparison only. |
| `npm test` | Run the full Playwright harness. |
| `npm run test:update` | Update visual baselines for intentional changes. |
| `npm run export:pdf` | Export a PDF from a running preview server. |

If the default preview port is busy, run tests with a shared `PORT`:

```bash
PORT=4180 npm test
```

## What To Read

- `SKILL.md`: agent-facing workflow and contracts.
- `assets/starter/README.md`: instructions for a copied deck project.
- `references/theming.md`: visual direction and theme tokens.
- `references/content-import.md`: importing existing content.
- `references/asset-handling.md`: images, logos, SVGs, and fonts.
- `references/troubleshooting.md`: common failures and fixes.
- `showcase/README.md`: planned demonstration flow for why the harness matters.

## Current Boundaries

This starter currently supports fullscreen browser presentation through the
normal deck view, keyboard navigation, structural audit, visual snapshots, and
PDF export of each scene's final beat.

It does not currently implement a separate presenter notes view, notes export, or
theme hot-swap UI. Treat those as future runtime work unless the starter code is
extended first.
