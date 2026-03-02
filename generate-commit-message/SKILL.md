---
name: generate-commit-message
description: Generate git commit message from staged changes without creating a commit.
---

# Generate Commit Message Only

Inspect staged changes and produce a commit message.

Run:

```bash
git diff --cached --name-status
git diff --cached
```

If no files are staged, stop and report that no commit message can be generated.

Write the message in English using this structure:

1. Subject line: One plain sentence, first letter capitalized.
2. Do not use conventional prefixes such as `fix:`, `feat:`, `chore:`, `docs:`, or similar tags.
3. Body: Detailed bullet points describing key file-level and behavior-level changes.

Output only the commit message content in a copy-ready format.

Do not run `git commit`.
Do not modify staging state unless the user explicitly asks.
