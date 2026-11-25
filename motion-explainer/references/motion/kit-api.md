# MotionKit API Reference

Load this reference when coding a custom `player.html` with
`/* motion-explainer-kit */`. `bundle_player()` inlines `assets/motion-kit.js`
and exposes `window.MotionKit`. Every primitive is stateless, pure in
time/inputs, safe for forward and reverse `seek()`, and honors `settled: true`.

## Stage Constants & Helpers

- `STAGE_WIDTH` (`1280`), `STAGE_HEIGHT` (`720`)
- `clamp(value, min = 0, max = 1)`
- `mix(a, b, t)`
- `easeOutCubic(t)`, `easeInOutCubic(t)`
- `element(tag, className, text)` — creates a DOM node concisely

## 15 Deterministic Motion Primitives

| # | Primitive | Signature & Defaults | Key Return Fields |
| --- | --- | --- | --- |
| 1 | `spring` / `springState` | `(age, { stiffness=220, damping=18, mass=1, velocity=0, from=0, to=1, settled=false, restDelta=1e-4 })` | `spring` returns scalar `value`; `springState` returns `{ value, velocity, done }` |
| 2 | `impact` | `(age, { intensity=0.22, frequency=16, damping=7.5, axis='y', offset=8, settled=false })` | `{ scaleX, scaleY, offsetX, offsetY, energy, transform }` |
| 3 | `smear` | `(vx, vy, { strength=0.00045, maxStretch=0.55, settled=false })` | `{ angle, stretch, squash, speed, transform, capsuleTransform }` |
| 4 | `sphereEyes` | `(yaw=0, pitch=0, { radius=40, eyeSpacing=22, eyeY=-4, maxAngle=55, radians=false })` | Left/right projected eye coordinates, squash & visibility |
| 5 | `inlineSlot` | `(age, { targetWidth=120, pad=0, duration=0.45, stiffness=240, damping=19, settled=false })` | `{ width, opacity, scale, progress }` |
| 6 | `wipeClip` | `(age, { duration=0.42, direction='left-to-right', ease=easeInOutCubic, settled=false })` | `{ progress, incomingClip, outgoingClip }` (`clip-path: inset(...)`) |
| 7 | `pillMorph` | `(age, { fromWidth=48, toWidth=280, fromHeight, toHeight, anchor='left', stiffness=220, damping=20, settled=false })` | `{ width, height, progress, transformOrigin }` |
| 8 | `camera` | `(keyframes, seconds, { stageWidth=1280, stageHeight=720, settled=false })` (`keyframes`: `[{ t, x, y, zoom, rotate, ease, spring }]`) | `{ x, y, zoom, rotate, transform, transformOrigin }` |
| 9 | `deterministicBlink` | `(seconds, { interval=3.6, blinkDuration=0.14, seed=0, doubleBlinkEvery=3, breathPeriod=2.8, settled=false })` | `{ open, scaleY, closed, breath, bobY }` |
| 10 | `blurBridge` | `(age, { duration=0.36, maxBlur=4, fromScale=0.95, toScale=1, fromOpacity=0, toOpacity=1, offsetY=6, ease=easeOutCubic, settled=false })` | `{ opacity, scale, blur, offsetY, filter, transform }` |
| 11 | `rollingDigits` | `(fromStr, toStr, progress, { settled=false, stagger=0.08, direction='auto', ease=easeOutCubic, lineHeight=1, padChar=' ' })` | `{ columns: [{ from, to, changed, offset, stripTransform }], text, progress }` |
| 12 | `beamPath` | `(seconds, { pathLength=240, pulseLength=44, period=1.6, phase=0, direction='forward', settled=false, settledProgress=1 })` | `{ progress, direction, strokeDasharray, strokeDashoffset, opacity }` |
| 13 | `stackedDeck` | `(index, count, expandedProgress, { collapsedGap=14, expandedGap=86, scaleStep=0.05, opacityStep=0.14, maxVisible=4, baseZIndex=10, direction='up', settled=false, settledExpanded=1 })` | `{ translateY, scale, opacity, zIndex, visible, transform }` |
| 14 | `morphPath` | `(pointsA, pointsB, progress, { smooth=true, closed=false, precision=2, ease=null, settled=false })` | `{ d, points, progress, count }` |
| 15 | `microBurst` | `(age, { count=8, duration=0.35, radius=46, spread=2π, startAngle=-π/2, gravity=16, minScale=0.55, maxScale=1.05, maxRotation=160, seed=1, originX=0, originY=0, settled=false })` | `{ active, progress, count, particles: [{ x, y, scale, rotation, opacity, transform }] }` (`count` clamped to `6..12`) |

## Player Shell — `MotionKit.createPlayerShell(config)`

Registers `window.motionExplainer` (and legacy alias `window.animatic`) and
handles scaling, word-synced karaoke caption pagination, progress bar, cue
state resolution, and multi-page `audit()`.

### Config Options

| Option | Default | Meaning |
| --- | --- | --- |
| `stage` | `'#stage'` | Selector or element for the `1280×720` stage |
| `caption` | `'#caption'` | Selector or element for karaoke subtitles |
| `progress` | `'#progress'` | Selector or element for the bottom progress bar |
| `auditRoot` | `stage` | Container inspected by `audit()` |
| `auditSelector` | `'h1,.support,.node,.code-line,[data-audit]'` | Elements checked for clipping, overflow, and caption clearance |
| `titleSelector` | `'h1,[data-title]'` | Required visible title check (disable with `requireTitle: false`) |
| `captionClearance` | `16` | Minimum pixel gap above `#caption` |
| `onLoad(ctx)` | optional | Called once during `load({storyboard, timeline, width})` |
| `onSeek(frame)` | required | Called on every `seek(seconds, settled)` |
| `onAudit(ctx)` | optional | Return extra error strings appended to `audit()` |

### `onSeek(frame)` Payload

- `time`, `settled`, `totalDuration`
- `storyboard`, `timeline`, `scenes`, `visualTracks`
- `beatIndex`, `beat`, `beatAge`
- `sceneIndex`, `scene`, `sceneMeta`, `sceneAge`
- `cueTrack` (ordered beat events), `activeCue` (most recent triggered cue),
  `activeState` (accumulated cue fields across the beat, including `state`,
  `action`, `badge`, `data`, `focus`, `show`), `triggeredCues`
