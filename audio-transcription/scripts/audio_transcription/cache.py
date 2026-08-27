from __future__ import annotations

import json
import os
import shutil
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .config import cache_root, write_json_atomic
from .errors import CliError

RETENTION_DAYS = 30


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _prepare_root(create: bool = True) -> tuple[Path, Path]:
    root = cache_root()
    if root.is_symlink():
        raise CliError(
            "CACHE_SAFETY_ERROR", f"Cache root must not be a symlink: {root}"
        )
    if create:
        root.mkdir(parents=True, exist_ok=True)
    if root.exists() and (root.is_symlink() or not root.is_dir()):
        raise CliError(
            "CACHE_SAFETY_ERROR", f"Cache root must be a normal directory: {root}"
        )
    if root.exists():
        os.chmod(root, 0o700)
    return root, root.resolve(strict=False)


def result_root(create: bool = True) -> Path:
    root, _ = _prepare_root(create=create)
    path = root / "results"
    if path.is_symlink():
        raise CliError(
            "CACHE_SAFETY_ERROR", f"Result cache must not be a symlink: {path}"
        )
    if create:
        path.mkdir(parents=True, exist_ok=True)
        os.chmod(path, 0o700)
    return path


def entry_path(key: str, *, create_root: bool = True) -> Path:
    if len(key) != 64 or any(character not in "0123456789abcdef" for character in key):
        raise CliError("CACHE_SAFETY_ERROR", "Invalid cache key")
    return result_root(create=create_root) / key


def _entry_manifest(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads((path / "cache-manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if value.get("cache_key") != path.name:
        return None
    return value


def is_safe_entry(path: Path, root: Path | None = None) -> bool:
    root = root or result_root()
    try:
        return (
            not root.is_symlink()
            and not path.is_symlink()
            and path.is_dir()
            and path.parent == root
            and path.resolve().parent == root.resolve()
            and _entry_manifest(path) is not None
        )
    except OSError:
        return False


def lookup(key: str) -> Path | None:
    root = result_root(create=False)
    if not root.is_dir():
        return None
    path = entry_path(key, create_root=False)
    if not is_safe_entry(path, root):
        return None
    manifest = _entry_manifest(path)
    if (
        manifest
        and manifest.get("status") in {"completed", "partial"}
        and (path / "manifest.json").is_file()
    ):
        return path
    return None


def store(key: str, source: Path, metadata: dict[str, Any]) -> Path:
    root = result_root()
    final = root / key
    if final.exists():
        if is_safe_entry(final, root):
            return final
        raise CliError("CACHE_SAFETY_ERROR", f"Refusing unknown cache entry: {final}")
    temporary = Path(tempfile.mkdtemp(prefix=f".{key}.", dir=root))
    try:
        os.chmod(temporary, 0o700)
        for item in source.iterdir():
            destination = temporary / item.name
            if item.is_dir() and not item.is_symlink():
                shutil.copytree(item, destination)
            elif item.is_file() and not item.is_symlink():
                shutil.copy2(item, destination)
        cache_manifest = {
            "schema_version": 1,
            "cache_key": key,
            "created_at": utc_now(),
            "status": metadata.get("status"),
            "source_sha256": metadata.get("input", {}).get("sha256"),
        }
        write_json_atomic(temporary / "cache-manifest.json", cache_manifest)
        os.replace(temporary, final)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return final


def restore(source: Path, destination: Path) -> None:
    if not is_safe_entry(source):
        raise CliError("CACHE_SAFETY_ERROR", f"Refusing unsafe cache entry: {source}")
    if destination.exists() and any(destination.iterdir()):
        raise CliError("OUTPUT_EXISTS", f"Output directory is not empty: {destination}")
    destination.mkdir(parents=True, exist_ok=True)
    os.chmod(destination, 0o700)
    for item in source.iterdir():
        if item.name == "cache-manifest.json":
            continue
        target = destination / item.name
        if item.is_dir() and not item.is_symlink():
            shutil.copytree(item, target)
        elif item.is_file() and not item.is_symlink():
            shutil.copy2(item, target)


def _created_at(manifest: dict[str, Any]) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(
            str(manifest["created_at"]).replace("Z", "+00:00")
        )
        return parsed if parsed.tzinfo else None
    except (KeyError, TypeError, ValueError):
        return None


def scan() -> list[dict[str, Any]]:
    root = result_root()
    items: list[dict[str, Any]] = []
    for path in sorted(root.iterdir()):
        if not is_safe_entry(path, root):
            continue
        manifest = _entry_manifest(path) or {}
        size = sum(
            child.stat().st_size
            for base, dirs, files in os.walk(path, followlinks=False)
            for name in files
            if not (child := Path(base) / name).is_symlink()
        )
        items.append(
            {
                "path": str(path),
                "size_bytes": size,
                "created_at": manifest.get("created_at"),
            }
        )
    return items


def clear(
    *, expired: bool = False, all_entries: bool = False, dry_run: bool = True
) -> list[dict[str, Any]]:
    root = result_root()
    cutoff = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)
    selected: list[tuple[Path, dict[str, Any]]] = []
    for item in scan():
        path = Path(item["path"])
        manifest = _entry_manifest(path) or {}
        created = _created_at(manifest)
        if all_entries or (expired and created is not None and created < cutoff):
            selected.append((path, item))
    if not dry_run:
        for path, _ in selected:
            if not is_safe_entry(path, root):
                raise CliError(
                    "CACHE_SAFETY_ERROR", f"Cache entry changed before deletion: {path}"
                )
            shutil.rmtree(path)
    return [item for _, item in selected]
