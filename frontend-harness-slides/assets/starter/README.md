# Frontend Harness Slides Starter

This is the runnable deck project copied by the skill. It is intentionally a
small React/Vite app plus a Playwright harness, not a single HTML file.

## First Run

```bash
npm install
npx playwright install chromium
npm run doctor
npm run dev
```

Open `http://localhost:5173`.

For the first visual baseline:

```bash
npm run visual:update
npm run test:full
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

scripts/
└── doctor.mjs                   # setup preflight
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
| `npm run doctor` | Lightweight preflight: Node, Chromium, port, Playwright loader, git warnings. |
| `npm run build` | Type-check and production build. |
| `npm run preview` | Serve `dist/` locally, default `http://localhost:4173`. |
| `npm run auditor` | Run `auditor.spec.ts`. |
| `npm run visual` | Run `visual.spec.ts`. |
| `npm test` | Fast gate: build plus auditor, no visual screenshots. |
| `npm run test:full` | Full gate: build plus all Playwright tests, including visual snapshots. |
| `npm run visual:update` | Update visual snapshots for intentional visual changes. |

If the preview port is busy, pass a shared `PORT`:

```bash
PORT=4180 npm test
```

## Test Tiers

- **Preflight**: `npm run doctor` after scaffolding or after moving the project.
  It reports environment errors and git tracking warnings without installing
  anything.
- **Fast iteration**: `npm test` after ordinary scene edits. It builds and runs
  the auditor, but does not spend time on screenshot comparison.
- **Visual check**: `npm run visual` after visual, animation, font, theme, or
  shared component changes.
- **Full gate**: `npm run test:full` before delivery, before rebasing visual
  snapshots, or whenever the impact range is unclear.

## Optional PDF Handoff

The starter does not bundle a PDF exporter. If the user explicitly needs a PDF,
handle it as a project-specific handoff after `npm run test:full` passes. Use the
current deck shape to choose browser print, a temporary Playwright capture script,
or a hosted URL plus manual export, then inspect the output before delivery.

## CI

`.github/workflows/harness.yml` is included as a ready GitHub Actions workflow.
It installs dependencies, installs Playwright Chromium, builds the app, runs the
harness, and uploads failure artifacts.

## Important Contracts

- Keep `exposeRegistryForTooling()` in `src/main.tsx`.
- Keep all slide content inside `[data-slide-stage]`.
- Do not use responsive breakpoints inside scene content.
- Keep scene `id` values stable after baselines are created.
- Run `npm run test:full` before delivery.
- Update snapshots only when the visual change is intentional.
