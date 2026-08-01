---
name: deslop
description: >-
  Review or rewrite existing Chinese, English, or mixed-language prose to remove
  formulaic AI-slop patterns while preserving facts, intent, stance, register,
  and author voice. Use when the user explicitly asks to deslop, humanize,
  remove AI writing patterns or AI 味, 说人话, 别像模板/机器人, make text less
  AI-generated, or audit a draft for those problems. Do not trigger for generic
  polishing, proofreading, translation, summarization, fact-checking, or
  drafting from scratch unless deslop is explicitly requested as a step.
---

# Deslop / 说人话

Edit existing prose so it sounds like a person making deliberate choices in a
specific context, not a model performing “human” style. Preserve truth before
style. A slightly awkward faithful sentence is better than a fluent invention.

This is an editorial skill, not an AI detector. Never assign an AI probability,
promise detector evasion, or treat one word or punctuation mark as proof of
authorship.

## Route the request

Choose one delivery mode:

- **Rewrite** — default. Return one ready-to-use revision.
- **Audit** — only when the user asks to inspect, review, mark, or explain
  problems before rewriting. Report findings; do not silently rewrite.
- **Embedded** — when another workflow needs prose as an intermediate result.
  Return only the final text, without process notes. If ambiguity remains,
  preserve the more conservative source wording instead of guessing.
- **File** — only when the user explicitly asks to edit a file. Modify prose in
  place while preserving protected file regions, then summarize the change.

A user-provided writing sample adds **voice calibration** to any mode. It does
not create a separate mode and never relaxes factual fidelity.

Choose an edit scope:

- **balanced** — default. Reshape short text freely without deleting unique
  information. In long text, also preserve headings, paragraph roles, and
  argument order. Remove only demonstrably empty scaffolding.
- **in-place** — when the user asks to keep the structure, sentence count, or
  layout. Rewrite within sentences; do not delete, merge, or reorder them.
  If a sentence contains only slop, keep an awkward source-faithful shell or
  the original sentence rather than inventing a concrete object or outcome.
- **rebuild** — only when the user explicitly asks for a substantial rewrite,
  compression, or reorganization. Preserve the semantic ledger even when the
  shape changes.

## Load only the needed references

Always read [fidelity.md](references/fidelity.md). Then load selectively:

- Chinese or Chinese-dominant mixed text:
  [patterns-zh.md](references/patterns-zh.md)
- English or English-dominant mixed text:
  [patterns-en.md](references/patterns-en.md)
- Genre, register, or long-form decisions:
  [scenes.md](references/scenes.md)
- A supplied author sample or explicit voice-matching request:
  [voice-calibration.md](references/voice-calibration.md)
- Natural text, quotations, academic/legal/technical prose, or any uncertain
  match: [boundary-cases.md](references/boundary-cases.md)

For mixed-language text, read both language pattern files but judge each phrase
in its local linguistic and technical context.

## Rewrite loop

1. **Read for meaning.** Identify the document’s job, audience, register, and
   the author’s actual position.
2. **Build a silent semantic ledger.** Record protected spans and relationships:
   who did what, to what, when, with what status, evidence, strength, and effect.
3. **Find clusters, not tokens.** Look for repeated formulaic structures,
   generic framing, performative transitions, flattened rhythm, and register
   mismatch. Do not rewrite merely because a watched word appears once.
4. **Rewrite toward the scene.** Prefer direct claims, concrete source-backed
   detail, natural sentence boundaries, and an appropriate amount of
   irregularity. Do not manufacture personality.
5. **Run the fidelity pass.** Compare every fact, number, name, attribution,
   relationship, modality, completion state, quotation, term, and protected
   file region against the source. Revert any unsupported change.
6. **Run the residual pass.** Remove remaining high-confidence slop without
   sanding away legitimate voice or genre conventions.
7. **Consider no-op.** If the source is already natural and fit for purpose,
   leave it alone. One weak signal is not enough to justify a rewrite.

## Hard boundaries

- Do not invent facts, examples, citations, dates, measurements, product
  capabilities, feedback, emotions, opinions, or first-person experience.
- Do not turn vague attribution into direct fact, or uncertainty into certainty.
- Do not change the actor, owner, object, direction, completion state, causal
  relationship, comparison, or type of effect.
- Keep quotations, titles, proper names, technical terms, commands, paths,
  identifiers, logs, schemas, and literals exact unless the user explicitly asks
  to edit them.
- In file mode, preserve frontmatter, code blocks, inline code, structured data,
  and link destinations. Edit link labels only when prose editing requires it.
- Treat unsupported claims as source content, not permission to fact-check.
  Preserve their attribution and confidence. In audit mode, note that a source
  is missing; in rewrite mode, do not add one or silently promote the claim.
- Never fetch or infer private voice samples. Use only material the current user
  explicitly supplies for the current task, and do not persist it.

## Positive target

Aim for prose that:

- says the useful thing without announcing that it is about to say it;
- uses the register the situation calls for, including neutral technical prose;
- varies rhythm when natural, without forced fragments or manufactured punch;
- preserves unusual, specific, defensible details already in the source;
- keeps uncertainty, mixed feelings, asides, repetition, and rough edges when
  they belong to the author;
- can be read aloud without sounding like a presentation script.

“More human” does not mean more casual, more emotional, more first-person, or
less precise. It means less statistically generic and more faithful to the
author, audience, and purpose.

## Output contracts

### Rewrite

Return one recommended revision. Do not show a draft, score, internal ledger,
or self-audit. Add a brief note only when a material ambiguity or fidelity risk
cannot be resolved from the source. In long or mixed-quality text, edit only the
parts that need it and return the rest unchanged.

### Audit

Return only material findings, normally one to five. For each finding include:

- the exact excerpt;
- the pattern and why it matters here;
- the fidelity or register risk, when one exists;
- a concrete editing direction.

Do not flag isolated words without contextual evidence.

If there are no material findings, say so and do not invent issues to fill the
format.

### File

Edit only the requested file. If the final prose is unchanged, do not rewrite
the file. Report the path and a short summary instead of pasting the full file.

### No-op

In rewrite or embedded mode, return the exact input without a preamble. In file
mode, retain the file byte-for-byte and report that no change was needed. In
audit mode, say there are no material findings.
