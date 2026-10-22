#!/usr/bin/env python3
"""Remove one mechanism at a time and observe the corresponding regression."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from check_run import CLI, Harness, SCRIPT, SKILL


def main():
    source = SCRIPT.read_text()
    checks = SKILL / "evals" / "check_run.py"
    variants = [
        ("launcher-binding", [('executable = os.path.abspath(executable)', '')],
         "test_relative_path_selection_survives_child_cwd_change"),
        ("prompt-validation", [('if not prompt.decode("utf-8").strip() or b"\\0" in prompt:', 'if False:')],
         "test_scope_prompt_and_protocol_reject_before_spawn"),
        ("home-boundary", [('if cwd == home or cwd in home.parents:', 'if False:')],
         "test_scope_prompt_and_protocol_reject_before_spawn"),
        ("cwd-binding", [('cwd=cwd, stdin=', 'cwd=Path.home(), stdin=')],
         "test_transport_arguments_and_optional_metadata"),
        ("child-exit", [('exit_code = child.wait(timeout=0.1)',
                         'child.wait(timeout=0.1)\n                    exit_code = 0')],
         "test_unique_capture_and_real_child_exit"),
        ("stream-verdict", [('    return evidence, answer',
                             '    evidence["status"] = "COMPLETED" if exit_code == 0 else "FAILED"\n    return evidence, answer')],
         "test_stream_positive_and_negative_controls"),
        ("prompt-snapshot", [('snapshot.write_bytes(prompt)', 'snapshot.write_bytes(b"")')],
         "test_transport_arguments_and_optional_metadata"),
        ("init-observation", [('evidence[target] = value if isinstance(value, str) and value else UNKNOWN',
                               'evidence[target] = UNKNOWN')],
         "test_transport_arguments_and_optional_metadata"),
    ]
    with tempfile.TemporaryDirectory(prefix=CLI + "-ablation-") as temporary:
        root = Path(temporary).resolve()
        baseline = subprocess.run([sys.executable, str(checks)], capture_output=True, text=True, timeout=90)
        assert baseline.returncode == 0, baseline.stdout + baseline.stderr
        print("PASS full mechanism: positive and negative controls", flush=True)
        for name, replacements, test in variants:
            mutant = source
            for old, new in replacements:
                assert mutant.count(old) == 1, f"Ablation anchor drift: {name}"
                mutant = mutant.replace(old, new)
            candidate = root / (name + ".py")
            candidate.write_text(mutant)
            compile(mutant, str(candidate), "exec")
            result = subprocess.run([sys.executable, str(checks), "RunChecks." + test],
                                    env=dict(os.environ, GROK_RUN_SCRIPT=str(candidate), PYTHONDONTWRITEBYTECODE="1"),
                                    capture_output=True, text=True, timeout=60)
            assert result.returncode != 0 and "FAIL:" in result.stderr and "ERROR:" not in result.stderr, (name, result.stderr)
            print(f"PASS ablation {name}: removing control restores observable regression", flush=True)

        harness = Harness(root / "legacy")
        stream, stderr = root / "reused.jsonl", root / "reused.stderr"
        native = ["--output-format", "streaming-messages-json", "--prompt-file", str(harness.prompt)]
        shell = 'cd "$1"\nshift\n"$@" < "$LEGACY_PROMPT" > "$LEGACY_STREAM" 2> "$LEGACY_STDERR"\nprintf "tail succeeded\\n"\n'
        command = ["sh", "-c", shell, "legacy", str(root / "absent"), str(harness.stub), *native]
        environment = dict(harness.env, LEGACY_PROMPT=str(harness.prompt),
                           LEGACY_STREAM=str(stream), LEGACY_STDERR=str(stderr), STUB_EXIT="7")
        first = subprocess.run(command, cwd=harness.home, env=dict(environment, STUB_STDERR="first failure"),
                               capture_output=True, text=True, timeout=15)
        assert first.returncode == 0
        assert harness.events()[0]["cwd"] == str(harness.home)
        assert stderr.read_text() == "first failure"
        subprocess.run(command, cwd=harness.home, env=dict(environment, STUB_STDERR="overwritten"),
                       capture_output=True, text=True, check=True, timeout=15)
        assert stderr.read_text() == "overwritten"
        guarded = harness.call(cwd=root / "absent")
        assert guarded.returncode != 0 and len(harness.events()) == 2
        print("PASS shell control: failed cd still starts, tail masks exit 7, reused stderr overwrites; guarded launch rejects", flush=True)
    print(CLI + " deterministic ablations passed; not an LLM obedience-rate measurement.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
