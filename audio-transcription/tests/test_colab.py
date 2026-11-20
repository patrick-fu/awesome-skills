from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def _load(name, filename):
    path = ROOT / "scripts" / filename
    if filename.endswith(".py"):
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    from importlib.machinery import SourceFileLoader

    loader = SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_file_location(name, str(path), loader=loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


runner = _load("colab_asr_runner", "colab_asr_runner.py")
cli = _load("colab_transcribe_cli", "colab-transcribe")


class SilenceParsingTests(unittest.TestCase):
    def test_parse_silences_pairs_start_end(self):
        log = (
            "[silencedetect @ 0.5s] silence_start: 1.2\n"
            "[silencedetect @ 2.0s] silence_end: 1.6 | silence_duration: 0.4\n"
            "[silencedetect @ 9.0s] silence_start: 8.4\n"
        )
        self.assertEqual(runner.parse_silences(log, 10.0), [(1.2, 1.6), (8.4, 10.0)])

    def test_parse_silences_empty_log(self):
        self.assertEqual(runner.parse_silences("no markers here", 30.0), [])


class PlanWindowsTests(unittest.TestCase):
    def test_short_duration_single_window(self):
        self.assertEqual(runner.plan_windows(45.0, []), [(0.0, 45.0)])

    def test_windows_cut_at_silence_midpoints(self):
        duration = 180.0
        silences = [(43.0, 45.0), (90.0, 92.0)]
        windows = runner.plan_windows(duration, silences)
        # 91->180 为 89s，超过 60s 上限，在 151 处硬切
        self.assertEqual(windows, [(0.0, 44.0), (44.0, 91.0), (91.0, 151.0), (151.0, 180.0)])

    def test_windows_respect_max_and_cover_all(self):
        duration = 300.0
        silences = [(50.0, 52.0), (101.0, 103.0), (160.0, 161.0), (220.0, 222.0)]
        windows = runner.plan_windows(duration, silences)
        covered = 0.0
        for a, b in windows:
            self.assertLessEqual(b - a, 60.0 + 1e-6)
            self.assertAlmostEqual(a, covered, places=2)
            covered = b
        self.assertAlmostEqual(covered, duration, places=2)
        self.assertGreater(len(windows), 1)

    def test_continuous_speech_hard_cut(self):
        windows = runner.plan_windows(150.0, [])
        self.assertEqual(windows, [(0.0, 60.0), (60.0, 120.0), (120.0, 150.0)])

    def test_silence_far_beyond_max_ignored(self):
        windows = runner.plan_windows(120.0, [(118.0, 119.0)])
        self.assertEqual(windows, [(0.0, 60.0), (60.0, 120.0)])


class CliHelpersTests(unittest.TestCase):
    def test_parse_usage(self):
        text = (
            "Current balance: 2470.31 compute units\n"
            "Usage rate: 1.94/hr\n"
            "Active assignments: 2\n"
        )
        self.assertEqual(
            cli.parse_usage(text),
            {"balance": 2470.31, "rate_per_hr": 1.94, "assignments": 2},
        )

    def test_parse_usage_garbled_returns_nones(self):
        self.assertEqual(
            cli.parse_usage("backend exploded"),
            {"balance": None, "rate_per_hr": None, "assignments": None},
        )

    def test_resolve_model(self):
        self.assertEqual(cli.resolve_model("turbo", "large-v3"), "large-v3")
        self.assertEqual(cli.resolve_model("turbo", "large-v3-turbo"), "large-v3-turbo")
        self.assertEqual(cli.resolve_model("qwen17", "large-v3"), cli.QWEN17_MODEL)

    def test_est_infer_s_conservative(self):
        # 保守系数：qwen17 8x、turbo 15x（实测 17.7-34x）
        self.assertAlmostEqual(cli.est_infer_s(160, "qwen17", cli.QWEN17_MODEL), 20.0)
        self.assertAlmostEqual(cli.est_infer_s(160, "turbo", "large-v3-turbo"), 160 / 15)

    def test_engine_dependent_install_lists(self):
        self.assertIn("av>=12,<14", cli.INSTALL_LISTS["turbo"])
        self.assertEqual(cli.INSTALL_LISTS["qwen17"], ["qwen-asr"])

    def test_default_session_machine_scoped_and_sanitized(self):
        name = cli.DEFAULT_SESSION
        self.assertTrue(name.startswith("asr-"))
        self.assertRegex(name, r"^asr-[a-z0-9-]+$")
        self.assertEqual(cli.default_session_name(), name)  # 稳定，随机性为零

    def test_default_session_distinguishes_real_hosts(self):
        # 真实双机主机名（[:10] 截断曾使两者同为 asr-patricks-m——回归守卫）
        mini = cli.default_session_name("Patricks-Mac-mini.local")
        mbp = cli.default_session_name("Patricks-MacBook-Pro.local")
        self.assertEqual(mini, "asr-patricks-mac-mini")
        self.assertEqual(mbp, "asr-patricks-macbook")
        self.assertNotEqual(mini, mbp)

    def test_default_session_fallback_on_blank(self):
        self.assertEqual(cli.default_session_name("   "), "asr-local")


if __name__ == "__main__":
    unittest.main()
