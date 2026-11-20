---
name: thread-naming
description: >-
  Title top-level threads and sessions at the first naming reminder, state changes,
  and completion; the host may generate a plain turn-one title, upgrade it to the
  format at the first reminder. Skip delegated or spawned subagent runs, even when
  they have an isolated thread or title tool.
---

# Thread Naming

Format: `<emoji> [tags] <mandate> · <focus>`

- **Tags:** 1–2 short scope labels (`[repo]`, `[area]`).
- **Mandate:** the thread's overall goal. Lock Mandate and Tags across follow-ups and detours; replace only when the user explicitly switches topics or cancels the prior task, or starts a clearly unrelated new task after genuine closure.
- **Focus:** concise current result, blocker, decision, or next step.

Match the user's language and preserve IDs and key terms. Explicit user format requests override defaults.

## Emoji

Show **who acts next** and **current task state** from established facts (a finished turn is not a completed task):

- **Attention / wait:** `🙋` user decision, approval, or input · `🕒` external job, CI, review, device, or timer · `⛔` blocked · `⏸️` user-paused · `⏳` queued, not started
- **Closure:** `🏁` mandate genuinely closed · `☑️` parked at agreed checkpoint or interim reply · `🔀` unfinished work handed off to an accepted successor (outgoing owner only)
- **Controllers:** `🕹️ <scope>` global controller · `🗂️ <project>` project controller (keep role headline stable; prefix `🏁` or `🔀` only when closed or handed off after acceptance)
- **Active work:** `🏃` or any self-explanatory action/domain emoji (`🐛`, `🔧`, `🧭`, `🧪`, `🔍`, `🧹`, `✍️`, etc.).

For ongoing follow-up work (tracking an upstream bug, awaiting approval or periodic checks), default to `☑️` or `🕒` after interim replies; reserve `🏁` for genuine closure, and never treat a finished turn or an earlier `🏁` as license to silently overwrite the Mandate.

## Detours, Return to Stack, and Fork Check

- **Mandate vs. Detour:** Questions, adjacent lookups, or opportunistic tasks branching off the main work are detours—even across multiple turns, delegated subagents, or committed changes. Keep the existing Mandate and Tags locked; at most reflect the detour briefly in `· <focus>` while active, then restore `focus` to the main-thread state when done.
- **Return to stack:** When a turn completes a detour off the main thread, end the reply with one short line pointing back to the main mandate and its current state or next step. Omit this when staying on the main thread.
- **Fork check:** If a detour stretches past ~2–3 turns or forms an independent deliverable (cross-repo edits, a standalone PR, or a separate ticket), ask once whether to keep it as a detour, switch this thread's mandate, or split into a new thread—never silently rewrite the Mandate.

## Rules

- Applies only to user-initiated top-level threads (and explicit controllers managing workers). If you are running a delegated or subagent assignment from a parent agent or orchestrator, skip this skill completely—do not inspect it or rename your own or the parent's thread, even if your run has its own thread ID or title tool.

- Compare the title with the task at the first reminder, meaningful state shifts, and wrap-up: keep it while accurate; a host-generated plain turn-one title is upgraded at the first reminder, not before; never update on routine tool steps or add extra verification just for naming.
- Rename your own top-level thread silently via the host's title tool; controllers may rename owned workers. First bulk rename needs user approval. Naming does not archive or transfer ownership.
- If the host has no title tool, output a title only when explicitly asked.
