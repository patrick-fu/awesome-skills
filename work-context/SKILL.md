---
name: work-context
description: >-
  Initialize or reconfigure a shared context environment and its local agent
  instructions. Use for first setup, migration, connecting another agent
  harness, or repairing configuration drift.
---

# Work Context

Set up a common starting place for work across projects, sessions, and agent
harnesses. Deliver the daily recovery and persistence rules into the user's
local instructions, so ordinary work continues without this skill installed.

## Workflow

Read [Setup and Migration](references/setup.md) for discovery, defaults, local
instruction templates, optional Wiki integration, and acceptance checks.

1. **Discover.** Identify the actual agent entry points, context destination,
   code locations, knowledge stores, and existing write rules. Separate working
   choices from missing configuration and conflicts.
2. **Configure.** Reuse the user's names and paths. Propose defaults only for
   gaps; resolve choices that affect durable location, ownership, migration,
   or sharing. Create the smallest useful recovery path.
3. **Deploy.** Merge short routing rules into global instructions and daily
   operating rules into the chosen context root's `AGENTS.md`. Connect existing
   source and workspace instructions by their real paths. Preserve unrelated
   rules and give each detailed policy one local owner.
4. **Verify.** Start from the deployed instructions without loading this skill.
   Recover a task, refresh changed sources, and save through the configured
   protocol. Check the actual consumer and report unverified entry points.

Completion is a usable local environment with resolved paths and policies, not
merely a proposed layout or a reference back to this skill. Daily task recovery
and updates follow the deployed instructions; return here when setup changes.

## Optional Integrations

Installation and environment configuration are separate facts. If source and
workspace setup is requested, use `git-task-workspace` when it is available in
the current skill catalog; otherwise retain the existing code workflow.

A Wiki can live inside the context repository or separately. Reuse its configured
access policy. New Wiki initialization needs the user's explicit request; if
`llm-wiki-capture` is available, the user can invoke it for that work. Neither
integration is required for a working context environment.
