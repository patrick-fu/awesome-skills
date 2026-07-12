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
style compares Hero Final Frames from Doubao-Seed-Evolving, GPT 5.6 Sol, and
Claude Opus 4.8, in that left-to-right order. Engineering Whiteboard Explainer
reserves its third slot until a Claude Opus 4.8 Topic is available.

### Minimal keynote

#### [Minimal Product Keynote](references/style/minimal-product-keynote.md)

Premium, focused, and sparse. Uses extreme whitespace, a single central object,
and dramatic type scale for opening claims or product reveals.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/product-keynote.webp" width="32%" alt="Minimal Product Keynote — Doubao-Seed-Evolving — Product Keynote — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/presolar-grain.webp" width="32%" alt="Minimal Product Keynote — GPT 5.6 Sol — Presolar Grain — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/last-feature-cut.webp" width="32%" alt="Minimal Product Keynote — Claude Opus 4.8 — The Last Feature We Cut — Hero Final Frame" />
</p>

#### [Sketch Board Emoji](references/style/sketch-board-emoji.md)

Warm, approachable, and human-in-the-loop. Uses sticky notes, tape, emoji actors,
and small interactive details.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/workshop-board.webp" width="32%" alt="Sketch Board Emoji — Doubao-Seed-Evolving — Workshop Board — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/stadium-wave.webp" width="32%" alt="Sketch Board Emoji — GPT 5.6 Sol — Stadium Wave — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/how-we-named-it.webp" width="32%" alt="Sketch Board Emoji — Claude Opus 4.8 — How We Named It — Hero Final Frame" />
</p>

#### [Interactive Dialogue Stage](references/style/interactive-dialogue-stage.md)

Dialog-focused and theatrical. Stages two roles, systems, or speakers through
dark console surfaces and visible turn-taking.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/dialogue-stage.webp" width="32%" alt="Interactive Dialogue Stage — Doubao-Seed-Evolving — Dialogue Stage — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/vocal-folds.webp" width="32%" alt="Interactive Dialogue Stage — GPT 5.6 Sol — Vocal Folds — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/rubber-duck.webp" width="32%" alt="Interactive Dialogue Stage — Claude Opus 4.8 — The Rubber Duck — Hero Final Frame" />
</p>

#### [Kinetic Type Punchline](references/style/kinetic-type-punchline.md)

Bold, poster-like, and high-energy. Built for memorable section beats,
contrastive claims, and typographic punchlines.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/type-poster.webp" width="32%" alt="Kinetic Type Punchline — Doubao-Seed-Evolving — Type Poster — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/before-a.webp" width="32%" alt="Kinetic Type Punchline — GPT 5.6 Sol — Before A — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/ship-it.webp" width="32%" alt="Kinetic Type Punchline — Claude Opus 4.8 — Ship It — Hero Final Frame" />
</p>

#### [Object Metaphor Hero](references/style/object-metaphor-hero.md)

Tactile and metaphor-led. Turns abstract preparation, planning, or toolkit ideas
into physical objects and organized compartments.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/object-metaphor.webp" width="32%" alt="Object Metaphor Hero — Doubao-Seed-Evolving — Object Hero — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/cocoon-to-cloth.webp" width="32%" alt="Object Metaphor Hero — GPT 5.6 Sol — Cocoon to Cloth — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/onboarding-toolkit.webp" width="32%" alt="Object Metaphor Hero — Claude Opus 4.8 — The Onboarding Toolkit — Hero Final Frame" />
</p>

#### [Blackboard Chalk Talk](references/style/blackboard-chalk-talk.md)

Handmade, educational, and reasoning-first. Uses chalk-drawn lines and formulas
on a deep green board.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/chalk-talk.webp" width="32%" alt="Blackboard Chalk Talk — Doubao-Seed-Evolving — Chalk Talk — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/hearing-path.webp" width="32%" alt="Blackboard Chalk Talk — GPT 5.6 Sol — How Hearing Begins — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/deriving-big-o.webp" width="32%" alt="Blackboard Chalk Talk — Claude Opus 4.8 — Deriving Big-O — Hero Final Frame" />
</p>

#### [Arcade Boss Fight](references/style/arcade-boss-fight.md)

Retro, playful, and risk-aware. Frames technical difficulty as a boss fight,
using HP bars, inventory panels, and pixel UI.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/boss-fight.webp" width="32%" alt="Arcade Boss Fight — Doubao-Seed-Evolving — Boss Fight — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/egg-mimicry.webp" width="32%" alt="Arcade Boss Fight — GPT 5.6 Sol — Egg Mimicry — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/defeating-tech-debt.webp" width="32%" alt="Arcade Boss Fight — Claude Opus 4.8 — Defeating Tech Debt — Hero Final Frame" />
</p>

#### [Spotlight Quote Poster](references/style/spotlight-quote-poster.md)

Dramatic and reflective. Uses stage darkness, radial light, and large quote
typography for pauses, closings, and core philosophy.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/quote-poster.webp" width="32%" alt="Spotlight Quote Poster — Doubao-Seed-Evolving — Quote Poster — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/freedive.webp" width="32%" alt="Spotlight Quote Poster — GPT 5.6 Sol — Freedive — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/on-quitting-well.webp" width="32%" alt="Spotlight Quote Poster — Claude Opus 4.8 — On Quitting Well — Hero Final Frame" />
</p>

### Balanced hybrid

#### [Signal Pipeline Flow](references/style/signal-pipeline-flow.md)

Technical and precise. Shows data, signals, or decisions moving through routed
nodes and structured pipeline stages.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/pipeline.webp" width="32%" alt="Signal Pipeline Flow — Doubao-Seed-Evolving — Pipeline — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/district-heat.webp" width="32%" alt="Signal Pipeline Flow — GPT 5.6 Sol — Second Heat — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/where-request-goes.webp" width="32%" alt="Signal Pipeline Flow — Claude Opus 4.8 — Where the Request Goes — Hero Final Frame" />
</p>

#### [Engineering Whiteboard Explainer](references/style/engineering-whiteboard-explainer.md)

Clear, engineering-led, and diagrammatic. Uses a clean white canvas for beat-driven technical explanation.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/tcp-congestion-control.webp" width="32%" alt="Engineering Whiteboard Explainer — Doubao-Seed-Evolving — TCP Handshake &amp; Congestion — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/water-tower.webp" width="32%" alt="Engineering Whiteboard Explainer — GPT 5.6 Sol — Water Tower — Hero Final Frame" />
  <!-- Claude Opus 4.8 Hero Final Frame pending. -->
</p>

#### [Mechanical Scoring Funnel](references/style/mechanical-scoring-funnel.md)

Energetic and evaluative. Turns filtering, scoring, and prioritization into
lanes, pins, score markers, and active funnel paths.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/scoring-funnel.webp" width="32%" alt="Mechanical Scoring Funnel — Doubao-Seed-Evolving — Scoring Funnel — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/snowflake-branches.webp" width="32%" alt="Mechanical Scoring Funnel — GPT 5.6 Sol — Snowflake Branches — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/triage-the-backlog.webp" width="32%" alt="Mechanical Scoring Funnel — Claude Opus 4.8 — Triage the Backlog — Hero Final Frame" />
</p>

#### [Collaborative Pairing Board](references/style/collaborative-pairing-board.md)

Clean and cooperative. Uses paired columns, role boundaries, and sync points to
explain collaboration between people, teams, or systems.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/pairing-board.webp" width="32%" alt="Collaborative Pairing Board — Doubao-Seed-Evolving — Pairing Board — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/elevator-counterweight.webp" width="32%" alt="Collaborative Pairing Board — GPT 5.6 Sol — Counterweight — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/human-reviews-ai.webp" width="32%" alt="Collaborative Pairing Board — Claude Opus 4.8 — Human Reviews the AI — Hero Final Frame" />
</p>

#### [Studio Mixing Console](references/style/studio-mixing-console.md)

Professional and tactile. Represents parameter tuning, noise filtering, and
trade-off balancing through faders, knobs, and level meters.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/mixing-console.webp" width="32%" alt="Studio Mixing Console — Doubao-Seed-Evolving — Mixing Console — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/tidal-time.webp" width="32%" alt="Studio Mixing Console — GPT 5.6 Sol — Tidal Time — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/tuning-the-model.webp" width="32%" alt="Studio Mixing Console — Claude Opus 4.8 — Tuning the Model — Hero Final Frame" />
</p>

#### [Subway Map of Intent](references/style/subway-map-of-intent.md)

Systematic and structured. Represents converging workflows as subway lines and
transfer stations.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/subway-flow.webp" width="32%" alt="Subway Map of Intent — Doubao-Seed-Evolving — Subway Flow — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/tea-cha-routes.webp" width="32%" alt="Subway Map of Intent — GPT 5.6 Sol — Tea / Cha — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/three-teams-launch.webp" width="32%" alt="Subway Map of Intent — Claude Opus 4.8 — Three Teams, One Launch — Hero Final Frame" />
</p>

#### [Kitchen Prep Station](references/style/kitchen-prep-station.md)

Warm and concrete. Turns raw-to-clean transformation into prep boards, trimmed
ingredients, recipe steps, and plated outputs.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/prep-station.webp" width="32%" alt="Kitchen Prep Station — Doubao-Seed-Evolving — Prep Station — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/cocoa-fermentation.webp" width="32%" alt="Kitchen Prep Station — GPT 5.6 Sol — Cocoa Fermentation — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/raw-logs-to-report.webp" width="32%" alt="Kitchen Prep Station — Claude Opus 4.8 — From Raw Logs to Report — Hero Final Frame" />
</p>

#### [Context Bento Box](references/style/context-bento-box.md)

Compact and organized. Uses compartment grids and layered boxes for handoffs,
multi-category overviews, and context packaging.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/context-bento.webp" width="32%" alt="Context Bento Box — Doubao-Seed-Evolving — Context Bento — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/lichen-partners.webp" width="32%" alt="Context Bento Box — GPT 5.6 Sol — Lichen Partners — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/everything-the-intern-needs.webp" width="32%" alt="Context Bento Box — Claude Opus 4.8 — Everything the Intern Needs — Hero Final Frame" />
</p>

#### [Debug Reaction Board](references/style/debug-reaction-board.md)

Developer-native and diagnostic. Uses neon status badges, terminal surfaces, and
actionable boards.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/debug-board.webp" width="32%" alt="Debug Reaction Board — Doubao-Seed-Evolving — Debug Board — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/acoustic-crack.webp" width="32%" alt="Debug Reaction Board — GPT 5.6 Sol — Acoustic Crack — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/safe-to-deploy.webp" width="32%" alt="Debug Reaction Board — Claude Opus 4.8 — Is It Safe to Deploy? — Hero Final Frame" />
</p>

### Editorial & Print

Styles drawn from editorial design, publication layout, and print typography traditions.

#### [Magazine Masthead](references/style/magazine-masthead.md)

Newsstand cover confidence with a saturated ink field and an enormous fashion serif demanding attention.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/masthead.webp" width="32%" alt="Magazine Masthead — Doubao-Seed-Evolving — Masthead — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/moth-experiment.webp" width="32%" alt="Magazine Masthead — GPT 5.6 Sol — Moth Experiment — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/comeback-issue.webp" width="32%" alt="Magazine Masthead — Claude Opus 4.8 — The Comeback Issue — Hero Final Frame" />
</p>

#### [Solar Biennale Poster](references/style/solar-biennale-poster.md)

Exhibition poster warmth on warm parchment with a slow solar glow and one enormous serif statement.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/biennale-poster.webp" width="32%" alt="Solar Biennale Poster — Doubao-Seed-Evolving — Biennale Poster — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/iron-from-stars.webp" width="32%" alt="Solar Biennale Poster — GPT 5.6 Sol — Iron from Stars — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/festival-slow-ideas.webp" width="32%" alt="Solar Biennale Poster — Claude Opus 4.8 — Festival of Slow Ideas — Hero Final Frame" />
</p>

#### [Warm Editorial Feature](references/style/warm-editorial-feature.md)

Magazine feature spread with cream paper, serif display, and pull-quote rhythm for narrative reading.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/editorial-feature.webp" width="32%" alt="Warm Editorial Feature — Doubao-Seed-Evolving — Editorial Feature — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/oral-to-written.webp" width="32%" alt="Warm Editorial Feature — GPT 5.6 Sol — Oral to Written — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/letter-to-past-self.webp" width="32%" alt="Warm Editorial Feature — Claude Opus 4.8 — A Letter to My Past Self — Hero Final Frame" />
</p>

#### [Scholars' Vellum](references/style/scholars-vellum.md)

Classical manuscript on aged parchment with marginalia and serif authority for deep-dive intellectual content.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/scholar-notes.webp" width="32%" alt="Scholar's Vellum — Doubao-Seed-Evolving — Scholar Notes — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/hidden-text.webp" width="32%" alt="Scholar's Vellum — GPT 5.6 Sol — Hidden Text — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/what-ancients-knew.webp" width="32%" alt="Scholar's Vellum — Claude Opus 4.8 — What the Ancients Knew — Hero Final Frame" />
</p>

#### [Front Page Broadsheet](references/style/front-page-broadsheet.md)

Newspaper front page with multi-column layout and headline hierarchy for packed information delivery.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/broadsheet.webp" width="32%" alt="Front-Page Broadsheet — Doubao-Seed-Evolving — Broadsheet — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/rogue-wave.webp" width="32%" alt="Front-Page Broadsheet — GPT 5.6 Sol — Rogue Wave — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/day-feed-stopped.webp" width="32%" alt="Front-Page Broadsheet — Claude Opus 4.8 — The Day the Feed Stopped — Hero Final Frame" />
</p>

#### [Duotone Session](references/style/duotone-session.md)

Blue Note LP sleeve with a duotone photo and enormous condensed gothic type — cool, disciplined, workmanlike.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/session-poster.webp" width="32%" alt="Duotone Session — Doubao-Seed-Evolving — Session Poster — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/dance-notation.webp" width="32%" alt="Duotone Session — GPT 5.6 Sol — Dance Notation — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/cut-in-one-take.webp" width="32%" alt="Duotone Session — Claude Opus 4.8 — Cut in One Take — Hero Final Frame" />
</p>

### Craft & Cultural Traditions

Styles rooted in craft techniques, cultural visual traditions, and physical media.

#### [Botanical Specimen Plate](references/style/botanical-specimen-plate.md)

Scientific botanical illustration with fine ink lines and Latin annotation for natural-world framing.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/specimen-plate.webp" width="32%" alt="Botanical Specimen Plate — Doubao-Seed-Evolving — Specimen Plate — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/leaf-stomata.webp" width="32%" alt="Botanical Specimen Plate — GPT 5.6 Sol — Leaf Stomata — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/anatomy-of-an-idea.webp" width="32%" alt="Botanical Specimen Plate — Claude Opus 4.8 — Anatomy of an Idea — Hero Final Frame" />
</p>

#### [Woodblock Floating World](references/style/woodblock-floating-world.md)

Japanese ukiyo-e woodblock with floating world composition and sumi-e textures for contemplative visual storytelling.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/woodblock.webp" width="32%" alt="Woodblock Floating-World — Doubao-Seed-Evolving — Woodblock — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/whistled-language.webp" width="32%" alt="Woodblock Floating-World — GPT 5.6 Sol — Whistled Language — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/a-rivers-journey.webp" width="32%" alt="Woodblock Floating-World — Claude Opus 4.8 — A River's Journey — Hero Final Frame" />
</p>

#### [Cyanotype Drafting Table](references/style/cyanotype-drafting-table.md)

Blueprint drafting with cyanotype tones and technical linework for system architecture and engineering diagrams.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/blueprint.webp" width="32%" alt="Cyanotype Drafting Table — Doubao-Seed-Evolving — Blueprint — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/comet-anatomy.webp" width="32%" alt="Cyanotype Drafting Table — GPT 5.6 Sol — Comet Anatomy — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/drawing-a-bridge.webp" width="32%" alt="Cyanotype Drafting Table — Claude Opus 4.8 — Drawing a Bridge — Hero Final Frame" />
</p>

#### [Expedition Screenprint](references/style/expedition-screenprint.md)

Field journal screenprint with stamped layers and map coordinates for exploration and discovery narratives.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/expedition-print.webp" width="32%" alt="Expedition Screenprint — Doubao-Seed-Evolving — Expedition Print — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/saharan-dust.webp" width="32%" alt="Expedition Screenprint — GPT 5.6 Sol — Saharan Dust — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/mapping-unknown-ground.webp" width="32%" alt="Expedition Screenprint — Claude Opus 4.8 — Mapping Unknown Ground — Hero Final Frame" />
</p>

#### [Machine-Age Deco](references/style/machine-age-deco.md)

Art Deco machine age with geometric patterns and stepped forms for grand visions and ambitious roadmaps.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/deco-gala.webp" width="32%" alt="Machine-Age Deco — Doubao-Seed-Evolving — Deco Gala — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/reinforced-concrete.webp" width="32%" alt="Machine-Age Deco — GPT 5.6 Sol — Reinforced Concrete — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/grand-unveiling.webp" width="32%" alt="Machine-Age Deco — Claude Opus 4.8 — The Grand Unveiling — Hero Final Frame" />
</p>

#### [Wabi-Sabi Ceramic](references/style/wabi-sabi-ceramic.md)

Hand-formed ceramic with wabi-sabi irregularity and matte glaze surfaces for craft and natural product framing.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/ceramic-calm.webp" width="32%" alt="Wabi-Sabi Ceramic — Doubao-Seed-Evolving — Ceramic Calm — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/stone-to-soil.webp" width="32%" alt="Wabi-Sabi Ceramic — GPT 5.6 Sol — Stone to Soil — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/beauty-unfinished.webp" width="32%" alt="Wabi-Sabi Ceramic — Claude Opus 4.8 — The Beauty of the Unfinished — Hero Final Frame" />
</p>

#### [Analog Cutout Collage](references/style/analog-cutout-collage.md)

Hand-cut paper collage with torn edges and mixed textures for creative process and idea assembly.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/cutout-collage.webp" width="32%" alt="Analog Cutout Collage — Doubao-Seed-Evolving — Cutout Collage — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/concealed-objects.webp" width="32%" alt="Analog Cutout Collage — GPT 5.6 Sol — Inside the Wall — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/piecing-idea-together.webp" width="32%" alt="Analog Cutout Collage — Claude Opus 4.8 — Piecing the Idea Together — Hero Final Frame" />
</p>

#### [Cassette-Era Packaging](references/style/cassette-era-packaging.md)

Cassette tape J-card design with 80s-90s graphic energy and mixtape layout for music and nostalgia content.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/cassette-pack.webp" width="32%" alt="Cassette-Era Packaging — Doubao-Seed-Evolving — Cassette Pack — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/ice-core-archive.webp" width="32%" alt="Cassette-Era Packaging — GPT 5.6 Sol — Ice-Core Archive — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/greatest-hits-vol1.webp" width="32%" alt="Cassette-Era Packaging — Claude Opus 4.8 — Greatest Hits, Vol. 1 — Hero Final Frame" />
</p>

#### [Riso Print Zine](references/style/riso-print-zine.md)

Risograph zine with limited palette, handmade collage density, and DIY rebellious character.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/riso-zine.webp" width="32%" alt="Riso Print Zine — Doubao-Seed-Evolving — Riso Zine — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/seven-blues.webp" width="32%" alt="Riso Print Zine — GPT 5.6 Sol — Seven Blues — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/make-something-weekly.webp" width="32%" alt="Riso Print Zine — Claude Opus 4.8 — Make Something Weekly — Hero Final Frame" />
</p>

#### [Neo-Brutalist Bulletin](references/style/neo-brutalist-bulletin.md)

Protest poster energy with thick black borders, hard offset shadows, and one high-voltage accent.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/brutalist-bulletin.webp" width="32%" alt="Neo-Brutalist Bulletin — Doubao-Seed-Evolving — Brutalist Bulletin — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/sinking-delta.webp" width="32%" alt="Neo-Brutalist Bulletin — GPT 5.6 Sol — Sinking Delta — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/read-before-merge.webp" width="32%" alt="Neo-Brutalist Bulletin — Claude Opus 4.8 — Read This Before You Merge — Hero Final Frame" />
</p>

#### [Red Wedge Agitprop](references/style/red-wedge-agitprop.md)

Constructivist political poster with red wedge geometry and diagonal dynamism for call-to-action.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/red-wedge.webp" width="32%" alt="Red-Wedge Agitprop — Doubao-Seed-Evolving — Red Wedge — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/pneumatic-post.webp" width="32%" alt="Red-Wedge Agitprop — GPT 5.6 Sol — Pneumatic Post — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/refactor-the-system.webp" width="32%" alt="Red-Wedge Agitprop — Claude Opus 4.8 — Refactor the System — Hero Final Frame" />
</p>

### Contemporary Digital

Modern digital-first styles drawing from current UI trends and platform aesthetics.

#### [Mid-Century Grove](references/style/mid-century-grove.md)

Organic mid-century calm with natural wood tones and gentle curves for sustainability and natural product stories.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/botanical-brand.webp" width="32%" alt="Mid-Century Grove — Doubao-Seed-Evolving — Botanical Brand — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/monarch-migration.webp" width="32%" alt="Mid-Century Grove — GPT 5.6 Sol — Monarch Migration — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/growing-slowly-on-purpose.webp" width="32%" alt="Mid-Century Grove — Claude Opus 4.8 — Growing Slowly on Purpose — Hero Final Frame" />
</p>

#### [After-Hours Luxe](references/style/after-hours-luxe.md)

Dark cocktail lounge luxury with deep jewel tones and gold accents for premium positioning and evening framing.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/after-hours.webp" width="32%" alt="After-Hours Luxe — Doubao-Seed-Evolving — Luxe Reveal — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/urushi-cure.webp" width="32%" alt="After-Hours Luxe — GPT 5.6 Sol — Urushi Cure — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/the-midnight-release.webp" width="32%" alt="After-Hours Luxe — Claude Opus 4.8 — The Midnight Release — Hero Final Frame" />
</p>

#### [Soft Pastel Friendly](references/style/soft-pastel-friendly.md)

Approachable pastel warmth with rounded pill geometry and gentle spring motion for onboarding and community decks.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/friendly-onboard.webp" width="32%" alt="Soft Pastel Friendly — Doubao-Seed-Evolving — Friendly Onboard — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/chrysalis-rebuild.webp" width="32%" alt="Soft Pastel Friendly — GPT 5.6 Sol — Inside a Chrysalis — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/first-week-here.webp" width="32%" alt="Soft Pastel Friendly — Claude Opus 4.8 — Your First Week Here — Hero Final Frame" />
</p>

#### [Retro Windows](references/style/retro-windows.md)

Windows 3.1/95 nostalgia with beveled chrome and system gray palette for developer tooling and retro-tech vibes.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/retro-desktop.webp" width="32%" alt="Retro Windows — Doubao-Seed-Evolving — Retro Desktop — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/voyager-boundary.webp" width="32%" alt="Retro Windows — GPT 5.6 Sol — Voyager Boundary — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/setup-exe.webp" width="32%" alt="Retro Windows — Claude Opus 4.8 — Setup.exe — Hero Final Frame" />
</p>

#### [Objective Swiss Grid](references/style/objective-swiss-grid.md)

Swiss International Style with rigid grid structure and sans-serif clarity for data-heavy reports and analytical frameworks.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/swiss-grid.webp" width="32%" alt="Objective Swiss Grid — Doubao-Seed-Evolving — Swiss Grid — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/bridge-movement.webp" width="32%" alt="Objective Swiss Grid — GPT 5.6 Sol — Bridge Movement — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/anatomy-timetable.webp" width="32%" alt="Objective Swiss Grid — Claude Opus 4.8 — Anatomy of a Timetable — Hero Final Frame" />
</p>

#### [Liquid Glass](references/style/liquid-glass.md)

Apple design language with frosted glass depth and spatial layering for premium tech and Apple-platform content.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/liquid-glass.webp" width="32%" alt="Liquid Glass — Doubao-Seed-Evolving — Liquid Glass — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/safety-glass.webp" width="32%" alt="Liquid Glass — GPT 5.6 Sol — Safety Glass — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/layers-of-a-product.webp" width="32%" alt="Liquid Glass — Claude Opus 4.8 — Layers of a Product — Hero Final Frame" />
</p>

#### [Widescreen Title Card](references/style/widescreen-title-card.md)

Cinematic letterbox title card with film typography and atmospheric stillness for opening titles and grand reveals.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/title-card.webp" width="32%" alt="Widescreen Title Card — Doubao-Seed-Evolving — Title Card — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/whale-fall.webp" width="32%" alt="Widescreen Title Card — GPT 5.6 Sol — Whale Fall — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/chapter-zero.webp" width="32%" alt="Widescreen Title Card — Claude Opus 4.8 — Chapter Zero — Hero Final Frame" />
</p>

### Text report

#### [Research Memo](references/style/research-memo.md)

Calm and authoritative. Uses memo structure, restrained rules, serif hierarchy,
and evidence blocks for credible reading-first decks.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/research-memo.webp" width="32%" alt="Research Memo — Doubao-Seed-Evolving — Research Memo — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/impact-evidence.webp" width="32%" alt="Research Memo — GPT 5.6 Sol — Impact Evidence — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/why-users-churn.webp" width="32%" alt="Research Memo — Claude Opus 4.8 — Why Users Churn — Hero Final Frame" />
</p>

#### [Maintainer Issue Brief](references/style/maintainer-issue-brief.md)

Clean, structured, and action-oriented. Inspired by modern issue trackers and
code review tools.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/issue-brief.webp" width="32%" alt="Maintainer Issue Brief — Doubao-Seed-Evolving — Issue Brief — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/ozone-hole.webp" width="32%" alt="Maintainer Issue Brief — GPT 5.6 Sol — Ozone Hole — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/flaky-test-root-cause.webp" width="32%" alt="Maintainer Issue Brief — Claude Opus 4.8 — Flaky Test, Root Cause — Hero Final Frame" />
</p>

#### [Decision Record](references/style/decision-record.md)

Rigorous and architectural. Frames context, decision, trade-offs, and
verification in an ADR-like document rhythm.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/decision-record.webp" width="32%" alt="Decision Record — Doubao-Seed-Evolving — Decision Record — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/standard-time.webp" width="32%" alt="Decision Record — GPT 5.6 Sol — Standard Time — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/why-we-chose-monorepo.webp" width="32%" alt="Decision Record — Claude Opus 4.8 — Why We Chose Monorepo — Hero Final Frame" />
</p>

#### [Benchmark Matrix](references/style/benchmark-matrix.md)

Analytical and comparative. Prioritizes structured evidence, criteria, metrics,
and table-like comparison surfaces.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/benchmark.webp" width="32%" alt="Benchmark Matrix — Doubao-Seed-Evolving — Benchmark — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/natural-clocks.webp" width="32%" alt="Benchmark Matrix — GPT 5.6 Sol — Natural Clocks — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/build-buy-borrow.webp" width="32%" alt="Benchmark Matrix — Claude Opus 4.8 — Build vs Buy vs Borrow — Hero Final Frame" />
</p>

#### [Field Notes Report](references/style/field-notes-report.md)

Tactile and observational. Uses ledger paper, charcoal ink, and card grids.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/field-notes.webp" width="32%" alt="Field Notes Report — Doubao-Seed-Evolving — Field Notes — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/ancient-sound.webp" width="32%" alt="Field Notes Report — GPT 5.6 Sol — Ancient Sound — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/shadowing-support.webp" width="32%" alt="Field Notes Report — Claude Opus 4.8 — A Day Shadowing Support — Hero Final Frame" />
</p>

#### [Operating Manual](references/style/operating-manual.md)

Procedural and high-contrast. Uses industrial runbook cues, terminal blocks, and
step execution for repeatable operating habits.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/manual.webp" width="32%" alt="Operating Manual — Doubao-Seed-Evolving — Runbook Manual — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/escapement.webp" width="32%" alt="Operating Manual — GPT 5.6 Sol — The Escapement — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/rotate-the-secrets.webp" width="32%" alt="Operating Manual — Claude Opus 4.8 — Rotate the Secrets — Hero Final Frame" />
</p>

#### [Checklist Ledger](references/style/checklist-ledger.md)

Trustworthy and practical. Uses ledger lines, compact rows, and visible checks
for acceptance criteria and final readiness.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/checklist-ledger.webp" width="32%" alt="Checklist Ledger — Doubao-Seed-Evolving — Checklist — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/pigment-without-touch.webp" width="32%" alt="Checklist Ledger — GPT 5.6 Sol — Pigment Without Touch — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/close-the-quarter.webp" width="32%" alt="Checklist Ledger — Claude Opus 4.8 — Close the Quarter — Hero Final Frame" />
</p>

#### [Annotated Source & Diff](references/style/annotated-source-and-diff.md)

Reviewable and transformation-focused. Shows before/after changes, annotations,
and evidence directly in source-like surfaces.

<p align="center">
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/source-diff.webp" width="32%" alt="Annotated Source &amp; Diff — Doubao-Seed-Evolving — Source Diff — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/reading-rosetta.webp" width="32%" alt="Annotated Source &amp; Diff — GPT 5.6 Sol — Reading Rosetta — Hero Final Frame" />
  <img src="https://raw.githubusercontent.com/patrick-fu/frontend-harness-slides-workbench/main/public/showcase/killing-a-god-object.webp" width="32%" alt="Annotated Source &amp; Diff — Claude Opus 4.8 — Killing a God Object — Hero Final Frame" />
</p>

<p align="center">
  <a href="https://frontend-harness-slides-workbench.vercel.app/"><b>🎬 Live demo</b></a>
</p>

## More curated skills

Browse my curated collection of practical agent skills:
[Awesome Skills](https://github.com/patrick-fu/awesome-skills).
