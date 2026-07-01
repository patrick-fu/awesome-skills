---
name: frontend-harness-slides
description: >-
  Create high-standard HTML slide decks that can be edited without breaking
  other slides. Use for non-trivial web slides where the user wants rigorous
  upfront alignment, polished visuals, lively motion/interactions, precise
  iterative edits, and final delivery as an online deployment, PDF/static
  export, or both. Avoid for tiny one-shot or mostly static decks.
---

# Frontend Harness Slides

Build HTML slides that survive iteration. This skill does not provide a starter
project or require React, Vite, Tailwind, Playwright, or any other stack. Its
unit is the **harness contract**: stable frame address, registry, fixed stage,
frozen mode, audit surface, visual checks, and verified handoff.

## **PRE-BUILD ALIGNMENT HARD GATE**

For any non-trivial deck, this is a hard gate. **DO NOT** create files, scaffold
a project, write code, start a dev server, or begin implementation until the user
has explicitly confirmed the Pre-Build Alignment in plain text.

**INFERRED ANSWERS ARE NOT CONFIRMATION.** If the user provides substantial
source material, inspect it first and state the inferred direction, but still ask
the user to confirm or adjust the key decisions before implementation.

Every key decision **MUST** include a recommended value with rationale, 3-5
credible candidate options with a brief reason for each, and an explicit request
for confirmation.

Cover these Pre-Build Alignment decisions, at the level the task needs:

- **Content plan**: scope, non-goals, orientation, presentation format, duration,
  and content mix.
- **Design plan**: style, density, audit profile, motion direction, visual
  references, and whether a preview is useful.
- **Build plan**: fixed stage, navigation/touch expectations, technology stack,
  source material, and delivery target.
- **Context/status plan**: where project state will live, when it will be
  updated, and whether the user wants a different location.

Style preview **MUST** be asked before implementation. Recommend a minimal
interactive preview by default; skip it only when the user explicitly declines or
explicitly asks to proceed directly. If style is vague, recommend real
interactive previews. If the user already gave a clear style, confirm that style,
offer refinements and a few nearby alternatives for inspiration, and ask whether
to create a same-style minimal preview.

Keep alignment details as implementation constraints, not slide copy. Do not
render duration, audience, density, stage size, delivery target, navigation
requirements, or implementation notes on the slide surface unless the user asks.

For non-trivial deliverable decks, establish a context/status ledger before
implementation unless the user explicitly declines or the task is tiny/local-only.
Follow the user's preferred location; otherwise use project docs for deliverable
decks and a temp path for small explorations. Treat context as memory, not
control.

If the user gives a reference URL, deployed deck, or source repository, inspect
it before choosing stage, scaling, animation, and interaction contracts.

## Reference Loading

If the task is exploratory discussion, answer from this file and load only the
needed reference. Once the user confirms a non-trivial deck build, import, or
substantial edit, read the stage references before implementation:

1. `references/01-plan.md`
2. `references/style/index.md`
3. `references/02-design.md`
4. `references/03-build.md`
5. `references/04-verify-and-ship.md`

Do not build from `SKILL.md` alone after production is confirmed. The references
are the single source of truth for planning detail, visual systems, harness
implementation, verification, deployment, and handoff.

Use `references/01-plan.md` when shaping an actual intake prompt; this file only
lists the decision surface.

| File | Use for |
|---|---|
| `references/01-plan.md` | Intake, defaults and alternatives, context, narrative/content mix, source material, registry draft, visible-copy boundary. |
| `references/style/index.md` | Style Index, 24 style directions, semantic-to-visual mapping, visual pacing, and design DNA contract. |
| `references/02-design.md` | Style previews, style presets, layout variation, navigation design, fonts/CJK, assets, components, copy quality. |
| `references/03-build.md` | Stable frames, registry, fixed/mobile stage, navigation, frozen mode, motion, interaction, implementation pitfalls. |
| `references/04-verify-and-ship.md` | Audit profiles, visual smoke, production smoke, mobile/WebKit coverage, deployment, PDF/static handoff, final report. |

## Branches

- **Tiny one-shot deck**: prefer a single static HTML file; do not impose a
  harness unless the user needs iteration, animation states, or visual checks.
- **New harness-backed deck**: align, plan, preview if useful, establish the
  harness contracts, build, verify, and ship.
- **Imported or source-heavy deck**: treat source material as content and intent,
  not layout preservation; rebuild narrative, registry, assets, and scenes.
- **Existing deck**: preserve existing stack and conventions; adapt the harness
  contracts instead of replacing the project style.

## Project And Stack

For a new deck, work in a clean deck root. Do not scatter files into a non-empty
directory. If the directory already has a deck project, treat it as existing
work. Recommend an independent git repository when useful; if working inside a
broad workspace or parent repo, briefly confirm the deck root and key files are
tracked or ignored as expected.

Prefer the user's existing stack. For a new non-trivial deck with no preference,
React + Vite + Playwright is a reasonable default, but the skill's identity is
the harness contract, not any framework or test library.

## Harness Contracts

Read `references/03-build.md` before implementing or adapting a harness. A deck
is ready to iterate only when these contracts exist:

- **Stable frame address**: every scene and meaningful beat can be opened
  directly by stable id/state.
- **Registry**: tooling can enumerate scene order and beat counts without
  scraping visible text.
- **Fixed stage**: slide content is authored inside a fixed-ratio stage that
  scales as a whole.
- **Frozen mode**: tests can render deterministic settled states.
- **Audit surface**: checks can catch route mismatch, missing/collapsed content,
  overflow, asset/font failures, console/runtime errors, and interaction leaks.
- **Visual baseline**: screenshots or equivalent visual checks exist where pixel
  drift matters.

## Working Loop

1. **Detect** the branch: tiny static, new harness-backed, imported/source-heavy,
   or existing deck.
2. **Align and plan** with `references/01-plan.md`; create or update the
   context/status ledger for non-trivial deliverables.
3. **Design** with `references/02-design.md`; selected style means a visual
   system, not one repeated template.
4. **Build** with `references/03-build.md`; preserve the harness contracts in
   the chosen stack and update the ledger after major implementation milestones.
5. **Verify and ship** with `references/04-verify-and-ship.md`; deliver a live
   URL, PDF/static export, or both according to the confirmed target, then record
   final delivery and verification status in the ledger when one exists.

Treat local servers as previews unless the user explicitly asks for local-only
work. Treat the work as ready only after the relevant final check passes, or
after skipped checks and residual risks are reported clearly.

## Anti-Patterns

- Starting implementation from a vague prompt.
- Treating recommendations as user-confirmed requirements.
- Rendering internal planning context on the slide surface.
- Treating this skill as a mandate for a specific framework.
- Using viewport breakpoints inside the fixed stage.
- Rendering whole static slides in canvas.
- Treating beats as decorative fades instead of story states.
- Renaming stable scene ids casually after links or baselines exist.
- Skipping verification after layout, motion, font, asset, shared visual, or
  harness changes.
