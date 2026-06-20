# Codex Nested Subagents

Use this reference only when Codex depth or multi-agent tooling blocks the
workflow.

Official sources:

- https://developers.openai.com/codex/subagents
- https://developers.openai.com/codex/config-basic

## Configuration

`parallel-goal-workflows` can use a deeper tree, but depth is capacity, not a
strategy instruction. The skill still has one global strategy owner: the
Orchestrator.

```toml
[agents]
max_threads = 50
max_depth = 5

[features]
multi_agent = true
goals = true
```

`max_depth` counts spawned-agent levels below the root session. The Codex
default is `1`, which allows a direct child but prevents that child from
spawning deeper helpers. Use `5` when the workflow needs room for patterns such
as:

```text
Lead -> Orchestrator -> Worker -> Helper -> Verifier -> Repair
```

## Guardrail

Do not fix Ultra-Strategy by lowering depth. Fix it in the delegation packet:

```text
Global strategy owner: the Orchestrator.
Boundary: delegate local helper work only; do not create another global
Orchestrator or re-invoke parallel-goal-workflows.
```

If an agent tries to spawn another Orchestrator for the same user goal, collapse
that plan into local goals under the current Orchestrator.

## Quick Checks

Inspect user config:

```bash
rg -n "\[agents\]|max_threads|max_depth|multi_agent|goals" ~/.codex/config.toml
```

Inspect project config when present:

```bash
rg -n "\[agents\]|max_threads|max_depth|multi_agent|goals" .codex/config.toml
```
