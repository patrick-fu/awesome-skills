---
name: llm-wiki-capture
description: >-
  User-invoked router for reviewing or capturing session knowledge, ingesting
  sources, integrating an existing LLM wiki, or bootstrapping one from zero.
disable-model-invocation: true
---

# LLM Wiki Capture

Route an explicit user request into the right LLM Wiki workflow. Keep this file
as the thin router; load only the reference for the selected branch.

## 1. Resolve Intent

Choose the business branch from the user's words, not merely from the presence
of a URL or repository:

- **Session Capture**: review or persist reusable knowledge learned in the
  current or identified historical session.
- **Source Ingest**: supplied external material is the object of an explicit
  ingest request (for example "入库", "炼化", or "沉淀这些资料") or a review
  of whether and how it should enter the Wiki.
- **Full Integration**: the user explicitly asks for a whole-Wiki audit,
  reorganization, or synthesis pass.
- **Bootstrap**: the user explicitly asks to create or initialize a new Wiki.

`review-only` is an orthogonal mutation stance, not a fifth business branch. It
can apply to Session Capture, Source Ingest, Full Integration, or Bootstrap.

A URL can be discussion context rather than an ingest target. "评估这篇材料是否
值得入库" selects Source Ingest with review-only stance; "参考这篇材料讨论另一
个问题" keeps it as task context. A bare URL remains ambiguous. If the intended
branch or mutation stance is not fully clear, ask before acting.

## 2. Resolve The Wiki Target

Read [`references/configuration-guide.md`](references/configuration-guide.md)
when the Wiki path, repository, authority, or write policy is not already
explicit in the current request.

Never enter Bootstrap merely because a Wiki was not found. Ask whether the user
already has one and where it lives. Enter Bootstrap only after the user
explicitly asks to create or initialize one.

## 3. Load The Selected Branch

Read the selected reference completely before taking branch actions:

| Branch | Load |
| --- | --- |
| Session Capture | [`references/session-capture.md`](references/session-capture.md) |
| Source Ingest | [`references/source-ingest.md`](references/source-ingest.md) and [`references/provenance-contract.md`](references/provenance-contract.md) |
| Full Integration | [`references/full-integration.md`](references/full-integration.md) and [`references/provenance-contract.md`](references/provenance-contract.md) |
| Bootstrap | [`references/bootstrap.md`](references/bootstrap.md) |

For any write-capable run, also read
[`references/integration-contract.md`](references/integration-contract.md)
before editing. In review-only mode, use it only to determine what would change
and stop before mutation.

## 4. Finish The Routed Workflow

The selected branch owns its discovery, evidence, delegation, and completion
criteria. The integration contract owns shared write, verification, commit, and
push rules. Do not import or require another skill to complete this workflow.
