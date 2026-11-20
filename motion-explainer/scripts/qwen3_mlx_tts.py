#!/usr/bin/env python3
"""Local Apple Silicon MLX worker for Qwen3-TTS 1.7B and Qwen3-ForcedAligner 0.6B.

Executed inside the managed runtime venv created by manage_runtime.py.
Runs TTS and ForcedAligner in separate invocations so GPU memory never stacks.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import subprocess
import sys
import uuid


LANG_MAP = {
    "zh": "Chinese",
    "en": "English",
    "ja": "Japanese",
    "ko": "Korean",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "pt": "Portuguese",
    "it": "Italian",
    "ru": "Russian",
}


def qwen_language(code: str) -> str:
    prefix = (code or "zh").lower().split("-")[0].split("_")[0]
    return LANG_MAP.get(prefix, "auto")


def normalize_wav(raw_wav: Path, final_wav: Path, speed: float = 1.0) -> None:
    filters = []
    if abs(speed - 1.0) > 1e-3:
        if not 0.5 <= speed <= 2.0:
            raise ValueError("Speed must be between 0.5 and 2.0")
        filters.append(f"atempo={speed:.4f}")
    # Normalize local Qwen3 output (~ -27 dB) to match standard narration loudness (~ -18 LUFS)
    filters.append("loudnorm=I=-18:TP=-1.5:LRA=11")
    tmp_out = final_wav.with_name(f".{final_wav.name}.{uuid.uuid4().hex}.wav")
    try:
        proc = subprocess.run([
            "ffmpeg", "-v", "error", "-y", "-i", str(raw_wav),
            "-af", ",".join(filters),
            "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", str(tmp_out),
        ], capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"ffmpeg loudnorm failed: {proc.stderr[-1500:]}")
        tmp_out.replace(final_wav)
    finally:
        tmp_out.unlink(missing_ok=True)


def run_tts_batch(model_dir: Path, jobs: list[dict]) -> list[dict]:
    import numpy as np
    import soundfile as sf
    from mlx_audio.tts.utils import load_model

    model = load_model(model_dir)
    results = []
    for job in jobs:
        out_path = Path(job["output"])
        out_path.parent.mkdir(parents=True, exist_ok=True)
        speaker = (job.get("voice") or "serena").lower()
        language = qwen_language(job.get("language", "zh-CN"))
        instruct = job.get("instruction") or None
        speed = float(job.get("speed", 1.0))

        chunks = []
        sr = 24000
        for item in model.generate_custom_voice(
            text=job["text"],
            speaker=speaker,
            language=language,
            instruct=instruct,
        ):
            chunks.append(np.asarray(item.audio, dtype=np.float32))
            if getattr(item, "sample_rate", None):
                sr = int(item.sample_rate)
        if not chunks:
            raise RuntimeError(f"Qwen3-TTS produced empty audio for {out_path.name}")
        wav_data = np.concatenate(chunks) if len(chunks) > 1 else chunks[0]
        raw_tmp = out_path.with_name(f".{out_path.name}.{uuid.uuid4().hex}.raw.wav")
        try:
            sf.write(str(raw_tmp), wav_data, sr, subtype="PCM_16")
            normalize_wav(raw_tmp, out_path, speed=speed)
        finally:
            raw_tmp.unlink(missing_ok=True)
        results.append({"output": str(out_path), "voice": speaker, "language": language})
    return results


def run_align_batch(model_dir: Path, jobs: list[dict]) -> list[dict]:
    from mlx_audio.stt.utils import load_model

    model = load_model(model_dir)
    results = []
    for job in jobs:
        audio_path = Path(job["audio"])
        ts_path = Path(job["timestamps"])
        text = job["text"]
        language = qwen_language(job.get("language", "zh-CN"))
        if language == "auto":
            language = "English"
        aligned = model.generate(str(audio_path), text=text, language=language)
        items = getattr(aligned, "items", aligned)
        words = []
        for item in items:
            if isinstance(item, dict):
                w_text = str(item.get("text", ""))
                start = float(item["start_time"])
                end = float(item["end_time"])
            else:
                w_text = str(getattr(item, "text", ""))
                start = float(getattr(item, "start_time", getattr(item, "start", 0.0)))
                end = float(getattr(item, "end_time", getattr(item, "end", 0.0)))
            if not math.isfinite(start + end) or start < 0 or end < start:
                raise RuntimeError("Qwen3-ForcedAligner returned invalid timestamps")
            words.append({"text": w_text, "start": round(start, 4), "end": round(end, 4)})
        if not words:
            raise RuntimeError(f"Qwen3-ForcedAligner returned no word timestamps for {audio_path.name}")
        ts_path.parent.mkdir(parents=True, exist_ok=True)
        ts_path.write_text(
            json.dumps({"text": text, "words": words}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        results.append({"timestamps": str(ts_path), "words": len(words)})
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run local Qwen3-TTS or Qwen3-ForcedAligner batch jobs")
    parser.add_argument("--mode", choices=["tts", "align"], required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--batch", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        jobs = json.loads(args.batch.read_text(encoding="utf-8"))
        if args.mode == "tts":
            out = run_tts_batch(args.model_dir, jobs)
        else:
            out = run_align_batch(args.model_dir, jobs)
        print(json.dumps({"ok": True, "mode": args.mode, "results": out}, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(str(exc)[:1500], file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
