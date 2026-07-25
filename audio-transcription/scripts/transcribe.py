#!/usr/bin/env python3
"""Transcribe media with local MLX Whisper, Doubao ASR, or both."""

from __future__ import annotations

import argparse
import base64
import concurrent.futures
import contextlib
import datetime as dt
import difflib
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from collections.abc import Mapping
from pathlib import Path
from typing import Any


SUBMIT_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
QUERY_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"
RESOURCE_ID = "volc.seedasr.auc"
MODEL_NAME = "bigmodel"
DEFAULT_WHISPER_MODEL = "mlx-community/whisper-large-v3-turbo"
PENDING_CODES = {"20000001", "20000002"}
COMPLETE_CODE = "20000000"
DOUBAO_DOC_URL = "https://docs.volcengine.com/docs/6561/1354868?lang=zh"


class TranscriptionError(RuntimeError):
    """A user-actionable transcription failure."""


def json_safe(value: Any) -> Any:
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(json_safe(value), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def timestamp(seconds: float) -> str:
    milliseconds = max(0, round(float(seconds) * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def require_command(name: str) -> str:
    resolved = shutil.which(name)
    if not resolved:
        raise TranscriptionError(f"Required command is missing: {name}")
    return resolved


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def probe_media(path: Path) -> dict[str, Any]:
    ffprobe = require_command("ffprobe")
    completed = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration,size,format_name:stream=index,codec_type,codec_name,sample_rate,channels",
            "-of",
            "json",
            str(path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or "unknown ffprobe error"
        raise TranscriptionError(f"ffprobe failed: {detail}")
    payload = json.loads(completed.stdout)
    if not any(stream.get("codec_type") == "audio" for stream in payload.get("streams", [])):
        raise TranscriptionError("Input contains no audio stream")
    return payload


def transcode_mp3(input_path: Path, output_path: Path) -> None:
    ffmpeg = require_command("ffmpeg")
    completed = subprocess.run(
        [
            ffmpeg,
            "-nostdin",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(input_path),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "64k",
            str(output_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or "unknown ffmpeg error"
        raise TranscriptionError(f"ffmpeg MP3 conversion failed: {detail}")


def extract_additions_speaker(additions: Any) -> Any:
    if isinstance(additions, str):
        with contextlib.suppress(json.JSONDecodeError):
            additions = json.loads(additions)
    if not isinstance(additions, dict):
        return None
    return additions.get("speaker", additions.get("speaker_id"))


def normalize_whisper_segments(raw: dict[str, Any]) -> list[dict[str, Any]]:
    result = raw.get("result", raw)
    segments = []
    for item in result.get("segments", []):
        text = str(item.get("text", "")).strip()
        if not text:
            continue
        segments.append(
            {
                "start": float(item.get("start", 0) or 0),
                "end": float(item.get("end", 0) or 0),
                "text": text,
                "speaker": None,
            }
        )
    return segments


def normalize_doubao_segments(raw: dict[str, Any]) -> list[dict[str, Any]]:
    response = raw.get("api_response", raw)
    result = response.get("result", response)
    utterances = result.get("utterances", response.get("utterances", []))
    segments = []
    for item in utterances:
        text = str(item.get("text", "")).strip()
        if not text:
            continue
        speaker = item.get("speaker_id", item.get("speaker"))
        if speaker in (None, ""):
            speaker = extract_additions_speaker(item.get("additions"))
        segments.append(
            {
                "start": float(item.get("start_time", 0) or 0) / 1000.0,
                "end": float(item.get("end_time", 0) or 0) / 1000.0,
                "text": text,
                "speaker": speaker,
            }
        )
    if not segments and str(result.get("text", "")).strip():
        segments.append(
            {
                "start": 0.0,
                "end": 0.0,
                "text": str(result["text"]).strip(),
                "speaker": None,
            }
        )
    return segments


def render_transcript(segments: list[dict[str, Any]]) -> str:
    lines = []
    for segment in segments:
        speaker = segment.get("speaker")
        speaker_suffix = f" speaker={speaker}" if speaker not in (None, "") else ""
        lines.append(
            f"[{timestamp(segment['start'])} --> {timestamp(segment['end'])}{speaker_suffix}] "
            f"{segment['text']}"
        )
    return "\n".join(lines) + ("\n" if lines else "")


def build_whisper_cli_command(
    args: argparse.Namespace,
    output_dir: Path,
    output_name: str,
) -> list[str]:
    mlx_whisper = shutil.which("mlx_whisper")
    if not mlx_whisper:
        raise TranscriptionError(
            "mlx_whisper CLI is missing. Install it with `uv tool install mlx-whisper`."
        )
    command = [
        mlx_whisper,
        str(args.input),
        "--model",
        args.whisper_model,
        "--output-dir",
        str(output_dir),
        "--output-name",
        output_name,
        "--output-format",
        "json",
        "--verbose",
        "False",
        "--task",
        "transcribe",
        "--condition-on-previous-text",
        str(args.condition_on_previous_text),
        "--word-timestamps",
        "False",
    ]
    if args.language != "auto":
        command.extend(["--language", args.language])
    if args.initial_prompt:
        command.extend(["--initial-prompt", args.initial_prompt])
    return command


def transcribe_whisper(args: argparse.Namespace, output_dir: Path) -> dict[str, Any]:
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="audio-transcription-whisper-") as temp_dir:
        cli_output_dir = Path(temp_dir)
        output_name = "mlx-whisper-result"
        command = build_whisper_cli_command(args, cli_output_dir, output_name)
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout).strip()[-2000:]
            raise TranscriptionError(
                f"mlx_whisper CLI failed with exit {completed.returncode}: {detail}"
            )
        result_path = cli_output_dir / f"{output_name}.json"
        if not result_path.is_file():
            raise TranscriptionError(
                f"mlx_whisper CLI did not create expected JSON: {result_path}"
            )
        result = json.loads(result_path.read_text(encoding="utf-8"))

    wrapped = {
        "provenance": {
            "provider": "local MLX Whisper CLI",
            "model": args.whisper_model,
            "model_resolution": "CLI and Hugging Face default cache",
            "language_requested": args.language,
            "condition_on_previous_text": args.condition_on_previous_text,
            "elapsed_seconds": round(time.monotonic() - started, 3),
        },
        "result": result,
    }
    segments = normalize_whisper_segments(wrapped)
    write_json(output_dir / "raw.json", wrapped)
    (output_dir / "transcript.txt").write_text(render_transcript(segments), encoding="utf-8")
    return {
        "status": "success",
        "segments": len(segments),
        "characters": sum(len(item["text"]) for item in segments),
        "language": result.get("language"),
        "elapsed_seconds": wrapped["provenance"]["elapsed_seconds"],
    }


def safe_response_headers(response: Any) -> dict[str, str]:
    return {
        key: response.headers.get(key, "")
        for key in ("X-Api-Status-Code", "X-Api-Message", "X-Tt-Logid")
    }


def resolve_doubao_auth(
    environ: Mapping[str, str] | None = None,
) -> tuple[dict[str, str], str]:
    source = os.environ if environ is None else environ
    api_key = source.get("DOUBAO_API_KEY")
    if api_key:
        return {"X-Api-Key": api_key}, "new-console-api-key"

    app_id = source.get("DOUBAO_APPID")
    access_token = source.get("DOUBAO_ACCESS_TOKEN")
    if app_id and access_token:
        return {
            "X-Api-App-Key": app_id,
            "X-Api-Access-Key": access_token,
        }, "legacy-app-id-access-token"

    raise TranscriptionError(
        "Missing Doubao credentials. Set DOUBAO_API_KEY for the new console, "
        "or set both DOUBAO_APPID and DOUBAO_ACCESS_TOKEN for the legacy console."
    )


def build_doubao_audio_payload(
    args: argparse.Namespace,
    converted_mp3: Path | None,
) -> tuple[dict[str, Any], str]:
    if args.doubao_audio_url:
        return {
            "url": args.doubao_audio_url,
            "format": args.doubao_audio_format,
        }, "documented-url"
    if converted_mp3 is None:
        raise TranscriptionError("Converted MP3 is required for inline audio upload")
    return {
        "data": base64.b64encode(converted_mp3.read_bytes()).decode("ascii"),
        "format": "mp3",
        "rate": 16000,
        "channel": 1,
    }, "base64-data-compatibility"


def post_json(url: str, headers: dict[str, str], payload: dict[str, Any], timeout: float) -> tuple[Any, dict[str, str]]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            safe = safe_response_headers(response)
    except urllib.error.HTTPError as error:
        body = error.read()
        safe = safe_response_headers(error)
        excerpt = body.decode("utf-8", errors="replace")[:1000]
        raise TranscriptionError(
            f"Doubao HTTP error: http={error.code} headers={safe} body={excerpt}"
        ) from error
    except urllib.error.URLError as error:
        raise TranscriptionError(f"Doubao network error: {error.reason}") from error

    try:
        decoded = json.loads(body.decode("utf-8")) if body else {}
    except json.JSONDecodeError as error:
        raise TranscriptionError(
            f"Doubao returned invalid JSON: headers={safe} body={body[:1000]!r}"
        ) from error
    return decoded, safe


def transcribe_doubao(args: argparse.Namespace, output_dir: Path) -> dict[str, Any]:
    auth_headers, auth_mode = resolve_doubao_auth()

    started = time.monotonic()
    task_id = str(uuid.uuid4())
    events: list[dict[str, Any]] = []
    request_options = {
        "model_name": MODEL_NAME,
        "ssd_version": "200",
        "enable_itn": True,
        "enable_punc": True,
        "enable_ddc": args.enable_ddc,
        "show_utterances": True,
        "enable_speaker_info": True,
    }

    with tempfile.TemporaryDirectory(prefix="audio-transcription-online-") as temp_dir:
        mp3_path: Path | None = None
        if not args.doubao_audio_url:
            mp3_path = Path(temp_dir) / "input-16k-mono.mp3"
            transcode_mp3(args.input, mp3_path)
        audio_payload, audio_transport = build_doubao_audio_payload(args, mp3_path)
        headers = {
            **auth_headers,
            "X-Api-Resource-Id": RESOURCE_ID,
            "X-Api-Request-Id": task_id,
            "X-Api-Sequence": "-1",
            "Content-Type": "application/json",
        }
        payload = {
            "user": {"uid": "audio-transcription-skill"},
            "audio": audio_payload,
            "request": request_options,
        }
        _, submit_headers = post_json(SUBMIT_URL, headers, payload, args.http_timeout)
        submit_code = submit_headers.get("X-Api-Status-Code")
        events.append(
            {
                "phase": "submit",
                "headers": submit_headers,
                "elapsed_seconds": round(time.monotonic() - started, 3),
            }
        )
        if submit_code not in {COMPLETE_CODE, *PENDING_CODES}:
            raise TranscriptionError(
                f"Doubao submit failed: status={submit_code} headers={submit_headers}"
            )

        query_headers = {
            **auth_headers,
            "X-Api-Resource-Id": RESOURCE_ID,
            "X-Api-Request-Id": task_id,
            "Content-Type": "application/json",
        }

        deadline = time.monotonic() + args.online_timeout
        response_json: dict[str, Any] | None = None
        attempt = 0
        while time.monotonic() < deadline:
            attempt += 1
            body, query_safe = post_json(
                QUERY_URL,
                query_headers,
                {},
                min(args.http_timeout, max(1.0, deadline - time.monotonic())),
            )
            code = query_safe.get("X-Api-Status-Code")
            event = {
                "phase": "query",
                "attempt": attempt,
                "headers": query_safe,
                "elapsed_seconds": round(time.monotonic() - started, 3),
            }
            events.append(event)
            print(
                json.dumps(
                    {"provider": "doubao", "status": code, "attempt": attempt},
                    ensure_ascii=False,
                ),
                flush=True,
            )
            if code == COMPLETE_CODE:
                response_json = body
                break
            if code not in PENDING_CODES:
                raise TranscriptionError(
                    f"Doubao query failed: status={code} headers={query_safe}"
                )
            time.sleep(args.poll_interval)

    if response_json is None:
        raise TranscriptionError(
            f"Doubao ASR query timed out after {args.online_timeout:.0f} seconds; "
            f"task_id={task_id}"
        )

    wrapped = {
        "provenance": {
            "provider": "Doubao Speech / Volcengine",
            "endpoint_submit": SUBMIT_URL,
            "endpoint_query": QUERY_URL,
            "resource_id": RESOURCE_ID,
            "model_name": MODEL_NAME,
            "documentation": DOUBAO_DOC_URL,
            "auth_mode": auth_mode,
            "options": request_options,
            "audio_format": audio_payload["format"],
            "audio_transport": audio_transport,
            "audio_conversion": (
                "16 kHz mono MP3 at 64 kbps"
                if mp3_path is not None
                else "not performed; caller supplied remote URL"
            ),
            "task_id": task_id,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "events": events,
        },
        "api_response": response_json,
    }
    segments = normalize_doubao_segments(wrapped)
    write_json(output_dir / "raw.json", wrapped)
    (output_dir / "transcript.txt").write_text(render_transcript(segments), encoding="utf-8")
    return {
        "status": "success",
        "segments": len(segments),
        "characters": sum(len(item["text"]) for item in segments),
        "enable_ddc": args.enable_ddc,
        "auth_mode": auth_mode,
        "audio_transport": audio_transport,
        "task_id": task_id,
        "elapsed_seconds": wrapped["provenance"]["elapsed_seconds"],
    }


def compact_text(value: str) -> str:
    return re.sub(r"[\W_]+", "", value, flags=re.UNICODE).lower()


def collect_terms(text: str) -> set[str]:
    return set(
        re.findall(r"[+-]?\d+(?:\.\d+)?%?|[A-Za-z][A-Za-z0-9+_.-]{1,}", text)
    )


def repeated_neighbors(segments: list[dict[str, Any]]) -> list[str]:
    warnings = []
    previous = ""
    for segment in segments:
        current = compact_text(segment["text"])
        if current and len(current) >= 6 and current == previous:
            warnings.append(f"{timestamp(segment['start'])}: {segment['text'][:80]}")
        previous = current
    return warnings


def overlap_text(
    segment: dict[str, Any],
    candidates: list[dict[str, Any]],
    padding: float = 1.0,
) -> str:
    chunks = [
        candidate["text"]
        for candidate in candidates
        if candidate["end"] >= segment["start"] - padding
        and candidate["start"] <= segment["end"] + padding
    ]
    return "".join(chunks)


def build_cross_validation(
    offline_segments: list[dict[str, Any]],
    online_segments: list[dict[str, Any]],
) -> str:
    offline_text = "".join(item["text"] for item in offline_segments)
    online_text = "".join(item["text"] for item in online_segments)
    global_ratio = difflib.SequenceMatcher(
        None, compact_text(offline_text), compact_text(online_text), autojunk=False
    ).ratio()
    offline_terms = collect_terms(offline_text)
    online_terms = collect_terms(online_text)

    divergences = []
    for segment in offline_segments:
        comparison = overlap_text(segment, online_segments)
        if not comparison:
            ratio = 0.0
        else:
            ratio = difflib.SequenceMatcher(
                None,
                compact_text(segment["text"]),
                compact_text(comparison),
                autojunk=False,
            ).ratio()
        if ratio < 0.45:
            divergences.append((ratio, segment, comparison))
    divergences.sort(key=lambda item: item[0])

    def coverage(segments: list[dict[str, Any]]) -> str:
        if not segments:
            return "无有效分段"
        return f"{timestamp(segments[0]['start'])} – {timestamp(max(item['end'] for item in segments))}"

    lines = [
        "# 双路转写机械核验",
        "",
        "> 本报告只做时间覆盖、字符串和术语差异检查。最终结论仍需结合音频上下文人工复核。",
        "",
        "## 概览",
        "",
        f"- Whisper 分段：{len(offline_segments)}；覆盖：{coverage(offline_segments)}",
        f"- 豆包分段：{len(online_segments)}；覆盖：{coverage(online_segments)}",
        f"- 全文字符相似度：{global_ratio:.1%}",
        "",
        "## 数字与英文术语差异",
        "",
        f"- 仅 Whisper：{', '.join(sorted(offline_terms - online_terms)) or '无'}",
        f"- 仅豆包：{', '.join(sorted(online_terms - offline_terms)) or '无'}",
        "",
        "## 疑似连续重复",
        "",
        f"- Whisper：{'; '.join(repeated_neighbors(offline_segments)) or '未发现'}",
        f"- 豆包：{'; '.join(repeated_neighbors(online_segments)) or '未发现'}",
        "",
        "## 低一致度时间段",
        "",
    ]
    if divergences:
        for ratio, segment, comparison in divergences[:20]:
            lines.extend(
                [
                    f"### {timestamp(segment['start'])} – {timestamp(segment['end'])}（{ratio:.0%}）",
                    "",
                    f"- Whisper：{segment['text'][:240]}",
                    f"- 豆包重叠内容：{comparison[:240] or '未找到重叠分段'}",
                    "",
                ]
            )
    else:
        lines.append("- 未发现低于阈值的 Whisper 分段。")
        lines.append("")

    lines.extend(
        [
            "## 人工复核重点",
            "",
            "- 姓名、公司名、产品名、英文缩写",
            "- 数字、百分比、日期、否定词",
            "- 一路缺失而另一路存在的完整句段",
            "- Whisper 连续复读或静音区幻觉",
            "- 豆包说话人聚类异常",
            "",
        ]
    )
    return "\n".join(lines)


def run_branch(
    name: str,
    args: argparse.Namespace,
    output_dir: Path,
) -> dict[str, Any]:
    branch_dir = output_dir / name
    branch_dir.mkdir(parents=True, exist_ok=True)
    try:
        if name == "offline":
            return transcribe_whisper(args, branch_dir)
        return transcribe_doubao(args, branch_dir)
    except Exception as error:
        failure = {
            "status": "failed",
            "error_type": type(error).__name__,
            "error": str(error),
        }
        write_json(branch_dir / "error.json", failure)
        return failure


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Local audio or video file")
    parser.add_argument(
        "--mode",
        choices=("dual", "offline", "online"),
        default="dual",
        help="Recognition mode; default: dual",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Artifact directory; defaults to a new system temporary directory",
    )
    parser.add_argument(
        "--online-consent",
        action="store_true",
        help="Confirm that uploading a converted copy to Doubao is authorized",
    )
    parser.add_argument("--language", default="auto", help="Whisper language code or auto")
    parser.add_argument("--initial-prompt", help="Optional domain terms for Whisper")
    parser.add_argument("--whisper-model", default=DEFAULT_WHISPER_MODEL)
    parser.add_argument(
        "--condition-on-previous-text",
        action="store_true",
        help="Enable Whisper previous-window conditioning; disabled by default",
    )
    parser.add_argument(
        "--enable-ddc",
        action="store_true",
        help="Enable Doubao semantic smoothing; disabled for faithful transcription",
    )
    parser.add_argument(
        "--doubao-audio-url",
        help="Use the standard API's documented remote URL transport",
    )
    parser.add_argument(
        "--doubao-audio-format",
        choices=("raw", "wav", "mp3", "ogg"),
        default="mp3",
        help="Container format of --doubao-audio-url; default: mp3",
    )
    parser.add_argument("--poll-interval", type=float, default=5.0)
    parser.add_argument("--online-timeout", type=float, default=1800.0)
    parser.add_argument("--http-timeout", type=float, default=180.0)
    return parser.parse_args(argv)


def preflight(args: argparse.Namespace) -> tuple[Path, dict[str, Any]]:
    args.input = args.input.expanduser().resolve()
    if not args.input.is_file():
        raise TranscriptionError(f"Input file does not exist: {args.input}")
    if args.mode in {"dual", "online"} and not args.online_consent:
        raise TranscriptionError(
            "Online upload is not authorized. Obtain explicit user consent, then pass "
            "--online-consent."
        )
    if args.mode in {"dual", "offline"} and not shutil.which("mlx_whisper"):
        raise TranscriptionError(
            "mlx_whisper CLI is missing. Install it with `uv tool install mlx-whisper`."
        )
    if args.mode in {"dual", "online"}:
        if not args.doubao_audio_url:
            require_command("ffmpeg")
        resolve_doubao_auth()
    metadata = probe_media(args.input)
    if args.output_dir:
        output_dir = args.output_dir.expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path(tempfile.mkdtemp(prefix="audio-transcription-")).resolve()
    return output_dir, metadata


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        output_dir, media_metadata = preflight(args)
    except TranscriptionError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    started_at = dt.datetime.now(dt.timezone.utc)
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "mode": args.mode,
        "input": {
            "path": str(args.input),
            "sha256": sha256_file(args.input),
            "probe": media_metadata,
        },
        "started_at": started_at.isoformat(),
        "output_dir": str(output_dir),
        "branches": {},
    }
    write_json(output_dir / "manifest.json", manifest)

    branches = ["offline", "online"] if args.mode == "dual" else [args.mode]
    if len(branches) == 2:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_map = {
                executor.submit(run_branch, name, args, output_dir): name
                for name in branches
            }
            for future in concurrent.futures.as_completed(future_map):
                name = future_map[future]
                manifest["branches"][name] = future.result()
                write_json(output_dir / "manifest.json", manifest)
    else:
        name = branches[0]
        manifest["branches"][name] = run_branch(name, args, output_dir)

    if all(
        manifest["branches"].get(name, {}).get("status") == "success"
        for name in ("offline", "online")
    ):
        offline_raw = json.loads((output_dir / "offline" / "raw.json").read_text(encoding="utf-8"))
        online_raw = json.loads((output_dir / "online" / "raw.json").read_text(encoding="utf-8"))
        report = build_cross_validation(
            normalize_whisper_segments(offline_raw),
            normalize_doubao_segments(online_raw),
        )
        (output_dir / "cross-validation.md").write_text(report, encoding="utf-8")

    finished_at = dt.datetime.now(dt.timezone.utc)
    manifest["finished_at"] = finished_at.isoformat()
    manifest["elapsed_seconds"] = round(
        (finished_at - started_at).total_seconds(), 3
    )
    write_json(output_dir / "manifest.json", manifest)

    failed = [
        name
        for name, result in manifest["branches"].items()
        if result.get("status") != "success"
    ]
    print(
        json.dumps(
            {
                "mode": args.mode,
                "output_dir": str(output_dir),
                "branches": manifest["branches"],
                "failed": failed,
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
