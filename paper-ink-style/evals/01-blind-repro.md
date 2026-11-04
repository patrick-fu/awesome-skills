# Eval 01 - blind reproduction

Purpose: prove the skill reproduces the style without seeing any original.

1. Give the agent ONLY: this skill's directory and a content brief (a neutral
   engineering topic, ~4 sections, one diagram, one comparison, one takeaway).
   No originals, no prior pages, no network.
2. The agent produces `page.html`, runs `scripts/audit.py` and
   `scripts/render.py`, and iterates until audit passes.
3. Pass criteria: audit PASS; screenshots at 1440 and 390 show the style
   (white canvas, pencil rough cards, one marker accent per screen, stickers
   on nodes, takeaway lane); a human familiar with the style says it matches
   `assets/examples/canonical-desktop.png` at a glance.
