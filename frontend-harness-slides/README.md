# Frontend Harness Slides

**[中文说明](README.zh-CN.md)**

Build HTML slides that an agent can keep changing without quietly breaking
unrelated frames.

A single HTML file is great for a fast first draft. The hard part starts after
that: the user asks to rewrite a page, add a section, remove a slide, tune an
animation, replace screenshots, or make one dense page more readable. In a
monolithic file, a small CSS or animation change can accidentally damage another
slide, and the breakage may stay invisible until review.

`frontend-harness-slides` turns that messy iteration phase into a checked
workflow. It starts from a React/Vite slide project and adds a Playwright harness
that can audit structure, freeze animation, and compare every frame before the
agent hands off a browser deck, hosted build, or project-specific export.

## Install

```bash
npx skills add patrick-fu/frontend-harness-slides
```

Update later:

```bash
npx skills update
```

## What It Solves

- **Repeated edits without silent collateral damage**: scenes and beats are
  addressable, testable frames rather than hidden states in one large file.
- **Insert, delete, and reorder safely**: a central registry owns order, so scene
  ids and visual baselines stay stable.
- **Layout stays fixed**: every scene lives on a 1920x1080 stage that scales as a
  whole instead of reflowing per viewport.
- **Animation becomes reviewable**: test mode freezes frames so pixel diffs mean
  real changes, not timing jitter.
- **Delivery stays grounded**: the agent checks the deck frames before choosing
  any final handoff format.

## How An Agent Uses It

1. Align with the user on audience, density, source material, and visual
   direction.
2. Copy the bundled starter.
3. Build scenes as React components registered by stable ids.
4. Run the appropriate test tier during iteration, then the full gate before
   delivery.
5. Update visual baselines only for intentional changes.
6. Deploy or create a project-specific handoff only after the checked frames
   match the intended result.

The user does not need to operate the frontend toolchain directly. The important
part is that the agent has a harness to keep iteration controlled.

## Quick Start

```bash
cp -r ~/.agents/skills/frontend-harness-slides/assets/starter ./my-deck
cd ./my-deck
npm install
npx playwright install chromium
npm run doctor
npm run dev
```

First baseline and verification:

```bash
npm run visual:update
npm run test:full
```

## When It Fits

Use it when the deck is non-trivial, expected to receive feedback, has animation
or state, uses screenshots/charts, or needs checked frames before handoff.

Skip it when you only need a tiny static one-off where a single HTML file is
enough and no regression harness is useful.

## More Skills

For more reusable agent skills, see
[Awesome Skills](https://github.com/patrick-fu/awesome-skills).
