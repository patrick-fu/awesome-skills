"""Bundled local audio-transcription implementation."""

import json
from pathlib import Path

_LOCK = Path(__file__).resolve().parents[2] / "runtime" / "models.lock.json"
__version__ = str(json.loads(_LOCK.read_text(encoding="utf-8"))["runtime_version"])
