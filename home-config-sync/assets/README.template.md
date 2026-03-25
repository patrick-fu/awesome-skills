# Home Config Sync

This repository stores personal dotfiles as a bare Git repository.

## Repo layout

- Git directory: `~/.dotfiles`
- Work tree: `~`

Preferred command form:

```bash
git --git-dir="$HOME/.dotfiles" --work-tree="$HOME" <subcommand>
```

Optional alias:

```bash
alias dotgit='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
```

## Common workflows

### Track a new file

1. Add a whitelist entry to `~/.gitignore`
2. Stage the file
3. Commit and push

### Pull changes on another machine

1. Clone the bare repo into `~/.dotfiles`
2. Check out tracked files into `$HOME`
3. Run `bash "$HOME/bootstrap.sh"`

### Push local updates

1. Review `status` and `diff`
2. Stage intended files
3. Commit
4. Push
