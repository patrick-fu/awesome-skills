# 01 Plan

Use this before creating or substantially changing a deck. The goal is to turn a
user brief into explicit implementation constraints, a content registry, and a
small visual direction decision before scene code starts.

## Intake Gate

For each important decision, give a recommended default, name credible
alternatives, and ask the user to confirm or adjust. Do not only ask "is my
default OK?"

When the user provides substantial source material, inspect it before asking
generic intake questions. First infer the story, likely format, content density,
style cues, and missing decisions; then propose a direction with alternatives
for confirmation.

Minimum decisions:

- **Content and presentation plan**: confirm what the deck should cover and what
  it should leave out. Confirm the content orientation, presentation format,
  expected duration, and rough content mix. Recommend a structure and offer
  alternatives: teaching, persuasion, product demo, research readout,
  retrospective, sales pitch, workshop, live talk, recording, internal review,
  or reading-first document.
- **Mode and style**: recommend a direction such as Sketchboard Emoji for a
  lively talk, but offer alternatives such as professional information design,
  tech grid, product-launch, editorial report, or a supplied reference.
- **Language and CJK Check**: Proactively ask the user if the slide deck will contain Chinese, Japanese, or Korean (CJK) characters. If yes, flag that the "Cross-Language Typography Alignment" guidelines must be activated during the design phase to ensure visual character consistency and reliable system fallback fonts. If no, keep the typography stack lightweight and Latin-only.
- **Information density**: recommend speaker-led, reading-first, or hybrid.
  Explain that this also sets the audit profile.
- **Animation**: recommend Keynote Magic Move-style continuity by default, and
  offer livelier, restrained, or mostly static motion.
- **Stage**: recommend `1920x1080` for most 16:9 decks, but explicitly offer
  `1280x720`, `2560x1440`, `4:3`, or a custom ratio.
- **Navigation**: recommend a subtle in-stage navigator plus keyboard/touch
  navigation, but offer no navigator, bottom dots, side dots, section tabs, or a
  project-specific style.
- **Technology stack**: recommend the simplest stack that fits the harness and
  the user's preferences. For a new non-trivial deck with no existing stack,
  React + Vite + Playwright is a reasonable default because it supports
  componentized scenes, animation state, direct frame routing, browser checks,
  and static deployment. Also name alternatives and tradeoffs: plain
  HTML/CSS/JS is light but weaker for long iteration; Vue/Svelte + Vite are
  fine if the user prefers them; Next.js is useful inside an existing Next app
  but usually heavy for a pure deck; Astro/static generators fit content-heavy
  decks but need extra care for rich interactions.
- **Delivery**: confirm online URL, PDF/static export, or both. If the user has
  no hosting preference, recommend Vercel and mention GitHub Pages or Cloudflare
  Pages as static-site alternatives.

Summarize confirmed decisions as implementation constraints, not slide copy.
Duration, audience, density, style, stage size, navigation, delivery target, and
tech stack should guide the work; render them only if the user explicitly wants
the audience to see them.

For non-trivial decks, prefer an external context document for decisions that
need to survive multi-hour or multi-turn work. This is project memory, not a
control mechanism. Follow the user's preferred location; otherwise use project
docs for deliverable decks and a temp path for small explorations.

Useful grouped prompt:

```text
I recommend treating this as a speaker-led live talk: 10% context, 20% problem
framing, 30% core argument, 25% demo/cases, and 15% method plus closing. If you
want it to be more like a product pitch, technical training, research readout,
or self-reading document, I will change the content ratio and slide density.
```

## Visual Preview Default

When visual direction is unclear, recommend making three real interactive slide
previews before building the full deck. If the user has already supplied a clear
style or strong visual reference, skip multi-direction previews and proceed with
that direction, optionally using a small same-style preview to confirm details.
Use the same planned production stack, stage basis, and harness skeleton where
possible so font loading, stage scaling, navigation, motion, and browser issues
surface early. Use the user's actual title, content, screenshots, or data. Do
not show abstract moodboards or option cards with internal labels.

Default preview set:

1. Sketchboard Emoji as the expressive recommended option, unless clearly
   inappropriate for the audience, brand, or compliance context.
2. A safe/professional option.
3. A content-specific wildcard.

All three previews should share at least one anchor slide so the user can
compare the same content fairly. Provide screenshots and a local server URL.
Each preview should include comparable interaction, beat/state change, and
transition behavior. After the user chooses, summarize a selected theme notes
before full expansion.

Good default phrasing:

```text
I recommend first making three real interactive slide previews using the same
stage and project skeleton: Sketchboard Emoji, professional information design,
and a content-specific wildcard. I will capture screenshots and start a local
server so you can compare them. After you pick a direction, I will write the
selected theme notes and expand the full deck.
```

## Context Ledger

For non-trivial decks, keep a context document when it will reduce drift or make
handoff easier. If the user has a preference, follow it. Otherwise, store
deliverable deck context in project docs such as `docs/context.md`,
`docs/implementation-context.md`, or the handoff note. For a small temporary
exploration, `/tmp` or another agreed temp path is fine. Do not edit
`.gitignore` just for this unless the user asks.

Useful things to track:

- confirmed intake decisions
- narrative plan and content mix
- registry draft
- selected theme notes & Design DNA (including chosen style system, visual guardrails, custom-invented metaphors, and pacing log)
- technology stack, commands, and ports
- harness contracts and route patterns
- style preview links/screenshots and preview check result
- verification status
- delivery target and production URL/PDF path
- open issues, skipped checks, and user decisions

Update after major phases when useful:

- intake / decision snapshot
- narrative plan
- style preview selection
- registry draft
- harness setup
- major content build
- verification
- deployment or export

When verification coverage, delivery status, production URLs, or skipped risks
change materially, prefer updating the context document so later edits do not
depend on chat history alone.

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
visual_language:
delivery_target:
non_goals:
context_document:
```

This snapshot is implementation memory. It is not slide copy.

## Narrative Plan

Before the registry draft, produce a concise narrative/content-mix plan for
non-trivial decks:

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

For non-trivial decks, prefer producing a narrative plan and registry draft
before scene implementation. This is planning guidance, not a polished
deliverable.

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

1. The intake decisions are confirmed or explicitly assumed.
2. Recommended defaults and alternatives were shown for the key decisions.
3. Content orientation, presentation format, duration, and content mix are
   confirmed or explicitly assumed.
4. Context location is clear when the task is long-running or deliverable.
5. Non-trivial decks have a narrative plan before the registry draft.
6. A three-direction interactive visual preview step was offered unless a clear
   style or strong reference already exists.
7. The decision snapshot separates constraints from slide copy.
8. Non-trivial decks have a registry draft with `visible_copy`.
9. Internal alignment details are not being treated as source content.
