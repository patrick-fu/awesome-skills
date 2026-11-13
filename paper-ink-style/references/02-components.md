# Vocabulary

The style vocabulary: values and roles first, Web class names second.
Single-file HTML (`05-web-instance.md`, `assets/base.css`) is the default
carrier; slides, Swift, Kotlin, or desktop toolkits reproduce the same
parameters in their own idiom. If the Web instance and this table disagree,
fix both and bump the `base.css` version.

## Tokens

| Token | Value | Role |
|---|---|---|
| ink | `#2a2a2a` (paper `#202723`, dot `#1c1c1e`) | reading ink, pencil family |
| pencil alphas | ink at .85 / .40 / .15 | borders, lines, folds, connectors |
| canvas white | `#ffffff`, card `#ffffff` | default canvas |
| canvas paper | `#f4efe3`, card `#fffdf8` | reading that lasts minutes; ops surfaces |
| canvas dot | `#f8f7f2` + 24px dots `#e2ddd0` 1.2px, card `#ffffff` | walkthrough notebook |
| marker yellow | `#ffe066` at .6 multiply, rotate -1deg | the focal accent |
| marker band | `#ffe28a`, band 58%-92% | underline emphasis in long prose |
| marker lime | `#dff56b` | board tiles; replaces yellow there |
| semantic kit | path `#2563eb`, ok `#16a34a`, risk `#dc2626`, warn `#d97706`, extra `#9333ea`, bgs `#eff6ff/#f0fdf4/#fef2f2/#fffbeb/#faf5ff` | labels in the argument |
| warm kit (paper) | `#1769c2/#237a4b/#b52d25/#b7790a/#8a4fbf`, bgs `#e3efff/#dff3e4/#ffe1da/#ffe8a3/#f3eafb` | same roles on paper |
| note tints | translucent `#fffdf0f2/#ffebeef2/#e3f2fdf2/#e8f5e9f2` on white; opaque `#dff3e4/#e3efff/#ffe1da` on paper | sticky notes |
| tape | beige `#f5f5dc` b3→66 gradient; warm `#ffe8a3` | attach a card to the canvas |
| pen blue | `#0066cc` | annotation arrows outside device frames |
| radii | rough `255px 15px 225px/15px 225px 15px 255px`; alt `14px 6px 14px 6px/6px 14px 6px 14px`; clean `16px`; board `20px`; note `2px 15px`; fold `11px`; device `48px`; pill `999px` | the shape allowlist |
| shadows | card `2px 2px` ink .05; note `3px 5px 12px` .08; hard `3px 4px 0` .12; lift `7px 8px 0` .12; pencil `2.5px 3px 0` .85; device layered | hard offsets or paper lifts |
| type roles | handwritten face = titles, annotations, body; system sans = inside device frames and dense scan; mono = precise objects | the three voices |
| type floors | body >= 14px; mono >= 10.5px; dense scan 10.5-13px sans | readability |

## Components

Roles first; the Web column names the class in base.css. Copy structure on the
Web, reproduce parameters elsewhere.

| Component | Dial | Use | Key parameters | Web |
|---|---|---|---|---|
| rough card | core | one argument unit | 2px pencil-line border, irregular radius `255px 15px 225px/15px 225px 15px 255px`, shadow `2px 2px rgba(42,42,42,.05)` | `.pvl-card` |
| marker highlight | core | the phrase carrying the verdict | `#ffe066`, opacity .6, multiply, rotate -1deg, radius `3px 8px 4px 6px` | `.pvl-highlight` |
| scribble underline | core | sentence-level verdict | inline SVG double wave, stroke `#2a2a2a` 1.5px | `.pvl-scribble` |
| sticky note | core | aside, wry comment, field note | tint at `f2` alpha, 1px pencil-light border, radius `2px 15px`, blur 2px, shadow `3px 5px 12px rgba(0,0,0,.08)` | `.pvl-note` + `--pink/--blue/--green` |
| tape | core | attach a card to the canvas | 80x24, beige gradient at `b3/66` alpha, rotate -2deg, top -12px | `.pvl-tape` |
| mono badge | core | stamps: CONFIRMED / REJECTED / panel headers | pill, mono 12px 700, white on semantic color | `.pvl-badge` |
| sticker | core | emoji as semantic object on a node | dashed 2px ring in semantic color, 44px | `.pvl-sticker` |
| connector | core | route between nodes | 3px dashed path-blue at .55 | `.pvl-connector` |
| takeaway | core | bottom lane of a teaching beat | display face 19px centered + `.pvl-highlight` on key phrase | `.pvl-takeaway` |
| reading layers | density | plain vs technical layer | `html:not([data-density="tech"]) .pvl-tech-only{display:none}` | `.pvl-tech-only`, `[data-density]` |
| whole-card expand | core | deep layer on click | body shows on `aria-expanded="true"`; hover leaves layout untouched | `.pvl-expand` + `aria-expanded` |
| beat reveal | stage | explanation unfolding | in/stamp keyframes; reduced-motion safe | `.pvl-reveal`, `.pvl-reveal--stamp`, `--pvl-d` |

Type voices: the handwritten face `--pvl-font-display` (LXGW WenKai Lite,
fallback Kaiti SC/STKaiti) is the reading voice — titles, annotations and body
via `--pvl-font-body`; system sans (`--pvl-font-sans`) speaks only inside
device frames and on dense scan surfaces (`data-dense` swaps
`--pvl-font-body`); precise objects (versions, files, logs, diffs, badges) =
`--pvl-font-mono`. Continuous reading body >= 14px; mono labels >= 10.5px;
dense scan surfaces opt into 10.5-13px sans.

TL;DR and framed asides are compositions: a rough card carrying a
`.pvl-badge` stamp in the semantic colour plus the verdict bullets; pencil
lines do the framing.

Surfaces: default true white (`--pvl-surface:#fff`); warm paper via
`<html data-surface="paper">` (`#f4efe3` family); dotted paper via
`<html data-surface="dot">`. Same components, same grammar; each surface is an
option of the canvas dial with its own token set (`03-composition.md`).

Snippets in `assets/snippets/` show each component in context; copy structure,
keep classes, replace content.

## Additional components

| Component | Dial | Use | Key parameters | Web |
|---|---|---|---|---|
| clean card | card / note / tape / highlight | report blocks on paper | 1.6px ink border, radius 16px, shadow `3px 4px 0 rgba(32,39,35,.12)` | `.pvl-card--clean` |
| board card | card / density / highlight | workbench tiles | 1.6px ink border, radius 20px, shadow `7px 8px 0 rgba(32,39,35,.12)` | `.pvl-card--board` |
| alt rough radius | card / note / tape / highlight | neighbour variation: adjacent cards keep their own shape | `14px 6px 14px 6px/6px 14px 6px 14px` | `.pvl-card--alt` |
| band highlight | card / note / tape / highlight | underline-band emphasis (report) | gradient band `#ffe28a` 58%-92%, no block | `.pvl-highlight--band` |
| lime marker | card / density / highlight | workbench marker variant, modifier on `.pvl-highlight` | `#dff56b`, same geometry as `.pvl-highlight`; on board tiles it is the focal accent in place of yellow | `.pvl-highlight--lime` |
| opaque notes | card / note / tape / highlight | paper-surface notes | `#dff3e4 / #e3efff / #ffe1da` | `.pvl-note--mint/--sky/--rose` |
| warm tape | card / note / tape / highlight | report tape | `#ffe8a3` | `.pvl-tape--warm` |
| dashed fold | fold / density | deep evidence layer | 2px dashed pencil-light, radius 11px, bg `rgba(255,255,255,.55)`, pill summary, ▸/▾ | `.pvl-fold` + `summary` |
| pencil annotation | annot | outer annotation cards on walkthroughs | rough radius + `2.5px 3px 0 rgba(42,42,42,.85)` | `.pvl-annot` |
| device frame | annot | realistic phone | frame `#1c1c1e`, border `#2c2c2e`, radius 48px, device shadow, iOS tokens inside, system sans inside | `.pvl-device` + `__status/__island/__sheet` |

Paper surface also swaps the semantic kit to the warm kit
(`#1769c2 / #237a4b / #b52d25 / #b7790a / #8a4fbf` with pastel bgs).
Dot surface adds the 24px dot grid (`#e2ddd0`, 1.2px).

Hand-made marks — the craft layer that keeps a page from reading as a generic
report: `.pvl-scribble`, `.pvl-tape`, `.pvl-note*`, rough `.pvl-card` (no
`--clean` / `--board`), `.pvl-highlight--band`, `.pvl-annot`. Aim for two or
more kinds per page, one of them on the first screen. Stickers and plain
`.pvl-highlight` are vocabulary, not craft.
