# Wiki Integration Contract

Apply this contract to every write-capable branch.

## Before Editing

1. Confirm a discovered target unless the user has already confirmed it in this
   session. Resolve the content root and actual containing Git root separately.
2. Read applicable parent instructions and the Wiki's purpose, schema, navigation,
   maintenance commands, and likely canonical pages. Check path conventions:
   content-relative evidence paths need not be repository-relative Git paths.
3. Run required pre-write checks and the repository owner's synchronization
   protocol. For an embedded Wiki, use the parent protocol rather than running
   an independent pull. A direct pull needs a clean, confirmed target and local
   authorization.
4. Inspect the containing repository's status and index. Preserve unrelated
   edits and staging. An explicit full-repository cleanliness requirement still
   applies: if it is unmet, stop at a proposal or review report. Otherwise use
   the configured ownership/shared-write protocol for the permitted scope.
5. Resolve mutation scope and authorization. Local rules can govern structure,
   validation, and saves; the user owns broader scope, repository creation,
   destructive moves, and public exposure.

## Canonical Integration

Integrate by knowledge ownership rather than session or source chronology:

- update an existing canonical page when it owns the knowledge
- merge equivalent claims while preserving independent provenance
- keep conflicting claims visible until evidence or the user resolves them
- create a page only for an independent claim with independent retrieval value
- update navigation, logs, overviews, and backlinks required by the local schema

Review-only is a hard mutation boundary: report candidate changes without edits,
commits, pushes, repository creation, or external publication.

## Confirmation Gates

Ask before writing when a change depends on inferred user intent or preference,
promotion from project to user-global scope, a choice between conflicting
canonical claims, or sensitive personal information.

Ask before replacing, deleting, marking knowledge obsolete, changing schema, or
moving files destructively unless the current request already authorizes that
action. Existing authorization in this session remains valid.

When a user-provided SOP conflicts with repository evidence, tools, or Wiki
content, research read-only and ask which account should be canonical.

## Verification and Saves

After editing:

1. inspect the owned diff against the request, schema, and initial Git state
2. verify changed pages' provenance, ownership, links, and navigation impact
3. run content validation from its documented working directory, plus required
   parent checks; sibling files remain outside Wiki schema validation
4. run `git diff --check` for owned paths from the actual Git root
5. verify unrelated edits and staging were preserved; report skipped, disputed,
   superseded, and unverified candidates

Commit when the user or applicable local policy explicitly authorizes it. For an
embedded Wiki, coordinate through the parent's saver, lock, or existing helper
using explicit repository-relative owned paths. Preserve other writers' staging;
a blanket add or commit of the shared index can include unrelated work. If the
configured protocol cannot safely save the owned changes, report the blocked save
without disturbing the other work.

Push only when separately authorized, through the containing repository's sync
protocol. Fetch first and stop on a non-fast-forward conflict; never force-push
as a capture shortcut. An applicable user-owned policy explicitly authorizing
push satisfies that boundary. Embedded Wikis inherit the parent's repository,
remote, and branch lifecycle, with no separate Git initialization or remote.

Completion means the requested knowledge is integrated and verified, or a review
report makes unresolved decisions explicit. Commit/push are completion criteria
only when authorized. If no candidate passes the selected branch's evidence and
value gates, leave content unchanged and explain the empty result.
