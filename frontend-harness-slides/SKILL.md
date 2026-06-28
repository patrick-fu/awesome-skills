---
name: frontend-harness-slides
description: Build a presentation as a harness-guarded engineering project — a complete, maintainable slide deck that stays visually consistent and won't silently break as it grows or gets edited, a step up from single-file HTML slides. Use when the user wants to create, extend, or refactor HTML slides into something built to last rather than a quick one-off.
---

# Frontend Harness Slides

Build React slide decks like production software: a Playwright **harness** guards every frame, a **registry** decouples order from filenames, and an absolute 16:9 **stage** keeps layout identical on any screen.

Each section below is a rule plus a pointer to copyable code or detail. Read the pointed file when you reach that piece — keep this file lean.

## Core Principles

1. **Harness over assertions** — Never trust "looks fine" by eye. The Playwright harness audits structure and compares pixels every run; a change is done only when the harness is green (§II).
2. **Resilience by architecture** — A central **registry** kills re-indexing hell; the **stage** locks a 1920×1080 canvas and scales as a whole, so you never reflow per device.
3. **Anti-slop aesthetics** — Reject generic AI-slop (no Inter, no default purple-on-white gradient). Commit to one bold, narrative-specific look (§III).

## I. Architecture

### 1. Registry — one array owns order
Inserting a slide must not rename files or break snapshots ("re-indexing hell"). Decouple order from filenames:
- Name components semantically (`CoverSlide.tsx`, not `Scene7.tsx`).
- One central `SlideRegistry.ts` array owns order; routing, page numbers, and tests all derive from array position plus each entry's stable `id` (which also names snapshots).
- → Copy `references/slide-registry.ts.example` — the single source for the registry shape and a `getSlideNavigation` helper. Keep `id`s stable once set; they are snapshot filenames.

### 2. Stage — absolute 16:9, no reflow
To look identical on ultra-wide, projector, and phone, never use responsive breakpoints to rearrange slide content. Lock content in a virtual 1920×1080 canvas and scale the whole stage to fit (letterbox/pillarbox).
- Contract: the stage frame exposes a `data-slide-stage` attribute; the harness uses it as the stable anchor for stage bounds. Don't make the harness hunt class chains — they drift.
- → Copy `references/SlideStage.tsx.example`.

### 3. Theming — config + context, picked by eye
Declare each theme as a config and inject it via React Context (slides read tokens, never hardcode color/font). Discover themes visually, not verbally.
- → `references/theming.md` — the `ThemeConfig` shape, the dual-preview (three-pane + live hot-swap), and the preview-authenticity rules. Read it during theme discovery.
- Fonts → `references/fonts.md` (open-source only, downloaded into `public/fonts/`).

### 4. Sandbox — isolate interactive demos
Embedding an input, terminal, or clickable demo? Stop its key/scroll/click events from bubbling into slide navigation, or typing a space flips the slide.
- → Copy `references/SandboxIsolator.tsx.example`.

## II. The Harness

The harness exists to make every screenshot a **frozen frame**: the same render every run, so a pixel diff means a real regression, not animation jitter.

### 1. Beat controller — state lives in the URL
Bind slide state to query params (`?scene=<id>&beat=<n>`). With `?test=true` the router locks scene+beat and components jump straight to that beat's final state (no stagger timers). That determinism is what makes a frame freezable.

### 2. Freeze — kill continuous motion in test mode
Infinite/looping animations (spinning gears, pulsing gradients) shift by milliseconds and break visual diffs. In test mode, **freeze** them: pause animation play-states, zero transition durations, then wait for the DOM to settle before the shot. Mask truly live regions (canvas, third-party iframes).
- The freeze CSS and the `waitForAnimationsToSettle` poller live in `assets/tests/visual.spec.ts.template` — the single source for the freeze mechanism. Copy it; don't restate it.

### 3. Audit — structure, not just pixels
Alongside snapshots, run the DOM audit in `assets/tests/auditor.spec.ts.template`:
- **Font floor** — fail if visible copy renders below **16px** at 1920×1080. Tiny text is an anti-slop tell.
- **Overflow / overlap** — nothing escapes `data-slide-stage`; adjacent blocks don't collide. Opt a deliberate bleed out with `data-allow-overflow`.

## III. Aesthetics & humanizer

- **Anti-slop** — one committed palette, distinctive type, one strong atmospheric device. No generic dashboard-card look, no Inter, no default purple gradient. The 16px font floor (§II.3) enforces part of this — tiny text reads as slop.
- **humanizer mode** — when the user asks for humanizer (`speak-like-human: true`), strip corporate hype and AI symmetry; keep on-slide text to keywords/metrics/one direct takeaway, and speaker notes in first-person practitioner voice. → Contrastive examples and rules in `references/humanizer-slides.md`.

## IV. Content Density

Ask once whether the deck is speaker-led or reading-first, then let the answer drive the design:

| Mode | Best for | Behavior |
| :--- | :--- | :--- |
| **Low / speaker-led** | live talks, keynotes | one idea per slide, big type, 1–3 lines, more slides |
| **High / reading-first** | handouts, async review | self-contained slides, grids/tables/annotations, 4–8 points |

The floor wins: if a high-density slide would push text under 16px or overflow the stage, split it into more slides — never shrink past legibility.

## V. Workflow

### Phase 0 — Detect mode (first)
- **New deck** → Phase 1.
- **Convert** (user has a PPT / markdown / outline) → extract content, confirm the outline, then Phase 1.
- **Enhance an existing deck** → the high-frequency case for a multi-session deck. Before editing:
  1. Run the existing harness once to capture a green baseline (`npx playwright test`).
  2. Insert/edit slides through the **registry** (append or reorder the array; never rename files).
  3. Before adding content to a slide, check it against the density floor (§IV); if it would overflow, split instead.
  4. Re-run the harness. Done only when audit + visual specs pass and every snapshot diff is intended and re-baselined (`--update-snapshots`).

For any deck under git, keep a root `CONTEXT.md` as the single source of decisions/backlog, and prune it during big restructures so it stays high-density.

### Phase 1 — Discover (ask together)
Ask in one batch: **purpose · audience · length · density** (speaker-led vs reading-first). Then:
- Propose three themes via the dual-preview (`references/theming.md`); let the user pick by eye.
- If the user supplied images/logo/screenshots: judge each (usable? what it shows) and design the outline *around* them (3 screenshots → 3 feature slides, logo → cover/closing). Put assets in `public/`.
- Seed the `SlideRegistry.ts` array from the agreed outline.

### Phase 2 — Build
- Author each registry component in `src/scenes/`. Done when every registry entry resolves to a real component (no placeholders).
- Bind each internal state to a `beat`, reachable via `?scene=&beat=` and identical on reload.
- Wrap every interactive widget in `<SandboxIsolator>`; verify key/scroll/click don't leak into navigation.
- Honor `prefers-reduced-motion` for real viewers — gate decorative/continuous motion behind it. (Distinct from test-mode **freeze**, which only stabilizes snapshots.)
- Expose a slim registry for tooling: `window.__SLIDE_REGISTRY__ = SLIDE_REGISTRY.map(s => ({ id: s.id, totalBeats: s.totalBeats }))` (the PDF export reads it).

### Phase 3 — Verify & ship
- Done when the auditor spec is green (no <16px copy, nothing escapes `data-slide-stage`, no zero-size visible element) **and** the visual spec is green for every registry slide at every beat, with any diff intended and re-baselined.
- Commit and push to trigger CI (it compiles the LXGW WenKai web font with `ttf2woff2` on the fly).
- Ship → `references/deploy.md`: Vercel `vercel.json` rewrite for `?scene=&beat=` deep links, plus PDF export via `assets/scripts/export-pdf.mjs`.

## VI. Supporting Files

| File | Read when |
| :--- | :--- |
| `references/slide-registry.ts.example` | wiring the registry / routing |
| `references/SlideStage.tsx.example` | building the 16:9 stage |
| `references/SandboxIsolator.tsx.example` | embedding an interactive demo |
| `references/theming.md` | theme discovery, dual-preview, preview rules |
| `references/fonts.md` | choosing / installing fonts |
| `references/humanizer-slides.md` | the user asks for humanizer copy |
| `references/deploy.md` | deploying to Vercel or exporting PDF |
| `assets/tests/visual.spec.ts.template` | the freeze + pixel-regression suite |
| `assets/tests/auditor.spec.ts.template` | the font-floor + overflow audit |
| `assets/scripts/export-pdf.mjs` | exporting the deck to PDF |
