# Wiki Integration Contract

Apply this contract to every write-capable branch.

## Before Editing

1. Confirm the target repository when it came from discovery rather than the
   current user request.
2. Read the repository instructions, purpose, schema, navigation, maintenance
   commands, and the likely canonical owner pages.
3. Run any repository-required pre-write maintenance and synchronization steps
   in their documented order. Never pull into a dirty or unconfirmed target.
4. Inspect Git status. Preserve unrelated user changes. If local policy
   requires a clean worktree and unrelated changes exist, stop at a proposed
   diff or review report.
5. Resolve the mutation boundary. Repository rules can define structure and
   validation, but only the user can authorize materially broader scope,
   repository creation, commit, push, destructive moves, or public exposure.

## Canonical Integration

Integrate knowledge by ownership rather than by the session or source that
revealed it:

- update an existing canonical page when one owns the knowledge
- merge equivalent claims while preserving their independent provenance
- keep conflicting claims visible until evidence or the user resolves them
- create a new page only when it has an independent claim and independent
  retrieval value
- update indexes, logs, overview pages, and backlinks required by the local
  schema

Use review-only as a hard mutation boundary. In review-only mode, inspect and
report candidate changes, but make no file edits, commits, pushes, remote
repository changes, or external publications.

## Confirmation Gates

Always ask before writing when the change depends on:

- inferred user intent or preference
- promotion from project scope to user-global scope
- choosing between conflicting canonical claims
- sensitive personal information

Also ask before replacing, deleting, marking knowledge obsolete, changing the
schema, or moving files destructively when the current request did not already
authorize that exact action.

When a user-provided SOP conflicts with repository evidence, tool results, or
existing Wiki content, research the discrepancy read-only and then always ask
the user which account should be canonical. Do not auto-resolve it even when
one explanation appears likely.

## Verification

After editing:

1. inspect the complete diff against the original request and local schema
2. verify every changed page's provenance, owner, links, and navigation impact
3. run the repository's maintenance command when one exists
4. run `git diff --check`
5. report skipped, disputed, superseded, and still-unverified candidates

Commit only when the user or an applicable local policy explicitly authorizes
it. Push only when separately authorized; fetch first and stop on a
non-fast-forward conflict. Never force-push a user's Wiki as a capture shortcut.
A user-owned repository policy that explicitly authorizes push satisfies this
separate authorization boundary.

Completion means the requested knowledge is integrated and verified, or the
review report makes every unresolved decision explicit. A commit or push is not
part of completion unless authorized.

If no candidate survives the selected branch's evidence and value gates, make
no changes and report the empty result with the reason.
