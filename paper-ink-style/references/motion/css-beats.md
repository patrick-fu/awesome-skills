# CSS Beats (Zero-JS Paper-Ink Motion)

Load this guide when a whiteboard page explains step-by-step unfolding, causal
flow, label swaps, or fold transitions and should stay **pure CSS, zero JS**.
Every class below ships in `assets/base.css` (v1.4.0) and stays strictly inside
the paper-and-pencil whiteboard hand—never introduce dark neon glows,
glassmorphism, or SVG Gooey filters.

## Physics & Craft Baseline

- **Underdamped paper spring**: `base.css` defines `--pvl-ease-spring` using
  CSS `linear(...)` with a `cubic-bezier(.22,1.25,.36,1)` fallback so cards and
  stamps settle crisply like paper landing on a desk.
- **Never pop from `scale(0)`**: `.pvl-reveal` enters from `scale(.95)` with a
  short `10px` lift so elements feel grounded rather than exploding from a
  point.
- **Origin-anchored transforms**: anchor `transform-origin` to the real hinge
  or attachment edge (left edge for `.pvl-pill-morph`, bottom edge for
  `.pvl-impact`, top edge for tilted cards).
- **Explicit properties, no idle loops**: transition only named properties
  (`transform`, `opacity`, `max-width`, `clip-path`, `block-size`)—never write
  `transition: all`, and never add continuous bobbing/breathing loops to static
  cards.
- **Aligned numerals**: apply `font-variant-numeric: tabular-nums` to counters,
  metrics, and latency tables so changing digits never jitter horizontally.

## Beat Entrances & Tactile Press

| Class | Role | Mechanics & Custom Properties |
| --- | --- | --- |
| `.pvl-reveal` | Default beat entrance | `translateY(10px) scale(.95) → none`; stagger with `--pvl-d` (e.g. `style="--pvl-d:120ms"`) |
| `.pvl-reveal--stamp` | Verdict badge / TL;DR stamp | `scale(1.25) → 1` crisp stamp landing |
| `.pvl-reveal--tilt` | Paper card placement | 2.5D perspective tilt (`perspective(720px) rotateX(10deg) scale(.95) → flat`) with soft drop shadow settle |
| `.pvl-reveal--sweep` | Marker highlight draw | Sweeps yellow/band highlight left-to-right across the verdict phrase |
| `.pvl-press` | Interactive button / expandable card | Tactile `:active { transform: scale(.97) }` press feedback with quick recovery |

## In-Place State Cues

Mutate existing whiteboard anchors instead of stacking extra 3-column summary
cards:

| Class | When to use | Mechanics & Custom Properties |
| --- | --- | --- |
| `.pvl-blur-bridge` | Continuous state handoff between views or readings | `blur(3.5px)` + `scale(.96)` + `4px` lift resolving crisply to `0` |
| `.pvl-slot` | Insert a live constraint, chip, or status right inside a sentence | Elastic `max-width` spring open (`--pvl-slot-w`, default `240px`; toggleable via `data-open`) |
| `.pvl-wipe` | Swap a label, tag, or verdict phrase in place | Horizontal `clip-path: inset(0 100% 0 0) → inset(0)` wipe |
| `.pvl-pill-morph` | Expand a pill or status token from one fixed edge | `transform-origin: left center`; expands from `--pvl-pill-from` to `--pvl-pill-to` (or `data-expanded`) |
| `.pvl-impact` | Emphasize weight landing on a vessel, queue, or threshold card | Bottom-anchored subtle squash (`scale(1.035, .95)`) and rebound |
| `.pvl-beam` | Show active directional flow along a dashed connector or SVG path | Blue-ink flow along `stroke-dashoffset` (`--pvl-beam-span`, `--pvl-beam-dur`) or dashed connector background |
| `.pvl-camera` | Focus-crop or pan onto a specific whiteboard region | Controlled by `--pvl-cam-x`, `--pvl-cam-y`, `--pvl-cam-scale` |

## Native Smooth Folds (`@starting-style` + `interpolate-size`)

`base.css` enables `interpolate-size: allow-keywords` on `:root` and animates
`<details class="pvl-fold">` natively via `::details-content` +
`@starting-style` (`block-size: 0 → auto`, `opacity: 0 → 1`) with graceful
fallback in browsers without keyword sizing—zero JS required for secondary
evidence layers.

## Mobile & Reduced-Motion Guardrails

- **390px / `<=640px` camera reset**: `base.css` automatically forces
  `.pvl-camera` back to identity (`--pvl-cam-x: 0px; --pvl-cam-y: 0px;
  --pvl-cam-scale: 1; transform: none !important`) at `max-width: 640px`, and
  rotates `.pvl-flow .pvl-connector.pvl-beam` vertically so narrow screens keep
  zero horizontal overflow.
- **`prefers-reduced-motion: reduce`**: `base.css` disables every `.pvl-*`
  keyframe animation, transition, and `.pvl-press:active` scale shift globally
  so the page renders immediately as a clean, settled whiteboard frame.
