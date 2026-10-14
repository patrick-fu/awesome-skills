# Change explanations, notes and replies

**Scope.** Identify the artifact version and delivery being described. Ground
an existing PR/MR in its diff at the described revision and relevant execution
path; ground a reply in the issue, diagnosis, actions, and observations. Include
uncommitted work when it belongs to the requested delivery.

**Reader.** Choose information for the destination:

- **PR/MR explanation or body:** problem, changed behavior, necessary mechanism,
  review focus, and verification.
- **PR/MR title:** a standalone description of this delivery, at the requested
  length; a title-only request needs only the title.
- **Issue, incident, or CI reply:** current status, cause and basis, actions,
  and verification. Usually no title.
- **QA handoff:** delivered behavior, usage conditions, cases to try, coverage,
  limits, and the next owner's action.

Use these as writing decisions, fitting the requested length and template.
For an existing draft, edit the requested scope and preserve the rest.

**Evidence.** Separate changed, deployed, and verified states. Report results
from matching records, including partial passes, failures, and unexecuted checks;
keep planned checks identifiable as plans. Use the actual command or steps and
a reviewable record where useful; link long logs.

For regression or improvement claims, show comparable before/after evidence
from the described revisions and conditions. For visible changes, prefer
matching screenshots when available; for logic changes, use actual test runs
or execution output. Keep test names and observed results distinct from
illustrative pseudocode. When the baseline is unavailable, say so: an after-only
pass establishes that check's outcome, not a measured improvement. Confounded
groups establish a difference, not its cause. When outcomes are unmeasured,
explain the supported mechanism and conditions, with the outcome still unknown.

**Focus.** Keep history only when it explains a consequential choice. Include
concrete compatibility, migration, rollback, or ownership constraints when they
affect the reader. A broad change needs a reading entry point.

## PR/MR explanation or body

Open with the concrete problem and resulting behavior. Default to
**Change illustration → Verification evidence → Merge impact**, scaled to the
request and destination template.
For writing, deliver usable text rather than advice about how to write it.

**Change illustration.** Read [Views](views.md) and choose the smallest useful view of the
trigger, old/new path, state, contract, or responsibility. Keep consequential
conditions beside the view. Anchor further detail in relevant files or symbols
rather than listing every changed file.

**Verification evidence.** Apply the evidence rules above, making the comparison and any
missing or unexecuted checks easy to inspect.

**Merge impact.** Describe **rollback difficulty**: whether reverting code restores behavior,
or data, migrations, or external effects require compensation or cannot be
undone. Describe **impact scope**: affected users, callers, states, and compatibility
or layout consequences supported by the change. Give concrete bounds and
unknowns rather than only a risk label. These effects do not by themselves
establish readiness to merge.

**Finish.** Deliver the requested explanation, title, body, reply, or note.
Its opening should stand alone, its evidence should support its conclusions,
and the reader should know what needs attention. Publish within the existing
task authorization.
