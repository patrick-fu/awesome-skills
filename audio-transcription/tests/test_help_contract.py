from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class HelpContractTests(unittest.TestCase):
    def run_script(self, name: str, *args: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["AUDIO_TRANSCRIPTION_APP_ROOT"] = (
            "/nonexistent/audio-transcription-test"
        )
        return subprocess.run(
            [str(ROOT / "scripts" / name), *args],
            text=True,
            capture_output=True,
            check=False,
            env=environment,
        )

    def test_help_and_topics_work_without_setup(self):
        for script in ("local-transcribe", "manage-runtime", "online-transcribe"):
            result = self.run_script(script, "--help")
            self.assertEqual(result.returncode, 0, (script, result.stderr))
            self.assertTrue(result.stdout.strip())
        for topic in (
            "transcribe",
            "plan",
            "doctor",
            "outputs",
            "profiles",
            "cache",
            "privacy",
            "errors",
            "examples",
        ):
            result = self.run_script("local-transcribe", "help", topic)
            self.assertEqual(result.returncode, 0, topic)
        for topic in ("inspect", "setup", "doctor", "install-cli", "cleanup"):
            result = self.run_script("manage-runtime", "help", topic)
            self.assertEqual(result.returncode, 0, topic)

    def test_main_help_exposes_agent_contract(self):
        text = self.run_script("local-transcribe", "--help").stdout
        for value in (
            "DEFAULT BEHAVIOR",
            "SAFE DISCOVERY",
            "network",
            "--json",
            "SETUP_REQUIRED",
            "Multiple media files run one invocation at a time",
            "Do not\n  parallelize files",
        ):
            self.assertIn(value, text)
        online = self.run_script("online-transcribe", "--help").stdout
        for value in (
            "NETWORK: required",
            "UPLOAD:",
            "CONSENT:",
            "Do not parallelize online jobs",
        ):
            self.assertIn(value, online)

    def test_every_public_subcommand_has_pre_setup_help(self):
        commands = {
            "local-transcribe": ("transcribe", "plan", "doctor", "cache"),
            "manage-runtime": ("inspect", "setup", "doctor", "install-cli", "cleanup"),
        }
        for script, subcommands in commands.items():
            for command in subcommands:
                result = self.run_script(script, command, "--help")
                self.assertEqual(result.returncode, 0, (script, command, result.stderr))
                self.assertTrue(result.stdout.strip())
        nested = self.run_script("local-transcribe", "cache", "status", "--help")
        self.assertEqual(nested.returncode, 0)

    def test_skill_is_compact_router_without_runtime_facts(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertLess(len(text), 2400)
        self.assertIn("scripts/local-transcribe plan", text)
        self.assertIn("事实源", text)
        self.assertIn("前一个命令退出后再开始下一个", text)
        for forbidden in (
            "a8379a2",
            "7210aef",
            "qwen_chunk_seconds",
            "minimum_memory_gib",
        ):
            self.assertNotIn(forbidden, text)

    def test_model_lock_has_two_explicit_profiles_and_revisions(self):
        value = json.loads(
            (ROOT / "runtime" / "models.lock.json").read_text(encoding="utf-8")
        )
        self.assertEqual(set(value["profiles"]), {"standard", "low-memory"})
        for profile in value["profiles"].values():
            for name in ("qwen", "moss"):
                self.assertRegex(profile[name]["revision"], r"^[0-9a-f]{40}$")
        self.assertTrue((ROOT / "runtime" / value["requirements_lock"]).is_file())
        for script in ("local-transcribe", "manage-runtime", "online-transcribe"):
            version = self.run_script(script, "--version")
            self.assertEqual(version.returncode, 0)
            self.assertIn(value["runtime_version"], version.stdout)

    def test_skill_remains_model_invoked(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("disable-model-invocation", text)
        openai = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertNotIn("allow_implicit_invocation: false", openai)


if __name__ == "__main__":
    unittest.main()
