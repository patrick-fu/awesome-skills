# Boundary cases and false positives

Use this file whenever a match is uncertain. The cost of erasing real voice or
changing meaning is higher than leaving one weak slop signal behind.

## Do not flag in isolation

- one em dash, semicolon, curly quote, emoji, or bold phrase;
- one three-item list;
- one transition such as *however*, `此外`, or `因此`;
- one fashionable or formal word;
- a short sentence or sentence fragment;
- first person, neutrality, passive voice, or a rhetorical question;
- clean formatting produced by an editor or template.

Look for repetition, density, generic use, and mismatch with the scene.

## Legitimate structures

- Academic methods and scientific summaries often use passive voice.
- Legal, policy, and compliance writing may need repetition, modality, and
  formal definitions.
- Reference documentation may use repeated terms, uniform headings, lists, and
  system subjects for reliable lookup. RFCs, API specifications, and structured
  requirements may be deliberately uniform.
- Tutorials and educational material may use previews, recaps, repetition, and
  staged examples to support navigation and learning.
- Practitioner-led public writing may use first-person failures, explicit
  knowledge limits, functional technical code-switching, sparse slang or emoji,
  fragments, and callouts as genuine evidence or voice.
- Titles, pull quotes, callouts, media companions, and conclusions may repeat a
  thesis when they have a distinct rendering, navigation, synthesis, consequence,
  or action role. A block label alone is not such a role; judge what the block
  does before protecting or compressing the recurrence.
- Release notes and migration guides legitimately describe additions, removals,
  and changes.
- Marketing copy may be promotional because promotion is its job; remove only
  templated excess while preserving its claims, audience, and brief.
- Chat may include warmth, emoji, fragments, and repetition as genuine social
  signals.

## Literal technical language

Words that are often slop can be exact terms: financial *leverage*, graph
*traversal*, network *routing*, ecosystem APIs, model alignment, a product named
*Landscape*, or a field literally called `summary`. Preserve literal meaning,
defined terms, identifiers, and quoted examples.

## Human signals worth preserving

- unusual, source-backed specifics;
- mixed feelings and unresolved tension;
- defensible opinions and uncertainty;
- era-bound slang, in-jokes, and local register;
- genuine asides, self-correction, and intentional repetition;
- uneven rhythm that follows thought rather than a template;
- awkwardness that carries identity or precise meaning.

Do not “repair” these into generic polish.

Repeated phrasing is not automatically intentional voice. Across a long text,
preserve recurrence that adds a new mechanism, example, consequence, or block
function; compress recurrence that only paraphrases the same thesis.

When only a final draft is available, audit the draft that exists. Do not claim
that an earlier edit improved, damaged, or introduced the voice without the
earlier version or revision evidence.

## Text about AI-writing patterns

When watched words or structures appear inside quotations, titles, examples,
or analysis, they are content under discussion. Preserve them. The same applies
to test fixtures and before/after examples.

## Already-natural input

If the prose fits its scene, preserves a coherent voice, and contains no cluster
of high-confidence slop signals, use the no-op contract. Invocation is not proof
that a rewrite is needed.

## Requests to beat a detector

Deslop does not optimize for detector scores or claim human authorship. It may
still edit the prose for clarity and naturalness, but refuse to promise a score,
guarantee evasion, or fabricate “human” noise for that purpose.
