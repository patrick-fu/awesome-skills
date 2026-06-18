# Codex Nested Subagents

Use this reference when the workflow design calls for nested delegation and the
local Codex environment appears to allow only one subagent layer, lacks
multi-agent tools, or behaves differently from the current official defaults.

Official sources:

- https://developers.openai.com/codex/subagents
- https://developers.openai.com/codex/config-basic

## Table of Contents

- Current default
- Configuration example
- Field meanings
- When to adjust
- Quick checks

## Current default

The Codex subagents documentation says current Codex releases enable subagent
workflows by default. The config basics documentation lists `multi_agent` as a
stable feature with a default of `true`.

This means a normal current install should not need a special feature flag just
to spawn direct subagents. If the tools are absent or a workflow can only create
one generation of child agents, check local configuration, project overrides,
and the installed Codex version.

## Configuration example

```toml
[agents]
max_threads = 50
max_depth = 5

[features]
multi_agent = true
```

Put this in `~/.codex/config.toml` for user-wide defaults, or in a trusted
project `.codex/config.toml` when the setting should apply only to that
project. Codex config precedence can also include CLI overrides, profile files,
user config, system config, and built-in defaults.

## Field meanings

`max_depth` controls how many spawn layers are allowed. The root session starts
at depth 0. The default `max_depth = 1` allows:

```text
main thread -> direct subagent
```

It prevents:

```text
main thread -> subagent -> nested subagent
```

Use `max_depth > 1` when a worker, reviewer, or orchestrator needs to launch
its own child agent. For example, `max_depth = 2` permits one nested generation;
`max_depth = 5` gives enough room for practical multi-stage orchestrator,
worker, review, repair, and acceptance workflows without making recursion
unbounded.

`max_threads` caps concurrent open agent threads. `max_threads = 50` gives a
nested workflow room to fan out and run review or repair agents, but it is still
a cap, not a goal. Raising it too far can make runs harder to inspect and can
increase local resource pressure.

`[features] multi_agent = true` enables the multi-agent feature on installs
that still require an explicit flag. If the current version already enables the
feature by default, or if the key is no longer needed, omit it and rely on the
default.

## When to adjust

Adjust these settings when:

- an orchestrator can spawn direct workers, but those workers cannot spawn their
  own helpers;
- the UI or CLI does not expose multi-agent tools even though the task calls for
  subagents;
- a workflow needs two or more levels of delegation, such as orchestrator ->
  worker -> focused researcher;
- repeated fan-out is exhausting resources, in which case lower `max_threads`
  or `max_depth` instead of adding more process instructions.

Do not raise depth or thread caps just because the task is large. Prefer a
small, explicit workflow shape first, then increase limits only when a concrete
delegation layer is blocked by configuration.

## Quick checks

Inspect the user-level config:

```bash
rg -n "\[agents\]|max_threads|max_depth|multi_agent" ~/.codex/config.toml
```

Also check a project override when present:

```bash
rg -n "\[agents\]|max_threads|max_depth|multi_agent" .codex/config.toml
```

If those files are absent or omit the fields, Codex falls back through its
documented precedence chain to built-in defaults.
