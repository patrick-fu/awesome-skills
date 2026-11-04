# Grammar

The style is a way of leading a reader, not a paint job. The invariants below
are the contract for "one core plus extensions": they hold at every density and
with every extension set; `03-composition.md` decides which of the freedoms a
given page takes.

## Identity invariants (never vary)

- Ink and three-alpha pencil line; no pure black; hard-offset or paper-lift shadows
- One focal marker accent per screen (yellow family; lime replaces it on board
  tiles); the highlight carries the verdict
- Stickers as semantic objects on real nodes; dashed connectors; verdict-sentence titles
- TL;DR stamp card opening (a rough card carrying a TL;DR stamp and the
  verdicts); takeaway lane closing each teaching beat
- The handwritten face is the reading voice: titles, annotations and body;
  system sans only inside device frames and on dense scan surfaces; mono for
  precise objects
- Diagrams carry the explanation; prose carries verdicts, conditions, key facts
- Hand-made marks on the page: scribble, tape, sticky note, rough card, band
  highlight, pencil annotation — two or more kinds, one of them on the first
  screen

## Freedoms (vary by content; each is a dial in `03-composition.md`)

- Surface preset: true white / warm paper / dotted paper
- Card family: irregular rough vs clean 16px vs board 20px
- Density and type tier (`data-dense`); marker hue variant (lime on board tiles)
- Interaction form: whole-card expand, dashed fold, beat reveal, long scroll,
  fixed stage
- Annotation treatment around realistic device frames

## One screen, one thesis
- Every block answers "what should the reader look at right now".
- Titles are verdicts or questions, never labels: "不是机器慢，是队列在等一把锁",
  "同一个开关，差别在消息闭环".
- A mono/sans kicker carries meta (date, duration, scope) so the title stays clean.

## Diagrams do the explaining
| Question | Diagram |
|---|---|
| causality / data flow | nodes + arrows (stickers on real roles) |
| time / windows | timeline on one shared scale |
| equal-weight options | side-by-side cards or table |
| condition combinations | matrix |
| who owns what | layers / swimlanes |
| what the user will see | realistic scene |
Text next to a diagram states verdicts, conditions, and key facts only.
Never restate what the diagram already shows.

## Layered reading
- Open with a TL;DR stamp card: a rough card, a mono/badge stamp, 3-6 bullets
  with the verdicts bolded. The stamp card is a composition, not a component —
  no filled colour block with a side rule; the pencil line does the framing.
 
- Plain layer first (experience, consequences, conditions); technical layer
  (events, processes, logs, experiments) behind `data-density="tech"` and
  whole-card expand. The switch must change what the reader processes, not
  hide unedited mess.
- Edit first (merge duplicates, compress sentences, draw relations), then
  layer. Hiding complexity is not organizing it.

## Emphasis discipline
- One focal accent per screen; highlight marks the phrase that carries the
  verdict, not every important word.
- Semantic kit: yellow = look here, blue = path/mechanism, green = passes,
  red = blocks/risk, purple = occasional agent/model state. Colors are labels
  in the argument, never brand gradients.

## Emoji and stickers
- Emoji are semantic objects attached to nodes, roles, files, tools,
  incidents. Naked floating emoji in running prose reads childish.
- Keep one mark per meaning; secondary marks step back.

## Voice
- Plain, concrete, engineering-toned: "现在卡在哪", "谁叫醒谁", "先看结论".
- Numbers, versions, experiment conditions stated exactly; mono face for them.
- First person is welcome in opinion/practice pieces; drop it in source-level
  comparisons. No defensive boilerplate.
- End each teaching beat with a takeaway lane: one sentence, marker highlight
  over the key phrase.

## Cross-referencing
- Documents cite each other and embed artifacts (HTML cards, decks) instead of
  restating them. In self-contained outputs, embed the artifact or link the
  reader to a sibling file; never duplicate the same fact in two places.
