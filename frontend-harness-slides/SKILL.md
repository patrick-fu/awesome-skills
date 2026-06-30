---
name: frontend-harness-slides
description: >-
  Build iteration-safe HTML slide decks with a React/Vite starter and a
  Playwright harness. Use when the user wants slides that an agent can keep
  changing: edit copy, adjust layout, add or remove scenes, tune animation, and
  verify that unrelated frames did not silently break. Best for non-trivial
  decks, repeated user feedback, animation states, visual regression checks, or
  team review. Avoid for tiny one-shot decks where a single static HTML file is
  enough.
version: 1.1.0
updated: 2026-06-30
---

# Frontend Harness Slides

Build HTML slides that survive iteration. A first draft is rarely the final deck:
users ask for wording changes, layout tweaks, animation timing, added sections,
removed slides, and visual polish. A single HTML file can be fast, but repeated
agent edits can quietly break another slide. This skill uses a real project
starter plus a Playwright harness so every frame can be audited before delivery.

## Core Promise

1. **Change freely, verify mechanically**: every scene and beat has a stable URL,
   can be frozen, and can be checked by Playwright.
2. **Structure prevents collateral damage**: a central registry owns order,
   semantic scene files hold content, and the 1920x1080 stage never reflows.
3. **The user should not be surprised**: align on intent before scaffolding, then
   keep changes reviewable through snapshots and audits.

## Brief Intake

Before scaffolding, do a short natural-language brief intake by default. Prefer
plain-text conversation over structured question tools; do not force the user
into fixed choices unless the user asks for that.

Adjust depth to the input:

- If the user gives only a vague idea, interview them until purpose, audience,
  density, tone, source material, and delivery context are clear enough to build.
- If the user provides a detailed document, old deck, outline, screenshots, or
  brand assets, summarize the inferred direction and ask only the few questions
  that materially affect the deck.
- If a choice can be inferred safely, state the assumption and continue.
- If the user explicitly says to proceed without questions, proceed and make the
  assumptions visible.

Useful dimensions to explore:

- **Mode**: launch/keynote-style, formal report, technical demo, hybrid, or a
  custom reference.
- **Audience and stakes**: who will see it, and what decision or feeling the deck
  should drive.
- **Density**: speaker-led with fewer words, reading-first with more detail, or a
  mixed rhythm.
- **Source material**: notes, documents, screenshots, brand assets, old slides,
  data, code snippets, or product demos.
- **Visual references and anti-references**: what it should resemble, and what it
  should avoid.

## When To Use

Use this skill when at least one of these is true:

- The deck is likely to go through user feedback and repeated agent edits.
- Layout, animation, screenshots, or charts are important enough to regression
  test.
- The deck has multiple sections, many scenes, or stateful animation beats.
- The user is worried that editing one slide will break another slide.

Do not use this skill for very small, throwaway, static slides where no harness is
needed. In that case, a single HTML output is usually enough.

## Glossary

| Term | Meaning | Starter location |
|---|---|---|
| **Stage** | Fixed 1920x1080 slide canvas scaled as a whole to the viewport. | `src/components/SlideStage.tsx` |
| **Scene** | One slide surface rendered by a React component. | `src/scenes/*.tsx` |
| **Beat** | A navigation state inside a scene, addressed by `?scene=<id>&beat=<n>`. Beat `0` is the initial state; `totalBeats` is the last beat index. | `src/SlideDeck.tsx` |
| **Registry** | Single source of truth for order and stable ids. | `src/SlideRegistry.tsx` |
| **Harness** | Playwright audit, visual regression, and setup preflight. | `tests/`, `scripts/` |
| **Frozen frame** | Test-time frame with animation, media, and live regions stabilized before screenshot capture. | `tests/visual.spec.ts` |

## Bootstrap

Start from the bundled starter instead of hand-assembling the project.

Before copying files, align on the deck root:

- If the current directory is empty, it can be the deck root; state that you will
  initialize the slides project there.
- If the current directory is not empty, do not scatter starter files into it.
  Ask whether to create a new subdirectory, continue an existing half-built deck,
  or use another path.
- If the directory already contains harness markers such as `src/SlideRegistry.tsx`
  and `tests/visual.spec.ts`, treat it as an existing deck instead of
  scaffolding over it.
- For a new deck, recommend an independent git repository after the target deck
  root is confirmed. If the target lives inside a parent git repo, explain the
  tradeoff and confirm before initializing nested git.

```bash
cp -r ~/.agents/skills/frontend-harness-slides/assets/starter ./my-deck
cd ./my-deck
npm install
npx playwright install chromium
npm run doctor
npm run dev
```

For the first visual baseline:

```bash
npm run visual:update
npm run test:full
```

Read `assets/starter/README.md` when working inside the copied project.

## Architecture Contracts

### Registry

- Add scenes in `src/scenes/` and register them in `src/SlideRegistry.tsx`.
- Keep `id` values stable; they name routes and visual snapshots.
- Reorder by moving registry entries, not by renaming files.
- The starter exposes `window.__SLIDE_REGISTRY__` through
  `exposeRegistryForTooling()`; keep this call in `src/main.tsx`.

### Stage

- All slide content lives inside `[data-slide-stage]`.
- Author at 1920x1080 stage coordinates. Do not use responsive breakpoints inside
  the stage.
- The stage carries `data-slide-id` and `data-beat`; tests assert these
  attributes instead of brittle class names.

### Beats

- URL state is the source of truth: `?scene=<id>&beat=<n>`.
- With `?test=true`, the deck locks to the requested frame for deterministic
  testing.
- Visual regression covers every scene and every beat.

### Interactive Regions

- Editable controls should not trigger slide navigation.
- Wrap embedded editors, playgrounds, or custom interactive widgets with
  `SandboxIsolator`.
- Keep iframes as external demo links plus a stable screenshot unless there is a
  specific reason to accept screenshot risk.

### Theming

- Put theme tokens in `src/theme/themes.ts` and consume them via CSS variables.
- Do not hardcode one-off color and font decisions across scene components.
- During visual discovery, show real deck-like previews rather than diagnostic
  option cards. See `references/theming.md`.

## Workflow

1. **Detect**: new deck, imported content, or existing harness deck.
2. **Align**: run brief intake or summarize the provided material and assumptions.
3. **Scaffold**: confirm the deck root, copy the starter, install dependencies,
   and run `npm run doctor`.
4. **Outline**: create registry ids and scene titles from the agreed narrative.
5. **Build**: author scene components, bind state to beats, and keep content
   inside the stage.
6. **Verify**: choose the smallest useful test tier during iteration, but run the
   full gate before delivery.
7. **Ship**: present, deploy, or create a project-specific handoff only after the
   checked frames match the intended result.

## Verification Tiers

Use the smallest tier that matches the risk of the change; do not mechanically
run full visual checks after every tiny text edit.

| Tier | Command | Use when |
|---|---|---|
| Preflight | `npm run doctor` | After scaffold, after moving the project, or when environment state is suspicious. |
| Fast gate | `npm test` | Ordinary scene/content edits; runs build plus auditor. |
| Visual check | `npm run visual` | Visual, animation, font, theme, shared component, stage, or CSS changes. |
| Full gate | `npm run test:full` | Before delivery, before accepting a new baseline, or when impact range is unclear. |

For intentional visual changes:

```bash
npm run visual:update
npm run test:full
```

The work is not ready to ship until the full gate passes or any remaining gap is
explicitly reported.

The harness must not be silently skipped: the registry must be non-empty, every
requested frame must land on the matching `data-slide-id` and `data-beat`, and the
auditor must report no unexpected collapse or overflow.

PDF is not a built-in starter concern. If the user explicitly asks for PDF, treat
it as a project-specific handoff after the full gate passes; choose the simplest
export path for that deck and inspect the output before delivery.

## Supporting Files

| File | Read/use when |
|---|---|
| `assets/starter/` | Copy this runnable project to start a deck. |
| `assets/starter/README.md` | Working inside the copied starter. |
| `references/theming.md` | Discovering or implementing a visual direction. |
| `references/fonts.md` | Choosing and bundling open-source fonts. |
| `references/asset-handling.md` | Preparing images, logos, SVGs, and fonts. |
| `references/content-import.md` | Importing content from documents or existing decks. |
| `references/document-to-deck.md` | Turning long-form text into a speaker-led or reading-first deck. |
| `references/cjk-fonts.md` | Choosing a simple Chinese/Japanese/Korean font strategy. |
| `references/visual-drift-triage.md` | Diagnosing visual snapshot drift before rebasing. |
| `references/component-libraries.md` | Choosing chart, code, diagram, and icon libraries. |
| `references/anti-patterns.md` | Reviewing risky slide/project patterns. |
| `references/troubleshooting.md` | Diagnosing common harness and rendering failures. |
| `references/deploy.md` | Deploying the built deck and handling optional handoff formats. |

## Anti-Patterns

- Rendering a whole static slide in canvas.
- Using viewport responsive breakpoints inside the fixed stage.
- Treating beats as decorative fades instead of story states.
- Renaming files or ids to insert a slide.
- Skipping the harness after changing scene code, CSS, animation, fonts, or assets.
- Promising features that are not implemented in the starter.

## Copy Quality Pass

Before final delivery, review the deck text for concrete claims, density, and tone.
Prefer specific titles, visible numbers, and direct takeaways over generic
corporate wording. If the deck is speaker-led, keep slide text short and put
detail in the spoken narrative. If it is reading-first, keep slides self-contained
without shrinking text into unreadability.
