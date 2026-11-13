---
name: clean-technical-writing
description: >-
  Keep research reports, postmortems, explanatory HTML pages, public
  technical articles, and prompt or tool descriptions neutral, direct, and
  single-layered across any language. Use when drafting or editing prose,
  UI copy, or request descriptions meant for readers; skip when an explicit
  personal-voice preference overrides.
---

# Clean Technical Writing

Apply these rules in the deliverable's language (Chinese, English, or mixed).
When an explicit personal-essay voice is requested (`patrick-personal-writing-preferences`),
that voice takes precedence; otherwise keep all reader-facing prose, HTML copy,
and request descriptions under these rules.

## 1. Neutral, subject-first facts

Make the system, artifact, mechanism, or constraint the grammatical subject.
State what happens and under what conditions without naming people, assigning
roles, or framing sentences as instructions aimed at someone ("for <person>",
"requires <role> to...", "面向某人", "需要某角色配合").

## 2. Direct claims, zero hedging or jargon

State verified scope and real preconditions directly. Never add defensive
disclaimers or contrast hedges ("A does not mean B", "X cannot prove Y",
"although..., it does not indicate...", "仅供参考", "A 不代表 B"). Replace
internal slang and buzzwords with concrete nouns and actions.

## 3. Single-layer labels, no secondary explanations

Keep headings, labels, badges, buttons, and cards self-explanatory on one
layer. Omit explanatory subtitles, secondary labels, and helper captions that
restate or gloss the primary item; keep only copy required for an operational
judgment.

## Examples

Report / postmortem:
- Before: "面向测试同学：本次绿灯仅覆盖了单节点，并不代表线上全链路可用，仅供参考。"
- After: "本次测试仅覆盖单节点环境；全链路可用性仍待多节点验证。"

Explanatory HTML / UI label:
- Before:
  Heading: "队列等待时长" + Subtitle: "用于展示任务在执行前排队等待的时间，帮助你理解当前瓶颈"
- After:
  Heading: "队列等待时长（p95）"
