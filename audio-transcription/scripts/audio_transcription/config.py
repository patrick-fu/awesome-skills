from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .errors import CliError, setup_required

SKILL_ROOT = Path(__file__).resolve().parents[2]
LOCK_PATH = SKILL_ROOT / "runtime" / "models.lock.json"
STORAGE_SCHEMA_VERSION = 1
STORAGE_KEYS = ("app_root", "cache_root", "temp_root", "transcript_root")


def storage_config_path() -> Path:
    override = os.environ.get("AUDIO_TRANSCRIPTION_STORAGE_CONFIG")
    return (
        Path(override).expanduser()
        if override
        else Path.home() / "Library/Application Support/audio-transcription/storage.json"
    )


def bootstrap_active_python_path() -> Path:
    return storage_config_path().parent / "active-python"


def _storage_error(message: str) -> CliError:
    return CliError("STORAGE_CONFIG_INVALID", message)


def _load_storage() -> dict[str, Path] | None:
    path = storage_config_path()
    if path.is_symlink() or not path.is_file():
        if not path.exists() and not path.is_symlink():
            return None
        raise _storage_error(f"Storage configuration must be a regular file: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise _storage_error(f"Cannot read storage configuration: {exc}") from exc
    if value.get("schema_version") != STORAGE_SCHEMA_VERSION:
        raise _storage_error("Unsupported or incomplete storage configuration.")
    roots: dict[str, Path] = {}
    for key in STORAGE_KEYS:
        raw = value.get(key)
        if not isinstance(raw, str) or not raw:
            raise _storage_error(f"Storage configuration is missing {key}.")
        root = Path(raw).expanduser()
        if not root.is_absolute() or root.is_symlink() or not root.is_dir():
            raise _storage_error(
                f"Configured {key} must be an available non-symlink directory: {root}"
            )
        roots[key] = root
    return roots


def _root_from(
    *, environment: str, storage_key: str, default: Path | None
) -> Path | None:
    override = os.environ.get(environment)
    if override:
        return Path(override).expanduser()
    storage = _load_storage()
    return storage[storage_key] if storage else default


def app_root() -> Path:
    return _root_from(
        environment="AUDIO_TRANSCRIPTION_APP_ROOT",
        storage_key="app_root",
        default=Path.home() / "Library/Application Support/audio-transcription",
    )


def cache_root() -> Path:
    return _root_from(
        environment="AUDIO_TRANSCRIPTION_CACHE_ROOT",
        storage_key="cache_root",
        default=Path.home() / "Library/Caches/audio-transcription",
    )


def temp_root() -> Path | None:
    return _root_from(
        environment="AUDIO_TRANSCRIPTION_TEMP_ROOT",
        storage_key="temp_root",
        default=None,
    )


def transcript_root() -> Path | None:
    return _root_from(
        environment="AUDIO_TRANSCRIPTION_TRANSCRIPT_ROOT",
        storage_key="transcript_root",
        default=None,
    )


def _is_nested(left: Path, right: Path) -> bool:
    try:
        left.relative_to(right)
        return True
    except ValueError:
        return False


def _prepare_storage_root(value: Path) -> Path:
    root = value.expanduser()
    if not root.is_absolute() or root == Path(root.anchor):
        raise _storage_error(f"Storage root must be a dedicated absolute directory: {root}")
    if len(root.parts) > 2 and root.parts[1] == "Volumes":
        volume = Path(root.anchor, root.parts[1], root.parts[2])
        if not volume.is_dir():
            raise _storage_error(f"Configured external volume is unavailable: {volume}")
    root.mkdir(parents=True, exist_ok=True)
    if root.is_symlink() or not root.is_dir():
        raise _storage_error(f"Storage root must be a normal directory: {root}")
    os.chmod(root, 0o700)
    return root.resolve()


def _write_bootstrap_active_python(python: Path) -> None:
    destination = bootstrap_active_python_path()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.parent.is_symlink() or not destination.parent.is_dir():
        raise _storage_error(
            f"Storage configuration directory must be a normal directory: {destination.parent}"
        )
    os.chmod(destination.parent, 0o700)
    descriptor, name = tempfile.mkstemp(prefix=".active-python.", dir=destination.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(f"{python}\n")
        os.chmod(temporary, 0o600)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def write_bootstrap_active_python(python: Path) -> None:
    if not python.is_file() or not os.access(python, os.X_OK):
        raise _storage_error(f"Active runtime Python must be executable: {python}")
    _write_bootstrap_active_python(python)


def clear_bootstrap_active_python() -> None:
    path = bootstrap_active_python_path()
    if path.exists() and not path.is_symlink() and path.is_file():
        path.unlink()


def configure_storage(
    *, app: Path, cache: Path, temporary: Path, transcripts: Path
) -> dict[str, str | int]:
    candidates = {
        "app_root": app.expanduser(),
        "cache_root": cache.expanduser(),
        "temp_root": temporary.expanduser(),
        "transcript_root": transcripts.expanduser(),
    }
    if any(value.is_symlink() for value in candidates.values()):
        raise _storage_error("Storage roots must not be symlinks.")
    candidates = {key: value.resolve(strict=False) for key, value in candidates.items()}
    values = list(candidates.values())
    if any(
        _is_nested(left, right)
        for index, left in enumerate(values)
        for other_index, right in enumerate(values)
        if index != other_index
    ):
        raise _storage_error("Storage roots must be distinct and must not overlap.")
    roots = {key: _prepare_storage_root(value) for key, value in candidates.items()}
    config = {"schema_version": STORAGE_SCHEMA_VERSION, **{key: str(value) for key, value in roots.items()}}
    destination = storage_config_path()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.parent.is_symlink() or not destination.parent.is_dir():
        raise _storage_error(
            f"Storage configuration directory must be a normal directory: {destination.parent}"
        )
    os.chmod(destination.parent, 0o700)
    write_json_atomic(destination, config)
    active_python = roots["app_root"] / "active-python"
    if active_python.is_file() and not active_python.is_symlink():
        python = Path(active_python.read_text(encoding="utf-8").strip())
        if python.is_file() and os.access(python, os.X_OK):
            _write_bootstrap_active_python(python)
    return {"config_path": str(destination), **config}


def reset_storage() -> Path | None:
    path = storage_config_path()
    if not path.exists():
        return None
    if path.is_symlink() or not path.is_file():
        raise _storage_error(f"Storage configuration must be a regular file: {path}")
    path.unlink()
    clear_bootstrap_active_python()
    return path


def storage_status() -> dict[str, object]:
    storage = _load_storage()
    roots = {
        "app_root": app_root(),
        "cache_root": cache_root(),
        "temp_root": temp_root(),
        "transcript_root": transcript_root(),
    }
    return {
        "config_path": str(storage_config_path()),
        "configured": storage is not None,
        "roots": {
            key: {
                "path": str(value) if value else None,
                "source": "environment"
                if os.environ.get(
                    {
                        "app_root": "AUDIO_TRANSCRIPTION_APP_ROOT",
                        "cache_root": "AUDIO_TRANSCRIPTION_CACHE_ROOT",
                        "temp_root": "AUDIO_TRANSCRIPTION_TEMP_ROOT",
                        "transcript_root": "AUDIO_TRANSCRIPTION_TRANSCRIPT_ROOT",
                    }[key]
                )
                else "persisted"
                if storage
                else "default",
            }
            for key, value in roots.items()
        },
    }


def active_config_path() -> Path:
    return app_root() / "active.json"


def load_lock() -> dict[str, Any]:
    try:
        value = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CliError(
            "RUNTIME_LOCK_INVALID", f"Cannot read runtime lock: {exc}"
        ) from exc
    if value.get("schema_version") != 1 or not isinstance(value.get("profiles"), dict):
        raise CliError(
            "RUNTIME_LOCK_INVALID", "Unsupported or incomplete models.lock.json"
        )
    return value


def load_active(*, require_complete: bool = True) -> dict[str, Any] | None:
    path = active_config_path()
    if not path.is_file():
        if require_complete:
            raise setup_required()
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CliError(
            "PROFILE_NOT_INSTALLED",
            f"Active runtime configuration is unreadable: {exc}",
            [{"command": "manage-runtime doctor --json"}],
        ) from exc
    required = ["runtime_version", "profile", "python", "models"]
    if any(not value.get(key) for key in required):
        raise CliError(
            "PROFILE_NOT_INSTALLED",
            "Active runtime configuration is incomplete.",
            [{"command": "manage-runtime doctor --json"}],
        )
    if require_complete:
        python = Path(value["python"])
        model_paths = [Path(item["path"]) for item in value["models"].values()]
        if not python.is_file() or any(not path.is_dir() for path in model_paths):
            raise CliError(
                "PROFILE_NOT_INSTALLED",
                "The active runtime or pinned model snapshot is missing.",
                [{"command": "manage-runtime doctor --json"}],
            )
    return value


def write_json_atomic(path: Path, value: Any, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
