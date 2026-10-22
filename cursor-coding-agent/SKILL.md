---
name: cursor-coding-agent
description: Run bounded tasks through Cursor CLI or its wrapper, when explicitly selected.
---

# Cursor Coding Agent

## Scope

Confirm `Start the Cursor Agent` in `--help`; a generic `agent` name is not
product identity. Use `--version`, authenticated `models` and current help
to choose supported model/effort settings. Honor explicit choices; keep wrappers
opaque because their source and environment may contain credentials. Compare
requested settings with observed evidence, leaving absent values unverified.

Fix the workspace, permitted actions and acceptance evidence. Experiments and
parallel writers need isolated workspaces. **Boundary:** before file-only work,
strict confinement or permission recovery, read
[Boundaries](references/monitoring.md#boundaries). The skill grants no extra scope.

## Run

For ordinary bounded headless tasks, use [cursor_run.py](scripts/cursor_run.py):

```bash
python3 "$SKILL_DIR/scripts/cursor_run.py" run \
  --launcher "$LAUNCHER" --cwd "$WORKSPACE" --prompt-file "$PROMPT_FILE" \
  --timeout-seconds 600 -- --model "$MODEL"
```

`SKILL_DIR` is this skill's directory. Choose the deadline deliberately
(0 is unbounded); pass authorized Cursor options after `--`.
Omit model overrides supplied by an opaque wrapper.

| Owner | Responsibility |
| --- | --- |
| Script | Target/prompt validation, native transport, unique captures, real child exit, compact receipt |
| Agent | Model, permissions, required successful actions, artifacts, recovery |

Retain the host process handle. The runner prints `run_dir`, then its receipt;
use `python3 "$SKILL_DIR/scripts/cursor_run.py" inspect "$RUN_DIR"` while
waiting. Quiet output alone is not failure.

## Accept

`COMPLETED` means process/stream completion, not task acceptance. Read
`answer.txt`; check necessary successful tools, refusals and artifacts/diff,
including untracked files. Missing or empty candidate text may be legitimate;
judge against Scope. Report unperformed checks.
**Decode:** for schema questions, read [Stream](references/monitoring.md#stream).
**Recover:** before cancellation recovery, another attempt or native resume,
read [Recovery](references/monitoring.md#recovery).
