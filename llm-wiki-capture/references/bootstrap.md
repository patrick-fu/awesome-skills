# Bootstrap a New LLM Wiki

Enter this branch only after the user explicitly asks to create or initialize a
Wiki. Failure to discover one is not authorization to bootstrap it.

## Resolve the Minimum Decisions

Ask only for choices that materially affect the result and cannot be discovered:

- the content location and whether it is standalone or embedded in an existing
  repository, such as a shared context repository
- whether an existing notes area should be upgraded in place
- the applicable save protocol and authorization for commits or remote actions

An independent local Git repository is the default when no containing repository
is selected. Recommend private hosting when cross-machine sync is wanted; an
embedded Wiki uses its parent's existing remote and sync protocol. A new public
remote requires the user's choice.

Inspect the resolved target, actual Git ownership, and nearby candidate Wikis.
For an embedded target, read all applicable parent instructions before creating
files. If the target contains existing content or colliding paths, inspect and
resolve reuse or migration within the user's scope; preserve existing material.
An explicit new module path inside a repository is not itself a collision with
that repository. If standalone versus embedded ownership remains ambiguous,
resolve it before initializing Git.

## Create a Small, Durable Core

Follow existing conventions. A minimal content root can contain:

```text
<content-root>/
  AGENTS.md
  purpose.md
  schema.md
  raw/
    sources/
  wiki/
    index.md
    log.md
    sources/
    concepts/
  scripts/
    wiki-maintenance
```

Give each part one job:

- `purpose.md`: durable inclusion and exclusion boundary
- `schema.md`: page types, provenance, link/path conventions, canonical ownership,
  and update rules
- `raw/sources/`: evidence with recoverable identity
- `wiki/sources/`: source summaries when they add retrieval value
- `wiki/concepts/`: canonical durable knowledge
- `wiki/index.md`: navigation
- `wiki/log.md`: meaningful knowledge changes
- `AGENTS.md`: module operating rules, validator working directory, and the
  actual Git root/save protocol or a pointer to its parent owner

Choose names freely. Add taxonomy and automation only when real content needs
them. Embedded content has a distinct knowledge scope even when task recovery
and knowledge share one Git repository.

## Install a Content-Scoped Check

Create `scripts/wiki-maintenance` using a runtime already guaranteed by the
environment. Its `check` command should:

- verify required module files and directories
- validate the chosen frontmatter or provenance contract
- report broken local Markdown links, including image targets, and resolvable
  Wiki links where practical
- ensure source summaries point to recoverable evidence
- exit nonzero with actionable file-level errors

Anchor checks to the content root, not the Git root. Document path semantics and
the command's working directory; sibling task records or parent documentation do
not become Wiki pages. Run the check successfully and verify it detects a broken
link or provenance error in a disposable example. Reuse parent-required checks
as well. Keep the checker small enough to understand and modify.

When setup is committed, run the checker against a saved-tree extraction as a
fresh consumer. Ensure required files and empty-directory markers survive Git
recovery, rather than relying on directories present only in the working copy.

## Use the Chosen Git Lifecycle

For a new standalone Wiki, initialize local Git and an appropriate ignore policy.
For an embedded Wiki, use the existing parent repository; create no nested Git
repository. Keep raw evidence and content under the chosen module path, while
transient task artifacts follow the environment's artifact policy.

Inspect the parent Git status and index before editing. Follow its ownership,
cleanliness, shared-save, and branch rules. For authorized commits, use the
parent's coordinated save mechanism with the exact owned paths; preserve
unrelated edits and staging. An explicit full-repository cleanliness rule still
applies. If no safe save mechanism is available, retain the scoped changes and
report the unsatisfied save step rather than capturing another writer's work.

Show the file inventory or diff and validation results. Commit only within
existing authorization. Create or push a remote only when authorized for that
action, verifying the actual repository, remote, and branch. An embedded Wiki
uses parent synchronization rather than creating or pushing its own remote.

Connect the chosen content root and read/write triggers to existing context or
global navigation within the requested setup scope. If environment setup skills
are absent, ordinary local instruction links suffice.

## Completion and Delegation

Bootstrap is complete when the confirmed content root exists, purpose and schema
are usable, content validation passes, local routing resolves, and Git/save
behavior matches the selected mode and authorization. Report unperformed remote
or save actions explicitly.

Use the main agent for minimal local setup. Independent perspectives are useful
for substantial notes migration, multi-type schemas, or complex validation.
Assign distinct questions when delegation is warranted.

In review-only mode, present the proposed target, mode, structure, schema,
validation, and save plan. Create nothing.
