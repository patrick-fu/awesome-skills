---
name: frontend-harness-slides
description: >-
  Build iteration-safe HTML slide decks with a framework-neutral harness
  pattern. Use when the user wants web slides that an agent will keep changing:
  edit copy, adjust layout, add or remove scenes, tune animation, and verify
  that unrelated frames did not silently break. Best for non-trivial decks,
  repeated user feedback, animation states, visual checks, or team review. Avoid
  for tiny one-shot decks where a single static HTML file is enough.
---

# Frontend Harness Slides

Build HTML slides that survive iteration. The skill does **not** provide a
starter project, copyable template, or required framework. It gives the agent a
process and harness contracts so a deck can be changed repeatedly without
silently breaking unrelated frames.

## Core Promise

1. **Align before building**: do not start implementation from a vague prompt.
2. **Change freely, verify mechanically**: every meaningful frame can be
   addressed, frozen, enumerated, and checked.
3. **Bind mechanisms, not frameworks**: choose the stack from the user's project
   and preferences; preserve the harness contracts in that stack.

## STOP: Brief Intake First

THIS IS A HARD GATE. For vague new-deck requests, the first user-facing response
must be a short plain-text intake, not code, scaffolding, or file creation. At
minimum, confirm the deck's style, information density, and animation direction
before implementation.

DO NOT create files, choose a framework, scaffold a deck, or start slide
implementation from a vague prompt. First align with the user in plain text
unless the supplied context already answers every minimum decision below.

Completion criterion: proceed only when one is true:

- The user has confirmed every minimum decision.
- The source material or prior conversation already clearly answers every
  minimum decision.
- The user explicitly says to proceed with defaults or assumptions; in that case,
  state those assumptions before creating files.

Minimum decisions:

- **Slides style**: keynote/product-launch, formal report, technical demo,
  hybrid, or a custom reference.
- **Information density**: speaker-led sparse slides, reading-first dense slides,
  or a balanced rhythm.
- **Animation direction**: cinematic keynote motion, restrained report motion, or
  another explicit style. The recommended default is keynote-like motion:
  directional scene transitions, Magic Move-style continuity, beat-by-beat
  reveals, spring/scale emphasis, and visual de-emphasis of superseded items.
  Explain this recommendation and ask the user to confirm or adjust it before
  implementation. Read `references/animation-style.md` when the user asks for
  polished animation, gives an animation reference, or leaves animation
  direction vague.
- **Stage basis**: default to `1920x1080` when the user has no preference, but
  ask whether they prefer `1280x720`, `2560x1440`, or another fixed 16:9 or
  project-specific ratio.
- **Touch navigation**: ask whether phone, tablet, or touchscreen viewing should
  support tap/swipe navigation. Recommend support by default unless the user says
  the deck is desktop/presenter-only.

Use interview-style follow-up, not structured question tools. Ask few questions,
but ask real ones. If the user gives only a short idea, ask for the highest-risk
preference first instead of creating files. If the user provides a detailed
document, existing deck, outline, screenshots, or brand assets, summarize the
inferred direction and ask only the questions that materially affect the deck.

Useful default phrasing: "I recommend a keynote/product-launch motion style:
short directional transitions, meaningful beat-by-beat reveals, light spring or
scale emphasis, old ideas fading or being crossed out, and a final takeaway
highlight. Should I use that, or keep it more report-like and restrained?"

Useful dimensions to explore:

- **Mode**: launch/keynote-style, formal report, technical demo, hybrid, or a
  custom reference.
- **Audience and stakes**: who will see it, and what decision or feeling the deck
  should drive.
- **Density**: speaker-led with fewer words, reading-first with more detail, or a
  mixed rhythm.
- **Motion**: keynote-like animated reveals, restrained report-style transitions,
  or another reference.
- **Source material**: notes, documents, screenshots, brand assets, old slides,
  data, code snippets, or product demos.
- **Visual references and anti-references**: what it should resemble, and what it
  should avoid.

If the user gives a reference URL, deployed deck, or source repository, inspect
it before choosing the deck's stage, scaling, animation, and interaction
contracts. Extract concrete behavior such as base stage size, whether scale can
exceed `1`, transition style, beat reveal style, and click/touch navigation.

## When To Use

Use this skill when at least one is true:

- The deck is likely to go through user feedback and repeated agent edits.
- Layout, animation, screenshots, charts, or visual polish are important enough
  to check after changes.
- The deck has multiple sections, many scenes, or stateful animation beats.
- The user is worried that editing one slide will break another slide.

Do not use this skill for very small, throwaway, static slides where no harness
is useful. A single HTML output is enough in that case.

## Project Boundary

For a new deck, initialize in a clean deck root:

- If the current directory is empty, it may be the deck root.
- If the current directory is not empty, do not scatter deck files into it. Ask
  whether to create a new subdirectory, continue an existing half-built deck, or
  use another path.
- If the directory already contains a slide harness or deck project, treat it as
  existing work; do not overwrite it.
- Recommend an independent git repository for a new deck. If the target lives
  inside a parent git repo, explain the tradeoff and confirm before nested git.

## Technology Posture

Do not require React, Vite, Tailwind, Playwright, or any bundled starter. Prefer
the user's existing stack when one exists. For a new project, choose the simplest
web stack that can satisfy the harness contracts and the deck's visual needs.

Playwright is a good default for browser-level verification, but it is not the
skill's identity. If another browser automation or visual check system is
already present and can enumerate, freeze, and inspect the frames, use it.

## Harness Contracts

Read `references/harness-pattern.md` before implementing a new harness or
adapting an existing one. The deck is ready to iterate only when these contracts
are satisfied:

- **Stable frame address**: every scene and meaningful beat has a stable id and a
  direct way to render that frame.
- **Frame registry**: tooling can enumerate all scenes, their order, and their
  beat counts without scraping visible text.
- **Fixed stage**: slide content is authored inside a fixed-ratio stage that
  scales as a whole; viewport responsive rules do not rearrange slide content.
- **Frozen mode**: test-time rendering can stop animation, media, clocks, live
  regions, and random values at a deterministic frame.
- **Audit surface**: tests can detect route mismatch, missing content, overflow,
  collapsed elements, broken assets, and unexpected console/runtime errors.
- **Visual baseline**: visual snapshots or equivalent screenshots exist for
  frames where pixel drift matters, and updates are accepted only intentionally.

## Workflow

1. **Detect**: decide whether this is a tiny static deck, a new harness-backed
   deck, imported content, or an existing deck.
2. **Align**: complete the brief intake or summarize the provided material and
   assumptions.
3. **Choose**: pick the deck root and technology stack; do not copy a bundled
   project.
4. **Establish**: implement or adapt the harness contracts in the chosen stack.
5. **Build**: create the narrative, frames, assets, animation states, and visual
   system.
6. **Verify**: run the smallest useful check during iteration and a final check
   before handoff; report any skipped check explicitly.
7. **Ship**: present, deploy, or create a project-specific handoff only after
   checked frames match the intended result. If shipping a hosted URL, read
   `references/deploy.md` and run the production smoke test.

## Verification Tiers

Use project-specific commands. Do not mechanically run the heaviest visual suite
after every tiny text edit.

| Tier | Purpose | Use when |
|---|---|---|
| Preflight | Environment, dependencies, server, browser availability, obvious config issues. | After project setup, moving the deck, or suspicious environment state. |
| Structural audit | Registry, addressability, stage geometry, overflow, collapsed content, asset errors. | Ordinary scene/content/layout edits. |
| Visual check | Deterministic screenshots or equivalent rendered-frame comparison. | Visual, animation, font, theme, shared component, stage, or CSS changes. |
| Full gate | All relevant build, audit, and visual checks. | Before delivery, before accepting a new baseline, or when impact is unclear. |

The work is not ready to ship until the final relevant gate passes, or the agent
clearly reports what was not checked and why.

## Supporting Files

| File | Read/use when |
|---|---|
| `references/harness-pattern.md` | Implementing or adapting the framework-neutral harness contracts. |
| `references/theming.md` | Discovering or implementing a visual direction. |
| `references/style-presets.md` | Choosing preset-inspired visual directions for presentation or static information decks. |
| `references/animation-style.md` | Choosing or describing a deck animation direction. |
| `references/fonts.md` | Choosing and bundling open-source fonts. |
| `references/asset-handling.md` | Preparing images, logos, SVGs, and fonts. |
| `references/content-import.md` | Importing content from documents or existing decks. |
| `references/document-to-deck.md` | Turning long-form text into a speaker-led or reading-first deck. |
| `references/cjk-fonts.md` | Choosing a simple Chinese/Japanese/Korean font strategy. |
| `references/visual-drift-triage.md` | Diagnosing visual snapshot drift before rebasing. |
| `references/component-libraries.md` | Choosing chart, code, diagram, and icon libraries without binding a stack. |
| `references/anti-patterns.md` | Reviewing risky slide/project patterns. |
| `references/troubleshooting.md` | Diagnosing common harness and rendering failures. |
| `references/deploy.md` | Deploying the checked deck or preparing optional handoff formats. |

## Anti-Patterns

- Skipping brief intake on a vague request and starting implementation.
- Treating this skill as a mandate to use a particular frontend framework.
- Rendering a whole static slide in canvas.
- Using viewport responsive breakpoints inside the fixed stage.
- Treating beats as decorative fades instead of story states.
- Renaming stable scene ids casually after baselines or links exist.
- Skipping the harness after changing layout, animation, fonts, assets, or shared
  visual code.

## Copy Quality Pass

Before final delivery, review the deck text for concrete claims, density, and
tone. Prefer specific titles, visible numbers, and direct takeaways over generic
corporate wording. If the deck is speaker-led, keep slide text short and put
detail in the spoken narrative. If it is reading-first, keep slides
self-contained without shrinking text into unreadability.
