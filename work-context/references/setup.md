# Setup and Migration

Deliver local rules that remain useful after this skill is removed. Reuse working
configuration and fill only the gaps. Resolve unknown durable locations, sharing
boundaries, and migration scope with the user before making dependent changes.

## 1. Discover Roles and Entry Points

Inspect known agent configuration and project directories for loaded instruction
files, task records, trackers, knowledge stores, code locations, and write/sync
rules. Check unfinished work and existing owners before changing structure.
Verify actual Git roots; a directory can belong to an unexpected ancestor repo.

Within the selected repositories and known agent entry points, inventory shared
instructions, skills, standards, and agent-facing docs. Identify each item's scope
and authoritative maintenance location, including material managed by an external
installer. Compare duplicate copies for divergent rules; resolve conflicts from
ownership and actual use rather than modification time alone.

Distinguish the session's starting directory, durable context, source repository
pool, and task workspaces. Names identify user choices, not roles: `work-context`,
`home-context`, or any other name can serve as the context root. Preserve existing
names and use resolved paths consistently in deployed instructions.

Identify the instructions each harness actually loads, including its global
entry and any `AGENTS.md` or `CLAUDE.md` adapter. A pointer to shared instructions
must say when to read them; file presence alone does not prove they are loaded.

## 2. Choose Defaults and Local Variations

Existing choices take precedence. For a new environment, recommend:

| Choice | Default recommendation | Customization |
| --- | --- | --- |
| Context | A Git-managed directory, such as `<root>/work-context/` | Any name, existing directory, documentation area, or durable service |
| Starting place | One context project or launcher shared across tasks | Each harness's supported startup mechanism; existing project entries |
| Recovery | A short index with task entries created as needed | Hierarchy, task granularity, and tracker integration |
| Business fields | Tracker remains authoritative; context holds execution recovery | Field owners and snapshot refresh rules |
| Code | Reuse existing code locations | Ordinary checkouts, task worktrees, or remote execution |
| Artifacts | Task-lifetime workspace storage; context keeps summaries and links | Allowed formats, size limits, archive destination, and retention |
| Knowledge | Optional existing Wiki, embedded or separate | Content root, schema, validation, and capture policy |
| Saving | Local history with commits at validated milestones | Existing commit cadence, branch, remote, and sync policy |
| Writers | One owner per task; coordinated saves to a shared checkout | Existing atomic update service or another proven write mechanism |

Choose permanent locations from the user's environment. Keep initial setup local
when no remote is configured. Context setup does not select a publication target.
A context repository can use its ordinary shared checkout under its chosen write
protocol; code isolation belongs to the code workflow.

A simple task may need only its existing issue. Create additional recovery records
when they hold material the issue does not. Keep projects, tasks, and execution
sessions distinct; a task spanning repositories still has one recovery entry.

## 3. Build the Recovery Path and Local Instructions

Preserve an existing structure. A minimal new layout is:

```text
<context>/
├── AGENTS.md
├── index.md
└── tasks/<task>/index.md
```

Add project navigation or detail files only when useful. A task entry should make
the goal and acceptance, owner/session locator, current understanding, next action,
code paths and revisions, source reading positions, and verification/evidence
locations easy to recover.

Merge the following fragments into existing instructions, replacing placeholders
with actual paths and chosen policies. Omit unused roles. Daily instructions must
point to local rules, not to installed skill files.

Use the material inventory during setup or migration. Deploy missing pointers and
reading conditions to authoritative material through the existing entry points.
Keep repository-specific rules in their repositories and preserve existing skill
sources and installation management.

### Global Agent Instructions

```markdown
## Shared Work Context

- Use <context> as the common starting project for work across repositories.
  From any starting directory, find existing work through <context>/index.md
  before creating a task; read <context>/AGENTS.md when recovering or saving work.
- Refresh relevant sources from their recorded revision or reading position
  before resuming work or making a consequential decision.
- Code locations: <existing-code-routing>. Read their local instructions before
  editing. Task artifacts: <artifact-routing>; save durable recovery in <context>.
```

Keep this entry thin. Configure the actual supported project or launcher for each
requested harness. An instruction file does not itself change the starting
directory or register an application project. Verify startup behavior separately
and report a remaining manual step when it cannot be configured here.

### Context Root AGENTS.md

```markdown
# Shared Work Context

- Start at index.md. Search by goal and scope before creating another task.
  Reuse one task recovery entry across repositories and preserve its owner
  unless reassigned. Projects group continuing goals; sessions identify runs.
- Before resuming or deciding, refresh relevant sources from recorded revisions
  or reading positions. Update the record's source, scope, position, and any
  corrected conclusions. Distinguish verified facts, assumptions, and unknowns.
- Keep each task entry short: goal and acceptance, owner/session, current state,
  open questions, next action, code paths and versions, and verification limits.
  Link detail and evidence. Tracker-owned fields remain authoritative at
  <tracker>; label local snapshots with their source and verification time.
- Keep code and versioned project documentation in their repositories. Use
  <code-routing> for code and <workspace-artifacts> for downloads, logs,
  screenshots, recordings, and generated output. Record evidence paths and
  versions; flag missing evidence. Task artifacts survive until task cleanup.
- Save only owned changes using <write-and-validation-protocol>. Re-read a
  conflicting update before integrating it. Coordinate shared Git index and
  commit operations through <save-owner-or-existing-mechanism>; preserve other
  writers' drafts and staging. Commit: <policy>. Sync: <policy>.
- Before a handoff, record relevant revisions, verified and unverified paths,
  outstanding waits, and resource holds. A session ending does not close the
  task or release resources. Preserve unique evidence before workspace cleanup.
- Reusable knowledge: <knowledge-root-and-read-instructions>. Follow its local
  capture authorization; task progress belongs here. Wiki writes require the
  configured capture request or authorization.
```

If a shared checkout permits concurrent agents, record how task ownership and
shared saves are coordinated. A single designated saver is sufficient when it
matches actual use. Do not claim concurrent write safety from task ownership
alone. Version preconditions and a short local lock can protect cooperating
filesystem writers; the shared Git index needs coordination too. Cross-device
writes need the store's own mechanism or a designated writer and remote revision
integration. Reuse existing tools rather than inventing a locking framework.

### Source and Workspace Connections

When those roots already exist, update their relevant routing to the chosen
context path and keep their detailed policies in their own `AGENTS.md` files.
For a requested new source/worktree layout, use `git-task-workspace` if available
in the current catalog. With only this skill installed, keep existing code
locations and their operating rules; no new source pool is required.

When only the workspace skill is installed, it can keep recovery in an issue or
existing notes location. Installing either skill later fills its own gaps and
reuses these local paths; daily instructions never depend on the other skill.

## 4. Connect an Optional Wiki

Keep task recovery and reusable knowledge distinct even when they share a Git
repository. Reuse an existing Wiki's schema and access policy. Record its content
root, actual Git root, read-first files, validator with working directory, and
write/commit/sync protocol in local instructions. Link it from context navigation
when useful. For configured knowledge, a global entry can stay this small:

```markdown
## Reusable Knowledge

- When existing knowledge is relevant to the task, read <wiki-content>/AGENTS.md
  and its knowledge index. For capture or ingest, follow its local authorization
  and save protocol; a knowledge lookup alone does not authorize a write.
```

For an embedded Wiki, keep content under a chosen subdirectory, with its own
`AGENTS.md`, schema, and content-scoped validation. Git ownership, shared-index
coordination, and synchronization belong to the parent repository. For a separate
Wiki, preserve that repository's policies and link to it.

When the user explicitly requests a new Wiki, `llm-wiki-capture` can handle
Bootstrap if present and explicitly invoked by the user, including a request
that invokes both skills together. Otherwise leave Wiki setup optional or use
an existing knowledge workflow. A missing Wiki is not a reason to create one.

## 5. Migrate and Verify the Consumer

For migration, inventory current records, owners, unfinished edits, and unique
artifacts. Transfer current conclusions and links within scope, preserve source
identity, and verify destination content and required sync before retiring the
old location. New cache rules do not retroactively make old material disposable.

For each approved material move or consolidation, record the current copies,
authoritative destination, and affected consumer entry points. Update those
pointers and verify the actual harness reads the intended rules before retiring
old copies, including any retained repository-specific rules.

Use an authorized task or isolated representative fixture. Start a fresh consumer
with only the deployed local instructions and the two environment skills absent
from its catalog:

1. Enter through a normal starting point, including an ordinary code repository,
   and locate the task, owner, sources, code paths, and next action.
2. Change a source, resume from its recorded position, and verify the correction
   and new reading position reach the task record.
3. Save through the configured protocol and inspect the destination. Check code
   revisions and evidence paths against the recovery record.
4. If workspace setup is included, add a repository during the task, retain an
   artifact across sessions, and exercise safe cleanup using local rules.
5. If concurrent writing is claimed, verify stale-write handling and preservation
   of valid updates and unrelated staging. Otherwise state the supported limit.
6. If shared material moved or was consolidated, verify the authoritative source
   and actual read path, resolution of divergent copies, and application of
   retained repository-specific rules.

Report deployed files, actual startup and consumer results, and unverified
harnesses, devices, sync, or conflict paths. Setup is complete only for the paths
actually configured and checked.
