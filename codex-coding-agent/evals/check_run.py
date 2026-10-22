#!/usr/bin/env python3
"""Observe launcher behavior with a local stub; never invoke a real model."""

from __future__ import annotations

import argparse
from contextlib import redirect_stdout
import importlib.util
import io
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
from unittest.mock import patch


SKILL = Path(__file__).resolve().parents[1]
CLI = "codex"
SCRIPT = Path(os.environ.get("CODEX_RUN_SCRIPT", SKILL / "scripts" / "codex_run.py"))
FIXTURE = SKILL / "evals" / "fixtures" / "read.jsonl"
EXPECTED = "fixture-marker|56"


class Harness:
    def __init__(self, root):
        self.root = root
        self.home = root / "home"
        self.cwd = self.home / "project with spaces"
        self.cwd.mkdir(parents=True)
        self.temp = root / "captures"
        self.temp.mkdir()
        self.prompt = root / "task.txt"
        self.prompt.write_text("Read a real file.\nKeep $(printf injection) and `text` literal.\n")
        self.stub = root / "opaque wrapper"
        shutil.copyfile(SKILL / "evals" / "stub_cli.py", self.stub)
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
                              capture_output=True, text=True, timeout=20)

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
        self.temporary = tempfile.TemporaryDirectory(prefix=CLI + "-check-")
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
        self.reject_before_spawn(prompt=self.harness.root / "absent")
        self.reject_before_spawn(prompt=self.harness.root)
        self.harness.prompt.write_text("valid task")
        for option in ("--json", "--cd=/elsewhere", "-C/elsewhere", "--"):
            self.reject_before_spawn(extra=[option])
        self.reject_before_spawn(timeout="-1")

    def test_transport_arguments_and_optional_metadata(self):
        extra = ["--model", "requested-alias", "-p", "named-profile", "--sandbox", "read-only", "-c", 'approval_policy="never"']
        result = self.harness.call(extra=extra)
        self.assertEqual(result.returncode, 0, result.stderr)
        observed = self.harness.events()[0]
        directory, evidence = receipt(result)
        self.assertEqual(observed["cwd"], str(self.harness.cwd))
        self.assertEqual(observed["home"], str(self.harness.home))
        self.assertEqual(observed["prompt"], self.harness.prompt.read_text())
        self.assertEqual(observed["argv"], ["exec", "--json", "--cd", str(self.harness.cwd), *extra, "-"])
        self.assertEqual(evidence["requested_cwd"], str(self.harness.cwd))
        self.assertEqual((directory / "answer.txt").read_text(), EXPECTED)
        self.assertEqual(evidence["status"], "COMPLETED")
        self.assertTrue(evidence["candidate_present"])
        self.assertEqual(evidence["model"], "UNKNOWN")
        self.assertEqual(evidence["cwd"], "UNKNOWN")
        self.assertEqual(evidence["diagnostic_items"], 2)
        self.assertGreater(evidence["tool_results"], 0)
        self.assertNotIn("aggregated_output", evidence)
        self.assertNotIn(EXPECTED, result.stdout)


    def test_relative_path_selection_survives_child_cwd_change(self):
        original = (SKILL / "evals" / "stub_cli.py").read_text()
        for directory, marker in ((self.harness.home, "selected host wrapper"), (self.harness.cwd, "target wrapper")):
            wrapper = directory / "selected-wrapper"
            wrapper.write_text(original.replace('sys.stderr.write(os.environ.get("STUB_STDERR", ""))',
                                                "sys.stderr.write(" + repr(marker) + ")"))
            wrapper.chmod(0o700)
        command = self.harness.command()
        command[command.index("--launcher") + 1] = "selected-wrapper"
        environment = dict(self.harness.env, PATH="." + os.pathsep + os.environ["PATH"])
        result = subprocess.run(command, cwd=self.harness.home, env=environment,
                                capture_output=True, text=True, timeout=15)
        directory, evidence = receipt(result)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((directory / "stderr.log").read_text(), "selected host wrapper")
        self.assertEqual(self.harness.events()[-1]["cwd"], str(self.harness.cwd))
        command[command.index("--launcher") + 1] = str(self.harness.cwd / "selected-wrapper")
        result = subprocess.run(command, cwd=self.harness.home, env=environment,
                                capture_output=True, text=True, timeout=15)
        directory, _ = receipt(result)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((directory / "stderr.log").read_text(), "target wrapper")
    def test_unique_capture_and_real_child_exit(self):
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

    def test_deadline_and_unfinalized_inspection(self):
        result = self.harness.call(timeout="1", env={"STUB_SLEEP": "30"})
        _, evidence = receipt(result)
        self.assertEqual((evidence["stopped"], evidence["status"]), ("DEADLINE", "FAILED"))
        if os.name == "posix":
            self.assertEqual(evidence["exit"], -15)
            self.assertEqual(result.returncode, 143)
        directory = self.harness.root / "unfinalized"
        directory.mkdir()
        shutil.copyfile(FIXTURE, directory / "stream.jsonl")
        result = subprocess.run([sys.executable, str(SCRIPT), "inspect", str(directory)],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0)
        evidence = json.loads(result.stdout)
        self.assertEqual((evidence["status"], evidence["exit"]), ("UNFINALIZED", "UNKNOWN"))

    def test_stream_positive_and_negative_controls(self):
        cases = [
            ("normal", self.events, "COMPLETED"),
            ("unknown-event", [*self.events[:1], {"type": "future"}, *self.events[1:]], "COMPLETED"),
            ("no-terminal", self.events[:-1], "INCOMPLETE"),
            ("duplicate-terminal", [*self.events, self.events[-1]], "INCOMPLETE"),
        ]
        cases.extend([
            ("no-init", [event for event in self.events if event.get("type") != "thread.started"], "COMPLETED"),
            ("pending-tool", [event for event in self.events if not (event.get("type") == "item.completed" and event.get("item", {}).get("type") == "command_execution")], "INCOMPLETE"),
            ("completed-only-tool", [event for event in self.events if event.get("type") != "item.started"], "COMPLETED"),
            ("failed-terminal", [*self.events[:-1], {"type": "turn.failed", "error": {"message": "failed"}}], "FAILED"),
            ("missing-candidate", [event for event in self.events if event.get("item", {}).get("type") != "agent_message"], "COMPLETED"),
        ])
        empty = json.loads(json.dumps(self.events))
        [event for event in empty if event.get("item", {}).get("type") == "agent_message"][-1]["item"]["text"] = ""
        cases.append(("empty-answer", empty, "COMPLETED"))
        error = json.loads(json.dumps(self.events))
        tool = [event["item"] for event in error if event.get("type") == "item.completed" and event.get("item", {}).get("type") == "command_execution"][0]
        tool.update(status="failed", exit_code=1)
        cases.append(("tool-error", error, "COMPLETED"))
        cases.append(("recoverable-error", [*self.events[:-1], {"type": "error", "message": "recovered"}, self.events[-1]], "COMPLETED"))
        for name, events, status in cases:
            with self.subTest(name=name):
                result = self.harness.call(env=self.harness.stream(events))
                directory, evidence = receipt(result)
                self.assertEqual(evidence["status"], status, evidence)
                self.assertEqual(result.returncode == 0, status == "COMPLETED")
                if name == "tool-error":
                    self.assertEqual(evidence["tool_errors"], 1)
                self.assertEqual((directory / "stream.jsonl").read_bytes(),
                                 (self.harness.root / "case.jsonl").read_bytes())
                if name == "missing-candidate":
                    self.assertFalse(evidence["candidate_present"])
                    self.assertEqual(evidence["response_bytes"], "UNKNOWN")
                if name == "empty-answer":
                    self.assertTrue(evidence["candidate_present"])
                    self.assertEqual(evidence["response_bytes"], 0)
        path = self.harness.root / "partial.jsonl"
        path.write_bytes(FIXTURE.read_bytes() + b'{"type":')
        _, evidence = receipt(self.harness.call(env={"STUB_STREAM": str(path)}))
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertTrue(evidence["incomplete_final_line"])
        path.write_bytes(FIXTURE.read_bytes().rstrip(b"\n"))
        _, evidence = receipt(self.harness.call(env={"STUB_STREAM": str(path)}))
        self.assertEqual(evidence["status"], "COMPLETED")
        self.assertTrue(evidence["incomplete_final_line"])
        _, evidence = receipt(self.harness.call(env={"STUB_STDERR": "Warning: unrelated config"}))
        self.assertEqual(evidence["status"], "COMPLETED")
        path.write_bytes(FIXTURE.read_bytes() + b"unrecognized stdout garbage\n")
        _, evidence = receipt(self.harness.call(env={"STUB_STREAM": str(path)}))
        self.assertEqual(evidence["status"], "INCOMPLETE")
        path.write_bytes(b"Reading additional input from stdin...\n" + FIXTURE.read_bytes())
        _, evidence = receipt(self.harness.call(env={"STUB_STREAM": str(path)}))
        self.assertEqual(evidence["status"], "COMPLETED")
        self.assertEqual(evidence["status_lines"], 1)
        self.assertEqual(evidence["diagnostic_items"], 2)

    def test_malformed_item_types_preserve_run_and_inspect_evidence(self):
        for phase in ("item.started", "item.updated", "item.completed"):
            for item_type in (["command_execution"], {"kind": "command_execution"}):
                with self.subTest(phase=phase, item_type=item_type):
                    events = [*self.events[:1], {"type": phase, "item": {"id": "bad-tool", "type": item_type}},
                              *self.events[1:]]
                    result = self.harness.call(env=self.harness.stream(events))
                    self.assertEqual(result.returncode, 1, result.stderr)
                    directory, evidence = receipt(result)
                    self.assertEqual((evidence["exit"], evidence["status"], evidence["malformed_lines"]),
                                     (0, "INCOMPLETE", 1))
                    self.assertFalse((directory / "receipt.pending").exists())
                    inspected = subprocess.run([sys.executable, str(SCRIPT), "inspect", str(directory)],
                                               capture_output=True, text=True, timeout=10)
                    self.assertEqual(inspected.returncode, 0, inspected.stderr)
                    self.assertEqual(json.loads(inspected.stdout), evidence)
                    unfinished = directory / "unfinished"
                    unfinished.mkdir()
                    shutil.copyfile(directory / "stream.jsonl", unfinished / "stream.jsonl")
                    inspected = subprocess.run([sys.executable, str(SCRIPT), "inspect", str(unfinished)],
                                               capture_output=True, text=True, timeout=10)
                    self.assertEqual(inspected.returncode, 0, inspected.stderr)
                    recovered = json.loads(inspected.stdout)
                    self.assertEqual((recovered["status"], recovered["exit"], recovered["malformed_lines"]),
                                     ("UNFINALIZED", "UNKNOWN", 1))

    def test_documented_path_has_no_legacy_recipe(self):
        main = (SKILL / "SKILL.md").read_text()
        reference = (SKILL / "references" / "monitoring.md").read_text()
        self.assertIn("scripts/" + CLI + "_run.py", main)
        self.assertNotIn("<launcher>", main)
        self.assertNotIn("fresh stdout/stderr captures", main)
        self.assertNotIn("nohup", reference)
        self.assertIn("references/monitoring.md#boundaries", main)

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
            self.assertEqual((directory / "answer.txt").read_text(), EXPECTED)
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
        spec = importlib.util.spec_from_file_location("sibling_cancel_check", SCRIPT)
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
        spec = importlib.util.spec_from_file_location("sibling_signal_windows", SCRIPT)
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
        spec = importlib.util.spec_from_file_location("sibling_stop_error", SCRIPT)
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
