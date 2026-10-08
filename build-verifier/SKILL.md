---
name: build-verifier
description: >-
  Create project-local verification skills and feature maps, or repair
  their recipes and maps after observed verification workflow drift.
---

# Build Verifier

Produce a project-local `verify-<app>` that a fresh agent can execute. Reuse an
existing verifier and the project's conventions. Ordinary feature acceptance
uses that verifier.

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

## Create

For creation or changes to discovery and feedback, read
[Project skill](references/project-skill.md). Seed grounded paths and run the
generated instructions on one feature before handing them over. Distinguish
mapped from live-verified paths.

## Maintain

After a verification run, compare observed friction with the recipe and current
source. Correct proven workflow drift or a missing reusable step. Clean runs,
product failures and temporary environment blockers alone need no verifier edit;
unresolved intent stays unresolved.

Keep automatic maintenance scoped to the encountered path and verifier-owned
docs or helpers. Preserve intended expectations when product behavior fails;
report the failure to the product task. Reconcile scoped paths and success
criteria with current source and live evidence. Use the requested scope for
broader audits; a full audit also checks for unmapped features.

Re-drive changed recipes against the real artifact. Stop when the correction is
proved, no drift is established, or a concrete blocker remains.

## Report

Report changes, actual commands/results, retained evidence and coverage gaps.
An unexecuted path remains unverified; blocked execution leaves an explicit
draft or partial result. Preserve invocation policy when maintaining a verifier.
