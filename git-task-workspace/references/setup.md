# Setup and Migration Guide

Guide the user to set up an upstream source pool and an isolated task workspace root.
Do not decide directory names or paths on behalf of the user.

## 1. Interactive Discovery

Inspect the current environment first, then present recommended choices:

1. `root-directory`: Propose the parent location, such as `~/dev`, `~/code`, or `~`.
2. `source-pool-naming`: Recommend `source` or `repos`. Ask whether sub-grouping
   is preferred (for example, `source/company/`, `source/oss/`, `source/personal/`)
   or a flat list of repositories.
3. `workspace-naming`: Recommend `workspace` or `tasks`.

## 2. Migration Policy

Ask the user whether existing Git repositories should be migrated:

- **Gradual (Recommended)**: Leave existing repositories untouched. Only new tasks
  and newly cloned projects adopt the dual-directory worktree layout. Existing
  repositories can be moved into the source pool on demand later.
- **Full**: Move existing repositories into `<source>/`, ensure their working
  trees are on clean default trunk branches, and prune obsolete local worktrees.

## 3. Local AGENTS.md Templates

Create an `AGENTS.md` inside `<source>/` and another inside `<workspace>/`.

### `<source>/AGENTS.md` Template

```markdown
# Upstream Source Pool

This directory is an upstream repository pool tracking trunk branches.

## Rules
- READ-ONLY TRUNK: Never edit code, run active builds, or create temporary branches here.
- WORKTREE SOURCE: Repositories here serve as checkout sources for `<workspace>/`.
- SYNC: Fast-forward trunk branches periodically.

## Repository Router Map
<!-- Keep this coarse and lightweight. Do not document internal codebase details. -->
- Frontend: `<repo-name>`
- Backend / Services: `<repo-name>`
- Shared Libraries / SDKs: `<repo-name>`
```

### `<workspace>/AGENTS.md` Template

```markdown
# Task Workspaces

This directory contains isolated, task-oriented workspaces.

## Workflow
- TASK FOLDER: Every task gets an isolated directory: `<workspace>/<task-name>/`.
- CHECKOUT: Locate required repositories in `<source>/`, then check out a worktree:
  `git -C <source>/<repo> worktree add <workspace>/<task-name>/<repo> -b <branch>`
- MULTI-REPO: Co-locate all affected repositories inside the same task directory.
- TEAR DOWN: When the task is merged or closed, delete `<workspace>/<task-name>/`
  and run `git -C <source>/<repo> worktree prune`.
```

## 4. Global AGENTS.md Linkage

Add context pointers in the user's top-level `AGENTS.md` (e.g. `~/.agents/AGENTS.md`
or `~/AGENTS.md`).

### With Skill Installed

```markdown
## Task Workspaces
- Project work is performed in dedicated task directories under `<workspace>/`.
- Repositories are checked out as worktrees from `<source>/`.
- Router map: `@<source>/AGENTS.md`. Workflow rules: `@<workspace>/AGENTS.md`.
- Reference skill: `$git-task-workspace`.
```

### Zero-Skill Standalone Mode

If the user prefers not to maintain or install this skill, omit the skill pointer.
The generated `<source>/AGENTS.md`, `<workspace>/AGENTS.md`, and top-level pointers
are fully self-contained and require no external skill dependency.
