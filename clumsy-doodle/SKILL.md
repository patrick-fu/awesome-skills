---
name: clumsy-doodle
description: >-
  Zero-dependency procedural MS Paint, toddler-crayon, and pencil-sketch doodle
  renderer (no image model). Use when drawing clumsy, scribbly illustrations,
  memes, photo-to-doodle redraws, or semi-realistic hand-drawn phone/window UI
  sketches (小孩丑画风, 手残涂鸦, 铅笔速写, Scribblification) as PNG or HTML.
---

# Clumsy Doodle

Generate deliberately clumsy MS Paint doodles, toddler crayon drawings, and
semi-realistic hand-drawn pencil sketches **without calling any
image-generation model** and **without external packages**. The LLM provides
semantic understanding and simple geometry in a declarative JSON spec;
`scripts/render_doodle.py` (pure Python 3 standard library) renders jagged
pixels, shaky mouse lines, overflowing scribble fills, dry wax-crayon textures,
or tapered graphite pencil cross-hatching.

## Orthogonal Dials (+ Shortcut Presets)

Mix two main dials and an optional color switch to cover everything from 2-year-old
chaos to readable hand-drawn UI/device mockups:

| Dial | Values | Controls |
|---|---|---|
| `--fidelity` | `toddler` · `clumsy` (default) · `sketch` | Abstraction, jitter/slop, and canvas precision (`240px` pixelated vs `440px` clean sketch) |
| `--medium` | `mspaint` (default) · `pencil` · `crayon` | Brush texture & paper (hard white pixels, graphite paper + hatching, warm grainy wax crayon) |
| `--color` | `full` (default) · `accent` · `mono` | Full color, monochrome graphite + `accent: true` highlights only, or pure grayscale |

Rule of thumb for UI / readable text:
- Scenes containing phone frames, desktop windows, buttons, or small labels
  should default to `--fidelity sketch` (e.g. `440×340` with `roundRect`,
  `solidRoundRect`, and `hatchRect`). You can still give surrounding characters
  or joke annotations `jitterScale: 1.8` for mixed-precision comedic contrast.
- Keep `toddler` / `clumsy` for bold icons, portraits, pets, and big-text memes.

Shortcut `--preset` names remain supported: `clumsy`, `messy`, `crayon`,
`cursed`, `neat-rough`, `pencil-sketch` (`sketch + pencil + accent`).

## Two Workflows

### 1. Text / Concept / UI Mockup to Doodle
1. Choose dials (default `clumsy + mspaint` for comedic punch; `sketch + pencil
   + accent` for readable phone/window diagrams or refined sketches).
2. Author a compact JSON spec following `references/dsl.md` (15–35 `ops` for
   `toddler`/`clumsy`; 35–80 `ops` for `sketch`). Layer back-to-front:
   **shadows/background → fills/hatching → outlines → eyes/labels/accents**.
3. Render with `scripts/render_doodle.py` and visually inspect the output before
   delivering.

### 2. Photo to Doodle (Multimodal Vision + Procedural Brush)
1. Read `references/photo-to-doodle.md` first.
2. Inspect the photo and extract **4–6 unmistakable identity anchors** (glasses,
   hair silhouette, fur patches, outfit color, iconic prop/background) plus an
   optional kid-style naive embellishment.
3. Translate anchors into a layered JSON spec (`clumsy + mspaint` for viral
   "Scribblification" contrast, or `sketch + pencil` for a cleaner hand-drawn
   portrait sketch).
4. Render, inspect the output side-by-side against the source photo, and iterate
   1–2 rounds until recognizability and comedic contrast land.

## Rendering CLI (Zero Third-Party Dependencies)

Requires only `python3` (standard library: `zlib`, `struct`, `json`, `math`).

```bash
# Default comedic MS Paint PNG (4x nearest-neighbor -> 960x960)
python3 scripts/render_doodle.py spec.json -o out.png

# Dial combinations: semi-realistic pencil sketch with single-color accents
python3 scripts/render_doodle.py spec.json -o out.png --fidelity sketch --medium pencil --color accent

# Shortcut preset + seed override
python3 scripts/render_doodle.py spec.json -o out.png --preset pencil-sketch --seed 77

# Standalone interactive HTML canvas (full Unicode/CJK text + reroll + PNG download)
python3 scripts/render_doodle.py spec.json -o out.png --html out.html
```

Note on text labels:
- PNG mode uses a built-in zero-dependency 5×7 pixel bitmap font for ASCII
  English, numbers, and punctuation (`LOOP!!`, `ERR 500`, `IT'S FINE`).
- When Chinese/Unicode text is needed inside the drawing, emit `--html out.html`
  (native browser Canvas renders all CJK characters cleanly).

## Self-Check Before Delivering

- **Readability**: Can you recognize the subject, UI text, or joke in under 1 second?
- **Dial fit**: Do UI/window/phone scenes stay crisp (`sketch`) while comedic
  drawings lean into messy overflow (`clumsy`/`toddler`)?
- **Visual verification**: Did you inspect the actual rendered PNG/HTML output
  before showing it to the user?

## Where Things Live

- `scripts/render_doodle.py` — self-contained Python 3 stdlib PNG & HTML renderer.
- `references/dsl.md` — full JSON schema, 14 drawing ops, dials, and recipes.
- `references/photo-to-doodle.md` — multimodal anchor distillation and critique loop.
- `assets/examples/` — runnable JSON specimens (`sam-helicopter.json`,
  `db-on-fire.json`, `toddler-cat.json`, `agent-loop-zh.json`,
  `phone-alert-sketch.json`), `assets/showcase.webp`, and `assets/showcase.zh-CN.webp`.
