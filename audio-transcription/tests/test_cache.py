from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audio_transcription import cache
from audio_transcription.errors import CliError


class CacheTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.old = os.environ.get("AUDIO_TRANSCRIPTION_CACHE_ROOT")
        os.environ["AUDIO_TRANSCRIPTION_CACHE_ROOT"] = str(self.root / "cache")

    def tearDown(self):
        if self.old is None:
            os.environ.pop("AUDIO_TRANSCRIPTION_CACHE_ROOT", None)
        else:
            os.environ["AUDIO_TRANSCRIPTION_CACHE_ROOT"] = self.old
        self.temporary.cleanup()

    def test_store_and_restore_exclude_original_media(self):
        source = self.root / "source"
        source.mkdir()
        (source / "manifest.json").write_text(json.dumps({"status": "completed"}))
        (source / "transcript.md").write_text("text")
        key = "a" * 64
        entry = cache.store(
            key, source, {"status": "completed", "input": {"sha256": "b" * 64}}
        )
        self.assertTrue((entry / "transcript.md").is_file())
        self.assertFalse(
            any(path.name.startswith("original") for path in entry.iterdir())
        )
        destination = self.root / "output"
        cache.restore(entry, destination)
        self.assertEqual((destination / "transcript.md").read_text(), "text")

    def test_symlink_cache_root_is_rejected(self):
        outside = self.root / "outside"
        outside.mkdir()
        linked = self.root / "cache"
        os.symlink(outside, linked)
        with self.assertRaisesRegex(CliError, "symlink"):
            cache.scan()
        self.assertTrue(outside.is_dir())

    def test_clear_defaults_can_be_dry_run(self):
        source = self.root / "source"
        source.mkdir()
        (source / "manifest.json").write_text("{}")
        entry = cache.store(
            "c" * 64, source, {"status": "completed", "input": {"sha256": "d" * 64}}
        )
        selected = cache.clear(all_entries=True, dry_run=True)
        self.assertEqual(len(selected), 1)
        self.assertTrue(entry.exists())
        cache.clear(all_entries=True, dry_run=False)
        self.assertFalse(entry.exists())


if __name__ == "__main__":
    unittest.main()
