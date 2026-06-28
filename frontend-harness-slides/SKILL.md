---
name: frontend-harness-slides
description: >-
  Build an HTML slide deck as a real engineering project — a complete,
  maintainable presentation that stays visually consistent and won't silently
  break as it grows or gets edited, a sturdier step up from single-file HTML
  slides. Use when the user wants to create, extend, refactor, or harden HTML
  slides (a talk or pitch deck) into something built to last, or wants slide
  work with automated visual checks and PDF export — not a quick one-off.
---

# Frontend Harness Slides

Build slide decks like production software: a Playwright **harness** guards every frame, a **registry** decouples order from filenames, and an absolute 16:9 **stage** keeps layout identical on any screen. The bundled `assets/starter/` is a runnable project that already wires all of this together — copy it first, then make it yours.

Each section below is a rule plus a pointer to the file that implements it. Read the pointed file when you reach that piece — keep this file lean.

## Core Principles

1. **Harness over eyeballing** — Never trust "looks fine" by eye. The Playwright harness audits structure and compares pixels every run; a change is done only when the harness is green (§II).
2. **Resilience by architecture** — A central **registry** kills re-indexing hell; the **stage** locks a 1920×1080 canvas and scales as a whole, so you never reflow per device.
3. **Anti-slop aesthetics** — Reject generic AI-slop (no Inter, no default purple-on-white gradient). Commit to one bold, narrative-specific look (§III).

## 0. Start from the starter

Don't hand-assemble the project. The repeated engineering — Vite + React + Tailwind, the router/beat-controller, the theme provider, `playwright.config`, the two specs, the PDF exporter, an optional CI — is bundled in `assets/starter/` and already green:

1. Copy `assets/starter/` to the project root.
2. `npm install`, then `npm run dev` to author and `npm test` to run the harness.
3. Replace the two demo scenes in `src/scenes/` with real content, registered through the array (§I.1).

Everything below explains the pieces you'll touch inside that starter.

## I. Architecture

### 1. Registry — one array owns order
Inserting a slide must not rename files or break snapshots ("re-indexing hell"). Decouple order from filenames:
- Name components semantically (`CoverScene.tsx`, not `Scene7.tsx`).
- One central array (`src/SlideRegistry.tsx`) owns order; routing, page numbers, and tests all derive from array position plus each entry's stable `id` (which also names snapshots). Keep `id`s stable once set.
- → `assets/starter/src/SlideRegistry.tsx` — the registry shape, `getSlideNavigation`, and `exposeRegistryForTooling` (publishes a slim list to `window.__SLIDE_REGISTRY__` for the harness and PDF export).

### 2. Stage — absolute 16:9, no reflow
To look identical on ultra-wide, projector, and phone, never use responsive breakpoints to rearrange slide content. Lock content in a virtual 1920×1080 canvas and scale the whole stage to fit (letterbox/pillarbox).
- Contract: the stage frame carries `data-slide-stage` (bounds anchor) plus `data-slide-id` / `data-beat` (so a test can assert the app landed on the right frame). The harness keys on these attributes, never on class chains — they drift.
- → `assets/starter/src/components/SlideStage.tsx`.

### 3. Theming — config + context, picked by eye
Declare each theme as a config and inject it via React Context (slides read tokens, never hardcode color/font). Discover themes visually, not verbally.
- → `references/theming.md` — the `ThemeConfig` shape, the dual-preview (three-pane + live hot-swap), and the preview-authenticity rules. Read it during theme discovery. The provider itself lives in `assets/starter/src/theme/`.
- Fonts → `references/fonts.md` (open-source only, downloaded into `public/fonts/`).

### 4. Sandbox — isolate interactive demos
Embedding an input, terminal, or clickable demo? Stop its key/scroll/click events from bubbling into slide navigation, or typing a space flips the slide.
- → `assets/starter/src/components/SandboxIsolator.tsx`.

## II. The Harness

The harness exists to make every screenshot a **frozen frame**: the same render every run, so a pixel diff means a real regression, not animation jitter.

### 1. Beat controller — state lives in the URL
Bind slide state to query params (`?scene=<id>&beat=<n>`). With `?test=true` the deck locks scene+beat and components jump straight to that beat's final state (no stagger timers, no live keyboard nav). That determinism is what makes a frame freezable, and it makes every frame a shareable deep link.
- → `assets/starter/src/SlideDeck.tsx` parses the query, clamps the beat, syncs the URL on navigation, and emits `data-slide-id` / `data-beat` so the specs can assert the frame actually rendered.

### 2. Freeze — kill continuous motion in test mode
Infinite/looping animations (spinning gears, pulsing gradients) shift by milliseconds and break visual diffs. In test mode, **freeze** them: pause animation play-states, zero transition durations, then wait for the DOM to settle before the shot. Mask truly live regions (canvas, third-party iframes).
- → `assets/starter/harness/freeze.mjs` is the single source of the freeze (the CSS + `waitForAnimationsToSettle`). Both `tests/visual.spec.ts` and `scripts/export-pdf.mjs` import it — change freeze once, here.

### 3. Audit — structure, not just pixels
Alongside snapshots, `assets/starter/tests/auditor.spec.ts` walks every scene/beat and checks, with near-zero false positives:
- **Beat honored** — the rendered `data-slide-id` / `data-beat` match the requested URL, so a snapshot can't silently pass on the wrong frame.
- **No collapse** — an element that should be visible (its own text, or media with a `src`) must not render 0×0. Opt a known-empty node out with `data-allow-empty`.
- **No overflow** — nothing escapes `data-slide-stage`; opt a deliberate bleed out with `data-allow-overflow`.

Element-vs-element collision is deliberately *not* a DOM assertion — real decks layer on purpose, so a generic check only cries wolf. Whether things *look* wrong is owned by the visual baseline (§II.2), not the auditor.

## III. Aesthetics & humanizer

- **Anti-slop** — one committed palette, distinctive type, one strong atmospheric device. No generic dashboard-card look, no Inter, no default purple gradient.
- **Legible type** — prefer large, confident type; tiny text reads as slop and is unreadable on a projector. This is guidance, not a gate — if the user wants small type for a dense handout, honor it.
- **humanizer mode** — when the user asks for humanizer (`speak-like-human: true`), strip corporate hype and AI symmetry; keep on-slide text to keywords/metrics/one direct takeaway, and speaker notes in first-person practitioner voice. → Contrastive examples and rules in `references/humanizer-slides.md`.

## IV. Content Density

Ask once whether the deck is speaker-led or reading-first, then let the answer drive the design:

| Mode | Best for | Behavior |
| :--- | :--- | :--- |
| **Low / speaker-led** | live talks, keynotes | one idea per slide, big type, 1–3 lines, more slides |
| **High / reading-first** | handouts, async review | self-contained slides, grids/tables/annotations, 4–8 points |

When a dense slide would force hard-to-read type or push content past `data-slide-stage`, split it into more slides rather than shrink past legibility — overflow is a hard fail (§II.3), and cramped type undercuts the deck.

## V. Workflow

### Phase 0 — Detect mode (first)
- **New deck** → scaffold from the starter (§0), then Phase 1.
- **Convert** (user has a PPT / markdown / outline) → extract content, confirm the outline, scaffold, then Phase 1.
- **Enhance an existing deck** → the high-frequency case for a multi-session deck. Before editing:
  1. Run the existing harness once to capture a green baseline (`npx playwright test`).
  2. Insert/edit slides through the **registry** (append or reorder the array; never rename files).
  3. Before adding content to a slide, check it against the density guidance (§IV); if it would overflow, split instead.
  4. Re-run the harness. Done only per the Phase 3 criterion, with every snapshot diff intended and re-baselined (`--update-snapshots`).

For any deck under git, keep a root `CONTEXT.md` as the single source of decisions/backlog, and prune it during big restructures so it stays high-density.

### Phase 1 — Discover (ask together)
Ask in one batch: **purpose · audience · length · density** (speaker-led vs reading-first). Then:
- Propose three themes via the dual-preview (`references/theming.md`); let the user pick by eye.
- If the user supplied images/logo/screenshots: judge each (usable? what it shows) and design the outline *around* them (3 screenshots → 3 feature slides, logo → cover/closing). Put assets in `public/`.
- Seed the `SLIDE_REGISTRY` array from the agreed outline.

### Phase 2 — Build
- Author each registry component in `src/scenes/`. Done when every registry entry resolves to a real component (no placeholders).
- Bind each internal state to a `beat`, reachable via `?scene=&beat=` and identical on reload.
- Wrap every interactive widget in `<SandboxIsolator>`; verify key/scroll/click don't leak into navigation.
- Honor `prefers-reduced-motion` for real viewers — gate decorative/continuous motion behind it. (Distinct from test-mode **freeze**, which only stabilizes snapshots.)
- The starter already calls `exposeRegistryForTooling()` in `main.tsx`; keep it so the harness and PDF export can read the deck.

### Phase 3 — Verify & ship
Done only when **all** of these hold:
1. `npm run build` passes (types + production build).
2. `npx playwright test` exits clean.
3. The auditor spec is green — every frame honors its URL, nothing collapses to 0×0, nothing escapes `data-slide-stage`.
4. The visual spec is green for every registry scene at every beat, with any diff intended and re-baselined (`--update-snapshots`).
5. The visual run is not silently skipped — the registry is non-empty (the specs assert this).

Then ship → `references/deploy.md`: Vercel `vercel.json` rewrite for `?scene=&beat=` deep links, plus PDF export via `assets/starter/scripts/export-pdf.mjs`.

## VI. Supporting Files

| File | Read / use when |
| :--- | :--- |
| `assets/starter/` | **start here** — copy this runnable project; it wires registry, stage, beat controller, theme, sandbox, harness, specs, PDF export, and optional CI |
| `assets/starter/src/SlideRegistry.tsx` | wiring the registry / routing |
| `assets/starter/src/SlideDeck.tsx` | the beat controller (URL → frame, test-mode lock) |
| `assets/starter/src/components/SlideStage.tsx` | building the 16:9 stage |
| `assets/starter/harness/freeze.mjs` | the single freeze mechanism |
| `assets/starter/tests/` | the auditor + visual specs |
| `references/theming.md` | theme discovery, dual-preview, preview rules |
| `references/fonts.md` | choosing / installing fonts |
| `references/humanizer-slides.md` | the user asks for humanizer copy |
| `references/deploy.md` | deploying to Vercel or exporting PDF |
