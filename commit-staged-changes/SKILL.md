---
name: commit-staged-changes
description: "This skill should be used when creating Git commits from already staged changes, including writing a compliant commit message and committing only the staged diff."
allowed-tools:
  - Bash(git diff*)
  - Bash(git commit*)
  - Bash(git status*)
  - Bash(git log*)
---

# Commit Staged Changes

Check staged content before committing.

Run each command as a **separate** Bash tool call.
Do not combine commands with `&&`, `;`, pipes, redirection, wrapper `echo` lines, or other shell glue unless a shell feature is truly required.

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

Run this as a single Bash tool call:

```bash
git commit
```

If commit hooks fail, report the exact failure and next actionable step.
