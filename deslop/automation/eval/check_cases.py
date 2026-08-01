#!/usr/bin/env python3
"""Validate Deslop's public evaluation corpus and coverage."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CASES_PATH = ROOT / "evals" / "cases.json"
TRIGGERS_PATH = ROOT / "evals" / "triggers.json"


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"{path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"{path}: top level must be an object")
    return value


def require_unique_ids(items: list[dict[str, Any]], label: str) -> None:
    ids = [item.get("id") for item in items]
    missing = [index for index, value in enumerate(ids) if not value]
    if missing:
        raise SystemExit(f"{label}: missing id at indexes {missing}")
    duplicates = [key for key, count in Counter(ids).items() if count > 1]
    if duplicates:
        raise SystemExit(f"{label}: duplicate ids: {duplicates}")


def validate_cases(data: dict[str, Any]) -> None:
    cases = data.get("cases")
    if data.get("version") != 1 or not isinstance(cases, list):
        raise SystemExit("cases.json: expected version 1 and a cases array")
    if len(cases) < 25:
        raise SystemExit("cases.json: expected at least 25 behavior cases")
    require_unique_ids(cases, "cases.json")

    required = {
        "id",
        "title",
        "language",
        "scene",
        "mode",
        "scope",
        "prompt",
        "source",
        "assertions",
        "critical",
    }
    for item in cases:
        missing = sorted(required - item.keys())
        if missing:
            raise SystemExit(f"{item.get('id')}: missing fields {missing}")
        if item["language"] not in {"zh", "en", "mixed"}:
            raise SystemExit(f"{item['id']}: invalid language")
        if item["mode"] not in {"rewrite", "audit", "embedded", "file"}:
            raise SystemExit(f"{item['id']}: invalid mode")
        if item["scope"] not in {"balanced", "in-place", "rebuild"}:
            raise SystemExit(f"{item['id']}: invalid scope")
        if not isinstance(item["assertions"], list) or not item["assertions"]:
            raise SystemExit(f"{item['id']}: assertions must be non-empty")
        if not isinstance(item["critical"], bool):
            raise SystemExit(f"{item['id']}: critical must be boolean")

    languages = Counter(item["language"] for item in cases)
    for language, minimum in {"zh": 8, "en": 8, "mixed": 5}.items():
        if languages[language] < minimum:
            raise SystemExit(
                f"cases.json: {language} needs {minimum} cases, found {languages[language]}"
            )

    modes = {item["mode"] for item in cases}
    scopes = {item["scope"] for item in cases}
    if modes != {"rewrite", "audit", "embedded", "file"}:
        raise SystemExit(f"cases.json: incomplete mode coverage: {sorted(modes)}")
    if scopes != {"balanced", "in-place", "rebuild"}:
        raise SystemExit(f"cases.json: incomplete scope coverage: {sorted(scopes)}")


def validate_triggers(data: dict[str, Any]) -> None:
    queries = data.get("queries")
    if data.get("version") != 1 or not isinstance(queries, list):
        raise SystemExit("triggers.json: expected version 1 and a queries array")
    if len(queries) != 20:
        raise SystemExit(f"triggers.json: expected 20 queries, found {len(queries)}")
    require_unique_ids(queries, "triggers.json")
    labels = Counter(item.get("should_trigger") for item in queries)
    if labels != {True: 10, False: 10}:
        raise SystemExit(f"triggers.json: expected 10/10 labels, found {labels}")
    for item in queries:
        if not isinstance(item.get("query"), str) or not item["query"].strip():
            raise SystemExit(f"{item.get('id')}: query must be non-empty")


def validate_public_safety(*data: dict[str, Any]) -> None:
    serialized = json.dumps(data, ensure_ascii=False).lower()
    forbidden = (
        "/users/",
        "@corp.example",
        "internal-only",
        "private-token",
        "customer-name",
    )
    hits = [token for token in forbidden if token in serialized]
    if hits:
        raise SystemExit(f"evaluation corpus contains private markers: {hits}")


def main() -> int:
    cases = load_json(CASES_PATH)
    triggers = load_json(TRIGGERS_PATH)
    validate_cases(cases)
    validate_triggers(triggers)
    validate_public_safety(cases, triggers)
    print(
        "Deslop eval corpus OK: "
        f"{len(cases['cases'])} behavior cases, {len(triggers['queries'])} trigger cases"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
