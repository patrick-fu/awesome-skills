---
name: git-task-workspace
description: >-
  Manage task worktrees from a shared source repository pool. Use when preparing
  or cleaning code workspaces, adding repositories to a task, or configuring the
  source/workspace layout.
---

# Git Task Workspace

Group the repositories needed for one task under a dedicated task directory.
Reuse the configured source pool, workspace layout, and persistence rules.

For initialization, migration, or missing layout configuration, read
[Setup](references/setup.md). Otherwise, use the existing layout directly.

## Boundaries

- **Source pool:** Keep source checkouts clean for inspection and repository
  administration, including clone and fetch. Make code changes, run builds, and
  write task artifacts in task worktrees.
- **Task workspace:** Keep related worktrees together and respect the task's
  current owner and working state. Persistent workspace instructions and
  management tools are not task caches.
- **Durable material:** Use the configured destination for task notes and recovery
  records. Code and versioned project documentation remain in their repositories.

## Workflow

1. **Locate.** Find the existing task directory and worktrees before creating
   another. Verify the repository, remote, and intended starting revision against
   current project rules. Preserve compatible working state.
2. **Prepare.** Add linked worktrees from the source pool for the repositories
   needed now. Clone a missing repository into the pool first, then add its task
   worktree. Use the appropriate existing or new branch and explicit start point.
3. **Work.** Edit and build in task worktrees. Add dependencies as the scope
   becomes clear. Record paths, branches, and version combinations needed to
   recover the task in its existing durable record.
4. **Clean up.** Confirm the workspace is no longer needed by active work.
   Inspect tracked, untracked, ignored, and checkout-external files. Preserve
   unique material and unmerged commits in durable locations, and verify required
   saves and syncs before removal. Use `git worktree remove` for worktrees, then
   clear disposable outputs and stale registrations. Inspect removal refusals
   before proceeding; preserve workspace management files and other tasks' state.

## Optional Context Guidance

Save durable notes to the configured location. For substantial shared task-context
organization, consult `work-context` if available in the current skill catalog;
otherwise, use the existing issue or documentation workflow. Reuse guidance
already read. Neither skill requires installing or loading the other for routine
work; configured paths and task records connect their environments.
