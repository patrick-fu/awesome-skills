from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audio_transcription import config, pipeline
from audio_transcription.errors import CliError


class StorageConfigTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.previous = {
            name: os.environ.get(name)
            for name in (
                "AUDIO_TRANSCRIPTION_STORAGE_CONFIG",
                "AUDIO_TRANSCRIPTION_APP_ROOT",
                "AUDIO_TRANSCRIPTION_CACHE_ROOT",
                "AUDIO_TRANSCRIPTION_TEMP_ROOT",
                "AUDIO_TRANSCRIPTION_TRANSCRIPT_ROOT",
            )
        }
        os.environ["AUDIO_TRANSCRIPTION_STORAGE_CONFIG"] = str(
            self.root / "state" / "storage.json"
        )
        for name in self.previous:
            if name != "AUDIO_TRANSCRIPTION_STORAGE_CONFIG":
                os.environ.pop(name, None)

    def tearDown(self):
        for name, value in self.previous.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value
        self.temporary.cleanup()

    def test_unconfigured_storage_preserves_legacy_defaults(self):
        self.assertEqual(
            config.app_root(), Path.home() / "Library/Application Support/audio-transcription"
        )
        self.assertEqual(
            config.cache_root(), Path.home() / "Library/Caches/audio-transcription"
        )
        self.assertIsNone(config.temp_root())
        self.assertIsNone(config.transcript_root())
        self.assertFalse(config.storage_config_path().exists())

    def test_configure_persists_distinct_roots_and_reports_them(self):
        app = self.root / "external" / "runtime"
        app.mkdir(parents=True)
        (app / "active-python").write_text("/bin/sh\n")
        value = config.configure_storage(
            app=app,
            cache=self.root / "external" / "cache",
            temporary=self.root / "external" / "tmp",
            transcripts=self.root / "external" / "transcripts",
        )
        self.assertEqual(value["schema_version"], 1)
        self.assertEqual(config.app_root(), (self.root / "external" / "runtime").resolve())
        self.assertEqual(config.cache_root(), (self.root / "external" / "cache").resolve())
        self.assertEqual(config.temp_root(), (self.root / "external" / "tmp").resolve())
        self.assertEqual(
            config.transcript_root(), (self.root / "external" / "transcripts").resolve()
        )
        stored = json.loads(config.storage_config_path().read_text())
        self.assertEqual(stored["app_root"], str(config.app_root()))
        self.assertEqual(config.storage_status()["roots"]["app_root"]["source"], "persisted")
        self.assertEqual(config.bootstrap_active_python_path().read_text(), "/bin/sh\n")

    def test_environment_overrides_persisted_root(self):
        config.configure_storage(
            app=self.root / "external" / "runtime",
            cache=self.root / "external" / "cache",
            temporary=self.root / "external" / "tmp",
            transcripts=self.root / "external" / "transcripts",
        )
        override = self.root / "one-shot-runtime"
        os.environ["AUDIO_TRANSCRIPTION_APP_ROOT"] = str(override)
        self.assertEqual(config.app_root(), override)
        self.assertEqual(config.storage_status()["roots"]["app_root"]["source"], "environment")

    def test_default_offline_output_uses_persisted_transcript_root(self):
        config.configure_storage(
            app=self.root / "external" / "runtime",
            cache=self.root / "external" / "cache",
            temporary=self.root / "external" / "tmp",
            transcripts=self.root / "external" / "transcripts",
        )
        output = pipeline._prepare_output(None)
        self.assertEqual(output.parent, config.transcript_root())
        output.rmdir()

    def test_rejects_invalid_or_overlapping_configuration(self):
        config.storage_config_path().parent.mkdir(parents=True)
        config.storage_config_path().write_text("{}")
        with self.assertRaisesRegex(CliError, "Unsupported or incomplete"):
            config.app_root()
        config.storage_config_path().unlink()
        with self.assertRaisesRegex(CliError, "must not overlap"):
            config.configure_storage(
                app=self.root / "external",
                cache=self.root / "external" / "cache",
                temporary=self.root / "tmp",
                transcripts=self.root / "transcripts",
            )
        with self.assertRaisesRegex(CliError, "must not overlap"):
            config.configure_storage(
                app=self.root / "shared" / ".." / "shared",
                cache=self.root / "shared",
                temporary=self.root / "tmp",
                transcripts=self.root / "transcripts",
            )


if __name__ == "__main__":
    unittest.main()
