#!/usr/bin/env python3
"""Smoke checks for user-invoked workflow and local brief contracts."""

from __future__ import annotations

import re
import sys
from pathlib import Path

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
    data: dict[str, object] = {}
    for line in frontmatter.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise AssertionError(f"unsupported front matter line: {line!r}")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip().strip('"')
        if value.lower() == "true":
            data[key] = True
        elif value.lower() == "false":
            data[key] = False
        else:
            data[key] = value
    return data


def openai_allows_implicit_invocation(text: str) -> bool:
    match = re.search(r"(?m)^\s+allow_implicit_invocation:\s*(true|false)\s*$", text)
    if not match:
        raise AssertionError("missing allow_implicit_invocation setting")
    return match.group(1) == "true"


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


def require_not_contains(haystack: str, needle: str, label: str) -> None:
    if normalize_space(needle) in normalize_space(haystack):
        raise AssertionError(f"unexpected {label}: {needle!r}")


def require_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def main() -> int:
    text = SKILL_PATH.read_text(encoding="utf-8")
    frontmatter = frontmatter_from(text)
    openai_text = OPENAI_PATH.read_text(encoding="utf-8")

    owner_packet = section_between(text, "For the Goal Owner:", "For downstream agents:")
    downstream_packet = section_between(text, "For downstream agents:", "## Observation Rhythm")

    value_checks = [
        (frontmatter.get("disable-model-invocation"), True, "Claude model invocation policy"),
        ("when_to_use" in frontmatter, False, "no model-triggering when_to_use field"),
        (
            openai_allows_implicit_invocation(openai_text),
            False,
            "OpenAI implicit invocation policy",
        ),
    ]

    contains_checks = [
        (text, "Use this skill only when the user explicitly invokes it", "explicit user invocation rule"),
        (text, "/parallel-goal-workflows", "Claude slash invocation example"),
        (text, "$parallel-goal-workflows", "OpenAI/Codex invocation example"),
        (text, "Only the Main Agent reads this skill", "skill isolation rule"),
        (text, "full main conversation", "no full-history forwarding rule"),
        (text, "fork_context", "clean context spawn option"),
        (text, "set it to `false`", "clean context spawn value"),
        (text, "not this SKILL.md", "no skill body forwarding rule"),
        (text, "narrower than the current assignment", "nested narrowing rule"),
        (text, "independently checkable result", "nested verification rule"),
        (text, "Do not create coordination-only layers", "no coordination-only layers rule"),
        (text, "do not ask another agent to own the entire assignment", "no wholesale transfer rule"),
        (owner_packet, "Take this goal to an acceptance-ready result", "owner goal line"),
        (owner_packet, "carry the following goal end to end", "owner goal ownership"),
        (owner_packet, "Useful context", "owner useful context section"),
        (owner_packet, "Please decide the execution shape yourself", "owner execution freedom"),
        (owner_packet, "focused helpers", "owner focused helper delegation"),
        (owner_packet, "Keep synthesis, acceptance judgment, and the final report with you", "owner retained synthesis"),
        (owner_packet, "A good final result should include", "owner acceptance criteria"),
        (owner_packet, "Pause if approval", "owner pause condition"),
        (downstream_packet, "one concrete local outcome", "downstream local goal"),
        (downstream_packet, "the following local task", "downstream natural local request"),
        (downstream_packet, "Relevant context", "downstream context section"),
        (downstream_packet, "Scope and boundaries", "downstream boundary section"),
        (downstream_packet, "Return:", "downstream deliverable section"),
        (downstream_packet, "anything that should pause further work", "downstream pause signal"),
    ]

    forbidden_packet_checks = [
        (owner_packet, "Main Agent", "owner Main Agent leakage"),
        (owner_packet, "Parent:", "owner parent leakage"),
        (owner_packet, "Parent", "owner parent leakage"),
        (owner_packet, "parent identity", "owner parent identity leakage"),
        (owner_packet, "Workflow Owner", "owner workflow-owner leakage"),
        (owner_packet, "parallel-goal-workflows", "owner skill trigger leakage"),
        (owner_packet, "$parallel-goal-workflows", "owner dollar trigger leakage"),
        (owner_packet, "/parallel-goal-workflows", "owner slash trigger leakage"),
        (owner_packet, "SKILL.md", "owner skill body leakage"),
        (owner_packet, "UI directive", "owner UI directive leakage"),
        (owner_packet, "You are not", "owner negative identity prompt"),
        (owner_packet, "delegation chain", "owner delegation-chain leakage"),
        (owner_packet, "/goal", "owner visible goal command"),
        (downstream_packet, "Main Agent", "downstream Main Agent leakage"),
        (downstream_packet, "Workflow Owner", "downstream workflow-owner leakage"),
        (downstream_packet, "Goal Owner", "downstream goal-owner leakage"),
        (downstream_packet, "Parent", "downstream parent leakage"),
        (downstream_packet, "parent identity", "downstream parent identity leakage"),
        (downstream_packet, "parallel-goal-workflows", "downstream skill trigger leakage"),
        (downstream_packet, "$parallel-goal-workflows", "downstream dollar trigger leakage"),
        (downstream_packet, "/parallel-goal-workflows", "downstream slash trigger leakage"),
        (downstream_packet, "SKILL.md", "downstream skill body leakage"),
        (downstream_packet, "UI directive", "downstream UI directive leakage"),
        (downstream_packet, "You are not", "downstream negative identity prompt"),
        (downstream_packet, "delegation chain", "downstream delegation-chain leakage"),
        (downstream_packet, "/goal", "downstream visible goal command"),
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

    for haystack, needle, label in forbidden_packet_checks:
        try:
            require_not_contains(haystack, needle, label)
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
