---
name: thread-naming
description: >-
  Title top-level threads and sessions at entry, state changes, and completion.
  Skip subagents.
---

# Thread Naming

Format: `<emoji> [tags] <mandate> · <focus>`

- **Tags:** 1–2 short scope labels (`[repo]`, `[area]`).
- **Mandate:** the overall goal. Keep stable across follow-ups and detours; replace only after completion or when the user replaces or cancels the task.
- **Focus:** concise current result, blocker, decision, or next step.

Match the user's language and preserve IDs and key terms. Explicit user format requests override defaults.

## Emoji

Show **who acts next** and **current task state** from established facts (a finished turn is not a completed task):

- **Attention / wait:** `🙋` user decision, approval, or input · `🕒` external job, CI, review, device, or timer · `⛔` blocked · `⏸️` user-paused · `⏳` queued, not started
- **Closure:** `🏁` mandate completed · `☑️` parked at agreed checkpoint · `🔀` unfinished work handed off to an accepted successor (outgoing owner only)
- **Controllers:** `🕹️ <scope>` global controller · `🗂️ <project>` project controller (keep role headline stable; prefix `🏁` or `🔀` only when closed or handed off after acceptance)
- **Active work:** `🏃` or any self-explanatory action/domain emoji (`🐛`, `🔧`, `🧭`, `🧪`, `🔍`, `🧹`, `✍️`, etc.).

## Rules

- Compare the title with the task at entry, meaningful state shifts, and wrap-up: keep it while accurate; never update on routine tool steps or add extra verification just for naming.
- Rename your own top-level thread silently via the host's title tool; controllers may rename owned workers. First bulk rename needs user approval. Naming does not archive or transfer ownership.
- If the host has no title tool, output a title only when explicitly asked.
