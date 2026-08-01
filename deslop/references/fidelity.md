# Fidelity contract

Read this file for every Deslop task. Naturalness is subjective; fidelity is a
hard constraint.

## Protected spans

Preserve exact text unless the user explicitly authorizes a change:

- names, handles, organizations, products, places, and named versions;
- numbers, dates, times, units, percentages, ranges, prices, and counts;
- quotations and their speakers or sources;
- commands, paths, URLs, identifiers, API names, fields, flags, schemas, logs,
  errors, stack traces, and code;
- legal, medical, financial, scientific, and domain-specific terms;
- titles, labels, examples under discussion, and secondhand text.

A protected value includes what it modifies. Keeping `30%` while attaching it
to a different metric is still a fidelity failure.

## Semantic ledger

Before editing, silently record the source relationships below. Recheck them
after editing.

| Relationship | Examples of drift to prevent |
|---|---|
| actor → action → object | a tool becomes a team decision; a user action becomes automatic |
| entity → value → unit | latency becomes throughput; monthly becomes daily |
| source → claim | “the report says” becomes an unattributed fact |
| condition → outcome | a result that holds only when cached becomes unconditional |
| cause → effect | correlation becomes causation; sequence becomes cause |
| plan → progress → completion | “proposed” becomes “started”; “started” becomes “shipped” |
| possibility → likelihood → certainty | may/can becomes will/is |
| comparison direction | faster becomes slower; lower risk becomes higher confidence |
| effect type | easier becomes faster; adoption becomes satisfaction |
| owner or scope | one team becomes the whole company; a subset becomes all users |

Preserve negation, exceptions, prerequisites, temporal order, and the strength
of evaluative language.

Do not promote rhetorical syntax into a factual relationship. In particular,
rewriting `ensuring`, `highlighting`, or `demonstrating` as `ensured`,
`highlighted`, or `demonstrated` can strengthen an unsupported outcome or
evidence claim even when the vocabulary looks equivalent.

Jargon can still carry a real action or state. Replacing `完成闭环`, `落地`, or
similar wording does not authorize deleting the underlying claim that something
was completed, implemented, started, or planned. If the object remains abstract,
keep it abstract and preserve the lowest-commitment literal meaning available
from the source.

## Unsupported claims

This skill does not verify the world. Treat unsourced claims as claims made by
the source:

- Keep `研究表明`, `experts say`, and similar attribution if removing it would
  turn the sentence into a direct assertion.
- Do not invent a study, institution, year, sample size, link, or quotation.
- Do not replace a vague statement with a plausible specific one.
- In audit mode, flag missing attribution when it materially affects trust.
- In rewrite mode, keep the epistemic status. If the sentence is pure rhetoric
  and carries no claim or unique information, it may be removed under the
  selected scope.

## Voice and stance

Preserve the writer’s degree of confidence, approval, criticism, humor,
uncertainty, and emotional distance. Never add an opinion because neutral prose
looks “too clean.” Neutrality is correct in many technical, legal, academic,
and reference contexts.

Voice samples guide style, not substance. They cannot authorize invented facts,
experiences, feelings, or claims.

## File boundaries

In file mode:

- preserve YAML/TOML/JSON frontmatter and configuration byte-for-byte;
- preserve fenced and inline code, command blocks, tables used as data, and
  machine-readable structures;
- preserve Markdown/HTML link targets, anchors, and image paths;
- preserve heading levels and document topology in `balanced` or `in-place`;
- avoid formatting-only churn outside the requested prose.

If prose and structured data are mixed in the same line, make the smallest safe
edit or leave the line unchanged.

## Final fidelity pass

Compare source and revision in this order:

1. protected spans;
2. actor/action/object relationships;
3. numbers and their modified objects;
4. modality, negation, conditions, and completion state;
5. attribution, quotations, and evidence boundaries;
6. unique information and argument order required by the chosen scope;
7. file structure and link targets.

Revert any change that cannot be justified from the source or an explicit user
instruction.
