# Extension · surface-paper

Warm paper reading surface plus the paper-native variants of card, note, tape
and highlight. Everything else stays core.

**Load when** the page will be read for minutes at a time — long-form report,
mechanism explainer, incident record, ops workbench — and true white reads as
glare or as "projected deck".
**Skip when** the page is projected on stage (keep true white) or you already
loaded `surface-dot`: both set `--pvl-surface`, never combine them.

## What it may activate (complete allowlist)

- `<html data-surface="paper">` → surface tokens only: `--pvl-surface #f4efe3`,
  `--pvl-surface-card #fffdf8`, `--pvl-ink #202723`, `--pvl-muted #59625d`,
  `--pvl-rule #d5cebf`, and the three pencil alphas rebuilt on the warm ink
  (`rgba(32,39,35,.85/.40/.15)`).
- Warm semantic kit, applied automatically by the same selector: path `#1769c2`,
  ok `#237a4b`, risk `#b52d25`, warn `#b7790a`, extra `#8a4fbf`, each with its
  pastel background. Use it as-is; do not hand-pick warm hexes.
- `.pvl-card--clean` (1.6px ink border, radius 16px, `--pvl-shadow-hard`) for
  report blocks; `.pvl-card--alt` (radius `14px 6px 14px 6px/6px 14px 6px 14px`)
  so neighbouring cards do not clone each other.
- `.pvl-highlight--band` (gradient band `#ffe28a`, 58%–92%) for underline-style
  emphasis inside long prose.
- `.pvl-note--mint/--sky/--rose` (opaque tints that survive warm paper) and
  `.pvl-tape--warm` (`#ffe8a3`).

## What it must never change

- Ink stays three-alpha pencil; no pure black, no new grey family.
- Marker stays in the yellow family; still one focal accent per screen.
- Radii and shadows stay inside the base.css allowlist.
- Type voices and size floors are untouched; paper is not a licence for smaller type.

## Markers it should leave on the page

Warm tape on at least one first-screen card, and a band highlight on the
verdict phrase of the TL;DR. A paper page whose only craft signal is a clean
rectangle is a generic report — see `references/04-anti-patterns.md` #13.
