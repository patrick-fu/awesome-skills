# Style Selection Index

This file is the flat style decision surface for agents. Use the catalog below to
shortlist candidate style directions from their tags, then load only the
individual style files you need. There is no category hierarchy: every style is a
peer, classified by tags rather than by folder or section, so nothing implies a
default or a ranking. The catalog is grouped into six visual families for
browsing convenience; use the tags (not the group order) for automated selection.

Agent reference files stay decision-focused; human-facing visual galleries live
in the README.

## Progressive Style Loading

Style selection is progressive:

1. Read this file first.
2. Use the catalog tags to shortlist three preview candidates.
3. Read only the individual style files needed for those candidates.
4. After the user chooses a direction, record the selected direction and its
   guardrails in the Context document / theme notes (see the "Selected Theme
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
| Hierarchy, stack, progression | Layered tower, stepped pyramid, concentric rings, stacked cards → Objective Swiss Grid, Scholars' Vellum, Decision Record |
| Chronology, before-during-after | Timeline track, era bands, flip-card sequence, annotated chronicle → Expedition Screenprint, Field Notes Report, Front Page Broadsheet |
| Metrics dashboard, KPI display | Tile grid, gauge row, scorecard, lede-numeral layout → Benchmark Matrix, Research Memo, Debug Reaction Board |
| Narrative arc, hero's journey | Act structure panels, story spine, journey map, rising-falling curve → Warm Editorial Feature, Woodblock Floating World, Kitchen Prep Station |

Invent new visual metaphors when they serve the material better than the listed
families. Keep the selected style system coherent across slides while varying
layout, scale, and rhythm.

## Visual Pacing

A strong deck alternates density and structure. Keep a pacing log in the theme
notes for non-trivial decks, such as `Low | Medium | Low | High | Medium`.
Adjacent slides can share a layout family when the repetition has a purpose;
otherwise, vary composition enough that the deck feels deliberately paced.

## Quick Decision Tree

Use these shortcuts to jump to candidate styles without scanning every catalog entry.

| I need... | Start with |
|---|---|
| One enormous idea, premium restraint | Minimal Product Keynote, Kinetic Type Punchline, Magazine Masthead |
| Data flowing through a system | Signal Pipeline Flow, Subway Map of Intent, Engineering Whiteboard Explainer, Cyanotype Drafting Table |
| Before/after transformation proof | Annotated Source & Diff, Kitchen Prep Station, Neo-Brutalist Bulletin |
| Technical content for developers | Engineering Whiteboard Explainer, Debug Reaction Board, Maintainer Issue Brief, Operating Manual, Signal Pipeline Flow |
| Formal evidence for async reading | Research Memo, Decision Record, Scholars' Vellum, Objective Swiss Grid |
| Warm hands-on approachable | Sketch Board Emoji, Kitchen Prep Station, Soft Pastel Friendly |
| Bold confrontational statement | Red Wedge Agitprop, Kinetic Type Punchline, Neo-Brutalist Bulletin |
| Editorial print publication | Magazine Masthead, Warm Editorial Feature, Front Page Broadsheet, Solar Biennale Poster |
| Craft handmade authenticity | Riso Print Zine, Analog Cutout Collage, Wabi-Sabi Ceramic, Expedition Screenprint |
| Retro tech nostalgia | Arcade Boss Fight, Retro Windows, Cassette-Era Packaging |
| Dark cinematic atmosphere | Spotlight Quote Poster, Widescreen Title Card, After-Hours Luxe, Duotone Session |
| Multi-category comparison | Benchmark Matrix, Context Bento Box, Objective Swiss Grid |
| Premium product showcase | Minimal Product Keynote, Liquid Glass, After-Hours Luxe, Magazine Masthead |
| Educational teaching | Blackboard Chalk Talk, Engineering Whiteboard Explainer, Sketch Board Emoji, Soft Pastel Friendly |
| Cultural artistic framing | Woodblock Floating World, Scholars' Vellum, Botanical Specimen Plate, Machine-Age Deco |

## Catalog

Each entry carries the tags used to shortlist it and a link to its full style
file. Match the user's occasion, audience, density, formality, and delivery risk
against `mood`, `tone`, `formality`, `density`, `scheme`, `best_for`, and
`avoid_for`. Treat `best_for` as feeling and example fit, not a strict industry
filter, and `avoid_for` as a soft warning, not a veto.

# === Band: Minimal Keynote ===

```yaml
name: Minimal Product Keynote
file: minimal-product-keynote.md
tagline: One idea, enormous, alone in a field of emptiness; restraint reads as luxury.
mood: [premium, calm, composed]
tone: [reverent, focused, confident]
formality: high
density: low
scheme: mixed          # lives at near-white or near-black extremes
best_for: Opening theses, product reveals, section thresholds, single big claims.
avoid_for: Dense evidence, multi-part comparison, or anything needing several facts on screen at once.
aliases: [apple keynote, gallery, extreme minimal, product launch]
motion: calm-slow
typography_voice: serif-display
```

```yaml
name: Sketch Board Emoji
file: sketch-board-emoji.md
tagline: A warm, in-progress workshop board where thinking happens out loud.
mood: [warm-approachable, playful, human]
tone: [candid, collaborative, workshop-like]
formality: low-medium
density: low-medium
scheme: light
best_for: Collaboration stories, messy-to-structured journeys, human-in-the-loop workflows.
avoid_for: Formal, regulated, or high-gravitas decks where hand-drawn looseness reads as unserious.
aliases: [sketch, whiteboard, workshop, emoji, hand-drawn]
motion: spring-gentle
typography_voice: handwritten
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
aliases: [dialogue, stage, conversation, two-voice, exchange]
motion: calm-slow
typography_voice: sans-grotesque
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
aliases: [kinetic type, punchline, poster, bold statement, type-driven]
motion: kinetic-punchy
typography_voice: display-condensed
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
aliases: [object metaphor, hero, physical, tangible, craft object]
motion: calm-slow
typography_voice: serif-display
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
aliases: [chalkboard, classroom, teaching, derivation, whiteboard dark]
motion: calm-slow
typography_voice: handwritten
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
aliases: [arcade, retro game, boss fight, 8-bit, pixel art]
motion: energetic-fluid
typography_voice: display-condensed
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
aliases: [spotlight, quote, poster, dark stage, reflective]
motion: calm-slow
typography_voice: serif-display
```

# === Band: Balanced Hybrid ===

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
aliases: [pipeline, data flow, system map, routing, technical diagram]
motion: energetic-fluid
typography_voice: mono-technical
```

```yaml
name: Engineering Whiteboard Explainer
file: engineering-whiteboard-explainer.md
tagline: A clean white engineering canvas for beat-driven technical explanation.
mood: [clear, engineering-led, explanatory]
tone: [technical, candid, diagrammatic]
formality: medium
density: medium-high
scheme: light
best_for: Technical talks, architecture walkthroughs, workflow methods, system mechanisms.
avoid_for: Warm workshop collaboration, formal reports, pure issue tracking, or artistic sketch decks.
aliases: [engineering whiteboard, white canvas, technical explainer, hand-written diagram, beat-driven explainer]
motion: spring-gentle
typography_voice: handwritten
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
aliases: [funnel, scoring, mechanical, filter, categorization]
motion: energetic-fluid
typography_voice: sans-grotesque
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
aliases: [pairing, collaboration, board, two-column, sync]
motion: minimal
typography_voice: sans-grotesque
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
aliases: [mixing console, studio, faders, audio, trade-offs]
motion: minimal
typography_voice: mono-technical
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
aliases: [subway map, transit, journey, stations, convergence]
motion: minimal
typography_voice: sans-grotesque
```

```yaml
name: Kitchen Prep Station
file: kitchen-prep-station.md
tagline: A warm prep station turning raw input into a plated result.
mood: [warm-approachable, concrete, hands-on]
tone: [friendly, tactile, inviting]
formality: medium-low
density: medium
scheme: light
best_for: Raw-to-clean transformations, pre-processing, step-by-step refinement.
avoid_for: Formal technical governance or pure data.
aliases: [kitchen, prep station, cooking, transformation, ingredients]
motion: spring-gentle
typography_voice: mixed-voice
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
aliases: [bento box, context, compartments, organized, compact]
motion: minimal
typography_voice: sans-grotesque
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
aliases: [debug, diagnostic, terminal, developer, risk]
motion: minimal
typography_voice: mono-technical
```

# === Band: Editorial & Print ===

```yaml
name: Magazine Masthead
file: magazine-masthead.md
tagline: A newsstand cover with saturated ink and an enormous fashion serif demanding attention.
mood: [theatrical, authoritative, unapologetic]
tone: [editorial, published, confident]
formality: high
density: low-medium
scheme: mixed
best_for: Deck covers, section thresholds, big statements, any moment needing editorial gravitas.
avoid_for: Dense evidence pages or several parallel facts — the register turns bombastic.
aliases: [magazine, masthead, editorial cover, newsstand, fashion serif]
motion: kinetic-punchy
typography_voice: serif-display
```

```yaml
name: Solar Biennale Poster
file: solar-biennale-poster.md
tagline: An exhibition poster on warm parchment with a slow solar glow and one enormous serif statement.
mood: [contemplative, warm-elegant, institutionally confident]
tone: [cultural, dignified, slow]
formality: high
density: low
scheme: light
best_for: Cultural programme decks, artistic research, manifesto statements, slow dignified reading.
avoid_for: Dashboard density, tech-forward energy, anything needing to feel fast or urgent.
aliases: [biennale, exhibition poster, solar, parchment, cultural]
motion: calm-slow
typography_voice: serif-display
```

```yaml
name: Warm Editorial Feature
file: warm-editorial-feature.md
tagline: A magazine feature spread on cream paper with serif display and pull-quote rhythm.
mood: [inviting, narrative, warm-elegant]
tone: [editorial, conversational, literary]
formality: medium-high
density: medium
scheme: light
best_for: Story-led decks, long-form features, narrative case studies, interview-driven content.
avoid_for: Pure data dashboards or anything that must read as a UI rather than a publication.
aliases: [editorial feature, magazine spread, cream paper, pull quote, longform]
motion: calm-slow
typography_voice: serif-display
```

```yaml
name: Scholars' Vellum
file: scholars-vellum.md
tagline: A classical manuscript on aged parchment with marginalia and serif authority.
mood: [scholarly, timeless, reverent]
tone: [academic, authoritative, deliberate]
formality: high
density: medium-high
scheme: light
best_for: Historical framing, theoretical arguments, deep-dive intellectual content, classical references.
avoid_for: Fast-paced product launches or casual workshop energy.
aliases: [vellum, manuscript, parchment, classical, academic]
motion: calm-slow
typography_voice: serif-display
```

```yaml
name: Front Page Broadsheet
file: front-page-broadsheet.md
tagline: A newspaper front page with multi-column layout and headline hierarchy.
mood: [informative, urgent, authoritative]
tone: [journalistic, structured, direct]
formality: high
density: high
scheme: light
best_for: News-heavy updates, multi-story briefings, executive morning reads, packed content.
avoid_for: Single-idea keynote moments or emotional storytelling.
aliases: [newspaper, broadsheet, front page, headline, multi-column]
motion: calm-slow
typography_voice: serif-display
```

```yaml
name: Duotone Session
file: duotone-session.md
tagline: A Blue Note LP sleeve with a duotone photo and enormous condensed gothic type.
mood: [cool, disciplined, workmanlike]
tone: [authentic, craft-led, session-like]
formality: medium
density: low-medium
scheme: dark
best_for: Product launches with musical angle, artist spotlights, editorial grit without fashion gloss.
avoid_for: Corporate polish, playful illustrations, data-heavy readouts.
aliases: [duotone, blue note, LP sleeve, vinyl, session]
motion: atmospheric-drift
typography_voice: display-condensed
```

# === Band: Craft & Cultural Traditions ===

```yaml
name: Botanical Specimen Plate
file: botanical-specimen-plate.md
tagline: A scientific botanical illustration with fine ink lines and Latin annotation.
mood: [observational, precise, natural]
tone: [scientific, patient, delicate]
formality: high
density: medium
scheme: light
best_for: Natural world framing, growth narratives, taxonomy, organic systems, patient reading.
avoid_for: High-energy launches or dense data dashboards.
aliases: [botanical, specimen, scientific illustration, plant, taxonomy]
motion: atmospheric-drift
typography_voice: serif-display
```

```yaml
name: Woodblock Floating World
file: woodblock-floating-world.md
tagline: A Japanese ukiyo-e woodblock with floating world composition and sumi-e textures.
mood: [contemplative, flowing, atmospheric]
tone: [artistic, patient, layered]
formality: medium-high
density: medium
scheme: light
best_for: Journey narratives, layered systems, cultural framing, contemplative visual storytelling.
avoid_for: Sharp technical diagrams or fast-paced punchlines.
aliases: [woodblock, ukiyo-e, japanese, floating world, sumi-e]
motion: atmospheric-drift
typography_voice: handwritten
```

```yaml
name: Cyanotype Drafting Table
file: cyanotype-drafting-table.md
tagline: A blueprint drafting table with cyanotype tones and technical linework.
mood: [technical, precise, architectural]
tone: [engineering, clear, systematic]
formality: high
density: medium-high
scheme: light
best_for: System architecture, technical specs, engineering diagrams, blueprint-level planning.
avoid_for: Emotional storytelling or purely visual brand moments.
aliases: [cyanotype, blueprint, drafting, engineering, technical drawing]
motion: minimal
typography_voice: mono-technical
```

```yaml
name: Expedition Screenprint
file: expedition-screenprint.md
tagline: A field journal screenprint with stamped layers and map coordinates.
mood: [adventurous, rugged, documented]
tone: [field-ready, layered, hand-recorded]
formality: medium
density: medium
scheme: light
best_for: Exploration narratives, field research, journey mapping, discovery stories.
avoid_for: Polished corporate decks or precise financial readouts.
aliases: [expedition, screenprint, field journal, map, adventure]
motion: minimal
typography_voice: mixed-voice
```

```yaml
name: Machine-Age Deco
file: machine-age-deco.md
tagline: An Art Deco machine age with geometric patterns and stepped forms.
mood: [optimistic, geometric, luxurious]
tone: [architectural, streamlined, confident]
formality: high
density: medium
scheme: mixed
best_for: Grand visions, infrastructure stories, ambitious roadmaps, 1920s-30s glamour energy.
avoid_for: Casual workshop vibes or hand-drawn looseness.
aliases: [art deco, machine age, geometric, 1920s, streamlined]
motion: calm-slow
typography_voice: serif-display
```

```yaml
name: Wabi-Sabi Ceramic
file: wabi-sabi-ceramic.md
tagline: Hand-formed ceramic with wabi-sabi irregularity and matte glaze surfaces.
mood: [organic, imperfect, grounded]
tone: [tactile, calm, artisanal]
formality: medium-low
density: low-medium
scheme: light
best_for: Craft narratives, natural product framing, mindful or wellness content, handmade stories.
avoid_for: Sharp technical precision or corporate authority moments.
aliases: [clay and ma, wabi sabi, ceramic, craft, handmade, japanese]
motion: spring-gentle
typography_voice: handwritten
```

```yaml
name: Analog Cutout Collage
file: analog-cutout-collage.md
tagline: A hand-cut paper collage with torn edges and mixed textures.
mood: [playful, tactile, assembled]
tone: [handmade, layered, energetic]
formality: low-medium
density: medium-high
scheme: mixed
best_for: Creative process, idea assembly, mixed-media stories, workshop documentation.
avoid_for: Formal executive briefings or pixel-precise technical diagrams.
aliases: [cutout, collage, paper craft, torn edges, handmade]
motion: spring-gentle
typography_voice: handwritten
```

```yaml
name: Cassette-Era Packaging
file: cassette-era-packaging.md
tagline: A cassette tape J-card with 80s-90s graphic energy and mixtape layout.
mood: [nostalgic, energetic, tactile]
tone: [retro, graphic, music-culture]
formality: low-medium
density: medium
scheme: mixed
best_for: Music-related content, nostalgia framing, mixtape-style curation, cultural throwbacks.
avoid_for: Formal corporate reports or minimalist luxury moments.
aliases: [cassette, mixtape, 80s, 90s, J-card]
motion: energetic-fluid
typography_voice: mixed-voice
```

```yaml
name: Riso Print Zine
file: riso-print-zine.md
tagline: A risograph zine with limited palette and handmade collage density.
mood: [playful, handmade, rebellious]
tone: [DIY, warm, slightly chaotic]
formality: low
density: medium-high
scheme: light
best_for: Creative process, community stories, zine-style documentation, youth culture.
avoid_for: Formal executive readouts or precise technical documentation.
aliases: [risograph, zine, riso, handmade print, DIY]
motion: energetic-fluid
typography_voice: mixed-voice
```

```yaml
name: Neo-Brutalist Bulletin
file: neo-brutalist-bulletin.md
tagline: A protest poster taped to concrete with thick black borders and hard offset shadows.
mood: [confident, blunt, irreverent]
tone: [bold, human, unapologetic]
formality: medium-low
density: medium-high
scheme: light
best_for: Product launches, process overviews, comparison decks, dense info with bold character.
avoid_for: Delicate subtlety, reverent minimalism, anything that needs to whisper.
aliases: [neo brutalist, protest poster, concrete, thick borders, offset shadow]
motion: snappy-blocky
typography_voice: display-condensed
```

```yaml
name: Red Wedge Agitprop
file: red-wedge-agitprop.md
tagline: A constructivist political poster with red wedge geometry and diagonal dynamism.
mood: [urgent, bold, ideological]
tone: [agitational, graphic, confrontational]
formality: medium
density: medium
scheme: mixed
best_for: Call-to-action, movement framing, bold thesis statements, activist energy.
avoid_for: Nuanced evidence or balanced comparison — the wedge does not do nuance.
aliases: [red wedge, constructivist, agitprop, political poster, diagonal]
motion: energetic-fluid
typography_voice: display-condensed
```

# === Band: Contemporary Digital ===

```yaml
name: Mid-Century Grove
file: mid-century-grove.md
tagline: Organic mid-century calm with natural wood tones and gentle curves.
mood: [warm-organic, organic, calm]
tone: [natural, grounded, timeless]
formality: medium
density: medium
scheme: light
best_for: Sustainability framing, natural product stories, calm authority, organic systems.
avoid_for: High-energy tech launches or sharp industrial aesthetics.
aliases: [mid-century, organic modern, wood tones, eames, scandinavian]
motion: atmospheric-drift
typography_voice: sans-grotesque
```

```yaml
name: After-Hours Luxe
file: after-hours-luxe.md
tagline: A dark cocktail lounge with deep jewel tones, gold accents, and velvet confidence.
mood: [sophisticated, indulgent, intimate]
tone: [luxurious, nocturnal, polished]
formality: high
density: low-medium
scheme: dark
best_for: Premium positioning, evening events, exclusive framing, sophisticated brand moments.
avoid_for: Daytime casual energy or transparent open-source framing.
aliases: [cocktail lounge, jewel tones, gold, velvet, premium dark]
motion: calm-slow
typography_voice: serif-display
```

```yaml
name: Soft Pastel Friendly
file: soft-pastel-friendly.md
tagline: Approachable pastel warmth with rounded pill geometry and gentle spring motion.
mood: [friendly, warm-approachable, unthreatening]
tone: [inviting, gentle, nostalgic]
formality: low-medium
density: medium
scheme: light
best_for: Onboarding flows, community decks, educational walkthroughs, audience-welcoming content.
avoid_for: Institutional gravitas, high-stakes drama, anything demanding austere authority.
aliases: [pastel, soft, friendly, rounded, approachable]
motion: spring-gentle
typography_voice: sans-grotesque
```

```yaml
name: Retro Windows
file: retro-windows.md
tagline: Windows 3.1/95 nostalgia with beveled chrome, system gray palette, and tiled windows.
mood: [nostalgic, familiar, utilitarian]
tone: [retro-OS, boxy, comfortable]
formality: medium
density: medium-high
scheme: light
best_for: Developer tooling stories, nostalgia framing, multi-panel workflows, retro-tech vibes.
avoid_for: Modern minimalist luxury or organic natural aesthetics.
aliases: [windows 95, retro OS, beveled chrome, system gray, tiled]
motion: snappy-blocky
typography_voice: sans-grotesque
```

```yaml
name: Objective Swiss Grid
file: objective-swiss-grid.md
tagline: Swiss International Style with rigid grid structure, sans-serif clarity, and objective order.
mood: [objective, systematic, precise]
tone: [rational, structured, impartial]
formality: high
density: medium
scheme: light
best_for: Data-heavy reports, analytical frameworks, systematic thinking, clear information design.
avoid_for: Emotional storytelling or expressive visual brand moments.
aliases: [swiss grid, international style, helvetica, grid, objective]
motion: snappy-blocky
typography_voice: sans-grotesque
```

```yaml
name: Liquid Glass
file: liquid-glass.md
tagline: Apple design language with frosted glass depth, spatial layering, and refined translucency.
mood: [premium, fluid, refined]
tone: [Apple-native, spatial, polished]
formality: high
density: medium
scheme: mixed
best_for: Product showcases, premium tech framing, Apple-platform content, layered UI metaphors.
avoid_for: Low-budget DIY energy or hand-drawn authenticity claims.
aliases: [liquid glass, frosted glass, apple design, spatial, translucent]
motion: calm-slow
typography_voice: sans-grotesque
```

```yaml
name: Widescreen Title Card
file: widescreen-title-card.md
tagline: A cinematic letterbox title card with film typography and atmospheric stillness.
mood: [epic, atmospheric, cinematic]
tone: [filmic, deliberate, grand]
formality: high
density: low
scheme: dark
best_for: Opening titles, section interludes, grand reveals, cinematic framing moments.
avoid_for: Dense content pages or quick-fire information delivery.
aliases: [cinematic, letterbox, title card, film, widescreen]
motion: calm-slow
typography_voice: serif-display
```

# === Band: Text Report ===

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
aliases: [research memo, brief, evidence, executive summary, async reading]
motion: minimal
typography_voice: sans-grotesque
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
aliases: [maintainer, issue brief, ticket, engineering, tracker]
motion: minimal
typography_voice: mono-technical
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
aliases: [decision record, ADR, trade-offs, architectural, choice]
motion: minimal
typography_voice: sans-grotesque
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
aliases: [benchmark, matrix, comparison, evaluation, scorecard]
motion: minimal
typography_voice: sans-grotesque
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
aliases: [field notes, notebook, observation, hand-recorded, research]
motion: minimal
typography_voice: handwritten
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
aliases: [operating manual, runbook, how-to, steps, command-line]
motion: snappy-blocky
typography_voice: mono-technical
```

```yaml
name: Checklist Ledger
file: checklist-ledger.md
tagline: A plain, trustworthy ledger of readiness checks, all accounted for.
mood: [trustworthy, practical, composed]
tone: [audit, sober, steady]
formality: high
density: high
scheme: light
best_for: Readiness checks, acceptance criteria, final quality checklists.
avoid_for: Expressive storytelling or a single big claim.
aliases: [checklist, ledger, audit, readiness, acceptance]
motion: snappy-blocky
typography_voice: sans-grotesque
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
aliases: [annotated diff, source code, before after, review, code annotation]
motion: minimal
typography_voice: mono-technical
```
