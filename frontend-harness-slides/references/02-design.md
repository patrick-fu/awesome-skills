# 02 Design

Use this after the plan is clear and before committing the deck's visual system.
The goal is to choose a style, preview it honestly, select fonts/assets, and
keep slide copy audience-facing.

## Discover By Eye

Most users cannot name the exact style they want; they recognize it when they
see it. When visual direction is unclear, make three real interactive slide
previews in meaningfully different directions. When the user already gives a
clear style, use it directly instead of forcing competing previews.

Preview rules:

- Use the same planned production stack, stage basis, and harness skeleton where
  possible.
- Use the user's real title, product, story, screenshots, or data.
- Render the same anchor slide in all three directions.
- Show actual slide composition, typography, navigation treatment, motion,
  beat/state changes, and interaction.
- Include hover feedback, click feedback or click-to-expand, at least one beat
  reveal/state change, and at least one transition or Magic Move-like continuity
  sample in every direction.
- Start a local server and provide screenshots for comparison.
- Explain options in chat, not on the slide surface.
- Do not render preset names, option labels, workflow notes, file paths, or
  internal requirements on the slide.
- Run a light preview check before asking the user to choose.
- After the user chooses, summarize and store selected theme notes, remove
  preview-only controls/routes that are not part of the final deck, and commit
  the direction into the normal theme mechanism.

Default preview set:

1. Sketchboard Emoji as the expressive recommended option, unless clearly
   inappropriate.
2. Safe/professional.
3. Content-specific wildcard.

Keep to three directions by default unless the user explicitly asks.

## Preview Check

Before asking the user to choose, verify:

- local server starts
- all three directions render the same anchor slide
- screenshots are captured from the same stage/view
- fixed stage is visible and correctly scaled
- no console/runtime errors
- hover target works in each direction
- click/reveal target works in each direction
- at least one beat/state change works in each direction
- at least one transition or Magic Move-like sample works in each direction

## Selected Theme Notes

After the user chooses a preview direction, summarize the selected theme notes
before expanding the full deck:

```text
chosen_direction:
keep:
borrow_from_other_previews:
typography:
colors_and_background:
navigation_treatment:
motion_vocabulary:
interaction_vocabulary:
annotation_style:
asset_or_emoji_strategy:
density_and_copy_tone:
```

For non-trivial decks, prefer recording these notes in the shared context
document, README, handoff note, or theme configuration so the chosen style
survives later edits. Follow the user's preferred documentation location.

## Theme Tokens

Keep recurring visual decisions in a theme layer:

- display font
- body font
- background
- text
- accent
- borders
- radii
- shadows
- chart colors
- navigation markers

CSS variables, design tokens, a context provider, global stylesheet, or
generated theme data are all acceptable. A theme change should not require
editing many unrelated scenes.

## Navigation Design

Navigation should feel like part of the slide composition, not a browser chrome
bolted outside the canvas. Keep it inside the fixed stage and match the visual
language of the chosen style.

When adding an in-stage navigator, prefer a picker-style marker window as the
starting point. Inspired by wheel controls, it shows only a small window of
markers, makes the current marker most prominent, fades or shrinks nearby
markers, and can let click, wheel, trackpad, or touch gestures move through the
sequence. Adapt the form to the style: hand-drawn dots, luminous particles,
quiet editorial ticks, or another matching treatment are all valid. Use simpler
dots, section tabs, or another navigator when they better fit the deck or the
user's preference.

## Style Presets

Presets are inspiration, not templates. Offer a small set of contrasting
directions, usually one safe option, one expressive option, and one wildcard.
Confirm the final direction before full implementation.

### 1. Sketchboard Emoji

**Best for:** live explanations, teaching, workflow demos, AI tooling stories,
and talks that benefit from a human, playful voice.

**Priority:** this is the strongest default recommendation when the user wants a
simple, lively presentation style and has not supplied a stricter brand system.
Treat it as a taste direction, not a fixed template.

**Visual language:** white background, black/white/gray sketchbook surface,
simple linework, hand-drawn arrows, loose boxes, and generous whitespace. Prefer
visual elements over text: use short titles and small supporting labels, not
paragraph-heavy slides.

**Emoji use:** enlarge emoji into scene actors or objects instead of using them
as inline punctuation. Use emoji for robots, people, phones, tools, microphones,
emotions, and small composite scenes. This often feels more natural than stiff
hand-drawn figures.

**Annotations:** explain supporting details with sticky notes, tape labels,
pinned notes, margin scribbles, speech bubbles, callout tags, and highlighted
keywords instead of plain paragraphs. Use quote or "golden sentence" moments
with marker strokes, fluorescent highlighter, circled keywords, underlines, or
handwritten emphasis.

**Navigation:** prefer a subtle right-side vertical navigator in a hand-drawn
style. The active scene can be a slightly larger sketch circle; inactive scenes
can be tiny filled dots. Avoid adding a separate textual page counter on the
canvas unless the user explicitly needs one.

**Interactivity:** treat emoji actors, robots, people, phones, microphones,
sticky notes, and labels as interactive visual objects when useful. Hover can
trigger wobble, scale, rotate, sketch underline, tooltip, or a small note. Click
can expand a sticky note, flip a note, pin an explanation, pulse a highlight, or
show a small callout without advancing the slide.

**Motion:** use Keynote Magic Move-style object continuity, bouncing or wobbling
emoji, flowing arrows, click-to-expand notes, hover emphasis, and local click
feedback. Keep motion lively and varied. Avoid using the same entrance or bounce
on every scene; rotate hops, wobbles, flowing arrows, rotations, sliding phones,
turning robots, nods, and continuity transforms.

**Typeface direction:** use a style-matched handwritten or warm CJK-capable font
when Chinese/Japanese/Korean text appears. Prefer a reliable local or bundled
font setup for deployed decks, with a fallback that still matches the style.

**Avoid when:** the deck must feel institutional, legally formal, or visually
neutral across many machines. Native emoji can render differently; use a
checked-in emoji asset strategy when visual baselines must be stable.

### 2. Neo-Grid Demo Board

**Best for:** product launches, technical keynotes, data comparisons, process
flows, and live step-by-step explanations.

**Visual language:** strict block grid, paper/black/neon-yellow panel system,
uppercase display type, mono labels, and editorial poster density.

**Motion and interaction:** Magic Move cell migration, panel zoom, state
replacement, progressive grid reveal, and click feedback on individual blocks.

**Avoid when:** the deck needs warmth, soft emotional storytelling, natural
imagery, or quiet institutional restraint.

### 3. BlockFrame Product Demo

**Best for:** SaaS demos, feature launches, comparison tables, creative pitches,
and fresh product-led decks.

**Visual language:** neobrutalist black borders, hard offset shadows, square
cards, candy-color blocks, tilted stickers, and dense feature grids.

**Motion and interaction:** card pop-ins, press states, shadow lift, status-card
flips, feature upgrades, emoji labels, and click-triggered emphasis.

**Avoid when:** the deck must feel legally formal, regulated, sober, or
traditionally executive.

### 4. Sakura Product Catalogue

**Best for:** hardware/tool demos, spec walkthroughs, catalogue-style launches,
creative technology, and tactile product storytelling.

**Visual language:** vintage Japanese package mood, cream paper, diagonal color
ribbons, condensed display type, spec checkboxes, product cards, stamps, seals,
and equalizer bars.

**Motion and interaction:** spec rows lighting up, checkbox state changes,
product cards entering in sequence, equalizer bars growing, and stamp/seal
emphasis beats.

**Avoid when:** the deck needs a neutral corporate voice or minimalist
restraint.

### 5. Blue Professional

**Best for:** B2B SaaS, advisory updates, investor reports, internal reviews,
and executive decks that should look modern without feeling stiff.

**Visual language:** warm cream base, cobalt accent, clean sans type, soft
tinted cards, pill labels, clear data hierarchy, and restrained chart emphasis.

**Motion and interaction:** smooth card reflow, staged metric reveals, subtle
hover affordances, click-to-expand supporting detail, and simple dot navigation.

### 6. Monochrome Ledger

**Best for:** research synthesis, white papers, academic/policy briefs, user
research readouts, bilingual reports, and word-led decks.

**Visual language:** ivory paper, black ink, generous whitespace, thin rules,
light sans headlines, serif quotes, and ledger-like structure.

**Motion and interaction:** quiet Magic Move, progressive row or paragraph
reveals, gentle underline/rule growth, and minimal hover feedback for evidence.

### 7. Cobalt Grid

**Best for:** design research, trend reports, architecture/art decks, academic
summaries, and dense indices that should feel printed and precise.

**Visual language:** warm cream canvas, electric cobalt ink, graph-paper grid,
hairline rules, index rows, QR/grid fragments, and editorial structure.

**Motion and interaction:** grid-aware Magic Move, rows filling in sequence,
data blocks sliding along grid lines, deterministic arrows, and dot navigation.

### 8. Signal

**Best for:** board presentations, investor updates, policy/legal briefings,
consulting deliverables, and credible institutional decks.

**Visual language:** navy, cream, restrained antique-gold accents, editorial
hairlines, serif-led headings, and flat institutional layouts.

**Motion and interaction:** subtle Magic Move, fade-up evidence blocks,
restrained scale on key numbers, dot navigation, and stable chart/table reveals.

## Fonts

Choose type as part of the visual direction. It should match the style, cover
the deck's languages, and render reliably in the final handoff.

Rules:

- Do not bundle commercial font files inside this skill.
- In a deck project, prefer the user's licensed font files when they provide
  them and the license allows web embedding/deployment.
- If the user does not provide fonts, use open-source faces from official
  sources.
- For Chinese, Japanese, or Korean text, choose a font family with real CJK
  coverage. Do not use Times New Roman, Helvetica, or another Latin-only face as
  the primary CJK font.
- Bundle delivery-critical fonts with the deck and load them with local
  `@font-face`; do not rely on remote font CDNs for a live talk or final deploy.
- Keep display, body, and mono choices separate.
- Subset large CJK fonts when stable deployed rendering matters and file size is
  excessive.

Useful directions to consider:

- Sans/display faces for modern product or technical decks.
- Serif or editorial faces for report, policy, or reading-first decks.
- Handwritten or warm CJK-capable faces for sketch, teaching, or playful decks.
- System or user-provided fonts when they are more reliable than adding large
  webfont bundles.

Avoid defaulting to Inter, Roboto, Arial, or system-ui when a stronger style
choice is available.

Do a light browser check for important fonts. Package names and CSS entry points
do not guarantee that the loaded font covers every language in the deck. If CJK
text falls back to a system font, make that fallback intentional and acceptable
for the delivery context.

For CJK decks, check font asset size after the first build when bundling fonts.
Large body fonts can dominate the output; a bundled display font plus intentional
system CJK fallback may be better than shipping a huge full font.

## Assets

Use the project's existing asset convention if one exists. For a new deck, group
assets by shared use or scene:

```text
assets/
├── shared/
├── scene-intro/
├── scene-demo/
└── fonts/
```

Rules:

- Use content-based names, not raw exports such as `image001.png`.
- Optimize large photos before committing or deploying.
- Prefer WebP/AVIF for photos when browser support is acceptable.
- Keep logos and diagrams as SVG when they need sharp scaling.
- SVGs that change with theme should use `currentColor` or theme tokens.
- Do not put slide assets inside test artifact folders.
- Avoid relying on remote assets for anything critical unless the delivery context
  explicitly allows network dependence.
- If an asset is visually central, verify it in the browser.

Native emoji are expressive and fast for live decks, but their pixels differ
across iOS, macOS, Android, and Windows. If visual baselines or cross-platform
rendering must be stable, convert important emoji into checked-in SVG or image
assets from an allowed emoji set.

## Components

Use proven libraries for complex chart, code, diagram, icon, or 3D needs, but do
not let libraries break the harness.

| Need | Prefer | Avoid |
|---|---|---|
| Charts | Lightweight SVG/canvas chart library already used by the project. | Screenshot-only charts with unreadable labels. |
| Code | Existing syntax highlighter or a minimal tokenizer. | Runtime editors unless interaction is required. |
| Diagrams | SVG/DOM diagrams with stable labels. | One giant raster diagram. |
| Icons | Existing icon set or a small tree-shakeable SVG library. | Whole icon fonts for a few symbols. |
| 3D | Three.js when 3D is central and verifiable. | Decorative 3D that cannot be tested or understood. |

## Copy Quality

Render only text meant for the audience. Remove leaked planning metadata such as
talk duration, target audience, density, style labels, stage size, deployment
target, navigation requirements, or implementation notes unless the user asked
for that information to appear.

Copy rules:

- Keep titles specific enough to make sense on their own.
- Replace vague claims with concrete evidence, numbers, examples, or direct
  takeaways.
- Remove duplicated phrases and symmetrical filler.
- For speaker-led decks, keep on-slide copy short and let spoken narrative carry
  detail.
- For reading-first decks, make each slide self-contained without shrinking text
  into unreadability.
- Do not add hype words to compensate for weak content; clarify the point.

Examples:

| Weak | Better |
|---|---|
| Unlock seamless collaboration | Cut review loops from 3 days to 1 |
| Our solution | What changes after the workflow is automated |
| Robust, scalable, and user-friendly | Handles 10k records without manual cleanup |
| 40-minute live talk for engineers | Why voice changes the coding loop |
