from __future__ import annotations

import importlib.util
import tempfile
import unittest
from unittest import mock
from pathlib import Path
from types import SimpleNamespace


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "transcribe.py"
SPEC = importlib.util.spec_from_file_location("audio_transcription", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TranscriptionHelpersTest(unittest.TestCase):
    def test_mode_defaults_to_dual(self) -> None:
        args = MODULE.parse_args(["recording.m4a"])
        self.assertEqual(args.mode, "dual")
        self.assertFalse(args.online_consent)
        self.assertFalse(args.enable_ddc)
        self.assertFalse(args.condition_on_previous_text)

    def test_whisper_command_uses_installed_cli_and_repo_id(self) -> None:
        args = MODULE.parse_args(["recording.m4a", "--mode", "offline"])
        with mock.patch.object(
            MODULE.shutil,
            "which",
            return_value="/Users/test/.local/bin/mlx_whisper",
        ):
            command = MODULE.build_whisper_cli_command(
                args,
                Path("/tmp/output"),
                "result",
            )
        self.assertEqual(command[0], "/Users/test/.local/bin/mlx_whisper")
        self.assertIn("mlx-community/whisper-large-v3-turbo", command)
        self.assertIn("--output-format", command)
        self.assertIn("json", command)
        self.assertNotIn("uv", command)

    def test_explicit_single_modes(self) -> None:
        self.assertEqual(
            MODULE.parse_args(["recording.m4a", "--mode", "offline"]).mode,
            "offline",
        )
        self.assertEqual(
            MODULE.parse_args(["recording.m4a", "--mode", "online"]).mode,
            "online",
        )

    def test_online_segments_include_speaker_and_milliseconds(self) -> None:
        raw = {
            "api_response": {
                "result": {
                    "utterances": [
                        {
                            "start_time": 1250,
                            "end_time": 2750,
                            "text": "测试文本",
                            "speaker_id": "2",
                        }
                    ]
                }
            }
        }
        segments = MODULE.normalize_doubao_segments(raw)
        self.assertEqual(segments[0]["start"], 1.25)
        self.assertEqual(segments[0]["end"], 2.75)
        self.assertEqual(segments[0]["speaker"], "2")
        rendered = MODULE.render_transcript(segments)
        self.assertIn("00:00:01.250 --> 00:00:02.750 speaker=2", rendered)

    def test_json_safe_replaces_non_finite_values(self) -> None:
        self.assertIsNone(MODULE.json_safe(float("nan")))
        self.assertIsNone(MODULE.json_safe(float("inf")))
        self.assertEqual(MODULE.json_safe({"value": 1.5}), {"value": 1.5})

    def test_cross_validation_marks_term_differences(self) -> None:
        offline = [
            {"start": 0.0, "end": 2.0, "text": "收益是 16.6% RTC", "speaker": None}
        ]
        online = [
            {"start": 0.0, "end": 2.0, "text": "收益是 16% RCT", "speaker": "1"}
        ]
        report = MODULE.build_cross_validation(offline, online)
        self.assertIn("16.6%", report)
        self.assertIn("RTC", report)
        self.assertIn("16%", report)
        self.assertIn("RCT", report)

    def test_write_json_emits_strict_json_for_nan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "raw.json"
            MODULE.write_json(output, {"value": float("nan")})
            self.assertEqual(output.read_text(encoding="utf-8"), '{\n  "value": null\n}\n')

    def test_new_console_auth_takes_precedence(self) -> None:
        headers, mode = MODULE.resolve_doubao_auth(
            {
                "DOUBAO_API_KEY": "new-key",
                "DOUBAO_APPID": "legacy-app",
                "DOUBAO_ACCESS_TOKEN": "legacy-token",
            }
        )
        self.assertEqual(headers, {"X-Api-Key": "new-key"})
        self.assertEqual(mode, "new-console-api-key")

    def test_legacy_auth_remains_supported(self) -> None:
        headers, mode = MODULE.resolve_doubao_auth(
            {
                "DOUBAO_APPID": "legacy-app",
                "DOUBAO_ACCESS_TOKEN": "legacy-token",
            }
        )
        self.assertEqual(
            headers,
            {
                "X-Api-App-Key": "legacy-app",
                "X-Api-Access-Key": "legacy-token",
            },
        )
        self.assertEqual(mode, "legacy-app-id-access-token")

    def test_mp3_payload_does_not_claim_raw_codec(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            mp3 = Path(directory) / "audio.mp3"
            mp3.write_bytes(b"fake-mp3")
            args = SimpleNamespace(
                doubao_audio_url=None,
                doubao_audio_format="mp3",
            )
            payload, transport = MODULE.build_doubao_audio_payload(args, mp3)
        self.assertEqual(payload["format"], "mp3")
        self.assertNotIn("codec", payload)
        self.assertEqual(payload["rate"], 16000)
        self.assertEqual(payload["channel"], 1)
        self.assertEqual(transport, "base64-data-compatibility")

    def test_documented_url_payload(self) -> None:
        args = SimpleNamespace(
            doubao_audio_url="https://example.com/audio.ogg",
            doubao_audio_format="ogg",
        )
        payload, transport = MODULE.build_doubao_audio_payload(args, None)
        self.assertEqual(
            payload,
            {
                "url": "https://example.com/audio.ogg",
                "format": "ogg",
            },
        )
        self.assertEqual(transport, "documented-url")


if __name__ == "__main__":
    unittest.main()
