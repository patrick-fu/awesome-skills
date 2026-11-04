# Anti-patterns (production corrections, distilled)

Each entry exists because a real deliverable got corrected. They are ways the
hand gets lost, not gates; entries 13-14 came out of a blind batch where four
pages built from the same skill drifted into four different looks.

1. **Too many highlights = no highlight.** <=1 `.pvl-highlight` per card,
   <=3 per section, one focal accent per screen.
2. **Hover must never expand or reveal layout.** Expand is a click on the
   whole card (`aria-expanded`), toggle back on second click.
3. **Do not scatter one problem into many small cards.** Related facts and
   their explanation live together; the reader should not reassemble them.
4. **Hiding complexity is not organizing it.** Edit first (merge, compress,
   draw), then layer. A collapsed block that is still a mess when opened fails.
5. **No defensive boilerplate.** State real constraints with conditions and
   impact; drop repeated generic disclaimers.
6. **No naked floating emoji.** Emoji attach to nodes/roles/objects, or stay
   out. Headings and callout markers may carry one.
7. **No tiny dense type as a default.** Continuous reading body >= 14px;
   10-12px is reserved for mono labels, tags, metadata. Workbench scan text and
   in-device system UI are the exception: 10.5-13px sans, declared once via
   `<html data-dense="true">` (verified against the Frontier workbench
   original). Never below 10.5px; scan text gets bolder, not smaller, when it
   must carry weight.
8. **No mobile horizontal overflow.** Verify at 390px; grids collapse.
9. **No pure black, no glossy chrome.** Ink is `#2a2a2a` (paper mode
   `#202723`); shadows are small hard offsets or soft paper lifts, never
   glossy gradients.
10. **Not everything is handwritten.** Display/annotation voice is the
    handwritten face; continuous reading stays system sans; precise objects
    stay mono.
11. **No brand gradients, no decorative motion.** Motion reveals argument
    state (card in, arrow draw, stamp, marker sweep); purely decorative
    animation breaks the style.
12. **Do not freeze paper as the only surface.** Default is true white; paper
    is a preset for long-form/ops surfaces.
13. **A page with no hand-made markers is not this style.** Clean rectangles
    plus a yellow block plus a sans title is a generic report; it loses the
    hand. Every page needs >= 2 distinct markers among scribble title, tape,
    sticky note, rough card, band highlight, pencil annotation, and one of them
    on the first screen.
14. **Option soup, or options as costumes.** Setting every dial "because it
    exists" crowds the page and mixes canvases; re-setting the dials per
    section turns one deliverable into a collage of styles. Set the options
    the content signals justify (`03-composition.md`) and keep them for the
    whole page. Two pages built with different options must still look like
    the same hand.
15. **A filled colour block with a side rule is not this style.** The old
    callout shape reads as a generic blockquote. Frame asides with pencil
    lines: rough cards, stamps, notes, folds.
