---
name: codex-async-followup
description: >-
  Schedule follow-ups in Codex App for long asynchronous waits when no
  independent work remains; resume work when the scheduled wakeup arrives.
---

# Codex Async Follow-up

Resume asynchronous work from the conversation's existing context. Choose the
continuation path for the session's role:

- Global and project controllers use `codex-session-controller` for follow-up
  mode selection, checks, and scheduling.
- Workers and ordinary tasks use the loop below for their own internal waits.

1. After starting asynchronous work, continue any independent work. When none
   remains and the expected wait is long, such as a lengthy build or extended
   research running in a subagent or background task, use `automation_update` to
   schedule a one-time heartbeat in the current task (`destination: "thread"`),
   then end the turn. Choose a delay from the expected duration, usually 5, 10,
   or 15 minutes. Set the prompt to `continue`.
2. On wakeup, check the existing work and apply step 1 again: reassess independent
   work and the expected wait before deciding whether to continue or schedule
   another wakeup and end the turn. Stay quiet when nothing actionable changed.
3. Reuse this follow-up's automation ID for later checks. Pause or delete this
   follow-up when its work is complete or canceled, or its wait ends.

If scheduling is unavailable or fails, report the failure and the remaining wait.
