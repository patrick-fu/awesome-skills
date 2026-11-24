# Storyboard & Rendering Contract

A storyboard is a UTF-8 JSON file (`version: 1`) containing metadata and an
ordered list of `scenes`, each with one or more narration `beats`. Validate
changes before rendering:

```bash
uv run --no-project scripts/motion_explainer.py validate storyboard.json
```

---

## Top-Level Fields

| Field | Required | Meaning |
| --- | --- | --- |
| `version` | Yes | Must be `1` |
| `title` | Yes | Video title and MP4 metadata title |
| `language` | No | BCP-47 tag (`zh-CN`, `en-US`, `ja-JP`, `ko-KR`, ...); defaults to `zh-CN` in `prepare_speech.py` |
| `speech_provider` | No | `auto`, `doubao`, `qwen3-mlx`, `edge`, or `supplied` |
| `voice` | No | Voice ID for the selected TTS provider (or macOS `say` fallback) |
| `speech_rate` | No | Words per minute for macOS `say` (`80–400`, default `180`) |
| `tts_command` | No | Direct CLI fallback without word timestamps; argv array containing `{text_file}`, `{output}`, optional `{voice}` |
| `scenes` | Yes | Non-empty scene list |

---

## Speech Preparation & Beats

Run `prepare_speech.py` to generate per-beat audio, aligned word timestamps, and
keyword-synced visual cues:

```bash
uv run --no-project scripts/prepare_speech.py storyboard.json \
  --out /path/to/artifacts/speech \
  --provider auto
```

Write each beat's `narration` as one complete semantic thought (may span
multiple sentences) and place mid-beat visual changes in `anchors`:

| Field | Meaning |
| --- | --- |
| `delivery.instruction` | Natural-language speaking direction (used by `doubao` and `qwen3-mlx`) |
| `delivery.speed` | `0.5–2.0`, default `1.0` |
| `pause_ms` | Trailing silence after the beat (`0–30000`, default `350`); aligned upward to video frames |
| `anchors` | Keyword string or `{word, occurrence?, focus?, show?, ...custom}` object |

`occurrence` is 1-based (default `1`); matching ignores punctuation, spaces, and
ASCII letter case. `focus` and `show` take effect at the first video frame
reaching the keyword's start timestamp (`~33.3 ms` per frame at 30 fps).

Anchors may also carry **custom semantic fields** (such as `state`, `action`,
`badge`, `data`, `camera`, etc.) alongside or instead of `focus` / `show`.
`prepare_speech.py` preserves all custom fields on generated `cues` (stripping
only the matching directive `occurrence` and writing authoritative `word`,
`start`, `end`). Example (built-in `flow` beat):

```json
{
  "narration": "第一次请求，缓存里还没有答案。去数据库，取回来，再存一份。",
  "pause_ms": 480,
  "focus": [],
  "show": 1,
  "anchors": [
    {"word": "请求", "focus": [0]},
    {"word": "缓存", "focus": [1], "show": 2},
    {"word": "数据库", "focus": [2], "show": 3},
    {"word": "取回来", "focus": [1]}
  ]
}
```

Example (`layout: "custom"` beat with semantic cues):

```json
{
  "narration": "请求一进网关，先命中热缓存，三毫秒内直接返回。",
  "pause_ms": 420,
  "anchors": [
    {"word": "网关", "state": "enter", "action": "push-camera", "data": {"target": "gateway"}},
    {"word": "热缓存", "state": "hit", "badge": "HIT", "action": "absorb"},
    {"word": "返回", "state": "return", "badge": "3ms"}
  ]
}
```

`prepare_speech.py` writes `speech/storyboard.json` along with per-beat `.wav`,
`.words.json`, `.request.json`, and `speech-session.json` (storing provider,
request sequence SHA-256, and `section_id` for Doubao):

- `audio`: relative WAV path.
- `words`: `[{"text": "...", "start": 0.2, "end": 0.8}]` with original
  punctuation/spaces restored for karaoke captions.
- `cues`: `[{"word": "...", "start": 0.2, "end": 0.8, ...preservedFields}]`.

### Cache & Safety Rules

- Re-running `prepare_speech.py` on the same output directory reuses cached
  audio offline when narration, voice, provider, delivery parameters, and beat
  order are unchanged—so editing layouts, custom cue fields, pauses, or
  `anchors` triggers **zero** synthesis calls.
- If narration text, voice, provider, delivery settings, beat order, or cached
  files change—or if a previous run partially failed—`prepare_speech.py` stops
  before making any new request and asks for a new output directory.
- Beats with supplied `audio` are validated before any billable or network
  request and are never uploaded into server context.
- `motion_explainer.py build` rejects unprepared `delivery` or `anchors` so
  configurations are never silently ignored.

### Direct `tts_command` (Optional Without Word Timestamps)

When skipping `prepare_speech.py` and building directly with an external CLI,
`tts_command` is an argv array containing `{text_file}`, `{output}`, and
optionally `{voice}`:

```json
{
  "voice": "en-US-AndrewNeural",
  "tts_command": [
    "uv", "run", "--no-project", "--with", "edge-tts==7.3.1",
    "edge-tts", "--voice", "{voice}", "--file", "{text_file}",
    "--write-media", "{output}"
  ]
}
```

When `words` are absent (external recording or `tts_command` / `say`), keep each
beat's narration within two caption lines so on-screen captions remain unclipped.

---

## Scenes

| Field | Meaning |
| --- | --- |
| `id` | Unique short ID (`[a-zA-Z0-9_-]+`) |
| `layout` | `title`, `flow`, `code`, or `custom` |
| `title` | Scene heading (question or takeaway) |
| `text` | Optional short supporting note |
| `items` | Required for `flow` (2–5 short labels; optional leading emoji separated by a space, e.g. `"📦 Cache"`); optional/unused for `custom` |
| `code` | Required for `code` (multiline snippet, max 12 lines); optional/unused for `custom` |
| `beats` | Non-empty narration beat list |

Visual state fields:

- For `title` / `flow` / `code`: `focus` (0-based indexes within `items` or
  `code` lines; must be empty for `title`) and `show` (1-based count of visible
  elements; must include every index in `focus`; omitted means show all).
- For `custom`: `items` and `code` are **not** required. Scenes may carry
  arbitrary domain properties (such as `theme`, `props`, `nodes`, `data`), and
  beats/anchors/cues may omit `focus`/`show` or use optional non-negative
  `focus` indexes and positive `show` counts alongside custom semantic cue
  fields (`state`, `action`, `badge`, `data`, etc.).

---

## Outputs, Bundling Placeholders & `MotionKit` Contract

`motion_explainer.py build` writes to a new directory or one carrying
`.motion-explainer`:

- `video.mp4` (H.264 / AAC / `mov_text`, default `1280×720`, `24` fps;
  `--width 1920 --fps 30` supported)
- `storyboard.json`, `player.html` (self-contained offline bundle),
  `timeline.json`, `captions.srt`, `poster.png`, `manifest.json`, `audio/`,
  `frames/`

### Offline Bundling Placeholders (`bundle_player`)

When building with default `assets/player.html` or a custom `--player
/path/to/player.html`, `bundle_player()` expands two optional placeholders so
the exported `player.html` renders with all network requests blocked:

- `/* motion-explainer-fonts */` (in `<style>`): embeds bundled `LXGW WenKai
  Lite` Latin + CJK subsets (`Motion Hand`, SIL OFL 1.1). Omit if your custom
  visual style uses local system fonts.
- `/* motion-explainer-kit */` (in `<script>`): inlines `assets/motion-kit.js`,
  exposing `window.MotionKit`.

### Shared Runtime (`window.MotionKit`)

1. **Engineering shell — `MotionKit.createPlayerShell(config)`**:
   Registers `window.motionExplainer` (and legacy alias `window.animatic`) so
   custom players keep every engineering guardrail without boilerplate:
   - `1280×720` proportional stage scaling (`#stage`), document title & lang.
   - Word-synced karaoke caption pagination (`#caption`) with sentence/clause
     punctuation priority and automatic reflow on `document.fonts` load.
   - Bottom progress bar (`#progress`).
   - Multi-page `audit()` verifying stage overflow, clipped text across every
     caption page, caption clearance, and title/narration presence.
   - Precomputed `cueTrack`, `activeCue`, `activeState`, and `triggeredCues`
     passed into `onSeek(frame)`.

   Minimal custom player skeleton:

   ```html
   <main id="stage">
     <div id="scene-root"></div>
     <p id="caption"></p>
     <div id="progress"></div>
   </main>
   <script>
     /* motion-explainer-kit */
     const { spring, camera, pillMorph, createPlayerShell } = window.MotionKit;
     createPlayerShell({
       stage: '#stage',
       caption: '#caption',
       progress: '#progress',
       auditRoot: '#scene-root',
       auditSelector: 'h1,[data-audit]',
       onSeek(frame) {
         // Purely deterministic render from frame.time, frame.sceneAge,
         // frame.activeState, frame.activeCue, and frame.settled
       },
     });
   </script>
   ```

2. **Stateless deterministic motion primitives** (pure functions of time/inputs;
   exact forward & reverse `seek()` and `settled=true` support):
   - `spring(age, {stiffness, damping, mass, velocity, from, to, settled})` /
     `springState(...)`: closed-form underdamped/critical/overdamped spring.
   - `impact(age, {intensity, frequency, damping, axis, offset, settled})`:
     volume-preserving squash-and-stretch landing recoil.
   - `smear(vx, vy, {strength, maxStretch, settled})`: velocity-aligned motion
     stretch (`transform` keeping upright content; `capsuleTransform` oriented).
   - `sphereEyes(yaw, pitch, {radius, eyeSpacing, eyeY, maxAngle, radians})`:
     2.5D orthographic spherical gaze projection (opt-in for any subject).
   - `inlineSlot(age, {targetWidth, pad, duration, stiffness, damping, settled})`:
     elastic in-line word/chip slot expansion.
   - `wipeClip(age, {duration, direction, ease, settled})`: directional
     `clip-path: inset(...)` mask swap (`incomingClip` / `outgoingClip`).
   - `pillMorph(age, {fromWidth, toWidth, fromHeight, toHeight, anchor, stiffness, damping, settled})`:
     single-edge anchored bubble/pill width & height expansion.
   - `camera(keyframes, seconds, {stageWidth, stageHeight, settled})`: virtual
     camera pan/zoom/rotate (`[{t, x, y, zoom, rotate, ease, spring}]`).
   - `deterministicBlink(seconds, {interval, blinkDuration, seed, doubleBlinkEvery, breathPeriod, settled})`:
     zero-RNG deterministic blink and subtle breathing oscillation.

### Low-Level Renderer Contract (`window.motionExplainer`)

If writing a renderer without `createPlayerShell`, implement
`window.motionExplainer` directly (legacy alias `window.animatic` is accepted):

- `load({storyboard, timeline, width})`: initialize stage at `1280×720` scaled
  cleanly to `width`.
- `seek(seconds, settled)`: render exact state for `seconds` (`settled=true`
  jumps to the beat's resting state). Must be purely a function of `seconds`—
  never rely on wall-clock time, `Math.random()`, or CSS autoplay animations.
- `audit()`: return an array of error strings catching stage overflow, clipped
  text (across every caption page), caption overlap, and missing
  title/narration.
