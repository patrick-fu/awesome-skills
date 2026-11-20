#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["edge-tts==7.3.1"]
# ///
"""Zero-key online Edge TTS adapter with WordBoundary timestamp extraction."""

from __future__ import annotations

import argparse
import asyncio
import json
import math
from pathlib import Path
import subprocess
import sys
import uuid

import edge_tts


DEFAULT_VOICES = {
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


def default_voice_for_language(language: str = "en-US") -> str:
    prefix = (language or "en-US").lower().split("-")[0].split("_")[0]
    if prefix in DEFAULT_VOICES:
        return DEFAULT_VOICES[prefix]
    raise ValueError(
        f"No built-in default Edge voice for language {language!r}; "
        "specify an explicit voice from `edge-tts --list-voices`"
    )


async def _synthesize(text: str, voice: str, speed: float) -> tuple[bytes, list[dict]]:
    rate_pct = round((speed - 1.0) * 100)
    rate_str = f"{rate_pct:+d}%"
    comm = edge_tts.Communicate(text, voice, rate=rate_str, boundary="WordBoundary")
    audio = bytearray()
    words: list[dict] = []
    async for chunk in comm.stream():
        ctype = chunk.get("type")
        if ctype == "audio":
            audio.extend(chunk["data"])
        elif ctype == "WordBoundary":
            start = chunk["offset"] / 1e7
            end = (chunk["offset"] + chunk["duration"]) / 1e7
            if not math.isfinite(start + end) or start < 0 or end < start:
                raise RuntimeError("Edge TTS returned invalid word timestamps")
            words.append({"text": chunk["text"], "start": round(start, 4), "end": round(end, 4)})
    return bytes(audio), words


def synthesize(text: str, voice: str, output: Path, *, speed: float = 1.0,
               timestamps: Path | None = None, audio_format: str = "wav") -> dict:
    if not text.strip():
        raise ValueError("Narration must not be empty")
    if not math.isfinite(speed) or not 0.5 <= speed <= 2.0:
        raise ValueError("Speed must be between 0.5 and 2")
    if audio_format not in ["mp3", "wav"]:
        raise ValueError("Audio format must be mp3 or wav")
    audio_bytes, words = asyncio.run(_synthesize(text, voice, speed))
    if not audio_bytes:
        raise RuntimeError("Edge TTS returned empty audio")
    if timestamps is not None and not words:
        raise RuntimeError(
            f"Edge voice {voice!r} returned no WordBoundary timestamps; "
            "choose a WordBoundary-capable voice or build via tts_command without word sync"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp_mp3 = output.with_name(f".{output.name}.{uuid.uuid4().hex}.mp3")
    tmp_out = output.with_name(f".{output.name}.{uuid.uuid4().hex}.wav")
    try:
        tmp_mp3.write_bytes(audio_bytes)
        if audio_format == "wav":
            proc = subprocess.run([
                "ffmpeg", "-v", "error", "-y", "-i", str(tmp_mp3),
                "-vn", "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", "-f", "wav", str(tmp_out)
            ], capture_output=True, text=True)
            if proc.returncode != 0:
                raise RuntimeError(f"ffmpeg failed converting Edge TTS audio: {proc.stderr[-1500:]}")
            tmp_out.replace(output)
        else:
            tmp_mp3.replace(output)
    finally:
        tmp_mp3.unlink(missing_ok=True)
        tmp_out.unlink(missing_ok=True)
    if timestamps is not None:
        timestamps.parent.mkdir(parents=True, exist_ok=True)
        timestamps.write_text(
            json.dumps({"text": text, "words": words}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return {
        "voice": voice,
        "text_characters": len(text),
        "bytes": output.stat().st_size,
        "words": len(words),
        "output": str(output),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Synthesize speech via unofficial Microsoft Edge online TTS")
    parser.add_argument("--text-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--language", default="en-US")
    parser.add_argument("--voice")
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--timestamps", type=Path)
    parser.add_argument("--format", choices=["mp3", "wav"], default="wav")
    args = parser.parse_args(argv)
    try:
        text = args.text_file.read_text(encoding="utf-8").strip()
        voice = args.voice or default_voice_for_language(args.language)
        result = synthesize(
            text, voice, args.output, speed=args.speed,
            timestamps=args.timestamps, audio_format=args.format,
        )
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(f"{type(exc).__name__}: {exc}"[:1000], file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
