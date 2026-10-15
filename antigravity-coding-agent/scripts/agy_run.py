#!/usr/bin/env python3
"""Launch one guarded Antigravity attempt and retain its process evidence."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
from contextlib import ExitStack
from datetime import datetime, timezone


UNKNOWN = "UNKNOWN"
DURATION = re.compile(r"(?:0|[0-9]+(?:\.[0-9]+)?(?:ns|us|µs|ms|s|m|h))")
TIMEOUT = re.compile(
    r"print[- ]timeout.*(?:reached|exceeded|expired)|timed out|"
    r"timeout (?:reached|exceeded|expired)|deadline exceeded",
    re.IGNORECASE,
)


def parse_stream(stream_path: Path, stderr_path: Path, exit_code=UNKNOWN) -> dict:
    receipt = {
        "status": UNKNOWN,
        "exit": exit_code,
        "model": UNKNOWN,
        "cwd": UNKNOWN,
        "denied_actions": UNKNOWN,
        "response_bytes": UNKNOWN,
        "incomplete_final_line": UNKNOWN,
        "timeout_warning": UNKNOWN,
        "result_status": UNKNOWN,
    }
    malformed = False
    structured_error = False
    seen = set()
    try:
        with stream_path.open("rb") as stream:
            receipt["incomplete_final_line"] = False
            for line in stream:
                receipt["incomplete_final_line"] = not line.endswith(b"\n")
                try:
                    event = json.loads(line)
                except (ValueError, UnicodeDecodeError):
                    malformed = True
                    continue
                if not isinstance(event, dict):
                    malformed = True
                    continue
                kind = event.get("event")
                if kind in ("init", "result"):
                    if kind in seen:
                        malformed = True
                        continue
                    seen.add(kind)
                if kind == "init":
                    payload = event.get("init")
                    if not isinstance(payload, dict):
                        malformed = True
                        continue
                    for field in ("model", "cwd"):
                        value = payload.get(field)
                        receipt[field] = value if isinstance(value, str) and value else UNKNOWN
                        try:
                            receipt[field].encode("utf-8")
                        except UnicodeError:
                            receipt[field] = UNKNOWN
                elif kind == "result":
                    payload = event.get("result")
                    if not isinstance(payload, dict):
                        malformed = True
                        continue
                    status = payload.get("status")
                    receipt["result_status"] = (
                        status if isinstance(status, str) and status else UNKNOWN
                    )
                    denied = payload.get("denied_actions")
                    receipt["denied_actions"] = denied if isinstance(denied, list) else UNKNOWN
                    response = payload.get("response")
                    try:
                        receipt["response_bytes"] = (
                            len(response.encode("utf-8")) if isinstance(response, str) else UNKNOWN
                        )
                    except UnicodeError:
                        malformed = True
                    if payload.get("error"):
                        structured_error = True
    except OSError:
        malformed = True
    try:
        with stderr_path.open(encoding="utf-8", errors="replace") as stderr:
            receipt["timeout_warning"] = False
            for line in stderr:
                if TIMEOUT.search(line):
                    receipt["timeout_warning"] = True
                if "AGY_ERROR:" in line:
                    structured_error = True
    except OSError:
        pass

    if structured_error or (isinstance(exit_code, int) and exit_code != 0) or receipt["result_status"] not in (
        "SUCCESS", UNKNOWN
    ):
        receipt["status"] = "FAILED"
    elif (
        malformed
        or exit_code != 0
        or receipt["result_status"] != "SUCCESS"
        or receipt["model"] == UNKNOWN
        or receipt["cwd"] == UNKNOWN
        or receipt["denied_actions"] != []
        or receipt["response_bytes"] in (UNKNOWN, 0)
        or receipt["incomplete_final_line"] is not False
        or receipt["timeout_warning"] is not False
    ):
        receipt["status"] = "INCOMPLETE"
    else:
        receipt["status"] = "SUCCESS"
    return receipt


def run(args: argparse.Namespace) -> int:
    if not DURATION.fullmatch(args.print_timeout):
        raise ValueError("G0: --print-timeout needs a unit (for example 240s or 45m), or 0.")
    forwarded = args.launcher_args
    if forwarded[:1] == ["--"]:
        forwarded = forwarded[1:]
    for argument in forwarded:
        flag = argument.split("=", 1)[0].lstrip("-")
        if argument == "--" or (argument.startswith("-") and flag in {
            "p", "prompt", "prompt-file", "print-timeout", "output-format", "cwd"
        }) or (argument.startswith("-p") and not argument.startswith("--")):
            raise ValueError(
                "G0: use the launcher's --prompt-file, --cwd and --print-timeout options; "
                "output-format is owned by agy_run.py. Put only other agy options after --."
            )

    cwd = Path(args.cwd)
    if not cwd.is_absolute() or not cwd.is_dir():
        raise ValueError("G1: --cwd must be an absolute path to an existing directory.")
    cwd = cwd.resolve()
    home = Path.home().resolve()
    if cwd == home or cwd in home.parents:
        raise ValueError("G1: choose a project directory for --cwd, not HOME or an ancestor of HOME.")

    try:
        prompt_path = Path(args.prompt_file)
        if not prompt_path.is_file():
            raise OSError("not a regular file")
        prompt = prompt_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ValueError("G2: --prompt-file must name a readable UTF-8 file with task text.") from error
    if not prompt.strip() or "\0" in prompt:
        raise ValueError("G2: put nonempty task text without NUL bytes in --prompt-file.")

    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.label):
        raise ValueError("G3: use a label starting with a letter/digit and containing only letters, digits, . _ -.")
    temp_root = Path(os.environ.get("TMPDIR") or tempfile.gettempdir())
    if not temp_root.is_absolute() or not temp_root.is_dir():
        raise ValueError("G3: set TMPDIR to an absolute, writable existing temporary directory.")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    try:
        run_dir = Path(tempfile.mkdtemp(
            prefix=f"agy-{args.label}-{timestamp}-{os.getpid()}-", dir=temp_root
        ))
        with ExitStack() as files:
            stream = files.enter_context((run_dir / "stream.jsonl").open("xb"))
            stderr = files.enter_context((run_dir / "stderr.log").open("xb"))
            rc_file = files.enter_context((run_dir / "rc.txt").open("x", encoding="utf-8"))
            receipt_file = files.enter_context((run_dir / "receipt.json").open("x", encoding="utf-8"))
            print(json.dumps({"run_dir": str(run_dir)}), flush=True)
            exit_code = UNKNOWN
            launch_error = None
            try:
                child = subprocess.Popen(
                    [args.agy_bin, *forwarded, "--output-format", "stream-json",
                     "--print-timeout", args.print_timeout, "-p", prompt],
                    cwd=cwd, stdin=subprocess.DEVNULL, stdout=stream, stderr=stderr,
                )
                previous_handlers = {}

                def forward_signal(signum, frame):
                    if child.poll() is None:
                        child.send_signal(signum)

                try:
                    for signum in (signal.SIGINT, signal.SIGTERM):
                        previous_handlers[signum] = signal.signal(signum, forward_signal)
                    exit_code = child.wait()
                finally:
                    for signum, handler in previous_handlers.items():
                        signal.signal(signum, handler)
            except OSError as error:
                launch_error = "G4: cannot execute --agy-bin; supply an executable binary or wrapper."
                stderr.write(f"{launch_error} {error}\n".encode("utf-8"))
            stderr.flush()
            rc_file.write(f"{exit_code}\n")
            rc_file.flush()
            receipt = parse_stream(run_dir / "stream.jsonl", run_dir / "stderr.log", exit_code)
            if launch_error:
                receipt["status"] = "FAILED"
                print(launch_error, file=sys.stderr)
            receipt["run_dir"] = str(run_dir)
            serialized = json.dumps(receipt)
            receipt_file.write(serialized + "\n")
            receipt_file.flush()
            print(serialized, flush=True)
    except OSError as error:
        raise ValueError(
            "G3/G5: cannot create or save attempt evidence; fix TMPDIR permissions/free space."
        ) from error
    if isinstance(exit_code, int) and exit_code != 0:
        return exit_code if exit_code > 0 else 128 - exit_code
    return 0 if receipt["status"] == "SUCCESS" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--print-timeout", required=True)
    parser.add_argument("--label", default="attempt")
    parser.add_argument("--agy-bin", default="agy")
    parser.add_argument("launcher_args", nargs=argparse.REMAINDER, help="agy options after --, forwarded unchanged")
    args = parser.parse_args()
    try:
        return run(args)
    except (ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
