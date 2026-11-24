---
name: motion-explainer
description: >-
  Produce narrated animated explainer videos from editable storyboards with
  progressive reveals, word-synced captions, customizable visual styles and
  deterministic motion, and MP4 export. Self-contained with cloud Doubao 2.0,
  local offline Qwen3-TTS MLX, zero-key Edge TTS, or supplied audio. Trigger
  when explicitly requested for animated video explainers of concepts, code
  changes, or supplied material.
disable-model-invocation: true
---

# Motion Explainer

Turn an explanation into an editable storyboard, synced voiceover, and rendered MP4 video. Storyboards, visual templates, word timings, and audio stay editable for iteration. This skill is self-contained and does not depend on any other skill.

## Language Selection

Determine the video language (narration, captions, titles, and diagram labels) in this exact order:

1. **Explicit user declaration wins**: if the user asks for a specific language (for example, "make an English explainer" or "做一个中文视频"), follow it. Keep technical identifiers and code symbols in their original form.
2. **Infer from the conversation language**: when the user does not specify a video language, match the language the user is speaking in chat (Chinese conversation → Chinese; English, Japanese, Spanish, Korean, etc. → that inferred language). Do not let the language of source materials silently override the user's conversation language.
3. **Confirm in the pre-build snapshot**: state the chosen language explicitly before generating audio or rendering video.

## Pre-Production Alignment & Mandatory Confirmation Gate

Inspect discoverable facts first: supplied documents, code, git diffs, existing storyboards, and available speech backends (`scripts/motion_explainer.py doctor`). Ask only unresolved unknowns that materially change the story or visual approach, in plain chat text (do not call structured form/multiple-choice question tools).

**Hard gate before any speech synthesis or video rendering** (generation incurs cloud API cost or local compute time): present one compact confirmation snapshot and wait for user approval before running `prepare_speech.py` or `motion_explainer.py build`:

- **Voice & TTS engine**: selected provider (`doubao`, `qwen3-mlx`, `edge`, `supplied`, or `macos_say`), recommended voice ID, online vs offline status, and billing/character-count notice when using a cloud API. If no speech backend is configured yet, enter the [Setup Guide](references/setup.md) branch first.
- **Visual direction, layout & density**: the chosen visual system for this video (paper-and-ink whiteboard is the zero-config fallback, **not** a mandatory lock—pick paper-ink physical, dark UI slice, Swiss editorial typography, warm science explainer, or a user-requested palette to fit the subject), whether using built-in `title` / `flow` / `code` layouts or `custom` scenes with `--player` + `/* motion-explainer-kit */`, low-density pacing plan, resolution/FPS, and output directory.
- **Production approach & story outline**: target audience, core causal mechanism to make clear, estimated duration, and scene-by-scene breakdown.
- **Final language**: explicitly declared or inferred language.

Small visual-only revisions that reuse existing cached audio do not require re-billing TTS; still confirm before re-synthesizing voiceover.

## Speech Routing & Setup Branch

Choose the speech backend in priority order based on what the host has ready and what the user approves. Voice recommendations in [Voice Guide](references/voices.md) are priority-ordered suggestions, never mandatory locks—any voice supported by the chosen engine or user-supplied recording is allowed.

1. **Doubao / Volcengine Seed-TTS 2.0 (`doubao`, recommended for best quality)**:
   - Best naturalness, serial cross-beat continuity (`section_id`), delivery instructions, and native word timestamps; near-zero local disk/RAM cost; billed per character via `DOUBAO_APPID` and `DOUBAO_ACCESS_TOKEN`.
   - When credentials are not configured yet, guide the user through [references/setup.md](references/setup.md) so they can register and configure Doubao Seed-TTS 2.0 for the best result. If they prefer not to set up a cloud API, fall back cleanly to local or zero-key options below.
2. **Local Offline MLX (`qwen3-mlx`, macOS Apple Silicon 16 GB+ recommended)**:
   - Runs `Qwen3-TTS 1.7B (8-bit)` and `Qwen3-ForcedAligner 0.6B (8-bit)` sequentially in separate processes so GPU memory never stacks (~6.5 GB peak GPU RAM, ~4.64 GB total disk, Apache 2.0 weights), with automatic `ffmpeg loudnorm` loudness normalization and full word-level sync.
   - Check readiness with `scripts/manage_runtime.py inspect --json`. On `SETUP_REQUIRED`, read [references/setup.md](references/setup.md), report disk size, memory requirements, and storage path (external disk supported via `storage configure`), and run `manage_runtime.py setup` **only after explicit user approval**.
3. **Zero-Key Online Quick-Try (`edge`, cross-platform)**:
   - Uses Microsoft Edge's unofficial online TTS (`edge-tts`) with zero API keys and word-level timing (`WordBoundary` / `SentenceBoundary` fallback). Only select when the user chooses a quick zero-key online option or neither Doubao nor local MLX is desired.
4. **Zero-Dependency Fallback (`supplied` / `macos_say`)**:
   - Reuse user-supplied recordings (optionally aligned via `--align-supplied` when local Qwen3 MLX runtime is installed), or fall back to macOS `say` (no word timestamps).

## Content, Storyboard & Visuals

- One main idea per scene; write each `narration` beat as a complete semantic unit (may contain multiple sentences) and trigger visual state, focus, or reveal shifts inside the beat with `anchors` / `cues`.
- Match the visual system and composition to the mechanism instead of defaulting every scene to uniform 1-2-3 horizontal boxes. Keep on-screen density low and reuse the same objects across beats to show cause-and-effect in place.
- Read [Visual Language & Motion](references/visuals.md) for visual-style options (paper-ink fallback, dark UI slice, Swiss typography, warm science), the de-carded composition & motion vocabulary, anti-patterns, and density checks.
- Follow [Storyboard & Rendering Contract](references/storyboard.md) for JSON schema (`title` / `flow` / `code` / `custom`), custom cue fields, multi-provider speech preparation, cache safety, and custom `--player` + `/* motion-explainer-kit */` (`window.MotionKit` / `window.motionExplainer`). Starter examples live in [assets/example.zh.json](assets/example.zh.json), [assets/example.en.json](assets/example.en.json), and [assets/example.rhythm.zh.json](assets/example.rhythm.zh.json).

## Local Production Commands

Resolve relative paths against this skill directory before executing:

```bash
uv run --no-project scripts/motion_explainer.py doctor
uv run --no-project scripts/motion_explainer.py validate /path/to/storyboard.json
uv run --no-project scripts/prepare_speech.py /path/to/storyboard.json --out /path/to/artifacts/speech --provider auto
uv run --no-project scripts/motion_explainer.py build /path/to/artifacts/speech/storyboard.json --out /path/to/artifacts/video --fps 30
uv run --no-project scripts/motion_explainer.py verify /path/to/artifacts/video
```

Host requirements: `uv`, `ffmpeg`, `ffprobe`, and Playwright's headless Chromium shell. Install the headless renderer if `doctor` reports it missing:

```bash
uv run --no-project --with playwright==1.65.1 python -m playwright install chromium --only-shell
```

Keep source artifacts (`storyboard.json`, `player.html`, `timeline.json`, per-beat audio, `captions.srt`) in a dedicated output directory owned by this tool (`.motion-explainer` marker). When editing only visuals, custom cue payloads, or pauses, re-run `prepare_speech.py` on the same speech output directory to reuse cached audio offline with zero synthesis calls. Pass `--player /path/to/player.html` to build with custom scene layouts and inline `/* motion-explainer-kit */` for offline deterministic motion primitives and player guardrails.

## Verification & Delivery

1. **Technical verification**: run `motion_explainer.py verify` (full FFmpeg decode, H.264/AAC/mov_text tracks, frame count, duration, timeline continuity, and SRT range match).
2. **Visual & timing inspection**: inspect real frames extracted from `video.mp4` at the opening, scene transitions, mid-motion/keyword anchors, and ending. Check font rendering (CJK/Latin), clipping, caption readability, low single-screen density, and reverse-seek determinism.
3. **Audio listening check**: confirm non-silent balanced loudness and check pacing/pronunciation/continuity; clearly report whether narration was listened to directly or still awaits user audition.
4. **Deliver**: playable `video.mp4`, editable source directory, short rebuild command, speech provider/voice used, visual direction chosen, and explicit technical + watching/listening verification status. Licensing and third-party notices live in [NOTICE.md](NOTICE.md). Never upload, publish, or attach outputs to a PR without explicit authorization.
