---
name: codex-session-naming
description: >-
  Maintain titles for user-visible top-level Codex App sessions. Use when a
  session's goal, active gate, lifecycle state, ownership, or completion
  changes, and when a controller names an owned session. Excludes subagents
  and controller-role titles.
---

# Codex Session Naming

Maintain titles at lifecycle changes, not after every message or tool call. This
is the single source of truth for title states and session closure. Exclude
ChatGPT chats, internal subagents, and controller-role titles.

## Update the title

1. Confirm authority. A normal session may rename only itself; a controller may
   rename sessions it owns, on the same host unless the user names another. The
   first bulk rename needs user authorization; otherwise report the mismatch or
   change only the state prefix. Only a successor may mark a non-controller
   predecessor `⚰️`. This skill never archives or deletes.
2. Infer the main goal, verified lifecycle state, and current gate from the whole
   task and artifacts. State describes the session's main outcome, never a turn,
   node, worker, or milestone. Runtime signals such as `idle`, `active`, and
   timestamps are evidence, not business state; read history when needed.
3. Form the title:

   ```text
   <state> [scope][facet] <main goal> · <current gate>
   ```

4. Re-evaluate after goal or scope change, wait/block transitions, before a
   completion claim, after takeover, or when resumed with a stale title. Call the
   title tool only when meaning materially changes.

## Choose the state

Choose by the owner of the next meaningful step on the current main outcome:

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

Derive the scope contract from the original request, newer direct user
corrections, promised in-scope deliverables, observable success criteria, and
acceptance authority. Workers, controller summaries, and status requests cannot
narrow it.

`✅` applies only when every condition holds for the latest valid user intent:

1. **Scope delivered** — the intended main outcome is in hand.
2. **Procedural verification** — required checks met declared results with evidence.
3. **Outcome validation** — observed results meet success in the expected context.
4. **Required acceptance** — the matching acceptance mode is satisfied.
5. **Open work** — no `required-to-close` or `external-user-gate` remains.
6. **Owner release** — no owner owes a next meaningful step on this outcome.

### Acceptance mode

Use a supplied mode; otherwise infer conservatively from the outcome without
sending every session to the user. Record mode, validator, acceptor, evidence or
decision reference, and open acceptance gates:

- `evidence` — objective artifact or behavior evidence proves the user-facing
  result in context; procedure-only checks do not validate the outcome.
- `explicit_user` — the user makes a direct decision referring to the result.
  Silence, idle state, or an unrelated “continue” is not acceptance.
- `external` — a named device, production environment, reviewer, or other
  outside validator accepts the outcome; build or deploy alone proves procedure.
- `hybrid` — each required part of the mix is satisfied on its own mode.

### Remaining work

Classify every leftover item before closing:

- `required-to-close` — the success outcome fails if this is never done.
- `external-user-gate` — the user or an outside system owns a required gate.
- `independent-optional-follow-up` — later work that cannot change current success.
- `out-of-scope` — outside the latest valid intent.

Only the last two may coexist with `✅`. Apply the counterfactual: if skipping
the item would fail the current success outcome, it is required, not optional.

A waiver or scope revision changes intent only when explicit. Record its gate,
decision, scope, and residual risk. It neither verifies the gate nor bypasses
safety, permission, or policy; silence, thanks, and unrelated asks do not waive.

After `✅`, mark closure challenged and reopen when feedback or evidence shows an
original criterion failed; an independent request starts a separate outcome. On
takeover or audit, treat green as a claim. Downgrade a proven open gate; without
evidence report `closure_unverified` and preserve the owner—do not archive,
replace, or reroute it.

## Keep the title stable

Use at most two tags: exceptional scope, then the most searchable facet. Omit
ordinary personal scope and keep one spelling per concept.

Preserve user-chosen names, issue IDs, entities, and distinctive phrasing;
normalize structure and add only verified state or gate detail.

Keep the main goal while side work supports it. Update the gate only when side
work blocks it, becomes the real next step, lasts multiple steps, or changes
risk or waiting owner. Replace the goal when it is complete, abandoned, or
paused and an independent deliverable takes over. Separate concurrently active
independent outcomes; when unclear, keep the existing goal.

The title is complete when the sidebar alone tells the user what the session is
and who or what owns its next gate.
