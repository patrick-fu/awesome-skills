from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import online_transcribe
from audio_transcription.errors import CliError


class OnlineTests(unittest.TestCase):
    def test_online_worker_requires_execution_consent_before_reading_input(self):
        args = online_transcribe.parse_args(["/does/not/exist.m4a", "--json"])
        with self.assertRaisesRegex(CliError, "Explicit online") as raised:
            online_transcribe.execute(args)
        self.assertEqual(raised.exception.code, "ONLINE_CONSENT_REQUIRED")
        self.assertTrue(raised.exception.requires_user_decision)


if __name__ == "__main__":
    unittest.main()
