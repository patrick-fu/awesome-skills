#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Internal offline MOSS transcription runner."
    )
    parser.add_argument("--model", required=True)
    parser.add_argument("--audio", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    from moss_transcribe_diarize.inference_utils import DEFAULT_PROMPT
    from moss_transcribe_diarize.mlx.model import load_model
    from moss_transcribe_diarize.subtitle import (
        export_json,
        subtitle_segments_from_transcript,
    )

    started = time.monotonic()
    model = load_model(str(Path(args.model).resolve()), strict=False)
    result = model.generate(
        Path(args.audio).resolve(),
        prompt=DEFAULT_PROMPT,
        max_tokens=8192,
        temperature=0.0,
        top_p=1.0,
        top_k=0,
        prefill_step_size=2048,
    )
    segments = json.loads(
        export_json(subtitle_segments_from_transcript(result.text, postprocess=False))
    )
    payload = {
        "schema_version": 1,
        "model": str(Path(args.model).resolve()),
        "text": result.text,
        "segments": segments,
        "prompt_tokens": result.prompt_tokens,
        "generation_tokens": result.generation_tokens,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    Path(args.output).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
