---
name: git-task-workspace
description: >-
  Initialize or reconfigure a source repository pool and task workspace layout.
  Use for first setup, migration, connecting another agent harness, or repairing
  workspace configuration drift.
---

# Git Task Workspace

Set up task directories that gather linked worktrees from a shared source pool
and hold task-lifetime artifacts. Deliver daily creation, expansion, recovery,
and cleanup rules into local instructions so the skill can retire after setup.

## Workflow

Read [Setup and Migration](references/setup.md) for defaults, deployable local
rules, migration, and acceptance checks.

1. **Discover.** Identify actual repository roots, existing task worktrees,
   owners, baselines, agent entry points, recovery records, and artifact policy.
2. **Configure.** Reuse the user's names, paths, and working state. Choose only
   missing defaults and resolve migration or retention choices before changing
   their scope. Prepare only the repositories needed now.
3. **Deploy.** Put routing in global instructions, repository administration in
   the source root's `AGENTS.md`, and task operations in the workspace root's
   `AGENTS.md`. Connect the chosen recovery destination by its actual location;
   preserve unrelated rules and existing ownership.
4. **Verify.** Without loading this skill, use the local instructions to recover
   a task, add a repository, retain evidence, and safely remove a disposable
   workspace. Inspect Git registrations and preserved material.

Completion is an operational local environment, including safe cleanup rules.
Ordinary task work follows its `AGENTS.md` files; return here for setup changes.
Directory names are recommendations. Roles come from the configured paths.

## Optional Context Integration

Use an existing issue or notes destination for durable recovery. If shared-context
setup is requested, use `work-context` when it is available in the current skill
catalog. Otherwise retain the existing recovery workflow. Neither installation
nor ordinary task work requires the other skill; local paths connect them.
