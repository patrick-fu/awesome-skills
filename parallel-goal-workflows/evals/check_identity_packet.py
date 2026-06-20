#!/usr/bin/env python3
"""Smoke checks for user-invoked workflow and identity packet contracts."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_PATH = SKILL_DIR / "SKILL.md"
OPENAI_PATH = SKILL_DIR / "agents" / "openai.yaml"


def frontmatter_from(text: str) -> dict:
    if not text.startswith("---\n"):
        raise AssertionError("missing YAML front matter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise AssertionError("missing closing YAML front matter fence")
    frontmatter = parts[1]
    data = yaml.safe_load(frontmatter)
    if not isinstance(data, dict):
        raise AssertionError("front matter must be a mapping")
    return data


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


def require_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def main() -> int:
    text = SKILL_PATH.read_text(encoding="utf-8")
    frontmatter = frontmatter_from(text)
    openai_config = yaml.safe_load(OPENAI_PATH.read_text(encoding="utf-8"))
    if not isinstance(openai_config, dict):
        raise AssertionError("agents/openai.yaml must be a mapping")

    owner_packet = section_between(text, "For the Workflow Owner:", "For downstream agents:")
    downstream_packet = section_between(text, "For downstream agents:", "## Observation Rhythm")

    value_checks = [
        (frontmatter.get("disable-model-invocation"), True, "Claude model invocation policy"),
        ("when_to_use" in frontmatter, False, "no model-triggering when_to_use field"),
        (
            openai_config.get("policy", {}).get("allow_implicit_invocation"),
            False,
            "OpenAI implicit invocation policy",
        ),
    ]

    contains_checks = [
        (text, "Use this skill only when the user explicitly invokes it", "explicit user invocation rule"),
        (text, "/parallel-goal-workflows", "Claude slash invocation example"),
        (text, "$parallel-goal-workflows", "OpenAI/Codex invocation example"),
        (owner_packet, "You are the Workflow Owner", "direct Workflow Owner identity"),
        (owner_packet, "You are not the Main Agent", "not-Main-Agent identity boundary"),
        (owner_packet, "do not read or invoke parallel-goal-workflows", "owner no-skill-invocation boundary"),
        (owner_packet, "Do not create or start another Workflow Owner", "no recursive Workflow Owner"),
        (owner_packet, "do not paste the raw user prompt", "owner no raw prompt forwarding"),
        (owner_packet, "already active", "forwarded trigger already handled"),
        (downstream_packet, "You are a downstream agent", "direct downstream identity"),
        (
            downstream_packet,
            "You are not the Main Agent or the Workflow Owner",
            "downstream not-Main-Agent-or-owner boundary",
        ),
        (downstream_packet, "do not read or invoke parallel-goal-workflows", "downstream no-skill-invocation boundary"),
        (downstream_packet, "do not paste the raw user prompt", "downstream no raw prompt forwarding"),
        (downstream_packet, "Do not create a Workflow Owner", "downstream no-owner boundary"),
    ]

    failures: list[str] = []
    for actual, expected, label in value_checks:
        try:
            require_equal(actual, expected, label)
        except AssertionError as exc:
            failures.append(str(exc))

    for haystack, needle, label in contains_checks:
        try:
            require_contains(haystack, needle, label)
        except AssertionError as exc:
            failures.append(str(exc))

    if failures:
        print("Parallel Goal Workflows checks failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Parallel Goal Workflows checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
