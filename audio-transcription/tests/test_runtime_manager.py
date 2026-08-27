from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import runtime_manager
from audio_transcription.errors import CliError


class RuntimeManagerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.old_app = os.environ.get("AUDIO_TRANSCRIPTION_APP_ROOT")
        self.old_cache = os.environ.get("AUDIO_TRANSCRIPTION_CACHE_ROOT")
        os.environ["AUDIO_TRANSCRIPTION_APP_ROOT"] = str(self.root / "app")
        os.environ["AUDIO_TRANSCRIPTION_CACHE_ROOT"] = str(self.root / "cache")

    def tearDown(self):
        for name, value in (
            ("AUDIO_TRANSCRIPTION_APP_ROOT", self.old_app),
            ("AUDIO_TRANSCRIPTION_CACHE_ROOT", self.old_cache),
        ):
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value
        self.temporary.cleanup()

    def test_inspect_recommends_low_memory_for_16_gib(self):
        with patch("runtime_manager.memory_gib", return_value=16):
            result = runtime_manager.inspect()
        self.assertEqual(result["profile"]["recommended"], "low-memory")
        self.assertTrue(result["profile"]["requires_user_decision"])
        self.assertEqual(result["cli_install"]["default"], "not-installed")

    def test_install_cli_refuses_unknown_existing_entry(self):
        directory = self.root / "bin"
        directory.mkdir()
        target = directory / "local-transcribe"
        target.write_text("unknown")
        with self.assertRaisesRegex(CliError, "unknown CLI entry"):
            runtime_manager.install_cli(directory)

    def test_install_cli_is_idempotent_for_owned_launcher(self):
        directory = self.root / "bin"
        first = runtime_manager.install_cli(directory)
        second = runtime_manager.install_cli(directory)
        self.assertEqual(first["path"], second["path"])
        self.assertIn(runtime_manager.CLI_MARKER, Path(first["path"]).read_text())

    def test_cleanup_is_preview_by_default(self):
        app = Path(os.environ["AUDIO_TRANSCRIPTION_APP_ROOT"])
        (app / "models").mkdir(parents=True)
        (app / "models" / "keep").write_text("x")
        result = runtime_manager.cleanup(cache_only=False, all_data=False, dry_run=True)
        self.assertTrue(result["dry_run"])
        self.assertTrue((app / "models" / "keep").exists())

    def test_setup_activates_only_after_smoke(self):
        app = Path(os.environ["AUDIO_TRANSCRIPTION_APP_ROOT"])

        def fake_run(command, **_kwargs):
            if len(command) >= 2 and command[1] == "venv":
                runtime = Path(command[-1])
                (runtime / "bin").mkdir(parents=True)
                (runtime / "bin" / "python").write_text("python")

        def fake_download(_python, root, name, _spec):
            model = root / "models" / name
            model.mkdir(parents=True, exist_ok=True)
            return model

        with (
            patch("runtime_manager.ensure_system_dependencies"),
            patch("runtime_manager.run", side_effect=fake_run),
            patch("runtime_manager.download_model", side_effect=fake_download),
            patch("runtime_manager.smoke"),
        ):
            result = runtime_manager.setup("low-memory")
        self.assertEqual(result["status"], "ready")
        active = json.loads((app / "active.json").read_text())
        self.assertEqual(active["profile"], "low-memory")
        self.assertIn("2026-08-27-r1-low-memory/bin/python", active["python"])
        self.assertFalse(
            any("staging" in path.name for path in (app / "runtimes").iterdir())
        )

    def test_smoke_failure_keeps_runtime_inactive(self):
        app = Path(os.environ["AUDIO_TRANSCRIPTION_APP_ROOT"])

        def fake_run(command, **_kwargs):
            if len(command) >= 2 and command[1] == "venv":
                runtime = Path(command[-1])
                (runtime / "bin").mkdir(parents=True)
                (runtime / "bin" / "python").write_text("python")

        def fake_download(_python, root, name, _spec):
            model = root / "models" / name
            model.mkdir(parents=True, exist_ok=True)
            return model

        with (
            patch("runtime_manager.ensure_system_dependencies"),
            patch("runtime_manager.run", side_effect=fake_run),
            patch("runtime_manager.download_model", side_effect=fake_download),
            patch(
                "runtime_manager.smoke",
                side_effect=CliError("SMOKE_FAILED", "bad smoke"),
            ),
            self.assertRaisesRegex(CliError, "bad smoke"),
        ):
            runtime_manager.setup("low-memory")
        self.assertFalse((app / "active.json").exists())
        self.assertFalse(
            any("staging" in path.name for path in (app / "runtimes").iterdir())
        )


if __name__ == "__main__":
    unittest.main()
