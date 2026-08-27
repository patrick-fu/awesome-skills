#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from audio_transcription.config import write_json_atomic
from audio_transcription.errors import CliError
from audio_transcription.media import probe, require_command

SUBMIT_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
QUERY_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"
RESOURCE_ID = "volc.seedasr.auc"
PENDING = {"20000001", "20000002"}
COMPLETE = "20000000"


def auth() -> tuple[dict[str, str], str]:
    if os.environ.get("DOUBAO_API_KEY"):
        return {"X-Api-Key": os.environ["DOUBAO_API_KEY"]}, "api-key"
    if os.environ.get("DOUBAO_APPID") and os.environ.get("DOUBAO_ACCESS_TOKEN"):
        return {
            "X-Api-App-Key": os.environ["DOUBAO_APPID"],
            "X-Api-Access-Key": os.environ["DOUBAO_ACCESS_TOKEN"],
        }, "legacy-app-token"
    raise CliError(
        "DOUBAO_CREDENTIALS_MISSING",
        "Set DOUBAO_API_KEY, or both DOUBAO_APPID and DOUBAO_ACCESS_TOKEN.",
    )


def safe_headers(response: Any) -> dict[str, str]:
    return {
        name: response.headers.get(name, "")
        for name in ("X-Api-Status-Code", "X-Api-Message", "X-Tt-Logid")
    }


def post(
    url: str, headers: dict[str, str], payload: dict[str, Any], timeout: float
) -> tuple[dict[str, Any], dict[str, str]]:
    if url not in {SUBMIT_URL, QUERY_URL}:
        raise CliError(
            "DOUBAO_URL_REJECTED", "Refusing a non-allowlisted API endpoint."
        )
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        # Endpoint is restricted to the fixed HTTPS allowlist above.
        with urllib.request.urlopen(request, timeout=timeout) as response:  # nosec B310
            body = response.read()
            response_headers = safe_headers(response)
    except urllib.error.HTTPError as exc:
        excerpt = exc.read().decode("utf-8", errors="replace")[:1000]
        raise CliError(
            "DOUBAO_HTTP_ERROR", f"Doubao HTTP {exc.code}: {excerpt}"
        ) from exc
    except urllib.error.URLError as exc:
        raise CliError(
            "DOUBAO_NETWORK_ERROR", f"Doubao network error: {exc.reason}"
        ) from exc
    try:
        return (json.loads(body.decode("utf-8")) if body else {}), response_headers
    except json.JSONDecodeError as exc:
        raise CliError(
            "DOUBAO_RESPONSE_INVALID", f"Doubao returned invalid JSON: {exc}"
        ) from exc


def convert_mp3(source: Path, destination: Path, stream: int) -> None:
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
        f"0:{stream}",
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "libmp3lame",
        "-b:a",
        "64k",
        str(destination),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode:
        raise CliError(
            "MEDIA_TRANSCODE_FAILED",
            (completed.stderr or "ffmpeg failed").strip()[-1500:],
        )


def segments(payload: dict[str, Any]) -> list[dict[str, Any]]:
    result = payload.get("result", payload)
    utterances = result.get("utterances", payload.get("utterances", []))
    normalized = []
    for item in utterances:
        text = str(item.get("text", "")).strip()
        if text:
            normalized.append(
                {
                    "start": float(item.get("start_time", 0) or 0) / 1000,
                    "end": float(item.get("end_time", 0) or 0) / 1000,
                    "speaker": item.get("speaker_id", item.get("speaker")),
                    "text": text,
                }
            )
    if not normalized and str(result.get("text", "")).strip():
        normalized.append(
            {"start": 0, "end": 0, "speaker": None, "text": str(result["text"]).strip()}
        )
    return normalized


def timestamp(value: float) -> str:
    milliseconds = max(0, round(value * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{millis:03d}"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("input", type=Path)
    parser.add_argument("--online-consent", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--doubao-audio-url")
    parser.add_argument(
        "--audio-format", choices=("raw", "wav", "mp3", "ogg"), default="mp3"
    )
    parser.add_argument("--enable-ddc", action="store_true")
    parser.add_argument("--poll-interval", type=float, default=5)
    parser.add_argument("--online-timeout", type=float, default=1800)
    parser.add_argument("--http-timeout", type=float, default=180)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def execute(args: argparse.Namespace) -> dict[str, Any]:
    if not args.online_consent:
        raise CliError(
            "ONLINE_CONSENT_REQUIRED",
            "Explicit online/cloud/upload intent is required before passing --online-consent.",
            requires_user_decision=True,
        )
    source = args.input.expanduser().resolve()
    metadata = probe(source)
    credentials, auth_mode = auth()
    output = (
        args.output_dir.expanduser().resolve()
        if args.output_dir
        else Path(tempfile.mkdtemp(prefix="audio-transcription-online-"))
    )
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise CliError(
            "OUTPUT_EXISTS", f"Output directory must be empty or absent: {output}"
        )
    output.mkdir(parents=True, exist_ok=True)
    os.chmod(output, 0o700)
    task_id = str(uuid.uuid4())
    with tempfile.TemporaryDirectory(prefix="audio-transcription-upload-") as temporary:
        if args.doubao_audio_url:
            audio = {"url": args.doubao_audio_url, "format": args.audio_format}
            transport = "documented-url"
        else:
            mp3 = Path(temporary) / "input.mp3"
            convert_mp3(source, mp3, metadata["selected_audio_stream"])
            audio = {
                "data": base64.b64encode(mp3.read_bytes()).decode("ascii"),
                "format": "mp3",
                "rate": 16000,
                "channel": 1,
            }
            transport = "base64-data"
        headers = {
            **credentials,
            "X-Api-Resource-Id": RESOURCE_ID,
            "X-Api-Request-Id": task_id,
            "X-Api-Sequence": "-1",
        }
        request = {
            "user": {"uid": "audio-transcription-skill"},
            "audio": audio,
            "request": {
                "model_name": "bigmodel",
                "ssd_version": "200",
                "enable_itn": True,
                "enable_punc": True,
                "enable_ddc": args.enable_ddc,
                "show_utterances": True,
                "enable_speaker_info": True,
            },
        }
        _, submit_headers = post(SUBMIT_URL, headers, request, args.http_timeout)
        if submit_headers.get("X-Api-Status-Code") not in {COMPLETE, *PENDING}:
            raise CliError(
                "DOUBAO_SUBMIT_FAILED", f"Doubao submit failed: {submit_headers}"
            )
        query_headers = {
            **credentials,
            "X-Api-Resource-Id": RESOURCE_ID,
            "X-Api-Request-Id": task_id,
        }
        deadline = time.monotonic() + args.online_timeout
        response = None
        while time.monotonic() < deadline:
            body, response_headers = post(
                QUERY_URL,
                query_headers,
                {},
                min(args.http_timeout, max(1, deadline - time.monotonic())),
            )
            code = response_headers.get("X-Api-Status-Code")
            print(f"doubao status={code}", file=sys.stderr)
            if code == COMPLETE:
                response = body
                break
            if code not in PENDING:
                raise CliError(
                    "DOUBAO_QUERY_FAILED", f"Doubao query failed: {response_headers}"
                )
            time.sleep(args.poll_interval)
    if response is None:
        raise CliError("DOUBAO_TIMEOUT", f"Doubao query timed out; task_id={task_id}")
    normalized = segments(response)
    raw = {
        "schema_version": 1,
        "provider": "Doubao Speech / Volcengine",
        "task_id": task_id,
        "auth_mode": auth_mode,
        "audio_transport": transport,
        "enable_ddc": args.enable_ddc,
        "api_response": response,
        "segments": normalized,
    }
    write_json_atomic(output / "raw.json", raw)
    transcript = "\n".join(
        f"[{timestamp(item['start'])} --> {timestamp(item['end'])}"
        + (
            f" speaker={item['speaker']}"
            if item.get("speaker") not in (None, "")
            else ""
        )
        + f"] {item['text']}"
        for item in normalized
    )
    (output / "transcript.txt").write_text(
        transcript + ("\n" if transcript else ""), encoding="utf-8"
    )
    result = {
        "schema_version": 1,
        "status": "completed",
        "mode": "online",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input": {"path": str(source), **metadata},
        "provider": {
            "name": "doubao",
            "task_id": task_id,
            "transport": transport,
            "enable_ddc": args.enable_ddc,
        },
        "output_dir": str(output),
        "artifacts": {
            "manifest": str(output / "manifest.json"),
            "raw": str(output / "raw.json"),
            "transcript": str(output / "transcript.txt"),
        },
    }
    write_json_atomic(output / "manifest.json", result)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parse_args(list(sys.argv[1:] if argv is None else argv))
    try:
        result = execute(args)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
        else:
            print(f"status: {result['status']}\noutput_dir: {result['output_dir']}")
        return 0
    except CliError as exc:
        if args.json:
            print(json.dumps(exc.envelope(), ensure_ascii=False, separators=(",", ":")))
        else:
            print(f"{exc.code}: {exc.message}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
