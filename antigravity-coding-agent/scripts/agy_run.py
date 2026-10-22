#!/usr/bin/env python3
"""Launch one guarded Antigravity attempt and retain its process evidence."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
from contextlib import ExitStack
from datetime import datetime, timezone


UNKNOWN = "UNKNOWN"
DURATION = re.compile(r"(?:0|[0-9]+(?:\.[0-9]+)?(?:ns|us|µs|ms|s|m|h))")
TIMEOUT = re.compile(
    r"print[- ]timeout\b.*(?:reached|exceeded|expired|timed out)",
    re.IGNORECASE,
)


def parse_stream(stream_path: Path, stderr_path: Path, exit_code=UNKNOWN, answer_file=None) -> dict:
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
    answer = None
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
                    if "denied_actions" in payload and not isinstance(denied, list):
                        malformed = True
                    response = payload.get("response")
                    try:
                        receipt["response_bytes"] = (
                            len(response.encode("utf-8")) if isinstance(response, str) else UNKNOWN
                        )
                        if isinstance(response, str):
                            answer = response
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
        or receipt["response_bytes"] in (UNKNOWN, 0)
        or receipt["timeout_warning"] is not False
    ):
        receipt["status"] = "INCOMPLETE"
    else:
        receipt["status"] = "SUCCESS"
    if answer_file is not None and answer is not None:
        answer_file.write(answer)
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
    previous_handlers = {}
    try:
        run_dir = Path(tempfile.mkdtemp(
            prefix=f"agy-{args.label}-{timestamp}-{os.getpid()}-", dir=temp_root
        ))
        with ExitStack() as files:
            stream = files.enter_context((run_dir / "stream.jsonl").open("xb"))
            stderr = files.enter_context((run_dir / "stderr.log").open("xb"))
            rc_file = files.enter_context((run_dir / "rc.txt").open("x", encoding="utf-8"))
            receipt_file = files.enter_context((run_dir / "receipt.pending").open("x", encoding="utf-8"))
            answer_file = files.enter_context((run_dir / "answer.txt").open("x", encoding="utf-8"))
            print(json.dumps({"run_dir": str(run_dir)}), flush=True)
            exit_code = UNKNOWN
            launch_error = None
            stopped = None
            pending_signal = None
            child = None

            def forward_signal(signum, frame):
                nonlocal pending_signal
                if child is None or child.returncode is None:
                    pending_signal = signal.Signals(signum).name

            for signum in (signal.SIGINT, signal.SIGTERM):
                previous_handlers[signum] = signal.signal(signum, forward_signal)
            try:
                executable = shutil.which(args.agy_bin)
                if not executable:
                    raise FileNotFoundError(args.agy_bin)
                child = subprocess.Popen(
                    [os.path.abspath(executable), *forwarded, "--output-format", "stream-json",
                     "--print-timeout", args.print_timeout, "-p", prompt],
                    cwd=cwd, stdin=subprocess.DEVNULL, stdout=stream, stderr=stderr,
                    start_new_session=(os.name == "posix"),
                )
                while True:
                    if pending_signal:
                        stopped = pending_signal
                        try:
                            if os.name == "posix":
                                os.killpg(child.pid, signal.SIGTERM)
                            else:
                                child.terminate()
                        except ProcessLookupError:
                            pass
                        try:
                            exit_code = child.wait(timeout=5)
                        except subprocess.TimeoutExpired:
                            if os.name == "posix":
                                try:
                                    os.killpg(child.pid, signal.SIGKILL)
                                except ProcessLookupError:
                                    pass
                            else:
                                child.kill()
                            exit_code = child.wait()
                        if os.name == "posix":
                            try:
                                os.killpg(child.pid, signal.SIGKILL)
                            except ProcessLookupError:
                                pass
                        break
                    try:
                        exit_code = child.wait(timeout=0.1)
                        if not pending_signal:
                            break
                    except subprocess.TimeoutExpired:
                        pass
            except OSError as error:
                if child is not None:
                    raise ValueError(
                        f"G4: cannot stop or reap this attempt's owned PID {child.pid}; keep its host handle, "
                        "resolve the process permission/state and confirm exit before releasing the workspace. "
                        "Evidence remains UNFINALIZED; do not broaden permissions automatically."
                    ) from error
                launch_error = "G4: cannot execute --agy-bin; supply an executable binary or wrapper."
                stderr.write(f"{launch_error} {error}\n".encode("utf-8"))
            stderr.flush()
            rc_file.write(f"{exit_code}\n")
            rc_file.flush()
            receipt = parse_stream(run_dir / "stream.jsonl", run_dir / "stderr.log", exit_code, answer_file)
            receipt["stopped"] = stopped
            if stopped:
                receipt["status"] = "FAILED"
            if launch_error:
                receipt["status"] = "FAILED"
                print(launch_error, file=sys.stderr)
            receipt["run_dir"] = str(run_dir)
            receipt["answer_file"] = str(run_dir / "answer.txt")
            serialized = json.dumps(receipt)
            receipt_file.write(serialized + "\n")
            receipt_file.flush()
        (run_dir / "receipt.pending").replace(run_dir / "receipt.json")
        print(serialized, flush=True)
    except OSError as error:
        raise ValueError(
            "G3/G5: cannot create or save attempt evidence; fix TMPDIR permissions/free space."
        ) from error
    finally:
        for signum, handler in previous_handlers.items():
            signal.signal(signum, handler)
    if isinstance(exit_code, int) and exit_code != 0:
        return exit_code if exit_code > 0 else 128 - exit_code
    return 0 if receipt["status"] == "SUCCESS" else 1


def inspect_attempt(argv) -> int:
    parser = argparse.ArgumentParser(description="Inspect evidence without claiming an unfinished process has exited.")
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args(argv)
    directory = args.run_dir
    try:
        if not directory.is_dir() or not (directory / "stream.jsonl").is_file() or not (directory / "stderr.log").is_file():
            raise ValueError("use an existing attempt directory containing stream.jsonl and stderr.log")
        final = directory / "receipt.json"
        if final.is_file() and final.stat().st_size:
            receipt = json.loads(final.read_text(encoding="utf-8"))
        else:
            receipt = parse_stream(directory / "stream.jsonl", directory / "stderr.log")
            receipt.update(status="UNFINALIZED", run_dir=str(directory))
        print(json.dumps(receipt))
        return 0
    except (OSError, ValueError) as error:
        print(f"Inspect: {error}. Check the capture path and retained host handle.", file=sys.stderr)
        return 2


def main() -> int:
    if sys.argv[1:2] == ["inspect"]:
        return inspect_attempt(sys.argv[2:])
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False,
                                     epilog="Inspect a live or finished attempt: agy_run.py inspect RUN_DIR")
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
