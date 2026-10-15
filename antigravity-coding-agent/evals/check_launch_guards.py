#!/usr/bin/env python3
"""Replay launch incidents against an offline executable, with positive controls."""

from __future__ import annotations

import json
import argparse
from contextlib import redirect_stdout
from datetime import datetime, timezone
import io
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "agy_run.py"


class Harness:
    def __init__(self, root: Path):
        self.home = root / "home"
        self.cwd = self.home / "project with spaces"
        self.cwd.mkdir(parents=True)
        self.captures = root / "captures"
        self.captures.mkdir()
        self.prompt = root / "prompt.txt"
        self.prompt.write_text("Read the authorized files.\nReturn an answer.\n", encoding="utf-8")
        self.stub = root / "stub agy"
        shutil.copyfile(SKILL_DIR / "evals" / "stub_agy.py", self.stub)
        self.stub.chmod(0o700)
        self.env = dict(os.environ, HOME=str(self.home), TMPDIR=str(self.captures))
        for key in ("STUB_STREAM", "STUB_EXIT", "STUB_STDERR"):
            self.env.pop(key, None)

    def command(self, timeout="45m", cwd=None, prompt=None, extra=()):
        return [sys.executable, str(SCRIPT), "--cwd", str(cwd or self.cwd),
                "--prompt-file", str(prompt or self.prompt), f"--print-timeout={timeout}",
                "--label", "same-attempt", "--agy-bin", str(self.stub), *extra]

    def invoke(self, env=None, **options):
        return subprocess.run(self.command(**options), cwd=self.home,
                              env=dict(self.env, **(env or {})), capture_output=True, text=True)

    def rejected(self, guard, **options):
        home_before = sorted(str(path) for path in self.home.rglob("*"))
        captures_before = sorted(self.captures.iterdir())
        observed = self.cwd / "invoked.json"
        marker_before = observed.read_bytes() if observed.exists() else None
        result = self.invoke(**options)
        assert result.returncode != 0, result
        assert guard in result.stderr, result.stderr
        assert not result.stdout, result.stdout
        assert home_before == sorted(str(path) for path in self.home.rglob("*"))
        assert captures_before == sorted(self.captures.iterdir())
        assert marker_before == (observed.read_bytes() if observed.exists() else None)
        print(f"PASS rejected {guard}: {options}")


def receipt_from(result):
    lines = result.stdout.splitlines()
    directory = Path(json.loads(lines[0])["run_dir"])
    receipt = json.loads(lines[1])
    assert json.loads((directory / "receipt.json").read_text()) == receipt
    assert (directory / "rc.txt").read_text().strip() == str(receipt["exit"])
    assert {path.name for path in directory.iterdir()} == {
        "stream.jsonl", "stderr.log", "rc.txt", "receipt.json"
    }
    return directory, receipt


def check_docs():
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    monitoring = (SKILL_DIR / "references" / "monitoring.md").read_text(encoding="utf-8")
    normalized = " ".join((skill + monitoring).split())
    for obsolete in (
        "unit-bearing `--print-timeout`", "check current help rather than relying on a default",
        "Retain the host process handle and fresh stdout/stderr captures",
        "Without that facility, capture to a fresh system-temp directory",
        "arrange for the launch wrapper to save the child's exit code", "nohup",
    ):
        assert obsolete not in normalized, obsolete
    examples = re.findall(r"```bash\n(.*?)\n```", skill, re.DOTALL)
    assert examples and all("python3" in example and "agy_run.py" in example for example in examples)
    assert "<launcher>" not in skill
    assert "only supported entry point" in skill
    extraction = '''For answer extraction only, after saving a stream:

```bash
jq -er '
  select(.event == "result") | .result
  | select(.status == "SUCCESS" and ((.denied_actions // []) | length) == 0)
  | .response | select(length > 0)
' "$STREAM_FILE"
```

This does not check the exit, timeout, completed tools, or artifact correctness.'''
    assert extraction in monitoring
    assert "authorization tree/status-diff" in monitoring
    print("PASS docs: obsolete recipes removed; answer-only jq boundary unchanged")


def main() -> int:
    check_docs()
    with tempfile.TemporaryDirectory(prefix="agy-guard-eval-") as temp:
        root = Path(temp).resolve()
        harness = Harness(root)
        for timeout in ("240", "2700", "-1s", "1h30m", "1s\n"):
            harness.rejected("G0", timeout=timeout)
        for cwd in (root / "missing", Path("relative"), harness.prompt, harness.home, root, Path("/")):
            harness.rejected("G1", cwd=cwd)
        link = root / "home-link"
        link.symlink_to(harness.home, target_is_directory=True)
        harness.rejected("G1", cwd=link)
        for content in ("", " \n\t", "bad\0text"):
            empty = root / "empty.txt"
            empty.write_text(content)
            harness.rejected("G2", prompt=empty)
        harness.rejected("G2", prompt=root / "absent.txt")
        harness.rejected("G2", prompt=root)
        harness.rejected("G3", env={"TMPDIR": str(root / "absent-temp")})
        for extra in (("--", "--print-timeout=240"), ("--", "-p", "bypass"),
                      ("--", "-print-timeout", "2700"), ("--", "--output-format=text")):
            harness.rejected("G0", extra=extra)
        for timeout in ("0", "45m", "240s", "5400s", "1.5ms", "1µs"):
            result = harness.invoke(timeout=timeout)
            assert result.returncode == 0, result.stderr
            directory, receipt = receipt_from(result)
            assert directory.parent == harness.captures
            assert re.fullmatch(r"agy-same-attempt-\d{8}T\d{6}\.\d+Z-\d+-.+", directory.name)
            assert receipt["status"] == "SUCCESS" and receipt["exit"] == 0
            assert receipt["model"] == "stub-model"
            assert receipt["cwd"] == str(harness.cwd)
            assert receipt["response_bytes"] == 6
            observed = json.loads((harness.cwd / "invoked.json").read_text())
            assert observed["args"] == ["--output-format", "stream-json", "--print-timeout", timeout,
                                        "-p", harness.prompt.read_text()]
            assert observed["home"] == str(harness.home)
            print(f"PASS allowed G0–G5: {timeout}, valid cwd/prompt, rc=0, SUCCESS")

        extra = ["--model", "chosen-model", "--effort", "high", "--add-dir", "space and ; literal",
                 "--add-dir", "cwd", "--conversation", "chosen-id", "--continue", "--mode", "accept-edits"]
        result = harness.invoke(extra=["--", *extra])
        assert result.returncode == 0, result.stderr
        observed = json.loads((harness.cwd / "invoked.json").read_text())
        assert observed["args"][:len(extra)] == extra
        print("PASS unchanged launcher arguments and HOME; no automatic resume or escalation")

        sys.path.insert(0, str(SKILL_DIR / "scripts"))
        import agy_run

        arguments = argparse.Namespace(cwd=str(harness.cwd), prompt_file=str(harness.prompt),
                                       print_timeout="0", label="same-attempt", agy_bin=str(harness.stub),
                                       launcher_args=[])
        directories = []
        with patch.object(agy_run, "datetime") as frozen:
            frozen.now.return_value = datetime(2026, 1, 1, tzinfo=timezone.utc)
            for message in ("first stderr retained\n", "second stderr\n"):
                output = io.StringIO()
                with patch.dict(os.environ, dict(harness.env, STUB_STDERR=message), clear=True), redirect_stdout(output):
                    assert agy_run.run(arguments) == 0
                directory, _ = receipt_from(subprocess.CompletedProcess([], 0, output.getvalue()))
                directories.append(directory)
        first, second = directories
        assert first != second
        assert first.name.rsplit("-", 1)[0] == second.name.rsplit("-", 1)[0]
        assert (first / "stderr.log").read_text() == "first stderr retained\n"
        assert (second / "stderr.log").read_text() == "second stderr\n"
        print("PASS G3: same label/time/PID produces independent attempts; first stderr survives")

        failure = harness.invoke(env={"STUB_EXIT": "7"})
        _, receipt = receipt_from(failure)
        assert failure.returncode == 7 and receipt["exit"] == 7 and receipt["status"] == "FAILED"
        outer = subprocess.run(
            ["sh", "-c", '"$@"; printf "tail succeeded\\n"', "outer", *harness.command()],
            cwd=harness.home, env=dict(harness.env, STUB_EXIT="7"), capture_output=True, text=True,
        )
        assert outer.returncode == 0 and outer.stdout.endswith("tail succeeded\n")
        _, receipt = receipt_from(outer)
        assert receipt["status"] == "FAILED" and receipt["exit"] == 7
        print("PASS G4/G5: trailing successful shell command cannot replace child rc=7")

        result = subprocess.run(harness.command() + ["--agy-bin", str(root / "missing-binary")],
                                env=harness.env, capture_output=True, text=True)
        _, receipt = receipt_from(result)
        assert result.returncode != 0 and receipt["exit"] == "UNKNOWN"
        assert receipt["status"] == "FAILED" and "--agy-bin" in result.stderr
        print("PASS G4: unavailable executable reports UNKNOWN exit and actionable error")
    print("Antigravity launch guard checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
