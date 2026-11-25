# Visual Language & Motion

Design each frame so the viewer *sees the mechanism move* rather than reading a
wall of labeled boxes. Choose a visual system that fits the subject and the
user's taste, keep color/type/stroke discipline consistent across the video, and
state the selected visual direction in the pre-build confirmation snapshot.

## Visual Direction (Paper Whiteboard Is Default Fallback, Not a Lock)

The built-in `assets/player.html` ships a zero-config **paper-and-ink
whiteboard** theme so quick explainers work immediately without authoring custom
HTML. It is a **fallback default, not the only style**. Pick the visual system
that best matches the topic and user preference:

| Visual system | Best fit | Core palette & surface cues |
| --- | --- | --- |
| **Paper & ink physical whiteboard** (built-in default) | Quick concept sketches, analogies, teaching walkthroughs | Paper `#f8f7f2` + 24 px dot grid (`#20272312`), ink `#202723`, highlighter `#ffe066`, path blue `#1769c2`, rough borders, tape strips, sparse semantic stickers |
| **Dark UI slice** | Developer tools, agent loops, APIs, terminal/code architecture | Deep charcoal/slate canvas (`#0d1117` / `#111418`), hairline borders (`1px`), crisp monospace + sans, selective glowing semantic accent (cyan/amber/emerald), cropped real UI/trace surfaces |
| **Swiss editorial typography** | Principles, tradeoffs, mental models, essays, product positioning | High-contrast grid (crisp off-white or pure black), bold grotesque/editorial display type, one decisive accent color, generous negative space |
| **Warm science / editorial illustration** | Physics, math, distributed systems, biology, spatial reasoning | Soft cream/sand canvas, muted cobalt/terracotta/sage tones, organic curves, tactile physical metaphors and measured diagrams |

Offline rendering rules that apply to **every** visual system:

- **One primary focus at a time**: keep accent colors purposeful; reserve red
  for actual errors, drops, or risks.
- **Offline fonts only**: the exporter blocks all network requests. Either
  include `/* motion-explainer-fonts */` (embeds bundled `LXGW WenKai Lite`
  Latin + CJK subsets, SIL OFL 1.1) or use verified local system fonts
  (`PingFang SC`, `SF Pro`, `SF Mono`, `Helvetica Neue`, `Georgia`, etc.) and
  verify CJK/Latin/symbol glyph coverage in rendered frames.
- **Semantic symbols over decoration**: when using icons or emoji (`📨 Request`,
  `📦 Cache`, `🗄️ Database`, `🔒 Lock`), bind each symbol to a concrete object
  and keep it consistent whenever that object recurs.

## Anti-Pattern: Wall-to-Wall 1-2-3 Equal-Width Boxes

Avoid turning every scene into **three equal-width horizontal cards with
arrows** ("通篇 1-2-3 等宽横排方框"). Repeating uniform boxed cards across scenes:

- flattens different causal structures (pipelines, trade-offs, hierarchies,
  state mutations, timelines, UI interactions) into identical slide templates;
- pushes the viewer to read static paragraphs inside boxes instead of watching
  an object transform;
- wastes canvas space on decorative card borders and padding.

Use the built-in `flow` layout only when a simple 2–5 step pipeline genuinely
fits; otherwise switch the scene to `layout: "custom"` with a tailored
`--player` powered by `/* motion-explainer-kit */`.

## De-Carded Composition & Motion Vocabulary

Pick compositions and `window.MotionKit` primitives that embody the causal
mechanism directly:

1. **Living sentence & inline elastic slot** (`MotionKit.inlineSlot`):
   Place one sharp sentence or equation directly on open canvas; when the
   narration hits a keyword cue, push neighboring words apart elastically to
   insert a live badge, constraint, or counter-value right inside the sentence.
2. **Physical container ingestion & stacking** (`MotionKit.spring` + `MotionKit.impact`):
   Represent caches, queues, buffers, context windows, and stacks as physical
   vessels that swallow, compress, bounce, or evict items on contact rather than
   toggling highlight borders on static rectangles.
3. **Conversation & tool-call stream morphing** (`MotionKit.pillMorph` + `MotionKit.wipeClip`):
   Anchor a compact pill or chat bubble to one edge and stretch it open smoothly
   as arguments or results arrive; swap status labels in place with a horizontal
   clip wipe instead of popping whole new cards onto the screen.
4. **Topology lift-and-reposition** (`MotionKit.spring` + `MotionKit.smear` + `MotionKit.impact`):
   Show before/after architecture or refactoring on the *same* nodes: lift a
   node out of its old slot, travel along a curved path with velocity-aligned
   smear, and settle into the new topology with a subtle landing impact.
5. **Cropped UI slices & virtual camera push** (`MotionKit.camera`):
   Instead of shrinking an entire dashboard, terminal, or diagram into an
   unreadable overview, crop to the decisive slice and smoothly pan/push the
   virtual camera onto the exact line, metric, or control being spoken about.
6. **Cross-container inverse-color absorption**:
   When a token, request, or state crosses a real boundary (client → server,
   draft → committed, dark sandbox → light host, user space → kernel), invert
   its surface/ink palette as it passes the threshold so the boundary crossing
   reads instantaneously.
7. **2.5D physical vitality on any protagonist** (`MotionKit.sphereEyes` + `MotionKit.deterministicBlink` + `MotionKit.impact`):
   Optionally give subtle gaze, deterministic blinking, or breathing bounce to
   whatever domain object owns the scene—a request packet, token orb, lock,
   cursor, or router node—rather than inventing an unrelated fixed mascot.

8. **Blur-bridged transitions & rolling metrics** (`MotionKit.blurBridge` + `MotionKit.rollingDigits`):
   Bridge adjacent states with a light `blur(3–4px) → 0` handoff starting from
   `scale(0.95)` instead of hard cuts; animate numeric deltas with tabular
   per-digit rolling columns so unchanged digits stay rock-steady.
9. **Directed path beams & depth-stacked history** (`MotionKit.beamPath` + `MotionKit.stackedDeck`):
   Send a deterministic pulse along an SVG `<path>` (single-direction or
   bidirectional) to show active dataflow, and layer prior events in a
   Sonner-style depth deck (`translateY / scale / opacity / zIndex`) that
   expands cleanly on cue without losing history context.

## Motion Craft Guardrails

- **Never pop from `scale(0)`**: enter objects from `scale(0.94–0.96)` with
  short travel so geometry feels grounded rather than explosive.
- **Anchor `transform-origin`**: set `transform-origin` to the actual trigger
  edge, parent attachment, or focal hinge before scaling or morphing.
- **Asymmetric enter/exit timing**: let exiting elements clear slightly faster
  (`~200–280 ms`) than entrances (`~320–550 ms`) so departing state never drags
  across the next beat.
- **Text continuity & thinking cues**: when mutating short phrases or status
  lines, preserve shared characters across frames (TextMorph continuity) instead
  of cross-fading whole blocks; reserve subtle horizontal Text Shimmer for
  explicit in-progress/thinking states (driven deterministically from `seconds`,
  never CSS autoplay loops).
- **SVG Gooey boundary**: reserve SVG Gooey (`feGaussianBlur` + `feColorMatrix`)
  strictly for stylized product-showcase or liquid-metaphor demos; never apply
  it to technical diagrams, code views, or whiteboard scenes where crisp edges
  carry meaning.

### New Deterministic Primitives Quick Index

| Primitive | Signature | Key outputs |
| --- | --- | --- |
| `MotionKit.blurBridge` | `(age, { duration, maxBlur, fromScale=0.95, settled })` | `opacity`, `scale`, `blur`, `filter`, `transform` |
| `MotionKit.rollingDigits` | `(fromStr, toStr, progress, { stagger, direction, settled })` | `columns[]` (`changed`, `offset`, `stripTransform`), `text` |
| `MotionKit.beamPath` | `(seconds, { pathLength, pulseLength, period, direction, settled })` | `progress`, `direction`, `strokeDasharray`, `strokeDashoffset`, `opacity` |
| `MotionKit.stackedDeck` | `(index, count, expandedProgress, { collapsedGap, expandedGap, settled })` | `translateY`, `scale`, `opacity`, `zIndex`, `transform` |

## Match Composition to the Question

| What you are explaining | Preferred composition |
| --- | --- |
| A key definition or constraint modifying a claim | Living sentence with inline elastic slot (`inlineSlot`) |
| Queuing, caching, eviction, or memory pressure | Physical vessel ingestion/stacking (`spring` + `impact`) |
| Agent loops, tool calls, or request/response dialogue | Single-edge anchored pill morph + clip wipe (`pillMorph` + `wipeClip`) |
| Before vs after / refactoring / routing change | Same objects lifting and re-seating in place (`spring` + `smear`), or inverse-color boundary crossing |
| Deep UI, trace, or complex diagram inspection | Cropped UI slice with virtual camera pan/push (`camera`) |
| Which lines of code changed behavior | Trimmed code (<= 12 lines) with sliding highlight |
| Numeric before/after metrics or counters | Tabular per-digit roll (`rollingDigits`) + blur handoff (`blurBridge`) |
| Active dataflow, routing, or retry loop | Directed SVG path pulse (`beamPath`) |
| Multi-step event history / notification stack | Depth-stacked deck expanding on demand (`stackedDeck`) |
| Simple linear 2–5 step pipeline | Built-in `flow` layout (default fallback) |

## Density & Pacing Discipline

- **One idea per scene, low text density**: never pack multi-sentence cards onto
  the stage. Show objects, geometry, and short labels; let the narration explain
  the *why*.
- **Progressive mutation over static dumps**: establish spatial anchors once and
  evolve them through `anchors` / `cues` (`focus`, `show`, or custom `state` /
  `action` / `badge` / `data`). Mutate existing objects in place rather than
  appending extra summary boxes.
- **Deterministic physics from `seconds` only**: settle entrances cleanly with
  closed-form springs (`300–650 ms`), land keyword accents within `200–350 ms`,
  and hold resting poses long enough to read. Never use wall-clock time,
  `Math.random()`, `requestAnimationFrame`, or CSS autoplay loops.

## Watching & Listening Self-Check

Before delivery, inspect real frames from `video.mp4` at normal viewing size
(not just `audit()`):

1. Does the visual style fit the topic, and does the composition avoid repetitive
   1-2-3 equal-width box layouts?
2. Is the current question or takeaway readable in one glance with low text density?
3. Do visual transitions, camera moves, and keyword highlights land cleanly on
   the spoken words?
4. Do all fonts render cleanly offline, and do visual elements stay well clear
   of the caption safe zone?
5. Does reverse seeking restore the exact earlier frame state?
6. Is narration volume balanced, pacing natural, and free of clipped words or
   jarring cross-beat shifts?
