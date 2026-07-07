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
> [dynamic style preset preview](https://frontend-harness-slides-workbench.vercel.app/).
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

The gallery below shows Workbench-backed preset styles across six visual
families: Minimal Keynote, Balanced Hybrid, Editorial & Print, Craft & Cultural
Traditions, Contemporary Digital, and Text Report. The style index may include
additional reference-only directions before a live demo exists. Each showcased
style includes low, medium, and high-density examples.

### Minimal keynote

#### [Minimal Product Keynote](references/style/minimal-product-keynote.md)

Premium, focused, and sparse. Uses extreme whitespace, a single central object,
and dramatic type scale for opening claims or product reveals.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/01-minimal-product-keynote-nova-launch-scene1.webp" width="32%" alt="Minimal Product Keynote — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/01-minimal-product-keynote-nova-launch-scene3.webp" width="32%" alt="Minimal Product Keynote — scene 3: Nova Launch" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/01-minimal-product-keynote-nova-launch-scene5.webp" width="32%" alt="Minimal Product Keynote — scene 5: closing" />
</p>

#### [Sketch Board Emoji](references/style/sketch-board-emoji.md)

Warm, approachable, and human-in-the-loop. Uses sticky notes, tape, emoji actors,
and small interactive details.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/07-sketch-board-emoji-collab-workshop-scene1.webp" width="32%" alt="Sketch Board Emoji — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/07-sketch-board-emoji-collab-workshop-scene3.webp" width="32%" alt="Sketch Board Emoji — scene 3: Collab Workshop" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/07-sketch-board-emoji-collab-workshop-scene5.webp" width="32%" alt="Sketch Board Emoji — scene 5: closing" />
</p>

#### [Interactive Dialogue Stage](references/style/interactive-dialogue-stage.md)

Dialog-focused and theatrical. Stages two roles, systems, or speakers through
dark console surfaces and visible turn-taking.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/04-interactive-dialogue-stage-human-ai-collaboration-scene1.webp" width="32%" alt="Interactive Dialogue Stage — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/04-interactive-dialogue-stage-human-ai-collaboration-scene3.webp" width="32%" alt="Interactive Dialogue Stage — scene 3: Human-AI Collaboration" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/04-interactive-dialogue-stage-human-ai-collaboration-scene5.webp" width="32%" alt="Interactive Dialogue Stage — scene 5: closing" />
</p>

#### [Kinetic Type Punchline](references/style/kinetic-type-punchline.md)

Bold, poster-like, and high-energy. Built for memorable section beats,
contrastive claims, and typographic punchlines.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/06-kinetic-type-punchline-punchline-impact-scene1.webp" width="32%" alt="Kinetic Type Punchline — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/06-kinetic-type-punchline-punchline-impact-scene3.webp" width="32%" alt="Kinetic Type Punchline — scene 3: Punchline Impact" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/06-kinetic-type-punchline-punchline-impact-scene5.webp" width="32%" alt="Kinetic Type Punchline — scene 5: closing" />
</p>

#### [Object Metaphor Hero](references/style/object-metaphor-hero.md)

Tactile and metaphor-led. Turns abstract preparation, planning, or toolkit ideas
into physical objects and organized compartments.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/48-object-metaphor-hero-system-metaphor-scene1.webp" width="32%" alt="Object Metaphor Hero — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/48-object-metaphor-hero-system-metaphor-scene3.webp" width="32%" alt="Object Metaphor Hero — scene 3: System Metaphor" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/48-object-metaphor-hero-system-metaphor-scene5.webp" width="32%" alt="Object Metaphor Hero — scene 5: closing" />
</p>

#### [Blackboard Chalk Talk](references/style/blackboard-chalk-talk.md)

Handmade, educational, and reasoning-first. Uses chalk-drawn lines and formulas
on a deep green board.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/39-blackboard-chalk-talk-chalkboard-derivation-scene1.webp" width="32%" alt="Blackboard Chalk Talk — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/39-blackboard-chalk-talk-chalkboard-derivation-scene3.webp" width="32%" alt="Blackboard Chalk Talk — scene 3: Chalkboard Derivation" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/39-blackboard-chalk-talk-chalkboard-derivation-scene5.webp" width="32%" alt="Blackboard Chalk Talk — scene 5: closing" />
</p>

#### [Arcade Boss Fight](references/style/arcade-boss-fight.md)

Retro, playful, and risk-aware. Frames technical difficulty as a boss fight,
using HP bars, inventory panels, and pixel UI.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/40-arcade-boss-fight-gamified-risk-framing-scene1.webp" width="32%" alt="Arcade Boss Fight — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/40-arcade-boss-fight-gamified-risk-framing-scene3.webp" width="32%" alt="Arcade Boss Fight — scene 3: Gamified Risk Framing" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/40-arcade-boss-fight-gamified-risk-framing-scene5.webp" width="32%" alt="Arcade Boss Fight — scene 5: closing" />
</p>

#### [Spotlight Quote Poster](references/style/spotlight-quote-poster.md)

Dramatic and reflective. Uses stage darkness, radial light, and large quote
typography for pauses, closings, and core philosophy.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/08-spotlight-quote-poster-mission-philosophy-scene1.webp" width="32%" alt="Spotlight Quote Poster — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/08-spotlight-quote-poster-mission-philosophy-scene3.webp" width="32%" alt="Spotlight Quote Poster — scene 3: Mission Philosophy" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/08-spotlight-quote-poster-mission-philosophy-scene5.webp" width="32%" alt="Spotlight Quote Poster — scene 5: closing" />
</p>

### Balanced hybrid

#### [Signal Pipeline Flow](references/style/signal-pipeline-flow.md)

Technical and precise. Shows data, signals, or decisions moving through routed
nodes and structured pipeline stages.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/11-signal-pipeline-flow-data-pipeline-flow-scene1.webp" width="32%" alt="Signal Pipeline Flow — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/11-signal-pipeline-flow-data-pipeline-flow-scene3.webp" width="32%" alt="Signal Pipeline Flow — scene 3: Data Pipeline Flow" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/11-signal-pipeline-flow-data-pipeline-flow-scene5.webp" width="32%" alt="Signal Pipeline Flow — scene 5: closing" />
</p>

#### [Mechanical Scoring Funnel](references/style/mechanical-scoring-funnel.md)

Energetic and evaluative. Turns filtering, scoring, and prioritization into
lanes, pins, score markers, and active funnel paths.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/32-mechanical-scoring-funnel-evaluation-funnel-scoring-scene1.webp" width="32%" alt="Mechanical Scoring Funnel — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/32-mechanical-scoring-funnel-evaluation-funnel-scoring-scene3.webp" width="32%" alt="Mechanical Scoring Funnel — scene 3: Evaluation Funnel Scoring" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/32-mechanical-scoring-funnel-evaluation-funnel-scoring-scene5.webp" width="32%" alt="Mechanical Scoring Funnel — scene 5: closing" />
</p>

#### [Collaborative Pairing Board](references/style/collaborative-pairing-board.md)

Clean and cooperative. Uses paired columns, role boundaries, and sync points to
explain collaboration between people, teams, or systems.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/14-collaborative-pairing-board-cross-team-pairing-scene1.webp" width="32%" alt="Collaborative Pairing Board — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/14-collaborative-pairing-board-cross-team-pairing-scene3.webp" width="32%" alt="Collaborative Pairing Board — scene 3: Cross-Team Pairing" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/14-collaborative-pairing-board-cross-team-pairing-scene5.webp" width="32%" alt="Collaborative Pairing Board — scene 5: closing" />
</p>

#### [Studio Mixing Console](references/style/studio-mixing-console.md)

Professional and tactile. Represents parameter tuning, noise filtering, and
trade-off balancing through faders, knobs, and level meters.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/15-studio-mixing-console-project-roadmap-scene1.webp" width="32%" alt="Studio Mixing Console — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/15-studio-mixing-console-project-roadmap-scene3.webp" width="32%" alt="Studio Mixing Console — scene 3: Project Roadmap" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/15-studio-mixing-console-project-roadmap-scene5.webp" width="32%" alt="Studio Mixing Console — scene 5: closing" />
</p>

#### [Subway Map of Intent](references/style/subway-map-of-intent.md)

Systematic and structured. Represents converging workflows as subway lines and
transfer stations.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/09-subway-map-of-intent-parallel-track-convergence-scene1.webp" width="32%" alt="Subway Map of Intent — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/09-subway-map-of-intent-parallel-track-convergence-scene3.webp" width="32%" alt="Subway Map of Intent — scene 3: Parallel Track Convergence" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/09-subway-map-of-intent-parallel-track-convergence-scene5.webp" width="32%" alt="Subway Map of Intent — scene 5: closing" />
</p>

#### [Kitchen Prep Station](references/style/kitchen-prep-station.md)

Warm and concrete. Turns raw-to-clean transformation into prep boards, trimmed
ingredients, recipe steps, and plated outputs.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/13-kitchen-prep-station-brainstorm-ideation-scene1.webp" width="32%" alt="Kitchen Prep Station — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/13-kitchen-prep-station-brainstorm-ideation-scene3.webp" width="32%" alt="Kitchen Prep Station — scene 3: Brainstorm Ideation" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/13-kitchen-prep-station-brainstorm-ideation-scene5.webp" width="32%" alt="Kitchen Prep Station — scene 5: closing" />
</p>

#### [Context Bento Box](references/style/context-bento-box.md)

Compact and organized. Uses compartment grids and layered boxes for handoffs,
multi-category overviews, and context packaging.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/47-context-bento-box-project-context-scene1.webp" width="32%" alt="Context Bento Box — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/47-context-bento-box-project-context-scene3.webp" width="32%" alt="Context Bento Box — scene 3: Project Context" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/47-context-bento-box-project-context-scene5.webp" width="32%" alt="Context Bento Box — scene 5: closing" />
</p>

#### [Debug Reaction Board](references/style/debug-reaction-board.md)

Developer-native and diagnostic. Uses neon status badges, terminal surfaces, and
actionable boards.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/16-debug-reaction-board-system-diagnostics-scene1.webp" width="32%" alt="Debug Reaction Board — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/16-debug-reaction-board-system-diagnostics-scene3.webp" width="32%" alt="Debug Reaction Board — scene 3: System Diagnostics" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/16-debug-reaction-board-system-diagnostics-scene5.webp" width="32%" alt="Debug Reaction Board — scene 5: closing" />
</p>

### Editorial & Print

Styles drawn from editorial design, publication layout, and print typography traditions.

#### [Magazine Masthead](references/style/magazine-masthead.md)

Newsstand cover confidence with a saturated ink field and an enormous fashion serif demanding attention.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/18-magazine-masthead-creative-intelligence-scene1.webp" width="32%" alt="Magazine Masthead — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/18-magazine-masthead-creative-intelligence-scene3.webp" width="32%" alt="Magazine Masthead — scene 3: Creative Intelligence" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/18-magazine-masthead-creative-intelligence-scene5.webp" width="32%" alt="Magazine Masthead — scene 5: closing" />
</p>

#### [Solar Biennale Poster](references/style/solar-biennale-poster.md)

Exhibition poster warmth on warm parchment with a slow solar glow and one enormous serif statement.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/21-solar-biennale-poster-slow-light-biennale-scene1.webp" width="32%" alt="Solar Biennale Poster — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/21-solar-biennale-poster-slow-light-biennale-scene3.webp" width="32%" alt="Solar Biennale Poster — scene 3: Slow Light Biennale" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/21-solar-biennale-poster-slow-light-biennale-scene5.webp" width="32%" alt="Solar Biennale Poster — scene 5: closing" />
</p>

#### [Warm Editorial Feature](references/style/warm-editorial-feature.md)

Magazine feature spread with cream paper, serif display, and pull-quote rhythm for narrative reading.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/19-warm-editorial-feature-attention-rebellion-scene1.webp" width="32%" alt="Warm Editorial Feature — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/19-warm-editorial-feature-attention-rebellion-scene3.webp" width="32%" alt="Warm Editorial Feature — scene 3: Attention Rebellion" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/19-warm-editorial-feature-attention-rebellion-scene5.webp" width="32%" alt="Warm Editorial Feature — scene 5: closing" />
</p>

#### [Scholars' Vellum](references/style/scholars-vellum.md)

Classical manuscript on aged parchment with marginalia and serif authority for deep-dive intellectual content.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/20-scholars-vellum-nature-of-knowing-scene1.webp" width="32%" alt="Scholars' Vellum — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/20-scholars-vellum-nature-of-knowing-scene3.webp" width="32%" alt="Scholars' Vellum — scene 3: Nature of Knowing" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/20-scholars-vellum-nature-of-knowing-scene5.webp" width="32%" alt="Scholars' Vellum — scene 5: closing" />
</p>

#### [Front Page Broadsheet](references/style/front-page-broadsheet.md)

Newspaper front page with multi-column layout and headline hierarchy for packed information delivery.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/17-front-page-broadsheet-urban-transformation-scene1.webp" width="32%" alt="Front Page Broadsheet — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/17-front-page-broadsheet-urban-transformation-scene3.webp" width="32%" alt="Front Page Broadsheet — scene 3: Urban Transformation" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/17-front-page-broadsheet-urban-transformation-scene5.webp" width="32%" alt="Front Page Broadsheet — scene 5: closing" />
</p>

#### [Duotone Session](references/style/duotone-session.md)

Blue Note LP sleeve with a duotone photo and enormous condensed gothic type — cool, disciplined, workmanlike.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/22-duotone-session-recording-session-scene1.webp" width="32%" alt="Duotone Session — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/22-duotone-session-recording-session-scene3.webp" width="32%" alt="Duotone Session — scene 3: Recording Session" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/22-duotone-session-recording-session-scene5.webp" width="32%" alt="Duotone Session — scene 5: closing" />
</p>

### Craft & Cultural Traditions

Styles rooted in craft techniques, cultural visual traditions, and physical media.

#### [Botanical Specimen Plate](references/style/botanical-specimen-plate.md)

Scientific botanical illustration with fine ink lines and Latin annotation for natural-world framing.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/26-botanical-specimen-plate-botanical-taxonomy-specimens-scene1.webp" width="32%" alt="Botanical Specimen Plate — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/26-botanical-specimen-plate-botanical-taxonomy-specimens-scene3.webp" width="32%" alt="Botanical Specimen Plate — scene 3: Botanical Taxonomy Specimens" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/26-botanical-specimen-plate-botanical-taxonomy-specimens-scene5.webp" width="32%" alt="Botanical Specimen Plate — scene 5: closing" />
</p>

#### [Woodblock Floating World](references/style/woodblock-floating-world.md)

Japanese ukiyo-e woodblock with floating world composition and sumi-e textures for contemplative visual storytelling.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/25-woodblock-floating-world-ukiyo-e-floating-world-scene1.webp" width="32%" alt="Woodblock Floating World — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/25-woodblock-floating-world-ukiyo-e-floating-world-scene3.webp" width="32%" alt="Woodblock Floating World — scene 3: Ukiyo-e Floating World" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/25-woodblock-floating-world-ukiyo-e-floating-world-scene5.webp" width="32%" alt="Woodblock Floating World — scene 5: closing" />
</p>

#### [Cyanotype Drafting Table](references/style/cyanotype-drafting-table.md)

Blueprint drafting with cyanotype tones and technical linework for system architecture and engineering diagrams.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/05-cyanotype-drafting-table-system-architecture-scene1.webp" width="32%" alt="Cyanotype Drafting Table — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/05-cyanotype-drafting-table-system-architecture-scene3.webp" width="32%" alt="Cyanotype Drafting Table — scene 3: System Architecture" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/05-cyanotype-drafting-table-system-architecture-scene5.webp" width="32%" alt="Cyanotype Drafting Table — scene 5: closing" />
</p>

#### [Expedition Screenprint](references/style/expedition-screenprint.md)

Field journal screenprint with stamped layers and map coordinates for exploration and discovery narratives.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/28-expedition-screenprint-public-lands-expedition-scene1.webp" width="32%" alt="Expedition Screenprint — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/28-expedition-screenprint-public-lands-expedition-scene3.webp" width="32%" alt="Expedition Screenprint — scene 3: Public Lands Expedition" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/28-expedition-screenprint-public-lands-expedition-scene5.webp" width="32%" alt="Expedition Screenprint — scene 5: closing" />
</p>

#### [Machine-Age Deco](references/style/machine-age-deco.md)

Art Deco machine age with geometric patterns and stepped forms for grand visions and ambitious roadmaps.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/27-machine-age-deco-flagship-product-launch-scene1.webp" width="32%" alt="Machine-Age Deco — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/27-machine-age-deco-flagship-product-launch-scene3.webp" width="32%" alt="Machine-Age Deco — scene 3: Flagship Product Launch" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/27-machine-age-deco-flagship-product-launch-scene5.webp" width="32%" alt="Machine-Age Deco — scene 5: closing" />
</p>

#### [Wabi-Sabi Ceramic](references/style/wabi-sabi-ceramic.md)

Hand-formed ceramic with wabi-sabi irregularity and matte glaze surfaces for craft and natural product framing.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/03-wabi-sabi-ceramic-craft-philosophy-scene1.webp" width="32%" alt="Wabi-Sabi Ceramic — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/03-wabi-sabi-ceramic-craft-philosophy-scene3.webp" width="32%" alt="Wabi-Sabi Ceramic — scene 3: Craft Philosophy" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/03-wabi-sabi-ceramic-craft-philosophy-scene5.webp" width="32%" alt="Wabi-Sabi Ceramic — scene 5: closing" />
</p>

#### [Analog Cutout Collage](references/style/analog-cutout-collage.md)

Hand-cut paper collage with torn edges and mixed textures for creative process and idea assembly.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/24-analog-cutout-collage-desk-fragments-scene1.webp" width="32%" alt="Analog Cutout Collage — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/24-analog-cutout-collage-desk-fragments-scene3.webp" width="32%" alt="Analog Cutout Collage — scene 3: Desk Fragments" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/24-analog-cutout-collage-desk-fragments-scene5.webp" width="32%" alt="Analog Cutout Collage — scene 5: closing" />
</p>

#### [Cassette-Era Packaging](references/style/cassette-era-packaging.md)

Cassette tape J-card design with 80s-90s graphic energy and mixtape layout for music and nostalgia content.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/29-cassette-era-packaging-retro-audio-catalogue-scene1.webp" width="32%" alt="Cassette-Era Packaging — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/29-cassette-era-packaging-retro-audio-catalogue-scene3.webp" width="32%" alt="Cassette-Era Packaging — scene 3: Retro Audio Catalogue" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/29-cassette-era-packaging-retro-audio-catalogue-scene5.webp" width="32%" alt="Cassette-Era Packaging — scene 5: closing" />
</p>

#### [Riso Print Zine](references/style/riso-print-zine.md)

Risograph zine with limited palette, handmade collage density, and DIY rebellious character.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/23-riso-print-zine-underground-music-scene1.webp" width="32%" alt="Riso Print Zine — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/23-riso-print-zine-underground-music-scene3.webp" width="32%" alt="Riso Print Zine — scene 3: Underground Music" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/23-riso-print-zine-underground-music-scene5.webp" width="32%" alt="Riso Print Zine — scene 5: closing" />
</p>

#### [Neo-Brutalist Bulletin](references/style/neo-brutalist-bulletin.md)

Protest poster energy with thick black borders, hard offset shadows, and one high-voltage accent.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/30-neo-brutalist-bulletin-product-launch-bulletin-scene1.webp" width="32%" alt="Neo-Brutalist Bulletin — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/30-neo-brutalist-bulletin-product-launch-bulletin-scene3.webp" width="32%" alt="Neo-Brutalist Bulletin — scene 3: Product Launch Bulletin" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/30-neo-brutalist-bulletin-product-launch-bulletin-scene5.webp" width="32%" alt="Neo-Brutalist Bulletin — scene 5: closing" />
</p>

#### [Red Wedge Agitprop](references/style/red-wedge-agitprop.md)

Constructivist political poster with red wedge geometry and diagonal dynamism for call-to-action.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/31-red-wedge-agitprop-movement-call-to-action-scene1.webp" width="32%" alt="Red Wedge Agitprop — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/31-red-wedge-agitprop-movement-call-to-action-scene3.webp" width="32%" alt="Red Wedge Agitprop — scene 3: Movement Call to Action" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/31-red-wedge-agitprop-movement-call-to-action-scene5.webp" width="32%" alt="Red Wedge Agitprop — scene 5: closing" />
</p>

### Contemporary Digital

Modern digital-first styles drawing from current UI trends and platform aesthetics.

#### [Mid-Century Grove](references/style/mid-century-grove.md)

Organic mid-century calm with natural wood tones and gentle curves for sustainability and natural product stories.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/35-mid-century-grove-brand-storytelling-scene1.webp" width="32%" alt="Mid-Century Grove — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/35-mid-century-grove-brand-storytelling-scene3.webp" width="32%" alt="Mid-Century Grove — scene 3: Brand Storytelling" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/35-mid-century-grove-brand-storytelling-scene5.webp" width="32%" alt="Mid-Century Grove — scene 5: closing" />
</p>

#### [After-Hours Luxe](references/style/after-hours-luxe.md)

Dark cocktail lounge luxury with deep jewel tones and gold accents for premium positioning and evening framing.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/36-after-hours-luxe-luxury-brand-launch-scene1.webp" width="32%" alt="After-Hours Luxe — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/36-after-hours-luxe-luxury-brand-launch-scene3.webp" width="32%" alt="After-Hours Luxe — scene 3: Luxury Brand Launch" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/36-after-hours-luxe-luxury-brand-launch-scene5.webp" width="32%" alt="After-Hours Luxe — scene 5: closing" />
</p>

#### [Soft Pastel Friendly](references/style/soft-pastel-friendly.md)

Approachable pastel warmth with rounded pill geometry and gentle spring motion for onboarding and community decks.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/12-soft-pastel-friendly-workspace-onboarding-scene1.webp" width="32%" alt="Soft Pastel Friendly — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/12-soft-pastel-friendly-workspace-onboarding-scene3.webp" width="32%" alt="Soft Pastel Friendly — scene 3: Workspace Onboarding" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/12-soft-pastel-friendly-workspace-onboarding-scene5.webp" width="32%" alt="Soft Pastel Friendly — scene 5: closing" />
</p>

#### [Retro Windows](references/style/retro-windows.md)

Windows 3.1/95 nostalgia with beveled chrome and system gray palette for developer tooling and retro-tech vibes.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/34-retro-windows-nostalgic-computing-scene1.webp" width="32%" alt="Retro Windows — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/34-retro-windows-nostalgic-computing-scene3.webp" width="32%" alt="Retro Windows — scene 3: Nostalgic Computing" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/34-retro-windows-nostalgic-computing-scene5.webp" width="32%" alt="Retro Windows — scene 5: closing" />
</p>

#### [Objective Swiss Grid](references/style/objective-swiss-grid.md)

Swiss International Style with rigid grid structure and sans-serif clarity for data-heavy reports and analytical frameworks.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/02-objective-swiss-grid-migration-sequence-scene1.webp" width="32%" alt="Objective Swiss Grid — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/02-objective-swiss-grid-migration-sequence-scene3.webp" width="32%" alt="Objective Swiss Grid — scene 3: Migration Sequence" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/02-objective-swiss-grid-migration-sequence-scene5.webp" width="32%" alt="Objective Swiss Grid — scene 5: closing" />
</p>

#### [Liquid Glass](references/style/liquid-glass.md)

Apple design language with frosted glass depth and spatial layering for premium tech and Apple-platform content.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/33-liquid-glass-museum-collection-showcase-scene1.webp" width="32%" alt="Liquid Glass — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/33-liquid-glass-museum-collection-showcase-scene3.webp" width="32%" alt="Liquid Glass — scene 3: Museum Collection Showcase" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/33-liquid-glass-museum-collection-showcase-scene5.webp" width="32%" alt="Liquid Glass — scene 5: closing" />
</p>

#### [Widescreen Title Card](references/style/widescreen-title-card.md)

Cinematic letterbox title card with film typography and atmospheric stillness for opening titles and grand reveals.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/38-widescreen-title-card-cinematic-title-cards-scene1.webp" width="32%" alt="Widescreen Title Card — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/38-widescreen-title-card-cinematic-title-cards-scene3.webp" width="32%" alt="Widescreen Title Card — scene 3: Cinematic Title Cards" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/38-widescreen-title-card-cinematic-title-cards-scene5.webp" width="32%" alt="Widescreen Title Card — scene 5: closing" />
</p>

### Text report

#### [Research Memo](references/style/research-memo.md)

Calm and authoritative. Uses memo structure, restrained rules, serif hierarchy,
and evidence blocks for credible reading-first decks.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/41-research-memo-model-performance-scene1.webp" width="32%" alt="Research Memo — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/41-research-memo-model-performance-scene3.webp" width="32%" alt="Research Memo — scene 3: Model Performance" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/41-research-memo-model-performance-scene5.webp" width="32%" alt="Research Memo — scene 5: closing" />
</p>

#### [Maintainer Issue Brief](references/style/maintainer-issue-brief.md)

Clean, structured, and action-oriented. Inspired by modern issue trackers and
code review tools.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/43-maintainer-issue-brief-bug-fix-brief-scene1.webp" width="32%" alt="Maintainer Issue Brief — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/43-maintainer-issue-brief-bug-fix-brief-scene3.webp" width="32%" alt="Maintainer Issue Brief — scene 3: Bug Fix Brief" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/43-maintainer-issue-brief-bug-fix-brief-scene5.webp" width="32%" alt="Maintainer Issue Brief — scene 5: closing" />
</p>

#### [Decision Record](references/style/decision-record.md)

Rigorous and architectural. Frames context, decision, trade-offs, and
verification in an ADR-like document rhythm.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/42-decision-record-architecture-decision-scene1.webp" width="32%" alt="Decision Record — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/42-decision-record-architecture-decision-scene3.webp" width="32%" alt="Decision Record — scene 3: Architecture Decision" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/42-decision-record-architecture-decision-scene5.webp" width="32%" alt="Decision Record — scene 5: closing" />
</p>

#### [Benchmark Matrix](references/style/benchmark-matrix.md)

Analytical and comparative. Prioritizes structured evidence, criteria, metrics,
and table-like comparison surfaces.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/10-benchmark-matrix-competitive-benchmark-scene1.webp" width="32%" alt="Benchmark Matrix — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/10-benchmark-matrix-competitive-benchmark-scene3.webp" width="32%" alt="Benchmark Matrix — scene 3: Competitive Benchmark" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/10-benchmark-matrix-competitive-benchmark-scene5.webp" width="32%" alt="Benchmark Matrix — scene 5: closing" />
</p>

#### [Field Notes Report](references/style/field-notes-report.md)

Tactile and observational. Uses ledger paper, charcoal ink, and card grids.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/44-field-notes-report-field-research-scene1.webp" width="32%" alt="Field Notes Report — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/44-field-notes-report-field-research-scene3.webp" width="32%" alt="Field Notes Report — scene 3: Field Research" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/44-field-notes-report-field-research-scene5.webp" width="32%" alt="Field Notes Report — scene 5: closing" />
</p>

#### [Operating Manual](references/style/operating-manual.md)

Procedural and high-contrast. Uses industrial runbook cues, terminal blocks, and
step execution for repeatable operating habits.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/37-operating-manual-industrial-runbook-scene1.webp" width="32%" alt="Operating Manual — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/37-operating-manual-industrial-runbook-scene3.webp" width="32%" alt="Operating Manual — scene 3: Industrial Runbook" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/37-operating-manual-industrial-runbook-scene5.webp" width="32%" alt="Operating Manual — scene 5: closing" />
</p>

#### [Checklist Ledger](references/style/checklist-ledger.md)

Trustworthy and practical. Uses ledger lines, compact rows, and visible checks
for acceptance criteria and final readiness.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/46-checklist-ledger-release-readiness-scene1.webp" width="32%" alt="Checklist Ledger — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/46-checklist-ledger-release-readiness-scene3.webp" width="32%" alt="Checklist Ledger — scene 3: Release Readiness" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/46-checklist-ledger-release-readiness-scene5.webp" width="32%" alt="Checklist Ledger — scene 5: closing" />
</p>

#### [Annotated Source & Diff](references/style/annotated-source-and-diff.md)

Reviewable and transformation-focused. Shows before/after changes, annotations,
and evidence directly in source-like surfaces.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/45-annotated-source-diff-code-refactor-scene1.webp" width="32%" alt="Annotated Source Diff — scene 1: opening" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/45-annotated-source-diff-code-refactor-scene3.webp" width="32%" alt="Annotated Source Diff — scene 3: Code Refactor" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/45-annotated-source-diff-code-refactor-scene5.webp" width="32%" alt="Annotated Source Diff — scene 5: closing" />
</p>

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/"><b>🎬 Live demo</b></a>
</p>

## More curated skills

Browse my curated collection of practical agent skills:
[Awesome Skills](https://github.com/patrick-fu/awesome-skills).
