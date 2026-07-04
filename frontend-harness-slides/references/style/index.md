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

<!-- MIGRATION NOTE: The Balanced Hybrid and Text Report directions are being
migrated into this flat, tagged catalog. Until their per-style files exist,
shortlist and read those directions from the current combined files
`balanced-hybrid.md` and `text-report.md`. -->
