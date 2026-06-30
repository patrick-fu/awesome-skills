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

The main skill file stays compact so accidental invocations are cheap. Once a
real slide production task is confirmed, the agent must read the four stage
references before building: plan, design, build, and verify/ship.

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

1. **Plan**: align with the user on content orientation, presentation format,
   duration, content mix, style, density, animation, stage, navigation,
   technology stack, and delivery. Recommend defaults, name alternatives, and
   maintain an external context document so long-running work does not drift.
2. **Design**: choose a visual direction, fonts, assets, copy boundary, and
   component approach. When style is unclear, build three interactive real-slide
   previews, capture screenshots, start a local server, and turn the user's
   choice into a selected theme contract.
3. **Build**: implement stable scenes, meaningful beats, fixed/mobile stage
   scaling, frozen mode, keyboard/touch navigation, and interactive motion in
   the chosen stack.
4. **Verify and ship**: run the relevant structural audit, visual smoke,
   interaction/mobile checks, production smoke when deployed, and then deliver
   the confirmed URL, PDF/static export, or both.

The user does not need to operate the frontend toolchain directly. The important
part is that the agent has enough structure to keep iteration controlled.

## Stage References

For confirmed non-trivial deck work, agents should read these in order:

- `references/01-plan.md`: intake, alternatives, visual preview, technology
  choice, context tracking, narrative plan, content registry, and visible-copy
  boundary.
- `references/02-design.md`: style presets, sketch emoji guidance, fonts, CJK,
  assets, components, interactive previews, selected theme contract, and copy
  quality.
- `references/03-build.md`: harness contracts, mobile fixed stage, navigation,
  frozen mode, motion, interactivity, and implementation pitfalls.
- `references/04-verify-and-ship.md`: audit profiles, visual smoke, production
  smoke, mobile/WebKit coverage, deployment, PDF/static handoff, and final
  reporting.

## When It Fits

Use it when the deck is non-trivial, expected to receive feedback, has animation
or state, uses screenshots/charts, or needs checked frames before handoff.

Skip it when you only need a tiny static one-off where a single HTML file is
enough and no regression harness is useful.

## More Skills

For more reusable agent skills, see
[Awesome Skills](https://github.com/patrick-fu/awesome-skills).
