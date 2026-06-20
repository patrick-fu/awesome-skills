# Codex Nested Subagents

Use this reference only when Codex depth or multi-agent tooling blocks the
workflow.

Official sources:

- https://developers.openai.com/codex/subagents
- https://developers.openai.com/codex/config-basic

## Configuration

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
Main Agent -> Workflow Owner -> Researcher -> Verifier -> Repair helper
```

`max_threads` caps concurrent open agent threads. Raise it only when the
workflow has a concrete fan-out need.

## Delegation Packet

Depth gives capacity; the packet gives shape. When nested helpers are used,
include:

```text
Local goal: [narrow task].
Context: [facts needed for this local goal].
Boundary: [owned files, systems, decisions, and areas to avoid].
Deliverable: [result, evidence, verification, risks, or decision].
Pause if: [approval, credentials, destructive action, or ownership conflict].
```

If a child agent starts solving a broader task than it was assigned, restate the
local goal and boundary before adding more depth.

## Quick Checks

Inspect user config:

```bash
rg -n "\[agents\]|max_threads|max_depth|multi_agent|goals" ~/.codex/config.toml
```

Inspect project config when present:

```bash
rg -n "\[agents\]|max_threads|max_depth|multi_agent|goals" .codex/config.toml
```
