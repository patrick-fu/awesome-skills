---
name: codex-async-followup
description: >-
  Schedule follow-ups in Codex App after starting subagents, background
  commands, or external jobs; continue when the task's scheduled wakeup arrives.
---

# Codex Async Follow-up

Avoid empty polling and come back to finish the work. Use the conversation's
existing context to resume.

1. After starting asynchronous work, use `automation_update` to schedule a one-time
   heartbeat in the current task (`destination: "thread"`). Choose a delay from the
   expected duration, usually 5, 10, or 15 minutes. Set the prompt to `continue`.
   Once scheduled, end the turn.
2. On wakeup, check the existing work and continue. If it still needs time, schedule
   the next wakeup and end the turn again. Stay quiet when nothing actionable changed.
3. Reuse this follow-up's automation ID for later checks; leave other automations
   alone. Pause or delete this follow-up when it is no longer needed.

If scheduling is unavailable or fails, say so rather than implying a wakeup is set.
