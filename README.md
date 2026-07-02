# Awesome Skills

**[中文说明](README.zh-CN.md)**

A practical collection of agent skills for planning, engineering workflows,
slides, knowledge capture, external coding agents, and personal setup.

## Quick Install

Install the full collection globally:

```bash
npx skills add patrick-fu/awesome-skills -g
```

Update global skills:

```bash
npx skills update -g
```

## Highlights

These three larger skills are included in the collection above. They also have
standalone repositories when you want to install only that skill or read the
full README, references, evals, and examples.

### 🎞️ `frontend-harness-slides`

Build HTML slide decks that stay editable after the first draft. This skill
helps an agent align on style, audience, stage size, interaction, and delivery
target, then use a harness, screenshots, and export checks so later edits do not
quietly break other slides.

Best for talks, product walkthroughs, teaching decks, or any slide project where
motion, navigation, PDF export, and online deployment matter.

```bash
npx skills add patrick-fu/frontend-harness-slides -g
```

Repository: [`patrick-fu/frontend-harness-slides`](https://github.com/patrick-fu/frontend-harness-slides)

### 🧭 `parallel-goal-workflows`

Run complex work without stuffing every subtask into one conversation. The Main
Agent turns a broad request into clean local briefs, starts one Goal Owner per
top-level goal, and keeps review, repair, acceptance, and final reporting
separated.

Best when a task benefits from parallel research, implementation, review, or
multiple independent checks.

```bash
npx skills add patrick-fu/parallel-goal-workflows -g
```

Repository: [`patrick-fu/parallel-goal-workflows`](https://github.com/patrick-fu/parallel-goal-workflows)

### 📚 `llm-wiki-capture`

Capture reusable knowledge from source links and agent sessions into a
Git-backed long-term wiki. It keeps evidence, ownership, verification, and local
commit/push policy visible, so future agents can reuse knowledge instead of
depending on chat history.

Best for patterns, decisions, setup notes, and lessons you expect to need again.

```bash
npx skills add patrick-fu/llm-wiki-capture -g
```

Repository: [`patrick-fu/llm-wiki-capture`](https://github.com/patrick-fu/llm-wiki-capture)

## Skill Groups

`npx skills add patrick-fu/awesome-skills -g` shows these groups in the
interactive installer.

### Slides and visual delivery

- `frontend-harness-slides`: Create high-standard HTML slide decks with
  upfront alignment, lively motion and interactions, harness-based iteration,
  screenshots, PDF/static export, and online delivery checks.

### Knowledge and memory

- `llm-wiki-capture`: Capture reusable knowledge from source links and agent
  sessions into a maintained Git-backed wiki or knowledge base.
- `x-twitter-reader`: Extract original content from X/Twitter posts, threads,
  Articles, metadata, links, and media references before summarizing,
  translating, quoting, or archiving it.

### Agent orchestration

- `parallel-goal-workflows`: Delegate complex work through clean local briefs,
  Goal Owners, focused helpers, review, repair, acceptance, and final reporting.
- `claude-code-coding-agent`: Launch Claude Code CLI as an explicitly selected
  external executor, with patterns for automation, review-only runs, interactive
  sessions, and model or permission pass-through.
- `codex-coding-agent`: Launch local Codex CLI from another host agent or
  automation harness, including `codex exec`, `codex review`, interactive
  resume/fork flows, and Git workspace expectations.
- `cursor-coding-agent`: Launch Cursor CLI only when Cursor is explicitly
  selected, with separate guidance for headless execution, review-only
  `--mode ask`, planning mode, and interactive sessions.

### Thinking and planning

- `brainstorm`: Use it before planning or coding, when the useful work is still
  clarifying the idea, audience, constraints, and first direction.
- `explore-and-plan`: Use it after the direction is mostly chosen, when the next
  output should be an executable plan with clear steps, boundaries, and
  acceptance checks.
- `faster-learning-coach`: Use it when the user's real goal is learning. It
  turns explanations into short learning loops with practice, teach-back, and
  review.

### Engineering workflow

- `write-unit-test`: A practical guide for behavior-focused unit tests around
  production code, bug fixes, refactors, and domain rules.
- `log-driven-debugging`: A diagnosis loop for slippery bugs: add targeted logs,
  let the user rerun the scenario, then use the returned logs to find the first
  real divergence.
- `commit-staged-changes`: Commit only what is already staged, after reviewing
  the staged diff and writing a factual English commit message.
- `generate-commit-message`: Inspect the staged diff and draft the commit message
  without creating the commit.

### Personal setup

- `home-config-sync`: Initialize and operate a personal bare-repo dotfiles setup
  under `~/.dotfiles`, including first push, new-machine deploys, whitelist
  updates, pull/merge safety, and optional GUI-discoverable mode.

## Duplicate Installs

The collection and the standalone repositories use the same skill names. If you
install `awesome-skills` and later install one standalone skill in the same
global scope, the standalone install overwrites that local skill instead of
creating a duplicate copy.
