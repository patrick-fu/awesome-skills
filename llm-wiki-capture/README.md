# LLM Wiki Capture

**[中文说明](README.zh-CN.md)**

`llm-wiki-capture` helps an agent turn explicit sources and AI work sessions
into durable, evidence-backed updates for a Git-backed long-term knowledge base.

It is not a generic memory dump. The skill asks the agent to find canonical
owners, preserve provenance, respect local write policy, verify changes, and
avoid saving secrets, one-off progress, or unsupported guesses.

## Install

```bash
npx skills add patrick-fu/llm-wiki-capture
```

Update later:

```bash
npx skills update
```

## What You Need

Prepare a Git-backed knowledge base before expecting the skill to write files.
Two setups work well:

- **Hosted Git repository**: GitHub, GitLab, Codeberg, a company Git host, or a
  self-hosted Git service. This is the best fit when you want cross-machine sync,
  backup, commit history, and optional push.
- **Local Git repository**: a `git init` repository on one machine. This works
  well for private or early experiments, while still giving the agent diffs,
  clean-worktree checks, and commit history.

The skill does not require a specific wiki layout, but it does need local
instructions that say where the knowledge base lives, what files define the
schema, what navigation files should be updated, and whether commit or push is
allowed.

## Quick Start

1. Create a Git repository for your knowledge base.
2. Add a small structure such as `purpose.md`, `schema.md`, `wiki/index.md`, and
   `wiki/log.md`.
3. Add local agent instructions that define the knowledge-base root, branch,
   read-first files, update-after files, clean-worktree policy, and commit/push
   policy.
4. Invoke the skill explicitly with `$llm-wiki-capture`.

Minimal local instruction block:

```markdown
## LLM Wiki Capture
- Knowledge base root: ~/path/to/my-wiki
- Clone URL: git@github.com:you/my-wiki.git
- Integration branch: main
- Read first: purpose.md, schema.md, wiki/index.md, wiki/log.md
- Update after knowledge edits: wiki/index.md, wiki/log.md
- Require clean worktree before capture: yes
- Commit policy: no-commit, commit-only, or commit-and-push
- Commit identity: Your Name <you@example.com>
- If raw session evidence or user-provided source material is unavailable,
  downgrade to review and do not edit the knowledge base.
```

See [`examples/minimal-wiki`](examples/minimal-wiki) for a small starter
knowledge base and [`references/configuration-guide.md`](references/configuration-guide.md)
for configuration options.

## Main Modes

### Source Ingest

Use Source Ingest when you provide URLs, documents, files, or other explicit
source material.

The agent should treat the provided sources as evidence. It may resolve
canonical URLs, fetch explicit originals, compare translations or
interpretations with the original, and gather relevant first-hop references. It
should deduplicate before writing and integrate stable claims into the knowledge
base with provenance.

Example:

```text
$llm-wiki-capture

Ingest these two articles into my LLM wiki. Keep the raw source notes separate
from durable conclusions, deduplicate against anything already captured, and
update the relevant concept pages.
```

### Capture

Use Capture when the current AI session produced reusable decisions, constraints,
commands, pitfalls, domain facts, or operating rules that should be saved.

Capture writes only evidence-backed memories. If the agent cannot access the raw
session record or user-provided source material, it should downgrade to Review
and report what it would capture instead of editing the knowledge base.

Example:

```text
$llm-wiki-capture

Capture the reusable lessons from this debugging session.
```

### Review

Use Review when you want the agent to inspect candidates without writing files.
Review mode makes no edits, commits, or pushes. It should report candidate
memories, evidence, likely owner pages, and reasons to skip weak candidates.

Example:

```text
$llm-wiki-capture

Review this session and tell me whether anything is worth saving. Do not edit
the wiki yet.
```

### Full Integration

Full Integration is an advanced maintenance mode for an existing knowledge base.
It asks the agent to inspect the graph, repair weak ownership, improve
provenance, connect related sources, and surface durable synthesis. Use it only
when you explicitly want a broader library maintenance pass.

## Safety Boundaries

- Do not capture secrets, tokens, credentials, private keys, temporary logs,
  noisy progress, or unsupported guesses.
- Do not write when required local configuration is missing. Ask once, then
  downgrade to Review if the user does not want to configure it.
- Do not commit or push unless local policy allows it.
- Fetch before pushing and stop on non-fast-forward conflicts instead of
  force-pushing.
- Prefer updating existing canonical owner pages over creating duplicate pages.

## Background

This skill is inspired by practical long-term memory workflows such as
[Karpathy's memory gist](https://gist.github.com/karpathy/1dd0294ef9567971c1e4348a90d69285),
but it does not depend on that gist or require its exact setup. Runtime behavior
comes from this skill, your local agent instructions, and your knowledge-base
repository docs.

## More Skills

For more reusable agent skills, see
[Awesome Skills](https://github.com/patrick-fu/awesome-skills).
