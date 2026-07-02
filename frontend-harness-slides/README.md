# Frontend Harness Slides

**[中文说明](README.zh-CN.md)**

Build lively, interactive HTML slide decks that still hold up after multiple
rounds of edits.

This skill helps an agent align on audience, content density, visual style,
motion, navigation, delivery format, and deployment before writing code. It then
treats the deck as a small web app: scenes are addressable, interactions are
testable, screenshots are repeatable, and the final deck can ship as a live site,
a PDF, or both.

> Live demo: explore all 24 visual styles and density levels in the
> [Style Preview Workbench](https://harness-slides-24-styles.vercel.app/).

## What it is good for

- Speaker-led talks that need motion, pacing, and interactive beats.
- Product walkthroughs, teaching decks, and technical explainers.
- High-control slide work where later edits should not quietly damage other
  pages.
- Decks that need both a local preview and a real delivery path, such as online
  deployment or PDF export.

For a tiny one-off static slide, a single HTML file is usually enough. This
skill is for decks where design quality, iteration, and verification matter.

## Visual style gallery

The style system is designed to stay coherent without forcing every page into
the same template. A deck can keep one visual language while changing layouts,
beats, motion, and interaction patterns from scene to scene.

The full catalog contains 24 styles across speaker-led, hybrid, and dense
reading formats. These six examples show the range.

### Minimal keynote

#### [Style 06: Blackboard chalk talk](references/style/minimal-keynote.md#style-06-blackboard-chalk-talk)

Handmade, educational, and reasoning-first. Uses chalk-drawn lines and formulas
on a deep green board.

Topic: *The first principles of quantum computing*

<p align="center">
  <img src="references/style/screenshots/style-06-low.webp" width="32%" alt="Low density: hero formula" />
  <img src="references/style/screenshots/style-06-med.webp" width="32%" alt="Medium density: routed proof" />
  <img src="references/style/screenshots/style-06-high.webp" width="32%" alt="High density: qubit bento" />
</p>

#### [Style 02: Sketch board emoji](references/style/minimal-keynote.md#style-02-sketch-board-emoji)

Warm, approachable, and human-in-the-loop. Uses sticky notes, tape, emoji actors,
and small interactive details.

Topic: *Offline-first sync engine design*

<p align="center">
  <img src="references/style/screenshots/style-02-low.webp" width="32%" alt="Low density: why offline-first" />
  <img src="references/style/screenshots/style-02-med.webp" width="32%" alt="Medium density: sync timeline" />
  <img src="references/style/screenshots/style-02-high.webp" width="32%" alt="High density: strategy bento" />
</p>

### Balanced hybrid

#### [Style 13: Subway map of intent](references/style/balanced-hybrid.md#style-13-transit-flow-subway-map)

Systematic and structured. Represents converging workflows as subway lines and
transfer stations.

Topic: *The lifecycle of a distributed request*

<p align="center">
  <img src="references/style/screenshots/style-13-low.webp" width="32%" alt="Low density: packet journey" />
  <img src="references/style/screenshots/style-13-med.webp" width="32%" alt="Medium density: transit map" />
  <img src="references/style/screenshots/style-13-high.webp" width="32%" alt="High density: schedule bento" />
</p>

#### [Style 16: Debug reaction board](references/style/balanced-hybrid.md#style-16-diagnostic-kanban-board)

Developer-native and diagnostic. Uses neon status badges, terminal surfaces, and
actionable boards.

Topic: *Microservices health self-check*

<p align="center">
  <img src="references/style/screenshots/style-16-low.webp" width="32%" alt="Low density: system ready" />
  <img src="references/style/screenshots/style-16-med.webp" width="32%" alt="Medium density: self-check flow" />
  <img src="references/style/screenshots/style-16-high.webp" width="32%" alt="High density: risk kanban" />
</p>

### Text report

#### [Style 18: Maintainer issue brief](references/style/text-report.md#style-18-developer-ticket-brief)

Clean, structured, and action-oriented. Inspired by modern issue trackers and
code review tools.

Topic: *Post-mortem: connection pool exhaustion*

<p align="center">
  <img src="references/style/screenshots/style-18-low.webp" width="32%" alt="Low density: issue header" />
  <img src="references/style/screenshots/style-18-med.webp" width="32%" alt="Medium density: incident timeline" />
  <img src="references/style/screenshots/style-18-high.webp" width="32%" alt="High density: code review diff" />
</p>

#### [Style 21: Field notes report](references/style/text-report.md#style-21-field-notes-report)

Tactile and observational. Uses ledger paper, charcoal ink, and card grids.

Topic: *Smart home UX field research*

<p align="center">
  <img src="references/style/screenshots/style-21-low.webp" width="32%" alt="Low density: research cover" />
  <img src="references/style/screenshots/style-21-med.webp" width="32%" alt="Medium density: user journey map" />
  <img src="references/style/screenshots/style-21-high.webp" width="32%" alt="High density: observation grid" />
</p>

<p align="center">
  <a href="references/style/preview.md"><b>Explore all 24 styles in the preview guide</b></a>
  <br />
  <a href="https://harness-slides-24-styles.vercel.app/"><b>Try the live style preview workbench</b></a>
</p>

## Why it stays editable

The skill does not ask an agent to make one large, fragile HTML file and hope it
survives feedback. It recommends a small harness around the deck:

- align on style, audience, density, stage size, technology, and delivery before
  building;
- keep scene and beat addresses stable, so a page can be inspected directly;
- render inside a fixed-ratio stage, so content stays inside the slide surface;
- provide a frozen mode for deterministic screenshots and visual checks;
- isolate custom interactions so inputs, drags, and clicks do not accidentally
  trigger slide navigation;
- run focused layout, interaction, screenshot, export, and deployment checks.

## Install

```bash
npx skills add patrick-fu/frontend-harness-slides -g
```

Update later:

```bash
npx skills update -g
```

## How an agent uses it

1. Plan: align on content, audience, presentation format, style direction,
   technology, delivery target, and whether the user wants style previews first.
2. Design: choose a coherent style system, then vary layouts, motion, and
   interaction patterns across scenes.
3. Build: implement stable scenes, a registry, fixed stage scaling, frozen mode,
   keyboard navigation, and event-isolated interactive elements.
4. Verify and ship: run meaningful layout and interaction checks, inspect
   screenshots, preview locally, then deploy online, export PDF, or do both.

## Agent references

For non-trivial deck work, agents should read these references in order:

| File | Purpose |
|---|---|
| `references/01-plan.md` | Intake, style alignment, technology choice, context tracking, and content registry. |
| `references/style/index.md` | Style directions and semantic-to-visual mapping. |
| `references/style/preview.md` | Full style preview guide with 24 styles and density examples. |
| `references/02-design.md` | Style previews, layout variation, navigation, fonts, and assets. |
| `references/03-build.md` | Stable frames, registry, fixed stage, frozen mode, and event isolation. |
| `references/04-verify-and-ship.md` | Visual checks, viewport stress, deployment, PDF export, and handoff. |

## More skills

For more reusable agent skills, see
[Awesome Skills](https://github.com/patrick-fu/awesome-skills).
