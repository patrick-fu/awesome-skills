from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audio_transcription.media import chunk_ranges


class MediaTests(unittest.TestCase):
    def test_short_audio_uses_one_chunk(self):
        self.assertEqual(chunk_ranges(500, 1200, []), [(0.0, 500)])

    def test_long_audio_prefers_silence_before_maximum(self):
        ranges = chunk_ranges(2500, 1200, [900, 1180, 2050, 2380])
        self.assertEqual(ranges[0], (0.0, 1180))
        self.assertEqual(ranges[1], (1180, 2380))
        self.assertEqual(ranges[2], (2380, 2500))
        self.assertTrue(all(end - start <= 1200 for start, end in ranges))

    def test_long_audio_falls_back_to_hard_boundary(self):
        self.assertEqual(
            chunk_ranges(1300, 600, []), [(0.0, 600.0), (600.0, 1200.0), (1200.0, 1300)]
        )


if __name__ == "__main__":
    unittest.main()
