---
name: codex-async-followup
description: >-
  Schedule follow-ups in Codex App for long asynchronous waits when no
  independent work remains; resume work when the scheduled wakeup arrives.
---

# Codex Async Follow-up

Avoid empty polling and come back to finish the work. Use the conversation's
existing context to resume.

1. After starting asynchronous work, continue any independent work. When none
   remains and the expected wait is long, such as a lengthy build or extended
   research running in a subagent or background task, use `automation_update` to schedule a one-time
   heartbeat in the current task (`destination: "thread"`), then end the turn.
   Choose a delay from the expected duration, usually 5, 10, or 15 minutes.
   Set the prompt to `continue`.
2. On wakeup, check the existing work and apply step 1 again: reassess independent
   work and the expected wait before deciding whether to continue or schedule
   another wakeup and end the turn. Stay quiet when nothing actionable changed.
3. Reuse this follow-up's automation ID for later checks; leave other automations
   alone. Pause or delete this follow-up when it is no longer needed.

If scheduling is unavailable or fails, say so rather than implying a wakeup is set.
