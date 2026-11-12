# Setup and Migration

Establish a source repository pool and task worktree layout that fits the user's
environment. Reuse working configuration and fill only the gaps. Present a short
proposal of paths, defaults, and intended changes; resolve unknown durable
locations or migration scope with the user when existing instructions do not
settle them.

## 1. Discover the Existing Layout

Inspect known development directories and entry instructions for source clones,
registered worktrees, task owners, branch rules, sync tools, and unfinished work.
Check actual repository roots and remotes, not directory names alone.

Locate any existing task-context destination, issue tracker, and artifact policy.
An environment may already have these without a `work-context` skill installed.
Keep unrelated repositories and active work intact.

## 2. Choose Defaults and Local Variations

Existing user choices take precedence. For a new layout, recommend:

| Choice | Default recommendation | Customization |
| --- | --- | --- |
| Root | Reuse the development root, or propose one for the user to select | Path, disk, and organizational grouping |
| Source pool | `<root>/source/<repo>` with clean source checkouts | Names, repository map, and per-repository trunk branches |
| Task workspace | `<root>/workspace/<task>/<repo>` using linked worktrees | Names, task grouping, and branch naming |
| Starting revision | The project's current approved baseline | A named branch, older revision, or existing task branch |
| Migration | Gradual adoption; leave existing working repositories in place | Explicitly scoped full migration |
| Source sync | Reuse the existing mechanism; otherwise sync on demand | Entry point, cadence, and responsible writer |
| Durable notes | An existing issue, documentation location, or configured context store | Another durable destination selected by the user |
| Artifacts and cleanup | Disposable task outputs in the workspace or system temp | Storage, retention, and archive destination |

Keep code and versioned project documentation in their repositories. Choose the
notes destination before creating unique checkout-external material. The absence
of a context skill does not require creating another repository.

Record real paths, repository routes, baselines, task branch conventions, sync
rules, notes locations, and cleanup responsibilities in local instructions.
Source synchronization does not imply permission for a new scheduled job.

## 3. Prepare or Migrate the Required Repositories

Create only the directories and source clones needed for the first task. For
each repository, verify its remote and approved baseline. Keep the source
checkout for inspection and repository administration; use linked task worktrees
for edits, builds, and generated output.

For a new task branch, adapt:

```sh
git -C "<source>/<repo>" worktree add -b "<task-branch>" \
  "<workspace>/<task>/<repo>" "<start-point>"
```

For an existing branch or worktree, reuse its compatible state instead of creating
a duplicate. Add repositories as the task requires them; the full dependency set
need not be known before work begins.

Under gradual adoption, keep existing working locations and direct new work into
the new layout. For a full migration, inventory dirty, untracked, ignored, and
unmerged work first; preserve it under the responsible owner's rules. Move
registered worktrees using supported Git operations and verify their references
and recovery paths before clearing old locations.

## 4. Connect the Local Entry Instructions

Integrate concise rules into existing instructions rather than replacing them
with templates. Keep one maintained source for shared details. Adapt these
examples with actual paths and remove unused entries.

### Source Pool Entry

```markdown
# Source Repositories

- Use these checkouts for inspection, clone/fetch, and approved source sync.
- Make task edits, run builds, and write task artifacts in <workspace>/<task>/.
- Repository routes and approved baselines: <local-repository-map>.
```

Keep the repository map coarse: repository identity, purpose, and baseline are
enough to route work. Inspect repository content when deeper detail is needed.

### Task Workspace Entry

```markdown
# Task Workspaces

- Reuse the task's existing directory and worktrees; add linked worktrees from
  <source> for missing repositories. Respect current owners and branch rules.
- Keep durable task notes in <notes-location>; code and versioned project
  documentation stay in their repositories. Put disposable outputs in <temporary>.
- Before cleanup, confirm active users are finished, inspect all worktree and
  checkout-external files, and preserve unique material and unmerged commits.
  Verify required saves and syncs, then use git worktree remove and clear only
  disposable outputs. Preserve management files and other tasks' working state.
```

### Agent Entry Point

Add a short routing rule to the instructions the user's agent tools actually
load, preserving their existing scope and content:

```markdown
## Code Workspaces

- Use <workspace>/<task>/ for task code worktrees from <source>.
- Read <source>/AGENTS.md for repository routing and <workspace>/AGENTS.md for
  working and cleanup rules. Save durable task notes in <notes-location>.
```

Deployed instructions should be sufficient for ordinary work even without the
skill installed. Optional guidance can name `git-task-workspace` when available;
avoid hardcoded skill installation paths. Verify deployed content and reachable
references from each normal starting location.

For a requested shared-context setup, consult `work-context` if available in the
current skill catalog. Otherwise, use the existing issue or documentation
workflow. When both environments exist, reuse the configured context destination
and code paths; the later setup fills its own gaps without rebuilding the other.

## 5. Verify the First Task and Cleanup

Use an authorized task or an isolated disposable example:

1. Enter through the normal instructions and identify the correct repository,
   baseline, owner, and notes destination.
2. Create or reuse a linked worktree, confirm its Git registration, and inspect
   its path, branch, and starting revision. Check that task output lands outside
   the source checkout.
3. Resume from the durable task record and verify that paths and versions match.
4. For a disposable cleanup example, place unique material inside and outside a
   worktree. Follow the preservation policy before removing it, verify recovery
   from the destination, and check that management files and unrelated worktrees
   remain usable. A removal refusal is a reason to inspect state, not force it.

Report actual results and unverified migration, synchronization, or cleanup paths.
Timers, automated pruning, and other infrastructure are optional follow-up work.
