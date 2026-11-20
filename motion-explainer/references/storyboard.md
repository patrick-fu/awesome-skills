# Storyboard & Rendering Contract

Top-level JSON requires `version: 1`, `title`, and non-empty `scenes`.
Optional top-level fields:

| Field | Purpose |
| --- | --- |
| `language` | BCP-47 language tag (e.g. `zh-CN`, `en-US`, `ja-JP`, `es-ES`); matches explicit user request or inferred conversation language |
| `speech_provider` | Optional provider hint for `prepare_speech.py`: `auto`, `doubao`, `qwen3-mlx`, `edge`, or `supplied` |
| `voice` | Optional voice ID for the selected provider; omitted values use the top recommended voice in [voices.md](voices.md) |
| `tts_command` | Optional custom argv array for direct `motion_explainer.py build` without word timestamps |
| `speech_rate` | Words per minute for macOS `say` fallback (`80–400`, default `180`) |

---

## Speech Preparation (`prepare_speech.py`)

Preferred workflow for synced captions and keyword-triggered visuals:

```bash
uv run --no-project scripts/prepare_speech.py script.json --out speech --provider auto
```

Supported providers:

- **`doubao`** (Volcengine Seed-TTS 2.0): calls `scripts/volcengine_tts.py` serially across beats sharing one `section_id` UUID for voice continuity, using `DOUBAO_APPID` and `DOUBAO_ACCESS_TOKEN`. Supports `delivery.instruction`, `delivery.speed` (`0.5–2.0`), and native word timestamps.
- **`qwen3-mlx`** (Local Apple Silicon MLX): invokes the managed runtime (`scripts/manage_runtime.py`) in two sequential batch subprocesses—first `Qwen3-TTS 1.7B (8-bit)` with `ffmpeg loudnorm` loudness normalization, then `Qwen3-ForcedAligner 0.6B (8-bit)`—so GPU memory never stacks. Supports `delivery.instruction`, `delivery.speed`, and full offline word timestamps.
- **`edge`** (Zero-key online Microsoft Edge): invokes `scripts/edge_tts_adapter.py` (`edge-tts==7.3.1`), supports `delivery.speed` and `WordBoundary` timestamps (ignores `delivery.instruction`).
- **`supplied`**: reuses pre-recorded audio attached via beat `audio` + `words` (or pass `--align-supplied` when the local Qwen3 MLX runtime is installed to auto-generate `words`).

### Per-Beat Delivery & Keyword Sync

Write each beat's `narration` as one complete semantic thought (may span multiple sentences) and place mid-beat visual changes in `anchors`:

| Field | Meaning |
| --- | --- |
| `delivery.instruction` | Natural-language speaking direction (used by `doubao` and `qwen3-mlx`) |
| `delivery.speed` | `0.5–2.0`, default `1.0` |
| `pause_ms` | Trailing silence after the beat (`0–30000`, default `350`); aligned upward to video frames |
| `anchors` | Keyword string or `{word, occurrence?, focus?, show?}` object |

`occurrence` is 1-based (default `1`); matching ignores punctuation, spaces, and ASCII letter case. `focus` and `show` use the scene's element indexes and take effect at the first video frame reaching the keyword's start timestamp (`~33.3 ms` per frame at 30 fps). Example:

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

`prepare_speech.py` writes `speech/storyboard.json` along with per-beat `.wav`, `.words.json`, `.request.json`, and `speech-session.json` (storing provider, request sequence SHA-256, and `section_id` for Doubao):

- `audio`: relative WAV path.
- `words`: `[{"text": "...", "start": 0.2, "end": 0.8}]` with original punctuation/spaces restored for karaoke captions.
- `cues`: `[{"word": "...", "start": 0.2, "end": 0.8, "focus": [2], "show": 3}]`.

### Cache & Safety Rules

- Re-running `prepare_speech.py` on the same output directory reuses cached audio offline when narration, voice, provider, delivery parameters, and beat order are unchanged—so editing layouts, pauses, or `anchors` triggers **zero** synthesis calls.
- If narration text, voice, provider, delivery settings, beat order, or cached files change—or if a previous run partially failed—`prepare_speech.py` stops before making any new request and asks for a new output directory.
- Beats with supplied `audio` are validated before any billable or network request and are never uploaded into server context.
- `motion_explainer.py build` rejects unprepared `delivery` or `anchors` so configurations are never silently ignored.

### Direct `tts_command` (Optional Without Word Timestamps)

When skipping `prepare_speech.py` and building directly with an external CLI, `tts_command` is an argv array containing `{text_file}`, `{output}`, and optionally `{voice}`:

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

When `words` are absent (external recording or `tts_command` / `say`), keep each beat's narration within two caption lines so on-screen captions remain unclipped.

---

## Scenes

| Field | Meaning |
| --- | --- |
| `id` | Unique short ID (`[a-zA-Z0-9_-]+`) |
| `layout` | `title`, `flow`, or `code` |
| `title` | Scene heading (question or takeaway) |
| `text` | Optional short supporting note |
| `items` | `flow`: 2–5 short labels; optional leading emoji separated by a space (e.g. `"📦 Cache"`) |
| `code` | `code`: multiline snippet, max 12 lines |
| `beats` | Non-empty narration beat list |

- `focus`: 0-based indexes of highlighted `items` or `code` lines.
- `show`: 1-based count of visible elements; must include every index in `focus`; omitted means show all. Revealed elements keep fixed layout positions so nothing jumps.

---

## Outputs & Custom Renderer Contract

`motion_explainer.py build` writes to a new directory or one carrying `.motion-explainer`:

- `video.mp4` (H.264 / AAC / `mov_text`, default `1280×720`, `24` fps; `--width 1920 --fps 30` supported)
- `storyboard.json`, `player.html` (with embedded OFL fonts), `timeline.json`, `captions.srt`, `poster.png`, `manifest.json`, `audio/`, `frames/`

For custom visual compositions, copy and edit `player.html` and pass `--player /path/to/player.html`. The exporter blocks all network requests during offscreen rendering and drives frames deterministically through `window.motionExplainer` (legacy alias `window.animatic` is also accepted):

- `load({storyboard, timeline, width})`: initialize stage at `1280×720` scaled cleanly to `width`.
- `seek(seconds, settled)`: render exact state for `seconds` (`settled=true` jumps to the beat's resting state). Must be purely a function of `seconds`—never rely on wall-clock time or CSS autoplay animations.
- `audit()`: return an array of error strings catching stage overflow, clipped text (across every caption page), caption overlap, and missing title/narration.
