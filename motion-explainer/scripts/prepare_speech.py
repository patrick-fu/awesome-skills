#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Prepare narrated audio, word timestamps, and visual cues across TTS providers."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import uuid

import manage_runtime
from motion_explainer import media_info, read_storyboard, validate_visual, validate_word_times, write_json
import volcengine_tts


SCRIPTS_DIR = Path(__file__).resolve().parent

QWEN3_DEFAULT_VOICES = {
    "zh": "serena",
    "en": "aiden",
    "ja": "ono_anna",
    "ko": "sohee",
}

EDGE_DEFAULT_VOICES = {
    "zh": "zh-CN-XiaoxiaoNeural",
    "en": "en-US-AndrewNeural",
    "ja": "ja-JP-NanamiNeural",
    "ko": "ko-KR-SunHiNeural",
    "es": "es-ES-ElviraNeural",
    "fr": "fr-FR-DeniseNeural",
    "de": "de-DE-KatjaNeural",
    "pt": "pt-BR-FranciscaNeural",
    "it": "it-IT-ElsaNeural",
    "ru": "ru-RU-SvetlanaNeural",
}


def normalized(text: str) -> str:
    return "".join(char for char in text if char.isalnum()).lower()


def lang_prefix(language: str) -> str:
    return (language or "en-US").lower().split("-")[0].split("_")[0]


def default_voice_for(provider: str, language: str) -> str:
    prefix = lang_prefix(language)
    if provider == "doubao":
        return volcengine_tts.default_voice_for_language(language)
    if provider == "qwen3-mlx":
        return QWEN3_DEFAULT_VOICES.get(prefix, "serena")
    if provider == "edge":
        if prefix in EDGE_DEFAULT_VOICES:
            return EDGE_DEFAULT_VOICES[prefix]
        raise ValueError(
            f"No default Edge voice for language {language!r}; pass --voice or set storyboard.voice"
        )
    return "supplied"


def default_instruction_for(language: str) -> str:
    return volcengine_tts.default_instruction_for_language(language)


def align_words(text, words):
    validate_word_times(words, "speech")
    usable = [word for word in words if normalized(word["text"])]
    if normalized("".join(word["text"] for word in usable)) != normalized(text):
        raise ValueError("Returned word text differs from narration; inspect the saved audio and word times")
    positions = [i for i, char in enumerate(text) if char.isalnum()]
    result, mapping = [], []
    offset = raw_start = 0
    for word in usable:
        count = len(normalized(word["text"]))
        offset += count
        raw_end = positions[offset] if offset < len(positions) else len(text)
        if offset < len(positions):
            for index in range(positions[offset - 1] + 1, raw_end):
                char = text[index]
                if char in "“‘（([<{〈《「『【" or unicodedata.category(char).startswith("S"):
                    raw_end = index
                    break
        item = {"text": text[raw_start:raw_end], "start": word["start"], "end": word["end"]}
        result.append(item)
        mapping.extend([item] * count)
        raw_start = raw_end
    if not result:
        raise ValueError("Narration has no alignable words")
    return result, mapping


def anchor_ranges(text, anchors):
    plain = normalized(text)
    ranges = []
    for anchor in anchors:
        if isinstance(anchor, str):
            anchor = {"word": anchor}
        target = normalized(anchor["word"])
        start = -len(target)
        for _ in range(anchor.get("occurrence", 1)):
            start = plain.find(target, start + len(target))
            if start < 0:
                raise ValueError(f"Keyword occurrence not found in narration: {anchor['word']!r}")
        ranges.append((start, start + len(target) - 1, anchor))
    return sorted(ranges, key=lambda item: item[0])


def make_cues(mapping, ranges):
    return [{"word": anchor["word"], "start": mapping[start]["start"], "end": mapping[end]["end"],
             **{key: anchor[key] for key in ["focus", "show"] if key in anchor}}
            for start, end, anchor in ranges]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_audio_words(path: Path, words: list[dict]) -> None:
    info = media_info(path)
    if not any(stream.get("codec_type") == "audio" for stream in info.get("streams", [])):
        raise ValueError(f"{path.name}: no audio stream")
    duration = float(info["format"]["duration"])
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError(f"{path.name}: audio duration must be positive and finite")
    if any(word["end"] > duration + 0.05 for word in words):
        raise ValueError(f"{path.name}: word timing exceeds audio duration")


def owned_speech_dir(output: Path) -> bool:
    for name, expected in [
        (".motion-explainer-speech", "motion-explainer-speech-v1\n"),
        (".animatic-speech", "animatic-speech-v1\n"),
    ]:
        marker = output / name
        if marker.is_file() and marker.read_text(encoding="utf-8") == expected:
            return True
    return False


def resolve_provider(requested: str | None, board: dict, all_supplied: bool, session: dict | None) -> str:
    chosen = requested or board.get("speech_provider") or (session.get("provider") if session else None) or "auto"
    if chosen != "auto":
        return chosen
    if all_supplied:
        return "supplied"
    if os.environ.get("DOUBAO_APPID") and os.environ.get("DOUBAO_ACCESS_TOKEN"):
        return "doubao"
    if manage_runtime.resolve_ready_runtime():
        return "qwen3-mlx"
    raise ValueError(
        "SETUP_REQUIRED: No configured TTS provider found. "
        "Configure Doubao Seed-TTS 2.0 (DOUBAO_APPID + DOUBAO_ACCESS_TOKEN; see references/setup.md), "
        "install the local Qwen3-TTS MLX runtime (manage_runtime.py setup), "
        "or explicitly choose --provider edge for zero-key online Microsoft Edge TTS."
    )


def run_edge_tts(text: str, voice: str, language: str, speed: float, audio: Path, timing: Path) -> None:
    if not shutil.which("uv"):
        raise RuntimeError("uv is required to run edge_tts_adapter.py")
    adapter = SCRIPTS_DIR / "edge_tts_adapter.py"
    with tempfile.TemporaryDirectory(prefix=".edge-") as tmp:
        text_file = Path(tmp) / "narration.txt"
        text_file.write_text(text, encoding="utf-8")
        proc = subprocess.run([
            "uv", "run", "--no-project", str(adapter),
            "--text-file", str(text_file),
            "--output", str(audio),
            "--language", language,
            "--voice", voice,
            "--speed", str(speed),
            "--timestamps", str(timing),
            "--format", "wav",
        ], capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"Edge TTS failed: {(proc.stderr or proc.stdout).strip()[-1500:]}")


def run_qwen3_mlx_batch(runtime: dict, mode: str, jobs: list[dict]) -> None:
    worker = SCRIPTS_DIR / "qwen3_mlx_tts.py"
    model_dir = runtime["tts_model_dir"] if mode == "tts" else runtime["aligner_model_dir"]
    env = os.environ.copy()
    env["HF_HOME"] = runtime["hf_home"]
    with tempfile.TemporaryDirectory(prefix=f".qwen3-{mode}-") as tmp:
        batch_file = Path(tmp) / "jobs.json"
        batch_file.write_text(json.dumps(jobs, ensure_ascii=False, indent=2), encoding="utf-8")
        proc = subprocess.run([
            runtime["python"], str(worker),
            "--mode", mode,
            "--model-dir", model_dir,
            "--batch", str(batch_file),
        ], env=env, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"Qwen3 MLX {mode} failed: {(proc.stderr or proc.stdout).strip()[-1500:]}")


def prepare(source: Path, output: Path, *, provider: str | None = None,
            voice_override: str | None = None, language_override: str | None = None,
            align_supplied: bool = False) -> dict:
    source, output = source.resolve(), output.resolve()
    board = read_storyboard(source)
    if language_override:
        board["language"] = language_override
    language = board.setdefault("language", "zh-CN")

    if output.exists() and any(output.iterdir()) and not owned_speech_dir(output):
        raise ValueError("Speech output must be empty or owned by prepare_speech")

    session_path = output / "speech-session.json"
    session_exists = session_path.exists()
    session = None
    if session_exists:
        session = json.loads(session_path.read_text(encoding="utf-8"))
        if not isinstance(session, dict) or session.get("version") != 1:
            raise ValueError("Invalid speech context; inspect it and use a new output directory")

    all_supplied = all("audio" in beat for scene in board["scenes"] for beat in scene["beats"])
    resolved_provider = resolve_provider(provider, board, all_supplied, session)
    board["speech_provider"] = resolved_provider

    if voice_override:
        board["voice"] = voice_override
    elif not board.get("voice") and resolved_provider != "supplied":
        board["voice"] = default_voice_for(resolved_provider, language)

    section_id = None
    if resolved_provider == "doubao":
        if session_exists:
            if not isinstance(session.get("section_id"), str):
                raise ValueError("Invalid speech context; inspect it and use a new output directory")
            section_id = str(uuid.UUID(session["section_id"]))
        else:
            section_id = str(uuid.uuid4())
    elif session_exists and session.get("provider") and session.get("provider") != resolved_provider:
        raise ValueError("Speech provider changed for existing output directory; use a new output directory")

    jobs = []
    need_supplied_align = False
    for scene in board["scenes"]:
        focus_count = len(scene["items"]) if scene["layout"] == "flow" else len(scene["code"].split("\n")) if scene["layout"] == "code" else 0
        for index, beat in enumerate(scene["beats"]):
            name = f"{scene['id']}-{index}"
            ranges = anchor_ranges(beat["narration"], beat.get("anchors", []))
            state = {key: beat[key] for key in ["focus", "show"] if key in beat}
            for _, _, anchor in ranges:
                state.update({key: anchor[key] for key in ["focus", "show"] if key in anchor})
                validate_visual(state, focus_count, name)
            delivery = beat.get("delivery", {})
            supplied = (source.parent / beat["audio"]).resolve() if "audio" in beat else None
            if supplied:
                if beat.get("words"):
                    align_words(beat["narration"], beat["words"])
                    validate_audio_words(supplied, beat["words"])
                    request = {
                        "provider": "supplied",
                        "text": beat["narration"],
                        "source_audio_sha256": digest(supplied),
                        "supplied_words": beat["words"],
                    }
                elif align_supplied:
                    info = media_info(supplied)
                    if not any(stream.get("codec_type") == "audio" for stream in info.get("streams", [])):
                        raise ValueError(f"{supplied.name}: no audio stream")
                    need_supplied_align = True
                    request = {
                        "provider": "supplied-aligned",
                        "text": beat["narration"],
                        "language": language,
                        "source_audio_sha256": digest(supplied),
                    }
                else:
                    raise ValueError(
                        f"{name}: supplied audio requires words for speech preparation "
                        "(or pass --align-supplied when the local Qwen3 MLX runtime is installed)"
                    )
            else:
                if resolved_provider == "supplied":
                    raise ValueError(f"{name}: provider 'supplied' requires audio on every beat")
                request = {
                    "provider": resolved_provider,
                    "text": beat["narration"],
                    "voice": board["voice"],
                    "language": language,
                    "speed": delivery.get("speed", 1),
                    "format": "wav",
                    "enable_subtitle": True,
                }
                if resolved_provider in ("doubao", "qwen3-mlx"):
                    request["instruction"] = delivery.get("instruction", default_instruction_for(language))
                if resolved_provider == "doubao":
                    request["section_id"] = section_id

            audio = output / f"{name}{supplied.suffix if supplied else '.wav'}"
            timing = output / f"{name}.words.json"
            record = output / f"{name}.request.json"
            present = [path.exists() for path in [audio, timing, record]]
            if any(present):
                if not all(present):
                    raise ValueError(f"{name}: incomplete speech cache; inspect it and choose a new output directory")
                saved = json.loads(record.read_text(encoding="utf-8"))
                if not isinstance(saved, dict) or saved.get("request") != request or saved.get("audio_sha256") != digest(audio) or saved.get("timing_sha256") != digest(timing):
                    raise ValueError(f"{name}: speech settings or cached files changed; use a new output directory")
            jobs.append((beat, supplied, request, audio, timing, record, all(present), ranges))

    sequence = [{"audio": job[3].name, "request": job[2]} for job in jobs]
    fingerprint = hashlib.sha256(json.dumps(sequence, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    if session_exists and session.get("request_sha256") != fingerprint:
        raise ValueError("Speech context or narration order changed; use a new output directory")

    generated = [job for job in jobs if job[1] is None]
    pending_generated = [job for job in generated if not job[6]]
    pending_supplied_align = [job for job in jobs if job[1] is not None and not job[6] and not job[0].get("words")]

    if pending_generated and (session_exists or any(job[6] for job in generated)):
        raise ValueError("Incomplete speech context; use a new output directory to regenerate the continuous narration")

    qwen_runtime = None
    if pending_generated:
        if resolved_provider == "doubao":
            missing = [name for name in ["DOUBAO_APPID", "DOUBAO_ACCESS_TOKEN"] if not os.environ.get(name)]
            if missing:
                raise ValueError(f"Missing environment variables: {', '.join(missing)}")
        elif resolved_provider == "qwen3-mlx":
            qwen_runtime = manage_runtime.resolve_ready_runtime()
            if not qwen_runtime:
                raise ValueError(
                    "SETUP_REQUIRED: Local Qwen3-TTS MLX runtime is not installed. "
                    "Inspect host readiness with `manage_runtime.py inspect --json` and run `manage_runtime.py setup` after user approval."
                )
    if pending_supplied_align and not qwen_runtime:
        qwen_runtime = manage_runtime.resolve_ready_runtime()
        if not qwen_runtime:
            raise ValueError("SETUP_REQUIRED: --align-supplied requires the local Qwen3 MLX runtime (`manage_runtime.py setup`).")

    output.mkdir(parents=True, exist_ok=True)
    (output / ".motion-explainer-speech").write_text("motion-explainer-speech-v1\n", encoding="utf-8")

    if pending_generated:
        session_payload = {"version": 1, "provider": resolved_provider, "request_sha256": fingerprint}
        if section_id is not None:
            session_payload["section_id"] = section_id
        with session_path.open("x", encoding="utf-8") as stream:
            json.dump(session_payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")

    synthesized = 0
    # Copy any uncached supplied audio first
    for beat, supplied, request, audio, timing, record, cached, _ in jobs:
        if cached or not supplied:
            continue
        shutil.copyfile(supplied, audio)
        if beat.get("words"):
            write_json(timing, {"text": beat["narration"], "words": beat["words"]})
            write_json(record, {"request": request, "audio_sha256": digest(audio), "timing_sha256": digest(timing)})

    # Run provider synthesis for pending generated beats
    if pending_generated:
        if resolved_provider == "doubao":
            for beat, _, request, audio, timing, record, _, _ in pending_generated:
                volcengine_tts.synthesize(
                    beat["narration"], board["voice"], audio,
                    instruction=request["instruction"], speed=request["speed"],
                    timestamps=timing, audio_format="wav", section_id=section_id,
                )
                synthesized += 1
                write_json(record, {"request": request, "audio_sha256": digest(audio), "timing_sha256": digest(timing)})
        elif resolved_provider == "qwen3-mlx":
            tts_batch = [
                {
                    "text": beat["narration"],
                    "voice": board["voice"],
                    "language": language,
                    "instruction": request["instruction"],
                    "speed": request["speed"],
                    "output": str(audio),
                }
                for beat, _, request, audio, _, _, _, _ in pending_generated
            ]
            run_qwen3_mlx_batch(qwen_runtime, "tts", tts_batch)
            align_batch = [
                {
                    "audio": str(audio),
                    "text": beat["narration"],
                    "language": language,
                    "timestamps": str(timing),
                }
                for beat, _, _, audio, timing, _, _, _ in pending_generated
            ]
            run_qwen3_mlx_batch(qwen_runtime, "align", align_batch)
            for _, _, request, audio, timing, record, _, _ in pending_generated:
                synthesized += 1
                write_json(record, {"request": request, "audio_sha256": digest(audio), "timing_sha256": digest(timing)})
        elif resolved_provider == "edge":
            for beat, _, request, audio, timing, record, _, _ in pending_generated:
                run_edge_tts(beat["narration"], board["voice"], language, request["speed"], audio, timing)
                synthesized += 1
                write_json(record, {"request": request, "audio_sha256": digest(audio), "timing_sha256": digest(timing)})
        else:
            raise ValueError(f"Unsupported speech provider: {resolved_provider!r}")

    if pending_supplied_align:
        align_batch = [
            {"audio": str(audio), "text": beat["narration"], "language": language, "timestamps": str(timing)}
            for beat, _, _, audio, timing, _, _, _ in pending_supplied_align
        ]
        run_qwen3_mlx_batch(qwen_runtime, "align", align_batch)
        for _, _, request, audio, timing, record, _, _ in pending_supplied_align:
            write_json(record, {"request": request, "audio_sha256": digest(audio), "timing_sha256": digest(timing)})

    result = copy.deepcopy(board)
    prepared = [beat for scene in result["scenes"] for beat in scene["beats"]]
    for target, (beat, _, _, audio, timing, _, _, ranges) in zip(prepared, jobs):
        data = json.loads(timing.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("text") != beat["narration"]:
            raise ValueError(f"{audio.name}: saved narration differs from the input")
        words, mapping = align_words(beat["narration"], data["words"])
        validate_audio_words(audio, words)
        target.update(audio=audio.name, words=words)
        if "anchors" in beat:
            target["cues"] = make_cues(mapping, ranges)

    path = output / "storyboard.json"
    write_json(path, result)
    read_storyboard(path)
    return {
        "storyboard": str(path),
        "provider": resolved_provider,
        "voice": board.get("voice"),
        "language": language,
        "beats": len(jobs),
        "synthesized": synthesized,
        "reused": len(jobs) - synthesized,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Prepare narrated audio and word-level timing across TTS providers")
    parser.add_argument("storyboard", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--provider", choices=["auto", "doubao", "qwen3-mlx", "edge", "supplied"])
    parser.add_argument("--voice", help="Override storyboard voice ID")
    parser.add_argument("--language", help="Override storyboard BCP-47 language code (e.g. zh-CN, en-US)")
    parser.add_argument("--align-supplied", action="store_true", help="Run local Qwen3-ForcedAligner on supplied audio without words")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(
            prepare(
                args.storyboard, args.out,
                provider=args.provider,
                voice_override=args.voice,
                language_override=args.language,
                align_supplied=args.align_supplied,
            ),
            ensure_ascii=False,
        ))
        return 0
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as exc:
        message = str(exc)
        for name in ["DOUBAO_APPID", "DOUBAO_ACCESS_TOKEN"]:
            if os.environ.get(name):
                message = message.replace(os.environ[name], "[redacted]")
        print(message[:1000], file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
