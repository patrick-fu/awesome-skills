#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import platform
import shutil
import sys
from pathlib import Path
from typing import Any

from audio_transcription import __version__, cache, pipeline
from audio_transcription.config import load_active, load_lock
from audio_transcription.errors import CliError

COMMANDS = {"transcribe", "plan", "doctor", "cache"}


def _common(parser: argparse.ArgumentParser, *, output: bool) -> None:
    parser.add_argument("input", type=Path)
    if output:
        parser.add_argument("--output-dir", type=Path)
        parser.add_argument("--require-all", action="store_true")
        parser.add_argument("--print", dest="print_transcript", action="store_true")
    parser.add_argument("--language", default="auto")
    parser.add_argument("--parallel", action="store_true")
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--json", action="store_true")


def parse_args(argv: list[str]) -> argparse.Namespace:
    if argv and argv[0] not in COMMANDS and not argv[0].startswith("-"):
        argv = ["transcribe", *argv]
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--version", action="version", version=f"local-transcribe {__version__}"
    )
    sub = parser.add_subparsers(dest="command", required=True)
    transcribe = sub.add_parser("transcribe", add_help=False)
    _common(transcribe, output=True)
    plan = sub.add_parser("plan", add_help=False)
    _common(plan, output=False)
    doctor = sub.add_parser("doctor", add_help=False)
    doctor.add_argument("--json", action="store_true")
    cache_parser = sub.add_parser("cache", add_help=False)
    cache_sub = cache_parser.add_subparsers(dest="cache_command", required=True)
    status = cache_sub.add_parser("status", add_help=False)
    status.add_argument("--json", action="store_true")
    clear = cache_sub.add_parser("clear", add_help=False)
    clear.add_argument("--dry-run", action="store_true")
    clear.add_argument("--expired", action="store_true")
    clear.add_argument("--all", action="store_true")
    clear.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if getattr(args, "print_transcript", False) and getattr(args, "json", False):
        parser.error("--print and --json are mutually exclusive")
    return args


def _print(value: dict[str, Any], *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(value, ensure_ascii=False, separators=(",", ":")))
        return
    if value.get("status") == "error":
        print(f"{value.get('error_code')}: {value.get('message')}", file=sys.stderr)
        for action in value.get("next_actions", []):
            suggestion = action.get("command") or action.get("instruction")
            if suggestion:
                print(f"Next: {suggestion}", file=sys.stderr)
        return
    print(f"status: {value.get('status')}")
    if value.get("output_dir"):
        print(f"output_dir: {value['output_dir']}")
    if value.get("cache"):
        print(f"cache_hit: {value['cache'].get('hit', False)}")


def doctor() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    checks.append(
        {
            "name": "macOS",
            "ok": platform.system() == "Darwin",
            "value": platform.system(),
        }
    )
    machine = platform.machine()
    checks.append({"name": "Apple Silicon", "ok": machine == "arm64", "value": machine})
    for command in ("ffmpeg", "ffprobe"):
        checks.append(
            {
                "name": command,
                "ok": bool(shutil.which(command)),
                "value": shutil.which(command),
            }
        )
    active = None
    try:
        active = load_active()
        checks.append(
            {"name": "active runtime", "ok": True, "value": active["runtime_version"]}
        )
        checks.append({"name": "profile", "ok": True, "value": active["profile"]})
        checks.append(
            {
                "name": "runtime python",
                "ok": Path(active["python"]).is_file(),
                "value": active["python"],
            }
        )
        for name, model in active["models"].items():
            checks.append(
                {
                    "name": f"{name} model",
                    "ok": Path(model["path"]).is_dir(),
                    "value": model["path"],
                }
            )
    except CliError as exc:
        checks.append({"name": "active runtime", "ok": False, "value": exc.code})
    ok = all(item["ok"] for item in checks)
    return {
        "status": "ready" if ok else "not_ready",
        "checks": checks,
        "active": active,
        "lock": load_lock(),
        "next_actions": []
        if ok
        else [
            {
                "kind": "invoke_skill",
                "instruction": "Invoke $audio-transcription and request setup.",
            }
        ],
    }


def cache_command(args: argparse.Namespace) -> dict[str, Any]:
    if args.cache_command == "status":
        items = cache.scan()
        return {
            "status": "ready",
            "entries": len(items),
            "size_bytes": sum(item["size_bytes"] for item in items),
            "items": items,
        }
    all_entries = bool(args.all)
    expired = bool(args.expired) or not all_entries
    dry_run = bool(args.dry_run) or not (args.expired or args.all)
    selected = cache.clear(expired=expired, all_entries=all_entries, dry_run=dry_run)
    return {
        "status": "ready",
        "dry_run": dry_run,
        "selected_entries": len(selected),
        "selected_size_bytes": sum(item["size_bytes"] for item in selected),
        "items": selected,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(list(sys.argv[1:] if argv is None else argv))
    try:
        if args.command == "plan":
            value = pipeline.plan(
                args.input,
                language=args.language,
                parallel=args.parallel,
                no_cache=args.no_cache,
            )
        elif args.command == "doctor":
            value = doctor()
        elif args.command == "cache":
            value = cache_command(args)
        else:
            value = pipeline.transcribe(
                args.input,
                output_dir=args.output_dir,
                language=args.language,
                parallel=args.parallel,
                require_all=args.require_all,
                no_cache=args.no_cache,
            )
        _print(value, as_json=args.json)
        if args.command == "transcribe":
            if value["status"] == "partial":
                print(
                    "warning: one local model failed; see manifest.json",
                    file=sys.stderr,
                )
            if args.print_transcript:
                print(
                    Path(value["output_dir"], "transcript.md").read_text(
                        encoding="utf-8"
                    )
                )
        return 0 if value.get("status") not in {"failed", "not_ready"} else 1
    except CliError as exc:
        _print(exc.envelope(), as_json=getattr(args, "json", False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
