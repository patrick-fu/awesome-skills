# Awesome Skills

**[中文说明](README.zh-CN.md)**

This repository contains a small set of reusable agent skills extracted from a
larger private workspace and published as a standalone public collection.

## Quick Install

Install everything in one line: the public collection plus the three standalone
picks.

```bash
npx skills add patrick-fu/awesome-skills && npx skills add patrick-fu/frontend-harness-slides && npx skills add patrick-fu/parallel-goal-workflows && npx skills add patrick-fu/llm-wiki-capture
```

Install only the public collection:

```bash
npx skills add patrick-fu/awesome-skills
```

Update installed skills:

```bash
npx skills update
```

## Featured Skills

These larger skills have their own standalone repositories. Install them
directly when you want the full version with its references, evals, and
examples.

### 🎞️ `frontend-harness-slides`

Build HTML slide decks that stay editable after the first draft. This skill
helps an agent align on style, audience, stage size, interaction, and delivery
target, then use a harness, screenshots, and export checks so later edits do not
quietly break other slides.

Best for talks, product walkthroughs, teaching decks, or any slide project where
motion, navigation, PDF export, and online deployment matter.

```bash
npx skills add patrick-fu/frontend-harness-slides
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
npx skills add patrick-fu/parallel-goal-workflows
```

Repository: [`patrick-fu/parallel-goal-workflows`](https://github.com/patrick-fu/parallel-goal-workflows)

### 📚 `llm-wiki-capture`

Capture reusable knowledge from source links and agent sessions into a
Git-backed long-term wiki. It keeps evidence, ownership, verification, and local
commit/push policy visible, so future agents can reuse knowledge instead of
depending on chat history.

Best for patterns, decisions, setup notes, and lessons you expect to need again.

```bash
npx skills add patrick-fu/llm-wiki-capture
```

Repository: [`patrick-fu/llm-wiki-capture`](https://github.com/patrick-fu/llm-wiki-capture)

## Included Skills

These smaller skills stay in this collection as everyday building blocks.

### Thinking and planning

- `brainstorm`: Use it before planning or coding, when the useful work is still
  clarifying the idea, audience, constraints, and first direction.
- `explore-and-plan`: Use it after the direction is mostly chosen, when the next
  output should be an executable plan with clear steps, boundaries, and
  acceptance checks.
- `faster-learning-coach`: Use it when the user's real goal is learning. It
  turns explanations into short learning loops with practice, teach-back, and
  review.

### Coding workflow helpers

- `write-unit-test`: A practical guide for behavior-focused unit tests around
  production code, bug fixes, refactors, and domain rules.
- `log-driven-debugging`: A diagnosis loop for slippery bugs: add targeted logs,
  let the user rerun the scenario, then use the returned logs to find the first
  real divergence.
- `commit-staged-changes`: Commit only what is already staged, after reviewing
  the staged diff and writing a factual English commit message.
- `generate-commit-message`: Inspect the staged diff and draft the commit message
  without creating the commit.

### External coding agents

- `claude-code-coding-agent`: Launch Claude Code CLI as an explicitly selected
  external executor, with patterns for automation, review-only runs, interactive
  sessions, and model or permission pass-through.
- `codex-coding-agent`: Launch local Codex CLI from another host agent or
  automation harness, including `codex exec`, `codex review`, interactive
  resume/fork flows, and Git workspace expectations.
- `cursor-coding-agent`: Launch Cursor CLI only when Cursor is explicitly
  selected, with separate guidance for headless execution, review-only
  `--mode ask`, planning mode, and interactive sessions.

### Personal workflow and source capture

- `home-config-sync`: Initialize and operate a personal bare-repo dotfiles setup
  under `~/.dotfiles`, including first push, new-machine deploys, whitelist
  updates, pull/merge safety, and optional GUI-discoverable mode.
- `x-twitter-reader`: Extract original content from X/Twitter posts, threads,
  Articles, metadata, links, and media references before summarizing,
  translating, quoting, or archiving it.

## Sync Model

This public collection is generated automatically from a private source
repository. Public changes should be made in the source repository, not directly
here.

The sync process preserves relevant file history and commit metadata for the
published paths while rewriting commit hashes as part of the filtered export.
