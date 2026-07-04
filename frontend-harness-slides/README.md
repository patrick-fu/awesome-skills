# Frontend Harness Slides

**[中文说明](README.zh-CN.md)**

Build HTML slide decks with a frontend harness, so the deck can survive real
iteration.

A single-file HTML deck is fine for a quick draft. It gets painful when the deck
grows, when one slide needs careful tuning, or when a CSS, animation, or layout
change quietly breaks another page. This skill is built for that later phase.

The main advantage is not just prettier slides. The harness treats the deck as a
small, testable web app: scenes are addressable, interactions are isolated,
screenshots are repeatable, and the final deck can ship as a live site, a PDF,
or both.

## Live preview

> 🖥️ Try the live Vercel Workbench:
> [dynamic style preset preview](https://frontend-harness-slides-demo.vercel.app/).
> It is the fastest way to see the motion, density, and visual range before
> reading the full catalog.

## Install

✨ Recommended: copy the current page link to your agent and say: `Please install this for me.`

```bash
npx skills add patrick-fu/frontend-harness-slides -g
```

Update later:

```bash
npx skills update -g
```

## Why the harness matters

Most slide generators can produce an attractive first version. The harder part
is keeping a larger deck stable after feedback. `frontend-harness-slides` puts a
small engineering frame around the deck:

- stable scene and beat addresses, so any frame can be opened directly;
- a registry, so tooling can enumerate the deck without scraping visible text;
- a fixed-ratio stage, so slide content stays inside the canvas;
- frozen mode, so screenshots and visual checks are repeatable;
- event-isolated interactions, so clicks, drags, inputs, and tooltips do not
  leak into global navigation;
- meaningful tests and smoke checks, so missing content, overflow, runtime
  errors, and navigation leaks are caught before handoff.

Visual style still matters. The difference is that the style sits on top of a
deck structure that is designed to be edited, tested, deployed, and exported.

## What it is good for

- Speaker-led talks that need motion, pacing, and interactive beats.
- Product walkthroughs, teaching decks, and technical explainers.
- High-control slide work where later edits should not quietly damage other
  pages.
- Decks that need both a local preview and a real delivery path, such as online
  deployment or PDF export.

For a tiny one-off static slide, a single HTML file is usually enough. This
skill is for decks where design quality, iteration, and verification matter.

## Model choice

For visual slide work, model taste matters. I usually recommend starting with
Gemini for stronger frontend aesthetics, then Claude. GPT 5.5 can work too, and
this skill includes guidance that helps it produce better visual results, but in
my own trials it still tends to need more direction than Gemini.

## Typical workflow

1. Plan: align on content, audience, presentation format, style direction,
   technology, delivery target, and whether the user wants style previews first.
2. Design: choose a coherent style system, then vary layouts, motion, and
   interaction patterns across scenes.
3. Build: create stable slide scenes with keyboard navigation, interactive
   elements, repeatable previews, and tests that protect future edits.
4. Verify and ship: run meaningful layout and interaction checks, inspect
   screenshots, preview locally, then deploy online, export PDF, or do both.

## Visual style gallery

The style system is designed to stay coherent without forcing every page into
the same template. A deck can keep one visual language while changing layouts,
beats, motion, and interaction patterns from scene to scene.

The full gallery below shows every style direction across three density bands:
Minimal Keynote, Balanced Hybrid, and Text Report. Each style includes low,
medium, and high-density examples.

### Minimal keynote

#### [Minimal Product Keynote](references/style/minimal-product-keynote.md)

Premium, focused, and sparse. Uses extreme whitespace, a single central object,
and dramatic type scale for opening claims or product reveals.

<p align="center">
  <img src="showcase/style-gallery/minimal-product-keynote-low.webp" width="32%" alt="Low density: product keynote hero" />
  <img src="showcase/style-gallery/minimal-product-keynote-medium.webp" width="32%" alt="Medium density: product keynote structure" />
  <img src="showcase/style-gallery/minimal-product-keynote-high.webp" width="32%" alt="High density: product keynote detail" />
</p>

#### [Sketch Board Emoji](references/style/sketch-board-emoji.md)

Warm, approachable, and human-in-the-loop. Uses sticky notes, tape, emoji actors,
and small interactive details.

<p align="center">
  <img src="showcase/style-gallery/sketch-board-emoji-low.webp" width="32%" alt="Low density: why offline-first" />
  <img src="showcase/style-gallery/sketch-board-emoji-medium.webp" width="32%" alt="Medium density: sync timeline" />
  <img src="showcase/style-gallery/sketch-board-emoji-high.webp" width="32%" alt="High density: strategy bento" />
</p>

#### [Interactive Dialogue Stage](references/style/interactive-dialogue-stage.md)

Dialog-focused and theatrical. Stages two roles, systems, or speakers through
dark console surfaces and visible turn-taking.

<p align="center">
  <img src="showcase/style-gallery/interactive-dialogue-stage-low.webp" width="32%" alt="Low density: dialogue setup" />
  <img src="showcase/style-gallery/interactive-dialogue-stage-medium.webp" width="32%" alt="Medium density: dual console" />
  <img src="showcase/style-gallery/interactive-dialogue-stage-high.webp" width="32%" alt="High density: dialogue transcript" />
</p>

#### [Kinetic Type Punchline](references/style/kinetic-type-punchline.md)

Bold, poster-like, and high-energy. Built for memorable section beats,
contrastive claims, and typographic punchlines.

<p align="center">
  <img src="showcase/style-gallery/kinetic-type-punchline-low.webp" width="32%" alt="Low density: kinetic phrase" />
  <img src="showcase/style-gallery/kinetic-type-punchline-medium.webp" width="32%" alt="Medium density: typographic contrast" />
  <img src="showcase/style-gallery/kinetic-type-punchline-high.webp" width="32%" alt="High density: poster detail" />
</p>

#### [Object Metaphor Hero](references/style/object-metaphor-hero.md)

Tactile and metaphor-led. Turns abstract preparation, planning, or toolkit ideas
into physical objects and organized compartments.

<p align="center">
  <img src="showcase/style-gallery/object-metaphor-hero-low.webp" width="32%" alt="Low density: hero object" />
  <img src="showcase/style-gallery/object-metaphor-hero-medium.webp" width="32%" alt="Medium density: object compartments" />
  <img src="showcase/style-gallery/object-metaphor-hero-high.webp" width="32%" alt="High density: toolkit layout" />
</p>

#### [Blackboard Chalk Talk](references/style/blackboard-chalk-talk.md)

Handmade, educational, and reasoning-first. Uses chalk-drawn lines and formulas
on a deep green board.

<p align="center">
  <img src="showcase/style-gallery/blackboard-chalk-talk-low.webp" width="32%" alt="Low density: hero formula" />
  <img src="showcase/style-gallery/blackboard-chalk-talk-medium.webp" width="32%" alt="Medium density: routed proof" />
  <img src="showcase/style-gallery/blackboard-chalk-talk-high.webp" width="32%" alt="High density: qubit bento" />
</p>

#### [Arcade Boss Fight](references/style/arcade-boss-fight.md)

Retro, playful, and risk-aware. Frames technical difficulty as a boss fight,
using HP bars, inventory panels, and pixel UI.

<p align="center">
  <img src="showcase/style-gallery/arcade-boss-fight-low.webp" width="32%" alt="Low density: battle screen" />
  <img src="showcase/style-gallery/arcade-boss-fight-medium.webp" width="32%" alt="Medium density: arcade progress" />
  <img src="showcase/style-gallery/arcade-boss-fight-high.webp" width="32%" alt="High density: inventory screen" />
</p>

#### [Spotlight Quote Poster](references/style/spotlight-quote-poster.md)

Dramatic and reflective. Uses stage darkness, radial light, and large quote
typography for pauses, closings, and core philosophy.

<p align="center">
  <img src="showcase/style-gallery/spotlight-quote-poster-low.webp" width="32%" alt="Low density: spotlight quote" />
  <img src="showcase/style-gallery/spotlight-quote-poster-medium.webp" width="32%" alt="Medium density: quote context" />
  <img src="showcase/style-gallery/spotlight-quote-poster-high.webp" width="32%" alt="High density: quote poster detail" />
</p>

### Balanced hybrid

#### [Signal Pipeline Flow](references/style/balanced-hybrid.md#signal-pipeline-flow)

Technical and precise. Shows data, signals, or decisions moving through routed
nodes and structured pipeline stages.

<p align="center">
  <img src="showcase/style-gallery/signal-pipeline-flow-low.webp" width="32%" alt="Low density: signal entry" />
  <img src="showcase/style-gallery/signal-pipeline-flow-medium.webp" width="32%" alt="Medium density: routed pipeline" />
  <img src="showcase/style-gallery/signal-pipeline-flow-high.webp" width="32%" alt="High density: system map" />
</p>

#### [Mechanical Scoring Funnel](references/style/balanced-hybrid.md#mechanical-scoring-funnel)

Energetic and evaluative. Turns filtering, scoring, and prioritization into
lanes, pins, score markers, and active funnel paths.

<p align="center">
  <img src="showcase/style-gallery/mechanical-scoring-funnel-low.webp" width="32%" alt="Low density: scoring moment" />
  <img src="showcase/style-gallery/mechanical-scoring-funnel-medium.webp" width="32%" alt="Medium density: funnel lanes" />
  <img src="showcase/style-gallery/mechanical-scoring-funnel-high.webp" width="32%" alt="High density: scoring board" />
</p>

#### [Collaborative Pairing Board](references/style/balanced-hybrid.md#collaborative-pairing-board)

Clean and cooperative. Uses paired columns, role boundaries, and sync points to
explain collaboration between people, teams, or systems.

<p align="center">
  <img src="showcase/style-gallery/collaborative-pairing-board-low.webp" width="32%" alt="Low density: collaboration thesis" />
  <img src="showcase/style-gallery/collaborative-pairing-board-medium.webp" width="32%" alt="Medium density: pairing board" />
  <img src="showcase/style-gallery/collaborative-pairing-board-high.webp" width="32%" alt="High density: sync plan" />
</p>

#### [Studio Mixing Console](references/style/balanced-hybrid.md#studio-mixing-console)

Professional and tactile. Represents parameter tuning, noise filtering, and
trade-off balancing through faders, knobs, and level meters.

<p align="center">
  <img src="showcase/style-gallery/studio-mixing-console-low.webp" width="32%" alt="Low density: master signal" />
  <img src="showcase/style-gallery/studio-mixing-console-medium.webp" width="32%" alt="Medium density: fader rack" />
  <img src="showcase/style-gallery/studio-mixing-console-high.webp" width="32%" alt="High density: console detail" />
</p>

#### [Subway Map of Intent](references/style/balanced-hybrid.md#subway-map-of-intent)

Systematic and structured. Represents converging workflows as subway lines and
transfer stations.

<p align="center">
  <img src="showcase/style-gallery/subway-map-of-intent-low.webp" width="32%" alt="Low density: packet journey" />
  <img src="showcase/style-gallery/subway-map-of-intent-medium.webp" width="32%" alt="Medium density: transit map" />
  <img src="showcase/style-gallery/subway-map-of-intent-high.webp" width="32%" alt="High density: schedule bento" />
</p>

#### [Kitchen Prep Station](references/style/balanced-hybrid.md#kitchen-prep-station)

Warm and concrete. Turns raw-to-clean transformation into prep boards, trimmed
ingredients, recipe steps, and plated outputs.

<p align="center">
  <img src="showcase/style-gallery/kitchen-prep-station-low.webp" width="32%" alt="Low density: prep thesis" />
  <img src="showcase/style-gallery/kitchen-prep-station-medium.webp" width="32%" alt="Medium density: prep board" />
  <img src="showcase/style-gallery/kitchen-prep-station-high.webp" width="32%" alt="High density: recipe detail" />
</p>

#### [Context Bento Box](references/style/balanced-hybrid.md#context-bento-box)

Compact and organized. Uses compartment grids and layered boxes for handoffs,
multi-category overviews, and context packaging.

<p align="center">
  <img src="showcase/style-gallery/context-bento-box-low.webp" width="32%" alt="Low density: bento concept" />
  <img src="showcase/style-gallery/context-bento-box-medium.webp" width="32%" alt="Medium density: bento compartments" />
  <img src="showcase/style-gallery/context-bento-box-high.webp" width="32%" alt="High density: layered bento" />
</p>

#### [Debug Reaction Board](references/style/balanced-hybrid.md#debug-reaction-board)

Developer-native and diagnostic. Uses neon status badges, terminal surfaces, and
actionable boards.

<p align="center">
  <img src="showcase/style-gallery/debug-reaction-board-low.webp" width="32%" alt="Low density: system ready" />
  <img src="showcase/style-gallery/debug-reaction-board-medium.webp" width="32%" alt="Medium density: self-check flow" />
  <img src="showcase/style-gallery/debug-reaction-board-high.webp" width="32%" alt="High density: risk kanban" />
</p>

### Text report

#### [Research Memo](references/style/text-report.md#research-memo)

Calm and authoritative. Uses memo structure, restrained rules, serif hierarchy,
and evidence blocks for credible reading-first decks.

<p align="center">
  <img src="showcase/style-gallery/research-memo-low.webp" width="32%" alt="Low density: research cover" />
  <img src="showcase/style-gallery/research-memo-medium.webp" width="32%" alt="Medium density: research memo" />
  <img src="showcase/style-gallery/research-memo-high.webp" width="32%" alt="High density: evidence page" />
</p>

#### [Maintainer Issue Brief](references/style/text-report.md#maintainer-issue-brief)

Clean, structured, and action-oriented. Inspired by modern issue trackers and
code review tools.

<p align="center">
  <img src="showcase/style-gallery/maintainer-issue-brief-low.webp" width="32%" alt="Low density: issue header" />
  <img src="showcase/style-gallery/maintainer-issue-brief-medium.webp" width="32%" alt="Medium density: incident timeline" />
  <img src="showcase/style-gallery/maintainer-issue-brief-high.webp" width="32%" alt="High density: code review diff" />
</p>

#### [Decision Record](references/style/text-report.md#decision-record)

Rigorous and architectural. Frames context, decision, trade-offs, and
verification in an ADR-like document rhythm.

<p align="center">
  <img src="showcase/style-gallery/decision-record-low.webp" width="32%" alt="Low density: decision title" />
  <img src="showcase/style-gallery/decision-record-medium.webp" width="32%" alt="Medium density: decision record" />
  <img src="showcase/style-gallery/decision-record-high.webp" width="32%" alt="High density: trade-off matrix" />
</p>

#### [Benchmark Matrix](references/style/text-report.md#benchmark-matrix)

Analytical and comparative. Prioritizes structured evidence, criteria, metrics,
and table-like comparison surfaces.

<p align="center">
  <img src="showcase/style-gallery/benchmark-matrix-low.webp" width="32%" alt="Low density: benchmark claim" />
  <img src="showcase/style-gallery/benchmark-matrix-medium.webp" width="32%" alt="Medium density: metric grid" />
  <img src="showcase/style-gallery/benchmark-matrix-high.webp" width="32%" alt="High density: comparison matrix" />
</p>

#### [Field Notes Report](references/style/text-report.md#field-notes-report)

Tactile and observational. Uses ledger paper, charcoal ink, and card grids.

<p align="center">
  <img src="showcase/style-gallery/field-notes-report-low.webp" width="32%" alt="Low density: research cover" />
  <img src="showcase/style-gallery/field-notes-report-medium.webp" width="32%" alt="Medium density: user journey map" />
  <img src="showcase/style-gallery/field-notes-report-high.webp" width="32%" alt="High density: observation grid" />
</p>

#### [Operating Manual](references/style/text-report.md#operating-manual)

Procedural and high-contrast. Uses industrial runbook cues, terminal blocks, and
step execution for repeatable operating habits.

<p align="center">
  <img src="showcase/style-gallery/operating-manual-low.webp" width="32%" alt="Low density: runbook title" />
  <img src="showcase/style-gallery/operating-manual-medium.webp" width="32%" alt="Medium density: command console" />
  <img src="showcase/style-gallery/operating-manual-high.webp" width="32%" alt="High density: procedure detail" />
</p>

#### [Checklist Ledger](references/style/text-report.md#checklist-ledger)

Trustworthy and practical. Uses ledger lines, compact rows, and visible checks
for acceptance criteria and final readiness.

<p align="center">
  <img src="showcase/style-gallery/checklist-ledger-low.webp" width="32%" alt="Low density: readiness claim" />
  <img src="showcase/style-gallery/checklist-ledger-medium.webp" width="32%" alt="Medium density: audit checklist" />
  <img src="showcase/style-gallery/checklist-ledger-high.webp" width="32%" alt="High density: checklist ledger" />
</p>

#### [Annotated Source & Diff](references/style/text-report.md#annotated-source-diff)

Reviewable and transformation-focused. Shows before/after changes, annotations,
and evidence directly in source-like surfaces.

<p align="center">
  <img src="showcase/style-gallery/annotated-source-diff-low.webp" width="32%" alt="Low density: diff thesis" />
  <img src="showcase/style-gallery/annotated-source-diff-medium.webp" width="32%" alt="Medium density: annotated source" />
  <img src="showcase/style-gallery/annotated-source-diff-high.webp" width="32%" alt="High density: source diff" />
</p>

<p align="center">
  <a href="https://frontend-harness-slides-demo.vercel.app/"><b>🎬 Live demo</b></a>
</p>

## More curated skills

Browse my curated collection of practical agent skills:
[Awesome Skills](https://github.com/patrick-fu/awesome-skills).
