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

Build lively HTML slide decks that can survive real iteration: style previews,
motion, interaction, navigation, screenshots, PDF export, and online delivery.

Use it when a deck needs to look good, feel alive, and stay editable after the
first version.

Standalone page: [`patrick-fu/frontend-harness-slides`](https://github.com/patrick-fu/frontend-harness-slides)

### 🧭 `parallel-goal-workflows`

Coordinate complex work without dumping every subtask into the main
conversation. It helps an agent split broad goals, run focused helpers when that
is useful, review the results, and return a clean final report.

Use it for audits, research, repair loops, or any task where independent checks
matter.

Standalone page: [`patrick-fu/parallel-goal-workflows`](https://github.com/patrick-fu/parallel-goal-workflows)

### 📚 `llm-wiki-capture`

Turn links, decisions, setup notes, and useful agent sessions into a Git-backed
knowledge base with enough evidence to be trusted later.

Use it when something from a session should still be findable next month.

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

- `llm-wiki-capture`: Save reusable source notes and session lessons into a
  Git-backed wiki or knowledge base.
- `x-twitter-reader`: Read X/Twitter posts, threads, Articles, metadata, links,
  and media before summarizing or archiving them.

### Agent orchestration

- `parallel-goal-workflows`: Split complex work into owned goals, focused helper
  work, review, repair, and final reporting.
- `claude-code-coding-agent`: Use Claude Code CLI as an explicitly selected
  external coding agent.
- `codex-coding-agent`: Use local Codex CLI from another host agent or
  automation harness.
- `cursor-coding-agent`: Use Cursor CLI when Cursor is the chosen external
  executor.

### Thinking and planning

- `brainstorm`: Explore a rough idea before turning it into a plan.
- `explore-and-plan`: Turn a mostly chosen direction into executable steps and
  acceptance checks.
- `faster-learning-coach`: Convert explanations into short learning loops with
  practice and review.

### Engineering workflow

- `write-unit-test`: Write or improve unit tests around behavior, regressions,
  and domain rules.
- `log-driven-debugging`: Add targeted logs, rerun the real scenario, and trace
  the first useful divergence.
- `commit-staged-changes`: Commit only staged changes with a factual English
  message.
- `generate-commit-message`: Draft a commit message from the staged diff without
  creating the commit.

### Personal setup

- `home-config-sync`: Manage a personal `~/.dotfiles` bare-repo workflow,
  including first setup, new-machine deploys, pull safety, and pushes.
