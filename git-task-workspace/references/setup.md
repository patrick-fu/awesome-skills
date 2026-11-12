# Setup and Migration

Deliver a source pool and task workspace environment that agents can use without
this skill installed. Reuse working configuration; resolve unknown permanent
locations, migration scope, and preservation destinations before dependent edits.

## 1. Discover the Environment

Inspect known development directories and loaded agent instructions for source
clones, registered worktrees, active owners, baseline and branch rules, sync
mechanisms, recovery destinations, and artifact retention. Verify Git roots and
remotes instead of assigning roles from directory names.

The context destination, source pool, and task workspace root are distinct roles.
The user can name them freely. Preserve their actual names and paths, including
layouts configured without either environment skill installed.

## 2. Choose Defaults and Local Variations

Existing choices take precedence. For a new layout, recommend:

| Choice | Default recommendation | Customization |
| --- | --- | --- |
| Location | Reuse an appropriate development/storage root | Disk, directory names, grouping |
| Source pool | `<root>/source/<repo>` with clean source checkouts | Repository map and per-repository baseline |
| Workspace | `<root>/workspace/<task>/<repo>` linked worktrees | Task grouping and branch naming |
| Starting revision | Project's approved baseline, resolved before checkout | Named branch, older revision, existing task branch |
| Adoption | Gradual; preserve current working repositories | Explicitly scoped migration |
| Source sync | Existing mechanism, otherwise on demand | Writer, cadence, and supported entry point |
| Recovery | Existing issue, notes area, or configured context | Destination, owner, validation, save/sync policy |
| Artifacts | `<workspace>/<task>/artifacts/`, outside code worktrees | Subdirectories, retention, storage, archive destination |
| Cleanup | After task use ends and unique material is preserved | Owner, archive branch/location, required saves/syncs |

Workspace artifacts are local and normally outside Git: downloaded packages,
screenshots, recordings, E2E evidence, experiments, and research output can survive
restarts and handoffs until task cleanup. Use system temp for shorter-lived
scratch. Keep durable conclusions in the recovery destination; code and versioned
project documentation stay in their repositories.

Record chosen paths and policies in local instructions. A source or workspace
root need not be a Git repository. Respect an existing parent repository's ignore
policy so task outputs are not accidentally tracked. Source sync setup does not
imply a new timer or scheduled job.

## 3. Deploy the Daily Operating Rules

Merge these fragments into the instructions the user's harnesses actually load.
Replace placeholders with real paths and chosen policies, omit unused entries,
and preserve unrelated content. Each detailed policy has one local owner.

### Global Agent Instructions

```markdown
## Task Code Workspaces

- Use <workspace>/<task>/ for task code and artifacts. Read <source>/AGENTS.md
  for repository routing and <workspace>/AGENTS.md for task operations.
- Find existing work and save durable recovery at <recovery-location>, following
  <recovery-instructions>. Keep source checkouts for inspection and administration.
```

When a context entry already supplies routing, extend it instead of creating a
second competing map. Verify each harness reads these instructions; use a thin
`CLAUDE.md` or other supported adapter when needed.

### Source Root AGENTS.md

```markdown
# Source Repositories

- Repository routes and approved baselines: <repository-map-or-inline-entries>.
  Verify remote identity and current project rules before creating task worktrees.
- Keep these checkouts clean for inspection and repository administration:
  clone missing repositories here, fetch as needed, and use <source-sync-policy>
  for approved baseline updates. Preserve unexpected local changes for their
  owner. Make task edits and run builds in <workspace>/<task>/<repo>.
- Read <workspace>/AGENTS.md when creating or expanding a task workspace.
  Durable recovery: <recovery-location-and-instructions>.
```

The repository map needs only identity, purpose, location, and approved baseline.
Reuse an existing map and maintain each repository entry in one place; inspect
repository content for implementation details.

Keep a short map flat. When navigation becomes difficult, use the existing domain
grouping or split the map by domain. Deploy a brief use condition and index path
for each domain in the source instructions, for example:

```markdown
- Client apps (UI and device behavior): see repos/client.md.
- Services (APIs and background jobs): see repos/services.md.
```

After grouping, repository details belong in the domain indexes. Context and
global instructions point to the map's entry point.

### Workspace Root AGENTS.md

````markdown
# Task Workspaces

- Find the existing task through <recovery-location>; reuse its directory,
  owner, branches, and compatible worktrees. Read each repository's instructions
  before editing. Shared workspace management files are persistent configuration.
- Source pool: <source>; repository map and sync policy: <source>/AGENTS.md.
  For a missing repository, clone it into the source pool first. Resolve the
  project's approved starting revision and branch convention <branch-policy>.
  Create only the worktrees needed now; add more as the task's scope grows.

  ```sh
  git -C "<source>/<repo>" worktree add -b "<task-branch>" \
    "<workspace>/<task>/<repo>" "<start-point>"
  ```

- For an existing branch or worktree, inspect and reuse compatible state while
  respecting its owner. Record each repository's worktree path, branch, and
  relevant revision in the task recovery entry, including new dependencies.
- Edit and build inside task worktrees. Keep downloads, screenshots, recordings,
  E2E evidence, and other local task output in <workspace>/<task>/artifacts/.
  These remain available across sessions until task cleanup. Use <scratch-path>
  for disposable process scratch. Keep code and versioned project docs in Git.
- Save concise conclusions and evidence paths in <recovery-location>, using
  <recovery-write-and-sync-policy>. Flag evidence that is missing or moved.
- Before cleanup, confirm active users and resource holders are finished.
  Inspect tracked, untracked, ignored, and checkout-external files, plus commits
  not integrated into the intended baseline. A clean Git status alone is
  insufficient. Preserve unique material at <archive-destination> and unmerged
  commits under <archive-branch-policy>; verify recovery and required saves/syncs
  before removal. Update the recovery entry with preserved locations.
- Remove worktrees with git worktree remove from their source repository, then
  remove only disposable task output and task-owned temporary branches. Inspect
  a removal refusal and preserve its cause before retrying; force removal needs
  verified preservation and applicable authorization. Keep archive branches,
  root management files, and other tasks' worktrees usable. Prune only stale
  registrations after checking their paths.
````

Adapt the worktree command for an existing branch. For a hosted or managed
worktree lifecycle, keep its required creation/removal API and record how it
maps to these locations. Do not replace it with raw Git commands.

If recovery already lives in a context repository, link its `AGENTS.md` and reuse
its save policy. With only this skill installed, an existing issue or notes area
is sufficient. When shared-context initialization is also requested,
`work-context` can configure it if available in the current catalog. Missing peer
skills do not require installation or another repository.

## 4. Prepare or Migrate Only What Is Needed

Create the selected roots and first required source clones. Verify remotes,
baselines, worktree registrations, and recovery links. Add no speculative
repository dependency set.

Gradual adoption leaves existing working checkouts in place and routes new work
through the layout. A full migration starts with an inventory of owners, dirty,
untracked, ignored, checkout-external, and unmerged material. Use supported Git
worktree moves; preserve identities and verify recovery before clearing old paths.

## 5. Verify Without the Environment Skills

Use an authorized task or isolated disposable fixture. Give a fresh consumer only
the deployed local instructions, with `git-task-workspace` and `work-context`
absent from its skill catalog:

1. From a normal entry point, locate the repository, baseline, existing task,
   owner, and recovery destination. Follow deployed domain pointers when the map
   is grouped.
2. Create or reuse a worktree; verify its Git registration, branch, and starting
   revision. Add a second repository later and update the recovery record.
3. Save task evidence outside the worktrees, resume in a new session, and read
   the same artifact and code revisions from the recovery entry.
4. In a disposable cleanup case, preserve unique tracked, untracked, ignored,
   and checkout-external material plus an unmerged commit. Verify recovery
   before removal and confirm management files and unrelated worktrees survive.

Report actual results and unverified harness, migration, sync, or conflict paths.
A written template alone is not an accepted operating environment.
