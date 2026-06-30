# Style Presets

Use this when the user asks for visual style ideas, gives only a vague aesthetic
direction, or wants preset inspiration before the deck is built.

Presets are starting points, not templates. Use them to create a deck-specific
visual direction, then confirm the direction with the user. Do not copy another
project's template implementation or demo content.

Reference source: several presets below are abstracted from
[`zarazhangrui/frontend-slides`](https://github.com/zarazhangrui/frontend-slides),
especially its style presets and bold template metadata. Treat those as
inspiration, not as a dependency.

## How To Use

- Offer a small set of contrasting directions, usually 3 options, instead of
  showing all presets.
- Match the options to the user's deck mode, audience, density, and motion
  preference.
- Explain the recommendation in plain text and ask the user to confirm, adjust,
  or reject it before implementation.
- Never render preset names, option labels, internal notes, or source paths on
  the slide surface. The preview should look like a real first slide from the
  user's deck.
- Preserve the harness contracts: fixed stage, stable frames, frozen states,
  interaction checks, and visual verification.

## Presentation Presets

Use these for live talks, sharing decks, demos, product-launch/keynote moments,
and decks that should feel energetic.

### 1. Sketchboard Emoji

**Best for:** live explanations, teaching, workflow demos, AI tooling stories,
and talks that benefit from a human, playful voice.

**Visual language:** black/white/gray sketchbook surface, simple linework,
large hand-drawn arrows, loose boxes, and enlarged emoji used as actors or
objects. Emoji should behave like visual components, not inline punctuation.
Use them for robots, people, devices, emotions, and simple scenes.

**Motion and interaction:** Magic Move-style object continuity, bouncing or
wobbling emoji, flowing arrows, click-to-expand notes, hover emphasis, and
local click feedback that does not advance the slide.

**Avoid when:** the deck must feel institutional, legally formal, or visually
neutral across many machines. System emoji can render differently; use a
consistent checked-in emoji asset set when visual baselines must be stable.

### 2. Neo-Grid Demo Board

**Best for:** product launches, technical keynotes, data comparisons, process
flows, and live step-by-step explanations.

**Visual language:** strict 12-by-8 block grid, paper/black/neon-yellow panel
system, uppercase display type, mono labels, and editorial poster density. Each
panel can become a stable scene beat.

**Motion and interaction:** Magic Move cell migration, panel zoom, state
replacement, progressive grid reveal, and click feedback on individual blocks.

**Avoid when:** the deck needs warmth, soft emotional storytelling, natural
imagery, or quiet institutional restraint.

### 3. BlockFrame Product Demo

**Best for:** SaaS demos, feature launches, comparison tables, creative pitches,
and decks that should feel fresh, graphic, and product-led.

**Visual language:** neobrutalist 4px black borders, hard offset shadows,
square cards, candy-color blocks, tilted stickers, and high-density feature
grids.

**Motion and interaction:** card pop-ins, press states, shadow lift, status-card
flips, feature upgrades, emoji labels, and click-triggered emphasis that stays
inside the current scene.

**Avoid when:** the deck must feel legally formal, regulated, sober, or
traditionally executive.

### 4. Sakura Product Catalogue

**Best for:** hardware/tool demos, spec walkthroughs, product catalogue-style
launches, creative technology, and tactile product storytelling.

**Visual language:** vintage Japanese cassette-package mood, cream paper,
diagonal color ribbons, condensed display type, spec checkboxes, product cards,
stamps, seals, and equalizer-like bars.

**Motion and interaction:** spec rows lighting up, checkbox state changes,
product cards entering in sequence, equalizer bars growing, and stamp/seal
emphasis beats.

**Avoid when:** the deck needs a neutral corporate voice, minimalist restraint,
or a style that does not imply product packaging.

## Static Information Presets

Use these for reading-first decks, executive updates, reports, research
synthesis, or high-density text/data where polish matters but theatrical motion
should stay controlled.

### 5. Blue Professional

**Best for:** B2B SaaS, advisory updates, investor reports, internal reviews,
and executive decks that need to look modern without feeling stiff.

**Visual language:** warm cream base, single cobalt accent, clean sans type,
soft tinted cards, pill labels, clear data hierarchy, and restrained chart
emphasis.

**Motion and interaction:** smooth card reflow, staged metric reveals, subtle
hover affordances on cards, click-to-expand supporting detail, and simple dot
navigation for non-linear review.

**Avoid when:** the deck should feel experimental, handmade, playful, or
deliberately raw.

### 6. Monochrome Ledger

**Best for:** research synthesis, white papers, academic/policy briefs, user
research readouts, bilingual reports, and decks where the words are the main
artifact.

**Visual language:** ivory paper, black ink, generous whitespace, thin rules,
light sans headlines, serif quotes, and ledger-like structure.

**Motion and interaction:** quiet page-to-page Magic Move, progressive row or
paragraph reveals, gentle underline or rule growth, and minimal hover feedback
for cited evidence.

**Avoid when:** the user wants visual heat, color-led storytelling, or an
obviously entertaining presentation.

### 7. Cobalt Grid

**Best for:** design research, trend reports, architecture/art decks, academic
summaries, and dense indices that should feel printed and precise.

**Visual language:** warm cream canvas, electric cobalt ink, graph-paper grid,
hairline rules, index rows, QR/grid fragments, and disciplined editorial
structure.

**Motion and interaction:** grid-aware Magic Move, rows filling in sequence,
data blocks sliding along grid lines, animated but deterministic arrows, and
dot navigation by section.

**Avoid when:** the deck needs warmth, casual friendliness, or many accent
colors.

### 8. Signal

**Best for:** board presentations, investor updates, policy/legal briefings,
consulting deliverables, and any deck that should feel weighty and credible.

**Visual language:** navy, cream, restrained antique-gold accents, editorial
hairlines, serif-led headings, and flat institutional layouts.

**Motion and interaction:** subtle Magic Move continuity, fade-up evidence
blocks, restrained scale on key numbers, dot navigation for quick review, and
stable chart/table reveals.

**Avoid when:** the deck should feel playful, hot, or highly experimental.

## Choosing A Set

For most decks, propose one safe option, one expressive option, and one wildcard
that responds to the actual content.

- Live demo about AI workflows: Sketchboard Emoji, Neo-Grid Demo Board, Cobalt
  Grid.
- Founder keynote: Neo-Grid Demo Board, Sakura Product Catalogue, Signal.
- Executive operating review: Blue Professional, Signal, Monochrome Ledger.
- Research readout: Monochrome Ledger, Cobalt Grid, Blue Professional.
- Hackathon or developer tool launch: BlockFrame Product Demo, Sketchboard
  Emoji, Neo-Grid Demo Board.

The final choice should come from user confirmation, not from the agent's silent
preference.
