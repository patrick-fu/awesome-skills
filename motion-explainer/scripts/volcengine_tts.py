#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

import argparse
import base64
import json
import math
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request
import uuid
import wave


DEFAULT_VOICE = "zh_female_tianmeitaozi_uranus_bigtts"
DEFAULT_EN_VOICE = "en_female_myra_cmb_uranus_bigtts"
DEFAULT_INSTRUCTION = "自然口语，短句讲清因果，重点词稍加重，句尾落稳"
DEFAULT_EN_INSTRUCTION = "Warm, natural conversational explainer tone, clear pacing with gentle emphasis on key words."


def default_voice_for_language(language: str = "zh-CN") -> str:
    lang = (language or "zh-CN").lower()
    if lang.startswith("en"):
        return DEFAULT_EN_VOICE
    return DEFAULT_VOICE


def default_instruction_for_language(language: str = "zh-CN") -> str:
    lang = (language or "zh-CN").lower()
    if lang.startswith("zh"):
        return DEFAULT_INSTRUCTION
    return DEFAULT_EN_INSTRUCTION


def synthesize(text, voice, output, *, instruction=DEFAULT_INSTRUCTION, speed=1.0, timestamps=None,
               audio_format="mp3", section_id=None):
    credentials = {name: os.environ.get(name, "") for name in ["DOUBAO_APPID", "DOUBAO_ACCESS_TOKEN"]}
    missing = [name for name, value in credentials.items() if not value]
    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")
    if not text.strip():
        raise ValueError("Narration must not be empty")
    if not math.isfinite(speed) or not 0.5 <= speed <= 2:
        raise ValueError("Speed must be between 0.5 and 2")
    if audio_format not in ["mp3", "wav"]:
        raise ValueError("Audio format must be mp3 or wav")
    if section_id is not None and (not isinstance(section_id, str) or not section_id.strip()):
        raise ValueError("Section ID must be a non-empty string")
    headers = {
        "Content-Type": "application/json",
        "X-Api-App-Id": credentials["DOUBAO_APPID"],
        "X-Api-Access-Key": credentials["DOUBAO_ACCESS_TOKEN"],
        "X-Api-Resource-Id": "seed-tts-2.0",
        "X-Api-Request-Id": str(uuid.uuid4()),
    }
    payload = {
        "user": {"uid": "motion-explainer"},
        "req_params": {
            "text": text,
            "speaker": voice,
            "audio_params": {
                "format": "pcm" if audio_format == "wav" else "mp3",
                "sample_rate": 24000,
                "speech_rate": round((speed - 1) * 100),
                "enable_subtitle": timestamps is not None,
            },
        },
    }
    additions = {}
    if instruction:
        additions["context_texts"] = [instruction]
    if section_id is not None:
        additions["section_id"] = section_id
    if additions:
        payload["req_params"]["additions"] = json.dumps(additions, ensure_ascii=False)
    request = urllib.request.Request(
        "https://openspeech.bytedance.com/api/v3/tts/unidirectional",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    audio = bytearray()
    words = []
    finished = False
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            for line in response:
                if not line.strip():
                    continue
                message = json.loads(line)
                code = message.get("code", 0)
                if code not in [0, 20000000]:
                    raise RuntimeError(f"Volcengine TTS {code}: {message.get('message', message.get('msg', 'request failed'))}")
                if message.get("data"):
                    audio.extend(base64.b64decode(message["data"], validate=True))
                sentence = message.get("sentence") or {}
                for word in sentence.get("words", []):
                    start, end = float(word["startTime"]), float(word["endTime"])
                    if not math.isfinite(start + end) or start < 0 or end < start:
                        raise RuntimeError("Volcengine returned invalid word timestamps")
                    words.append({"text": word["word"], "start": start, "end": end})
                if code == 20000000:
                    finished = True
                    break
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Volcengine HTTP {exc.code}: {exc.read(2000).decode('utf-8', 'replace')}") from None
    if not finished or not audio:
        raise RuntimeError("Volcengine returned incomplete or empty audio")
    if timestamps is not None and not words:
        raise RuntimeError("Volcengine returned no word timestamps")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f".{output.name}.{uuid.uuid4().hex}.tmp")
    try:
        if audio_format == "wav":
            with wave.open(str(temporary), "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(24000)
                wav.writeframes(audio)
        else:
            temporary.write_bytes(audio)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    if timestamps is not None:
        timestamps.parent.mkdir(parents=True, exist_ok=True)
        timestamps.write_text(json.dumps({"text": text, "words": words}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"voice": voice, "text_characters": len(text), "bytes": len(audio), "words": len(words), "output": str(output)}


def main():
    parser = argparse.ArgumentParser(description="Synthesize speech with the billable Volcengine Seed-TTS 2.0 API")
    parser.add_argument("--text-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--language", default="zh-CN")
    parser.add_argument("--voice")
    parser.add_argument("--instruction")
    parser.add_argument("--section-id", help="Shared context ID for serial synthesis requests")
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--timestamps", type=Path)
    parser.add_argument("--format", choices=["mp3", "wav"], default="mp3")
    args = parser.parse_args()
    try:
        text = args.text_file.read_text(encoding="utf-8").strip()
        voice = args.voice or default_voice_for_language(args.language)
        instruction = args.instruction if args.instruction is not None else default_instruction_for_language(args.language)
        result = synthesize(text, voice, args.output, instruction=instruction, speed=args.speed,
                            timestamps=args.timestamps, audio_format=args.format, section_id=args.section_id)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        message = str(exc)
        for name in ["DOUBAO_APPID", "DOUBAO_ACCESS_TOKEN"]:
            secret = os.environ.get(name)
            if secret:
                message = message.replace(secret, "[redacted]")
        print(message[:1000], file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
