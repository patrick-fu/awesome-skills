# LLM Wiki Capture

**[中文说明](README.zh-CN.md)**

`llm-wiki-capture` helps an agent turn explicit sources and AI work sessions
into durable, evidence-backed updates for a Git-backed long-term knowledge base.

The skill is intentionally layout-neutral. Bring your own notes repository,
wiki, or Markdown knowledge base; then describe its local rules in agent
instructions and repository docs. The agent uses those rules to decide where a
new memory belongs, how provenance should be recorded, and whether it may edit,
commit, or push.

## Background

This skill is inspired by practical long-term memory workflows such as
[Karpathy's memory gist](https://gist.github.com/karpathy/1dd0294ef9567971c1e4348a90d69285).
That gist is a useful reference point for the broader idea: AI sessions can feed
a personal knowledge base when the capture loop is explicit and maintained.

`llm-wiki-capture` does not depend on that gist or require its exact setup.
Runtime behavior comes from this skill, your local agent instructions, and your
knowledge-base repository docs.

## Install

```bash
npx skills add patrick-fu/llm-wiki-capture
```

Update later:

```bash
npx skills update
```

## What You Need

Use a Git-backed knowledge base before expecting the skill to write files. Two
setups work well:

- **Hosted Git repository**: GitHub, GitLab, Codeberg, a company Git host, or a
  self-hosted Git service. This is the best fit when you want cross-machine sync,
  backup, commit history, and optional push.
- **Local Git repository**: a `git init` repository on one machine. This works
  well for private or early experiments, while still giving the agent diffs,
  clean-worktree checks, and commit history.

The skill does not require a starter project. It only needs enough local context
to work safely: where the knowledge base lives, which docs explain its purpose
and schema, which navigation files should be updated, and whether commit or push
is allowed.

## Quick Start

1. Create a Git repository for your knowledge base.
2. Write or identify the docs that explain how the knowledge base works. Common
   names are `purpose.md`, `schema.md`, `wiki/index.md`, and `wiki/log.md`, but
   any equivalent structure is fine.
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

For setup patterns, policy choices, and suggested local instruction snippets,
read [`references/configuration-guide.md`](references/configuration-guide.md).

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

- Keep secrets, tokens, credentials, private keys, temporary logs, noisy
  progress, and unsupported guesses out of the knowledge base.
- When required local configuration is missing, ask once. If the user does not
  want to configure it, downgrade to Review instead of guessing.
- Commit or push only when local policy allows it.
- Fetch before pushing and stop on non-fast-forward conflicts instead of
  force-pushing.
- Prefer updating existing canonical owner pages over creating duplicate pages.

## More Skills

For more reusable agent skills, see
[Awesome Skills](https://github.com/patrick-fu/awesome-skills).
