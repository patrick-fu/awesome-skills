# Clumsy Doodle JSON DSL

Every doodle is a plain JSON object rendered by `scripts/render_doodle.py` into
a crisp PNG and/or standalone interactive HTML5 Canvas.

## Top-Level Fields

```json
{
  "width": 440,
  "height": 340,
  "scale": 2,
  "fidelity": "sketch",
  "medium": "pencil",
  "color": "accent",
  "seed": 42,
  "ops": []
}
```

- `width`, `height`: internal canvas grid. Defaults to `240×240` for `toddler` /
  `clumsy`, and `440×340` (or `440×440`) for `sketch`.
- `scale`: PNG integer upscale factor. Defaults to `4` when `width < 400`, or
  `2` when `width >= 400`.
- `fidelity`: `"toddler"` | `"clumsy"` (default) | `"sketch"`.
- `medium`: `"mspaint"` (default) | `"pencil"` | `"crayon"`.
- `color`: `"full"` (default) | `"accent"` (grayscale except ops with `"accent": true`) | `"mono"` (pure grayscale).
- `preset`: optional shortcut (`"clumsy"`, `"messy"`, `"crayon"`, `"cursed"`, `"neat-rough"`, `"pencil-sketch"`). Explicit `fidelity` / `medium` / `color` override preset values.
- `seed`: deterministic integer PRNG seed.
- `bg`: optional background hex override.

## Per-Op Common Modifiers

Any drawing op accepts:
- `color`: hex (`#rrggbb`, `#rgb`) or basic color name.
- `accent`: `true` keeps this op in vivid color when `color: "accent"` is active.
- `alpha`: `0.0–1.0` opacity blending (especially nice for `pencil` shading and `solidRoundRect` card tints).
- `jitterScale`: local jitter/overshoot multiplier (e.g., `0.6` on a phone frame for clean edges, `1.8` on a frantic stick figure next to it for comedic contrast).
- `double`: `true` retraces an outline twice like an uncertain mouse/pencil fix.

## Drawing Operations (`ops`)

Ops execute in strict array order (back-to-front painter's algorithm).

### 1. Fills & Pencil Hatching
- **`fillRect`** / **`hatchRect`**: `{ "op": "hatchRect", "x": 56, "y": 28, "w": 196, "h": 292, "color": "#666666", "angle": -0.72, "spacing": 6.5, "cross": false, "alpha": 0.45 }`
  - `fill*` uses continuous back-and-forth zigzag scribbles; `hatch*` lifts the pen between parallel strokes (set `"cross": true` for cross-hatching).
- **`fillEllipse`** / **`hatchEllipse`**: `{ "op": "fillEllipse", "cx": 120, "cy": 100, "rx": 40, "ry": 35, "color": "#fff1c1" }`
- **`fillPoly`** / **`hatchPoly`**: `{ "op": "hatchPoly", "points": [[40,80],[70,30],[100,80]], "color": "#555555", "cross": true }`
- **`solidRoundRect`**: `{ "op": "solidRoundRect", "x": 46, "y": 18, "w": 196, "h": 292, "r": 26, "color": "#ffffff", "alpha": 1.0 }`
  - Clean flat tinted surface under hand-drawn outlines (ideal for phone screens, macOS window bars, chat bubbles, buttons).

### 2. Outlines, Curves & Connectors
- **`line`**: `{ "op": "line", "points": [[20,20],[100,25],[140,80]], "color": "#111111", "size": 2 }`
- **`curve`**: `{ "op": "curve", "points": [[126,96],[116,38],[164,76]], "steps": 18, "size": 2.4 }`
  - Quadratic (3 points) or cubic (4 points) Bezier curve rendered through the shaky brush — great for cat ears, hair arcs, swooping arrows, coffee steam.
- **`rect`**: `{ "op": "rect", "x": 40, "y": 50, "w": 80, "h": 60, "size": 2.5 }`
- **`roundRect`**: `{ "op": "roundRect", "x": 46, "y": 18, "w": 196, "h": 292, "r": 26, "size": 2.4, "double": true, "jitterScale": 0.65 }`
- **`ellipse`**: `{ "op": "ellipse", "cx": 120, "cy": 100, "rx": 40, "ry": 35, "start": 0, "end": 6.4, "wobble": 0.12 }`
- **`arrow`**: `{ "op": "arrow", "points": [[40,120],[120,100],[190,125]], "head": 10, "size": 2.5 }`
- **`dot`**: `{ "op": "dot", "x": 105, "y": 96, "size": 5, "color": "#111111" }`

### 3. Text Labels & Speech Bubbles
- **`label`**: `{ "op": "label", "x": 70, "y": 61, "text": "9:41", "scale": 2, "fontSize": 12, "align": "left", "mono": true, "color": "#111111" }`
  - PNG mode uses `scale` (1–4) with the built-in 5×7 ASCII bitmap font; HTML mode uses `fontSize` (or `scale * 7`) with full Unicode/CJK font support.
- **`bubble`**: `{ "op": "bubble", "x": 140, "y": 16, "w": 84, "h": 34, "tail": [132, 62], "text": "IT'S FINE", "fill": "#e8f5e9", "color": "#237a4b" }`

## Mixed-Precision UI Recipe (`sketch + pencil + accent`)

When illustrating a phone screen or desktop window alongside a funny character:
1. Cast a light `hatchRect` drop shadow behind the device/window (`alpha: 0.4`, `angle: -0.7`).
2. Draw clean paper/white interiors with `solidRoundRect`, then frame them with `roundRect` (`jitterScale: 0.55–0.75`).
3. Keep screen text legible (`label` with `mono: true` for timestamps/commands) and reserve `"accent": true` for 1–2 focal elements (red `99+` badge, green chat reply, danger button).
4. Give surrounding stick-figure reactions or callout arrows `jitterScale: 1.5–1.8` so the comedic contrast pops.
