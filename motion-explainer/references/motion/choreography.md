# Choreography & Composition Patterns

Load this reference when designing scene-by-scene staging, choosing how objects
transform across word cues, and checking motion craft guardrails.

## Core Rule: Mutate Objects in Place, Not Box Walls

Avoid turning scenes into repeating **1-2-3 equal-width horizontal cards with
arrows**. Uniform box rows flatten distinct causal structures (pipelines,
tradeoffs, state mutations, queues, UI traces) into static slides and waste
canvas area on decorative borders.

Establish spatial anchors once per scene, then mutate those same objects in
place on word-synced `anchors` / `cues` (`state`, `action`, `badge`, `data`)
instead of appending summary boxes.

## Match Composition to the Mechanism

| Mechanism you are explaining | Preferred stage composition | Primitives / technique |
| --- | --- | --- |
| Definition or constraint modifying a claim | Living sentence on open canvas pushing words apart to insert a live chip or constraint | `inlineSlot` |
| Queuing, caching, eviction, or memory pressure | Physical vessel swallowing, stacking, compressing, and bouncing items | `spring` + `impact` |
| Agent loop, tool call, or request/response dialogue | Single-edge anchored pill morph expanding with directional clip wipe | `pillMorph` + `wipeClip` |
| Refactoring, routing switch, or before/after state | Same objects lifting, stretching along velocity, and re-seating—or crossing an inverse-color boundary | `spring` + `smear` |
| Capacity, fill level, or liquid progress | Rising wave or clip boundary cleanly splitting base and inverted-color typography | Pure `seconds` `clip()` |
| Deep UI, trace, or complex diagram inspection | Cropped UI slice with smooth virtual camera pan and push-in | `camera` |
| Specific code lines changing behavior | Trimmed snippet (`<= 12` lines) with sliding focus band | `spring` + `wipeClip` |
| Numeric before/after metrics or latency deltas | Tabular per-digit vertical counter roll paired with soft focus handoff | `rollingDigits` + `blurBridge` |
| Active dataflow, routing, or retry loop | Directed light/ink pulse traveling along the actual SVG connector path | `beamPath` |
| Multi-step event history or notification stack | Shallow depth-stacked deck expanding cleanly on cue | `stackedDeck` |
| Shape, icon, waveform, or state-glyph change | Isomorphic SVG quadratic curve interpolation between matched point arrays | `morphPath` |
| Task completion, verification pass, or milestone lock-in | Restrained 6–12 seeded micro-particles dissipating cleanly within `~350 ms` | `microBurst` |
| Surface UI vs underlying execution stack | X-Ray scanning spotlight mask (`mask-image` aperture or sweep driven by `seconds`) | Pure `seconds` mask |
| State, version, or deployment switch | 3D Split-Flap flip or deterministic Text Scramble decode (fixed seed, no `Math.random()`) | Pure `seconds` hash |
| Hardware/architecture teardown or AI listening state | Precision SVG Callout stroke-draw leaders, or Dot Matrix acoustic ripple field | `stroke-dashoffset` / `seconds` |
| Expressive character or mascot focus *(opt-in)* | 2.5D spherical gaze tracking plus zero-RNG deterministic blink/breath | `sphereEyes` + `deterministicBlink` |

## Motion Craft & Determinism Guardrails

- **Pure function of `seconds` only**: compute every transform, opacity, clip,
  mask, and particle position deterministically from `frame.time` /
  `frame.sceneAge` / `frame.settled`. Never use `Date.now()`, `Math.random()`,
  `requestAnimationFrame`, or CSS autoplay loops—forward and reverse `seek()`
  must reproduce pixel-identical frames.
- **Pacing windows**: settle primary entrances with closed-form springs in
  `300–650 ms`, land keyword accents in `200–350 ms`, and hold resting poses
  long enough to read comfortably.
- **Never pop from `scale(0)`**: enter elements from `scale(0.94–0.96)` with
  short travel so geometry feels physically grounded instead of bursting from a
  point.
- **Anchor `transform-origin`**: bind `transform-origin` to the actual trigger
  edge, attachment point, or hinge before scaling or morphing.
- **Asymmetric enter/exit timing**: clear exiting elements slightly faster
  (`~200–280 ms`) than entrances (`~320–550 ms`) so departing state never
  lingers over the incoming beat.
- **FLIP shared-element handoffs**: when expanding a badge, node, or UI slice
  into a detail view across cues, derive both rects in `1280×720` stage
  coordinates and animate the inverted `translate` + `scale` with `spring(age)`
  so spatial identity holds without hard cuts.
- **Velocity-aligned sandwich squash**: during diagonal travel or bounces,
  compute velocity angle `θ` and clamped stretch factor `s` purely from
  `seconds` and apply `rotate(θ) scale(1 + s, 1 - 0.6s) rotate(-θ)` so objects
  compress and stretch along their trajectory while keeping inner glyphs
  upright.
- **Dual-part overlapping action & anticipation**: split compound icons or
  actors into primary and secondary sub-parts (clapper, arrow tail, shadow)
  with a deterministic `30–50 ms` phase lag or counter-phase swing derived from
  `seconds`, paired with a brief counter-direction anticipation beat and
  piecewise ascent/descent gravity easing.
- **Clip-path / canvas wave dual-tone inversion**: for capacity, liquid-level,
  or fill progress, evaluate the wave or clip geometry purely from `seconds`,
  draw base-color text first, then apply `clip()` / `clip-path` to redraw
  inverted-color text cleanly across the boundary without `Math.random()` or
  `requestAnimationFrame`.
- **Text continuity & thinking cues**: when mutating short phrases or status
  labels, preserve shared characters across frames (TextMorph continuity)
  instead of cross-fading whole blocks. Reserve subtle horizontal Text Shimmer
  strictly for explicit in-progress/thinking states driven from `seconds`.
- **Skeleton-to-content boundary**: pair equal-footprint skeleton placeholders
  with `blurBridge` only when async fetch, streaming inference, or hydration
  latency is part of the story—never add decorative shimmers to static reveals.
- **SVG Gooey strict boundary**: reserve SVG Gooey (`feGaussianBlur` +
  `feColorMatrix`) solely for stylized product-showcase or liquid-metaphor
  scenes; never apply it to technical diagrams, code views, or crisp
  whiteboards where sharp edges carry meaning.
