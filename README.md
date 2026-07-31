# Awesome Skills

**[中文说明](README.zh-CN.md)**

My personal collection of agent skills for coding, planning, knowledge capture,
slides, multi-agent work, and day-to-day setup.

I keep this collection small enough to browse, but broad enough to cover the
workflows I actually reach for: making better plans, writing safer code,
building richer HTML slides, saving reusable knowledge, coordinating complex
agent work, and keeping my local setup repeatable.

## Install the collection

```bash
npx skills add patrick-fu/awesome-skills -g
```

Update later:

```bash
npx skills update -g
```

The full collection is the easiest starting point. If one of the larger skills
below is what you came for, its standalone page gives a more focused walkthrough
and a one-skill install command.

## Featured skills

### 🎞️ `frontend-harness-slides`

Build lively HTML slide decks with a frontend harness: stable scenes, repeatable
screenshots, meaningful tests, PDF export, and online delivery.

Use it when a deck needs to look good, feel alive, and stay hard to break after
many rounds of edits.

> 🖥️ Live demo: try the
> [dynamic Workbench Demo](https://frontend-harness-slides-workbench.vercel.app/).
> The visual styles are useful, but the bigger win is harness-backed iteration
> instead of fragile single-file HTML.

Standalone page: [`patrick-fu/frontend-harness-slides`](https://github.com/patrick-fu/frontend-harness-slides)

### 🧭 `parallel-goal-workflows`

Coordinate complex work without dumping every subtask into the main
conversation. It delegates each explicitly invoked top-level goal to one Goal
Owner, which owns execution, optional focused helpers, review, verification,
and the final report.

Use it for audits, research, repair loops, or any task where independent checks
matter.

Standalone page: [`patrick-fu/parallel-goal-workflows`](https://github.com/patrick-fu/parallel-goal-workflows)

### 🤖 External coding agents

Run Claude Code, Codex, Cursor, or Grok as an explicitly selected external
coding executor from another host agent. The guides share one compact workflow
for wrappers, model and reasoning-effort selection, monitored streaming,
permissions, sandboxes, and host-side verification.

Choose an executor: [`claude-code-coding-agent`](./claude-code-coding-agent) ·
[`codex-coding-agent`](./codex-coding-agent) ·
[`cursor-coding-agent`](./cursor-coding-agent) ·
[`grok-coding-agent`](./grok-coding-agent)

### 📚 `llm-wiki-capture`

Capture session lessons and external sources into a maintained Git-backed LLM
Wiki, audit an existing Wiki, or bootstrap one from zero. It preserves
provenance and canonical ownership while keeping repository mutations explicit.

Standalone page: [`patrick-fu/llm-wiki-capture`](https://github.com/patrick-fu/llm-wiki-capture)

## Install one skill

```bash
npx skills add patrick-fu/frontend-harness-slides -g
npx skills add patrick-fu/parallel-goal-workflows -g
npx skills add patrick-fu/llm-wiki-capture -g
```

If you install the full collection and later install a standalone skill in the
same global scope, the standalone version replaces that one local skill. It does
not create a second copy.

## What's inside

### Slides and visual delivery

- `frontend-harness-slides`: HTML slide decks with style alignment, interaction,
  motion, screenshot checks, PDF export, and online delivery.

### Knowledge and memory

- `llm-wiki-capture`: Capture sessions and sources, audit an existing LLM Wiki,
  or bootstrap one from zero with explicit repository boundaries.
- `x-twitter-reader`: Read X/Twitter posts, threads, Articles, metadata, links,
  and media before summarizing or archiving them.

### Communication and writing

- `be-concise`: Keep agent responses brief and direct without dropping details
  needed for correctness, safety, or action.

### Agent orchestration

- `parallel-goal-workflows`: Delegate each top-level goal to one Goal Owner for
  execution, focused helpers when useful, review, repair, and final reporting.
- `claude-code-coding-agent`: Use Claude Code CLI as an explicitly selected
  external coding agent.
- `codex-coding-agent`: Use local Codex CLI from another host agent or
  automation harness.
- `cursor-coding-agent`: Use Cursor CLI when Cursor is the chosen external
  executor.
- `grok-coding-agent`: Use Grok Build CLI when Grok is the explicitly selected
  external coding agent.

### Thinking and planning

- `brainstorm`: Broaden an idea or open problem into a possibility map of
  genuinely different directions before choosing where to go deeper.
- `explore-and-plan`: Turn a mostly chosen direction into executable steps and
  acceptance checks.
- `faster-learning-coach`: Convert explanations into short learning loops with
  practice and review.

### Engineering workflow

- `write-unit-test`: Write or improve unit tests around behavior, regressions,
  and domain rules.
- `log-driven-debugging`: Add targeted logs, rerun the real scenario, and trace
  the first useful divergence.
- `generate-commit-message`: Draft a concise English commit message with simple
  formatting constraints.

### Personal setup

- `home-config-sync`: Manage a personal `~/.dotfiles` bare-repo workflow,
  including first setup, new-machine deploys, pull safety, and pushes.
