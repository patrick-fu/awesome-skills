# Change notes and replies

**Scope.** Identify the artifact version and delivery being described. Ground
an existing PR in its diff and relevant context; ground a reply in the issue,
diagnosis, actions, and observations. Include uncommitted work when it belongs
to the requested delivery.

**Reader.** Choose information for the destination:

- **PR/MR:** problem, changed behavior, necessary implementation, review focus,
  and verification. The title must describe this delivery on its own.
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

Use comparable observations for performance or improvement claims. Confounded
groups establish a difference, not its cause. When outcomes are unmeasured,
explain the supported mechanism and conditions, with the outcome still unknown.

**Focus.** Keep history only when it explains a consequential choice. Include
concrete compatibility, migration, rollback, or ownership constraints when they
affect the reader. A broad PR needs a reading entry point. Add a view only when
it resolves a reader's difficulty; then read [Views](views.md).

**Finish.** Deliver the requested title, body, reply, or note. Its opening should
stand alone, its evidence should support its conclusions, and the reader should
know what needs attention. Publish within the existing task authorization.
