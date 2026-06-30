# 01 Plan

Use this before creating or substantially changing a deck. The goal is to turn a
user brief into explicit implementation constraints, a content registry, and a
small visual direction decision before scene code starts.

## Intake Gate

For each important decision, give a recommended default, name credible
alternatives, and ask the user to confirm or adjust. Do not only ask "is my
default OK?"

Minimum decisions:

- **Mode and style**: recommend a direction such as Sketchboard Emoji for a
  lively talk, but offer alternatives such as professional information design,
  tech grid, product-launch, editorial report, or a supplied reference.
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

## Visual Preview Default

When visual direction is unclear, recommend making 1-2 real slide previews in
2-3 contrasting styles before building the full deck. Use the user's actual
title, content, screenshots, or data. Do not show abstract moodboards or option
cards with internal labels.

Good default phrasing:

```text
I recommend first making 1-2 real slide previews in three directions:
Sketchboard Emoji, professional information design, and tech grid. After you
pick a direction, I will expand the full deck. We can skip preview if you want
me to proceed with the recommended style.
```

## Decision Snapshot

Before implementation, write a compact snapshot in chat or project notes:

```text
deck_root:
audience:
talk_duration:
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
```

This snapshot is an implementation contract. It is not slide copy.

## Content Source

Use this section when the user provides a long article, memo, PRD, transcript,
old deck, outline, screenshots, or product captures.

Import is not layout preservation. Treat source material as content and intent,
then rebuild the deck into stable scenes inside the fixed stage.

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

For non-trivial decks, do not start scene implementation before producing a
registry draft. This is a planning gate, not a polished deliverable.

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
3. A visual preview step was offered unless a strong reference already exists.
4. The decision snapshot separates constraints from slide copy.
5. Non-trivial decks have a registry draft with `visible_copy`.
6. Internal alignment details are not being treated as source content.
