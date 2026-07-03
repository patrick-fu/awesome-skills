# LLM Wiki Capture

**[中文说明](README.zh-CN.md)**

`llm-wiki-capture` helps an agent turn useful links, decisions, setup notes,
pitfalls, and work sessions into a Git-backed knowledge base you can trust
later.

The goal is simple: keep reusable knowledge out of chat history. A good capture
keeps the source, the conclusion, the owner page, and the reason it is worth
remembering.

Use your own notes repository, wiki, or Markdown knowledge base. This skill does
not force a folder layout. It follows the local rules you describe in your agent
instructions and repository docs.

## Good for

- Saving durable lessons from a debugging or implementation session.
- Turning source links, papers, posts, or docs into reusable notes.
- Recording project decisions and setup details that future agents should know.
- Reviewing a session and deciding what is worth saving before anything is
  written.

It is not a dumping ground for raw logs, temporary progress, guesses, or secrets.

## Install

```bash
npx skills add patrick-fu/llm-wiki-capture -g
```

Update later:

```bash
npx skills update -g
```

## What you need

Prepare a Git-backed knowledge base before asking the skill to write files.
Either setup works:

- Hosted Git repository: good for sync, backup, history, and optional push.
- Local Git repository: good for private experiments while still keeping diffs,
  clean-worktree checks, and history.

The agent needs enough local context to work safely:

- where the knowledge base lives;
- which docs explain its purpose and structure;
- which index or log files should be updated after edits;
- whether commit or push is allowed.

## Quick start

1. Create or choose a Git repository for your knowledge base.
2. Add a small doc that explains how the knowledge base is organized.
3. Add local agent instructions with the repository path, read-first files,
   update-after files, and commit policy.
4. Invoke `$llm-wiki-capture` and name the mode you want.

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

For setup patterns and policy choices, read
[`references/configuration-guide.md`](references/configuration-guide.md).

## Modes

### Source ingest

Use Source Ingest when you provide URLs, documents, files, or other explicit
source material.

The agent treats the provided sources as evidence, deduplicates before writing,
and integrates stable claims into the knowledge base with provenance.

Example:

```text
$llm-wiki-capture

Ingest these two articles into my LLM wiki. Keep the raw source notes separate
from durable conclusions, deduplicate against anything already captured, and
update the relevant concept pages.
```

### Capture

Use Capture when the current AI session produced reusable decisions, constraints,
commands, pitfalls, domain facts, or operating rules.

Capture should write only evidence-backed memories. If the agent cannot access
the source material or session evidence, it should downgrade to Review and report
what it would capture instead of editing the wiki.

Example:

```text
$llm-wiki-capture

Capture the reusable lessons from this debugging session.
```

### Review

Use Review when you want candidates without file edits. Review reports likely
memories, evidence, owner pages, and reasons to skip weak candidates.

Example:

```text
$llm-wiki-capture

Review this session and tell me whether anything is worth saving. Do not edit
the wiki yet.
```

### Full integration

Use Full Integration only when you want a broader maintenance pass over an
existing knowledge base: weak ownership, missing provenance, duplicate pages, and
links between related notes.

## Safety boundaries

- Keep secrets, tokens, credentials, private keys, temporary logs, noisy
  progress, and unsupported guesses out of the knowledge base.
- When required local configuration is missing, ask once. If the user does not
  want to configure it, downgrade to Review.
- Commit or push only when local policy allows it.
- Fetch before pushing and stop on non-fast-forward conflicts.
- Prefer updating an existing owner page over creating a duplicate page.

## Background

This skill is inspired by practical long-term memory workflows such as
[Karpathy's memory gist](https://gist.github.com/karpathy/1dd0294ef9567971c1e4348a90d69285).
The gist is a useful reference for the broader idea: AI sessions can feed a
personal knowledge base when the capture loop is explicit and maintained.

`llm-wiki-capture` does not depend on that gist or require its exact setup.
Runtime behavior comes from this skill, your local agent instructions, and your
knowledge-base repository docs.

## More curated skills

Browse my curated collection of practical agent skills:
[Awesome Skills](https://github.com/patrick-fu/awesome-skills).
