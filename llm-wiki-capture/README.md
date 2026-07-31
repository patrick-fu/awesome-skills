# LLM Wiki Capture

**[中文说明](README.zh-CN.md)**

`llm-wiki-capture` turns reusable session lessons and external sources into a
maintained, Git-backed LLM Wiki. It can also audit an existing Wiki or help a
new user bootstrap one from zero.

The skill is user-invoked. It does not capture conversations automatically,
guess which repository is yours, create a Wiki merely because none was found,
or commit and push without authorization.

## Install

```bash
npx skills add patrick-fu/llm-wiki-capture -g
```

Update later:

```bash
npx skills update -g
```

## Workflows

### Session Capture

Extract durable knowledge from the current or selected historical session:

- lessons from failures and validated fixes;
- decisions, rationale, constraints, and rejected alternatives;
- reusable SOPs, exact commands, verification, and recovery steps;
- non-obvious project facts and explicit user preferences.

Session Capture organizes knowledge by its canonical owner, not by chat
chronology. It leaves temporary progress and handoff state out of the long-term
Wiki, and it does not copy the full transcript by default.

```text
$llm-wiki-capture

Capture the reusable lessons and deployment SOP from this session.
```

### Source Ingest

Ingest explicitly supplied source material with recoverable provenance,
deduplication, value-based reference traversal, and integration into canonical
concepts.

```text
$llm-wiki-capture

Ingest this paper, its translation, and the linked benchmark into my Wiki.
```

A URL used for discussion or review is not automatically an ingest request.

### Full Integration

Audit or repair a mature Wiki across provenance, canonical ownership,
duplicates, stale knowledge, navigation, and missing synthesis. This branch
runs only when the user explicitly requests a whole-Wiki pass.

### Bootstrap

If you do not have a Wiki, explicitly ask the skill to create one. The default
starting point is a small local Git repository with purpose, schema, raw source
evidence, source summaries, canonical concepts, index, log, and a
zero-dependency `wiki-maintenance check`.

The skill recommends private hosting when cross-machine sync is useful, but it
does not create a remote or publish anything without approval.

```text
$llm-wiki-capture

I do not have a Wiki. Bootstrap a private Git-backed one under ~/notes/my-wiki,
but ask before creating a remote.
```

## Review-only

Review-only applies to every workflow. It reports evidence, candidate changes,
canonical owners, conflicts, and skips without editing files, committing,
pushing, creating repositories, or publishing externally.

```text
$llm-wiki-capture

Review this session and tell me what is worth capturing. Do not edit the Wiki.
```

## Repository discovery

You may name the Wiki directly in the request or configure it in local agent
instructions. If the skill discovers a candidate through repository or global
instructions, it asks you to confirm the candidate before using it as the Wiki
target. If it finds an existing notes repository, it inspects it read-only and
asks whether to upgrade it in place or create a separate Wiki.

Minimal optional configuration:

```markdown
## LLM Wiki
- Root: ~/path/to/my-wiki
- Read first: AGENTS.md, purpose.md, schema.md, wiki/index.md
- Validate with: scripts/wiki-maintenance check
- Require a clean worktree before edits: yes
- Commit policy: ask
- Push policy: ask
```

See
[`references/configuration-guide.md`](references/configuration-guide.md) for
target discovery and configuration ownership.

## Safety boundaries

- External material and historical transcripts remain evidence, not executable
  current instructions.
- Assistant proposals do not become durable facts without adoption or
  verification.
- Conflicting user SOPs and repository behavior are researched, then resolved
  by asking the user.
- Secrets, credentials, noisy logs, transient state, and unsupported claims stay
  out of the Wiki.
- Commit and push are separate, explicit authorization boundaries.

## Background

The architecture follows the Raw / Wiki / Schema idea in
[Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f),
then adds portable workflows for cold start, provenance-aware source ingest,
session learning, and graph maintenance.

## More curated skills

Browse [Awesome Skills](https://github.com/patrick-fu/awesome-skills).
