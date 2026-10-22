---
name: claude-code-coding-agent
description: Run bounded tasks through Claude Code CLI or its wrapper, when explicitly selected.
---

# Claude Code Coding Agent

## Scope

Use the selected launcher's `--version` and `--help` to choose supported
model/effort settings. Keep wrappers opaque: their source and environment may
contain credentials. Honor explicit choices; compare requested settings with
the receipt's effective settings, leaving absent values unverified.

Fix the workspace, permitted actions, and acceptance evidence. Experiments and
parallel writers need isolated workspaces. **Boundary:** before file-only work,
strict confinement, or a wrapper/permission conflict, read
[Boundaries](references/monitoring.md#boundaries). Permission changes require
authorization; the skill grants no extra scope.

## Run

Use [claude_run.py](scripts/claude_run.py) as the single print-task entry point:

```bash
python3 "$SKILL_DIR/scripts/claude_run.py" run \
  --launcher "$LAUNCHER" --cwd "$WORKSPACE" --prompt-file "$PROMPT_FILE" \
  --timeout-seconds 600 -- --model "$MODEL"
```

`SKILL_DIR` is this skill's directory. Choose the host deadline deliberately
(0 is unbounded); pass other authorized Claude options after `--`. Omit the
model override when the selected wrapper supplies it.

| Owner | Responsibility |
| --- | --- |
| Script | Scope/prompt validation, stdin, stream flags, unique captures, child exit, compact receipt |
| Agent | Model, permissions, required tool evidence, artifact acceptance, recovery |

Retain the host process handle. The script prints `run_dir`, then a final
receipt; use `python3 "$SKILL_DIR/scripts/claude_run.py" inspect "$RUN_DIR"`
for compact evidence while waiting. Quiet output alone is not failure.

## Accept

`COMPLETED` means the process and stream completed, not that the task passed.
Read `answer.txt`; check required successful tool results, denied actions and
errors, then verify artifacts/diff against Scope. Report unperformed checks.
**Recover:** for failure, unfinalized evidence, cancellation or resume, read
[Recovery](references/monitoring.md#recovery) before another attempt.
