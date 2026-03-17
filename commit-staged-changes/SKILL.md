---
name: commit-staged-changes
description: Create Git commits for already staged changes.
allowed-tools:
  - Bash(git diff*)
  - Bash(git commit*)
  - Bash(git status*)
  - Bash(git log*)
---

# Commit Staged Changes

Check staged content before committing.

Run each command as a **separate** Bash tool call (do NOT combine them with `&&` or `echo`):

```bash
git diff --cached --name-status
```

```bash
git diff --cached
```

If no files are staged, stop and report that nothing is ready to commit.

Write the commit message in English.

Use this message structure:

1. Subject line: One plain sentence with the first letter capitalized.
2. Do not use conventional prefixes such as `fix:`, `feat:`, `chore:`, `docs:`, or similar tags.
3. Body: Add detailed bullet points that clearly explain key code or behavior changes.

Keep the subject concise and specific.
Keep the body factual and implementation-focused.

Commit only staged changes. Do not stage additional files unless the user explicitly asks.

Run:

```bash
git commit
```

If commit hooks fail, report the exact failure and next actionable step.
