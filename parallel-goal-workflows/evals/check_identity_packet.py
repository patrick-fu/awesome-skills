#!/usr/bin/env python3
"""Smoke checks for Workflow Owner identity packet wording."""

from __future__ import annotations

import re
import sys
from pathlib import Path


SKILL_PATH = Path(__file__).resolve().parents[1] / "SKILL.md"


def section_between(text: str, start: str, end: str) -> str:
    pattern = re.compile(rf"{re.escape(start)}(?P<body>.*?){re.escape(end)}", re.DOTALL)
    match = pattern.search(text)
    if not match:
        raise AssertionError(f"missing section between {start!r} and {end!r}")
    return match.group("body")


def normalize_space(value: str) -> str:
    return " ".join(value.split())


def require_contains(haystack: str, needle: str, label: str) -> None:
    if normalize_space(needle) not in normalize_space(haystack):
        raise AssertionError(f"missing {label}: {needle!r}")


def main() -> int:
    text = SKILL_PATH.read_text(encoding="utf-8")
    owner_packet = section_between(text, "For the Workflow Owner:", "For downstream agents:")
    downstream_packet = section_between(text, "For downstream agents:", "## Observation Rhythm")

    checks = [
        (owner_packet, "You are the Workflow Owner", "direct Workflow Owner identity"),
        (owner_packet, "You are not the Main Agent", "not-Main-Agent identity boundary"),
        (owner_packet, "Do not create or start another Workflow Owner", "no recursive Workflow Owner"),
        (owner_packet, "already active", "forwarded trigger already handled"),
        (downstream_packet, "You are a downstream agent", "direct downstream identity"),
        (downstream_packet, "Do not create a Workflow Owner", "downstream no-owner boundary"),
    ]

    failures: list[str] = []
    for haystack, needle, label in checks:
        try:
            require_contains(haystack, needle, label)
        except AssertionError as exc:
            failures.append(str(exc))

    if failures:
        print("Workflow Owner identity packet checks failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Workflow Owner identity packet checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
