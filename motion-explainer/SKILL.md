---
name: motion-explainer
description: >-
  Direct narrated animated explainer videos scene by scene with custom stage
  compositions, subject-matched visual systems, stateless deterministic motion
  primitives, word-synced captions, and offline MP4 export. Self-contained with
  cloud Doubao 2.0, local offline Qwen3-TTS MLX, zero-key Edge TTS, or supplied
  audio. Trigger when explicitly requested for animated video explainers of
  concepts, code changes, or supplied material.
disable-model-invocation: true
---

# Motion Explainer

Turn an explanation into a directed storyboard, synced voiceover, bespoke
offline HTML stage, and rendered MP4 video. Storyboards, custom players, word
timings, and audio stay editable for iteration. This skill is self-contained
and does not depend on any other skill.

## Language Selection

Determine the video language (narration, captions, titles, and diagram labels)
in this exact order:

1. **Explicit user declaration wins**: if the user asks for a specific language
   (for example, "make an English explainer" or "做一个中文视频"), follow it.
   Keep technical identifiers and code symbols in their original form.
2. **Infer from the conversation language**: when the user does not specify a
   video language, match the language the user is speaking in chat (Chinese
   conversation → Chinese; English, Japanese, Spanish, Korean, etc. → that
   inferred language). Do not let the language of source materials silently
   override the user's conversation language.
3. **Confirm in the pre-build snapshot**: state the chosen language explicitly
   before generating audio or rendering video.

## Pre-Production Alignment & Mandatory Confirmation Gate

Inspect discoverable facts first: supplied documents, code, git diffs, existing
storyboards, and available speech backends (`scripts/motion_explainer.py doctor`).
Ask only unresolved unknowns that materially change the story or visual
approach, in plain chat text (do not call structured form/multiple-choice
question tools).

**Hard gate before any speech synthesis or video rendering** (generation incurs
cloud API cost or local compute time): present one compact confirmation
snapshot and wait for user approval before running `prepare_speech.py` or
`motion_explainer.py build`:

- **Voice & TTS engine**: selected provider (`doubao`, `qwen3-mlx`, `edge`,
  `supplied`, or `macos_say`), recommended voice ID, online vs offline status,
  and billing/character-count notice when using a cloud API. If no speech
  backend is configured yet, enter the [Setup Guide](references/setup.md)
  branch first.
- **Visual direction & scene staging**: chosen visual system for the subject
  (dark UI slice, Swiss editorial typography, warm science/editorial
  illustration, paper-and-ink whiteboard, or a user-requested palette), custom
  `player.html` scene plan (`/* motion-explainer-kit */`), low-density pacing,
  resolution/FPS, and output directory.
- **Story & causal arc**: target audience, core causal mechanism to make clear,
  estimated duration, and scene-by-scene breakdown.
- **Final language**: explicitly declared or inferred language.

Small visual-only revisions that reuse existing cached audio do not require
re-billing TTS; still confirm before re-synthesizing voiceover.

## Directing Workflow (Primary Path)

Author every video from the mechanism outward rather than fitting ideas into
fixed slide boxes:

1. **Choose the visual system**: pick palette, typography, and surface cues for
   the subject in [Visual Direction & Style Purity](references/visuals.md).
2. **Design each scene's stage around the mechanism**: keep one idea and low
   text density per scene. Author layout-free scenes in `storyboard.json` with
   domain data and word-synced `anchors` (`state`, `action`, `badge`, `data`,
   or optional `focus`/`show`)—see
   [Storyboard & Player Contract](references/storyboard.md) and starter
   [assets/example.free.zh.json](assets/example.free.zh.json).
3. **Author a dedicated `player.html`**: inline `/* motion-explainer-kit */`
   and register through `MotionKit.createPlayerShell(...)` so `1280×720`
   scaling, word-synced karaoke captions, progress bar, and multi-page
   `audit()` guardrails stay automatic while every scene renders bespoke
   DOM/SVG geometry driven deterministically from `seconds` and `cues`.
   (The bundled `assets/player.html` remains available only as a zero-config
   fallback when no `--player` is passed.)
4. **Load motion references on demand**:
   - Choreographing scene transitions, de-carded compositions, or motion craft
     guardrails → [Choreography & Pattern Dictionary](references/motion/choreography.md).
   - Implementing deterministic `window.MotionKit` calls in `player.html` →
     [MotionKit API Reference](references/motion/kit-api.md).

## Speech Routing & Setup Branch

Choose the speech backend in priority order based on what the host has ready
and what the user approves. Voice recommendations in
[Voice Guide](references/voices.md) are priority-ordered suggestions, never
mandatory locks—any voice supported by the chosen engine or user-supplied
recording is allowed.

1. **Doubao / Volcengine Seed-TTS 2.0 (`doubao`, recommended for best quality)**:
   - Best naturalness, serial cross-beat continuity (`section_id`), delivery
     instructions, and native word timestamps; near-zero local disk/RAM cost;
     billed per character via `DOUBAO_APPID` and `DOUBAO_ACCESS_TOKEN`.
   - When credentials are not configured yet, guide the user through
     [references/setup.md](references/setup.md) so they can register and
     configure Doubao Seed-TTS 2.0 for the best result. If they prefer not to
     set up a cloud API, fall back cleanly to local or zero-key options below.
2. **Local Offline MLX (`qwen3-mlx`, macOS Apple Silicon 16 GB+ recommended)**:
   - Runs `Qwen3-TTS 1.7B (8-bit)` and `Qwen3-ForcedAligner 0.6B (8-bit)`
     sequentially in separate processes so GPU memory never stacks (~6.5 GB
     peak GPU RAM, ~4.64 GB total disk, Apache 2.0 weights), with automatic
     `ffmpeg loudnorm` loudness normalization and full word-level sync.
   - Check readiness with `scripts/manage_runtime.py inspect --json`. On
     `SETUP_REQUIRED`, read [references/setup.md](references/setup.md), report
     disk size, memory requirements, and storage path (external disk supported
     via `storage configure`), and run `manage_runtime.py setup` **only after
     explicit user approval**.
3. **Zero-Key Online Quick-Try (`edge`, cross-platform)**:
   - Uses Microsoft Edge's unofficial online TTS (`edge-tts`) with zero API
     keys and word-level timing (`WordBoundary` / `SentenceBoundary` fallback).
     Only select when the user chooses a quick zero-key online option or
     neither Doubao nor local MLX is desired.
4. **Zero-Dependency Fallback (`supplied` / `macos_say`)**:
   - Reuse user-supplied recordings (optionally aligned via `--align-supplied`
     when local Qwen3 MLX runtime is installed), or fall back to macOS `say`
     (no word timestamps).

## Local Production Commands

Resolve relative paths against this skill directory before executing:

```bash
uv run --no-project scripts/motion_explainer.py doctor
uv run --no-project scripts/motion_explainer.py validate /path/to/storyboard.json
uv run --no-project scripts/prepare_speech.py /path/to/storyboard.json --out /path/to/artifacts/speech --provider auto
uv run --no-project scripts/motion_explainer.py build /path/to/artifacts/speech/storyboard.json --player /path/to/player.html --out /path/to/artifacts/video --fps 30
uv run --no-project scripts/motion_explainer.py verify /path/to/artifacts/video
```

Host requirements: `uv`, `ffmpeg`, `ffprobe`, and Playwright's headless
Chromium shell. Install the headless renderer if `doctor` reports it missing:

```bash
uv run --no-project --with playwright==1.65.1 python -m playwright install chromium --only-shell
```

Keep source artifacts (`storyboard.json`, `player.html`, `timeline.json`,
per-beat audio, `captions.srt`) in a dedicated output directory owned by this
tool (`.motion-explainer` marker). When editing only visuals, custom cue
payloads, or pauses, re-run `prepare_speech.py` on the same speech output
directory to reuse cached audio offline with zero synthesis calls.

## Verification & Delivery

1. **Technical verification**: run `motion_explainer.py verify` (full FFmpeg
   decode, H.264/AAC/mov_text tracks, frame count, duration, timeline
   continuity, and SRT range match).
2. **Visual & timing inspection**: inspect real frames extracted from
   `video.mp4` at the opening, scene transitions, mid-motion/keyword anchors,
   and ending. Check font rendering (CJK/Latin), clipping, caption readability,
   low single-screen density, and reverse-seek determinism.
3. **Audio listening check**: confirm non-silent balanced loudness and check
   pacing/pronunciation/continuity; clearly report whether narration was
   listened to directly or still awaits user audition.
4. **Deliver**: playable `video.mp4`, editable source directory, short rebuild
   command, speech provider/voice used, visual direction chosen, and explicit
   technical + watching/listening verification results.
