from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .errors import CliError, setup_required

SKILL_ROOT = Path(__file__).resolve().parents[2]
LOCK_PATH = SKILL_ROOT / "runtime" / "models.lock.json"


def app_root() -> Path:
    override = os.environ.get("AUDIO_TRANSCRIPTION_APP_ROOT")
    return (
        Path(override).expanduser()
        if override
        else Path.home() / "Library/Application Support/audio-transcription"
    )


def cache_root() -> Path:
    override = os.environ.get("AUDIO_TRANSCRIPTION_CACHE_ROOT")
    return (
        Path(override).expanduser()
        if override
        else Path.home() / "Library/Caches/audio-transcription"
    )


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
