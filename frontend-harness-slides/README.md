# Frontend Harness Slides

**[中文说明](README.zh-CN.md)**

Build HTML slides that an agent can keep changing without quietly breaking
unrelated frames.

A single HTML file is useful for a quick draft. The hard part starts after that:
the user asks to rewrite a page, add a section, remove a slide, tune an
animation, replace screenshots, or make one dense page more readable. In a
monolithic file, a small CSS or animation change can accidentally damage another
slide, and the breakage may stay invisible until review.

`frontend-harness-slides` turns that iteration phase into a checked workflow. It
does not ship a starter project or require React, Vite, Tailwind, Playwright, or
any other framework. It gives the agent a framework-neutral harness pattern:
stable frame addresses, a registry, fixed stage geometry, deterministic frozen
mode, structural audits, and visual checks when they matter.

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
- **Insert, delete, and reorder safely**: a registry owns order, so scene ids and
  visual baselines stay stable.
- **Layout stays fixed**: slide content lives on a fixed-ratio stage that scales
  as a whole instead of reflowing per viewport.
- **Animation becomes reviewable**: frozen mode makes frame checks deterministic.
- **Delivery stays grounded**: the agent checks the deck before choosing a final
  handoff format.

## How An Agent Uses It

1. First align with the user on audience, density, source material, visual
   direction, and delivery context.
2. Choose the project root and technology stack from the user's situation.
3. Implement the harness mechanisms in that stack.
4. Build the deck as stable scenes and meaningful beats.
5. Run the smallest useful checks during iteration and the final gate before
   delivery.
6. Deploy or create a project-specific handoff only after checked frames match
   the intended result.

The user does not need to operate the frontend toolchain directly. The important
part is that the agent has enough structure to keep iteration controlled.

## When It Fits

Use it when the deck is non-trivial, expected to receive feedback, has animation
or state, uses screenshots/charts, or needs checked frames before handoff.

Skip it when you only need a tiny static one-off where a single HTML file is
enough and no regression harness is useful.

## More Skills

For more reusable agent skills, see
[Awesome Skills](https://github.com/patrick-fu/awesome-skills).
