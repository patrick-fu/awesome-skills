#!/usr/bin/env python3
"""colab_asr_runner — VM-side ASR runner for colab-transcribe (dual engine).

Executed on the Colab VM via `colab exec`. Reads a plan JSON:
  {"engine": "turbo"|"qwen17", "model": <repo/size>, "language": null,
   "out_dir": "/content/asr_out",
   "files": [{"id", "base", "source_name", "remote_path"}]}

engines:
  turbo  — faster-whisper, whole-file, segment-level SRT. Needs the pinned
           faster-whisper + nvidia wheels installed by the CLI beforehand.
  qwen17 — Qwen3-ASR-1.7B via the official `qwen-asr` package. Long audio MUST
           be windowed: whole-file input loses content (package-internal
           chunking drops middle/tail chunks; measured 2026-11-20). We cut
           silence-aligned windows <=60s (target 45s, hard-cut fallback) and
           batch-transcribe them. SRT granularity = one entry per window
           (character-level timestamps are the ForcedAligner's job; not wired).

Writes per-file .txt/.srt/.json plus result.json (the only trusted result —
stdout may be polluted by CLI banners). Progress goes to stderr.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

QWEN17_MODEL = "Qwen/Qwen3-ASR-1.7B"


class RunnerError(Exception):
    def __init__(self, code, detail):
        super().__init__(detail)
        self.code = code
        self.detail = detail


def fmt_srt_ts(seconds):
    ms = int(round(seconds * 1000))
    h, rem = divmod(ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(path, segments):
    with open(path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            f.write(f"{i}\n{fmt_srt_ts(seg['start'])} --> {fmt_srt_ts(seg['end'])}\n{seg['text'].strip()}\n\n")


def preload_cuda():
    """pip 的 nvidia-*-cu12 wheel 不在默认 ld 路径，bash 子进程也没有 kernel 的
    LD_LIBRARY_PATH。import ctranslate2 前用 RTLD_GLOBAL 显式预加载。"""
    import ctypes
    import glob
    import site

    patterns = []
    for sp in list(dict.fromkeys(site.getsitepackages() + [site.getusersitepackages()])):
        patterns += [os.path.join(sp, "nvidia", "cublas", "lib", "libcublas.so*"),
                     os.path.join(sp, "nvidia", "cudnn", "lib", "libcudnn*.so*")]
    patterns += ["/usr/local/cuda/lib64/libcublas.so*", "/usr/local/cuda/lib64/libcudnn*"]
    loaded = 0
    for pat in patterns:
        for so in sorted(glob.glob(pat)):
            try:
                ctypes.CDLL(so, mode=ctypes.RTLD_GLOBAL)
                loaded += 1
            except OSError:
                pass
    print(f"[runner] cuda preload: {loaded} libs", file=sys.stderr, flush=True)


def sh(argv, timeout=600):
    return subprocess.run(argv, capture_output=True, text=True, timeout=timeout)


def probe_duration(path):
    r = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], timeout=120)
    try:
        return float(r.stdout.strip())
    except ValueError:
        raise RunnerError("FFPROBE_FAILED", f"cannot probe duration: {path}")


def parse_silences(ffmpeg_log, media_duration):
    """Parse ffmpeg silencedetect stderr into [(start, end)].

    A trailing silence_start with no silence_end (audio ends while silent) is
    closed at media_duration."""
    silences = []
    start = None
    for m in re.finditer(r"silence_(start|end):\s*([0-9.]+)", ffmpeg_log):
        kind, val = m.group(1), float(m.group(2))
        if kind == "start":
            start = val
        elif start is not None:
            silences.append((start, min(val, media_duration)))
            start = None
    if start is not None and start < media_duration:
        silences.append((start, media_duration))
    return silences


def plan_windows(duration, silences, target_s=45.0, max_s=60.0):
    """Silence-midpoint-aligned greedy packing. Returns [(start, end)].

    Cut points are 0, silence midpoints, duration. From the current position we
    take the farthest cut within max_s, preferring one at or beyond target_s.
    A speech stretch longer than max_s with no usable cut is hard-cut at max_s
    (quality cost noted in reference; unavoidable for continuous speech).
    """
    if duration <= max_s:
        return [(0.0, duration)]
    cuts = [0.0] + [min((a + b) / 2.0, duration) for a, b in silences if 0 < (a + b) / 2.0 < duration] + [duration]
    cuts = sorted(set(round(c, 3) for c in cuts))
    windows = []
    cur = 0.0
    while duration - cur > max_s:
        reachable = [c for c in cuts if cur < c <= cur + max_s]
        pick = None
        for c in reachable:  # farthest first
            if c >= cur + target_s:
                pick = c
        if pick is None:
            pick = max(reachable) if reachable else cur + max_s
        windows.append((cur, pick))
        cur = pick
    windows.append((cur, duration))
    return [(round(a, 3), round(b, 3)) for a, b in windows if b - a > 0.05]


def transcribe_turbo(plan, item, out_dir):
    from faster_whisper import WhisperModel

    model_size = plan.get("model", "large-v3-turbo")
    language = plan.get("language") or None
    t0 = time.time()
    print(f"[runner] loading faster-whisper model={model_size} device=cuda", file=sys.stderr, flush=True)
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    print(f"[runner] model loaded in {time.time() - t0:.1f}s", file=sys.stderr, flush=True)
    return model, language


def run_turbo_file(model, language, item, out_dir):
    media, base = item["remote_path"], item["base"]
    t1 = time.time()
    print(f"[runner] transcribing {media}", file=sys.stderr, flush=True)
    segments_iter, info = model.transcribe(media, language=language, vad_filter=True)
    segments = [{"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text}
                for s in segments_iter]
    text = "".join(s["text"] for s in segments).strip()
    return {"duration_s": round(info.duration, 3), "language": getattr(info, "language", None),
            "language_probability": round(getattr(info, "language_probability", 0.0), 4),
            "segments": segments, "text": text, "infer_s": round(time.time() - t1, 1)}


def run_qwen17_file(model, item, out_dir, language=None):
    media, base = item["remote_path"], item["base"]
    duration = probe_duration(media)
    t1 = time.time()
    sil = sh(["ffmpeg", "-i", media, "-af", "silencedetect=noise=-30dB:d=0.4", "-f", "null", "-"],
             timeout=600)
    silences = parse_silences(sil.stderr or "", duration)
    windows = plan_windows(duration, silences)
    print(f"[runner] qwen17 {media}: {duration:.1f}s -> {len(windows)} windows "
          f"({len(silences)} silences)", file=sys.stderr, flush=True)
    work = os.path.join(out_dir, "work")
    os.makedirs(work, exist_ok=True)
    win_paths, win_metas = [], []
    for wi, (a, b) in enumerate(windows):
        wp = os.path.join(work, f"{base}_w{wi:03d}.wav")
        r = sh(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(a), "-t", str(round(b - a, 3)),
                "-i", media, "-ar", "16000", "-ac", "1", wp], timeout=300)
        if not os.path.exists(wp) or os.path.getsize(wp) == 0:
            raise RunnerError("WINDOW_FAILED", f"window cut failed: {wp} :: {(r.stderr or '')[-200:]}")
        win_paths.append(wp)
        win_metas.append((a, b))
    results = model.transcribe(audio=win_paths, language=language)
    segments, text_parts = [], []
    for (a, b), r in zip(win_metas, results):
        text = (getattr(r, "text", "") or "").strip()
        text_parts.append(text)
        segments.append({"start": round(a, 3), "end": round(b, 3), "text": text,
                         "language": getattr(r, "language", None)})
    for wp in win_paths:
        try:
            os.remove(wp)
        except OSError:
            pass
    return {"duration_s": round(duration, 3), "language": next(
        (s["language"] for s in segments if s.get("language")), None),
        "segments": segments, "text": "".join(text_parts).strip(),
        "infer_s": round(time.time() - t1, 1), "windows": len(windows)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    args = ap.parse_args()
    with open(args.plan, "r", encoding="utf-8") as f:
        plan = json.load(f)
    out_dir = plan["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    engine = plan.get("engine", "turbo")

    results = []
    shared_model = None
    try:
        if engine == "turbo":
            preload_cuda()
            shared_model, language = transcribe_turbo(plan, None, out_dir)
        elif engine == "qwen17":
            import torch
            from qwen_asr import Qwen3ASRModel

            t0 = time.time()
            print(f"[runner] loading {QWEN17_MODEL} fp16 device=cuda", file=sys.stderr, flush=True)
            shared_model = Qwen3ASRModel.from_pretrained(
                QWEN17_MODEL, dtype=torch.float16, device_map="cuda",
                max_new_tokens=1024, max_inference_batch_size=16)
            language = plan.get("language") or None
            print(f"[runner] qwen17 loaded in {time.time() - t0:.1f}s", file=sys.stderr, flush=True)
        else:
            raise RunnerError("UNKNOWN_ENGINE", f"engine not supported: {engine}")

        for item in plan["files"]:
            entry = {"id": item["id"], "media": item["remote_path"], "status": "failed",
                     "error_code": None}
            try:
                if engine == "turbo":
                    r = run_turbo_file(shared_model, language, item, out_dir)
                else:
                    r = run_qwen17_file(shared_model, item, out_dir, language)
                text = r.pop("text")
                txt_path = os.path.join(out_dir, item["base"] + ".txt")
                srt_path = os.path.join(out_dir, item["base"] + ".srt")
                js_path = os.path.join(out_dir, item["base"] + ".json")
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text + "\n")
                write_srt(srt_path, r["segments"])
                with open(js_path, "w", encoding="utf-8") as f:
                    json.dump({"media": item["source_name"], "engine": engine,
                               "model": plan.get("model") or (QWEN17_MODEL if engine == "qwen17" else None),
                               **r, "text_chars": len(text), "segments": r["segments"]},
                              f, ensure_ascii=False, indent=1)
                entry.update({
                    "status": "ok", "duration_s": r["duration_s"], "language": r.get("language"),
                    "text_chars": len(text), "segment_count": len(r["segments"]),
                    "infer_s": r["infer_s"],
                    "artifacts": {"txt": os.path.basename(txt_path), "srt": os.path.basename(srt_path),
                                  "json": os.path.basename(js_path)},
                })
                print(f"[runner] ok {item['remote_path']}: {len(r['segments'])} segs, "
                      f"{r['duration_s']}s audio in {r['infer_s']}s", file=sys.stderr, flush=True)
            except RunnerError as e:
                entry["error_code"] = e.code
                entry["detail"] = e.detail[:500]
                print(f"[runner] FAILED {item['remote_path']}: {e}", file=sys.stderr, flush=True)
            except Exception as e:  # noqa: BLE001 - per-file isolation into result.json
                entry["error_code"] = "REMOTE_INFER_FAILED"
                entry["detail"] = repr(e)[:500]
                print(f"[runner] FAILED {item['remote_path']}: {e!r}", file=sys.stderr, flush=True)
            results.append(entry)
    except Exception as e:  # noqa: BLE001 - fatal: engine load failed, nothing transcribed
        result = {"status": "error", "error_code": "ENGINE_LOAD_FAILED",
                  "detail": repr(e)[:500], "engine": engine, "files": []}
        with open(os.path.join(out_dir, "result.json"), "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=1)
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(3)

    result = {"status": "ok" if all(r["status"] == "ok" for r in results) else
              ("failed" if all(r["status"] != "ok" for r in results) else "partial"),
              "engine": engine, "model": plan.get("model") or (QWEN17_MODEL if engine == "qwen17" else None),
              "language": plan.get("language"), "files": results}
    with open(os.path.join(out_dir, "result.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
