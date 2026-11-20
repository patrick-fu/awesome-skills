#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Manage the optional local Apple Silicon MLX TTS + ForcedAligner runtime."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = SKILL_ROOT / "runtime"
LOCK_FILE = RUNTIME_DIR / "models.lock.json"


def config_dir() -> Path:
    override = os.environ.get("MOTION_EXPLAINER_CONFIG_DIR")
    if override:
        return Path(override).expanduser().resolve()
    return Path.home() / "Library" / "Application Support" / "motion-explainer"


def storage_file() -> Path:
    return config_dir() / "storage.json"


def load_lock() -> dict:
    return json.loads(LOCK_FILE.read_text(encoding="utf-8"))


def default_storage() -> dict:
    base = config_dir()
    return {
        "schema_version": 1,
        "app_root": str(base / "runtime"),
        "cache_root": str(base / "cache"),
        "configured": False,
    }


def load_storage() -> dict:
    path = storage_file()
    if not path.is_file():
        return default_storage()
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not data.get("app_root") or not data.get("cache_root"):
        raise ValueError(f"Invalid storage configuration in {path}")
    return {
        "schema_version": 1,
        "app_root": str(Path(data["app_root"]).expanduser().resolve()),
        "cache_root": str(Path(data["cache_root"]).expanduser().resolve()),
        "configured": True,
    }


def active_runtime_file(storage: dict | None = None) -> Path:
    cfg = storage or load_storage()
    return Path(cfg["app_root"]) / "active-runtime.json"


def unified_memory_gib() -> float | None:
    if platform.system() != "Darwin":
        return None
    try:
        raw = subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True).strip()
        return round(int(raw) / (1024 ** 3), 1)
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def is_apple_silicon() -> bool:
    return platform.system() == "Darwin" and platform.machine() == "arm64"


def resolve_ready_runtime() -> dict | None:
    try:
        storage = load_storage()
        meta_path = active_runtime_file(storage)
        if not meta_path.is_file():
            return None
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        lock = load_lock()
        if meta.get("runtime_version") != lock["runtime_version"]:
            return None
        python_bin = Path(meta.get("python", ""))
        tts_dir = Path(meta.get("tts_model_dir", ""))
        align_dir = Path(meta.get("aligner_model_dir", ""))
        if not (python_bin.is_file() and tts_dir.is_dir() and align_dir.is_dir()):
            return None
        return {
            "runtime_version": meta["runtime_version"],
            "python": str(python_bin),
            "hf_home": meta["hf_home"],
            "tts_model_dir": str(tts_dir),
            "aligner_model_dir": str(align_dir),
            "storage": storage,
        }
    except (OSError, ValueError, KeyError):
        return None


def inspect_host() -> dict:
    lock = load_lock()
    storage = load_storage()
    supported = is_apple_silicon()
    mem_gib = unified_memory_gib()
    tools = {name: shutil.which(name) for name in ["uv", "ffmpeg", "ffprobe"]}
    ready = resolve_ready_runtime()
    status = "UNSUPPORTED_PLATFORM" if not supported else ("READY" if ready else "SETUP_REQUIRED")
    warnings = []
    if not supported:
        warnings.append("Local Qwen3-TTS MLX runtime requires macOS Apple Silicon (arm64).")
    elif mem_gib is not None and mem_gib < lock["minimum_memory_gib"]:
        warnings.append(
            f"Detected {mem_gib} GiB unified memory; recommended minimum is {lock['minimum_memory_gib']} GiB "
            f"(peak GPU memory is ~{lock['estimated_peak_gpu_gib']} GiB)."
        )
    missing_tools = [name for name, path in tools.items() if not path]
    if missing_tools:
        warnings.append(f"Missing required host tools: {', '.join(missing_tools)}")
    return {
        "status": status,
        "platform": {"system": platform.system(), "machine": platform.machine(), "apple_silicon": supported},
        "unified_memory_gib": mem_gib,
        "minimum_memory_gib": lock["minimum_memory_gib"],
        "estimated_disk_gib": lock["estimated_disk_gib"],
        "estimated_peak_gpu_gib": lock["estimated_peak_gpu_gib"],
        "runtime_version": lock["runtime_version"],
        "models": lock["models"],
        "tools": tools,
        "storage": storage,
        "active_runtime": ready,
        "warnings": warnings,
    }


def configure_storage(app_root: Path, cache_root: Path) -> dict:
    app = app_root.expanduser().resolve()
    cache = cache_root.expanduser().resolve()
    if app == cache or app in cache.parents or cache in app.parents:
        raise ValueError("app-root and cache-root must be distinct, non-overlapping directories")
    cfg_dir = config_dir()
    cfg_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "app_root": str(app),
        "cache_root": str(cache),
    }
    storage_file().write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {**payload, "configured": True, "config_file": str(storage_file())}


def run_step(cmd: list[str], *, env: dict | None = None) -> str:
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()[-2500:]
        raise RuntimeError(f"Command failed ({' '.join(cmd[:4])}): {detail}")
    return proc.stdout


def setup_runtime(force: bool = False) -> dict:
    if not is_apple_silicon():
        raise RuntimeError("Local Qwen3-TTS MLX runtime is supported only on macOS Apple Silicon (arm64).")
    for tool in ["uv", "ffmpeg", "ffprobe"]:
        if not shutil.which(tool):
            raise RuntimeError(f"Missing required tool: {tool}")
    lock = load_lock()
    storage = load_storage()
    if not force:
        existing = resolve_ready_runtime()
        if existing:
            return {"status": "READY", "reused": True, **existing}
    app_root = Path(storage["app_root"])
    cache_root = Path(storage["cache_root"])
    venv_dir = app_root / "venvs" / lock["runtime_version"]
    hf_home = cache_root / "huggingface"
    uv_cache = cache_root / "uv"
    for directory in [app_root / "venvs", hf_home, uv_cache]:
        directory.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["UV_CACHE_DIR"] = str(uv_cache)
    env["HF_HOME"] = str(hf_home)

    python_bin = venv_dir / "bin" / "python"
    if force or not python_bin.is_file():
        run_step(["uv", "venv", str(venv_dir), "--python", lock["python"], "--clear"], env=env)
    req_file = RUNTIME_DIR / lock["requirements_in"]
    run_step(["uv", "pip", "install", "--python", str(python_bin), "-r", str(req_file)], env=env)

    # Download exact pinned snapshots and verify MLX GPU availability
    download_code = (
        "import json, sys; from huggingface_hub import snapshot_download; "
        "import mlx.core as mx, mlx_audio; "
        "tts = snapshot_download(sys.argv[1], revision=sys.argv[2]); "
        "align = snapshot_download(sys.argv[3], revision=sys.argv[4]); "
        "print(json.dumps({'tts_model_dir': tts, 'aligner_model_dir': align, 'device': str(mx.default_device())}))"
    )
    out = run_step([
        str(python_bin), "-c", download_code,
        lock["models"]["tts"]["repo"], lock["models"]["tts"]["revision"],
        lock["models"]["aligner"]["repo"], lock["models"]["aligner"]["revision"],
    ], env=env)
    resolved = json.loads(out.strip().splitlines()[-1])

    meta = {
        "schema_version": 1,
        "runtime_version": lock["runtime_version"],
        "python": str(python_bin),
        "hf_home": str(hf_home),
        "tts_model_dir": resolved["tts_model_dir"],
        "aligner_model_dir": resolved["aligner_model_dir"],
        "device": resolved["device"],
    }
    meta_path = active_runtime_file(storage)
    tmp_path = meta_path.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp_path.replace(meta_path)
    return {"status": "READY", "reused": False, **meta}


def doctor_runtime() -> dict:
    info = inspect_host()
    ready = info["active_runtime"]
    if not ready:
        return {"ok": False, "status": info["status"], "warnings": info["warnings"], "storage": info["storage"]}
    env = os.environ.copy()
    env["HF_HOME"] = ready["hf_home"]
    probe = run_step([
        ready["python"], "-c",
        "import json, mlx.core as mx, mlx_audio; print(json.dumps({'mlx_audio': getattr(mlx_audio, '__version__', 'installed'), 'device': str(mx.default_device())}))"
    ], env=env)
    details = json.loads(probe.strip().splitlines()[-1])
    return {"ok": True, "status": "READY", **ready, **details}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Manage motion-explainer's local Qwen3-TTS MLX runtime")
    sub = parser.add_subparsers(dest="command", required=True)

    p_inspect = sub.add_parser("inspect", help="Inspect host readiness, memory, storage, and download estimate")
    p_inspect.add_argument("--json", action="store_true", help="Emit JSON output")

    p_storage = sub.add_parser("storage", help="Read or configure local runtime storage roots")
    storage_sub = p_storage.add_subparsers(dest="storage_cmd", required=True)
    p_st_status = storage_sub.add_parser("status", help="Show current storage directories")
    p_st_status.add_argument("--json", action="store_true")
    p_st_cfg = storage_sub.add_parser("configure", help="Persist custom app-root and cache-root directories")
    p_st_cfg.add_argument("--app-root", type=Path, required=True)
    p_st_cfg.add_argument("--cache-root", type=Path, required=True)
    p_st_cfg.add_argument("--json", action="store_true")

    p_setup = sub.add_parser("setup", help="Create isolated MLX venv and download pinned Qwen3-TTS + ForcedAligner models")
    p_setup.add_argument("--force", action="store_true", help="Reinstall runtime environment and re-verify snapshots")
    p_setup.add_argument("--json", action="store_true")

    p_doctor = sub.add_parser("doctor", help="Verify installed local MLX runtime and pinned model snapshots")
    p_doctor.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            result = inspect_host()
        elif args.command == "storage":
            if args.storage_cmd == "status":
                result = load_storage()
            else:
                result = configure_storage(args.app_root, args.cache_root)
        elif args.command == "setup":
            result = setup_runtime(force=args.force)
        else:
            result = doctor_runtime()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.command == "doctor" and not result.get("ok"):
            return 1
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
