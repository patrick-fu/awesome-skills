# Third-party notices

This skill does not relicense upstream models or libraries. Local setup
downloads pinned quantized weights and Python packages; the online worker
calls a proprietary cloud API. Exact revisions live in
`runtime/models.lock.json` and `runtime/requirements.lock`.

## Local models

Setup downloads only these pinned Apache-2.0 snapshots, and only after an
explicit setup request:

- `mlx-community/Qwen3-ASR-1.7B-8bit` and `mlx-community/Qwen3-ASR-1.7B-4bit`
- `vanch007/mlx-MOSS-Transcribe-Diarize-8bit` and
  `vanch007/mlx-MOSS-Transcribe-Diarize-4bit`

Those snapshots are MLX quantized projections of:

- `Qwen/Qwen3-ASR-1.7B` (Apache-2.0)
- `OpenMOSS-Team/MOSS-Transcribe-Diarize` (Apache-2.0)

This skill does not download the original BF16 checkpoints.

## Direct local runtime dependencies

Pinned by `runtime/requirements.in`:

- `mlx-audio` (MIT), including its `mlx` dependency (MIT).
- `moss-transcribe-diarize` from
  `https://github.com/vanch007/mlx-MOSS-Transcribe-Diarize` (Apache-2.0).
- `torch` and `torchaudio` (BSD-3-Clause).
- Transitive packages, including `transformers` (Apache-2.0) and
  `huggingface_hub` (Apache-2.0), as locked in `runtime/requirements.lock`.

Setup may install system `uv`, `ffmpeg`, and `ffprobe` through Homebrew. Those
binaries are not bundled here; `ffmpeg` licensing depends on the installed
build.

## Online service

The Doubao / Volcengine speech API (`volc.seedasr.auc`, 豆包录音文件识别模型
2.0) is a proprietary cloud service. This skill does not redistribute that
model. When the online worker runs, it uploads a converted copy of the selected
audio to Doubao/Volcengine. Use it only after explicit cloud/upload consent.
