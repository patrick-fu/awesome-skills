# Extension · card-board

Board tiles: sturdier cards, denser scan type, and the lime marker variant, for
surfaces that are used rather than read.

**Load when** the page is an ops workbench, dashboard, triage queue or control
panel: action-first, revisited daily, 6–12 stable tiles per screen, most of the
value in scanning rather than in reading prose.
**Skip when** the page is a long argument (use `surface-paper` + `fold-deep`)
or a projected deck.

## What it may activate (complete allowlist)

- `.pvl-card--board` for tiles: 1.6px ink border, radius 20px,
  `--pvl-shadow-lift` (`7px 8px 0 rgba(32,39,35,.12)`). Rough `.pvl-card`
  remains allowed for the one or two tiles that carry an argument.
- `<html data-dense="true">`, the only declared density switch: it lowers the
  sans scan floor to 10.5–13px. Continuous reading prose on the same page still
  stays >= 14px; never go below 10.5px anywhere.
- `.pvl-highlight--lime` (modifier on `.pvl-highlight`, `#dff56b`) as the marker
  variant for this composition. Still one focal accent per screen: lime
  *replaces* yellow here, it does not join it.
- Pastel tag palette for sources and actions, taken from the semantic-kit
  backgrounds (`--pvl-risk-bg`, `--pvl-path-bg`, `--pvl-ok-bg`,
  `--pvl-warn-bg`, `--pvl-extra-bg`) via `.pvl-badge` or a mono pill. Do not
  invent new pastels.

## Layout obligations that come with it

- The current top action owns the prime slot; status, sources and filters keep
  stable positions across visits.
- Deep layers open on a whole-card click (`.pvl-expand` + `aria-expanded`),
  never on hover; remember scroll/expand/filter state if the page persists.

## What it must never change

Ink, pencil line, shadow style (hard offsets only), radii allowlist, type
voices, emoji-on-nodes rule, and every invariant in `01-grammar.md`.

## Markers it should leave on the page

A workbench is the composition most likely to drift into a generic dashboard,
so it needs craft on purpose: a scribble or display-face title, tape on the
prime tile, and at least one sticky note carrying the human aside ("这个源昨天
才开始报"). Tiles alone are not enough.
