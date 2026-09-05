from __future__ import annotations

import fcntl
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import ANY, call, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audio_transcription import pipeline
from audio_transcription.errors import CliError


def active(root: Path) -> dict:
    return {
        "runtime_version": "test-r1",
        "profile": "standard",
        "memory_gib": 48,
        "python": sys.executable,
        "models": {
            "qwen": {
                "repo": "qwen",
                "revision": "1" * 40,
                "path": str(root / "qwen-model"),
            },
            "moss": {
                "repo": "moss",
                "revision": "2" * 40,
                "path": str(root / "moss-model"),
            },
        },
        "chunking": {"qwen_seconds": 1200, "moss_seconds": 1200},
    }


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.input = self.root / "input.wav"
        self.input.write_bytes(b"audio")
        self.old_cache = os.environ.get("AUDIO_TRANSCRIPTION_CACHE_ROOT")
        self.old_app = os.environ.get("AUDIO_TRANSCRIPTION_APP_ROOT")
        self.old_storage = os.environ.get("AUDIO_TRANSCRIPTION_STORAGE_CONFIG")
        os.environ["AUDIO_TRANSCRIPTION_CACHE_ROOT"] = str(self.root / "cache")
        os.environ["AUDIO_TRANSCRIPTION_APP_ROOT"] = str(self.root / "app")
        os.environ["AUDIO_TRANSCRIPTION_STORAGE_CONFIG"] = str(
            self.root / "storage.json"
        )
        (self.root / "app").mkdir()

    def tearDown(self):
        if self.old_cache is None:
            os.environ.pop("AUDIO_TRANSCRIPTION_CACHE_ROOT", None)
        else:
            os.environ["AUDIO_TRANSCRIPTION_CACHE_ROOT"] = self.old_cache
        if self.old_app is None:
            os.environ.pop("AUDIO_TRANSCRIPTION_APP_ROOT", None)
        else:
            os.environ["AUDIO_TRANSCRIPTION_APP_ROOT"] = self.old_app
        if self.old_storage is None:
            os.environ.pop("AUDIO_TRANSCRIPTION_STORAGE_CONFIG", None)
        else:
            os.environ["AUDIO_TRANSCRIPTION_STORAGE_CONFIG"] = self.old_storage
        self.temporary.cleanup()

    @staticmethod
    def media(_):
        return {"duration_seconds": 10, "size_bytes": 5, "selected_audio_stream": 0}

    @staticmethod
    def transcode(_, destination, __):
        destination.write_bytes(b"wav")

    @staticmethod
    def ok_model(name):
        def run(_, __, directory, *args):
            directory.mkdir(parents=True, exist_ok=True)
            (directory / "raw.json").write_text(
                json.dumps({"text": name, "segments": []})
            )
            (directory / "transcript.txt").write_text(name + "\n")
            return {"status": "success", "characters": len(name), "segments": 0}

        return run

    def patches(self):
        return (
            patch("audio_transcription.pipeline.probe", self.media),
            patch(
                "audio_transcription.pipeline.load_active",
                return_value=active(self.root),
            ),
            patch("audio_transcription.pipeline.transcode_wav", self.transcode),
            patch("audio_transcription.pipeline._run_qwen", self.ok_model("QWEN")),
            patch("audio_transcription.pipeline._run_moss", self.ok_model("MOSS")),
        )

    def test_default_is_sequential_and_writes_independent_markdown(self):
        managers = self.patches()
        with managers[0], managers[1], managers[2], managers[3], managers[4]:
            result = pipeline.transcribe(
                self.input,
                output_dir=self.root / "out",
                language="auto",
                parallel=False,
                require_all=False,
                no_cache=True,
            )
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["execution"]["strategy"], "sequential")
        self.assertEqual(result["execution"]["input_scope"], "single-media")
        self.assertEqual(result["execution"]["cross_file_strategy"], "serialized")
        self.assertIn("queue_wait_seconds", result["execution"])
        text = (self.root / "out" / "transcript.md").read_text()
        self.assertIn("## Qwen3-ASR", text)
        self.assertIn("## MOSS-Transcribe-Diarize", text)
        self.assertIn("not merged", text)

    def test_single_model_failure_is_partial(self):
        managers = self.patches()
        failed = patch(
            "audio_transcription.pipeline._run_moss",
            return_value={
                "status": "failed",
                "error_code": "MODEL_FAILED",
                "message": "boom",
            },
        )
        with managers[0], managers[1], managers[2], managers[3], failed:
            result = pipeline.transcribe(
                self.input,
                output_dir=self.root / "partial",
                language="auto",
                parallel=False,
                require_all=False,
                no_cache=True,
            )
        self.assertEqual(result["status"], "partial")
        self.assertIn("FAILED", (self.root / "partial" / "transcript.md").read_text())

    def test_require_all_rejects_partial_but_keeps_artifacts(self):
        managers = self.patches()
        failed = patch(
            "audio_transcription.pipeline._run_moss",
            return_value={
                "status": "failed",
                "error_code": "MODEL_FAILED",
                "message": "boom",
            },
        )
        with (
            managers[0],
            managers[1],
            managers[2],
            managers[3],
            failed,
            self.assertRaisesRegex(CliError, "--require-all"),
        ):
            pipeline.transcribe(
                self.input,
                output_dir=self.root / "strict",
                language="auto",
                parallel=False,
                require_all=True,
                no_cache=True,
            )
        self.assertTrue((self.root / "strict" / "manifest.json").is_file())

    def test_low_memory_profile_rejects_parallel(self):
        value = active(self.root)
        value["profile"] = "low-memory"
        with (
            patch("audio_transcription.pipeline.probe", self.media),
            patch("audio_transcription.pipeline.load_active", return_value=value),
            self.assertRaisesRegex(CliError, "disabled"),
        ):
            pipeline.plan(self.input, language="auto", parallel=True, no_cache=True)

    def test_plan_does_not_create_cache_root(self):
        value = active(self.root)
        cache_root = Path(os.environ["AUDIO_TRANSCRIPTION_CACHE_ROOT"])
        with (
            patch("audio_transcription.pipeline.probe", self.media),
            patch("audio_transcription.pipeline.load_active", return_value=value),
        ):
            result = pipeline.plan(
                self.input, language="auto", parallel=False, no_cache=False
            )
        self.assertEqual(result["status"], "ready")
        self.assertFalse(cache_root.exists())

    def test_model_process_environment_is_forced_offline(self):
        environment = pipeline._offline_env()
        for name in (
            "HF_HUB_OFFLINE",
            "TRANSFORMERS_OFFLINE",
            "HF_DATASETS_OFFLINE",
            "HF_HUB_DISABLE_TELEMETRY",
            "DO_NOT_TRACK",
        ):
            self.assertEqual(environment[name], "1")
        self.assertEqual(environment["TOKENIZERS_PARALLELISM"], "false")

    def test_concurrent_transcription_waits_for_shared_lock(self):
        with (
            patch(
                "audio_transcription.pipeline.fcntl.flock",
                side_effect=[BlockingIOError(), None],
            ) as flock,
            patch(
                "audio_transcription.pipeline.time.monotonic", side_effect=[1.0, 2.25]
            ),
            patch("audio_transcription.pipeline.print") as report,
            pipeline.transcription_lock() as waited,
        ):
            self.assertEqual(waited, 1.25)
        self.assertEqual(
            flock.call_args_list,
            [
                call(ANY, fcntl.LOCK_EX | fcntl.LOCK_NB),
                call(ANY, fcntl.LOCK_EX),
            ],
        )
        report.assert_called_once()

    def test_symlink_transcription_lock_is_rejected(self):
        lock_path = self.root / "app" / ".transcription.lock"
        lock_path.symlink_to(self.input)
        with (
            self.assertRaisesRegex(CliError, "lock safely"),
            pipeline.transcription_lock(),
        ):
            self.fail("unsafe lock unexpectedly acquired")


if __name__ == "__main__":
    unittest.main()
