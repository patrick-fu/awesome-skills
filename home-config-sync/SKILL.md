---
name: home-config-sync
description: "Initialize and operate a generic personal dotfiles bare repo under ~/.dotfiles with work-tree=$HOME: guide the user to create an empty private remote repo, bootstrap local starter files, push the first commit, deploy onto another machine, update whitelist-managed files, pull remote changes into local home config, resolve stash and merge flows, and push local updates. Use when the user explicitly invokes $home-config-sync or explicitly asks to initialize, manage, or sync a bare-repo dotfiles setup."
allowed-tools:
  - Read
  - Edit
  - Glob
  - Bash(git init*)
  - Bash(git clone*)
  - Bash(git remote*)
  - Bash(git config*)
  - Bash(git status*)
  - Bash(git diff*)
  - Bash(git ls-files*)
  - Bash(git add*)
  - Bash(git restore*)
  - Bash(git stash*)
  - Bash(git fetch*)
  - Bash(git pull*)
  - Bash(git merge*)
  - Bash(git commit*)
  - Bash(git push*)
  - Bash(git log*)
  - Bash(git checkout*)
  - Bash(bash*)
  - Bash(mkdir*)
  - Bash(cp*)
  - Bash(mv*)
  - Bash(ls*)
  - Bash(sed*)
---

# Home Config Sync

Use this skill for a generic, shareable bare-repo dotfiles workflow:

- Git dir: `~/.dotfiles`
- Work tree: `~`
- Remote: user-provided private repo URL
- Preferred explicit command:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" <subcommand>
```

Keep these rules:

- Prefer the explicit `git --git-dir="$HOME/.dotfiles" --work-tree="$HOME"` form over assuming an alias exists.
- Inspect live state before acting: run `status`, `ls-files`, and read `.gitignore`, `bootstrap.sh`, and `README.md` when relevant.
- Treat `.gitignore` as a whitelist. New files are not trackable until both the whitelist and the file itself are added.
- Prefer one command per Bash tool call. Translate multi-step flows from the reference into separate invocations instead of copying several shell operations into one command.
- Do not add `&&`, `;`, pipes, redirection, or wrapper `echo` lines unless the shell feature is genuinely required for the task.
- During first-time initialization, read the starter templates in `assets/` before creating or updating `.gitignore`, `bootstrap.sh`, or `README.md`.
- During first-time initialization, the default starter-file scope is exactly:
  - `.gitignore`
  - `bootstrap.sh`
  - `README.md`
- Do not invent extra shell config files, helper scripts, aliases, or wrappers during initialization unless the user explicitly asks for them.
- If `.gitignore`, `bootstrap.sh`, or `README.md` already exist, ask the user file-by-file whether to `merge`, `overwrite`, or `skip`. Do not silently replace or delete existing content.
- If the user chooses `merge`, preserve the user's existing machine-specific settings while adding the generic template structure that keeps this workflow maintainable.
- Interpret `merge`, `overwrite`, and `skip` as decisions about how the local file should be reconciled with the starter template. Do not reinterpret those decisions based on whether the remote repo is empty or already populated.
- If the user already provided a remote repo URL and initialization succeeds locally, treat the first push as part of the default initialization flow. Do not stop at a local-only first commit unless push fails or the user explicitly wants to defer it.
- Do not use `git stash -u` by default in this repo. The work tree is the whole home directory and `-u` can sweep huge unrelated caches into stash.
- If local tracked edits block `pull`, stash tracked files only, pull, then re-apply and resolve conflicts.
- If `stash apply` stages files automatically, restore them back to unstaged unless the user explicitly wants them staged.
- Treat GUI-discoverable mode as a reversible operational mode, not a one-time migration. The user may enable it, disable it, and re-enable it repeatedly.
- When the user starts using this skill for interactive repo management, ask whether they want GUI-discoverable mode enabled so Git GUI tools can detect and manage the dotfiles repo more easily.
- If the user wants GUI-discoverable mode:
  - load the GUI mode flow from the reference
  - use the bundled scripts under `${CLAUDE_SKILL_DIR}/scripts/`
- If the user does not want GUI-discoverable mode, or wants to turn it back off mid-session, run the `exit` flow.
- Before switching GUI mode, inspect current mode first and explain whether the repo is already enabled, already disabled, or needs a state change.

Workflow:

1. Confirm whether the user wants first-time initialization, deployment on another machine, inspection, local update, pull/merge, push, or GUI mode enter/exit.
2. Load [references/dotfiles-operations.md](./references/dotfiles-operations.md).
3. If the task is first-time initialization or starter-file refresh, also load the relevant template files from `assets/`.
4. If the task involves GUI mode, use the bundled scripts from `${CLAUDE_SKILL_DIR}/scripts/`.
5. Follow the matching command flow, but keep default execution at one command per Bash call. Only preserve complex shell syntax when it is truly necessary.
6. Re-check `status` and explain the final repo state clearly, including the next safe step for the user.

Use the reference file for:

- Repo shape and command conventions
- First-time initialization from an empty private remote repo
- Starter-file handling and merge/overwrite/skip decisions
- New-machine deployment steps
- Day-to-day update workflow
- Pull and merge workflow with or without local edits
- Push workflow
- GUI-discoverable mode enter / exit / inspect flow
- Safety notes for a whole-home work tree
