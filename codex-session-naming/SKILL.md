---
name: codex-session-naming
description: >-
  Maintain titles for user-visible top-level Codex sessions. Use when a
  session's goal, active gate, lifecycle state, or ownership changes, and when
  a controller names an owned session. Excludes subagents and controller-role
  titles.
---

# Codex Session Naming

Maintain titles at lifecycle changes, not after every message or tool call.
Apply this skill to user-visible top-level Codex sessions; exclude ChatGPT
chats, internal subagents, and controller-role titles.

## Update the title

1. Confirm authority. A normal session may rename only itself. A controller may
   rename sessions it owns, on the same host unless the user names another.
   The first bulk rename needs user authorization. Only a successor may mark a
   non-controller predecessor `⚰️`. This skill never archives or deletes.
2. Determine the main goal, verified lifecycle state, and current gate from the
   whole task and its actual artifacts. Treat `idle`, `active`, timestamps, and
   similar runtime signals as evidence, not business state. Read history when
   the visible context is insufficient.
3. Form the title:

   ```text
   <state> [scope][facet] <main goal> · <current gate>
   ```

4. Call the available title tool only when the title's meaning materially
   changes.

Re-evaluate after the goal or scope changes, on entering or leaving a wait or
block, before reporting completion, after takeover, and when a resumed session's
title is visibly stale.

## Choose the state

Use one leading state according to the owner of the next meaningful step:

- `✅` — the goal and required acceptance gates are complete.
- `⚰️` — a named successor accepted the unfinished ownership; completed work
  merely reused elsewhere stays `✅`.
- `🙋‍♂️` — the user must decide, authorize, confirm, or act personally.
- `🕒` — time, a device, build, review, or external system must advance.
- `⚠️` — a real exception leaves no valid path forward.
- `⏸️` — the user explicitly paused the work.
- `📋` — owned backlog or queued work has not started.
- `▶️` — work is actively progressing.

## Keep the title stable

Use at most two tags: an exceptional scope such as `[DJI]` or `[OpenSource]`,
then the most searchable facet such as `[Jira]`, `[Wiki]`, `[iOS]`, `[Mac]`,
`[Skill]`, or `[研究]`. Omit the ordinary personal scope. Keep one stable
spelling per concept.

Preserve user-chosen project names, issue IDs, entities, and distinctive
phrasing. Normalize their structure and add only verified state or gate detail.
During controller-led maintenance without bulk-rename authorization, avoid a
silent body rewrite: report the mismatch or update only the state prefix.

Keep the main goal while side work supports the same deliverable. Update the
gate only when the side work blocks the goal, becomes the real next step, lasts
multiple steps, or changes risk or the waiting owner. Replace the main goal
when the old goal is complete, abandoned, or paused and a new independent
deliverable takes over. Suggest separate sessions when independent outcomes
remain active together; when direction is unclear, keep the existing goal.

The title is complete when the sidebar alone tells the user what the session is
and who or what owns its next gate.
