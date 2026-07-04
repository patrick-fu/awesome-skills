# Style Index & Design DNA Methodology

This file is the compact style decision surface for agents. Use it to choose
candidate style directions, then load only the relevant category detail file.
Agent reference files stay decision-focused; human-facing visual galleries live
in the README.

## Progressive Style Loading

Style selection is progressive:

1. Read this file first.
2. Use the compact catalog to shortlist three preview candidates.
3. Read only the category detail files needed for those candidates.
4. After the user chooses a direction, record the selected Design DNA.
5. Let the selected style drive the full deck. Borrowing from another preview is
   a user-visible decision and should be recorded in the Design DNA.

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

A strong deck alternates density and structure. Keep a pacing log in the Design
DNA for non-trivial decks, such as `Low | Medium | Low | High | Medium`.
Adjacent slides can share a layout family when the repetition has a purpose;
otherwise, vary composition enough that the deck feels deliberately paced.

## Compact Style Catalog

### Minimal Keynote

Use these for sparse, presentation-led moments: live talks, openings, section
transitions, and memorable claims.

| Name | Density fit | Tone | Formality | Best for | Less suited for | Visual signature | Motion fit |
|---|---|---|---|---|---|---|---|
| Minimal Product Keynote | Low | Premium, focused | High | Opening thesis, product reveal, big claim | Dense evidence pages | Extreme whitespace, central object, high-scale type | Slow spotlight, subtle object motion |
| Sketch Board Emoji | Low-medium | Warm, workshop-like | Low-medium | Human workflows, collaboration, messy-to-structured stories | Formal regulated decks | Sticky notes, tape, hand-drawn lines, emoji actors | Hand-drawn reveals, playful hover states |
| Interactive Dialogue Stage | Low-medium | Dramatic, conversational | Medium | Human-agent dialogue, clarifying questions, role exchange | Data-heavy reports | Dark stage, speech bubbles, dual consoles | Speaker-to-speaker transitions |
| Kinetic Type Punchline | Low | High-energy, graphic | Medium-low | Section punches, memorable contrast, strong takeaways | Reading-first detail | Massive stacked type, sharp color contrast | Type hits, strike-through replacement |
| Object Metaphor Hero | Low-medium | Tactile, prepared | Medium | Toolkits, preparation, abstract concept simplification | Dense comparison matrices | Physical kit, compartments, hero object | Object assembly, gentle rotation |
| Blackboard Chalk Talk | Low-medium | Educational, reasoning-first | Medium | Principles, formulas, conceptual explanation | Polished corporate reports | Chalkboard, proof marks, hand-drawn diagrams | Chalk-line drawing, proof-step reveal |
| Arcade Boss Fight | Low-medium | Retro, playful | Low | Risk framing, recaps, re-engagement | Serious executive readouts | Pixel UI, HP bars, inventory screens | Game-state changes, power-up reveals |
| Spotlight Quote Poster | Low | Dramatic, reflective | Medium-high | Closing statements, philosophical pauses | Procedural explanations | Dark stage, radial spotlight, large quote | Slow fade, spotlight shift |

Read details from `minimal-keynote.md` after shortlisting one of these styles.

### Balanced Hybrid

Use these when the deck should work live and remain readable afterward.

| Name | Density fit | Tone | Formality | Best for | Less suited for | Visual signature | Motion fit |
|---|---|---|---|---|---|---|---|
| Signal Pipeline Flow | Medium | Technical, precise | Medium-high | Architecture, data flow, pipelines | Emotional openers | Dark grid, glowing nodes, routed arrows | Progressive signal routing |
| Mechanical Scoring Funnel | Medium | Energetic, evaluative | Medium | Filtering, prioritization, scoring | Quiet reports | Pinball lanes, score markers, funnel paths | Ball movement, score increments |
| Collaborative Pairing Board | Medium | Clean, cooperative | Medium | Role division, pair workflows, sync points | Highly expressive talks | Split board, avatars, sync timeline | Alternating role reveals |
| Studio Mixing Console | Medium | Professional, tactile | Medium | Parameter tuning, trade-offs, balancing | Sparse keynote claims | Faders, knobs, level meters | Meter movement, knob/fader changes |
| Subway Map of Intent | Medium | Systematic, structured | Medium-high | Multi-track workflows, convergence, milestones | Single emotional claim | Transit lines, transfer stations, route colors | Station-to-station continuity |
| Kitchen Prep Station | Medium | Warm, concrete | Medium-low | Raw-to-clean transformations, refinement | Formal technical governance | Cutting board, prep steps, plated output | Prep-step progression |
| Context Bento Box | Medium-high | Organized, compact | Medium | Handoffs, multi-category overview, context packaging | Minimal keynote beats | Compartment grids, layered boxes | Layer reveal, compartment focus |
| Debug Reaction Board | Medium-high | Developer-native, diagnostic | Medium | Risk assessment, system checks, remediation | Non-technical audiences | Status badges, terminal panels, kanban columns | Status transitions, card expansion |

Read details from `balanced-hybrid.md` after shortlisting one of these styles.

### Text Report

Use these for self-contained, evidence-rich, reading-first decks.

| Name | Density fit | Tone | Formality | Best for | Less suited for | Visual signature | Motion fit |
|---|---|---|---|---|---|---|---|
| Research Memo | High | Calm, authoritative | High | Research findings, executive summaries, evidence | High-energy launches | Memo header, serif hierarchy, clean rules | Gentle section fades |
| Maintainer Issue Brief | High | Actionable, engineering-led | Medium-high | Engineering tasks, PR reviews, handoff specs | Emotional storytelling | Issue header, status badges, checklists, diffs | Checklist reveal, diff emphasis |
| Decision Record | High | Rigorous, architectural | High | Technical decisions, trade-offs, boundaries | Playful workshops | ADR sheet, decision blocks, trade-off matrix | Decision-state transition |
| Benchmark Matrix | High | Analytical, comparative | High | Tool comparison, benchmark evidence | Narrative keynote scenes | Tables, score cards, criteria matrix | Row/column emphasis |
| Field Notes Report | Medium-high | Observational, tactile | Medium | User research, physical setup notes, case studies | Formal legal or finance decks | Notebook paper, margin notes, observation sketches | Note-by-note reveal |
| Operating Manual | High | Commanding, procedural | Medium-high | Runbooks, repeatable habits, command-line guides | Reflective closings | Industrial black/yellow, terminal blocks | Step execution, command output reveal |
| Checklist Ledger | High | Trustworthy, practical | High | Readiness checks, acceptance criteria, quality gates | Expressive storytelling | Ledger lines, checkmarks, compact rows | Check-off progression |
| Annotated Source & Diff | High | Reviewable, transformation-focused | Medium-high | Before/after proof, code or text annotation | Abstract vision slides | Diff panels, highlights, side annotations | Before/after replacement |

Read details from `text-report.md` after shortlisting one of these styles.

## Design DNA Contract

When the user chooses a direction, record:

```text
chosen_direction:
borrow_from_other_previews:
visual_guardrails:
typography:
palette:
layout_families:
motion_vocabulary:
interaction_vocabulary:
annotation_style:
asset_strategy:
density_and_copy_tone:
custom_metaphors:
pacing_log:
```

These notes are project memory. They keep later edits aligned without forcing
every slide into one rigid template.
