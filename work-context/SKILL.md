---
name: work-context
description: >-
  Maintain durable task context across sessions and agent tools. Use when
  recovering ongoing work, updating shared task records, or setting up a
  work-context environment.
---

# Work Context

Keep ongoing work recoverable across sessions. Reuse existing task records and
local persistence rules; a short task may need only its existing issue.

For initialization, migration, or missing persistence configuration, read
[Setup](references/setup.md). Otherwise, follow the daily workflow directly.

## Daily Workflow

1. **Locate.** Search existing work by goal and scope before creating another
   record. A task can serve several projects while keeping one recovery entry.
   Identify its owner and authoritative sources; preserve established ownership
   unless reassigned.
2. **Refresh.** Read from the short entry point into relevant detail. Before
   resuming or making a consequential decision, check source updates from the
   recorded revision or reading position. Update superseded conclusions and
   distinguish verified facts, assumptions, and unknowns.
3. **Update.** Keep the goal, acceptance criteria, current understanding,
   unresolved questions, and next action easy to find. Move detail out of the
   entry point as needed. Link tracker-owned fields; label local snapshots with
   their source and verification time.
4. **Save and hand off.** Follow the configured write and sync protocol, saving
   only owned changes. Re-read conflicting updates before integrating them.
   Leave accessible recovery material, including relevant code locations,
   revisions, verification limits, and outstanding waits or resource holds.
   Ending a session does not close the task or release its resources.

## Content

Keep code and versioned project documentation in their repositories. Task context
holds concise conclusions, decisions, key excerpts, relevant versions, and
reproduction steps. Put reusable knowledge in its configured store within the
existing authorization. Views derive from authoritative records.

Store generated or bulky artifacts according to the local storage policy.
Record their location and version when cited; identify evidence that is no longer
available. Before clearing a workspace, preserve unique material and verify the
required saves and syncs.

## Optional Workspace Guidance

Use the existing code workspace. When task worktree management is needed,
consult `git-task-workspace` if available in the current skill catalog; otherwise,
follow the project's existing workspace workflow. The environment's configured
paths and recovery records connect the two skills. Reuse guidance already read;
neither skill requires installing or loading the other for routine work.
