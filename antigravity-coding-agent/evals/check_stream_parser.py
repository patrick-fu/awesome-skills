#!/usr/bin/env python3
"""Replay stream fixtures through the actual launcher and an offline stub."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

from check_launch_guards import Harness, SKILL_DIR, SCRIPT, receipt_from


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="agy-parser-eval-") as temp:
        root = Path(temp).resolve()
        harness = Harness(root)
        fixture = SKILL_DIR / "evals" / "fixtures" / "denied.jsonl"
        result = harness.invoke(env={"STUB_STREAM": str(fixture)})
        _, receipt = receipt_from(result)
        assert result.returncode != 0 and receipt["status"] == "INCOMPLETE"
        assert receipt["result_status"] == "SUCCESS" and receipt["exit"] == 0
        assert receipt["model"] == "gemini-3.8-flash-high"
        assert receipt["cwd"] == "/workspace/probe"
        assert receipt["denied_actions"] == ["RunCommand"] and receipt["response_bytes"] == 0
        assert receipt["incomplete_final_line"] is False
        assert Path(receipt["answer_file"]).read_text(encoding="utf-8") == ""
        print("PASS reconstructed historical fixture: RunCommand denied + empty response = INCOMPLETE")

        live_fixture = SKILL_DIR / "evals" / "fixtures" / "success-1.3.6.jsonl"
        result = harness.invoke(env={"STUB_STREAM": str(live_fixture)})
        directory, receipt = receipt_from(result)
        assert result.returncode == 0 and receipt["status"] == "SUCCESS", receipt
        assert receipt["model"] == "gemini-3.8-flash-high"
        assert receipt["cwd"] == "/workspace/live-probe"
        assert receipt["denied_actions"] == "UNKNOWN"
        assert Path(receipt["answer_file"]).read_text() == "live-sanitized|46\n"
        assert (directory / "stream.jsonl").read_bytes() == live_fixture.read_bytes()
        print("PASS sanitized agy 1.3.6 live success: omitted denials remain UNKNOWN, not a false incomplete")

        init = {"event": "init", "init": {"model": "fixture-model", "cwd": "/workspace/probe"}}
        success = {"event": "result", "result": {
            "status": "SUCCESS", "response": "回答", "denied_actions": []
        }}
        encode = lambda events: "".join(json.dumps(event) + "\n" for event in events)
        cases = [
            ("complete", encode([init, success]), {}, "SUCCESS", {}),
            ("complete-without-newline", encode([init, success]).rstrip("\n"), {},
             "SUCCESS", {"incomplete_final_line": True}),
            ("truncated-result", encode([init]) + '{"event":"result","result":', {},
             "INCOMPLETE", {"incomplete_final_line": True, "result_status": "UNKNOWN"}),
            ("truncated-after-result", encode([init, success]) + '{"event":', {},
             "INCOMPLETE", {"incomplete_final_line": True}),
            ("missing-init-model", encode([{"event": "init", "init": {"cwd": "/workspace/probe"}}, success]),
             {}, "INCOMPLETE", {"model": "UNKNOWN"}),
            ("unknown-event-only", encode([{"event": "future", "status": "SUCCESS", "model": "fake"}]),
             {}, "INCOMPLETE", {"model": "UNKNOWN", "cwd": "UNKNOWN", "denied_actions": "UNKNOWN",
                                "response_bytes": "UNKNOWN"}),
            ("unknown-event-alongside-success", encode([init, {"event": "future", "payload": {}}, success]),
             {}, "SUCCESS", {}),
            ("step-noise", encode([init, {"event": "step_update", "step_update": {
                "text_delta": "unshown-delta " * 5000}}, success]), {}, "SUCCESS", {}),
            ("missing-denials", encode([init, {"event": "result", "result": {"status": "SUCCESS", "response": "ok"}}]),
             {}, "SUCCESS", {"denied_actions": "UNKNOWN"}),
            ("invalid-denials", encode([init, {"event": "result", "result": {
                "status": "SUCCESS", "response": "ok", "denied_actions": {}}}]),
             {}, "INCOMPLETE", {"denied_actions": "UNKNOWN"}),
            ("null-denials", encode([init, {"event": "result", "result": {
                "status": "SUCCESS", "response": "ok", "denied_actions": None}}]),
             {}, "INCOMPLETE", {"denied_actions": "UNKNOWN"}),
            ("denied-with-answer", encode([init, {"event": "result", "result": {
                "status": "SUCCESS", "response": "partial answer", "denied_actions": ["RunCommand"]}}]),
             {}, "SUCCESS", {"denied_actions": ["RunCommand"]}),
            ("empty-without-denials", encode([init, {"event": "result", "result": {
                "status": "SUCCESS", "response": "", "denied_actions": []}}]),
             {}, "INCOMPLETE", {"response_bytes": 0}),
            ("timeout-exit-zero", encode([init, success]), {"STUB_STDERR": "Warning: print timeout reached\n"},
             "INCOMPLETE", {"timeout_warning": True, "exit": 0}),
            ("auxiliary-timeout", encode([init, success]),
             {"STUB_STDERR": "Warning: optional telemetry request timed out; main turn finished\n"},
             "SUCCESS", {"timeout_warning": False}),
            ("cli-deadline", encode([init, success]),
             {"STUB_STDERR": "Warning: print-timeout deadline exceeded\n"},
             "INCOMPLETE", {"timeout_warning": True}),
            ("ordinary-warning", encode([init, success]), {"STUB_STDERR": "Warning: optional update unavailable\n"},
             "SUCCESS", {"timeout_warning": False}),
            ("timeout-option-not-expiry", encode([init, success]),
             {"STUB_STDERR": "Warning: print-timeout default is 0s\n"},
             "SUCCESS", {"timeout_warning": False}),
            ("error-with-answer", encode([init, {"event": "result", "result": {
                "status": "ERROR", "response": "partial", "denied_actions": []}}]),
             {}, "FAILED", {"result_status": "ERROR", "response_bytes": 7}),
            ("malformed-middle", encode([init]) + "not JSON\n" + encode([success]), {}, "INCOMPLETE", {}),
            ("wrong-schema", encode([{"type": "init", "model": "fake", "cwd": "/fake"}, success]),
             {}, "INCOMPLETE", {"model": "UNKNOWN", "cwd": "UNKNOWN"}),
            ("wrong-types", encode([init, {"event": "result", "result": {
                "status": True, "response": 12, "denied_actions": {}}}]),
             {}, "INCOMPLETE", {"result_status": "UNKNOWN", "response_bytes": "UNKNOWN", "denied_actions": "UNKNOWN"}),
            ("error-then-success", encode([init, {"event": "result", "result": {
                "status": "ERROR", "response": "partial", "denied_actions": []}}, success]),
             {}, "FAILED", {"result_status": "ERROR"}),
            ("denied-then-success", fixture.read_text() + encode([success]), {},
             "INCOMPLETE", {"denied_actions": ["RunCommand"], "response_bytes": 0}),
            ("success-then-extra-result", encode([init, success, success]), {}, "INCOMPLETE", {}),
            ("structured-stderr-error", encode([init, success]),
             {"STUB_STDERR": 'AGY_ERROR: {"status":"ERROR","error_code":"STREAM_FAILED"}\n'},
             "FAILED", {"exit": 0}),
            ("unpaired-surrogate", encode([init, {"event": "result", "result": {
                "status": "SUCCESS", "response": "\ud800", "denied_actions": []}}]),
             {}, "INCOMPLETE", {"response_bytes": "UNKNOWN"}),
            ("invalid-init-model", encode([{"event": "init", "init": {
                "model": "\ud800", "cwd": "/workspace/probe"}}, success]),
             {}, "INCOMPLETE", {"model": "UNKNOWN"}),
        ]
        for name, stream, environment, status, fields in cases:
            path = root / f"{name}.jsonl"
            path.write_text(stream, encoding="utf-8")
            result = harness.invoke(env={"STUB_STREAM": str(path), **environment})
            directory, receipt = receipt_from(result)
            assert receipt["status"] == status, (name, receipt)
            assert (result.returncode == 0) == (status == "SUCCESS"), (name, result)
            assert (directory / "stream.jsonl").read_bytes() == path.read_bytes()
            for key, expected in fields.items():
                assert receipt[key] == expected, (name, key, receipt)
            if name == "error-with-answer":
                assert Path(receipt["answer_file"]).read_text(encoding="utf-8") == "partial"
            elif name == "complete":
                assert Path(receipt["answer_file"]).read_text(encoding="utf-8") == "回答"
            elif name == "step-noise":
                inspect = subprocess.run([sys.executable, str(SCRIPT), "inspect", str(directory)],
                                         env=harness.env, capture_output=True, text=True, timeout=10)
                assert inspect.returncode == 0 and json.loads(inspect.stdout) == receipt
                assert "unshown-delta" not in inspect.stdout
                assert len(inspect.stdout.encode()) < path.stat().st_size / 10
            print(f"PASS {name}: {status}, {fields}")

        child = subprocess.Popen(harness.command(), cwd=harness.home,
                                 env=dict(harness.env, STUB_SLEEP="1"), stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True)
        try:
            directory = Path(json.loads(child.stdout.readline())["run_dir"])
            deadline = time.monotonic() + 5
            while not (directory / "stream.jsonl").stat().st_size and child.poll() is None and time.monotonic() < deadline:
                time.sleep(0.01)
            assert child.poll() is None, "Stub must still be alive for the incomplete-process control"
            assert not (directory / "receipt.json").exists()
            inspect = subprocess.run([sys.executable, str(SCRIPT), "inspect", str(directory)],
                                     env=harness.env, capture_output=True, text=True, timeout=10)
            evidence = json.loads(inspect.stdout)
            assert inspect.returncode == 0 and evidence["status"] == "UNFINALIZED"
            assert evidence["exit"] == "UNKNOWN" and evidence["result_status"] == "SUCCESS"
            child.communicate(timeout=10)
            assert child.returncode == 0
            assert not (directory / "receipt.pending").exists()
            inspect = subprocess.run([sys.executable, str(SCRIPT), "inspect", str(directory)],
                                     env=harness.env, capture_output=True, text=True, timeout=10)
            assert json.loads(inspect.stdout) == json.loads((directory / "receipt.json").read_text())
            assert json.loads(inspect.stdout)["status"] == "SUCCESS"
            print("PASS inspect: terminal line before child exit stays UNFINALIZED; final receipt is atomic")
        finally:
            if child.poll() is None:
                child.kill()
                child.communicate()
        unfinalized = root / "abandoned"
        unfinalized.mkdir()
        (unfinalized / "stream.jsonl").write_text(encode([init, success]))
        (unfinalized / "stderr.log").write_text("")
        inspect = subprocess.run([sys.executable, str(SCRIPT), "inspect", str(unfinalized)],
                                 env=harness.env, capture_output=True, text=True, timeout=10)
        assert json.loads(inspect.stdout)["status"] == "UNFINALIZED"
        inspect = subprocess.run([sys.executable, str(SCRIPT), "inspect", str(root / "absent")],
                                 env=harness.env, capture_output=True, text=True, timeout=10)
        assert inspect.returncode != 0 and "capture path" in inspect.stderr
        print("PASS inspect: abandoned capture is not called running; missing path is rejected")
    print("Antigravity stream parser checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
