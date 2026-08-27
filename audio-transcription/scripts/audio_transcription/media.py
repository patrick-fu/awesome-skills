from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .errors import CliError

SILENCE_END_RE = re.compile(r"silence_end:\s*([0-9.]+)")


def require_command(name: str) -> str:
    resolved = shutil.which(name)
    if not resolved:
        raise CliError(
            "SETUP_REQUIRED",
            f"Required command is missing: {name}",
            [
                {
                    "kind": "invoke_skill",
                    "instruction": "Invoke $audio-transcription and request setup.",
                }
            ],
        )
    return resolved


def probe(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise CliError("INPUT_NOT_FOUND", f"Input file does not exist: {path}")
    command = [
        require_command("ffprobe"),
        "-v",
        "error",
        "-show_entries",
        "format=duration,size,format_name:stream=index,codec_type,codec_name,sample_rate,channels,disposition",
        "-of",
        "json",
        str(path),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode:
        detail = completed.stderr.strip()[-1000:] or "unknown ffprobe failure"
        raise CliError("MEDIA_PROBE_FAILED", f"ffprobe failed: {detail}")
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise CliError(
            "MEDIA_PROBE_FAILED", f"ffprobe returned invalid JSON: {exc}"
        ) from exc
    audio_streams = [
        item for item in result.get("streams", []) if item.get("codec_type") == "audio"
    ]
    if not audio_streams:
        raise CliError("NO_AUDIO_STREAM", f"Input contains no audio stream: {path}")
    default = next(
        (
            item
            for item in audio_streams
            if item.get("disposition", {}).get("default") == 1
        ),
        None,
    )
    selected = default or audio_streams[0]
    try:
        duration = float(result.get("format", {}).get("duration", 0) or 0)
    except (TypeError, ValueError):
        duration = 0.0
    return {
        "duration_seconds": duration,
        "size_bytes": path.stat().st_size,
        "format_name": result.get("format", {}).get("format_name"),
        "audio_streams": len(audio_streams),
        "selected_audio_stream": int(selected.get("index", 0)),
        "selected_codec": selected.get("codec_name"),
        "selected_sample_rate": selected.get("sample_rate"),
        "selected_channels": selected.get("channels"),
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def transcode_wav(source: Path, destination: Path, stream_index: int) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    command = [
        require_command("ffmpeg"),
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(source),
        "-map",
        f"0:{stream_index}",
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        str(destination),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode:
        detail = completed.stderr.strip()[-1500:] or "unknown ffmpeg failure"
        raise CliError(
            "MEDIA_TRANSCODE_FAILED", f"ffmpeg WAV conversion failed: {detail}"
        )


def silence_points(wav: Path) -> list[float]:
    command = [
        require_command("ffmpeg"),
        "-nostdin",
        "-hide_banner",
        "-i",
        str(wav),
        "-af",
        "silencedetect=noise=-35dB:d=0.5",
        "-f",
        "null",
        "-",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    text = (completed.stderr or "") + "\n" + (completed.stdout or "")
    return sorted({float(match.group(1)) for match in SILENCE_END_RE.finditer(text)})


def chunk_ranges(
    duration: float, maximum: float, silences: list[float]
) -> list[tuple[float, float]]:
    if duration <= maximum:
        return [(0.0, duration)]
    ranges: list[tuple[float, float]] = []
    start = 0.0
    while duration - start > maximum:
        target = start + maximum
        minimum = start + maximum * 0.6
        candidates = [point for point in silences if minimum <= point <= target]
        end = max(candidates) if candidates else target
        if end <= start:
            end = target
        ranges.append((start, end))
        start = end
    if duration > start:
        ranges.append((start, duration))
    return ranges


def extract_wav_chunk(
    source: Path, destination: Path, start: float, end: float
) -> None:
    command = [
        require_command("ffmpeg"),
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-ss",
        f"{start:.3f}",
        "-i",
        str(source),
        "-t",
        f"{end - start:.3f}",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        str(destination),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode:
        detail = completed.stderr.strip()[-1500:] or "unknown ffmpeg failure"
        raise CliError(
            "MEDIA_TRANSCODE_FAILED", f"ffmpeg chunk extraction failed: {detail}"
        )
