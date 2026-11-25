# Storyboard & Player Contract

A storyboard is a UTF-8 JSON file (`version: 1`) containing metadata and an
ordered list of free-form `scenes`, each carrying its own domain data and one
or more narration `beats`. Validate changes before rendering:

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

## Free-Form Scenes (Primary Schema)

Each scene defines only the fields its custom stage needs—no `layout` field is
required:

| Field | Required | Meaning |
| --- | --- | --- |
| `id` | Yes | Unique ASCII identifier (`[a-zA-Z0-9_-]+`) |
| `title` | Yes | Scene headline (newlines allowed) |
| `text` | No | Optional short supporting line |
| `beats` | Yes | Non-empty list of narration beats |
| *custom domain fields* | No | Any JSON fields consumed by your `player.html` (e.g. `stage`, `theme`, `nodes`, `metrics`, `layers`, `snippet`, `props`) |

Example layout-free scene with custom data and semantic word cues (see full
runnable starter in [assets/example.free.zh.json](../assets/example.free.zh.json)):

```json
{
  "id": "hot-cache",
  "title": "命中热缓存，三毫秒直返",
  "metrics": { "before": "148ms", "after": "3ms" },
  "beats": [
    {
      "narration": "请求一进网关，先命中热缓存，三毫秒内直接返回，数据库根本不用醒来。",
      "pause_ms": 420,
      "anchors": [
        {"word": "网关", "state": "enter", "action": "push-camera", "data": {"target": "gateway"}},
        {"word": "热缓存", "state": "hit", "badge": "HIT", "action": "absorb"},
        {"word": "三毫秒", "state": "metric", "data": {"latency": "3ms"}},
        {"word": "数据库", "state": "idle-db", "badge": "0 QPS"}
      ]
    }
  ]
}
```

*Legacy compatibility*: existing storyboards that set `layout` to `"title"`,
`"flow"` (with 2–5 `items`), `"code"` (with `code` up to 12 lines), or
`"custom"` remain silently supported by `validate`, `prepare_speech.py`, and
the zero-config fallback `assets/player.html`.

---

## Speech Preparation, Beats & Anchors

Run `prepare_speech.py` to generate per-beat audio, aligned word timestamps,
and keyword-synced cues:

```bash
uv run --no-project scripts/prepare_speech.py storyboard.json \
  --out /path/to/artifacts/speech \
  --provider auto
```

Write each beat's `narration` as one complete semantic thought (may span
multiple sentences) and place mid-beat visual state shifts in `anchors`:

| Field | Meaning |
| --- | --- |
| `narration` | Spoken text for this beat (required, non-empty) |
| `delivery.instruction` | Natural-language speaking direction (`doubao`, `qwen3-mlx`) |
| `delivery.speed` | `0.5–2.0`, default `1.0` |
| `pause_ms` | Trailing silence after the beat (`0–30000`, default `350`), rounded up to whole video frames |
| `anchors` | Keyword string or `{word, occurrence?, ...custom}` object carrying arbitrary semantic fields (`state`, `action`, `badge`, `data`, `camera`, etc.) and optional non-negative `focus` / positive `show` |

`occurrence` is 1-based (default `1`); matching ignores punctuation, spaces,
and ASCII letter case. `prepare_speech.py` preserves every custom field on
generated `cues` (stripping only `occurrence` and writing authoritative `word`,
`start`, `end`), taking effect at the first video frame reaching `start`
(`~33.3 ms` at 30 fps).

`prepare_speech.py` writes `speech/storyboard.json` along with per-beat `.wav`,
`.words.json`, `.request.json`, and `speech-session.json`:

- `audio`: relative audio path.
- `words`: `[{"text": "...", "start": 0.2, "end": 0.8}]` with original
  punctuation/spaces restored for karaoke captions.
- `cues`: `[{"word": "...", "start": 0.2, "end": 0.8, ...preservedFields}]`.

### Cache & Safety Rules

- Re-running `prepare_speech.py` on the same output directory reuses cached
  audio offline when narration, voice, provider, delivery parameters, and beat
  order are unchanged—so editing custom scene fields, cue payloads, pauses, or
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
`tts_command` is an argv array containing `{text_file}` and `{output}` (and
optional `{voice}`). Audio-file paths in `beat.audio` resolve relative to the
storyboard file.

---

## Custom `player.html` & Offline Bundling

Build against your scene-specific player with `--player /path/to/player.html`.
`motion_explainer.py build` writes to a new directory or one carrying
`.motion-explainer`:

- `video.mp4` (H.264 / AAC / `mov_text`, default `1280×720`, `24` fps;
  `--width 1920 --fps 30` supported)
- `storyboard.json`, `player.html` (self-contained offline bundle),
  `timeline.json`, `captions.srt`, `poster.png`, `manifest.json`, `audio/`,
  `frames/`

### Bundling Placeholders (`bundle_player`)

Because the headless renderer aborts all network requests, `bundle_player()`
expands two optional placeholders inline into the exported `player.html`:

- `/* motion-explainer-kit */` (inside `<script>`): inlines
  `assets/motion-kit.js`, exposing `window.MotionKit`.
- `/* motion-explainer-fonts */` (inside `<style>`): embeds bundled `LXGW
  WenKai Lite` Latin + CJK subsets (`Motion Hand`, SIL OFL 1.1). Omit when
  your chosen visual system uses local system fonts.

### Recommended Shell (`MotionKit.createPlayerShell`)

Use `MotionKit.createPlayerShell(config)` to inherit `1280×720` proportional
stage scaling (`#stage`), word-synced karaoke caption pagination (`#caption`),
progress bar (`#progress`), precomputed `cueTrack` / `activeCue` /
`activeState` / `triggeredCues`, and multi-page `audit()` without boilerplate:

```html
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    * { box-sizing: border-box; }
    html, body { margin: 0; width: 100%; height: 100%; overflow: hidden; }
    #stage { position: relative; width: 1280px; height: 720px; transform-origin: 0 0; overflow: hidden; }
    #scene-root { position: absolute; inset: 0 0 112px 0; }
    #caption { position: absolute; left: 96px; right: 96px; bottom: 26px; margin: 0; text-align: center; }
    #progress { position: absolute; left: 0; bottom: 0; height: 4px; width: 0; }
  </style>
</head>
<body>
  <main id="stage">
    <div id="scene-root"></div>
    <p id="caption"></p>
    <div id="progress"></div>
  </main>
  <script>
    /* motion-explainer-kit */
    const { spring, camera, rollingDigits, createPlayerShell } = window.MotionKit;
    createPlayerShell({
      stage: '#stage',
      caption: '#caption',
      progress: '#progress',
      auditRoot: '#scene-root',
      auditSelector: 'h1,[data-audit]',
      onSeek(frame) {
        // Pure deterministic render from frame.time, frame.scene,
        // frame.sceneAge, frame.activeCue, frame.activeState, frame.settled
      },
    });
  </script>
</body>
</html>
```

For all 15 stateless motion primitives and the full `createPlayerShell` frame
payload, read [MotionKit API Reference](motion/kit-api.md).

### Low-Level Renderer Contract (`window.motionExplainer`)

If authoring a renderer without `createPlayerShell`, expose
`window.motionExplainer` directly (legacy alias `window.animatic` is accepted):

- `load({storyboard, timeline, width})`: initialize the `1280×720` stage scaled
  cleanly to `width`.
- `seek(seconds, settled)`: render exact state for `seconds` (`settled=true`
  jumps to the beat's resting state). Must be purely a function of `seconds`—no
  wall-clock time, `Math.random()`, `requestAnimationFrame`, or CSS autoplay
  loops.
- `audit()`: return an array of error strings catching stage overflow, clipped
  text across every caption page, caption overlap, and missing title/narration.
