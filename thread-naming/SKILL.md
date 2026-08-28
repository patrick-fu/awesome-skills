---
name: codex-session-naming
description: >-
  Maintain titles for user-visible top-level Codex App sessions. Use when a
  session's goal, active gate, lifecycle state, ownership, or completion
  changes, and when a controller names an owned session. Excludes subagents
  and controller-role titles.
---

# Codex Session Naming

Maintain titles at lifecycle changes, not after every message or tool call.
Apply this skill to user-visible top-level Codex sessions; exclude ChatGPT
chats, internal subagents, and controller-role titles. This skill is the
single source of truth for title state semantics and the session closure
contract.

## Update the title

1. Confirm authority. A normal session may rename only itself. A controller may
   rename sessions it owns, on the same host unless the user names another.
   The first bulk rename needs user authorization. Only a successor may mark a
   non-controller predecessor `⚰️`. This skill never archives or deletes.
2. Determine the main goal, verified lifecycle state, and current gate from the
   whole task and its actual artifacts. The leading state belongs to the
   session's current main outcome, not a turn, node, worker, or milestone.
   Treat `idle`, `active`, timestamps, and similar runtime signals as evidence,
   not business state. Read history when the visible context is insufficient.
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

Use one leading state according to the owner of the next meaningful step on the
current main outcome:

- `✅` — the session closure contract is satisfied.
- `⚰️` — a named successor accepted the unfinished ownership; completed work
  merely reused elsewhere stays `✅`.
- `🙋‍♂️` — the user must decide, authorize, confirm, or act personally.
- `🕒` — time, a device, build, review, or external system must advance.
- `⚠️` — a real exception leaves no valid path forward.
- `⏸️` — the user explicitly paused the work.
- `⏳` — owned backlog or queued work has not started.
- `🏃‍♂️` — work is actively progressing.

A worker, turn, phase, or node reporting done does not close the session.

## Close the session

Build the scope contract from the original request, newer direct user
corrections, promised in-scope deliverables, observable success criteria, and
acceptance authority. A worker, controller summary, or later status request
cannot silently narrow it.

`✅` applies only when every condition holds for the latest valid user intent:

1. **Scope delivered** — that intent's current main outcome is in hand.
2. **Procedural verification** — the required checks met their declared result
   with evidence.
3. **Outcome validation** — in the expected context, the observed result meets
   the success outcome.
4. **Required acceptance** — the matching acceptance mode is satisfied.
5. **Open work** — no `required-to-close` or `external-user-gate` item remains.
6. **Owner release** — no owner still owes a next meaningful step on this
   outcome.

### Acceptance mode

Use a prewritten mode when the task supplies one. Otherwise judge conservatively
from the outcome, without sending every session to the user:

- `evidence` — objective artifact or behavior evidence in the expected context
  proves the user-facing result. Procedure-only checks cannot satisfy outcome
  validation.
- `explicit_user` — the user must personally accept, confirm, or sign off.
- `external` — a named device, production environment, reviewer, or other
  outside validator observes and accepts the success outcome. A successful
  build or deployment step alone proves only its procedure.
- `hybrid` — each required part of the mix is satisfied on its own mode.

Record the mode, validator, acceptor, evidence or decision reference, and open
acceptance gates. These fields record authority as well as state.

For `explicit_user`, require a direct decision that refers to the result;
silence, idle state, or an unrelated “continue” is not acceptance.

### Remaining work

Classify every leftover item before closing:

- `required-to-close` — the success outcome fails if this is never done.
- `external-user-gate` — the user or an outside system still owns a required
  gate.
- `independent-optional-follow-up` — later work that does not change the
  current success outcome.
- `out-of-scope` — outside the latest valid intent.

Only the last two may coexist with `✅`. Apply the counterfactual: if skipping
the item would fail the current success outcome, it is required, not optional.

A user waiver or scope revision changes the latest valid intent only when it
is explicit. Record the named gate, decision, scope, and residual risk; a
waiver does not make that gate verified or bypass a safety, permission, or
policy boundary. Silence, thanks, or an unrelated ask is not a waiver.

After `✅`, mark closure challenged and reopen if user feedback or new evidence
shows that an original criterion failed. A truly independent new request does
not reopen; start or suggest a separate outcome. On takeover or audit, treat a
green title as a claim, not proof. Downgrade a confirmed open gate; if evidence
is unavailable, report `closure_unverified` and preserve the owner rather than
archiving, replacing, or rerouting it. Without bulk-rename authorization,
report the mismatch or update only the state prefix.

## Keep the title stable

Use at most two tags: an exceptional scope such as `[Project]` or `[OpenSource]`,
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
