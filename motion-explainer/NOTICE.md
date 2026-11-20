# Third-Party Notices

This skill's own scripts, templates, and documentation are licensed under MIT
(see the repository root `LICENSE`). Bundled assets, optional downloaded models,
host tools, and external speech APIs remain under their respective licenses and
terms.

## Bundled Fonts

Included directly under `assets/fonts/` and embedded into exported `player.html`
files for offline rendering:

- **LXGW WenKai Lite** (`lxgw-wenkai-lite-cjk-common.woff2`,
  `lxgw-wenkai-lite-latin.woff2`) — licensed under the **SIL Open Font License
  1.1**. The full license text is preserved in `assets/fonts/OFL.txt` and copied
  into bundled player CSS.

## Optional Local MLX Models & Runtime Dependencies

Installed only on macOS Apple Silicon (arm64) after explicit user approval via
`scripts/manage_runtime.py setup`. Exact revisions are pinned in
`runtime/models.lock.json` and `runtime/requirements.in`:

- `mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit` — MLX 8-bit quantization
  of `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` (**Apache-2.0**).
- `mlx-community/Qwen3-ForcedAligner-0.6B-8bit` — MLX 8-bit quantization of
  `Qwen/Qwen3-ForcedAligner-0.6B` (**Apache-2.0**).
- `mlx-audio` (MIT), `mlx` (MIT), `transformers` (Apache-2.0),
  `huggingface_hub` (Apache-2.0), and transitive Python packages installed into
  the skill-managed isolated virtualenv.

## Host Tools

Not bundled in this repository; installed and managed by the user:

- `uv`, `ffmpeg`, `ffprobe` (`ffmpeg` licensing depends on the user's build).
- `playwright` (Apache-2.0) and its headless Chromium shell downloaded on demand.
- `edge-tts` (LGPL-3.0) fetched dynamically by `uv` only when the user opts
  into the `edge` provider.

## External Online Speech Services

Used only after user confirmation:

- **Volcengine / Doubao Seed-TTS 2.0** (`openspeech.bytedance.com`,
  `seed-tts-2.0`): proprietary billable cloud API. Narration text is sent to
  Volcengine servers under your account's terms and billing rules. Credentials
  are read only from `DOUBAO_APPID` and `DOUBAO_ACCESS_TOKEN`.
- **Microsoft Edge Read Aloud (`edge-tts`)**: unofficial consumer WebSocket
  endpoint with no SLA. Narration text is sent to Microsoft servers.
