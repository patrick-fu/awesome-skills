# Style Selection Index

This file is the flat style decision surface for agents. Use the catalog below to
shortlist candidate style directions from their tags, then load only the
individual style files you need. There is no category hierarchy: every style is a
peer, classified by tags rather than by folder or section, so nothing implies a
default or a ranking.

Agent reference files stay decision-focused; human-facing visual galleries live
in the README.

## Progressive Style Loading

Style selection is progressive:

1. Read this file first.
2. Use the catalog tags to shortlist three preview candidates.
3. Read only the individual style files needed for those candidates.
4. After the user chooses a direction, record the selected direction and its
   guardrails in the `context ledger` / theme notes (see the "Selected Theme
   Notes & Design DNA" section in `../02-design.md`).
5. Let the selected style drive the full deck. Borrowing from another preview is
   a user-visible decision and should be recorded in the theme notes.

Each style file is the full Design DNA for that direction: its aesthetic thesis,
color and type temperament, spatial feel, material, signature gestures, motion
register, and — most importantly — its identity invariants versus its freedoms.
The invariants are what must stay constant to keep the style recognizable; the
freedoms are everything the content is free to change. Treat the style as a
visual system, not one repeated template.

## Default Preview Mix

When style direction is open, recommend three real previews:

| Slot | Selection rule |
|---|---|
| Density-Fit | Choose the direction that best matches the deck's confirmed or inferred density, delivery mode, and audience. |
| Safe | Choose the most readable and delivery-stable direction that still has clear visual character. |
| Wildcard | Choose the strongest content-specific visual thesis, prioritizing semantic fit over catalog balance. |

Each candidate needs a content-grounded reason: the material it supports, the
density it fits, the audience or delivery risk it handles, and the visual thesis
it brings. Keep the three candidates meaningfully distinct in typography,
composition, motion, and visual metaphor.

For formal, executive, regulatory, or reading-first decks, the Safe option
should emphasize clarity, restraint, and information stability. For live talks,
launches, workshops, or expressive decks, the Wildcard can carry a stronger
visual point of view when it improves comprehension.

This is the canonical definition of the preview mix. The plan and design
references point here instead of restating it.

## Semantic-To-Visual Mapping

Start from the content's semantic structure, then choose a spatial idea:

| Content structure | Useful layout family |
|---|---|
| Contrast, comparison, dialogue | Split theatre, diagonal split, dual-console scene |
| Steps, process, flow, pipeline | Routed flow, transit map, timeline, progressive track |
| Core thesis, golden sentence, big claim | Hero metaphor, poster, quote, spotlight object |
| Evidence, categories, checklist | Asymmetric bento, memo blocks, ledger, matrix |
| Trade-offs, balance, cycles | Balance scale, gear mesh, loop, custom topology |

Invent new visual metaphors when they serve the material better than the listed
families. Keep the selected style system coherent across slides while varying
layout, scale, and rhythm.

## Visual Pacing

A strong deck alternates density and structure. Keep a pacing log in the theme
notes for non-trivial decks, such as `Low | Medium | Low | High | Medium`.
Adjacent slides can share a layout family when the repetition has a purpose;
otherwise, vary composition enough that the deck feels deliberately paced.

## Catalog

Each entry carries the tags used to shortlist it and a link to its full style
file. Match the user's occasion, audience, density, formality, and delivery risk
against `mood`, `tone`, `formality`, `density`, `scheme`, `best_for`, and
`avoid_for`. Treat `best_for` as feeling and example fit, not a strict industry
filter, and `avoid_for` as a soft warning, not a veto.

```yaml
name: Minimal Product Keynote
file: minimal-product-keynote.md
tagline: One idea, enormous, alone in a field of emptiness; restraint reads as luxury.
mood: [premium, composed, unhurried]
tone: [reverent, focused, confident]
formality: high
density: low
scheme: mixed          # lives at near-white or near-black extremes
best_for: Opening theses, product reveals, section thresholds, single big claims.
avoid_for: Dense evidence, multi-part comparison, or anything needing several facts on screen at once.
```

```yaml
name: Sketch Board Emoji
file: sketch-board-emoji.md
tagline: A warm, in-progress workshop board where thinking happens out loud.
mood: [warm, playful, human]
tone: [candid, collaborative, workshop-like]
formality: low-medium
density: low-medium
scheme: light
best_for: Collaboration stories, messy-to-structured journeys, human-in-the-loop workflows.
avoid_for: Formal, regulated, or high-gravitas decks where hand-drawn looseness reads as unserious.
```

```yaml
name: Interactive Dialogue Stage
file: interactive-dialogue-stage.md
tagline: A dim stage or console where the drama is a two-voice exchange.
mood: [dramatic, conversational, attentive]
tone: [digital, staged, precise]
formality: medium
density: low-medium
scheme: dark
best_for: Human-agent dialogue, clarifying questions, role exchange, request-and-response stories.
avoid_for: Data-heavy reports or broad multi-topic overviews with no exchange to stage.
```

```yaml
name: Kinetic Type Punchline
file: kinetic-type-punchline.md
tagline: A loud poster where a few massive words are the whole image.
mood: [high-energy, graphic, bold]
tone: [confrontational, punchy, poster-like]
formality: medium-low
density: low
scheme: dark           # deep black or one high-voltage saturated field
best_for: Section punches, hard contrasts, memorable one-liners, waking a room up.
avoid_for: Reading-first detail, nuance, evidence, or anything needing qualification.
```

```yaml
name: Object Metaphor Hero
file: object-metaphor-hero.md
tagline: An abstract idea made tangible as a crafted physical object or kit.
mood: [tactile, prepared, reassuring]
tone: [crafted, considered, concrete]
formality: medium
density: low-medium
scheme: light          # warm material tones
best_for: Toolkits, preparation, readiness, simplifying an abstract concept via a physical metaphor.
avoid_for: Dense side-by-side comparison or pure data with no single tangible metaphor.
```

```yaml
name: Blackboard Chalk Talk
file: blackboard-chalk-talk.md
tagline: A live board where reasoning is derived by hand, stroke by stroke.
mood: [educational, patient, reasoning-first]
tone: [handmade, sincere, studious]
formality: medium
density: low-medium
scheme: dark           # matte chalkboard tone
best_for: Core principles, conceptual formulas, derivations, "why this works" explanations.
avoid_for: Glossy corporate polish, hype, or finished results with no reasoning to show.
```

```yaml
name: Arcade Boss Fight
file: arcade-boss-fight.md
tagline: A retro game screen that reframes difficulty as a boss fight.
mood: [playful, nostalgic, energizing]
tone: [retro, game-native, rebellious]
formality: low
density: low-medium
scheme: dark
best_for: Risk framing, recaps, re-engaging a room after a heavy stretch, making difficulty approachable.
avoid_for: Serious executive readouts or anything needing gravitas and precise tone.
```

```yaml
name: Spotlight Quote Poster
file: spotlight-quote-poster.md
tagline: A dark stage with one lit statement, held for a reflective pause.
mood: [reflective, dramatic, reverent]
tone: [literary, hushed, emotional]
formality: medium-high
density: low
scheme: dark
best_for: Closing statements, guiding philosophies, mission lines, deliberate pauses between sections.
avoid_for: Procedural, explanatory, or data content with steps or evidence to walk through.
```

```yaml
name: Signal Pipeline Flow
file: signal-pipeline-flow.md
tagline: A dark technical map tracing signals through a routed system.
mood: [technical, precise, systematic]
tone: [exact, instrument-like, confident]
formality: medium-high
density: medium
scheme: dark
best_for: System architecture, data flow, pipelines, technical process mapping.
avoid_for: Emotional openers or human stories with no system to route.
```

```yaml
name: Mechanical Scoring Funnel
file: mechanical-scoring-funnel.md
tagline: A colorful machine that filters and scores inputs through lanes.
mood: [energetic, playful, evaluative]
tone: [kinetic, game-like, systematic]
formality: medium
density: medium
scheme: dark
best_for: Categorization, multi-stage filtering, scoring, prioritization.
avoid_for: Quiet reports or reflective moments with nothing to sort or score.
```

```yaml
name: Collaborative Pairing Board
file: collaborative-pairing-board.md
tagline: A clean board where two partners divide work and sync.
mood: [clean, cooperative, professional]
tone: [even-handed, tidy, calm]
formality: medium
density: medium
scheme: light
best_for: Role division, pair workflows, sync points, human-system collaboration.
avoid_for: Highly expressive talks or single-voice claims with no pairing.
```

```yaml
name: Studio Mixing Console
file: studio-mixing-console.md
tagline: A console where balancing trade-offs becomes faders and meters.
mood: [professional, tactile, precise]
tone: [hardware, instrument-like]
formality: medium
density: medium
scheme: dark
best_for: Parameter tuning, multi-factor balancing, noise filtering, trade-offs.
avoid_for: Sparse keynote claims with a single variable and nothing to balance.
```

```yaml
name: Subway Map of Intent
file: subway-map-of-intent.md
tagline: A transit map where separate tracks converge at deliberate stations.
mood: [systematic, calm, structured]
tone: [public-info, orderly, legible]
formality: medium-high
density: medium
scheme: light
best_for: Multi-track workflows, converging processes, milestone mapping.
avoid_for: A single emotional claim with one track and no convergence.
```

```yaml
name: Kitchen Prep Station
file: kitchen-prep-station.md
tagline: A warm prep station turning raw input into a plated result.
mood: [warm, concrete, hands-on]
tone: [friendly, tactile, inviting]
formality: medium-low
density: medium
scheme: light
best_for: Raw-to-clean transformations, pre-processing, step-by-step refinement.
avoid_for: Formal technical governance or pure data.
```

```yaml
name: Context Bento Box
file: context-bento-box.md
tagline: An organized bento where context is neatly compartmentalized.
mood: [organized, compact, considered]
tone: [refined, tidy, premium]
formality: medium
density: medium-high
scheme: dark
best_for: Context structuring, handoff specifications, multi-category overviews.
avoid_for: Sparse keynote beats with a single idea and no compartments.
```

```yaml
name: Debug Reaction Board
file: debug-reaction-board.md
tagline: A diagnostic board that surfaces checks, risks, and uncertainty.
mood: [developer-native, diagnostic, candid]
tone: [terminal, technical, honest]
formality: medium
density: medium-high
scheme: dark
best_for: System diagnostics, risk assessment, readiness checks, remediation.
avoid_for: Non-technical audiences or emotional stories with no checks to show.
```

```yaml
name: Research Memo
file: research-memo.md
tagline: A calm, evidence-first research brief that earns trust by hierarchy.
mood: [calm, authoritative, evidence-first]
tone: [editorial, credible, unhurried]
formality: high
density: high
scheme: light
best_for: Research findings, executive summaries, evidence-led readouts for async reading.
avoid_for: High-energy launches or playful moods.
```

```yaml
name: Maintainer Issue Brief
file: maintainer-issue-brief.md
tagline: A structured ticket where work reads as actionable and reviewable.
mood: [actionable, engineering-led]
tone: [tracker, no-nonsense, tidy]
formality: medium-high
density: high
scheme: light
best_for: Engineering tasks, handoff specs, action items for developers and reviewers.
avoid_for: Emotional storytelling or non-technical audiences.
```

```yaml
name: Decision Record
file: decision-record.md
tagline: A formal record making a choice's context, trade-offs, and verification explicit.
mood: [rigorous, architectural, deliberate]
tone: [documentation, exact, serious]
formality: high
density: high
scheme: light
best_for: Technical decisions, trade-offs, architectural boundaries, the reasoning behind a choice.
avoid_for: Playful workshops or emotional talks.
```

```yaml
name: Benchmark Matrix
file: benchmark-matrix.md
tagline: A clean matrix for fair, legible like-against-like comparison.
mood: [analytical, comparative, even-handed]
tone: [objective, scannable, orderly]
formality: high
density: high
scheme: light
best_for: Tool comparisons, evaluation criteria, data-heavy benchmarks.
avoid_for: Narrative keynote scenes with nothing to compare.
```

```yaml
name: Field Notes Report
file: field-notes-report.md
tagline: A field notebook of grounded, hand-recorded observation.
mood: [observational, tactile, honest]
tone: [notebook, grounded, warm]
formality: medium
density: medium-high
scheme: light
best_for: User-research observations, physical setup notes, tactile case studies.
avoid_for: Formal legal or finance decks.
```

```yaml
name: Operating Manual
file: operating-manual.md
tagline: A high-contrast runbook of clear, numbered, do-this steps.
mood: [commanding, procedural, urgent]
tone: [industrial, terminal, disciplined]
formality: medium-high
density: high
scheme: dark
best_for: Runbooks, repeatable habits, command-line guides, step-by-step how-tos.
avoid_for: Reflective closings or emotional beats.
```

```yaml
name: Checklist Ledger
file: checklist-ledger.md
tagline: A plain, trustworthy ledger of readiness checks, all accounted for.
mood: [trustworthy, practical, restrained]
tone: [audit, sober, steady]
formality: high
density: high
scheme: light
best_for: Readiness checks, acceptance criteria, final quality checklists.
avoid_for: Expressive storytelling or a single big claim.
```

```yaml
name: Annotated Source & Diff
file: annotated-source-and-diff.md
tagline: A before/after diff that proves the value of a change.
mood: [reviewable, precise, transformation-focused]
tone: [reviewer, exact, clear]
formality: medium-high
density: high
scheme: light
best_for: Before/after transformations, diff explanations, code or text annotation.
avoid_for: Abstract vision slides with no concrete change.
```
