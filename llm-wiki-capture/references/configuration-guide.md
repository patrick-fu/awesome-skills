# Wiki Discovery And Configuration

Read this reference when the target Wiki or its local policy is not already
explicit in the user's current request.

## Configuration Ownership

Resolve each concern from the authority that owns it instead of forcing one
global precedence chain:

- the user owns the objective, scope, target repository, mutation stance, and
  commit or push authorization
- the Wiki repository owns its schema, provenance model, navigation, validation
  commands, and content conventions
- local or global agent instructions may identify candidate paths and defaults
- this public skill supplies defaults only where the user and repository are
  silent

Surface a material conflict and ask the user. Do not silently let a convenient
default override the owner of that concern.

## Target Discovery

Use this sequence:

1. If the current request explicitly identifies the Wiki path or repository and
   its role is clear, use it.
2. Otherwise perform read-only discovery in project and global instructions,
   the current or ancestor directories, repository markers, and any configured
   fixed path.
3. Treat anything found outside the current request as a candidate. Inspect only
   enough to identify it, report what was found, and ask the user to confirm it
   before using it as the target for branch work.
4. If nothing is found, ask whether the user already has a Wiki repository and
   where it lives.
5. Offer Bootstrap only after that question. Do not create a repository until
   the user explicitly requests creation.

Do not interpret an arbitrary URL as the Wiki repository or as source-ingest
intent without confirming its role.

## Existing Notes Repositories

If discovery finds an existing notes repository that is not clearly an LLM
Wiki:

1. inspect it read-only to understand structure, Git state, navigation,
   provenance, and likely migration cost
2. report the evidence and the smallest viable options
3. ask whether to upgrade it in place or create a separate Wiki

Even when the evidence strongly favors one option, let the user choose before
changing structure.

## Minimum Runtime Configuration

Resolve only what the selected branch actually needs:

- knowledge-base root
- read-first repository instructions and schema files
- canonical navigation or log files, when present
- clean-worktree policy
- branch policy
- commit and push authorization
- commit identity when a commit is authorized

Do not require a clone URL, hosted remote, fixed folder layout, or automation
policy for a local or review-only workflow.

## Portable Local Instruction Example

```markdown
## LLM Wiki
- Root: ~/path/to/my-wiki
- Read first: AGENTS.md, purpose.md, schema.md, wiki/index.md
- Validate with: scripts/wiki-maintenance check
- Require a clean worktree before edits: yes
- Commit policy: ask
- Push policy: ask
```

Keep machine-specific paths and personal preferences in the user's local
instructions rather than in the public skill.
