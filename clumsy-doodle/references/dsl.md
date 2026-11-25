# Clumsy Doodle JSON DSL

Every doodle is a plain JSON object rendered onto a low-resolution integer grid
(default `240×240`) and upscaled cleanly via nearest-neighbor (`scale: 4` →
`960×960` PNG) so every jagged pixel stays crisp.

## Top-Level Fields

```json
{
  "width": 240,
  "height": 240,
  "scale": 4,
  "preset": "clumsy",
  "seed": 42,
  "bg": "#ffffff",
  "ops": []
}
```

- `width`, `height`: internal pixel grid (recommended `200–320`; lower = chunkier
  MS Paint pixels, higher = finer scribbles). Default `240×240`.
- `scale`: PNG integer upscale factor. Default `4`.
- `preset`: `"clumsy"` (default) | `"messy"` | `"crayon"` | `"cursed"` | `"neat-rough"`.
- `seed`: deterministic integer PRNG seed. Changing `seed` redraws the exact
  same scene with fresh hand-shake variations.
- `bg`: optional background hex color. Defaults to `#ffffff` (or `#fbf9f2` with
  subtle paper grain under `crayon`).

## Drawing Operations (`ops`)

Ops execute in strict array order (painter's algorithm: draw back-to-front).

### 1. Sloppy Scribble Fills (Back-and-forth zigzag strokes with overflow)

- **`fillRect`**: `{ "op": "fillRect", "x": 40, "y": 50, "w": 80, "h": 60, "color": "#ffe066", "angle": -0.4, "spacing": 4.5, "slop": 3.0, "size": 3, "texture": "pixel" }`
- **`fillEllipse`**: `{ "op": "fillEllipse", "cx": 120, "cy": 100, "rx": 40, "ry": 35, "color": "#fff1c1", "angle": 0.25, "spacing": 5.0, "slop": 2.5, "size": 4 }`
- **`fillPoly`**: `{ "op": "fillPoly", "points": [[40,80],[70,30],[100,80]], "color": "#ff922b", "angle": 0.6, "spacing": 4.2, "slop": 3.0, "size": 3 }`

Optional fill tuning:
- `angle`: stroke direction in radians (`0` = vertical scan / horizontal strokes, `-0.45` = diagonal). Vary angles between neighboring regions so it looks hand-colored.
- `spacing`: distance between zigzag passes (larger = more white paper gaps showing through).
- `slop`: max pixel overflow outside shape boundaries (higher = sloppier kid coloring).
- `size`: pixel brush diameter (`2–5`).
- `texture`: `"pixel"` (solid hard pixels) or `"crayon"` (dry speckled wax grain). Inherits from preset when omitted.

### 2. Shaky Outlines & Connectors

- **`line`**: `{ "op": "line", "points": [[20,20],[100,25],[140,80]], "color": "#111111", "size": 2, "jitter": 1.8, "overshoot": 2.2, "double": false }`
- **`rect`**: `{ "op": "rect", "x": 40, "y": 50, "w": 80, "h": 60, "color": "#111111", "size": 3, "double": true }`
- **`ellipse`**: `{ "op": "ellipse", "cx": 120, "cy": 100, "rx": 40, "ry": 35, "start": 0, "end": 6.4, "wobble": 0.14, "color": "#111111", "size": 2, "double": false }`
  - Omit `start`/`end` for an automatically slightly-unclosed or slightly-overlapping full loop. Pass radians (`0` to `3.14`, etc.) for arcs and retry loops.
- **`arrow`**: `{ "op": "arrow", "points": [[40,120],[120,100],[190,125]], "color": "#1769c2", "size": 3, "head": 11 }`
- **`dot`**: `{ "op": "dot", "x": 105, "y": 96, "size": 5, "color": "#111111" }` (pupils, buttons, LEDs, nostrils).

Tip: Setting `"double": true` on one or two hero outlines (like sunglasses, a monitor, or a robot head) mimics someone trying to "fix" a bad mouse line by tracing over it twice.

### 3. Labels & Meme Speech Bubbles

- **`label`**: `{ "op": "label", "x": 24, "y": 28, "text": "LOOP!!", "color": "#111111", "scale": 2, "jitter": 1 }`
  - In PNG mode: renders crisp 5×7 pixel glyphs at integer `scale` (`1–4`) with slight per-letter vertical wobble (`jitter`). Supports ASCII letters, digits, and punctuation.
  - In `--html` mode: renders via browser Canvas with full Unicode/CJK support.
- **`bubble`**: `{ "op": "bubble", "x": 140, "y": 16, "w": 84, "h": 34, "tail": [132, 62], "text": "IT'S FINE", "fill": "#e8f5e9", "color": "#237a4b", "textColor": "#237a4b", "scale": 1 }`
  - Draws a sloppy filled box + wobbly outline + optional crooked pointer triangle to `tail` + centered text.

## Composition Recipes That Always Land

1. **Keep the layer order strict**:
   - Layer 1: Faint background hints (3–6 lines max: horizon, window, ceiling ovals).
   - Layer 2: `fill*` scribble blocks (face, clothes, fur, props).
   - Layer 3: Dark outlines (`rect`, `ellipse`, `line`) on top of fills so black ink cuts cleanly over the messy colors.
   - Layer 4: Expressive anchors last — oversized mismatched eyes (`fillEllipse` white sclera → `ellipse` outline → `dot` colored iris → `dot` black pupil), crooked mouth, sweat drops, `bubble`/`label`.
2. **Use classic primary MS Paint / crayon colors** instead of subtle muted gradients:
   - Ink `#111111`, Cream skin `#fff1c1`, Crayon orange `#ff922b`, Bright red `#ff2a2a`, MS Paint blue `#1e90ff`, Grass green `#2ecc71`, Sun yellow `#ffe066`, Seat gray `#8f9396`, Deep navy `#101f4d`, Hair brown `#8b4513`.
3. **Asymmetry creates comedy**: make left and right eyes slightly different sizes (`rx: 10` vs `rx: 7`) or 2–3px offset in `y`, tilt mouths slightly, and avoid perfect horizontal alignment.
