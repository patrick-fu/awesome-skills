# Colab transcription

This branch uploads a copy of the supplied media to a Google Colab VM through
`google-colab-cli` and transcribes it there on a GPU. Uploaded media leaves the
machine. Do not enter this branch for media that must remain local. Enter it
only when the user explicitly asks for Colab / cloud-GPU transcription,
explicitly permits upload, or the routing rule below applies and the user has
approved cloud processing for this material.

- The upload authorization gate is the same class as the Doubao branch:
  `colab-transcribe transcribe` refuses to run without `--allow-upload`.
  `plan` and `doctor` never upload and never create a session.
- Company meeting recordings and work-screen recordings must be manually
  screened for sensitivity before any upload is requested. The script gates
  authorization only; it does not detect content.
- A local-only or no-upload instruction always wins.

## Prerequisites (one-time init, only on explicit user request)

1. `pip install google-colab-cli` (or `colab update --install` to 0.8.0+).
2. First OAuth must be completed by the user in a real interactive terminal
   (`colab sessions`); in-agent login fails with `Malformed auth code`.
3. `colab-transcribe doctor --json` verifies ffmpeg/ffprobe, auth, and the CU
   balance. CU is paid quota — report the balance before the first run.

## Engine routing (agent decision rule, not a user option)

Measured 2026-11-20/21 on T4 across 10 cases (WER/CER vs verbatim ground
truth; see life-context task `colab-asr-pipeline`):

| Material | Engine | Reason |
| --- | --- | --- |
| Default / short clips / English / Cantonese / mixed-language | `turbo` | Best or tied everywhere here; zero chunking complexity |
| Chinese-dominant long audio (>30 min) | `qwen17` | 0.062 vs 0.085 CER; `-27%` |
| Meeting records (far-field, multi-speaker) | `qwen17` | 0.271 vs 0.335 WER on AMI far-field; `-19%` |
| Heavy noise (babble ≈10 dB SNR or worse) | neither | Both engines degrade ~5×; needs front-end enhancement first |

`turbo` runs `large-v3-turbo` whole-file. `qwen17` runs `Qwen3-ASR-1.7B`
through the official `qwen-asr` package; the runner force-slices long audio
into silence-aligned windows (target 45 s, hard cap 60 s) and batch-transcribes
them. Do not bypass windowing: whole-file input to qwen-asr silently drops
middle and tail chunks (measured; 5 sentences and a 100 s tail vanished on a
254 s file). qwen17 SRT granularity is per-window; character-level timestamps
would need the ForcedAligner and are not wired.

## Protocol

Read `scripts/colab-transcribe help <topic>` and `--help` before execution;
`plan --json` is the read-only estimate (upload seconds, session minutes, CU).
Artifacts per media: `.txt`, `.srt`, `.json` plus `manifest.json` and
`result.json` — the downloaded `result.json` is the only trusted result.

Costs (T4, 1.07 CU/hr): both engines ≈ 0.06–0.1 CU per audio-hour of batch
transcription; a short session is dominated by fixed alloc + install + load
(3–6 min). For single short clips the local MLX route is faster and free.
Session hygiene: the script stops the session at the end unless
`--keep-session`; check `colab usage` afterwards — `Usage rate: 0.00/hr` and
`Active assignments: 0`. An orphaned session keeps burning CU.

## Known limitations

- Continuous speech with no silence gaps falls back to hard cuts at 60 s.
- qwen17 auto-detects language per window. Two observed failure modes
  (2026-11-21 E2E): a window that begins in one language and switches to
  another can under-transcribe the minority block (a 31 s Cantonese block
  inside an English-headed window produced almost no output), and a sentence
  split across a window boundary can appear twice. The routing table already
  sends mixed-language material to `turbo`; if qwen17 must run on
  language-switching audio, check the per-window `language` labels in the
  `.json` and re-cut at language boundaries.
- Engine versions are unpinned on the VM (`qwen-asr` from PyPI); re-verify
  after upstream releases if results drift.
