# Visual Direction & Style Purity

Design every frame so the viewer *sees the causal mechanism move* instead of
scanning boxed slides. Pick the visual system that fits the subject and user
taste, enforce offline style purity, and load the detailed motion references
below when choreographing scenes or coding `player.html`.

## Choose a Visual System for the Subject

Treat visual direction as a deliberate first decision—paper-and-ink whiteboard
is only the built-in zero-config fallback, never a mandatory default. State the
selected system in the pre-build confirmation snapshot:

| Visual system | Best fit | Core palette & surface cues |
| --- | --- | --- |
| **Dark UI slice** | Developer tools, agent loops, APIs, terminal/code architecture | Charcoal/slate canvas (`#0d1117` / `#111418`), `1px` hairlines, crisp monospace + sans, selective glowing semantic accent (cyan/amber/emerald), cropped UI/trace surfaces |
| **Swiss editorial typography** | Principles, tradeoffs, mental models, essays, positioning | High-contrast grid (crisp off-white or black), bold grotesque/editorial display type, one decisive accent color, generous negative space |
| **Warm science / editorial illustration** | Physics, math, distributed systems, biology, spatial reasoning | Soft cream/sand canvas, muted cobalt/terracotta/sage tones, organic curves, physical metaphors and measured diagrams |
| **Paper & ink whiteboard** *(fallback)* | Quick concept sketches, analogies, teaching walkthroughs | Paper `#f8f7f2` + 24 px dot grid (`#20272312`), ink `#202723`, highlighter `#ffe066`, path blue `#1769c2`, rough borders, tape strips, sparse semantic stickers |

## Offline Rendering & Anti-Slop Purity

These guardrails apply across every visual system:

- **One primary focus at a time**: keep accent colors purposeful; reserve red
  for real errors, drops, or risks.
- **One idea per scene, low text density**: never pack multi-sentence cards
  onto the stage. Show objects, geometry, and short labels; let narration carry
  the explanation.
- **Offline fonts only**: headless rendering blocks all network traffic. Either
  inline `/* motion-explainer-fonts */` (bundled `LXGW WenKai Lite` Latin + CJK
  subsets, SIL OFL 1.1) or use verified local system fonts (`PingFang SC`,
  `SF Pro`, `SF Mono`, `Helvetica Neue`, `Georgia`, etc.) and verify glyph
  coverage in rendered frames.
- **Frame purity & numeric discipline**: open straight on the headline or
  mechanism—omit reflexive `ALL CAPS` eyebrow kickers, non-interactive
  decorative pills, nested cards-inside-cards, decorative `01/02` prefixes when
  sequence is not real, and fake `"LIVE"` badges. Render numbers with
  `font-variant-numeric: tabular-nums` instead of adding a third font family.
- **Intentional palette & image negative space**: never default reflexively to
  off-topic beige or generic AI purple. Over full-bleed visuals or
  illustrations, reserve clean negative space that meets contrast directly
  instead of covering the frame in a muddy dark scrim.
- **Semantic symbols over decoration**: when using icons or emoji
  (`📨 Request`, `📦 Cache`, `🗄️ Database`, `🔒 Lock`), bind each symbol to a
  concrete object and reuse it consistently whenever that object recurs.

## Progressive Motion References (Load on Demand)

Load only what the current production step needs:

| Need | Load reference |
| --- | --- |
| Choosing scene compositions, avoiding 1-2-3 equal-width box layouts, or applying motion craft guardrails (`scale(0.95)`, FLIP, TextMorph, X-Ray, Split-Flap, SVG Gooey boundaries) | [Choreography & Pattern Dictionary](motion/choreography.md) |
| Calling `window.MotionKit`'s 15 stateless deterministic primitives or `createPlayerShell` inside a custom `player.html` | [MotionKit API Reference](motion/kit-api.md) |

## Watching & Listening Self-Check

Before delivery, inspect real frames extracted from `video.mp4` at normal
viewing size (not just `audit()`):

1. Does the visual system fit the subject, and does every scene match its
   causal mechanism instead of repeating uniform equal-width boxes?
2. Is the current question or takeaway readable in one glance with low text
   density?
3. Do visual transitions, camera moves, and keyword accents land cleanly on the
   spoken words?
4. Do all fonts render cleanly offline, and do visual elements stay clear of
   the caption safe zone?
5. Does reverse seeking restore the exact earlier frame state?
6. Is narration loudness balanced, pacing natural, and free of clipped words or
   jarring cross-beat shifts?
