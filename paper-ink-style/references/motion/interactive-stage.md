# Interactive Stage (Stateless `seek(t)` Whiteboard Lab)

Load this guide only when a page explains **continuous physical processes**—
queues, backpressure, cache eviction, metric before/after evolution, layered
event history, or scrubbed annotation overlays—where pure CSS beats cannot let
the reader inspect intermediate states. Keep ordinary reading pages zero-JS.

Stay strictly within the paper-and-pencil whiteboard hand: ink lines, warm
paper surfaces, semantic kit colors, and clean paper/clip masks. Never add
dark neon themes, glassmorphism, or SVG Gooey effects.

## Core Contract: Stateless `seek(t)`

Every interactive whiteboard stage must be driven by a single pure function
`seek(t)` over `[0, duration]`:

- **Exact forward and reverse scrubbing**: `seek(t)` computes every transform,
  opacity, digit column, beam phase, deck offset, and caption strictly from `t`
  and explicit UI toggles (never accumulated delta drift or `Math.random()`).
  Dragging the scrubber backward or jumping to an anchor restores the exact
  earlier frame.
- **Required inspection controls**:
  - **Play / Pause** button (`aria-pressed`)
  - **`0.4×` slow-motion toggle** scaling `dt` cleanly so compression, beam
    flow, and state transitions are easy to study
  - **Continuous scrub bar** (`<input type="range">`) that pauses playback on
    manual drag
  - **Named beat anchor buttons** letting readers jump straight to key phases
    for low-cognitive-load re-entry
- **Verification hook**: expose `window.pvlMotionStage = { seek, duration }`
  so headless screenshots or tests can inspect any deterministic timestamp.

## Whiteboard Stage Patterns

Combine only the patterns the mechanism actually calls for:

1. **Rolling Digits**: render changing metrics (`p95`, queue depth, hit rate)
   as per-digit vertical strips inside `.pvl-digits` (`font-variant-numeric:
   tabular-nums`, monospace). Roll only the digits that change so unchanged
   places stay anchored.
2. **Vessel ingestion & landing impact**: represent buffers, queues, or caches
   as rough-bordered containers (`.pvl-vessel`) where incoming tokens trigger a
   damped, volume-preserving squash-and-rebound while a dashed blue-ink SVG
   beam (`stroke-dasharray` / `stroke-dashoffset` driven from `t`) drains items
   downstream.
3. **Stacked depth deck**: keep prior events or state transitions visible in a
   shallow depth stack (`.pvl-deck-card`, newest in front with progressive
   scale/opacity recession) plus a one-click **Expand / Collapse** toggle so
   history stays scannable without cluttering the viewport.
4. **X-Ray scribble & overlay comparison**: compare a surface view against
   underlying mechanics—or before/after pencil corrections—using a scrubbed
   horizontal clip wipe or opacity/aperture mask driven by `t`. Render the
   revealed layer as clean pencil annotations, redline strike-throughs, or warm
   paper diagrams (never neon scanner beams).
5. **Local camera emphasis**: nudge `.pvl-camera` (`--pvl-cam-x`,
   `--pvl-cam-y`, `--pvl-cam-scale`) subtly during peak moments while letting
   `base.css` automatically zero it out at `<=640px` and when
   `prefers-reduced-motion: reduce` is active.

## Adopting `assets/snippets/motion-stage.html`

Start from `assets/snippets/motion-stage.html`:

1. Copy the `.pvl-stage-shell` markup, stage-local styles, and inline
   `<script>` into your standalone HTML page (which already inlines
   `assets/base.css`).
2. Keep the `.pvl-*` classes, control bar (`play`, `0.4×`, scrubber, beat
   anchors), `prefers-reduced-motion` check, and `window.pvlMotionStage` hook.
3. Replace `ANCHORS`, token/event specs, numeric targets, and stage captions
   with the real domain mechanism—never leave placeholder telemetry or generic
   labels behind.
