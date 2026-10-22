#!/usr/bin/env python3
"""Check cancellation ownership with real offline parent/worker processes."""

import argparse
from contextlib import redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import time
from unittest.mock import patch

from check_launch_guards import Harness, SCRIPT, receipt_from


def wait_for(predicate):
    deadline = time.monotonic() + 5
    while not predicate():
        assert time.monotonic() < deadline, "Offline process did not reach the checkpoint"
        time.sleep(0.01)


def active(pid):
    result = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True)
    return bool(result.stdout.strip()) and not result.stdout.strip().startswith("Z")


def main():
    if os.name != "posix":
        print("SKIP process-group controls: POSIX required")
        return 0
    with tempfile.TemporaryDirectory(prefix="agy-cancel-") as temporary:
        root = Path(temporary).resolve()
        for behavior in ("zero", "ignore"):
            first, second = Harness(root / behavior / "first"), Harness(root / behavior / "second")
            worker = root / behavior / "worker"
            release = root / behavior / "release"
            children = []
            try:
                for harness, environment in (
                    (first, dict(STUB_WORKER=str(worker), STUB_TERM=behavior, STUB_SLEEP="30")),
                    (second, dict(STUB_RELEASE=str(release), STUB_STDERR="second preserved")),
                ):
                    child = subprocess.Popen(harness.command(), env=dict(harness.env, **environment),
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    directory = Path(json.loads(child.stdout.readline())["run_dir"])
                    children.append((child, directory))
                wait_for(lambda: worker.exists() and all((directory / "stream.jsonl").stat().st_size for _, directory in children))
                first_child, first_dir = children[0]
                second_child, second_dir = children[1]
                assert all(child.poll() is None for child, _ in children)
                assert not (first_dir / "receipt.json").exists()
                first_child.send_signal(signal.SIGTERM)
                first_child.communicate(timeout=12)
                evidence = json.loads((first_dir / "receipt.json").read_text())
                assert first_child.returncode != 0 and evidence["status"] == "FAILED", evidence
                assert evidence["stopped"] == "SIGTERM", evidence
                assert evidence["exit"] == (0 if behavior == "zero" else -9), evidence
                assert int((first_dir / "rc.txt").read_text()) == evidence["exit"]
                wait_for(lambda: not active(int(Path(str(worker) + ".pid").read_text())))
                saved = worker.read_bytes()
                time.sleep(0.15)
                assert worker.read_bytes() == saved
                assert second_child.poll() is None
                release.touch()
                second_child.communicate(timeout=5)
                assert second_child.returncode == 0
                assert json.loads((second_dir / "receipt.json").read_text())["status"] == "SUCCESS"
                assert (second_dir / "stderr.log").read_text() == "second preserved"
                assert (first_dir / "answer.txt").read_text() == "完成"
                print(f"PASS cancel {behavior}: full result before exit cannot mask cancellation; worker stops, other attempt succeeds")
            finally:
                for child, _ in children:
                    if child.poll() is None:
                        child.send_signal(signal.SIGTERM)
                        try:
                            child.communicate(timeout=12)
                        except subprocess.TimeoutExpired:
                            child.kill()
                            child.communicate()
                if Path(str(worker) + ".pid").exists():
                    worker_pid = int(Path(str(worker) + ".pid").read_text())
                    if active(worker_pid):
                        os.kill(worker_pid, signal.SIGKILL)

        harness = Harness(root / "late-signal")
        spec = importlib.util.spec_from_file_location("agy_cancel_check", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        original_wait = subprocess.Popen.wait

        def wait_then_signal(child, *args, **kwargs):
            result = original_wait(child, *args, **kwargs)
            os.kill(os.getpid(), signal.SIGTERM)
            return result

        arguments = argparse.Namespace(cwd=str(harness.cwd), prompt_file=str(harness.prompt),
                                       print_timeout="0", label="late", agy_bin=str(harness.stub), launcher_args=[])
        output = io.StringIO()
        with patch.dict(os.environ, harness.env, clear=True), patch.object(subprocess.Popen, "wait", wait_then_signal), redirect_stdout(output):
            assert module.run(arguments) == 0
        _, evidence = receipt_from(subprocess.CompletedProcess([], 0, output.getvalue()))
        assert evidence["status"] == "SUCCESS" and evidence["stopped"] is None
        print("PASS late signal after observed child exit preserves success")

        for phase in ("spawn", "finalize"):
            harness = Harness(root / phase)
            original_spawn = subprocess.Popen
            original_parse = module.parse_stream
            spawned = []

            def spawn_then_signal(*args, **kwargs):
                child = original_spawn(*args, **kwargs)
                spawned.append(child)
                os.kill(os.getpid(), signal.SIGTERM)
                return child

            def parse_then_signal(*args, **kwargs):
                os.kill(os.getpid(), signal.SIGTERM)
                return original_parse(*args, **kwargs)

            target, attribute, replacement = (
                (module.subprocess, "Popen", spawn_then_signal) if phase == "spawn"
                else (module, "parse_stream", parse_then_signal)
            )
            arguments.cwd, arguments.prompt_file, arguments.agy_bin = str(harness.cwd), str(harness.prompt), str(harness.stub)
            environment = dict(harness.env, **({"STUB_SLEEP": "30"} if phase == "spawn" else {}))
            output = io.StringIO()
            previous = signal.getsignal(signal.SIGTERM)
            with patch.dict(os.environ, environment, clear=True), patch.object(target, attribute, replacement), redirect_stdout(output):
                exit_code = module.run(arguments)
            _, evidence = receipt_from(subprocess.CompletedProcess([], exit_code, output.getvalue()))
            assert signal.getsignal(signal.SIGTERM) == previous
            if phase == "spawn":
                assert exit_code != 0 and evidence["stopped"] == "SIGTERM" and evidence["status"] == "FAILED"
                assert spawned[0].poll() is not None
            else:
                assert exit_code == 0 and evidence["stopped"] is None and evidence["status"] == "SUCCESS"
            print(f"PASS {phase} signal: startup is owned, finalized evidence survives late cancellation")

        harness = Harness(root / "termination-denied")
        spawned = []
        original_spawn, original_killpg = subprocess.Popen, os.killpg

        def cancel_during_spawn(*args, **kwargs):
            child = original_spawn(*args, **kwargs)
            spawned.append(child)
            os.kill(os.getpid(), signal.SIGTERM)
            return child

        arguments.cwd, arguments.prompt_file, arguments.agy_bin = str(harness.cwd), str(harness.prompt), str(harness.stub)
        output = io.StringIO()
        try:
            with patch.dict(os.environ, dict(harness.env, STUB_SLEEP="30"), clear=True), patch.object(subprocess, "Popen", cancel_during_spawn), patch.object(os, "killpg", side_effect=PermissionError("termination denied")), redirect_stdout(output):
                try:
                    module.run(arguments)
                except ValueError as error:
                    assert "UNFINALIZED" in str(error) and str(spawned[0].pid) in str(error)
                else:
                    raise AssertionError("A failed stop cannot publish a final receipt")
            directory = Path(json.loads(output.getvalue().splitlines()[0])["run_dir"])
            assert not (directory / "receipt.json").exists()
            assert (directory / "rc.txt").read_text() == ""
            assert spawned[0].poll() is None
        finally:
            for child in spawned:
                if child.poll() is None:
                    original_killpg(child.pid, signal.SIGKILL)
                    child.wait(timeout=5)
        print("PASS termination denied: actionable owned PID, no false final receipt, explicit cleanup")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
