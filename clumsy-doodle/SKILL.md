---
name: clumsy-doodle
description: >-
  Zero-dependency procedural MS Paint and toddler-crayon doodle renderer (no
  image model). Use when drawing clumsy, scribbly illustrations, memes, or
  photo-to-doodle redraws (小孩丑画风, 手残涂鸦, Scribblification) as PNG or
  HTML.
---

# Clumsy Doodle

Generate deliberately clumsy, hilarious, mouse-drawn MS Paint and toddler-crayon
doodles **without calling any image-generation model** and **without external
packages**. The LLM provides semantic understanding and simple geometry in a
declarative JSON spec; `scripts/render_doodle.py` (pure Python 3 standard
library) turns that clean geometry into authentic jagged pixels, shaky mouse
lines, sloppy overflowing scribble fills, or dry wax-crayon paper strokes.

## Two Workflows

### 1. Text / Concept to Doodle
Use for technical metaphors (e.g., server on fire, infinite retry loop), avatars,
reaction memes, or blog/slide spot illustrations:
1. Pick a preset (`clumsy`, `messy`, `crayon`, `cursed`, or `neat-rough`) and
   plan 4–6 recognizable visual anchors on a `240×240` (or `240×200`) canvas.
2. Author a compact JSON spec (typically 15–35 `ops`) following
   `references/dsl.md`. Always layer back-to-front:
   **background hints → scribble color fills → black outlines → eyes/mouth/labels**.
3. Render to PNG (and/or standalone HTML) with `scripts/render_doodle.py`.
4. Visually inspect the rendered PNG before delivering. If it looks too neat,
   cluttered, or off-center, adjust coordinates or bump preset (`clumsy` →
   `messy` / `cursed`) and re-render.

### 2. Photo to Doodle (Multimodal Vision + Procedural Brush)
Use when the user supplies a photo (selfie, pet, travel shot, team photo) and
wants the viral "Scribblification / MSPaintify" contrast without an image model:
1. Read `references/photo-to-doodle.md` first.
2. Inspect the photo and extract **4–6 unmistakable identity anchors** (glasses,
   hair silhouette, fur patches, outfit color, iconic prop/background) plus an
   optional kid-style naive embellishment (e.g. a tiny yellow sun in a window).
3. Translate those anchors into a layered JSON spec — intentionally simplify
   complex backgrounds into a few crooked lines and keep a plain white (or
   crayon-paper) background.
4. Render, inspect the output PNG side-by-side against the source photo, and
   iterate 1–2 rounds until the silhouette and comedic contrast land.

## Rendering CLI (Zero Third-Party Dependencies)

Requires only `python3` (standard library: `zlib`, `struct`, `json`, `math`).

```bash
# Render spec JSON to a crisp nearest-neighbor upscaled PNG (default 4x -> 960x960)
python3 scripts/render_doodle.py spec.json -o out.png

# Override preset, seed, or upscale factor without editing JSON
python3 scripts/render_doodle.py spec.json -o out.png --preset crayon --seed 77 --scale 4

# Also emit a standalone interactive HTML canvas (supports full Unicode/CJK labels + reroll + PNG download)
python3 scripts/render_doodle.py spec.json -o out.png --html out.html

# Read spec directly from stdin
cat spec.json | python3 scripts/render_doodle.py - -o out.png
```

Note on text labels:
- PNG mode uses a built-in zero-dependency 5×7 pixel bitmap font for ASCII
  English, numbers, and punctuation (`LOOP!!`, `ERR 500`, `IT'S FINE`).
- When Chinese/Unicode text is needed inside the drawing, emit `--html out.html`
  (native browser Canvas renders all CJK characters cleanly with pixelated
  scaling) or keep PNG labels short ASCII/symbolic.

## Style Presets

| Preset | Vibe | Best for |
|---|---|---|
| `clumsy` | Classic 90s MS Paint mouse scribble, white bg, jagged black outlines, overflowing zigzag fills | Viral Sam-style portraits, pets, general memes |
| `messy` | 2-year-old chaotic scribble, heavy wobble, wide color overflow, unclosed shapes | Peak "barely recognizable" toddler chaos |
| `crayon` | Dry wax crayon on warm speckled paper (`#fbf9f2`), broken grain texture | Real paper toddler crayon drawings |
| `cursed` | High wobble + automatic double-traced frantic outlines | Unhinged reaction memes |
| `neat-rough` | Calmer low-jitter whiteboard cartoon | Technical docs, blog posts, slides |

## Self-Check Before Delivering

- **Readability**: Can you recognize the subject or joke in under 1 second?
- **Intentional clumsiness**: Are fills visibly scribbled with gaps/overflow
  rather than solid flat blocks, and outlines jagged/unclosed?
- **Clean negative space**: Is the background uncluttered (white or subtle paper
  grain) with at most 4–6 focal elements?
- **Visual verification**: Did you inspect the actual rendered PNG/HTML output
  (not just the JSON) before showing it to the user?

## Where Things Live

- `scripts/render_doodle.py` — self-contained Python 3 stdlib PNG & HTML renderer.
- `references/dsl.md` — full JSON schema, 10 drawing ops, palettes, and tips.
- `references/photo-to-doodle.md` — multimodal anchor distillation and critique loop.
- `assets/examples/` — runnable JSON specimens (`sam-helicopter.json`,
  `db-on-fire.json`, `toddler-cat.json`, `agent-loop-zh.json`) and `assets/showcase.webp`.
