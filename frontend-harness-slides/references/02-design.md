# 02 Design

Use this after the plan is clear and before committing the deck's visual system.
The goal is to choose a style, preview it honestly, select fonts/assets, and
keep slide copy audience-facing.

## Discover By Eye

Most users cannot name the exact style they want; they recognize it when they
see it. Before implementation, explicitly ask whether to make a minimal
interactive style preview. When visual direction is unclear, recommend three
real interactive slide previews in meaningfully different directions. When the
user already gives a clear style, confirm the main style, offer same-style
refinements and nearby alternatives for inspiration, then ask whether to make a
small same-style preview or proceed directly.

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

## Selected Theme Notes & Design DNA

After the user chooses a preview direction, summarize the selected theme notes and Design DNA before expanding the full deck, and record them in the external context document (e.g., `docs/context.md`):

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
custom_invented_metaphors:
pacing_log:
```

For non-trivial decks, prefer recording these notes in the shared context
document, README, handoff note, or theme configuration so the chosen style
survives later edits. Follow the user's preferred documentation location.

## Style System, Not Template

A selected style is a visual system, not one repeated layout. Unless the user
wants a uniform template rhythm, vary layout families, composition direction,
object scale, interaction moments, and motion beats while keeping typography,
palette, navigation, and visual language coherent.

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
starting point. It should feel like a small wheel, not a cropped dot list: keep
the active marker visually centered, fade or scale nearby markers by distance,
animate the marker track when the scene changes, and support click plus wheel,
trackpad, or touch when useful. Adapt the form to the style: hand-drawn dots,
luminous particles, quiet editorial ticks, or another matching treatment are all
valid. Use simpler dots, section tabs, or another navigator when they better fit
the deck or the user's preference.

**Bad Experience Avoidance**: Avoid making the navigator a flashy or distracting control that obstructs the main content. When there are many slides, display only a localized sliding window of markers; ensure that click, wheel, and touch interactions are highly predictable, and prevent the active marker from jumping or jittering during transitions.

Treat any carousel, picker, feathered rail, note panel, or control surface as a
stage-local design object. If it needs a fade, mask, safe zone, or reserved
reading area, design that boundary inside the fixed stage rather than borrowing
the browser viewport. A good navigation treatment should survive screenshot,
PDF/static export, and viewport scaling without depending on off-stage chrome.

## Style Selection & Catalog Guidance

If you are choosing or designing a style for the deck, use
`references/style/index.md` as the style catalog and inspiration library.

Use the following guiding principles to select and align the visual system:
- **Style proposal**: Include a style proposal in the Pre-Build Alignment. If the
  user does not have a pre-existing brand or design system, select 2-3 curated
  options from the 24-style catalog that best fit the audience, content, and
  delivery target.
- **Clear user style**: If the user already chose a style, confirm that main
  direction, offer 3-5 refinements inside the chosen style, and include a few
  nearby catalog options as inspiration rather than pressure to switch.
- **Preview prompt**: Ask whether to create a minimal interactive preview before
  full implementation. Recommend doing so by default, and skip it only when the
  user explicitly declines or asks to proceed directly.

## Fonts

Choose type as part of the visual direction. It should match the style, cover
the deck's languages, and render reliably in the final handoff.

If the slide deck contains Chinese, Japanese, or Korean (CJK) characters, keep the following light reminders in mind to ensure a solid reading experience:
- **Font Selection & Fallbacks**: Select fonts and fallback stacks that cover CJK characters (e.g., pairing handwritten Latin fonts with Kaiti; elegant serif Latin fonts with Songti/Mingti; clean sans-serif Latin fonts with modern Heiti).
- **Weight & Spacing Compensation**: CJK characters are visually denser. Consider adjusting letter spacing (e.g., `tracking-wide`) and line height to prevent visual crowding, especially on high-density slides.
- **Rendering Verification**: Perform a light browser check to ensure proper rendering without falling back to unexpected default system fonts. Avoid making this a heavy font audit process; keep the setup lightweight and focused on reliable rendering.

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

### Aesthetic & Semantic Alignment of Data Visualization
When integrating charts or data visualizations, avoid generic, unstyled library defaults. Proactively guide the visual design of the chart to align with the chosen style:
- **Style Integration**: For hand-drawn styles (e.g., Sketchboard), guide the chart to use organic lines or stacked visual elements instead of sharp 2D grids. For technical styles, use high-contrast neon accents and precise gridlines.
- **Semantic Focus**: Minimize visual noise (remove redundant gridlines, borders, or legends). Highlight only the key data points or trends that directly support the slide's narrative conclusion.
- **Progressive Reveals**: Guide data elements to grow or enter sequentially to support live presentation pacing.

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
| 40-minute live talk for engineers | Why automation changes the coding loop |
