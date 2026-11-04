# Acceptance

A page in this style is done only when all three gates pass.

## Gate 1 - static audit
`python3 scripts/audit.py <page.html>` checks: base.css linked or tokens
inlined verbatim; **>= 2 distinct hand-made markers** (scribble, tape, sticky
note, rough card, band highlight, pencil annotation); no hover-driven layout
reveal; highlight caps; radius and shadow values inside the allowlist; no pure
black ink; emoji attached (sticker / note / badge / heading / callout only);
body and mono size floors; no external network references required by the page
itself. The marker list it prints is the identity evidence — check it, do not
just check the exit code.

Fixed-width warnings are expected in two by-design cases: tables sized inside
`.pvl-scroll` (horizontal scroll is the containment) and fixed-stage decks
(`data-stage`, exempt in audit). In both cases the MEASURE line from Gate 2 is
the authority for real overflow.

## Gate 2 - render
`python3 scripts/render.py <page.html> <out-dir>` screenshots at 1440 and 390
widths (mobile via a 390px iframe probe, because macOS headless Chrome clamps windows to >=500px) and reports `MEASURE mobile: scrollWidth=...` as the overflow gate. If no
headless Chrome is available the script says so and exits 0; in that case the
human gate must include a manual narrow-width check.

## Gate 3 - human checklist
- First glance: can you name the current question and the verdict?
- Are >= 2 hand-made markers visible, one of them above the fold?
- Does the extension set match the content (and stay loaded consistently for
  the whole page)?
- Are the main relations already drawn (not described)?
- One focal accent per screen?
- Realistic UI (if any) keeps experience detail; annotations explain it?
- Text plain and concrete; precise objects in mono?
- Deep dive: can the reader reach complete facts through the layers?
- Would Patrick say "对味"? Compare against `assets/examples/canonical*.png`
  (pure core) and `assets/examples/extensions*.png` (extension showcase). A
  page that matches neither at a glance is drifting.

Evals in `evals/` codify blind reproduction, token drift, and mobile overflow.
