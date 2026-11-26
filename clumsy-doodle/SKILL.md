---
name: clumsy-doodle
description: >-
  Zero-dependency procedural MS Paint, toddler-crayon, and pencil-sketch doodle
  renderer (no image model). Use when drawing clumsy, scribbly illustrations,
  transparent character stickers, memes, photo-to-doodle redraws, or
  semi-realistic hand-drawn phone/window UI sketches (小孩丑画风, 手残涂鸦,
  铅笔速写, Scribblification) as PNG, standalone HTML, or embeddable HTML/JS.
---

# Clumsy Doodle

Generate deliberately clumsy MS Paint doodles, transparent character stickers,
toddler crayon drawings, and semi-realistic hand-drawn pencil sketches
**without calling any image-generation model** and **without external
packages**. The LLM provides semantic understanding and geometry in a
declarative JSON spec; `scripts/render_doodle.py` (pure Python 3 standard
library) renders jagged pixels, shaky mouse lines, overflowing scribble fills,
dry wax-crayon textures, or tapered graphite pencil cross-hatching.

## Orthogonal Dials (+ Shortcut Presets)

Mix two main dials and an optional color switch to cover everything from 2-year-old
chaos to readable hand-drawn UI/device mockups:

| Dial | Values | Controls |
|---|---|---|
| `--fidelity` | `toddler` · `clumsy` (default) · `sketch` | Abstraction, jitter/slop, and canvas precision (`240px` pixelated vs `440px` clean sketch) |
| `--medium` | `mspaint` (default) · `pencil` · `crayon` | Brush texture & paper (hard white pixels, graphite paper + hatching, warm grainy wax crayon) |
| `--color` | `full` (default) · `accent` · `mono` | Full color, monochrome graphite + `accent: true` highlights only, or pure grayscale |

Rule of thumb for dialing:
- **UI / readable text**: Scenes containing phone frames, desktop windows,
  buttons, or small labels default to `--fidelity sketch` (e.g. `440×340` with
  `roundRect`, `solidRoundRect`, and `hatchRect`). Give surrounding characters
  or joke annotations `jitterScale: 1.8` for mixed-precision comedic contrast.
- **Standalone memes / portraits / pets**: Use `clumsy + mspaint` (default) or
  `toddler` for maximum naive charm.
- **Embedded character stickers inside clean cards/articles**: Use
  `preset: "neat-rough"` + `medium: "mspaint"` + `bg: "transparent"` on a
  `180–260px` internal grid (`25–45 ops`) so the figure stays unmistakable while
  keeping authentic MS Paint jagged pixel soul.

Shortcut `--preset` names remain supported: `clumsy`, `messy`, `crayon`,
`cursed`, `neat-rough`, `pencil-sketch` (`sketch + pencil + accent`).

## Sticker Mode & Composite Article Diagrams

When combining doodles with structured diagrams, editorial cards, or rich HTML
documents (such as Feishu/blog embeds):

1. **Separate structure from comedy**: Keep multi-column architecture, labels,
   and connectors in clean static HTML/SVG layout. Reserve `clumsy-doodle` for
   **single-focus character/prop gag stickers** rather than stuffing a dense
   multi-column diagram into one shaky pixel canvas.
2. **Use native transparency — never strip white pixels**: Set
   `"bg": "transparent"` (or pass `--transparent`). Both RGBA8 PNG and HTML5
   Canvas preserve interior pure `#ffffff` (eye whites, chef hats, shirts,
   pillows, speech bubbles) 100% opaque. Never hack global white-removal
   (`r > 246 && g > 246 && b > 246`), which punches holes inside characters.
3. **Character canvas floor & opaque base layering**:
   - Keep character sticker internal grids at **`180–260px`** (shrink visually
     with CSS `width` + `image-rendering: pixelated`). Tiny grids (`~110px`)
     magnify absolute pixel jitter and collapse faces into noise.
   - Author **`25–45 ops`** per character with clear silhouette, asymmetric eyes,
     hands/posture, and one unmistakable prop.
   - Lay opaque bases first (`solidEllipse`, `solidPoly`, `solidRoundRect`),
     then layer jagged `fill*` coloring and shaky outlines on top so facial
     features never look muddy.
4. **Reuse the built-in JS runtime**: Use `--embed` (chromeless snippet) or
   `--runtime-js` (shared `window.ClumsyDoodle` runtime across multiple
   canvases via `ClumsyDoodle.mountAll()`) instead of hand-coding custom canvas
   renderers inside every HTML file.

## Workflows

### 1. Text / Concept / Sticker / UI Mockup to Doodle
1. Pick the right mode:
   - Standalone comedic doodle: `clumsy + mspaint` (`240×240`, 15–35 `ops`).
   - Transparent character sticker for a card/article: `neat-rough + mspaint`
     with `"bg": "transparent"` (`180–260px`, 25–45 `ops`, see
     `assets/examples/chef-sticker-transparent.json`).
   - Readable UI/device sketch: `sketch + pencil + accent` (`440×340`, 35–80 `ops`).
2. Author the JSON spec following `references/dsl.md`, layering back-to-front:
   **shadows/background → solid bases (`solid*`) → scribble fills/hatching → outlines → eyes/labels/accents**.
3. **Single-benchmark rule for batches (≥3 illustrations)**: Before generating a
   full multi-figure set or changing art direction, render and preview **1–2
   benchmark samples** first to confirm recognizability, MS Paint charm, and
   motion restraint; only batch-produce after alignment.
4. Render with `scripts/render_doodle.py` and visually inspect the actual output
   before delivering.

### 2. Photo to Doodle (Multimodal Vision + Procedural Brush)
1. Read `references/photo-to-doodle.md` first.
2. Inspect the photo and extract **4–6 unmistakable identity anchors** (glasses,
   hair silhouette, fur patches, outfit color, iconic prop/background) plus an
   optional kid-style naive embellishment.
3. Translate anchors into a layered JSON spec (`clumsy + mspaint` for viral
   "Scribblification" contrast, or `sketch + pencil` for a cleaner hand-drawn
   portrait sketch).
4. Render, inspect side-by-side against the source photo, and iterate 1–2 rounds
   until recognizability and comedic contrast land.

## Critique & Tuning Guardrails (Never Over-Correct Away from the Soul)

- **User says "too ugly / unrecognizable" (`过丑 / 看不出人样`)**:
  - **NEVER** abandon `mspaint` to switch to clean smooth vector `<svg>`
    illustrations or an image-generation model — that over-corrects and kills
    the skill's soul.
  - **DO**: Stay on `medium: "mspaint"`, raise the internal grid to
    **`200–260px`**, shift to `preset: "neat-rough"` (preserves jagged pixels
    and playful slop without scrambling anatomy), lay opaque `solidEllipse` /
    `solidPoly` bases under white/skin areas, and complete `25–45 ops` of clear
    anatomy, eyes, and props.
- **User says "too messy / too much animation" (`太乱 / 动太多`)**:
  - **NEVER** animate the whole doodle with rapid seed-reroll "line boil"
    timers (`setInterval`) or auto-cycling multi-scene hard cuts.
  - **DO**: Keep the doodle canvas **100% static** and limit motion to 1–2
    peripheral elements using slow, calm CSS micro-motion (`4s–7s` dashed flow,
    gentle steam rise, slow `Zzz` float).

## Rendering CLI (Zero Third-Party Dependencies)

Requires only `python3` (standard library: `zlib`, `struct`, `json`, `math`, `html`).

```bash
# Default comedic MS Paint PNG (4x nearest-neighbor -> 960x960 RGB)
python3 scripts/render_doodle.py spec.json -o out.png

# Transparent MS Paint character sticker (RGBA8 PNG, preserves interior white)
python3 scripts/render_doodle.py spec.json -o sticker.png --preset neat-rough --transparent

# Semi-realistic pencil sketch with single-color accents
python3 scripts/render_doodle.py spec.json -o out.png --fidelity sketch --medium pencil --color accent

# Standalone interactive HTML canvas (full Unicode/CJK text + reroll + PNG download)
python3 scripts/render_doodle.py spec.json -o out.png --html out.html

# Chromeless embeddable HTML snippet (ready for article cards / HTML5 blocks)
python3 scripts/render_doodle.py spec.json --transparent --embed sticker-snippet.html --canvas-id chefCanvas

# Export reusable JS runtime once for multi-sticker pages (window.ClumsyDoodle)
python3 scripts/render_doodle.py --runtime-js clumsy-doodle-runtime.js
```

Note on text labels:
- PNG mode uses a built-in zero-dependency 5×7 pixel bitmap font for ASCII
  English, numbers, and punctuation (`LOOP!!`, `ERR 500`, `IT'S FINE`).
- When Chinese/Unicode text is needed inside the drawing, emit `--html` or
  `--embed` (native browser Canvas renders all CJK characters cleanly).

## Self-Check Before Delivering

- **Readability**: Can you recognize the subject, facial expression, UI text, or
  joke in under 1 second?
- **Soul preserved**: For MS Paint requests, do jagged pixels, slight asymmetry,
  and playful hand-drawn charm remain visible (not over-smoothed into clean SVG)?
- **Transparency integrity**: On transparent stickers, are interior white areas
  (eyes, hats, shirts, bubbles) 100% solid opaque with clean transparent edges?
- **Visual verification**: Did you inspect the actual rendered PNG/HTML output
  before showing it to the user?

## Where Things Live

- `scripts/render_doodle.py` — self-contained Python 3 stdlib PNG (RGB8/RGBA8),
  HTML, chromeless `--embed`, and `--runtime-js` renderer.
- `references/dsl.md` — full JSON schema, 16 drawing ops, dials, and recipes.
- `references/photo-to-doodle.md` — multimodal anchor distillation and critique loop.
- `assets/examples/` — runnable JSON specimens (`sam-helicopter.json`,
  `db-on-fire.json`, `toddler-cat.json`, `agent-loop-zh.json`,
  `phone-alert-sketch.json`, `chef-sticker-transparent.json`),
  `assets/showcase.webp`, and `assets/showcase.zh-CN.webp`.
