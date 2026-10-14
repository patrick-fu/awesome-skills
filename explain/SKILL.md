---
name: explain
description: >-
  Explain concepts, code/design, or PR/MR changes; draft PR/MR titles and
  bodies, issue/incident replies, or QA handoffs; recover named tasks or
  historical decisions. Use for requested explanations, visualizations,
  writing, and context recovery. Routine implementation, debugging, code
  review, and completion summaries stay in their existing workflows.
---

# Explain

**Scope.** Apply to requested explanation, context recovery, or writing work.
Ordinary implementation and its routine wrap-up remain in their existing workflow.

**Route.** Choose the primary outcome from the requested action and final
deliverable before retrieving material. Load only the references needed for it.

| User request | Primary deliverable | Reference |
| --- | --- | --- |
| Explain a concept, code, or current design; explain it differently | Mechanism, execution path, or example | Relevant material; usually no branch reference |
| Explain an existing PR/MR | Change illustration, verification evidence, and merge impact | [Delivery](references/delivery.md) |
| Write or edit PR/MR titles or bodies, issue/incident replies, or QA handoffs | Usable destination text | [Delivery](references/delivery.md) |
| Recover a named task or explain a historical decision | Grounded status and next action, or decision rationale | [Orientation](references/orientation.md) |

“Write an MR” routes to writing even when it needs background recovery or diagrams.
For any scenario, read [Views](references/views.md) when a diagram, structural
view, or interaction helps. These are presentation choices, not a replacement
for the requested deliverable. For a bare link, use the conversation's active
request; ask only if the intended action remains materially ambiguous.
Review and debugging use their own workflows; Explain may support a requested
explanation or writing subtask within them. When asked to resume work, follow
the recovery reference through the next authorized action.

**Reuse.** Use supported material already in context; retrieve only facts needed
for the request that are missing, stale, or conflicting.

**Ground.** Preserve consequential conditions. Distinguish recorded facts,
mechanism-based inference, and unknowns; bound benefit and completion claims to
evidence for the described artifact.

**Frame.** Answer first, or establish the current position when catching up.
Reframe a confusing explanation with a different structure, example, or view.
Apply ISO 24495-1's outcome standard: the intended reader can find,
understand, and use the result. Borrow ASD-STE100's controlled-expression
discipline—stable terms, direct sentence patterns, and explicit actions or
conditions—without importing its English-only word list. Keep each section
around one idea and match the requested depth. Prefer a compact visual beside
brief prose when explaining relationships or changes; use prose alone when a
visual adds no information.

**Language.** For each deliverable, use the user's explicitly requested language
first. Otherwise follow their established language preference in the current
conversation, inferring it from their own messages when unstated. In a mixed
conversation without an established preference, use the language of the latest
substantive user request. The language of these instructions, examples, quoted
sources, code, or templates does not set the output language.

Apply the resolved language consistently to titles, body text, summaries,
headings at every level, subheadings, captions, diagram labels, and explanatory
pseudocode. Use supplied terminology and the project's `GLOSSARY.md` when
available. Translate ordinary explanatory terms into established domain terms
in the resolved language, without redundant foreign-language equivalents;
explain unfamiliar terms locally. Descriptive source vocabulary is prose, not
a code identifier. Keep source spelling where it identifies actual code symbols,
paths, commands, protocol fields, or proper names, adding a gloss in the resolved
language when useful.

**Re-entry.** When the user names ADHD or asks for low cognitive load,
optimize resuming rather than simplifying away substance: foreground the
current position and next action, use short labeled units, and attach
conditions to the decision they constrain.

Anchor code walkthroughs in the relevant execution path.

**Output.** Honor explicit language and destination-format requests. Answer in
chat by default; create a file when requested or required by the chosen visual medium.
