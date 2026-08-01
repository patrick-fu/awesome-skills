#!/usr/bin/env python3
"""Create deterministic blind inputs and a private-to-judge mapping."""

from __future__ import annotations

import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASES_PATH = ROOT / "evals" / "cases.json"
BLIND_PATH = ROOT / "evals" / "benchmark-blind.json"
MAP_PATH = ROOT / "evals" / "benchmark-map.json"
SEED = 20260801


def main() -> None:
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    cases = list(data["cases"])
    random.Random(SEED).shuffle(cases)

    blind_cases = []
    mapping = []
    for index, case in enumerate(cases, start=1):
        blind_id = f"B-{index:02d}"
        visible = {
            "id": blind_id,
            "language": case["language"],
            "scene": case["scene"],
            "mode": case["mode"],
            "scope": case["scope"],
            "prompt": case["prompt"],
            "source": case["source"],
        }
        if "voice_sample" in case:
            visible["voice_sample"] = case["voice_sample"]
        blind_cases.append(visible)
        mapping.append(
            {
                "blind_id": blind_id,
                "case_id": case["id"],
                "title": case["title"],
                "assertions": case["assertions"],
                "critical": case["critical"],
            }
        )

    BLIND_PATH.write_text(
        json.dumps(
            {"version": 1, "seed": SEED, "cases": blind_cases},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    MAP_PATH.write_text(
        json.dumps(
            {"version": 1, "seed": SEED, "mapping": mapping},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(blind_cases)} blind cases with seed {SEED}")


if __name__ == "__main__":
    main()
