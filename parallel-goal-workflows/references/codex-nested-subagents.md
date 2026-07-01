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
spawning deeper helpers. Raise it only when the assigned goal has concrete,
narrower helper work that can be verified independently.

Depth is capacity, not permission to create coordination-only layers. Each
nested helper must receive a local task that is smaller than its parent task and
must return evidence upward. Do not add a pure coordinator, and do not transfer
the current assignment wholesale to another agent.

`max_threads` caps concurrent open agent threads. Raise it only when the
workflow has a concrete fan-out need.

## Delegation Packet

Depth gives capacity; the local brief gives shape. When nested helpers are used,
ask for one concrete local outcome in natural language. If the Codex host needs
the in-band `/goal` command to put the spawned agent into goal mode, place
`/goal` on its own first line. This is runtime syntax, not task context; do not
include `$parallel-goal-workflows`, parent identity, or delegation-chain details.

```text
/goal

[one concrete local outcome.]

Please [inspect / implement / review / verify / research] the following local
task:

[Specific task details.]

Relevant context:
[Only the facts needed for this local task.]

Scope and boundaries:
[Owned files, systems, decisions, and areas to avoid.]

Return:
- what you inspected, changed, verified, or decided
- evidence requested by the task
- risks, uncertainty, and unhandled items
- anything that should pause further work

Pause if approval, credentials, destructive action, or an ownership conflict is
required.
```

If a child agent starts solving a broader task than it was assigned, restate the
local goal and boundary before adding more depth. Do not tell helpers about the
full delegation chain; give them only the context required for their local task.

## Quick Checks

Inspect user config:

```bash
rg -n "\[agents\]|max_threads|max_depth|multi_agent|goals" ~/.codex/config.toml
```

Inspect project config when present:

```bash
rg -n "\[agents\]|max_threads|max_depth|multi_agent|goals" .codex/config.toml
```
