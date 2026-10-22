---
name: grok-coding-agent
description: Run bounded tasks through Grok Build CLI or its wrapper, when explicitly selected.
---

# Grok Coding Agent

## Scope

Use the selected launcher's `--version`, `--help` and authenticated `models`
to choose supported model/effort settings. Honor explicit choices; keep wrappers
opaque because their source and environment may contain credentials. Compare
requested settings with observed evidence, leaving absent values unverified.

Fix the workspace, permitted actions and acceptance evidence. Experiments and
parallel writers need isolated workspaces. **Boundary:** before file-only work,
strict confinement or permission recovery, read
[Boundaries](references/monitoring.md#boundaries). The skill grants no extra scope.

## Run

For ordinary bounded headless tasks, use [grok_run.py](scripts/grok_run.py):

```bash
python3 "$SKILL_DIR/scripts/grok_run.py" run \
  --launcher "$LAUNCHER" --cwd "$WORKSPACE" --prompt-file "$PROMPT_FILE" \
  --timeout-seconds 600 -- --model "$MODEL"
```

`SKILL_DIR` is this skill's directory. Choose the deadline deliberately
(0 is unbounded); pass authorized Grok options after `--`.
Omit model overrides supplied by an opaque wrapper.

| Owner | Responsibility |
| --- | --- |
| Script | Target/prompt validation, native transport, unique captures, real child exit, compact receipt |
| Agent | Model, permissions, required successful actions, artifacts, recovery |

Retain the host process handle. The runner prints `run_dir`, then its receipt;
use `python3 "$SKILL_DIR/scripts/grok_run.py" inspect "$RUN_DIR"` while
waiting. Quiet output alone is not failure.

## Accept

`COMPLETED` means process/stream completion, not task acceptance. Read
`answer.txt`; check necessary successful tools, refusals and artifacts/diff,
including untracked files. Missing or empty candidate text may be legitimate;
judge against Scope. Report unperformed checks.
**Decode:** for schema questions, read [Stream](references/monitoring.md#stream).
**Recover:** before cancellation recovery, another attempt or native resume,
read [Recovery](references/monitoring.md#recovery).
