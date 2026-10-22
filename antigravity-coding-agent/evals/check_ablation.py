#!/usr/bin/env python3
"""Replay one-mechanism removals through the real launcher and offline stub."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile

import check_launch_guards as guards


def verdict(result):
    if not result.stdout:
        return "REJECTED"
    return guards.receipt_from(result)[1]["status"]


def main():
    original_script = guards.SCRIPT
    source = original_script.read_text(encoding="utf-8")
    init = {"event": "init", "init": {"model": "fixture-model", "cwd": "/workspace/probe"}}
    success = {"event": "result", "result": {"status": "SUCCESS", "response": "answer", "denied_actions": []}}
    variants = [
        ("duration", 'if not DURATION.fullmatch(args.print_timeout):', 'if False:', "bare-duration"),
        ("home-boundary", 'if cwd == home or cwd in home.parents:', 'if False:', "home"),
        ("prompt", 'if not prompt.strip() or "\\0" in prompt:', 'if False:', "empty-prompt"),
        ("child-exit", 'exit_code = child.wait(timeout=0.1)',
         'child.wait(timeout=0.1)\n                        exit_code = 0', "exit-seven"),
        ("timeout", 'if TIMEOUT.search(line):', 'if False:', "timeout-zero-exit"),
        ("duplicate-terminal", 'if kind in seen:', 'if False:', "duplicate-result"),
    ]
    with tempfile.TemporaryDirectory(prefix="agy-ablation-") as temporary:
        root = Path(temporary).resolve()
        try:
            for name, old, new, case in variants:
                assert source.count(old) == 1, f"Ablation anchor drift: {name}"
                mutated = source.replace(old, new)
                candidate = root / f"{name}.py"
                compile(mutated, str(candidate), "exec")
                candidate.write_text(mutated)
                observations = {}
                for label, script in (("full", original_script), ("removed", candidate)):
                    guards.SCRIPT = script
                    harness = guards.Harness(root / name / label)
                    positive = harness.invoke()
                    assert positive.returncode == 0 and verdict(positive) == "SUCCESS", (name, label, positive)
                    options = {}
                    if case == "bare-duration":
                        options["timeout"] = "240"
                    elif case == "home":
                        options["cwd"] = harness.home
                    elif case == "empty-prompt":
                        harness.prompt.write_text("")
                    elif case == "exit-seven":
                        options["env"] = {"STUB_EXIT": "7"}
                    elif case == "timeout-zero-exit":
                        options["env"] = {"STUB_STDERR": "Warning: print timeout reached\n"}
                    else:
                        events = [init, success]
                        if case == "duplicate-result":
                            events.append(success)
                        fixture = root / name / label / "stream.jsonl"
                        fixture.write_text("".join(json.dumps(event) + "\n" for event in events))
                        options["env"] = {"STUB_STREAM": str(fixture)}
                    result = harness.invoke(**options)
                    observations[label] = verdict(result)
                    if label == "full":
                        assert result.returncode != 0 and observations[label] != "SUCCESS", (name, result)
                    else:
                        assert result.returncode == 0 and observations[label] == "SUCCESS", (name, result)
                print(json.dumps(dict(mechanism=name, positive_control="SUCCESS in both", **observations)), flush=True)

            old = 'receipt["denied_actions"] = denied if isinstance(denied, list) else UNKNOWN'
            assert source.count(old) == 1
            candidate = root / "denial-observation.py"
            candidate.write_text(source.replace(old, 'receipt["denied_actions"] = UNKNOWN'))
            for label, script in (("full", original_script), ("removed", candidate)):
                guards.SCRIPT = script
                harness = guards.Harness(root / "denial-observation" / label)
                fixture = root / "denial-observation" / label / "stream.jsonl"
                events = [init, {"event": "result", "result": dict(success["result"], denied_actions=["RunCommand"])}]
                fixture.write_text("".join(json.dumps(event) + "\n" for event in events))
                result = harness.invoke(env={"STUB_STREAM": str(fixture)})
                evidence = guards.receipt_from(result)[1]
                assert result.returncode == 0 and evidence["status"] == "SUCCESS"
                assert evidence["denied_actions"] == (["RunCommand"] if label == "full" else "UNKNOWN")
            print("PASS denial observation: removal loses evidence, not completion; task acceptance remains separate", flush=True)

            old = '''run_dir = Path(tempfile.mkdtemp(
            prefix=f"agy-{args.label}-{timestamp}-{os.getpid()}-", dir=temp_root
        ))'''
            new = '''run_dir = temp_root / "fixed-attempt"
        run_dir.mkdir(exist_ok=True)'''
            assert source.count(old) == 1, "Unique-capture ablation anchor drift"
            candidate = root / "fixed-capture.py"
            candidate.write_text(source.replace(old, new))
            for label, script in (("full", original_script), ("removed", candidate)):
                guards.SCRIPT = script
                harness = guards.Harness(root / "identity" / label)
                first = harness.invoke(env={"STUB_STDERR": "first evidence"})
                assert first.returncode == 0
                first_dir, _ = guards.receipt_from(first)
                second = harness.invoke(env={"STUB_STDERR": "second evidence"})
                assert (first_dir / "stderr.log").read_text() == "first evidence"
                if label == "full":
                    second_dir, _ = guards.receipt_from(second)
                    assert second.returncode == 0 and second_dir != first_dir
                else:
                    assert second.returncode != 0, "Removing uniqueness must break the second attempt"
            print("PASS capture identity: removing uniqueness blocks the second valid run; full mechanism preserves both", flush=True)
        finally:
            guards.SCRIPT = original_script
    print("Eight mechanism ablations passed. Denials are telemetry, not a completion gate; no prompt obedience rates measured.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
