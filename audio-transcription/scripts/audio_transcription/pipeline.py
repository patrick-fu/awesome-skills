from __future__ import annotations

import concurrent.futures
import hashlib
import json
import os
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import cache
from .config import SKILL_ROOT, load_active, write_json_atomic
from .errors import CliError
from .media import (
    chunk_ranges,
    extract_wav_chunk,
    probe,
    sha256,
    silence_points,
    transcode_wav,
)

SCRIPTS = SKILL_ROOT / "scripts"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _cache_key(input_sha: str, active: dict[str, Any], options: dict[str, Any]) -> str:
    value = {
        "schema_version": 1,
        "input_sha256": input_sha,
        "runtime_version": active["runtime_version"],
        "profile": active["profile"],
        "models": {
            name: {"repo": item["repo"], "revision": item["revision"]}
            for name, item in active["models"].items()
        },
        "chunking": active["chunking"],
        "language": options["language"],
    }
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def plan(
    source: Path, *, language: str, parallel: bool, no_cache: bool
) -> dict[str, Any]:
    source = source.expanduser().resolve()
    metadata = probe(source)
    active = load_active()
    if parallel and active["profile"] == "low-memory":
        raise CliError(
            "PARALLEL_UNSAFE",
            "Parallel execution is disabled for the low-memory profile.",
            [{"command": f'local-transcribe "{source}" --json'}],
            requires_user_decision=True,
        )
    input_sha = sha256(source)
    options = {"language": language}
    key = _cache_key(input_sha, active, options)
    hit = None if no_cache else cache.lookup(key)
    return {
        "status": "ready",
        "input": {"path": str(source), "sha256": input_sha, **metadata},
        "runtime": {
            "runtime_version": active["runtime_version"],
            "profile": active["profile"],
            "memory_gib_at_setup": active.get("memory_gib"),
            "python": active["python"],
            "models": {
                name: {
                    "repo": item["repo"],
                    "revision": item["revision"],
                    "path": item["path"],
                }
                for name, item in active["models"].items()
            },
        },
        "execution": {
            "strategy": "parallel" if parallel else "sequential",
            "network": False,
            "upload": False,
            "language": language,
            "chunking": active["chunking"],
            "cache_enabled": not no_cache,
            "cache_hit": bool(hit),
            "cache_key": key,
        },
        "next_actions": [
            {
                "command": f'local-transcribe "{source}"'
                + (" --parallel" if parallel else "")
                + " --json",
            }
        ],
    }


def _offline_env() -> dict[str, str]:
    environment = os.environ.copy()
    environment.update(
        {
            "HF_HUB_OFFLINE": "1",
            "TRANSFORMERS_OFFLINE": "1",
            "HF_DATASETS_OFFLINE": "1",
            "HF_HUB_DISABLE_TELEMETRY": "1",
            "DO_NOT_TRACK": "1",
            "TOKENIZERS_PARALLELISM": "false",
        }
    )
    return environment


def _runner(command: list[str], output_path: Path) -> dict[str, Any]:
    started = time.monotonic()
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
        env=_offline_env(),
    )
    if completed.returncode:
        detail = (
            completed.stderr or completed.stdout or "unknown model failure"
        ).strip()[-4000:]
        code = (
            "MODEL_LOAD_OOM"
            if any(
                token in detail.lower()
                for token in ("out of memory", "metal", "memoryerror")
            )
            else "MODEL_FAILED"
        )
        return {
            "status": "failed",
            "error_code": code,
            "message": detail,
            "exit_code": completed.returncode,
            "elapsed_seconds": round(time.monotonic() - started, 3),
        }
    try:
        payload = json.loads(output_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "status": "failed",
            "error_code": "MODEL_OUTPUT_INVALID",
            "message": str(exc),
            "elapsed_seconds": round(time.monotonic() - started, 3),
        }
    return {
        "status": "success",
        "characters": len(str(payload.get("text", ""))),
        "segments": len(payload.get("segments", [])),
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def _run_qwen(
    active: dict[str, Any], wav: Path, directory: Path, language: str
) -> dict[str, Any]:
    directory.mkdir(parents=True, exist_ok=True)
    raw = directory / "raw.json"
    model = active["models"]["qwen"]
    command = [
        active["python"],
        str(SCRIPTS / "qwen_runner.py"),
        "--model",
        model["path"],
        "--audio",
        str(wav),
        "--output",
        str(raw),
        "--language",
        language,
        "--chunk-seconds",
        str(active["chunking"]["qwen_seconds"]),
    ]
    result = _runner(command, raw)
    if result["status"] == "success":
        payload = json.loads(raw.read_text(encoding="utf-8"))
        (directory / "transcript.txt").write_text(
            str(payload.get("text", "")).strip() + "\n", encoding="utf-8"
        )
    else:
        write_json_atomic(directory / "error.json", result)
    return result


def _qualify_moss_segments(
    segments: list[dict[str, Any]], offset: float, chunk_index: int
) -> list[dict[str, Any]]:
    qualified = []
    for item in segments:
        copy = dict(item)
        copy["start"] = float(copy.get("start", 0)) + offset
        copy["end"] = float(copy.get("end", 0)) + offset
        speaker = str(copy.get("speaker") or "S00")
        copy["speaker"] = f"chunk-{chunk_index:02d}:{speaker}"
        copy["chunk_index"] = chunk_index
        qualified.append(copy)
    return qualified


def _run_moss(
    active: dict[str, Any], wav: Path, directory: Path, duration: float
) -> dict[str, Any]:
    directory.mkdir(parents=True, exist_ok=True)
    maximum = float(active["chunking"]["moss_seconds"])
    ranges = chunk_ranges(duration, maximum, silence_points(wav))
    chunks = directory / "chunks"
    chunks.mkdir()
    combined_segments: list[dict[str, Any]] = []
    raw_chunks: list[dict[str, Any]] = []
    started = time.monotonic()
    model = active["models"]["moss"]
    for index, (start, end) in enumerate(ranges, 1):
        audio = chunks / f"chunk-{index:02d}.wav"
        raw = chunks / f"chunk-{index:02d}.json"
        extracted = len(ranges) != 1
        if not extracted:
            audio = wav
        else:
            extract_wav_chunk(wav, audio, start, end)
        command = [
            active["python"],
            str(SCRIPTS / "moss_runner.py"),
            "--model",
            model["path"],
            "--audio",
            str(audio),
            "--output",
            str(raw),
        ]
        try:
            result = _runner(command, raw)
        finally:
            if extracted:
                audio.unlink(missing_ok=True)
        if result["status"] != "success":
            failure = {**result, "chunk_index": index, "start": start, "end": end}
            write_json_atomic(directory / "error.json", failure)
            return failure
        payload = json.loads(raw.read_text(encoding="utf-8"))
        raw_chunks.append(
            {
                "index": index,
                "start": start,
                "end": end,
                "text": payload.get("text", ""),
                "segments": payload.get("segments", []),
                "metrics": {
                    "prompt_tokens": payload.get("prompt_tokens"),
                    "generation_tokens": payload.get("generation_tokens"),
                    "elapsed_seconds": payload.get("elapsed_seconds"),
                },
            }
        )
        combined_segments.extend(
            _qualify_moss_segments(payload.get("segments", []), start, index)
        )
    text = "\n".join(
        str(item["text"]).strip() for item in raw_chunks if str(item["text"]).strip()
    )
    payload = {
        "schema_version": 1,
        "model": model,
        "text": text,
        "segments": combined_segments,
        "chunks": raw_chunks,
        "speaker_warning": "Speaker IDs are qualified by chunk and are not stable identities across chunks.",
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    write_json_atomic(directory / "raw.json", payload)
    (directory / "transcript.txt").write_text(
        text + ("\n" if text else ""), encoding="utf-8"
    )
    return {
        "status": "success",
        "characters": len(text),
        "segments": len(combined_segments),
        "chunks": len(ranges),
        "elapsed_seconds": payload["elapsed_seconds"],
    }


def _safe_model_call(name: str, directory: Path, function: Any) -> dict[str, Any]:
    try:
        return function()
    except CliError as exc:
        failure = {
            "status": "failed",
            "error_code": exc.code,
            "message": exc.message,
        }
    except Exception as exc:  # noqa: BLE001 - isolate independent model failures.
        failure = {
            "status": "failed",
            "error_code": "MODEL_FAILED",
            "message": f"{type(exc).__name__}: {exc}",
        }
    directory.mkdir(parents=True, exist_ok=True)
    write_json_atomic(directory / "error.json", failure)
    return failure


def _markdown(manifest: dict[str, Any], output: Path) -> None:
    source = manifest["input"]["path"]
    profile = manifest["runtime"]["profile"]
    lines = [
        "---",
        f"source: {json.dumps(source, ensure_ascii=False)}",
        f"created_at: {manifest['started_at']}",
        f"profile: {profile}",
        "models:",
        f"  qwen: {manifest['runtime']['models']['qwen']['repo']}@{manifest['runtime']['models']['qwen']['revision']}",
        f"  moss: {manifest['runtime']['models']['moss']['repo']}@{manifest['runtime']['models']['moss']['revision']}",
        "---",
        "",
        "> These are independent local ASR outputs. They were not merged or corrected.",
        "> Resolve disagreements from the original audio and context; agreement is not proof.",
        "",
    ]
    for key, title in (("qwen", "Qwen3-ASR"), ("moss", "MOSS-Transcribe-Diarize")):
        lines.extend([f"## {title}", ""])
        branch = manifest["models"][key]
        transcript = output / key / "transcript.txt"
        if branch["status"] == "success" and transcript.is_file():
            lines.append(transcript.read_text(encoding="utf-8").strip())
        else:
            lines.append(
                f"[FAILED: {branch.get('error_code', 'MODEL_FAILED')}] {branch.get('message', '')}"
            )
        lines.append("")
    (output / "transcript.md").write_text(
        "\n".join(lines).rstrip() + "\n", encoding="utf-8"
    )


def _prepare_output(requested: Path | None) -> Path:
    if requested is None:
        path = Path(tempfile.mkdtemp(prefix="audio-transcription-"))
        os.chmod(path, 0o700)
        return path.resolve()
    path = requested.expanduser().resolve()
    if path.exists() and (not path.is_dir() or any(path.iterdir())):
        raise CliError(
            "OUTPUT_EXISTS", f"Output directory must be empty or absent: {path}"
        )
    path.mkdir(parents=True, exist_ok=True)
    os.chmod(path, 0o700)
    return path


def transcribe(
    source: Path,
    *,
    output_dir: Path | None,
    language: str,
    parallel: bool,
    require_all: bool,
    no_cache: bool,
) -> dict[str, Any]:
    resolved = plan(source, language=language, parallel=parallel, no_cache=no_cache)
    output = _prepare_output(output_dir)
    key = resolved["execution"]["cache_key"]
    cached = None if no_cache else cache.lookup(key)
    if cached:
        cache.restore(cached, output)
        manifest_path = output / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["output_dir"] = str(output)
        manifest["cache"] = {"enabled": True, "hit": True, "key": key}
        write_json_atomic(manifest_path, manifest)
        if require_all and manifest["status"] != "completed":
            raise CliError(
                "PARTIAL_SUCCESS",
                "Cached result is partial and --require-all was requested.",
            )
        return manifest

    cache.clear(expired=True, dry_run=False)
    active = load_active()
    started = time.monotonic()
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "status": "running",
        "started_at": _utc_now(),
        "input": resolved["input"],
        "runtime": resolved["runtime"],
        "execution": resolved["execution"],
        "output_dir": str(output),
        "cache": {"enabled": not no_cache, "hit": False, "key": key},
        "models": {},
    }
    write_json_atomic(output / "manifest.json", manifest)
    with tempfile.TemporaryDirectory(prefix="audio-transcription-work-") as temporary:
        wav = Path(temporary) / "input.wav"
        transcode_wav(
            Path(resolved["input"]["path"]),
            wav,
            resolved["input"]["selected_audio_stream"],
        )
        raw_calls = {
            "qwen": lambda: _run_qwen(active, wav, output / "qwen", language),
            "moss": lambda: _run_moss(
                active, wav, output / "moss", resolved["input"]["duration_seconds"]
            ),
        }
        calls = {
            name: (
                lambda branch=name, call=function: _safe_model_call(
                    branch, output / branch, call
                )
            )
            for name, function in raw_calls.items()
        }
        if parallel:
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                futures = {
                    executor.submit(function): name for name, function in calls.items()
                }
                for future in concurrent.futures.as_completed(futures):
                    manifest["models"][futures[future]] = future.result()
                    write_json_atomic(output / "manifest.json", manifest)
        else:
            for name, function in calls.items():
                manifest["models"][name] = function()
                write_json_atomic(output / "manifest.json", manifest)

    successes = sum(
        item.get("status") == "success" for item in manifest["models"].values()
    )
    manifest["status"] = (
        "completed" if successes == 2 else "partial" if successes == 1 else "failed"
    )
    manifest["finished_at"] = _utc_now()
    manifest["elapsed_seconds"] = round(time.monotonic() - started, 3)
    _markdown(manifest, output)
    write_json_atomic(output / "manifest.json", manifest)
    if manifest["status"] in {"completed", "partial"} and not no_cache:
        cache.store(key, output, manifest)
    if manifest["status"] == "failed":
        raise CliError("MODEL_FAILED", "Both local transcription models failed.")
    if require_all and manifest["status"] != "completed":
        raise CliError(
            "PARTIAL_SUCCESS", "One model failed and --require-all was requested."
        )
    return manifest
