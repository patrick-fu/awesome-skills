---
name: frontend-harness-slides
description: >-
  Create high-standard HTML slide decks that can be edited without breaking
  other slides. Use for HTML slide work where the user wants rigorous upfront
  alignment, polished visuals, lively motion/interactions, precise iterative
  edits, and final delivery as an online deployment, PDF/static export, or both.
---

# Frontend Harness Slides

Build HTML slides that survive iteration. This skill does not provide a starter
project or require React, Vite, Tailwind, Playwright, or any other stack. Its
unit is the **harness contract**: stable frame address, registry, fixed stage,
frozen mode, audit surface, visual checks, and verified handoff.

## **PRE-BUILD ALIGNMENT HARD GATE**

Before creating or modifying any HTML slide artifact, this is a hard gate.
**DO NOT** create files, scaffold a project, write code, start a dev server, or
begin implementation until the user has explicitly confirmed the Pre-Build
Alignment in plain text.

**INFERRED ANSWERS ARE NOT CONFIRMATION.** If the user provides substantial
source material, inspect it first and state the inferred direction, but still ask
the user to confirm or adjust the key decisions before implementation.

Every key decision **MUST** include a recommended value with rationale, credible
candidate options when the decision naturally has multiple useful directions,
and an explicit request for confirmation. For `deck root`, recommend one exact
project location with rationale and ask the user to confirm or replace it; do
not force artificial location alternatives. For execution parameters such as the
context ledger, testing, harness contracts, visible-copy boundary, source path,
or CJK font check, give a concrete plan and ask for confirmation or correction
instead of inventing option sets.

Cover these Pre-Build Alignment decisions, at the level the task needs:

- **Content plan**: scope, non-goals, orientation, presentation format, duration,
  and content mix.
- **Design plan**: style, density, audit profile, motion direction, visual
  references, and whether a preview is useful.
- **Project location plan**: confirmed `deck root`, whether it is new, existing,
  inside a parent repo, an independent repo, or temporary, and which files are
  expected there. Recommend one exact path and ask the user to confirm or
  replace it.
- **Build plan**: fixed stage, navigation/touch expectations, technology stack,
  source material, and delivery target.
- **Testing plan**: test runner, test command, and required coverage across
  render, frame addressing, navigation, interaction isolation, layout safety,
  runtime errors, assets/fonts, and build/export/deployment checks.
- **Context ledger plan**: where the `context ledger` will live, when it will be
  updated, and whether the user wants a different location.

Project location is part of the hard gate. **DO NOT** scaffold into the current
working directory by default. Confirm the exact `deck root` in plain text before
creating files, even when the current directory looks plausible.

Style preview **MUST** be asked before implementation. Recommend a minimal
interactive preview by default; skip it only when the user explicitly declines or
explicitly asks to proceed directly. If style is vague, recommend real
interactive previews. If the user already gave a clear style, confirm that style,
offer refinements and a few nearby alternatives for inspiration, and ask whether
to create a same-style minimal preview.

During style alignment, send the user the Live Demo link as a reference:
`https://frontend-harness-slides-demo.vercel.app/`. Explain that it is a dynamic
Workbench Demo with multiple preset styles, transitions, animations, and motion
examples. This does not replace the preview question: still ask whether to make
a few small, content-specific style previews before the full build.

Keep alignment details as implementation constraints, not slide copy. Do not
render duration, audience, density, stage size, delivery target, navigation
requirements, or implementation notes on the slide surface unless the user asks.

For delivered slide work or multi-turn implementation, establish a
`context ledger` before implementation unless the user explicitly declines.
The `deck root` owns source, assets, tests, and delivery commands; the
`context ledger` tracks decisions and progress. Follow the user's preferred
ledger location; otherwise use project docs for delivered decks and a temp path
for explorations. Treat context as memory, not control.

If the user gives a reference URL, deployed deck, or source repository, inspect
it before choosing stage, scaling, animation, and interaction contracts.

## Reference Loading

If the task is exploratory discussion, answer from this file and load only the
needed reference. Once the user confirms an HTML slide build, import, or
substantial edit, read the stage references before implementation:

1. `references/01-plan.md`
2. `references/style/index.md`
3. `references/style/preview.md`
4. `references/02-design.md`
5. `references/03-build.md`
6. `references/04-verify-and-ship.md`

Do not build from `SKILL.md` alone after production is confirmed. The references
are the single source of truth for planning detail, visual systems, harness
implementation, verification, deployment, and handoff.

Use `references/01-plan.md` when shaping an actual intake prompt; this file only
lists the decision surface.

| File | Use for |
|---|---|
| `references/01-plan.md` | Intake, defaults and alternatives, context, narrative/content mix, source material, registry draft, visible-copy boundary. |
| `references/style/index.md` | Style Index, curated style directions, semantic-to-visual mapping, visual pacing, and design DNA contract. |
| `references/style/preview.md` | Full style visual catalog with preset style progressions and Design DNA tokens. |
| `references/02-design.md` | Style previews, style presets, layout variation, navigation design, fonts/CJK, assets, components, copy quality. |
| `references/03-build.md` | Stable frames, registry, fixed/mobile stage, navigation, frozen mode, motion, interaction, implementation pitfalls. |
| `references/04-verify-and-ship.md` | Audit profiles, visual smoke, production smoke, mobile/WebKit coverage, deployment, PDF/static handoff, final report. |

## Branches

- **New slide artifact**: align, plan, preview if useful, establish the harness
  contracts the work needs, build, verify, and ship.
- **Imported or source-heavy deck**: treat source material as content and intent,
  not layout preservation; rebuild narrative, registry, assets, and scenes.
- **Existing deck**: preserve existing stack and conventions; adapt the harness
  contracts instead of replacing the project style.

## Project And Stack

Use the confirmed `deck root` for slide project files. The `deck root` is the
filesystem directory that owns the deck source, package/config files, assets,
tests, and delivery commands. For a new deck, prefer a new clean directory; an
existing deck project, a subdirectory inside a parent repo, an independent repo,
or a temporary exploration path are all acceptable when confirmed. Do not
scatter files into a non-empty directory or scaffold into the current working
directory just because the agent started there. If the confirmed root is inside
a broad workspace or parent repo, briefly confirm key generated files are
tracked or ignored as expected.

Prefer the user's existing stack. For a new deck with no preference, React +
Vite + Playwright is a reasonable default, but the skill's identity is the
harness contract, not any framework or test library.

**NO TEST-FREE OR UNDER-TESTED SLIDE OUTPUTS.** Every created or modified HTML
slide artifact must have a runnable test command and a sufficient multi-angle
test suite before delivery. Required coverage includes render and visible stage
content, frame addressing, navigation, interaction isolation, layout safety,
runtime errors, assets/fonts, and build/export/deployment behavior when
relevant. Use a TDD-style flow by default: establish the test entry early, then
implement and verify the harness, navigation, layout, interaction, and
export-risk areas in small steps.

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

1. **Detect** the branch: new slide artifact, imported/source-heavy, or existing
   deck.
2. **Align and plan** with `references/01-plan.md`; create or update the
   `context ledger` when the work is delivered or multi-turn.
3. **Design** with `references/02-design.md`; selected style means a visual
   system, not one repeated template.
4. **Build** with `references/03-build.md`; preserve the harness contracts in
   the chosen stack, keep tests moving with the implementation, and update the
   ledger after major implementation milestones.
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
- Creating or modifying HTML slide artifacts without a runnable test command and
  sufficient multi-angle tests.
- Using viewport breakpoints inside the fixed stage.
- Rendering whole static slides in canvas.
- Treating beats as decorative fades instead of story states.
- Renaming stable scene ids casually after links or baselines exist.
- Skipping verification after layout, motion, font, asset, shared visual, or
  harness changes.
