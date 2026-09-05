#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fcntl
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from audio_transcription import __version__, cache
from audio_transcription.config import (
    SKILL_ROOT,
    active_config_path,
    app_root,
    configure_storage,
    load_active,
    load_lock,
    reset_storage,
    storage_status,
    temp_root,
    write_bootstrap_active_python,
    write_json_atomic,
)
from audio_transcription.errors import CliError

SCRIPTS = SKILL_ROOT / "scripts"
CLI_MARKER = "# audio-transcription-managed-launcher:v1"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def memory_gib() -> float | None:
    try:
        completed = subprocess.run(
            ["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, check=True
        )
        return round(int(completed.stdout.strip()) / 1024**3, 1)
    except (OSError, ValueError, subprocess.CalledProcessError):
        return None


def disk_free_gib(path: Path | None = None) -> float:
    candidate = path or app_root()
    while not candidate.exists() and candidate != candidate.parent:
        candidate = candidate.parent
    return round(shutil.disk_usage(candidate).free / 1024**3, 1)


def _is_in_path(path: Path) -> bool:
    resolved = path.expanduser().resolve(strict=False)
    return any(
        Path(item).expanduser().resolve(strict=False) == resolved
        for item in os.environ.get("PATH", "").split(os.pathsep)
        if item
    )


def _candidate(path: Path) -> dict[str, Any]:
    expanded = path.expanduser()
    parent = expanded if expanded.exists() else expanded.parent
    return {
        "path": str(expanded),
        "exists": expanded.is_dir(),
        "in_path": _is_in_path(expanded),
        "writable": os.access(parent, os.W_OK),
    }


def inspect() -> dict[str, Any]:
    lock = load_lock()
    memory = memory_gib()
    recommendation = (
        "standard"
        if memory is not None
        and memory >= lock["profiles"]["standard"]["minimum_memory_gib"]
        else "low-memory"
    )
    candidates = [
        _candidate(Path("~/bin")),
        _candidate(Path("~/.local/bin")),
        _candidate(Path("/usr/local/bin")),
    ]
    recommended_bin = next(
        (
            item["path"]
            for item in candidates
            if item["exists"] and item["in_path"] and item["writable"]
        ),
        None,
    )
    if recommended_bin is None:
        recommended_bin = str(Path("~/.local/bin").expanduser())
    active = load_active(require_complete=False)
    missing = [name for name in ("uv", "ffmpeg", "ffprobe") if not shutil.which(name)]
    estimated_download = 4.5 if recommendation == "low-memory" else 6.0
    return {
        "status": "ready",
        "host": {
            "system": platform.system(),
            "machine": platform.machine(),
            "memory_gib": memory,
            "disk_free_gib": disk_free_gib(),
            "supported": platform.system() == "Darwin"
            and platform.machine() == "arm64",
        },
        "runtime": {"active": active, "lock_version": lock["runtime_version"]},
        "storage": storage_status(),
        "dependencies": {"missing": missing, "homebrew": shutil.which("brew")},
        "profile": {
            "recommended": recommendation,
            "requires_user_decision": recommendation == "low-memory",
            "reason": "Unified memory is below the standard profile threshold."
            if recommendation == "low-memory"
            else "Unified memory meets the standard profile threshold.",
            "estimated_download_gib": estimated_download,
            "minimum_free_disk_gib_for_setup": 10
            if recommendation == "low-memory"
            else 12,
        },
        "cli_install": {
            "default": "not-installed",
            "recommended_bin_dir": recommended_bin,
            "candidates": candidates,
        },
    }


def _prepare_app_root() -> Path:
    root = app_root()
    if root.is_symlink():
        raise CliError(
            "RUNTIME_SAFETY_ERROR",
            f"Application Support root must not be a symlink: {root}",
        )
    root.mkdir(parents=True, exist_ok=True)
    if root.is_symlink() or not root.is_dir():
        raise CliError(
            "RUNTIME_SAFETY_ERROR",
            f"Application Support root must be a normal directory: {root}",
        )
    os.chmod(root, 0o700)
    return root


@contextmanager
def setup_lock(root: Path) -> Iterator[None]:
    lock_file = root / ".setup.lock"
    with lock_file.open("a+", encoding="utf-8") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise CliError(
                "SETUP_ALREADY_RUNNING", "Another runtime setup is already running."
            ) from exc
        yield


def run(command: list[str], *, env: dict[str, str] | None = None) -> None:
    completed = subprocess.run(
        command, text=True, capture_output=True, check=False, env=env
    )
    if completed.returncode:
        detail = (
            completed.stderr or completed.stdout or "unknown command failure"
        ).strip()[-4000:]
        raise CliError(
            "SETUP_COMMAND_FAILED", f"Command failed ({command[0]}): {detail}"
        )


def ensure_system_dependencies() -> None:
    missing = [name for name in ("uv", "ffmpeg", "ffprobe") if not shutil.which(name)]
    if not missing:
        return
    brew = shutil.which("brew")
    if not brew:
        raise CliError(
            "SYSTEM_DEPENDENCY_MISSING",
            f"Missing {', '.join(missing)} and Homebrew is unavailable. Setup never installs Homebrew.",
            [
                {
                    "instruction": "Install Homebrew or provide uv, ffmpeg, and ffprobe, then rerun setup."
                }
            ],
            requires_user_decision=True,
        )
    packages = []
    if "uv" in missing:
        packages.append("uv")
    if "ffmpeg" in missing or "ffprobe" in missing:
        packages.append("ffmpeg")
    run([brew, "install", *packages])


def _valid_model(path: Path) -> bool:
    return (
        path.is_dir()
        and not path.is_symlink()
        and (path / "config.json").is_file()
        and (path / "model.safetensors").is_file()
    )


def download_model(python: Path, root: Path, name: str, spec: dict[str, Any]) -> Path:
    repository_name = spec["repo"].replace("/", "--")
    models_root = root / "models"
    if models_root.is_symlink():
        raise CliError(
            "RUNTIME_SAFETY_ERROR", f"Models root must not be a symlink: {models_root}"
        )
    models_root.mkdir(parents=True, exist_ok=True)
    model_parent = models_root / repository_name
    if model_parent.is_symlink():
        raise CliError(
            "RUNTIME_SAFETY_ERROR",
            f"Model directory must not be a symlink: {model_parent}",
        )
    model_parent.mkdir(parents=True, exist_ok=True)
    final = model_parent / spec["revision"]
    if _valid_model(final):
        return final
    if final.exists():
        raise CliError(
            "MODEL_SNAPSHOT_INVALID",
            f"Refusing incomplete existing model path: {final}",
        )
    staging = model_parent / f".{spec['revision']}.staging-{os.getpid()}"
    if staging.exists():
        shutil.rmtree(staging)
    code = (
        "from huggingface_hub import snapshot_download; import sys; "
        "snapshot_download(repo_id=sys.argv[1], revision=sys.argv[2], local_dir=sys.argv[3])"
    )
    try:
        run([str(python), "-c", code, spec["repo"], spec["revision"], str(staging)])
        if not _valid_model(staging):
            raise CliError(
                "MODEL_SNAPSHOT_INVALID",
                f"Downloaded snapshot is incomplete: {spec['repo']}",
            )
        os.replace(staging, final)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return final


def _make_smoke_audio(destination: Path) -> None:
    say = shutil.which("say")
    if not say:
        raise CliError("SMOKE_FAILED", "macOS say command is unavailable.")
    aiff = destination.with_suffix(".aiff")
    run([say, "-o", str(aiff), "Local transcription setup is working correctly."])
    run(
        [
            shutil.which("ffmpeg") or "ffmpeg",
            "-nostdin",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(aiff),
            "-ac",
            "1",
            "-ar",
            "16000",
            "-c:a",
            "pcm_s16le",
            str(destination),
        ]
    )


def smoke(
    python: Path, models: dict[str, dict[str, Any]], profile_spec: dict[str, Any]
) -> None:
    environment = os.environ.copy()
    environment.update(
        {
            "HF_HUB_OFFLINE": "1",
            "TRANSFORMERS_OFFLINE": "1",
            "HF_DATASETS_OFFLINE": "1",
            "HF_HUB_DISABLE_TELEMETRY": "1",
            "TOKENIZERS_PARALLELISM": "false",
        }
    )
    temporary_kwargs = {"dir": temp_root()} if temp_root() else {}
    with tempfile.TemporaryDirectory(
        prefix="audio-transcription-smoke-", **temporary_kwargs
    ) as temporary:
        root = Path(temporary)
        audio = root / "smoke.wav"
        _make_smoke_audio(audio)
        run(
            [
                str(python),
                str(SCRIPTS / "qwen_runner.py"),
                "--model",
                models["qwen"]["path"],
                "--audio",
                str(audio),
                "--output",
                str(root / "qwen.json"),
                "--language",
                "English",
                "--chunk-seconds",
                str(profile_spec["qwen_chunk_seconds"]),
            ],
            env=environment,
        )
        run(
            [
                str(python),
                str(SCRIPTS / "moss_runner.py"),
                "--model",
                models["moss"]["path"],
                "--audio",
                str(audio),
                "--output",
                str(root / "moss.json"),
            ],
            env=environment,
        )
        for name in ("qwen", "moss"):
            try:
                value = json.loads((root / f"{name}.json").read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise CliError(
                    "SMOKE_FAILED", f"{name} smoke output is invalid: {exc}"
                ) from exc
            if not str(value.get("text", "")).strip():
                raise CliError("SMOKE_FAILED", f"{name} smoke output is empty.")


def _write_active_python(root: Path, python: Path) -> None:
    descriptor, name = tempfile.mkstemp(prefix=".active-python.", dir=root)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(str(python) + "\n")
        os.chmod(temporary, 0o600)
        os.replace(temporary, root / "active-python")
    finally:
        temporary.unlink(missing_ok=True)


def setup(profile: str) -> dict[str, Any]:
    lock = load_lock()
    if profile not in lock["profiles"]:
        raise CliError("PROFILE_UNKNOWN", f"Unknown profile: {profile}")
    if platform.system() != "Darwin" or platform.machine() != "arm64":
        raise CliError(
            "UNSUPPORTED_HOST", "Local MLX transcription requires Apple Silicon macOS."
        )
    required_free = 10 if profile == "low-memory" else 12
    available = disk_free_gib()
    if available < required_free:
        raise CliError(
            "INSUFFICIENT_DISK",
            f"Setup requires at least {required_free} GiB free; only {available} GiB is available.",
            requires_user_decision=True,
        )
    root = _prepare_app_root()
    with setup_lock(root):
        ensure_system_dependencies()
        profile_spec = lock["profiles"][profile]
        runtimes = root / "runtimes"
        if runtimes.is_symlink():
            raise CliError(
                "RUNTIME_SAFETY_ERROR",
                f"Runtimes root must not be a symlink: {runtimes}",
            )
        runtimes.mkdir(exist_ok=True)
        final = runtimes / f"{lock['runtime_version']}-{profile}"
        staging = (
            runtimes / f".{lock['runtime_version']}-{profile}.staging-{os.getpid()}"
        )
        if final.exists() and (final / "bin/python").is_file():
            python = final / "bin/python"
        else:
            if final.exists() or staging.exists():
                raise CliError(
                    "RUNTIME_SAFETY_ERROR",
                    f"Refusing incomplete runtime path: {final if final.exists() else staging}",
                )
            run(
                [
                    shutil.which("uv") or "uv",
                    "venv",
                    "--python",
                    lock["python"],
                    str(staging),
                ]
            )
            python = staging / "bin/python"
            requirements = SKILL_ROOT / "runtime" / lock["requirements_lock"]
            run(
                [
                    shutil.which("uv") or "uv",
                    "pip",
                    "install",
                    "--python",
                    str(python),
                    "--requirements",
                    str(requirements),
                ]
            )
        try:
            models = {
                name: {
                    **spec,
                    "path": str(download_model(python, root, name, spec)),
                }
                for name, spec in (
                    ("qwen", profile_spec["qwen"]),
                    ("moss", profile_spec["moss"]),
                )
            }
            run([str(python), "-c", "import mlx, mlx_audio, moss_transcribe_diarize"])
            smoke(python, models, profile_spec)
            if staging.exists():
                os.replace(staging, final)
                python = final / "bin/python"
            active = {
                "schema_version": 1,
                "runtime_version": lock["runtime_version"],
                "installed_at": utc_now(),
                "profile": profile,
                "memory_gib": memory_gib(),
                "runtime_path": str(final),
                "python": str(python),
                "models": models,
                "chunking": {
                    "qwen_seconds": profile_spec["qwen_chunk_seconds"],
                    "moss_seconds": profile_spec["moss_chunk_seconds"],
                },
            }
            write_json_atomic(active_config_path(), active)
            _write_active_python(root, python)
            write_bootstrap_active_python(python)
            return {
                "status": "ready",
                "active": active,
                "network_used": True,
                "upload": False,
            }
        finally:
            if staging.exists():
                shutil.rmtree(staging)


def doctor() -> dict[str, Any]:
    report = inspect()
    checks = [
        {
            "name": "supported host",
            "ok": report["host"]["supported"],
            "value": report["host"],
        },
        {
            "name": "system dependencies",
            "ok": not report["dependencies"]["missing"],
            "value": report["dependencies"],
        },
    ]
    try:
        active = load_active()
        checks.append({"name": "active runtime", "ok": True, "value": active})
        completed = subprocess.run(
            [
                active["python"],
                "-c",
                "import mlx.core as mx; import mlx_audio, moss_transcribe_diarize; print(mx.metal.is_available())",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        checks.append(
            {
                "name": "MLX imports and Metal",
                "ok": completed.returncode == 0 and completed.stdout.strip() == "True",
                "value": (completed.stdout or completed.stderr).strip()[-1000:],
            }
        )
    except CliError as exc:
        checks.append({"name": "active runtime", "ok": False, "value": exc.envelope()})
    ok = all(item["ok"] for item in checks)
    return {
        "status": "ready" if ok else "not_ready",
        "checks": checks,
        "next_actions": []
        if ok
        else [
            {
                "kind": "invoke_skill",
                "instruction": "Invoke $audio-transcription and request setup or repair.",
            }
        ],
    }


def install_cli(bin_dir: Path) -> dict[str, Any]:
    directory = bin_dir.expanduser().resolve(strict=False)
    if directory.exists() and (directory.is_symlink() or not directory.is_dir()):
        raise CliError(
            "CLI_INSTALL_UNSAFE",
            f"Bin directory must be a normal directory: {directory}",
        )
    directory.mkdir(parents=True, exist_ok=True)
    if not os.access(directory, os.W_OK):
        raise CliError(
            "CLI_INSTALL_PERMISSION",
            f"Bin directory is not writable; setup never invokes sudo: {directory}",
        )
    target = directory / "local-transcribe"
    if (target.exists() or target.is_symlink()) and (
        target.is_symlink()
        or not target.is_file()
        or CLI_MARKER not in target.read_text(encoding="utf-8", errors="replace")
    ):
        raise CliError(
            "CLI_ENTRY_EXISTS",
            f"Refusing to overwrite an unknown CLI entry: {target}",
        )
    source = (SCRIPTS / "local-transcribe").resolve()
    content = f'#!/bin/sh\n{CLI_MARKER}\nexec {json.dumps(str(source))} "$@"\n'
    descriptor, name = tempfile.mkstemp(prefix=".local-transcribe.", dir=directory)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        # The managed file is intentionally executable.
        os.chmod(temporary, 0o755)  # nosec B103
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)
    root = _prepare_app_root()
    write_json_atomic(
        root / "cli-entry.json",
        {"schema_version": 1, "path": str(target), "source": str(source)},
    )
    return {
        "status": "ready",
        "path": str(target),
        "in_path": _is_in_path(directory),
        "path_action": None if _is_in_path(directory) else f"Add {directory} to PATH.",
    }


def _tree_size(path: Path) -> int:
    if not path.exists() or path.is_symlink():
        return 0
    return sum(
        item.stat().st_size
        for base, dirs, files in os.walk(path, followlinks=False)
        for name in files
        if not (item := Path(base) / name).is_symlink()
    )


def cleanup(*, cache_only: bool, all_data: bool, dry_run: bool) -> dict[str, Any]:
    if not (cache_only or all_data or dry_run):
        dry_run = True
    root = app_root()
    targets: list[dict[str, Any]] = []
    cache_path = (
        cache.cache_root()
        if hasattr(cache, "cache_root")
        else Path.home() / "Library/Caches/audio-transcription"
    )
    targets.append(
        {"kind": "cache", "path": str(cache_path), "size_bytes": _tree_size(cache_path)}
    )
    if all_data:
        for name in (
            "runtimes",
            "models",
            "active.json",
            "active-python",
            "cli-entry.json",
        ):
            path = root / name
            targets.append(
                {
                    "kind": name,
                    "path": str(path),
                    "size_bytes": _tree_size(path)
                    if path.is_dir()
                    else path.stat().st_size
                    if path.exists()
                    else 0,
                }
            )
    if dry_run:
        return {"status": "ready", "dry_run": True, "targets": targets}
    cache.clear(all_entries=True, dry_run=False)
    if all_data:
        if root.is_symlink() or (root.exists() and root.resolve() != root):
            raise CliError(
                "RUNTIME_SAFETY_ERROR",
                f"Refusing cleanup through a symlinked root: {root}",
            )
        cli_record = root / "cli-entry.json"
        if cli_record.is_file():
            try:
                target = Path(
                    json.loads(cli_record.read_text(encoding="utf-8"))["path"]
                )
                if (
                    target.is_file()
                    and not target.is_symlink()
                    and CLI_MARKER
                    in target.read_text(encoding="utf-8", errors="replace")
                ):
                    target.unlink()
            except (OSError, KeyError, json.JSONDecodeError):
                pass
        for name in ("runtimes", "models"):
            path = root / name
            if path.exists():
                if path.is_symlink() or path.parent != root:
                    raise CliError(
                        "RUNTIME_SAFETY_ERROR",
                        f"Refusing unsafe cleanup target: {path}",
                    )
                shutil.rmtree(path)
        for name in ("active.json", "active-python", "cli-entry.json"):
            path = root / name
            if path.is_file() and not path.is_symlink():
                path.unlink()
    return {"status": "ready", "dry_run": False, "targets": targets}


def storage(args: argparse.Namespace) -> dict[str, Any]:
    if args.storage_command == "status":
        return {"status": "ready", **storage_status()}
    if args.storage_command == "configure":
        value = configure_storage(
            app=args.app_root,
            cache=args.cache_root,
            temporary=args.temp_root,
            transcripts=args.transcript_root,
        )
        return {
            "status": "ready",
            "storage": value,
            "next_actions": [
                {"command": "manage-runtime inspect --json"},
                {"command": "manage-runtime setup --profile <standard|low-memory> --json"},
            ],
        }
    removed = reset_storage()
    return {"status": "ready", "removed": str(removed) if removed else None}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--version", action="version", version=f"manage-runtime {__version__}"
    )
    sub = parser.add_subparsers(dest="command", required=True)
    inspect_parser = sub.add_parser("inspect", add_help=False)
    inspect_parser.add_argument("--json", action="store_true")
    setup_parser = sub.add_parser("setup", add_help=False)
    setup_parser.add_argument(
        "--profile", choices=("standard", "low-memory"), required=True
    )
    setup_parser.add_argument("--json", action="store_true")
    doctor_parser = sub.add_parser("doctor", add_help=False)
    doctor_parser.add_argument("--json", action="store_true")
    install = sub.add_parser("install-cli", add_help=False)
    install.add_argument("--bin-dir", type=Path, required=True)
    install.add_argument("--json", action="store_true")
    clean = sub.add_parser("cleanup", add_help=False)
    clean.add_argument("--dry-run", action="store_true")
    clean.add_argument("--cache", action="store_true")
    clean.add_argument("--all", action="store_true")
    clean.add_argument("--json", action="store_true")
    storage_parser = sub.add_parser("storage", add_help=False)
    storage_sub = storage_parser.add_subparsers(dest="storage_command", required=True)
    storage_status_parser = storage_sub.add_parser("status", add_help=False)
    storage_status_parser.add_argument("--json", action="store_true")
    storage_configure = storage_sub.add_parser("configure", add_help=False)
    storage_configure.add_argument("--app-root", type=Path, required=True)
    storage_configure.add_argument("--cache-root", type=Path, required=True)
    storage_configure.add_argument("--temp-root", type=Path, required=True)
    storage_configure.add_argument("--transcript-root", type=Path, required=True)
    storage_configure.add_argument("--json", action="store_true")
    storage_reset = storage_sub.add_parser("reset", add_help=False)
    storage_reset.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def emit(value: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(value, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(value, ensure_ascii=False, indent=2))


def main(argv: list[str] | None = None) -> int:
    args = parse_args(list(sys.argv[1:] if argv is None else argv))
    try:
        if args.command == "inspect":
            value = inspect()
        elif args.command == "setup":
            value = setup(args.profile)
        elif args.command == "doctor":
            value = doctor()
        elif args.command == "install-cli":
            value = install_cli(args.bin_dir)
        elif args.command == "storage":
            value = storage(args)
        else:
            value = cleanup(
                cache_only=args.cache,
                all_data=args.all,
                dry_run=args.dry_run or not (args.cache or args.all),
            )
        emit(value, args.json)
        return 0 if value.get("status") not in {"failed", "not_ready"} else 1
    except CliError as exc:
        emit(exc.envelope(), getattr(args, "json", False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
