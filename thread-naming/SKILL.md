---
name: codex-session-naming
description: >-
  Maintain clear, accurate titles for top-level Codex App tasks at entry,
  meaningful changes, and wrap-up. Excludes ChatGPT chats and subagents.
---

# Codex Session Naming

Keep titles short, recognizable, and faithful to the conversation. Use the user's
language and supplied names; preserve IDs and terminology. Explicit format
requests override defaults.

## Title

`<state> [tags] <mandate> · <focus>`

Use 1–2 useful scope tags and two parts:

- **Mandate:** the overall task or topic. Preserve through follow-up questions,
  detours, experiments, and approach changes. Replace for a new task after
  completion, or the user's clear replacement or cancellation.
- **Focus:** the meaningful current result, bottleneck, decision, or next step.
  Keep it concise rather than listing intermediate actions.

## Updates

At entry, meaningful state changes, and wrap-up, compare the title with the task:
keep it while accurate; otherwise update it. Routine tool calls need no update.
Reuse task facts and results already in context; naming introduces no new
verification or coordination work.

## State

Express who acts next and the current task state from established facts.
A finished turn is not a completed task.

- `🏁` mandate completed
- `☑️` agreed checkpoint reached; work parked
- `🔀` unfinished work handed to an accepted successor
- `🙋` user decision, authorization, or action
- `🕒` time, device, review, build, or external system
- `⛔` no valid path
- `⏸️` user pause
- `⏳` owned queue not started
- `🏃` Agent-owned active work; a self-explanatory action emoji also fits

## Controllers

Established global controllers use `🕹️ <scope or name>`; project controllers use
`🗂️ <project or name>`. Keep the role and name stable during routine progress;
prefix `🏁` or `🔀` only for established completion or outgoing handoff.

## Authority

Rename your own session without confirmation; controllers may rename owned
workers. First bulk rename needs user authorization. Naming does not archive or
transfer ownership.
