#!/usr/bin/env python3
"""Run one bounded CLI task or inspect its compact process evidence."""

from __future__ import annotations

import argparse
from contextlib import ExitStack
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time


UNKNOWN = "UNKNOWN"


def summarize(stream: Path, exit_code=UNKNOWN):
    evidence = dict(status="UNFINALIZED", exit=exit_code, model=UNKNOWN, cwd=UNKNOWN,
                    session_id=UNKNOWN, terminal=UNKNOWN, candidate_present=False, response_bytes=UNKNOWN,
                    tool_calls=0, tool_results=0, tool_errors=0, unknown_tool_results=0,
                    pending_tools=0, diagnostic_items=0, nonterminal_errors=0,
                    status_lines=0, malformed_lines=0, unknown_events=0, incomplete_final_line=False)
    calls, results = set(), set()
    terminal_count = thread_count = turn_count = 0
    failed = False
    answer = None
    tool_types = {"command_execution", "file_change", "mcp_tool_call", "web_search"}
    with stream.open("rb") as source:
        for line in source:
            evidence["incomplete_final_line"] = not line.endswith(b"\n")
            if line.rstrip(b"\r\n") == b"Reading additional input from stdin...":
                evidence["status_lines"] += 1
                continue
            try:
                event = json.loads(line)
                if not isinstance(event, dict):
                    raise ValueError("event is not an object")
            except (ValueError, UnicodeError):
                evidence["malformed_lines"] += 1
                continue
            kind = event.get("type")
            if kind == "thread.started":
                thread_count += 1
                value = event.get("thread_id")
                if thread_count == 1 and isinstance(value, str) and value:
                    evidence["session_id"] = value
            elif kind == "turn.started":
                turn_count += 1
            elif kind in ("turn.completed", "turn.failed"):
                terminal_count += 1
                failed |= kind == "turn.failed"
                if terminal_count == 1:
                    evidence["terminal"] = kind
            elif kind == "error":
                evidence["nonterminal_errors"] += 1
            elif kind in ("item.started", "item.updated", "item.completed"):
                item = event.get("item")
                if not isinstance(item, dict):
                    evidence["malformed_lines"] += 1
                    continue
                item_type = item.get("type")
                if not isinstance(item_type, str):
                    evidence["malformed_lines"] += 1
                    continue
                if kind == "item.completed" and item_type == "agent_message" and isinstance(item.get("text"), str):
                    answer = item["text"]
                elif kind == "item.completed" and item_type == "error":
                    evidence["diagnostic_items"] += 1
                elif item_type in tool_types and kind != "item.updated":
                    identifier = item.get("id")
                    if not isinstance(identifier, str) or not identifier:
                        evidence["malformed_lines"] += 1
                        continue
                    if kind == "item.started":
                        if identifier in calls:
                            evidence["malformed_lines"] += 1
                        calls.add(identifier)
                    else:
                        if identifier in results:
                            evidence["malformed_lines"] += 1
                        results.add(identifier)
                        state = item.get("status")
                        if state in ("failed", "declined") or (type(item.get("exit_code")) is int and item["exit_code"] != 0):
                            evidence["tool_errors"] += 1
                        elif state != "completed":
                            evidence["unknown_tool_results"] += 1
            else:
                evidence["unknown_events"] += 1
    evidence.update(tool_calls=len(calls), tool_results=len(results), pending_tools=len(calls - results))
    if answer is not None:
        try:
            evidence["response_bytes"] = len(answer.encode("utf-8"))
        except UnicodeError:
            evidence["malformed_lines"] += 1
            answer = None
    evidence["candidate_present"] = answer is not None
    if isinstance(exit_code, int):
        if exit_code != 0 or failed:
            evidence["status"] = "FAILED"
        elif (terminal_count != 1 or thread_count > 1 or turn_count > 1
              or evidence["malformed_lines"] or evidence["pending_tools"]):
            evidence["status"] = "INCOMPLETE"
        else:
            evidence["status"] = "COMPLETED"
    return evidence, answer


def prepare(args):
    cwd = Path(args.cwd)
    if not cwd.is_absolute() or not cwd.is_dir():
        raise ValueError("Scope: --cwd must be an absolute, existing project directory.")
    cwd = cwd.resolve()
    home = Path.home().resolve()
    if cwd == home or cwd in home.parents:
        raise ValueError("Scope: choose a project directory, not HOME or its ancestor.")
    prompt_path = Path(args.prompt_file)
    if not prompt_path.is_file():
        raise ValueError("Prompt: --prompt-file must name a regular UTF-8 task file.")
    prompt = prompt_path.read_bytes()
    if not prompt.decode("utf-8").strip() or b"\0" in prompt:
        raise ValueError("Prompt: supply nonempty UTF-8 task text without NUL bytes.")
    if args.timeout_seconds < 0:
        raise ValueError("Deadline: --timeout-seconds must be a nonnegative integer; 0 means unbounded.")
    launcher = args.launcher
    if os.sep in launcher and not Path(launcher).is_absolute():
        raise ValueError("Launcher: use an absolute wrapper path or an executable name on PATH.")
    executable = shutil.which(launcher)
    if not executable:
        raise ValueError("Launcher: --launcher must name the selected executable binary or wrapper.")
    executable = os.path.abspath(executable)
    forwarded = args.launcher_args
    if forwarded[:1] == ["--"]:
        forwarded = forwarded[1:]
    owned = {"--json", "--cd", "-C"}
    for argument in forwarded:
        option = argument.split("=", 1)[0]
        if argument == "--" or option in owned or (argument.startswith("-C") and not argument.startswith("--")):
            raise ValueError("Protocol: codex_run.py owns cwd, prompt and stream flags; remove the duplicate transport option.")
    return cwd, prompt, [executable, "exec", "--json", "--cd", str(cwd), *forwarded, "-"]


def run(args):
    cwd, prompt, command = prepare(args)
    temp_root = Path(os.environ.get("TMPDIR") or tempfile.gettempdir())
    if not temp_root.is_absolute() or not temp_root.is_dir():
        raise ValueError("Capture: set TMPDIR to an absolute, writable existing directory.")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    attempt = Path(tempfile.mkdtemp(prefix=f"codex-{timestamp}-{os.getpid()}-", dir=temp_root))
    with ExitStack() as lifecycle:
        return run_attempt(args, cwd, prompt, command, attempt, lifecycle)


def run_attempt(args, cwd, prompt, command, attempt, lifecycle):
    exit_code = UNKNOWN
    stopped = None
    launch_error = None
    child = None
    pending_signal = None

    def interrupted(signum, frame):
        nonlocal pending_signal
        if child is None or child.returncode is None:
            pending_signal = signal.Signals(signum).name

    for signum in (signal.SIGINT, signal.SIGTERM):
        previous = signal.signal(signum, interrupted)
        lifecycle.callback(signal.signal, signum, previous)
    with ExitStack() as files:
        stdout = files.enter_context((attempt / "stream.jsonl").open("xb"))
        stderr = files.enter_context((attempt / "stderr.log").open("xb"))
        rc_file = files.enter_context((attempt / "rc.txt").open("x", encoding="utf-8"))
        receipt_file = files.enter_context((attempt / "receipt.pending").open("x", encoding="utf-8"))
        answer_file = files.enter_context((attempt / "answer.txt").open("x", encoding="utf-8"))
        stdin = files.enter_context(tempfile.TemporaryFile())
        stdin.write(prompt)
        stdin.seek(0)
        print(json.dumps({"run_dir": str(attempt)}), flush=True)
        try:
            deadline = time.monotonic() + args.timeout_seconds if args.timeout_seconds else None
            child = subprocess.Popen(command, cwd=cwd, stdin=stdin, stdout=stdout,
                                     stderr=stderr, start_new_session=(os.name == "posix"))
            while True:
                if pending_signal or (deadline is not None and time.monotonic() >= deadline):
                    stopped = pending_signal or "DEADLINE"
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
                    f"Process: cannot stop or reap this attempt's owned PID {child.pid}; keep its host handle, resolve the "
                    "process permission/state and confirm exit before releasing the workspace. "
                    "Evidence remains UNFINALIZED; do not broaden permissions automatically."
                ) from error
            launch_error = f"Launcher: cannot execute the selected wrapper; check its path/interpreter ({error})."
            stderr.write((launch_error + "\n").encode())
        stderr.flush()
        rc_file.write(f"{exit_code}\n")
        rc_file.flush()
        evidence, answer = summarize(attempt / "stream.jsonl", exit_code)
        if stopped or launch_error:
            evidence["status"] = "FAILED"
        evidence.update(run_dir=str(attempt), requested_cwd=str(cwd), stopped=stopped,
                        launch_error=launch_error, answer_file=str(attempt / "answer.txt"))
        if answer is not None:
            answer_file.write(answer)
        receipt_file.write(json.dumps(evidence) + "\n")
    (attempt / "receipt.pending").replace(attempt / "receipt.json")
    print(json.dumps(evidence), flush=True)
    if launch_error:
        print(launch_error, file=sys.stderr)
    if isinstance(exit_code, int) and exit_code != 0:
        return exit_code if exit_code > 0 else 128 - exit_code
    return 0 if evidence["status"] == "COMPLETED" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    modes = parser.add_subparsers(dest="mode", required=True)
    launch = modes.add_parser("run", allow_abbrev=False)
    launch.add_argument("--launcher", required=True)
    launch.add_argument("--cwd", required=True)
    launch.add_argument("--prompt-file", required=True)
    launch.add_argument("--timeout-seconds", type=int, required=True, help="Host deadline; 0 means unbounded")
    launch.add_argument("launcher_args", nargs=argparse.REMAINDER, help="Other Codex exec options after --, forwarded unchanged")
    inspect = modes.add_parser("inspect", allow_abbrev=False)
    inspect.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    try:
        if args.mode == "run":
            return run(args)
        receipt = args.run_dir / "receipt.json"
        if receipt.exists() and receipt.stat().st_size:
            evidence = json.loads(receipt.read_text(encoding="utf-8"))
        else:
            evidence, _ = summarize(args.run_dir / "stream.jsonl")
            evidence["run_dir"] = str(args.run_dir)
        print(json.dumps(evidence))
        return 0
    except (OSError, ValueError, RuntimeError) as error:
        print(f"{error}\nCheck the named path/option and available temporary storage before another attempt.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
