---
name: build-verifier
description: >-
  Create or maintain a project's reusable verification skill and feature map.
  Use for verifier authoring or repairs to its documented workflow.
---

# Build Verifier

Produce a project-local `verify-<app>` that a fresh agent can execute. Reuse an
existing verifier and the project's skill conventions. Ordinary feature
acceptance uses that verifier.

## Project knowledge

Make these properties executable with existing tools:

- **Readiness:** identify the correct build, instance, data and access; diagnose
  surprising failures before continuing.
- **Drive:** exercise public user paths and observe relevant state and side
  effects, including dry-run writes. Mock only an existing external-system
  boundary and mark the substituted behavior unverified.
- **Evidence:** retain actions and resulting state sufficient to prove behavior;
  confirm evidence remains readable after cleanup.
- **Ownership:** isolate scratch data, serialize drivers of a shared instance,
  and remove only this run's resources, including failed attempts. Preserve user
  data, borrowed instances and evidence.

Ground feature paths and success criteria in the repo. Cache hard-to-discover
facts and gotchas; point to canonical commands. Document helper invocations and
match their permissions. Split feature detail only when it improves navigation.

## Create or maintain

For creation, seed grounded paths and run the generated instructions on one
feature before handing them over. Distinguish mapped from live-verified paths.

For maintenance, use the requested scope. Reconcile the map with source; a full
audit also checks for unmapped features. Repair verifier-owned docs and helpers.
If intended product behavior fails, preserve the expectation and report it;
product changes belong to a separate task. Unresolved intent stays unresolved.

Exercise scoped paths and re-drive changed recipes. Report changes, actual
commands/results, retained evidence and coverage gaps. An unexecuted path remains
unverified; blocked execution leaves an explicit draft or partial result.

For Codex, generated verifiers include `agents/openai.yaml` with quoted
`display_name`, a 25–64-character `short_description`, and a `default_prompt`
naming `$verify-<app>`. Preserve invocation policy when maintaining a verifier.
