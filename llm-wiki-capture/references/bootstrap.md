# Bootstrap A New LLM Wiki

Enter this branch only after the user explicitly asks to create or initialize a
Wiki. Failure to discover a Wiki is not authorization to bootstrap one.

## Confirm The Minimum Decisions

Ask only for choices that materially change the result and cannot be discovered
reliably:

- where the local repository should live
- whether to use local Git only or a hosted remote
- whether an existing notes repository should be upgraded in place
- whether commit, remote creation, or push is authorized

Recommend a private hosted repository when the user wants cross-machine sync
and backup. A local Git repository is a complete safe fallback. Never default
to a public remote, and never create a remote merely because credentials are
available.

If an existing notes repository may be reused, inspect it read-only first and
then ask whether to upgrade it in place or create a separate Wiki.

Before creating files, inspect the resolved target and nearby candidate Wikis.
If the target is non-empty, contains colliding paths, or another LLM Wiki may
already own the knowledge, report what exists and ask whether to reuse, migrate,
or create a separate repository. Never overwrite an existing path during
Bootstrap.

## Create A Small, Durable Core

Follow the user's existing conventions when present. Otherwise start with:

```text
my-llm-wiki/
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

Give each file one job:

- `purpose.md`: durable inclusion and exclusion boundary
- `schema.md`: page types, provenance, links, canonical ownership, and update
  rules
- `raw/sources/`: source evidence with recoverable identity
- `wiki/sources/`: source-level summaries when they add retrieval value
- `wiki/concepts/`: canonical durable knowledge
- `wiki/index.md`: navigation and discovery
- `wiki/log.md`: meaningful knowledge changes, not chat chronology
- `AGENTS.md`: portable operating and validation instructions for this repo

Do not prebuild a large taxonomy, query system, automation stack, or personal
policy. Add those only after real content creates pressure for them.

## Install A Zero-Dependency Check

Create `scripts/wiki-maintenance` from day one, using only the language runtime
already guaranteed by the environment. Its `check` command should at minimum:

- verify required files and directories
- validate the small frontmatter or provenance contract actually chosen for the
  repository
- find broken local Markdown links and resolvable Wiki links where practical
- ensure every source summary points to recoverable source evidence
- exit nonzero with actionable file-level errors

Keep the first checker small enough to understand and modify. Extend it only as
the schema gains real invariants. Run it successfully before declaring the
Bootstrap complete.

## Initialize Git Safely

Initialize local Git and add an appropriate `.gitignore`. Show the initial diff
or file inventory and validation result. Commit only after authorization.

Create a hosted repository only after explicit authorization. Prefer private
visibility, verify the resolved remote and branch, and push only after separate
authorization. Report what was created and where.

## Delegation

Use the main agent for a minimal local Bootstrap. Prefer valuable subagent
perspectives when an existing notes repository needs migration analysis, a
schema must serve several content types, or remote and validation design can be
reviewed independently. Assign distinct questions rather than a fixed agent
count.

Bootstrap is complete when the repository exists at the confirmed target, its
purpose and schema are understandable, `wiki-maintenance check` passes, and all
remote, commit, and push actions match explicit authorization.

In review-only mode, stop after presenting the proposed target, structure,
schema choices, validation plan, and authorization gates. Create nothing.
