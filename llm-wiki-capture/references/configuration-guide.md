# Wiki Discovery and Configuration

Read this reference when the target Wiki or its local policy is not already
explicit in the user's current request.

## Configuration Ownership

Resolve each concern from the authority that owns it:

- the user owns the objective, scope, target, mutation stance, and authorization
- the Wiki module owns its schema, provenance, navigation, and content validation
- the containing Git repository owns branch, shared-index, commit, and sync rules
- local or global instructions may identify candidate paths and defaults
- this public skill supplies defaults only where those authorities are silent

An embedded Wiki inherits its parent's write protocol. A standalone Wiki owns
both content and repository policy. Surface material conflicts for the user.

## Target Discovery

1. If the current request explicitly identifies the Wiki path or repository and
   its role is clear, use it.
2. Otherwise inspect known project/global instructions, current or ancestor
   directories, repository markers, and configured paths read-only.
3. Treat a discovered path as a candidate: inspect enough to identify it and ask
   the user to confirm it before using it for branch work. Confirmation already
   given in this session remains valid.
4. If none is found, ask whether the user already has a Wiki and where it lives.
   Offer Bootstrap only after that question and an explicit creation request.

A URL alone establishes neither the Wiki target nor source-ingest intent.
Directory names are user choices; a Wiki need not be named `my-llm-wiki` or own
an independent Git repository.

For an existing notes area that is not clearly an LLM Wiki, inspect structure,
Git state, navigation, provenance, and migration cost read-only. Present the
smallest viable options and let the user choose an in-place upgrade or a new
Wiki before changing structure.

## Minimum Runtime Configuration

Resolve only what the selected branch needs:

- **Content root:** the Wiki module containing its schema and content.
- **Git root and mode:** standalone or embedded; resolve actual Git ownership,
  including worktrees, instead of assuming `.git` is a directory at content root.
- **Read-first files:** applicable ancestor instructions, Wiki instructions,
  purpose, schema, navigation, and likely canonical pages.
- **Path conventions:** which root anchors schema paths, provenance, and links.
- **Validation:** content-scoped command and working directory, plus any required
  parent repository checks.
- **Writes and saves:** clean-worktree scope, ownership, shared save/index
  coordination, branch policy, and commit/push authorization.
- **Identity:** the required identity when a commit is authorized.

A local or review-only workflow needs no hosted remote or fixed directory layout.
For an embedded Wiki, capture the parent's actual save protocol, not a second
independent Git policy. Preserve an explicit parent requirement for a clean
repository; module-scoped checks do not relax it.

## Portable Local Instruction Example

Replace paths and policies with the user's choices. Here the Wiki is embedded
in a context repository; all Wiki-relative paths use the content root:

```markdown
## LLM Wiki

- Content root: <context>/knowledge
- Git root: <context> (embedded; use the parent's Git lifecycle)
- Read first: <context>/AGENTS.md; then AGENTS.md, purpose.md, schema.md,
  and wiki/index.md from the content root
- Validate: scripts/wiki-maintenance check, working directory <context>/knowledge
- Parent validation and save protocol: <context>/AGENTS.md
- Clean-worktree scope: <parent-policy>
- Commit policy: <parent-policy-or-user-choice>
- Push policy: <parent-policy-or-user-choice>
```

For a standalone Wiki, the content and Git roots usually coincide and the Wiki's
own instructions hold the save protocol. Keep machine paths and personal policy
in local instructions; environment skills are optional setup aids, not runtime
dependencies.
