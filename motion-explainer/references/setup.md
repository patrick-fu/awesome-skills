# Setup & Speech Backend Guide

Use this branch when `motion_explainer.py doctor` or `prepare_speech.py` reports
that no TTS provider is configured yet (`SETUP_REQUIRED`), or when the user asks
to set up, switch, or repair a speech backend or renderer.

Present the choices transparently, starting with **Doubao Seed-TTS 2.0** for the
highest narration quality, and fall back to **Local Qwen3-TTS MLX** or **Edge TTS**
if the user prefers not to register a cloud API.

---

## Option 1 (Recommended for Best Quality): Doubao / Volcengine Seed-TTS 2.0

Best overall naturalness, multi-beat voice continuity (`section_id`), delivery
instructions, and native word timestamps—with zero local model storage and
near-zero RAM overhead.

- **Cost & privacy**: Official billable cloud API (typically a few cents per
  short explainer video, or covered by trial/resource packages). Narration text
  is sent to Volcengine (`openspeech.bytedance.com`).
- **Setup steps to guide the user through**:
  1. Sign in or register at the Volcengine console (`https://console.volcengine.com/`)
     and open **豆包语音 (Speech / Doubao Voice)** → **语音合成大模型 2.0** (`seed-tts-2.0`).
  2. Activate the service (check free trial quota or pay-as-you-go / resource pack)
     and create an application to obtain your **APP ID** and **Access Token**.
  3. Export credentials in your shell environment (for example `~/.zshrc`, never
     commit them to git or paste them into storyboards):
     ```bash
     export DOUBAO_APPID="<your-app-id>"
     export DOUBAO_ACCESS_TOKEN="<your-access-token>"
     ```
  4. Verify with one short test sentence (replace `<skill-dir>` with the resolved
     installed path):
     ```bash
     printf '%s\n' "你好，这是一句简短的配音连通性测试。" > /tmp/me-tts-test.txt
     uv run --no-project <skill-dir>/scripts/volcengine_tts.py \
       --text-file /tmp/me-tts-test.txt \
       --output /tmp/me-tts-test.mp3
     ```
- Once `DOUBAO_APPID` and `DOUBAO_ACCESS_TOKEN` are present in the environment,
  `prepare_speech.py --provider auto` selects `doubao` automatically.

---

## Option 2 (Fully Offline, Apple Silicon 16 GB+): Local Qwen3-TTS 1.7B + ForcedAligner 0.6B (MLX)

Runs completely offline with Apache-2.0 weights, delivery instructions, and
accurate local word timestamps (`Qwen3-ForcedAligner-0.6B-8bit`), with automatic
`ffmpeg loudnorm` loudness normalization. TTS and Aligner run in separate
sequential subprocesses so GPU memory never stacks.

- **Platform & resource requirements**:
  - **macOS Apple Silicon (arm64)** only. Other OS/architectures must not run setup.
  - **Unified memory**: **16 GB+ recommended** (measured Metal GPU peak ~6.5 GB
    for TTS, ~2.1 GB for Aligner).
  - **Disk space**: **~4.64 GB total** (~2.88 GB TTS + ~1.20 GB Aligner +
    ~0.56 GB isolated Python venv).
- **Workflow (never download without explicit user approval)**:
  1. Inspect host readiness and storage paths first:
     ```bash
     uv run --no-project <skill-dir>/scripts/manage_runtime.py inspect --json
     ```
  2. Report the platform check, unified memory, estimated ~4.64 GB download, and
     default install directories (`~/Library/Application Support/motion-explainer/`).
  3. If the user prefers an external SSD or custom storage root, check and save
     distinct non-overlapping `app-root` and `cache-root` directories first (this
     persists paths only and does not move existing data):
     ```bash
     uv run --no-project <skill-dir>/scripts/manage_runtime.py storage status --json
     uv run --no-project <skill-dir>/scripts/manage_runtime.py storage configure \
       --app-root "/Volumes/External/motion-explainer/runtime" \
       --cache-root "/Volumes/External/motion-explainer/cache" --json
     ```
  4. Only after the user explicitly approves installation, run setup and verify:
     ```bash
     uv run --no-project <skill-dir>/scripts/manage_runtime.py setup --json
     uv run --no-project <skill-dir>/scripts/manage_runtime.py doctor --json
     ```
- Once installed, `prepare_speech.py --provider qwen3-mlx` (or `--provider auto`
  when Doubao credentials are absent) runs completely offline.

---

## Option 3 (Zero-Key Cross-Platform Quick-Try): Edge TTS

If the user wants to try `motion-explainer` immediately without registering for
Doubao or downloading ~4.6 GB of local weights:

- Pass `--provider edge` to `prepare_speech.py` (or set `"speech_provider": "edge"`
  in the storyboard).
- Uses `edge-tts==7.3.1` via `uv` (~7 MB cache, zero API key) and extracts
  `WordBoundary` word timestamps for synced captions and anchors.
- **Disclose tradeoffs before using**: unofficial Microsoft Edge Read Aloud
  endpoint with no SLA, occasional network latency spikes, no natural-language
  delivery instructions, and narration text is sent to Microsoft servers.

---

## Option 4 (Zero-Dependency Fallback): Supplied Audio or macOS `say`

- **Supplied recordings**: attach `"audio"` (and `"words"` for word-level sync,
  or pass `--align-supplied` when the local Qwen3 MLX runtime is installed) to
  each beat.
- **macOS `say`**: omit `prepare_speech.py` and run `motion_explainer.py build`
  directly on macOS for a rough offline draft (mechanical voice, no word sync).

---

## Renderer Setup (Playwright Headless Chromium)

If `motion_explainer.py doctor` reports `renderer_error`, install the pinned
headless Chromium shell (~200 MB):

```bash
uv run --no-project --with playwright==1.65.1 python -m playwright install chromium --only-shell
```
