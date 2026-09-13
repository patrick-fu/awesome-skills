---
name: git-task-workspace
description: >-
  Manage task-oriented Git worktree workspaces from an upstream source pool.
  Use when starting a task, checking out worktrees, adding multi-repo dependencies,
  tearing down workspaces, or setting up the directory layout.
---

# Git Task Workspace

Operate isolated, task-oriented worktrees from an upstream repository pool.

## Invariants

- `source-pool`: Clean, read-only upstream repository pool tracking trunk branches.
  Do not make dirty edits, run builds, or place temporary artifacts here.
- `workspace`: Task directory root where every work item gets a dedicated
  folder (`<workspace>/<task-name>/`). Worktrees are checked out here.
- `single-owner`: A task directory belongs to one active work stream. Multi-repo
  dependencies co-locate under that same task directory.

## Workflow

1. `start-task`: Create `<workspace>/<task-name>/`. For each required repository in
   the source pool, add a worktree into the task directory:
   `git -C <source>/<repo> worktree add <workspace>/<task-name>/<repo> -b <branch> [start-point]`
   Start points can be the default trunk, an older commit, or an existing branch.
2. `multi-repo`: When a task spans multiple repositories, check out worktrees
   for all affected repositories directly into `<workspace>/<task-name>/`.
3. `add-repo`: If an un-cloned dependency is needed mid-task, clone it into the
   source pool first, then add a worktree into the active task directory.
4. `tear-down`: After code is merged or abandoned, remove the task directory
   (`rm -rf <workspace>/<task-name>`) and prune worktree references:
   `git -C <source>/<repo> worktree prune`
   The source pool remains pristine.

## Setup and Migration

To initialize a new source/workspace layout, generate local `AGENTS.md` rules,
or migrate existing repositories, read [references/setup.md](references/setup.md).
