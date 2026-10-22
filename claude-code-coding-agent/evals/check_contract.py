#!/usr/bin/env python3
"""Keep the supported entry point and progressive disclosure from drifting."""

from pathlib import Path
import re


SKILL = Path(__file__).resolve().parents[1]


def main():
    main_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    reference = (SKILL / "references" / "monitoring.md").read_text(encoding="utf-8")
    examples = re.findall(r"```bash\n(.*?)\n```", main_text, re.DOTALL)
    assert examples and all('claude_run.py" run' in example for example in examples), "Launch through the script."
    assert "<launcher>" not in main_text + reference, "Remove obsolete direct launch recipes."
    assert "printf '%s'" not in main_text + reference, "stdin and stream flags belong to the script."
    for document in (SKILL / "SKILL.md", SKILL / "references" / "monitoring.md"):
        for link in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
            if "://" in link:
                continue
            target, _, anchor = link.partition("#")
            path = document.parent / target
            assert path.is_file(), (document, link)
            if anchor:
                headings = [heading.lower().replace(" ", "-") for heading in
                            re.findall(r"^#+ (.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)]
                assert anchor in headings, (document, link)
    print(f"Claude contract lint passed: main={len(main_text.split())} words, reference={len(reference.split())} words.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
