#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Internal offline Qwen3-ASR runner.")
    parser.add_argument("--model", required=True)
    parser.add_argument("--audio", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--language", default="auto")
    parser.add_argument("--chunk-seconds", type=float, required=True)
    args = parser.parse_args()

    from mlx_audio.stt import load

    started = time.monotonic()
    model = load(str(Path(args.model).resolve()))
    language_aliases = {
        "zh": "Chinese",
        "zh-cn": "Chinese",
        "en": "English",
        "ja": "Japanese",
        "ko": "Korean",
        "de": "German",
        "es": "Spanish",
        "fr": "French",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
        "yue": "Cantonese",
    }
    kwargs = {"chunk_duration": args.chunk_seconds, "batch_size": 1}
    if args.language != "auto":
        kwargs["language"] = language_aliases.get(args.language.lower(), args.language)
    result = model.generate(str(Path(args.audio).resolve()), **kwargs)
    payload = {
        "schema_version": 1,
        "model": str(Path(args.model).resolve()),
        "text": result.text,
        "segments": result.segments or [],
        "language": getattr(result, "language", None),
        "prompt_tokens": getattr(result, "prompt_tokens", 0),
        "generation_tokens": getattr(result, "generation_tokens", 0),
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    Path(args.output).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
