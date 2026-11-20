# Visual Language & Motion

Design each frame like explaining a mechanism on clean paper: hand-drawn frames,
ink lines, yellow highlighter focus, and sparse semantic stickers. Keep colors,
stroke weights, and typography consistent while letting each scene's layout fit
the question it answers.

## Visual Tokens

- **Paper & ink**: light paper canvas `#f8f7f2` (or crisp white) with a subtle
  24 px dot grid (`#20272312`). Primary ink `#202723` at 85% / 40% / 15% opacity
  tiers.
- **Focus & path**: highlighter yellow `#ffe066` marks the active focus; path
  blue `#1769c2` traces data/control flow; introduce red only for real risks or
  failures. Keep **one primary focus at a time** and leave already-explained
  objects in place.
- **Typography**: handwritten face for headings, labels, and brief notes;
  monospace for code, paths, and numbers. The default `player.html` embeds the
  bundled `LXGW WenKai Lite` Latin + CJK subsets (`assets/fonts/`, SIL OFL 1.1)
  so offline rendering needs no external network or other skills. For Japanese,
  Korean, or other scripts, verify glyph coverage in rendered frames and add
  local system fallbacks if needed.
- **Tactile paper cues**: 1.5–2 px rough-radius frames, 3–5 px hard offset
  shadows, masking tape strips, highlighter sweeps, and sticky notes—subtle
  enough that they never obscure text.
- **Semantic emoji**: attach an emoji to a concrete object (`📨 Request`,
  `📦 Cache`, `🗄️ Database`, `🔒 Lock`) and keep the same symbol whenever that
  object recurs. Avoid decorative floating icons.

## Match Composition to the Question

| What you are explaining | Best layout |
| --- | --- |
| Where data or control moves | Object nodes, drawn arrows, moving packet |
| Before vs after / why something changed | Same set of objects transitioning in place, or side-by-side contrast |
| Sequence or wait time | Shared-axis timeline |
| Ownership across layers | Horizontal bands or swimlanes |
| Which lines changed behavior | Trimmed code (<= 12 lines) with sliding pencil highlight |
| One core takeaway | Bold takeaway card, highlighter sweep, minimal annotation |

The default template provides `title`, `flow`, and `code`. When the story calls
for a comparison, timeline, or layered architecture, customize the task's
`player.html` while keeping the `window.motionExplainer` contract.

## Density & Pacing Discipline

- **One idea per scene, low text density**: avoid turning scenes into dense
  slide decks packed with multi-sentence cards. Put relationships and short
  labels on screen; let the narration explain the *why*.
- **Progressive change over static dumps**: pre-place the scene's complete
  geometry, then reveal elements and move focus step by step via `show`,
  `focus`, and keyword `anchors`. When showing a multi-step cause-and-effect,
  mutate the same objects in place rather than stacking extra summary boxes.
- **Purposeful motion**: cards settle lightly (300–650 ms), arrows draw along
  the path, highlighter sweeps on keywords (200–350 ms), stickers stamp gently.
  Hold elements steady after entry so viewers have time to read. Compute every
  frame strictly from `seconds` passed to `seek()`.

## Watching & Listening Self-Check

Before delivery, inspect real frames from `video.mp4` at normal viewing size
(not just `audit()`):

1. Is the current question or takeaway readable in one glance?
2. Is on-screen text sparse enough to read while listening, with no dense walls of cards?
3. Do visual transitions and highlights land cleanly on the spoken keywords?
4. Do emoji map to real objects, and do tape/borders stay clear of text and captions?
5. Does reverse seeking restore the exact earlier frame state?
6. Is narration volume balanced, pacing natural, and free of clipped words or jarring cross-beat shifts?
