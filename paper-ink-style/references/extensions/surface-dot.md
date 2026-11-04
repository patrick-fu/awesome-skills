# Extension · surface-dot

Dotted paper: the canvas becomes graph/notebook paper, so a scene-by-scene
walkthrough reads as annotated field notes.

**Load when** the page walks a reader through screens, scenes or steps and the
canvas itself should feel like a notebook page — experience walkthroughs,
annotated UI tours, onboarding explainers.
**Skip when** the page is a long evidence-driven report (use `surface-paper`)
or a projected deck (true white). Never combine with `surface-paper`.

## What it may activate (complete allowlist)

- `<html data-surface="dot">` (or the same attribute on a wrapping block, to
  make one section of a page notebook paper) → `--pvl-surface #f8f7f2`,
  `--pvl-surface-card #ffffff`, `--pvl-ink #1c1c1e`, `--pvl-muted #545350`,
  `--pvl-rule #e2ddd0`, plus the 24px dot grid drawn with
  `radial-gradient(var(--pvl-paper-dot) 1.2px, transparent 1.2px)`.
- Cards on dot paper stay white so they lift off the grid; keep `.pvl-card`
  (rough) or `.pvl-annot` for pencil annotation cards.

## What it must never change

- Dot size and spacing (1.2px / 24px) are fixed; do not densify the grid to
  "look more technical".
- Ink, marker, semantic kit, radii, shadows, type voices: all core.
- The grid is a surface, not a decoration layer — never add a second texture.

## Markers it should leave on the page

Dot paper usually travels with `device-real`: annotations outside the device
(`.pvl-annot` + pen-blue connectors) are the hand-made markers here. If the
page has no device, keep at least a scribble title and one sticky note.
