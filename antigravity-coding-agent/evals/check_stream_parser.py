#!/usr/bin/env python3
"""Replay stream fixtures through the actual launcher and an offline stub."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile

from check_launch_guards import Harness, SKILL_DIR, receipt_from


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
        print("PASS reconstructed historical fixture: RunCommand denied + empty response = INCOMPLETE")

        init = {"event": "init", "init": {"model": "fixture-model", "cwd": "/workspace/probe"}}
        success = {"event": "result", "result": {
            "status": "SUCCESS", "response": "回答", "denied_actions": []
        }}
        encode = lambda events: "".join(json.dumps(event) + "\n" for event in events)
        cases = [
            ("complete", encode([init, success]), {}, "SUCCESS", {}),
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
            ("missing-denials", encode([init, {"event": "result", "result": {"status": "SUCCESS", "response": "ok"}}]),
             {}, "INCOMPLETE", {"denied_actions": "UNKNOWN"}),
            ("timeout-exit-zero", encode([init, success]), {"STUB_STDERR": "Warning: print timeout reached\n"},
             "INCOMPLETE", {"timeout_warning": True, "exit": 0}),
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
            print(f"PASS {name}: {status}, {fields}")
    print("Antigravity stream parser checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
