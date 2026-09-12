---
name: frontend-harness-slides
description: >-
  Build and revise iteration-safe HTML slide decks with polished visuals,
  motion, testing, and web/PDF/static delivery. Use only for HTML slide
  projects.
---

# Frontend Harness Slides

Build HTML slides that survive iteration. This skill does not provide a starter
project or require React, Vite, Tailwind, Playwright, or any other stack. Its
unit is the **harness contract**: stable frame address, registry, fixed stage,
frozen mode, audit surface, visual checks, and verified handoff.

## Pre-Build Alignment

Use explicit user requirements. An inferred or recommended default is a working
plan, not an explicit user requirement. For a small edit with clear requirements
to an existing deck, preserve the current stack, `deck root`, and visual system
except where the user requests a change, and proceed.

Inspect discoverable facts first: source material, the existing deck, the repo,
a deployed URL, and project files. Ask only unresolved decisions that materially
affect the result or scope. Do not re-ask a path, style, stage, stack, density,
navigation, or delivery target the user already gave.

When the brief is still vague, treat alignment as focused grilling: purpose and
audience, content boundary and story, presentation format and density, then the
remaining execution constraints. Keep each round on the next highest-impact
unknown. Ask in normal chat text, with a recommended answer, rationale, and
impact. Group related low-risk questions when that reduces back-and-forth. Do
not call `AskUserQuestion`, `AskQuestion`, `request_user_input`, or any
structured single-choice, multiple-choice, or form-style prompt. Candidate
options may clarify a real directional choice, but they stay as plain text.

Cover these decisions at the level the task needs. This is a decision surface,
not a confirmation ritual:

- **Content plan**: scope, non-goals, orientation, presentation format, duration,
  and content mix.
- **Design plan**: style, density, audit profile, motion direction, visual
  references, and whether a preview would reduce visual uncertainty.
- **Project location plan**: the `deck root`, whether it is new, existing,
  inside a parent repo, an independent repo, or temporary, and which files are
  expected there. Use a path the user already gave or the existing deck's root.
  A user home directory or other broad workspace is not a reliable long-term
  `deck root`. If a long-term deliverable has no reliable specified target,
  recommend one exact path and confirm before scaffolding. Do not scaffold into
  the current working directory just because the agent started there.
- **Build plan**: fixed stage, navigation/touch expectations, technology stack,
  source material, and delivery target. Do not publish or deploy without
  authorization.
- **Testing plan**: test runner, test command, and required coverage across
  render, frame addressing, navigation, interaction isolation, layout safety,
  runtime errors, assets/fonts, and build/export/deployment checks. Testing is
  required for created or modified HTML slide artifacts; do not present it as a
  preference to confirm.
- **Context document plan**: where the Context document will live, when it will be
  updated, and whether the user wants a different location.

Follow the user's explicit choice to make or skip a style preview. Otherwise,
recommend one when unresolved visual choices would benefit from comparison;
proceed without one when the style is clear or the edit preserves the visual
system. For open-ended style selection,
use a three-candidate preview mix: Density-Fit, Safe, and Wildcard. Choose those
candidates from the user's material, audience, density, formality, risk level,
delivery target, and visual references. Read `references/style/index.md` first,
then load only the individual style files needed for shortlisted candidates.

During open style choice, send the Live Demo link as a reference:
`https://frontend-harness-slides-workbench.vercel.app/`. It is a dynamic Workbench
Demo with preset styles, transitions, animations, and motion examples. It does
not replace a content-specific preview and is not a required extra question.

Keep alignment details as implementation constraints, not slide copy. Do not
render duration, audience, density, stage size, delivery target, navigation
requirements, or implementation notes on the slide surface unless the user asks.

For delivered slide work or multi-turn implementation, create or update a
Context document when useful state needs to survive beyond chat, unless the user
explicitly declines. The `deck root` owns source, assets, tests, and delivery
commands; the Context document tracks decisions and progress. Follow the user's
or repo's existing context convention; otherwise use project docs for delivered
decks and a temp path for explorations. Treat context as memory, not control.

If the user gives a reference URL, deployed deck, or source repository, inspect
it before choosing stage, scaling, animation, and interaction contracts.

## Reference Loading

If the task is exploratory discussion, answer from this file and load only the
needed reference. Once the task is an HTML slide build, import, or substantial edit, read the
stage references before implementation:

1. `references/01-plan.md`
2. `references/style/index.md`
3. `references/02-design.md`
4. `references/03-build.md`
5. `references/04-verify-and-ship.md`

Do not build from `SKILL.md` alone once production implementation starts. The references
are the single source of truth for planning detail, visual systems, harness
implementation, verification, deployment, and handoff.

Use `references/01-plan.md` when shaping an actual intake prompt; this file only
lists the decision surface.

| File | Use for |
|---|---|
| `references/01-plan.md` | Intake, defaults and alternatives, context, narrative/content mix, source material, registry draft, visible-copy boundary. |
| `references/style/index.md` | Flat, tagged style catalog with progressive loading, canonical preview mix, semantic-to-visual mapping, and per-style Design DNA links. |
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

Use the `deck root` for slide project files. The `deck root` is the filesystem
directory that owns the deck source, package/config files, assets, tests, and
delivery commands. For a new deck, prefer a new clean directory; an existing
deck project, a subdirectory inside a parent repo, an independent repo, or a
temporary exploration path is fine when that is the target. Do not scatter
files into a non-empty directory or scaffold into the current working directory
just because the agent started there. If the root is inside a broad workspace
or parent repo, check that key generated files are tracked or ignored as
expected.

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
   Context document when the work is delivered or multi-turn.
3. **Design** with `references/02-design.md`; selected style means a visual
   system, not one repeated template.
4. **Build** with `references/03-build.md`; preserve the harness contracts in
   the chosen stack, keep tests moving with the implementation, and update the
   Context document after major implementation milestones.
5. **Verify and ship** with `references/04-verify-and-ship.md`; deliver a live
   URL, PDF/static export, or both according to the delivery target, then record
   final delivery and verification status in the Context document when one
   exists.

Treat local servers as previews unless the user explicitly asks for local-only
work. Treat the work as ready only after the relevant final check passes, or
after skipped checks and residual risks are reported clearly.

## Anti-Patterns

- Starting implementation from a vague prompt.
- Re-asking a path, style, or other decision the user already made.
- Treating the agent's own recommendations or inferences as explicit user
  requirements.
- Blocking on confirmation of defaults that do not change result or scope.
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
