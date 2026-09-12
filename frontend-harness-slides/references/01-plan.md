# 01 Plan

Use this before creating or substantially changing a deck. The goal is to turn a
user brief into implementation constraints, a content registry, and a visual
direction before scene code starts. Small edits to an existing deck with explicit
requirements can skip intake and start the change.

## Demand Alignment Interview

Before planning the harness, align on the user's real presentation need. The
intake is not a checklist collection exercise; it is the process that turns a
vague request into a shared understanding the agent can act on.

Use a soft grilling posture: explore what can be known from files, repos, URLs,
old decks, or source material before asking; then challenge unclear assumptions
and resolve the most consequential dependencies first. The tone should stay
collaborative and concrete, not adversarial. The point is to make the user react
to a recommended direction with rationale, not to force them through a form.

Start with the highest-impact unknown. Resolve upstream decisions before
downstream execution details:

1. **Purpose and audience**: what the deck needs to achieve, who will see it,
   and what they should understand, believe, or do afterward.
2. **Content boundary and story**: what belongs in the deck, what should be left
   out, which source material matters most, and what core narrative should carry
   the presentation.
3. **Use context**: live talk, workshop, recording, product pitch, internal
   review, reading-first document, or another consumption mode.
4. **Density and pacing**: speaker-led, reading-first, or hybrid, plus expected
   duration and section balance.
5. **Visual and motion direction**: style family, references, preview need,
   motion intensity, and delivery risk.
6. **Execution constraints**: `deck root`, stack, harness contracts, testing,
   Context document, delivery target, and artifact hygiene.

Ask one major decision branch at a time when the direction is unclear. Provide
your recommended answer and rationale with each question so the user can react
to a concrete proposal instead of inventing the deck from scratch. For compact
or low-risk tasks, group remaining unknowns when that is ordered by decision
priority and each important default is visible. Do not dump an unordered
checklist of questions.

If a question can be answered by exploring the user's files, source material,
old deck, repository, or URL, inspect that source first. Then summarize the
inference and ask only about unresolved parts that materially affect the result
or scope.

Useful first-turn pattern for a vague request:

```text
I recommend first locking the purpose and audience, because that decides the
story, density, and style. My read is <recommended purpose/audience> because
<reason>. If that is right, I will shape the deck as <format/density>. If not,
tell me the real audience or outcome and I will recalibrate before choosing
style or implementation details.
```

Before implementation, produce a compact shared-understanding snapshot. Treat it
as implementation memory, not slide copy. Start work when remaining unknowns do
not materially affect the result or scope, or after those unknowns are resolved.

## Intake Gate

Ask only unresolved decisions that materially affect the result or scope. For
each of those, give a recommended default with a reason. Name candidate options
only when the decision naturally has several useful directions, such as style,
visual direction, content orientation, information density, motion direction,
navigation style, delivery target, or technology stack. Do not only ask "is my
default OK?" Keep all intake questions in normal chat text. Do not call
`AskUserQuestion`, `AskQuestion`, `request_user_input`, or any structured
single-choice, multiple-choice, or form-style question tool.

Execution parameters should be concrete plans, not artificial option sets. Use
a path the user already gave or the existing deck's root. If a long-term
deliverable has no reliable specified target, recommend one exact `deck root`
with a reason and confirm it before scaffolding. A user home directory or other
broad workspace is not a reliable long-term `deck root`. Do not assume the
current working directory is the deck root. State Context document location,
testing requirement, harness contracts, visible-copy boundary, source material
path, and fonts/CJK reminders as plans unless a remaining unknown would change
the result or scope.

When the user provides substantial source material, inspect it before asking
generic intake questions. Infer the story, likely format, content density,
style cues, and missing decisions, then proceed from that inference. An
inference is a working plan, not an explicit user requirement. Confirm only
leftovers that still materially affect the result or scope.

Use the format that fits the decision. State a routine recommendation and
continue when the choice is already decided or does not change result or scope.
For a material unknown, ask a concrete confirmation and wait.

For a material unknown:

```text
Recommendation: <value> because <reason>.
Candidates:
1. <option>: <why it may fit>
2. <option>: <why it may fit>
3. <option>: <why it may fit>
This still changes the result or scope. Please confirm or give the corrected
value before I continue.
```

These candidate options are plain-text discussion aids, not structured question
tool choices.

For a routine recommendation:

```text
I'll use <exact value or plan> because <reason>.
```

Minimum decisions:

- **Content and presentation plan**: lock what the deck should cover and what
  it should leave out when those are still open. Use a given orientation,
  presentation format, duration, and content mix. Recommend a structure and
  offer alternatives when the format is still open: teaching, persuasion,
  product demo, research readout, retrospective, sales pitch, workshop, live
  talk, recording, internal review, or reading-first document.
- **Mode and style**: recommend style directions from
  `references/style/index.md` using the user's material, audience, density,
  formality, delivery target, and references. Offer at least five style
  recommendations or refinements with reasons when the user has not already
  chosen a clear direction.
- **Project location / deck root**: this is the directory that owns deck source,
  package/config files, assets, tests, and delivery commands. Use a given path
  or existing deck root. If a long-term deliverable has no reliable specified
  target, give one recommended path with rationale and confirm it before
  scaffolding. Do not assume the current working directory is the deck root.
- **Language and CJK Check**: If the content contains Chinese, Japanese, or Korean (CJK) characters, select fonts and fallback stacks that cover CJK, and perform a browser check to ensure proper rendering. Avoid making this a heavy font audit process; keep the intake lightweight and focus on selecting reliable system fallbacks or bundled CJK fonts if needed.
- **Information density**: recommend speaker-led, reading-first, or hybrid.
  Explain that this also sets the audit profile.
- **Animation**: recommend Keynote Magic Move-style continuity by default, and
  offer livelier, restrained, or mostly static motion.
- **Stage**: recommend `1920x1080` for most 16:9 decks, but explicitly offer
  `1280x720`, `2560x1440`, `4:3`, or a custom ratio.
- **Navigation**: recommend a subtle in-stage navigator plus keyboard/touch
  navigation, but offer no navigator, bottom dots, side dots, section tabs, or a
  project-specific style.
- **Technology stack**: recommend the stack that fits the harness and the user's
  preferences. For a new deck with no existing stack, React + Vite + Playwright
  is a reasonable default because it supports
  componentized scenes, animation state, direct frame routing, browser checks,
  and static deployment. Also name alternatives and tradeoffs: plain
  HTML/CSS/JS is light but weaker for long iteration; Vue/Svelte + Vite are
  fine if the user prefers them; Next.js is useful inside an existing Next app
  but usually heavy for a pure deck; Astro/static generators fit content-heavy
  decks but need extra care for rich interactions.
- **Testing plan**: state the test runner, test command, and required coverage
  before implementation. The plan should cover render and visible stage content,
  frame addressing, navigation, interaction isolation, layout safety,
  console/runtime errors, asset/font loading, and build/export/deployment checks
  when relevant. Recommend a browser-based test path such as Playwright when
  the deck has navigation, animation, interaction, screenshots, or delivery
  checks. Testing is mandatory for created or modified HTML slide artifacts; do
  not present it as an optional preference. Mention alternatives only when
  project constraints make them relevant, and explain the coverage tradeoff.
- **Delivery**: use the stated delivery target. If the long-term handoff is
  still unresolved, recommend online URL, PDF/static export, or both and
  confirm. If the user has no hosting preference, recommend Vercel and mention
  GitHub Pages or Cloudflare Pages as static-site alternatives. Do not publish
  or deploy without authorization.

Summarize the working decisions as implementation constraints, not slide copy.
Duration, audience, density, style, stage size, navigation, delivery target, and
tech stack should guide the work; render them only if the user explicitly wants
the audience to see them.

For delivered slide work or multi-turn implementation, prefer a Context document
for decisions that need to survive beyond the current chat. This is project
memory, not a control mechanism. Follow the user's preferred location or the
repo's existing `CONTEXT.md` / `CONTEXT-MAP.md` convention; otherwise use project
docs for delivered decks and a temp path for explorations.

Keep `deck_root` and `context_document` separate. The deck root owns the source
project; the Context document records decisions and progress. They may live near
each other, but choosing one does not choose the other.

Useful grouped prompt:

```text
I recommend treating this as a speaker-led live talk: 10% context, 20% problem
framing, 30% core argument, 25% demo/cases, and 15% method plus closing. If you
want it to be more like a product pitch, technical training, research readout,
or self-reading document, I will change the content ratio and slide density.
```

## Visual Preview Default

Follow the user's explicit choice to make or skip a visual preview. Otherwise,
recommend one when unresolved visual choices would benefit from comparison;
proceed without one when the style is clear or the edit preserves the visual
system. When visual direction is unclear and the user has not declined previews,
recommend making three real interactive slide previews before building the full
deck. If the user already supplied a clear style or strong visual reference, use
that direction. Offer at least five same-style refinements or nearby style
recommendations with reasons as optional inspiration, not a required extra
question.
Also send the Live Demo link during open style choice:
`https://frontend-harness-slides-workbench.vercel.app/`. Explain that it is a dynamic
Workbench Demo with multiple preset styles, transitions, animations, and motion
examples, so the user can judge movement and density directly. Treat this as a
parallel aid to real previews, not a substitute for them and not a required
extra question.
Use the same planned production stack, stage basis, and harness skeleton where
possible so font loading, stage scaling, navigation, motion, and browser issues
surface early. Use the user's actual title, content, screenshots, or data.
Render previews as real slides from the user's deck, with audience-facing copy
on the slide surface and candidate rationale kept in chat or theme notes.

Use the Density-Fit / Safe / Wildcard preview mix defined in
`references/style/index.md` (the canonical definition); do not restate it here.

All three previews should share an anchor slide so the user can compare the
same content fairly. Provide screenshots and a local server URL.
Each preview should include comparable interaction, beat/state change, and
transition behavior. After the user chooses, summarize a selected theme notes
before full expansion.

When the user already chose a style, use it and proceed unless a remaining
visual unknown would change the result or the user asked for a preview. A
same-style preview is optional unless the user requested one.

Good default phrasing when visual direction is still open:

```text
I recommend first making three real interactive slide previews using the same
stage and project skeleton: one Density-Fit direction, one Safe direction, and
one Wildcard direction. I will choose those from the content, audience, density,
formality, delivery target, and visual references. I will also send the dynamic
Live Demo link so you can inspect preset styles, transitions, and motion
behavior while I prepare the previews. I will capture screenshots and start a
local server so you can compare them. After you pick a direction, I will write
the selected theme notes and expand the full deck.
```

## Context Document

For delivered slide work or multi-turn implementation, create or update a
Context document when there is useful state to preserve, unless the user
explicitly declines. Create it lazily, the first time there is something worth
recording. This is project memory, not a control mechanism: it keeps decisions
and progress outside chat so later edits do not depend on hidden conversation
state.

If the user or repo already has a context convention, follow it. If a root
`CONTEXT.md` or `CONTEXT-MAP.md` exists, use that structure to decide where deck
context belongs. Otherwise, store deliverable deck context in project docs such
as `docs/context.md`, `docs/implementation-context.md`, or the handoff note. For
exploratory work, `/tmp` or another agreed temp path is fine. Do not edit
`.gitignore` just for this unless the user asks.

Useful things to track:

- intake decisions
- deck root and project location decision
- narrative plan and content mix
- registry draft
- selected theme notes & Design DNA (including chosen style system, visual guardrails, custom-invented metaphors, and pacing log)
- technology stack, commands, and ports
- harness contracts and route patterns
- style preview links/screenshots and preview check result
- verification status
- delivery target and production URL/PDF path
- open issues, skipped checks, and user decisions

Update after major phases with a compact status entry:

- intake / decision snapshot
- narrative plan
- style preview selection
- registry draft
- harness setup
- major content build
- verification
- deployment or export

When verification coverage, delivery status, production URLs, or skipped risks
change materially, update the Context document so later edits do not depend on
chat history alone. If no Context document is used, keep the reason explicit in
the chat or final report.

## Decision Snapshot

Before implementation, write a compact snapshot in chat or project notes:

```text
deck_root:
audience:
talk_duration:
content_orientation:
presentation_format:
content_mix:
mode:
style:
density:
audit_profile:
motion:
stage:
navigation:
technology_stack:
testing_plan:
test_command:
visual_language:
delivery_target:
non_goals:
context_document:
```

This snapshot is implementation memory. It is not slide copy.

## Narrative Plan

Before the registry draft, produce a concise narrative/content-mix plan for
delivered or multi-turn slide work:

```text
orientation:
presentation_format:
duration:
section_mix:
pacing_notes:
non_goals:
```

The section mix may be percentages or slide counts. Example:

```text
orientation: teaching + demo
presentation_format: 40-minute live talk
section_mix:
  - 10% context
  - 20% problem framing
  - 30% core argument
  - 25% demo/cases
  - 15% method + closing
pacing_notes: sparse slides, one idea per scene, demo beats get more time
non_goals: not a self-contained whitepaper
```

## Content Source

Use this section when the user provides a long article, memo, PRD, transcript,
old deck, outline, screenshots, or product captures.

Import is not layout preservation. Treat source material as content and intent,
then rebuild the deck into stable scenes inside the fixed stage.

For source-heavy requests, understand the material before deciding what to ask
the user. Summarize the inferred direction, propose defaults, and confirm only
the choices that still materially affect the deck.

Before mapping content, decide the deck's narrative allocation. A 40-minute live
talk, a 10-minute product pitch, a workshop, and a reading-first report should
not use the same slide count, text density, or section weights.

For long or sprawling source material, first rebuild the core story and trimming
strategy. Record the important content choices when useful: what was kept,
condensed, moved to speaker notes, or deliberately removed. Keep this as
planning context rather than slide copy.

Practical paths:

| Source | Path | Notes |
|---|---|---|
| PPTX / PowerPoint | Extract text, images, notes, and slide order. | Rebuild layout; do not copy absolute coordinates blindly. |
| Keynote | Export to PPTX first when possible. | Smart builds may flatten; inspect notes or source text. |
| Google Slides | Download as PPTX or use the outline. | Verify image quality after export. |
| Markdown / Notion / docs | Split by headings, narrative sections, and evidence. | Often better than forcing a fake PPTX conversion. |
| Screenshots / product captures | Keep originals as assets and design scenes around them. | Screenshots should drive outline decisions, not be pasted after the fact. |

Map source fields carefully:

| Source field | Deck destination | Rule |
|---|---|---|
| Slide order | Registry order | Preserve first, then intentionally trim or reorder. |
| Title | Stable id plus display title | Ids should survive wording changes. |
| Text blocks | Scene content | Split dense content into scenes or beats. |
| Images | Project assets | Optimize and name by content. |
| Speaker notes | Planning/script material | Render only in presenter mode if the project supports it. |

## Registry Draft

For delivered or multi-turn slide work, prefer producing a narrative plan and
registry draft before scene implementation. This is planning guidance, not a
polished deliverable.

Required fields:

```text
id:
title:
visible_copy:
speaker_intent:
beats:
visual_idea:
mode:
section:
source:
internal_constraints:
```

`visible_copy` is the audience-facing text that belongs on the slide surface.
Keep planning metadata out of it. Talk duration, audience, style labels,
information density, stage size, delivery target, deployment provider,
navigation requirements, implementation notes, and review instructions are
internal constraints unless the user explicitly asks to show them.

Planning registry fields do not all need to enter runtime code. The runtime
manifest can stay smaller as long as stable ids, ordering, and beat or frame
counts remain aligned with the planning registry.

For longer decks, add `layoutFamily` or an equivalent visual structure tag when
useful. The goal is to let the selected style expand into varied scene
structures instead of one repeated component.

Example:

```text
id: opening
title: Why this matters now
visible_copy: The old workflow is no longer the bottleneck.
speaker_intent: Explain that coordination, not typing, is the pain.
beats: 3
visual_idea: robot, keyboard, and microphone converge into one workflow
mode: speaker-led
section: setup
source: paragraphs 1-4
internal_constraints: 40-minute talk, low text density, 1920x1080 stage
```

## Density Heuristics

- Speaker-led technical talks need fewer words and more pacing beats than the
  source document suggests.
- Reading-first decks can carry more detail, but each page still needs a clear
  title and visible hierarchy.
- Hybrid decks should mark each scene or section as speaker-led or
  reading-first.
- If one source section contains several claims, split it into multiple scenes
  instead of shrinking text.
- Preserve concrete numbers, names, examples, and evidence. Remove duplicated
  setup.

## Planning Checklist

Before building:

1. Material decisions are resolved. Routine defaults are recorded as
   assumptions. Given path, style, and similar constraints were not re-asked.
2. Recommended defaults were shown for remaining key decisions, with
   alternatives only where the decision naturally benefits from them.
3. Content orientation, presentation format, duration, and content mix are
   known or explicitly assumed.
4. Context location is clear when the task is long-running or deliverable.
5. Non-trivial decks have a narrative plan before the registry draft.
6. A visual preview was made or offered when the user asked for one, or when
   the visual direction was unclear and a preview would reduce uncertainty.
7. The decision snapshot separates constraints from slide copy.
8. Non-trivial decks have a registry draft with `visible_copy`.
9. Internal alignment details are not being treated as source content.
