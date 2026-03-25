# Dotfiles Operations

## Repo Shape

- Git dir: `$HOME/.dotfiles`
- Work tree: `$HOME`
- Remote: user-provided private repository URL
- Preferred explicit command:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" <subcommand>
```

- Optional convenience alias if the user wants one in their shell config:

```bash
alias dotgit='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
```

This skill should prefer the explicit command form even if the alias exists.

## GUI-Discoverable Mode

Some users want the dotfiles repo to become temporarily discoverable by Git GUI tools. In this mode:

- `$HOME/.git` becomes a gitfile that points at `$HOME/.dotfiles`
- `core.bare` becomes `false`
- `core.worktree` becomes `..`

When GUI-discoverable mode is disabled again:

- `$HOME/.git` is removed if and only if it points at `$HOME/.dotfiles`
- `core.worktree` is unset
- `core.bare` returns to `true`

This is a reversible mode switch. Treat it as safe to turn on, turn off, and turn on again, as long as the repo-state checks pass.

Preferred operational pattern:

- First inspect whether GUI mode is currently enabled, currently disabled, or in an unexpected state.
- Ask the user whether they want it enabled when they are using this skill interactively for ongoing repo management.
- Use the bundled scripts from `${CLAUDE_SKILL_DIR}/scripts/` so the skill owns the full flow and does not depend on user-local helper paths.
- Treat `${CLAUDE_SKILL_DIR}` as the script root when invoking those bundled scripts.

### Inspect GUI Mode State

Relevant paths and values:

- repo dir: `$HOME/.dotfiles`
- gitfile path: `$HOME/.git`
- expected gitfile content: `gitdir: $HOME/.dotfiles`

Preferred script entrypoint:

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/dotfiles-gui-status.sh"
```

Equivalent checks:

```bash
ls -ld "$HOME/.dotfiles"
```

```bash
ls -ld "$HOME/.git"
```

```bash
git --git-dir="$HOME/.dotfiles" config --get core.bare
```

```bash
git --git-dir="$HOME/.dotfiles" config --get core.worktree
```

Interpretation:

- Enabled:
  - `$HOME/.git` is a file that points to `$HOME/.dotfiles`
  - `core.bare=false`
  - `core.worktree=..`
- Disabled:
  - `$HOME/.git` does not exist
  - `core.bare=true`
  - `core.worktree` is unset
- Unexpected:
  - `$HOME/.git` is a directory
  - `$HOME/.git` points somewhere else
  - repo config is partially switched

If the state is unexpected, stop and explain why before changing anything.

### Enter GUI-Discoverable Mode

Preferred script entrypoint:

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/dotfiles-gui-enter.sh"
```

Equivalent steps:

1. Confirm the repo exists and `$HOME/.git` is not a conflicting directory.
2. If `$HOME/.git` already exists as a file, confirm it already points to `$HOME/.dotfiles`; otherwise stop.
3. Set:

```bash
git --git-dir="$HOME/.dotfiles" config core.bare false
```

```bash
git --git-dir="$HOME/.dotfiles" config core.worktree ..
```

4. Write the gitfile:

```bash
printf 'gitdir: %s\n' "$HOME/.dotfiles" > "$HOME/.git"
```

5. Verify with:

```bash
git -C "$HOME" status --short --branch
```

### Exit GUI-Discoverable Mode

Preferred script entrypoint:

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/dotfiles-gui-exit.sh"
```

Equivalent steps:

1. Confirm `$HOME/.git` is a file and points to `$HOME/.dotfiles`; otherwise stop.
2. Remove the gitfile:

```bash
rm "$HOME/.git"
```

3. Unset the worktree:

```bash
git --git-dir="$HOME/.dotfiles" config --unset core.worktree
```

4. Restore bare mode:

```bash
git --git-dir="$HOME/.dotfiles" config core.bare true
```

5. Verify with:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" status --short --branch
```

### GUI Mode Safety Notes

- Never remove `$HOME/.git` unless it is a file and its content points exactly to `$HOME/.dotfiles`.
- Never overwrite a real `$HOME/.git` directory.
- Never partially switch modes without checking the resulting state.
- Explain clearly whether the repo is now GUI-discoverable or back in normal bare-repo mode.

## Starter Files

The public workflow ships with three starter files:

- `$HOME/.gitignore`
- `$HOME/bootstrap.sh`
- `$HOME/README.md`

Unless the user explicitly asks for more, initialization should stop at these three files. Do not add shell aliases, shell rc files, helper binaries, or extra dotfiles by default.

The templates live in `assets/`:

- `assets/gitignore.template`
- `assets/bootstrap.sh.template`
- `assets/README.template.md`

Initialization rule:

- If a starter file does not exist, create it from the template.
- If it already exists, ask the user whether to `merge`, `overwrite`, or `skip`.
- If the user chooses `merge`, read both versions first and preserve local content that is clearly user-specific while adding the generic template structure.
- If the user chooses `overwrite`, replace the local file with the starter template even if the remote repo is currently empty.
- If the user chooses `skip`, keep the local file untouched even if that means the repository will not contain the template version for now.
- If the user chooses `skip`, explain any consequence. Skipping `.gitignore` means whitelist-based tracking may not work until the user provides an equivalent file.

## Whitelist Rule

This workflow uses a whitelist `.gitignore` in `$HOME/.gitignore`:

- `*` ignores everything by default
- `!*/` keeps directories traversable
- Explicit `!path/to/file` entries opt files into version control

Implication:

- Existing tracked files can be updated directly.
- New files require two actions:
  1. Add a whitelist entry to `.gitignore`
  2. Add the file itself to the repo

## First-Time Initialization From An Empty Private Repo

Prerequisites:

- The user has already created an empty private repository on GitHub, GitLab, or another Git hosting platform.
- The user provides the remote URL, either SSH or HTTPS.
- The remote should be empty. No README, license, or starter commit unless the user explicitly wants to merge with it.

Recommended sequence:

1. Confirm the remote URL and whether the user wants SSH or HTTPS.

2. Inspect whether the local bare repo already exists:

```bash
ls -la "$HOME/.dotfiles"
```

If it already exists and is an active repo, stop and clarify whether the user wants to reuse it or replace it.

3. Initialize the bare repo with `main` as the initial branch:

```bash
git init --bare --initial-branch=main "$HOME/.dotfiles"
```

4. Attach the remote:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" remote add origin <repo-url>
```

If `origin` already exists, inspect `git remote -v` first and confirm before changing it.

5. Apply repo-local Git tuning:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" config status.showUntrackedFiles no
```

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" config core.untrackedCache true
```

6. Create or update the starter files using the template rules above.

7. Review the starter files before staging them.

8. Stage the starter files:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" add "$HOME/.gitignore"
```

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" add "$HOME/bootstrap.sh"
```

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" add "$HOME/README.md"
```

9. If the user wants to start tracking additional files right away, add whitelist entries first, then stage those files.

10. Verify:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" status --short
```

11. Commit:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" commit -m "Initialize home config sync"
```

12. Push:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" push -u origin main
```

If push fails, report the failure explicitly and keep the local repo state intact. Do not silently downgrade a failed push into a "local initialization complete" success message.

13. Run the bootstrap script:

```bash
bash "$HOME/bootstrap.sh"
```

14. Re-check final state:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" status --short --branch
```

Expected clean result:

```text
## main...origin/main
```

## Deploy On Another Machine

Use this when the remote repo already exists and the user wants to attach a new computer.

1. Clone the bare repo:

```bash
git clone --bare <repo-url> "$HOME/.dotfiles"
```

2. Define the helper alias for the current shell session if useful:

```bash
alias dotgit='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
```

3. Checkout tracked files into the home directory:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" checkout
```

4. If checkout reports existing-file conflicts, do not delete anything blindly.

Default safe path:

- Create a backup directory:

```bash
mkdir -p "$HOME/.dotfiles-backup"
```

- Move each conflicting file with a separate command, then retry checkout.

If the user wants a true merge instead of backup-and-replace, inspect both versions first and merge intentionally.

5. Apply repo-local Git tuning:

```bash
bash "$HOME/bootstrap.sh"
```

6. Optionally reload shell configuration if the user wants it and the file applies to the current shell:

```bash
source "$HOME/.zshrc"
```

7. Verify:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" status --short --branch
```

## Update Current Configuration

### Update An Existing Tracked File

1. Edit the file.

2. Review:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" status
```

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" diff -- <path>
```

3. Stage:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" add <path>
```

### Start Tracking A New File

1. Add a whitelist entry to `.gitignore`, for example:

```bash
!.config/example/config.json
```

2. Stage `.gitignore` and the new file:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" add "$HOME/.gitignore"
```

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" add "$HOME/.config/example/config.json"
```

3. Verify:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" status --short
```

## Pull Remote Changes Into Local Dotfiles

### If The Working Tree Is Clean

Use:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" pull --ff-only
```

If the branch already diverged because of local commits, fetch and merge explicitly:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" fetch origin
```

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" merge origin/main
```

### If The Working Tree Has Local Tracked Changes

Do not start with `git stash -u`.

Use tracked-only stash:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" stash push -m "pre-pull tracked stash"
```

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" pull --ff-only
```

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" stash apply
```

Then:

- Resolve conflicts if any.
- Run `status`.
- If `stash apply` left files staged, move them back to unstaged if that better matches the pre-pull state:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" restore --staged <paths...>
```

## Push Local Changes To Remote

1. Inspect:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" status --short --branch
```

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" diff
```

2. Stage the intended files:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" add <paths...>
```

3. Review staged content:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" diff --cached --name-status
```

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" diff --cached
```

4. Commit:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" commit -m "Update home configuration"
```

5. Push:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" push origin main
```

6. Verify:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" status --short --branch
```

Expected clean result:

```text
## main...origin/main
```

## Safety Notes

- Prefer explicit paths and commands over relying on shell aliases in automation.
- Default to one command per Bash call. Keep shell operators and pipes as rare exceptions, not the normal workflow style.
- Re-check the actual tracked-file list with `ls-files` before documenting it elsewhere.
- Do not reset or discard unrelated home-directory files.
- Avoid `git stash -u` unless the user explicitly wants untracked home-directory content included.
- When stash entries were only temporary transport during pull and restore, remove them after verifying the working tree is correct.
