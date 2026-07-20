#!/usr/bin/env python3
"""Smoke-check the workflow's invocation, ownership, and local-brief contract."""

from __future__ import annotations

import re
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_PATH = SKILL_DIR / "SKILL.md"
OPENAI_PATH = SKILL_DIR / "agents" / "openai.yaml"


def require(text: str, needle: str) -> None:
    if " ".join(needle.split()) not in " ".join(text.split()):
        raise AssertionError(f"missing required contract: {needle!r}")


def reject(text: str, needle: str) -> None:
    if needle in text:
        raise AssertionError(f"local brief leaks orchestration context: {needle!r}")


def main() -> int:
    text = SKILL_PATH.read_text(encoding="utf-8")
    openai = OPENAI_PATH.read_text(encoding="utf-8")

    required = [
        "disable-model-invocation: true",
        "Use only when the user explicitly invokes",
        "/parallel-goal-workflows",
        "$parallel-goal-workflows",
        "exactly one Goal Owner",
        "fork_context: false",
        "never fork or forward the main conversation",
        "`done`, `blocked`, or `needs-human`",
        "Starting an owner is not completion",
        "Only the Main Agent reads this skill",
        "narrower independently",
        "Acceptance requires completed criteria",
    ]
    for needle in required:
        require(text, needle)
    require(openai, "allow_implicit_invocation: false")

    packets = re.findall(r"```text\n(.*?)\n```", text, re.DOTALL)
    if len(packets) != 1:
        raise AssertionError(f"expected one canonical local-brief packet, found {len(packets)}")
    packet = packets[0]
    if not packet.startswith("/goal\n\n"):
        raise AssertionError("local brief must start with '/goal' and a blank line")

    for field in [
        "Local goal:",
        "Relevant context:",
        "Boundary:",
        "Deliverable and evidence:",
        "Pause if:",
    ]:
        require(packet, field)

    for leaked in [
        "Main Agent",
        "Goal Owner",
        "parallel-goal-workflows",
        "SKILL.md",
        "delegation chain",
    ]:
        reject(packet, leaked)

    print("Parallel Goal Workflows checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
