# Practice

Each entry exists because a real deliverable got corrected; each states the
target behaviour directly.

1. **One accent, placed.** At most one highlight per card, three per section,
   one focal accent per screen — on the phrase that carries the verdict.
2. **Expand on click.** The whole card toggles (`aria-expanded`); a second
   click closes it; hover leaves layout untouched.
3. **One problem, one card.** Related facts and their explanation live
   together, so the reader receives them assembled.
4. **Edit, then layer.** Merge duplicates, compress sentences, draw relations;
   then put genuinely secondary material behind a fold, an expand, or the
   density toggle — and keep it clean when opened.
5. **Real constraints, stated once.** Conditions and impact, in plain words.
6. **Emoji on objects.** Nodes, roles, files, tools, incidents; headings and
   stamps may carry one.
7. **Type floors by role.** Continuous reading >= 14px; mono labels >= 10.5px;
   scan surfaces and in-device rows declare `<html data-dense="true">` for
   10.5-13px sans, and gain weight rather than lose size when they must carry
   weight.
8. **390px holds.** Grids collapse to one column, tables scroll inside their
   card, notes stay inside the canvas.
9. **Pencil ink, paper shadows.** Ink `#2a2a2a` (paper `#202723`); shadows stay
   small hard offsets or soft paper lifts; colour stays inside the semantic
   kit.
10. **Three voices, three jobs.** Handwritten face for titles, annotations and
    body; system sans inside device frames and on dense scan; mono for precise
    objects.
11. **Motion reveals argument state.** Prefer in-place state evolution (slot
    open, clip wipe, blur bridge, landing impact, ink beam, or scrubbed
    `seek(t)` stage) over walls of static 3-column boxes. Enter from
    `scale(.95)` rather than `scale(0)`, keep ordinary reading pages zero-JS,
    and stay strictly inside the paper-ink whiteboard hand — no dark neon,
    glassmorphism, or SVG Gooey.
12. **White first.** True white is the default canvas; paper and dot arrive
    with the content that asks for them.
13. **Hand-made marks on the page.** Scribble, tape, sticky note, rough card,
    band highlight, pencil annotation — two or more kinds, one of them on the
    first screen.
14. **Dials set once, kept.** Set the options the content signals justify
    (`03-composition.md`) and hold them for the whole page; pages with
    different dials still read as the same hand.
15. **Pencil lines frame asides.** Rough cards, stamps, notes and folds carry
    the framing role.
16. **No cards inside cards.** A `.pvl-card` already carries a hand-drawn
    border; divide internal regions with whitespace, thin or dashed rules, or a
    soft tinted band rather than nesting another bordered card.
17. **No decorative kickers or fake telemetry.** Omit reflexive `ALL CAPS`
    kickers above headings (keep `.pvl-kicker` strictly for real page metadata),
    fake `"LIVE"` dots, and meaningless decorative pills; reserve `.pvl-badge`
    for semantic status stamps.
18. **Clean transitions, aligned numerals.** Declare transitioned properties
    explicitly—never use `transition: all` or idle bobbing loops—and enable
    `font-variant-numeric: tabular-nums` on numeric metrics.
