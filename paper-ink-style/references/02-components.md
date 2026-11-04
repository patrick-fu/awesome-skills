# Components

All classes live in `assets/base.css` and are always available. Do not
reimplement them inline; if a needed component is missing, add it to base.css
first (bump the version). Which content signals should make you reach for a
component, and how far its overrides may go, is declared per extension in
`extensions/`; the Ext column below names the owning extension, `core` meaning
it belongs to no extension and should usually be present.

| Component | Class | Ext | Use | Key parameters |
|---|---|---|---|---|
| rough card | `.pvl-card` | core | one argument unit | 2px pencil-line border, irregular radius `255px 15px 225px/15px 225px 15px 255px`, shadow `2px 2px rgba(42,42,42,.05)` |
| marker highlight | `.pvl-highlight` | core | the phrase carrying the verdict | `#ffe066`, opacity .6, multiply, rotate -1deg, radius `3px 8px 4px 6px` |
| scribble underline | `.pvl-scribble` | core | sentence-level verdict | inline SVG double wave, stroke `#2a2a2a` 1.5px |
| sticky note | `.pvl-note` + `--pink/--blue/--green` | core | aside, wry comment, field note | tint at `f2` alpha, 1px pencil-light border, radius `2px 15px`, blur 2px, shadow `3px 5px 12px rgba(0,0,0,.08)` |
| tape | `.pvl-tape` | core | attach a card to the canvas | 80x24, beige gradient at `b3/66` alpha, rotate -2deg, top -12px |
| mono badge | `.pvl-badge` | core | stamps: CONFIRMED / REJECTED / panel headers | pill, mono 12px 700, white on semantic color |
| sticker | `.pvl-sticker` | core | emoji as semantic object on a node | dashed 2px ring in semantic color, 44px |
| connector | `.pvl-connector` | core | route between nodes | 3px dashed path-blue at .55 |
| callout | `.pvl-callout` + `--path/--ok/--risk` | core | TL;DR and framed asides | 8px left rule in semantic color, soft bg, radius `0 12px 12px 0` |
| takeaway | `.pvl-takeaway` | core | bottom lane of a teaching beat | display face 19px centered + `.pvl-highlight` on key phrase |
| reading layers | `.pvl-tech-only`, `[data-density]` | core (fold-deep composes it) | plain vs technical layer | `html:not([data-density="tech"]) .pvl-tech-only{display:none}` |
| whole-card expand | `.pvl-expand` + `aria-expanded` | core | deep layer on click | body hidden unless `aria-expanded="true"`; hover must never expand |
| beat reveal | `.pvl-reveal`, `.pvl-reveal--stamp`, `--pvl-d` | core (stage-deck composes beats) | explanation unfolding | in/stamp keyframes; reduced-motion safe |

Type voices: display/annotation = `--pvl-font-display` (LXGW WenKai Lite,
fallback Kaiti SC/STKaiti); continuous reading = `--pvl-font-sans`; precise
objects (versions, files, logs, diffs, badges) = `--pvl-font-mono`.
Continuous reading body >= 14px; mono labels >= 10.5px; dense scan
surfaces (workbench, in-device UI) opt into 10.5-13px sans via
`<html data-dense="true">`.

Surfaces: default true white (`--pvl-surface:#fff`); warm paper via
`<html data-surface="paper">` (`#f4efe3` family); dotted paper via
`<html data-surface="dot">`. Same components, same grammar; each surface is an
extension note with its own override allowlist. Verified against the
style originals in v1.1.0.

Snippets in `assets/snippets/` show each component in context; copy structure,
keep classes, replace content.

## Additional components

| Component | Class | Ext | Use | Key parameters |
|---|---|---|---|---|
| clean card | `.pvl-card--clean` | surface-paper | report blocks on paper | 1.6px ink border, radius 16px, shadow `3px 4px 0 rgba(32,39,35,.12)` |
| board card | `.pvl-card--board` | card-board | workbench tiles | 1.6px ink border, radius 20px, shadow `7px 8px 0 rgba(32,39,35,.12)` |
| alt rough radius | `.pvl-card--alt` | surface-paper | variation so cards don't clone | `14px 6px 14px 6px/6px 14px 6px 14px` |
| band highlight | `.pvl-highlight--band` | surface-paper | underline-band emphasis (report) | gradient band `#ffe28a` 58%-92%, no block |
| lime marker | `.pvl-highlight--lime` | card-board | workbench marker variant, modifier on `.pvl-highlight` | `#dff56b`, same geometry as `.pvl-highlight`; replaces yellow on board tiles, never joins it |
| opaque notes | `.pvl-note--mint/--sky/--rose` | surface-paper | paper-surface notes | `#dff3e4 / #e3efff / #ffe1da` |
| warm tape | `.pvl-tape--warm` | surface-paper | report tape | `#ffe8a3` |
| dashed fold | `.pvl-fold` + `summary` | fold-deep | deep evidence layer | 2px dashed pencil-light, radius 11px, bg `rgba(255,255,255,.55)`, pill summary, ▸/▾ |
| pencil annotation | `.pvl-annot` | device-real | outer annotation cards on walkthroughs | rough radius + `2.5px 3px 0 rgba(42,42,42,.85)` |
| device frame | `.pvl-device` + `__status/__island/__sheet` | device-real | realistic phone | frame `#1c1c1e`, border `#2c2c2e`, radius 48px, device shadow, iOS tokens inside, system sans inside |

Paper surface also swaps the semantic kit to the warm kit
(`#1769c2 / #237a4b / #b52d25 / #b7790a / #8a4fbf` with pastel bgs).
Dot surface adds the 24px dot grid (`#e2ddd0`, 1.2px).

Hand-made markers — the identity check in `scripts/audit.py` counts distinct
kinds and requires >= 2 per page: `.pvl-scribble`, `.pvl-tape`, `.pvl-note*`,
rough `.pvl-card` (no `--clean` / `--board`), `.pvl-highlight--band`,
`.pvl-annot`. Stickers and plain `.pvl-highlight` are core, not craft, and do
not count toward the two.
