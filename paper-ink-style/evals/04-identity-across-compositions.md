# Eval 04 - identity across compositions

Purpose: prove that extensions change density and surface, not the hand. This
is the eval that failed before v1.2: four blind pages built from the same skill
came out looking like four different styles.

1. Pick two content briefs that force different extension sets, for example
   (a) a long incident report with an experiment matrix -> `surface-paper` +
   `fold-deep`, and (b) an ops workbench with 8 tiles -> `surface-paper` +
   `card-board` + `data-dense`. Give each to a fresh agent with only this
   skill's directory, no originals and no prior pages.
2. Both agents run `scripts/audit.py` and `scripts/render.py` and iterate to
   PASS.
3. Pass criteria:
   - audit reports >= 2 distinct hand-made markers on each page, and neither
     page needed a custom token, radius or shadow.
   - Placed side by side at 1440px, the two pages share: pencil-line ink, one
     focal accent, three type voices, verdict-sentence titles, TL;DR callout
     first, diagrams carrying the relations.
   - Only these differ: surface tokens, card family, density, interaction form.
   - A human familiar with the style says both look like the same person drew
     them, and neither looks like a generic report or dashboard template.
4. Fail if either page is clean-rectangle-only, if a page mixes two surface
   presets, or if the difference between the two reads as "different design
   systems" rather than "different density".
