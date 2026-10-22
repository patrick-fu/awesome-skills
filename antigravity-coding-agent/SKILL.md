---
name: antigravity-coding-agent
description: Run bounded tasks through Antigravity CLI (agy) or its wrapper, when explicitly selected.
---

# Antigravity Coding Agent

## Scope

Check the selected launcher's `--version`, `--help`, and `models`. Tiered model
IDs already carry effort; add `--effort` only when needed. Honor explicit
choices and compare requested settings with emitted values. Keep wrappers
opaque: source, arguments and environment may contain credentials.

Fix workspace, permitted actions and acceptance evidence; isolate experiments
and parallel writers. **Boundary:** before file-only work, confined writes or
permission recovery, read [Boundaries](references/monitoring.md#boundaries).
**API:** before key/endpoint setup or route verification, read
[API mode](references/api-mode.md). The skill grants no extra authorization.

## Run

Use [agy_run.py](scripts/agy_run.py) as the only supported entry point:

```bash
python3 "$SKILL_DIR/scripts/agy_run.py" \
  --cwd "$WORKSPACE" --prompt-file "$PROMPT_FILE" \
  --label review --print-timeout 45m --agy-bin "$LAUNCHER" \
  -- --model "$MODEL"
```

`SKILL_DIR` is this skill's directory. Choose the CLI deadline deliberately;
0 is unbounded. Pass other authorized launcher arguments unchanged after `--`.

| Owner | Responsibility |
| --- | --- |
| Script | G0 duration, G1 cwd, G2 prompt, G3 unique captures, G4 child exit, G5 typed receipt |
| Agent | Model, permissions, required tool evidence, artifact acceptance, recovery |

Retain the host process handle. The script prints `run_dir`, then the final
receipt. Use `python3 "$SKILL_DIR/scripts/agy_run.py" inspect "$RUN_DIR"` for
compact evidence while waiting. Quiet output alone is not failure.

## Accept

`SUCCESS` is an evidence verdict, not artifact acceptance. Read `answer.txt`;
check required completed tools and actual artifacts/diff against Scope; report
unperformed checks. **Recover:** for failed/incomplete evidence, timeout,
cancellation, raw-stream diagnosis or resume, read
[Recovery](references/monitoring.md#recovery) before another attempt.
