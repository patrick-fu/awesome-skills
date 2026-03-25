# Awesome Skills

This repository contains a small set of reusable agent skills extracted from a larger private workspace and published as a standalone public collection.

## Included Skills

### `brainstorm`

Use this skill when the right next step is conversation rather than execution. It pushes the assistant to ask clarifying questions first, uncover hidden assumptions, and guide the user toward a clearer problem statement before proposing solutions.

### `commit-staged-changes`

Use this skill when changes are already staged and the task is to create a commit. It enforces a clean review of staged content and a factual English commit message without staging extra files implicitly.

### `explore-and-plan`

Use this skill when an idea needs to be turned into a concrete execution plan. It drives the work from exploration to convergence to a plan with no unresolved decisions or placeholders.

### `generate-commit-message`

Use this skill when you want a high-quality commit message for staged changes but do not want to create the commit yet. It inspects the staged diff and outputs commit message text only.

### `home-config-sync`

Use this skill when you want to initialize, deploy, or maintain a personal bare-repo dotfiles workflow under `~/.dotfiles` with work-tree set to `$HOME`. It covers first-time setup from an empty private remote, starter-file handling, multi-machine sync, pull and merge safety, and ongoing push workflow.

## Usage

Install the published skills:

```bash
npx skills add patrick-fu/awesome-skills
```

Update skills:

```bash
npx skills update
```

## Sync Model

This public repository is generated automatically from a private source repository. Public changes should be made in the source repository, not directly here.

The sync process preserves relevant file history and commit metadata for the published paths while rewriting commit hashes as part of the filtered export.
