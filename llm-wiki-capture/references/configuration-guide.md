# LLM Wiki Capture Configuration Guide

Read this guide when the user asks how to install, configure, or operationalize
`llm-wiki-capture` for their own environment.

This guide is intentionally generic. The shared skill defines the capture
workflow; each user should define local paths, policies, and automation style
in their own `AGENTS.md` or equivalent local agent instructions.

Keep the shared skill generic. Put machine-specific wiring and personal
preferences in local instructions rather than hard-coding them into the public
skill.

Configuration inspiration can also come from shell-level helper patterns such
as Karpathy's gist:

- https://gist.github.com/karpathy/1dd0294ef9567971c1e4348a90d69285

Treat that reference as background only. Runtime behavior should come from the
user's local instructions and repository docs, not from fetching an external
gist.

## Quick Start

Use this sequence:

1. initialize a wiki or knowledge-base repository
2. add local capture policy to `AGENTS.md`
3. choose a capture operating mode that matches the user's tolerance for
   interruptions and automation

## 1. Initialize The Wiki

The skill works best when the user has a durable repository for long-term
knowledge. It does not require a specific layout, but a simple starting point
looks like this:

```text
my-wiki/
  purpose.md
  schema.md
  wiki/
    index.md
    log.md
```

Recommended file roles:

- `purpose.md`: why this knowledge base exists and what belongs in it
- `schema.md`: page types, linking rules, provenance rules, and update policy
- `wiki/index.md`: top-level navigation
- `wiki/log.md`: chronological record of meaningful knowledge updates

The user can start from an existing notes repository instead. The important
part is to make the integration rules explicit somewhere the agent can read.

## 2. Configure `AGENTS.md`

The local `AGENTS.md` should answer the environment-specific questions that a
shared public skill should not hard-code.

The exact headings and keys do not matter. What matters is that the local
instructions make the environment-specific values explicit and stable.

At minimum, configure:

- knowledge base root path
- clone URL, if missing repositories should be cloned automatically
- integration branch
- pages to read before writing
- pages to update after a successful knowledge edit
- clean-worktree policy
- commit and push policy
- commit identity, if commits are allowed
- review-only fallback rules when evidence is insufficient

Minimal example:

```markdown
## LLM Wiki Capture Config
- Knowledge base root: ~/path/to/my-wiki
- Clone URL: git@github.com:you/my-wiki.git
- Integration branch: main
- Read first: purpose.md, schema.md, wiki/index.md, wiki/log.md
- Update after knowledge edits: wiki/index.md, wiki/log.md
- Require clean worktree before capture: yes
- Commit policy: commit-and-push
- Commit identity: Your Name <you@example.com>
```

More opinionated example:

```markdown
## LLM Wiki 长期知识和记忆
- 长期记忆知识库位于 `~/path/to/my-wiki`。
- 凡是要写入这个 Wiki，先读 `purpose.md`、`schema.md`、`wiki/index.md`、`wiki/log.md` 和相关 owner pages。
- 写入必须 evidence-backed；没有原始 session 或明确 source material 时，降级为 review-only。
- 普通 capture 保持轻量；只有明确要求时才做 full integration。
- 优先更新 canonical owner，必要时才新建页面；知识变更后同步更新 `wiki/index.md` 和 `wiki/log.md`。
- 默认要求 clean worktree、fast-forward only、push 前先 fetch；push 被拒绝时停止并报告。
- 任务结束后，如果有值得长期保存的内容，可以提醒我使用 `llm-wiki-capture`。
```

The exact wording does not matter. The agent only needs stable, explicit local
rules.

## 3. Configure User Preferences

Encourage the user to choose preferences instead of inheriting yours.

Useful preference knobs:

- notification style: ask before capture, recommend capture, or run silently
- write scope: review-only, diff-only, commit locally, or commit-and-push
- trigger style: explicit invocation only, end-of-task review, or scheduled
  recap
- branch strategy: direct-to-main, fixed integration branch, or per-capture
  branch
- source-ingest policy: first-hop references only, or more aggressive manual
  research when explicitly requested
- asset policy: text-first, store transcripts only, or keep selected evidence
  files
- verbosity: short capture summary or detailed provenance report

Good defaults for most users:

- explicit invocation or end-of-task review
- evidence-backed only
- clean-worktree required
- commit allowed only after verification
- push only on confirmation or on trusted personal repositories

## 4. Operating Modes

There is no single correct automation policy. Offer the user a few patterns and
explain the tradeoff.

### Option A: Automatic Capture After Every Turn

Pattern:

- after each conversation turn, the host automatically invokes
  `llm-wiki-capture`
- the skill reviews the turn and writes durable memories immediately when the
  local policy allows it

Good for:

- personal workflows where the user wants aggressive automation
- low-friction memory accumulation

Tradeoffs:

- can create noise if the inclusion policy is weak
- can surprise users if it commits or pushes without clear expectations

Suggested `AGENTS.md` policy snippet:

```markdown
- After every turn, run a lightweight memory review.
- Only write evidence-backed, reusable knowledge.
- If nothing durable is worth saving, do nothing.
- Keep user-facing reporting short unless a real capture happened.
```

### Option B: End-Of-Task Review

Pattern:

- when a task appears complete, the system performs a quick review for
  capture-worthy knowledge
- depending on local preference, it either reminds the user or handles the
  review silently

Good for:

- users who want capture without constant interruption
- task-oriented workflows where the best memories emerge at the end

Tradeoffs:

- weaker for long conversations with multiple independent insights
- requires the host to detect task boundaries reasonably well

Suggested `AGENTS.md` policy snippet:

```markdown
- At the end of each task, check whether the work produced durable knowledge.
- If yes, either remind me to capture it or run a quiet capture pass, depending
  on the current repo and task sensitivity.
- Do not expose noisy review chatter unless I ask.
```

### Option C: Scheduled Recap

Pattern:

- the user runs a daily or weekly automation that reviews recent sessions,
  notes, or source material and captures the durable pieces

Good for:

- users who prefer batching
- teams or individuals who already use periodic review habits

Tradeoffs:

- memories are captured later, so context may be colder
- requires host-level automation support

Suggested `AGENTS.md` policy snippet:

```markdown
- Support periodic memory maintenance runs.
- Prefer a daily or weekly recap over constant capture when the user values low
  interruption.
- During recap runs, favor review-first behavior unless the automation
  explicitly permits writing.
```

## 5. How To Guide The User

When helping someone adopt this skill:

1. ask where they want their long-term knowledge to live
2. ask whether they want explicit-only, task-end, or scheduled capture
3. propose a small `AGENTS.md` block they can paste and edit
4. keep the first setup minimal, then refine policies after a few real uses

Avoid starting with a giant schema or a fully automated pipeline unless the
user explicitly wants that level of structure.
