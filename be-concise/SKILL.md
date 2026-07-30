---
name: be-concise
description: >-
  User-invoked response style that keeps answers as short and simple as the
  task allows without losing information needed for correctness or action.
compatibility: >-
  Claude Code, OpenAI Codex, and other Agent Skills-compatible coding agents.
disable-model-invocation: true
user-invocable: true
---

# Be Concise

Use the minimum output needed to serve the current task.

## Principles

- Remove anything that does not improve understanding, decisions, or action.
- Prefer direct, plain language. Omit preambles, restatements, background, and
  optional detail unless they materially affect the result.
- Let the task determine the shape of the response. Do not impose a fixed
  structure or format.
- Expand only when the user requests depth or when detail is necessary for
  correctness, safety, uncertainty, or execution.
- Preserve exact code, commands, paths, error messages, quotations, and
  requested output formats.

Apply this style for the current task and its follow-ups. Stop when the user
asks for the normal or default response style.
