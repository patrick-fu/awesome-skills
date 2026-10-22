#!/usr/bin/env python3
"""Replay launch and evidence contracts without invoking a real model."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
import argparse
from contextlib import redirect_stdout
import importlib.util
import io
from unittest.mock import patch


SKILL = Path(__file__).resolve().parents[1]
SCRIPT = Path(os.environ.get("CLAUDE_RUN_SCRIPT", SKILL / "scripts" / "claude_run.py"))
FIXTURE = SKILL / "evals" / "fixtures" / "read.jsonl"


class Harness:
    def __init__(self, root):
        self.root = root
        self.home = root / "home"
        self.cwd = self.home / "project with spaces"
        self.cwd.mkdir(parents=True)
        self.temp = root / "captures"
        self.temp.mkdir()
        self.prompt = root / "task.txt"
        self.prompt.write_text("Read only target.txt.\nReply with its marker.\n")
        self.stub = root / "opaque wrapper"
        shutil.copyfile(SKILL / "evals" / "stub_claude.py", self.stub)
        self.stub.chmod(0o700)
        self.observed = root / "observed.jsonl"
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("STUB_")}
        self.env.update(HOME=str(self.home), TMPDIR=str(self.temp), STUB_OBSERVED=str(self.observed),
                        STUB_STREAM=str(FIXTURE), PYTHONDONTWRITEBYTECODE="1")

    def command(self, cwd=None, prompt=None, extra=(), timeout="0"):
        return [sys.executable, str(SCRIPT), "run", "--launcher", str(self.stub),
                "--cwd", str(cwd or self.cwd), "--prompt-file", str(prompt or self.prompt),
                "--timeout-seconds", timeout, "--", *extra]

    def call(self, env=None, **options):
        return subprocess.run(self.command(**options), cwd=self.home, env=dict(self.env, **(env or {})),
                              capture_output=True, text=True, timeout=15)

    def events(self):
        return [json.loads(line) for line in self.observed.read_text().splitlines()] if self.observed.exists() else []

    def stream(self, events):
        path = self.root / "case.jsonl"
        path.write_text("".join(json.dumps(event) + "\n" for event in events))
        return {"STUB_STREAM": str(path)}


def receipt(result):
    lines = result.stdout.splitlines()
    directory = Path(json.loads(lines[0])["run_dir"])
    evidence = json.loads(lines[-1])
    assert json.loads((directory / "receipt.json").read_text()) == evidence
    assert (directory / "rc.txt").read_text().strip() == str(evidence["exit"])
    return directory, evidence


class RunChecks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="claude-check-")
        self.addCleanup(self.temporary.cleanup)
        self.harness = Harness(Path(self.temporary.name).resolve())
        self.events = [json.loads(line) for line in FIXTURE.read_text().splitlines()]

    def reject_before_spawn(self, **options):
        before = self.harness.events()
        home_before = sorted(str(path) for path in self.harness.home.rglob("*"))
        result = self.harness.call(**options)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(result.stderr)
        self.assertEqual(self.harness.events(), before)
        self.assertEqual(home_before, sorted(str(path) for path in self.harness.home.rglob("*")))
        self.assertFalse(result.stdout)

    def test_scope_prompt_and_protocol_reject_before_spawn(self):
        for cwd in (self.harness.root / "missing", "relative", self.harness.prompt,
                    self.harness.home, self.harness.root, Path("/")):
            with self.subTest(cwd=cwd):
                self.reject_before_spawn(cwd=cwd)
        alias = self.harness.root / "alias"
        alias.symlink_to(self.harness.home, target_is_directory=True)
        self.reject_before_spawn(cwd=alias)
        for content in (b"", b" \n\t", b"bad\0text", b"\xff"):
            self.harness.prompt.write_bytes(content)
            self.reject_before_spawn()
        self.reject_before_spawn(prompt=self.harness.root / "missing.txt")
        self.reject_before_spawn(prompt=self.harness.root)
        self.harness.prompt.write_text("valid task")
        for option in ("--output-format=text", "--input-format=stream-json", "--verbose", "-p", "--background", "--"):
            self.reject_before_spawn(extra=[option])
        self.reject_before_spawn(timeout="-1")

    def test_stdin_wrapper_arguments_and_effective_settings(self):
        extra = ["--model", "requested-alias", "--effort", "high", "--tools", "Read", "Grep", "Glob",
                 "--add-dir", "path with spaces", "--continue", "--resume", "chosen-session"]
        result = self.harness.call(extra=extra)
        self.assertEqual(result.returncode, 0, result.stderr)
        observed = self.harness.events()[0]
        self.assertEqual(observed["argv"], ["--print", "--output-format", "stream-json", "--verbose", *extra])
        self.assertEqual(observed["prompt"], self.harness.prompt.read_text())
        self.assertEqual(observed["cwd"], str(self.harness.cwd))
        self.assertEqual(observed["home"], str(self.harness.home))
        directory, evidence = receipt(result)
        self.assertEqual(evidence["model"], "deepseek-flash")
        self.assertEqual(evidence["permission_mode"], "bypassPermissions")
        self.assertEqual(evidence["tools"], ["Glob", "Grep", "Read"])
        self.assertEqual((evidence["tool_calls"], evidence["tool_results"], evidence["pending_tools"]), (1, 1, 0))
        self.assertEqual((directory / "answer.txt").read_text(), "probe-marker")

    def test_relative_path_selection_survives_child_cwd_change(self):
        original = (SKILL / "evals" / "stub_claude.py").read_text()
        for directory, marker in ((self.harness.home, "selected host wrapper"), (self.harness.cwd, "target wrapper")):
            wrapper = directory / "selected-wrapper"
            wrapper.write_text(original.replace('os.environ.get("STUB_STDERR", "")', repr(marker)))
            wrapper.chmod(0o700)
        command = self.harness.command()
        environment = dict(self.harness.env, PATH="." + os.pathsep + os.environ["PATH"])
        for launcher, expected in (("selected-wrapper", "selected host wrapper"),
                                   (str(self.harness.cwd / "selected-wrapper"), "target wrapper")):
            with self.subTest(launcher=launcher):
                command[command.index("--launcher") + 1] = launcher
                result = subprocess.run(command, cwd=self.harness.home, env=environment,
                                        capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)
                directory, evidence = receipt(result)
                self.assertEqual((directory / "stderr.log").read_text(), expected)
                self.assertEqual(self.harness.events()[-1]["cwd"], str(self.harness.cwd))
                self.assertEqual(evidence["status"], "COMPLETED")

    def test_attempts_and_child_exit_survive_shell_tail(self):
        first, _ = receipt(self.harness.call(env={"STUB_STDERR": "first evidence"}))
        second, _ = receipt(self.harness.call(env={"STUB_STDERR": "second evidence"}))
        self.assertNotEqual(first, second)
        self.assertEqual((first / "stderr.log").read_text(), "first evidence")
        result = self.harness.call(env={"STUB_EXIT": "7"})
        self.assertEqual(result.returncode, 7)
        _, evidence = receipt(result)
        self.assertEqual((evidence["exit"], evidence["status"]), (7, "FAILED"))
        outer = subprocess.run(["sh", "-c", '"$@"; printf "tail success\\n"', "outer", *self.harness.command()],
                               cwd=self.harness.home, env=dict(self.harness.env, STUB_EXIT="7"),
                               capture_output=True, text=True, timeout=15)
        self.assertEqual(outer.returncode, 0)
        directory = Path(json.loads(outer.stdout.splitlines()[0])["run_dir"])
        self.assertEqual(json.loads((directory / "receipt.json").read_text())["status"], "FAILED")
        self.assertEqual((directory / "rc.txt").read_text().strip(), "7")

    def test_permission_conflict_is_not_retried_or_downgraded(self):
        result = self.harness.call(extra=["--restricted"], env={"STUB_BYPASS": "1"})
        directory, evidence = receipt(result)
        self.assertEqual(evidence["status"], "FAILED")
        self.assertEqual(evidence["exit"], 1)
        self.assertIn("bypassPermissions not supported", (directory / "stderr.log").read_text())
        self.assertEqual(len(self.harness.events()), 1)
        self.assertIn("--restricted", self.harness.events()[0]["argv"])

    def test_deadline_and_signal_keep_actual_exit(self):
        result = self.harness.call(timeout="1", env={"STUB_SLEEP": "30"})
        _, evidence = receipt(result)
        self.assertEqual(evidence["stopped"], "DEADLINE")
        self.assertEqual(evidence["status"], "FAILED")
        if os.name == "posix":
            self.assertEqual(evidence["exit"], -15)
            self.assertEqual(result.returncode, 143)
        _, evidence = receipt(self.harness.call(env={"STUB_SIGNAL": "1"}))
        self.assertEqual(evidence["status"], "FAILED")

    def test_inspect_does_not_call_an_unfinalized_capture_running(self):
        directory = self.harness.root / "unfinalized"
        directory.mkdir()
        shutil.copyfile(FIXTURE, directory / "stream.jsonl")
        result = subprocess.run([sys.executable, str(SCRIPT), "inspect", str(directory)],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0)
        evidence = json.loads(result.stdout)
        self.assertEqual((evidence["status"], evidence["exit"]), ("UNFINALIZED", "UNKNOWN"))

    @unittest.skipUnless(os.name == "posix", "POSIX signal forwarding")
    def test_host_cancellation_is_not_success(self):
        child = subprocess.Popen(self.harness.command(), cwd=self.harness.home,
                                 env=dict(self.harness.env, STUB_SLEEP="30"),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            deadline = time.monotonic() + 5
            while not self.harness.observed.exists() and time.monotonic() < deadline:
                time.sleep(0.01)
            self.assertTrue(self.harness.observed.exists())
            child.send_signal(signal.SIGTERM)
            stdout, stderr = child.communicate(timeout=10)
            _, evidence = receipt(subprocess.CompletedProcess([], child.returncode, stdout, stderr))
            self.assertEqual((evidence["status"], evidence["stopped"], evidence["exit"]), ("FAILED", "SIGTERM", -15))
        finally:
            if child.poll() is None:
                child.kill()
                child.communicate()

    @unittest.skipUnless(os.name == "posix", "POSIX process-group ownership")
    def test_cancel_workers_without_touching_another_attempt(self):
        worker = self.harness.root / "worker"
        release = self.harness.root / "release"
        other = Harness(self.harness.root / "other")
        children = []

        def active(pid):
            result = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True)
            return bool(result.stdout.strip()) and not result.stdout.strip().startswith("Z")

        try:
            for harness, environment in (
                (self.harness, dict(STUB_WORKER=str(worker), STUB_TERM="zero", STUB_EARLY_STREAM="1", STUB_SLEEP="30")),
                (other, dict(STUB_RELEASE=str(release), STUB_EARLY_STREAM="1", STUB_STDERR="other preserved")),
            ):
                child = subprocess.Popen(harness.command(), env=dict(harness.env, **environment),
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                directory = Path(json.loads(child.stdout.readline())["run_dir"])
                children.append((child, directory))
            deadline = time.monotonic() + 5
            while not (worker.exists() and all((directory / "stream.jsonl").stat().st_size for _, directory in children)):
                self.assertLess(time.monotonic(), deadline)
                time.sleep(0.01)
            child, directory = children[0]
            second, second_dir = children[1]
            child.send_signal(signal.SIGTERM)
            child.communicate(timeout=10)
            evidence = json.loads((directory / "receipt.json").read_text())
            self.assertNotEqual(child.returncode, 0)
            self.assertEqual((evidence["status"], evidence["stopped"], evidence["exit"]), ("FAILED", "SIGTERM", 0))
            self.assertEqual((directory / "rc.txt").read_text().strip(), "0")
            worker_pid = int(Path(str(worker) + ".pid").read_text())
            deadline = time.monotonic() + 5
            while active(worker_pid):
                self.assertLess(time.monotonic(), deadline)
                time.sleep(0.01)
            self.assertIsNone(second.poll())
            release.touch()
            second.communicate(timeout=5)
            self.assertEqual(second.returncode, 0)
            self.assertEqual(json.loads((second_dir / "receipt.json").read_text())["status"], "COMPLETED")
            self.assertEqual((second_dir / "stderr.log").read_text(), "other preserved")
            self.assertEqual((directory / "answer.txt").read_text(), "probe-marker")
        finally:
            for child, _ in children:
                if child.poll() is None:
                    child.send_signal(signal.SIGTERM)
                    try:
                        child.communicate(timeout=10)
                    except subprocess.TimeoutExpired:
                        child.kill()
                        child.communicate()
            if Path(str(worker) + ".pid").exists():
                worker_pid = int(Path(str(worker) + ".pid").read_text())
                if active(worker_pid):
                    os.kill(worker_pid, signal.SIGKILL)

    @unittest.skipUnless(os.name == "posix", "POSIX late signal")
    def test_late_signal_preserves_observed_exit(self):
        spec = importlib.util.spec_from_file_location("claude_cancel_check", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        original_wait = subprocess.Popen.wait

        def wait_then_signal(child, *args, **kwargs):
            result = original_wait(child, *args, **kwargs)
            os.kill(os.getpid(), signal.SIGTERM)
            return result

        arguments = argparse.Namespace(cwd=str(self.harness.cwd), prompt_file=str(self.harness.prompt),
                                       launcher=str(self.harness.stub), timeout_seconds=0, launcher_args=[])
        output = io.StringIO()
        with patch.dict(os.environ, self.harness.env, clear=True), patch.object(subprocess.Popen, "wait", wait_then_signal), redirect_stdout(output):
            self.assertEqual(module.run(arguments), 0)
        _, evidence = receipt(subprocess.CompletedProcess([], 0, output.getvalue()))
        self.assertEqual(evidence["status"], "COMPLETED")
        self.assertIsNone(evidence["stopped"])

    @unittest.skipUnless(os.name == "posix", "POSIX startup/finalization signals")
    def test_startup_and_finalization_signals(self):
        spec = importlib.util.spec_from_file_location("claude_signal_windows", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        original_spawn, original_parse = subprocess.Popen, module.summarize
        for phase in ("spawn", "finalize"):
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
                else (module, "summarize", parse_then_signal)
            )
            arguments = argparse.Namespace(cwd=str(self.harness.cwd), prompt_file=str(self.harness.prompt),
                                           launcher=str(self.harness.stub), timeout_seconds=0, launcher_args=[])
            environment = dict(self.harness.env, **({"STUB_SLEEP": "30"} if phase == "spawn" else {}))
            output = io.StringIO()
            previous = signal.getsignal(signal.SIGTERM)
            with self.subTest(phase=phase), patch.dict(os.environ, environment, clear=True), patch.object(target, attribute, replacement), redirect_stdout(output):
                exit_code = module.run(arguments)
            _, evidence = receipt(subprocess.CompletedProcess([], exit_code, output.getvalue()))
            self.assertEqual(signal.getsignal(signal.SIGTERM), previous)
            if phase == "spawn":
                self.assertNotEqual(exit_code, 0)
                self.assertEqual((evidence["status"], evidence["stopped"]), ("FAILED", "SIGTERM"))
                self.assertIsNotNone(spawned[0].poll())
            else:
                self.assertEqual(exit_code, 0)
                self.assertEqual(evidence["status"], "COMPLETED")
                self.assertIsNone(evidence["stopped"])

    @unittest.skipUnless(os.name == "posix", "POSIX termination permission")
    def test_failed_termination_cannot_publish_a_final_receipt(self):
        spec = importlib.util.spec_from_file_location("claude_stop_error", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        original_spawn, original_killpg = subprocess.Popen, os.killpg
        spawned = []

        def cancel_during_spawn(*args, **kwargs):
            child = original_spawn(*args, **kwargs)
            spawned.append(child)
            os.kill(os.getpid(), signal.SIGTERM)
            return child

        arguments = argparse.Namespace(cwd=str(self.harness.cwd), prompt_file=str(self.harness.prompt),
                                       launcher=str(self.harness.stub), timeout_seconds=0, launcher_args=[])
        output = io.StringIO()
        try:
            with patch.dict(os.environ, dict(self.harness.env, STUB_SLEEP="30"), clear=True), patch.object(subprocess, "Popen", cancel_during_spawn), patch.object(os, "killpg", side_effect=PermissionError("termination denied")), redirect_stdout(output):
                with self.assertRaisesRegex(ValueError, "UNFINALIZED") as raised:
                    module.run(arguments)
            self.assertIn(str(spawned[0].pid), str(raised.exception))
            directory = Path(json.loads(output.getvalue().splitlines()[0])["run_dir"])
            self.assertFalse((directory / "receipt.json").exists())
            self.assertEqual((directory / "rc.txt").read_text(), "")
            self.assertIsNone(spawned[0].poll())
        finally:
            for child in spawned:
                if child.poll() is None:
                    original_killpg(child.pid, signal.SIGKILL)
                    child.wait(timeout=5)

    def test_stream_negative_and_positive_controls(self):
        cases = []
        def add(name, events, status, fields=None):
            cases.append((name, events, status, fields or {}))
        add("normal", self.events, "COMPLETED")
        add("unknown-event", [*self.events[:1], {"type": "future"}, *self.events[1:]], "COMPLETED")
        add("no-terminal", self.events[:-1], "INCOMPLETE")
        add("pending-tool", [*self.events[:2], self.events[-1]], "INCOMPLETE", {"pending_tools": 1})
        add("orphan-result", [self.events[0], *self.events[2:]], "INCOMPLETE", {"orphan_results": 1})
        add("duplicate-terminal", [*self.events, self.events[-1]], "INCOMPLETE")
        add("is-error", [*self.events[:-1], dict(self.events[-1], is_error=True)], "FAILED")
        add("error-subtype", [*self.events[:-1], dict(self.events[-1], subtype="error_max_turns")], "FAILED")
        add("missing-is-error", [*self.events[:-1], {"type": "result", "subtype": "success", "result": "ok"}], "INCOMPLETE")
        add("empty-answer", [*self.events[:-1], dict(self.events[-1], result="")], "INCOMPLETE")
        add("structured-answer", [*self.events[:-1], dict(self.events[-1], result="", structured_output={"ok": True})],
            "COMPLETED", {"answer_format": "json"})
        add("nested-terminal", [*self.events[:1], dict(self.events[-1], parent_tool_use_id="agent-1"), *self.events[1:]], "COMPLETED")
        add("denial-evidence", [*self.events[:-1], dict(self.events[-1], permission_denials=[{"tool_name": "Bash"}])],
            "COMPLETED", {"permission_denials": 1})
        add("invalid-unicode", [*self.events[:-1], dict(self.events[-1], result="\ud800")], "INCOMPLETE")
        init = dict(self.events[0])
        del init["model"]
        add("optional-model", [init, *self.events[1:]], "COMPLETED", {"model": "UNKNOWN"})
        error_result = {"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": "read-1", "is_error": True, "content": "missing"}]}}
        add("tool-error-evidence", [*self.events[:2], error_result, self.events[-1]], "COMPLETED", {"tool_errors": 1})
        add("conflicting-result", [*self.events[:3], error_result, self.events[-1]], "INCOMPLETE", {"tool_errors": 1})
        for name, events, status, fields in cases:
            with self.subTest(name=name):
                result = self.harness.call(env=self.harness.stream(events))
                directory, evidence = receipt(result)
                self.assertEqual(evidence["status"], status)
                self.assertEqual(result.returncode == 0, status == "COMPLETED")
                for field, expected in fields.items():
                    self.assertEqual(evidence[field], expected)
                self.assertEqual((directory / "stream.jsonl").read_bytes(), (self.harness.root / "case.jsonl").read_bytes())
        path = self.harness.root / "partial.jsonl"
        path.write_bytes(FIXTURE.read_bytes() + b'{"type":')
        _, evidence = receipt(self.harness.call(env={"STUB_STREAM": str(path)}))
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertTrue(evidence["incomplete_final_line"])
        path.write_bytes(FIXTURE.read_bytes().rstrip(b"\n"))
        _, evidence = receipt(self.harness.call(env={"STUB_STREAM": str(path)}))
        self.assertEqual(evidence["status"], "COMPLETED")
        self.assertTrue(evidence["incomplete_final_line"])
        _, evidence = receipt(self.harness.call(env={"STUB_STDERR": "Warning: model alias changed"}))
        self.assertEqual(evidence["status"], "COMPLETED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
