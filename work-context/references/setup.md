# Setup and Migration

Make one ongoing task recoverable from the user's normal agent entry points.
Reuse working configuration and fill only the gaps. Present a concise proposal
with recommended defaults; resolve unknown durable locations, sharing boundaries,
sync targets, or migration scope with the user when existing instructions do not
settle them.

## 1. Discover the Existing Environment

Inspect known configuration and project directories for:

- Instructions actually loaded by the agent tools in use, such as `AGENTS.md`
  or `CLAUDE.md`.
- Existing task records, trackers, knowledge stores, code workspaces, and owners.
- Persistence, write, validation, and sync rules, including unfinished changes.

Distinguish the session's starting directory, the context store, and code working
directories. Verify repository roots where Git is involved; an ordinary directory
may otherwise be mistaken for an unrelated ancestor repository.

Separate existing choices, missing choices, and conflicts before proposing changes.

## 2. Choose Defaults and Local Variations

Existing user choices take precedence. For a new environment, recommend:

| Choice | Default recommendation | Customization |
| --- | --- | --- |
| Context store | A separate Git-managed `<root>/work-context/` | An existing directory, documentation area, or durable service |
| Structure | A short index and task entries added as needed | Names, hierarchy, and task granularity |
| Business fields | Keep existing tracker authority; context holds execution recovery | Field ownership and snapshot refresh rules |
| Code workspace | Reuse current repositories and working directories | Ordinary checkouts, task worktrees, or remote execution |
| Saving and sync | Local version history; commit validated milestones | Existing cadence, remote, and sync mechanism |
| Sharing | One writer until concurrent writing is required | An existing atomic update service or coordinated shared checkout |
| Artifacts | Concise text records; raw outputs outside the context store | Allowed formats, size limits, storage, and retention |

Choose the root from the user's environment rather than inventing a permanent
location. If there is no configured remote, keep the initial environment local;
setting up context does not select a publication destination. Keep existing
checkout and branch policies. A new single-writer context repository can use its
ordinary checkout without task worktrees.

A tracker may already be sufficient for simple work. Add local context only when
recovery needs material the tracker does not hold. Projects express continuing
goals, tasks express scoped work, and sessions identify execution instances.
Keep parent, blocking, source, and ordinary reference links distinct.

Record the chosen locations, field owners, write method, sync policy, and cleanup
responsibilities in local instructions. Knowledge-store setup is optional; reuse
its existing access and capture policy.

## 3. Create One Recovery Path

Preserve an existing layout. A new local environment can start with:

```text
<context>/
├── AGENTS.md
├── index.md
└── tasks/<task>/index.md
```

Create only the entries needed now. Add `projects/<project>/index.md` when project
navigation becomes useful. A task may link to several projects while retaining
one stable recovery entry. Derive reverse navigation from links where practical.

A minimal task entry can use existing tracker fields or this shape:

```markdown
# Task name

Goal and acceptance:
Current owner and session locator:
Current understanding, open questions, and next action:
Code locations and relevant versions:
Sources and reading scope, revision, or position:
Verification results, evidence locations, and unverified paths:
```

Keep the entry current; split research, decisions, or verification detail when it
obscures recovery. Preserve meaningful source locations instead of copying entire
chats or logs into the daily reading path.

For migration, work within each owner's scope. Extract current conclusions,
update active links, and verify the destination and required sync before clearing
the old location. Protect unique, unidentified, or actively written material;
new cache rules do not retroactively make it disposable. Historical evidence
retains its original identity.

## 4. Connect the Agent Entry Points

Integrate short rules into the instructions each agent tool actually loads,
preserving existing content and scope. Keep shared details in one maintained
location. Adapt this fragment with real paths and remove unused parts:

```markdown
## Work Context

- Find ongoing work in <context>/index.md; check the goal, owner, and latest
  recovery point before creating another task.
- Save durable conclusions in the task record. Use <code-workspace> for code
  and <temporary> for disposable outputs.
- Follow <context>/AGENTS.md for writing, validation, and sync. Refresh sources
  from their recorded reading positions before resuming work.
```

Inline the key behavior at the relevant entry point; link conditional details.
Keep organization-specific paths and authorizations in their proper local scope.
Verify the deployed instructions and links, rather than assuming a file is loaded
because it exists. The environment should remain usable if the skill is removed.

If a source/worktree layout is already configured, reference its actual paths.
For a requested worktree setup, consult `git-task-workspace` when available in the
current skill catalog. Without it, retain the existing code workflow. Installation
and environment configuration are separate facts; avoid installation-directory
guesses and circular skill loading.

## 5. Enable the Required Write Model

Reuse existing tools and validators. A new single-writer environment needs a
clear writer and save policy, not a new locking framework.

If concurrent writers are required now, choose a mechanism appropriate to the
store before claiming the environment supports them. For a shared checkout,
version preconditions can reject stale writes, with a short lock covering check
and replacement. Coordinate the shared Git index and commit operations as well,
preserving other writers' drafts and staging.

A local file lock covers cooperating writers on that filesystem, not separate
machines. Across devices, use the store's concurrency mechanism or a designated
writer; integrate new remote revisions before retrying rejected Git syncs.
Version checks do not provide semantic deduplication, transfer ownership, or wake
another agent.

Add artifact admission checks or hooks only when needed, reusing existing ones.
Verify actual installation with representative allowed and rejected content.
Ignore rules control tracking; persistence and cleanup still need their own owners.

## 6. Verify from the Consumer

Use a real task within its authorization, or an isolated representative example:

1. Enter through a normal agent entry point and locate the task, owner, sources,
   and next action.
2. Resume after a source update and check that its correction reaches the current
   task record, including the new reading position.
3. Follow the configured save, validation, and sync path; inspect the destination
   content. Verify that code versions and recovery records agree.
4. If concurrency is claimed, demonstrate stale-write rejection and preservation
   of valid updates and unrelated staging. Otherwise, record the single-writer limit.

Report the deployed entry points, actual results, and unverified agent tools,
devices, or conflict paths. Timers, dashboards, and extra infrastructure are
separate additions driven by a demonstrated need.
