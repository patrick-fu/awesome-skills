#!/usr/bin/env python3
"""Remove one mechanism at a time; its observable regression must return."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from check_run import Harness, SKILL, SCRIPT, receipt


def main():
    source = SCRIPT.read_text(encoding="utf-8")
    checks = SKILL / "evals" / "check_run.py"
    variants = [
        ("stdin", [('stdin.seek(0)', 'stdin.seek(0, os.SEEK_END)')],
         "test_stdin_wrapper_arguments_and_effective_settings"),
        ("verbose", [('"stream-json", "--verbose", *forwarded', '"stream-json", *forwarded')],
         "test_stdin_wrapper_arguments_and_effective_settings"),
        ("prompt-validation", [('if not prompt.decode("utf-8").strip() or b"\\0" in prompt:', 'if False:')],
         "test_scope_prompt_and_protocol_reject_before_spawn"),
        ("home-boundary", [('if cwd == home or cwd in home.parents:', 'if False:')],
         "test_scope_prompt_and_protocol_reject_before_spawn"),
        ("child-exit", [('exit_code = child.wait(timeout=0.1)',
                         'child.wait(timeout=0.1)\n                    exit_code = 0')],
         "test_attempts_and_child_exit_survive_shell_tail"),
        ("stream-verdict", [('return evidence, answer',
                             'evidence["status"] = "COMPLETED" if exit_code == 0 else "FAILED"\n    return evidence, answer')],
         "test_stream_negative_and_positive_controls"),
        ("init-observation", [('evidence[target] = value if isinstance(value, str) and value else UNKNOWN',
                               'evidence[target] = UNKNOWN')],
         "test_stdin_wrapper_arguments_and_effective_settings"),
    ]
    with tempfile.TemporaryDirectory(prefix="claude-ablation-") as temporary:
        root = Path(temporary).resolve()
        baseline = subprocess.run([sys.executable, str(checks)], capture_output=True, text=True, timeout=60)
        assert baseline.returncode == 0, baseline.stdout + baseline.stderr
        print("PASS full mechanism: all positive and negative controls", flush=True)
        for name, replacements, test in variants:
            mutant = source
            for old, new in replacements:
                assert mutant.count(old) == 1, f"Ablation anchor drift: {name}"
                mutant = mutant.replace(old, new)
            candidate = root / (name + ".py")
            candidate.write_text(mutant)
            compile(mutant, str(candidate), "exec")
            result = subprocess.run([sys.executable, str(checks), "RunChecks." + test],
                                    env=dict(os.environ, CLAUDE_RUN_SCRIPT=str(candidate)),
                                    capture_output=True, text=True, timeout=60)
            assert result.returncode != 0 and "FAIL:" in result.stderr and "ERROR:" not in result.stderr, (name, result.stderr)
            print(f"PASS ablation {name}: removing the mechanism restores an observed regression", flush=True)

        harness = Harness(root / "shell-control")
        shell = 'cd "$1"\n"$2" --print --output-format stream-json --verbose < "$3" > "$4" 2> "$5"\nprintf "tail succeeded\\n"\n'
        stream, stderr = root / "reused.jsonl", root / "reused.stderr"
        command = ["sh", "-c", shell, "legacy", str(root / "absent"), str(harness.stub),
                   str(harness.prompt), str(stream), str(stderr)]
        first = subprocess.run(command, cwd=harness.home, env=dict(harness.env, STUB_EXIT="7", STUB_STDERR="first failure"),
                               capture_output=True, text=True, timeout=10)
        assert first.returncode == 0
        assert harness.events()[0]["cwd"] == str(harness.home)
        assert stderr.read_text() == "first failure"
        subprocess.run(command, cwd=harness.home, env=dict(harness.env, STUB_STDERR="second attempt"),
                       capture_output=True, text=True, check=True, timeout=10)
        assert stderr.read_text() == "second attempt"
        print("PASS shell baseline: failed cd still invokes; tail masks exit 7; reused capture loses first stderr", flush=True)
        guarded = harness.call(cwd=root / "absent")
        assert guarded.returncode != 0 and len(harness.events()) == 2
        print("PASS guarded launch: identical missing cwd cannot invoke the child", flush=True)

        rows = []
        original = [json.loads(line) for line in (SKILL / "evals" / "fixtures" / "read.jsonl").read_text().splitlines()]
        for name, events in (("positive", original), ("missing-result", original[:-1]),
                             ("error-result", [*original[:-1], dict(original[-1], is_error=True)])):
            result = harness.call(env=harness.stream(events))
            _, evidence = receipt(result)
            rows.append(dict(case=name, launch_only_accepts=evidence["exit"] == 0,
                             launch_and_stream_accepts=evidence["status"] == "COMPLETED"))
        assert rows == [
            dict(case="positive", launch_only_accepts=True, launch_and_stream_accepts=True),
            dict(case="missing-result", launch_only_accepts=True, launch_and_stream_accepts=False),
            dict(case="error-result", launch_only_accepts=True, launch_and_stream_accepts=False),
        ]
        print(json.dumps(rows))
    print("Claude ablations passed; these are deterministic fault replays, not LLM obedience rates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
