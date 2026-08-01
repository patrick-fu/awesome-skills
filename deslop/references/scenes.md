# Scene routing

Use the scene to decide what “natural” means. Do not make every genre casual.

| Scene | Default scope | Preserve | Remove first |
|---|---|---|---|
| chat or direct reply | balanced | answer, boundaries, social intent | therapy voice, praise, repeated framing |
| status update | balanced | owner, action, result, blocker, next step | executive theater, vague progress language |
| technical/reference docs | balanced | terminology, topology, conditions, examples | narrator voice, promotional claims, redundant recap |
| public article or essay | balanced | thesis, arc, rhythm, stance, intentional repetition | generic hooks, false profundity, canned conclusions |
| marketing copy | balanced | product claims, audience, platform register, CTA | interchangeable hype, fake intimacy, repeated slogans |
| email or issue reply | balanced | request, decision, accountability, politeness level | throat-clearing, defensive over-explanation |
| release note or changelog | balanced | change, impact, compatibility, migration facts | significance inflation, feature-marketing filler |
| README | balanced | task path, commands, constraints, links | welcome-tour narration, repeated feature summaries |

## Chat and direct replies

Answer before explaining. Match the relationship and stakes. Do not diagnose the
other person’s emotions or open with automatic praise. Keep genuine warmth and
necessary politeness.

## Status updates

Prefer observable work and current state. Preserve who owns each action, what is
blocked, and whether something is proposed, underway, verified, or shipped. Do
not convert uncertainty into executive confidence.

## Technical and reference documents

Accuracy, consistency, and scanability outrank personality. Keep defined terms,
repetition needed for reference lookup, schema-shaped sections, normal passive
voice, and system subjects. Do not turn documentation into conversation.

## Public writing

Preserve the thesis, sequence, and author’s real stance. Remove generic hooks,
performed intimacy, slogan endings, and listicle scaffolding. Do not inject
first person, controversy, humor, or a personal anecdote without source support
or a supplied voice sample.

For long text under `balanced`, preserve headings, paragraph roles, and argument
order. Local sentence repair is preferred to global compression.

Marketing copy is not neutral documentation. Preserve its selling purpose,
claims, audience, platform register, and CTA. Remove formulaic excess without
silently fact-checking the offer or flattening it into generic product prose.

## README, release note, issue, and email

- **README:** Keep installation and usage paths direct. Commands and link targets
  are protected. A short summary can be useful; repeated tours are not.
- **Release note:** Diff-oriented language is legitimate. Preserve compatibility,
  version, migration, and rollout details exactly.
- **Issue reply:** State the observed behavior, decision, and next action. Avoid
  pretending confidence or empathy not present in the source.
- **Email:** Preserve politeness and relationship signals. “Concise” is not a
  license to make the sender colder or more forceful.

## Scope overrides

- Use `in-place` when the user asks to keep structure, sentence count, layout,
  or review comments anchored to existing text.
- Use `rebuild` only for an explicit rewrite, compression, reorganization, or
  new target genre.
- In file mode, `balanced` still preserves document topology and protected
  regions. File editing never implies `rebuild`.
