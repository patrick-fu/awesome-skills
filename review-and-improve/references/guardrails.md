# Structural Enforcement

For each retained structural finding, try the highest level that works within
scope. A single incident can justify repair; two observed occurrences are needed
to call it a repeated mistake class.

1. **Architecture:** one owner and supported path; remove duplicate truth,
   exposed internals and legacy examples agents would copy. Explain why this
   level does or does not fit before moving down.
2. **Types:** make invalid states or calls unrepresentable.
3. **Lint / CI:** if bad code still compiles, use a deterministic check whose
   error names the fix. For existing violations, ratchet against new additions.
4. **Behavior:** make the relevant regression executable. A test that does not
   observe the subject's behavior cannot prove protection; repair its assertion
   or remove it. Verify failures expose the intended defect.
5. **Guidance:** reserve rules and documentation for judgement calls that the
   preceding mechanisms cannot reliably enforce.

Inspect the repository's canonical check command and wiring first. Treat absent
hooks and CI as guardrail candidates; distinguish a candidate from an authorized
change. Prioritize the most frequent classes. Keep each implementation scoped.

## Prove

For proposals, specify this proof; execute it when implementing an authorized
repair. Replay the real incident through the repaired contributor path and
confirm the corrected outcome against the original contract: reject previously
missed violations, and accept legitimate inputs previously blocked in error.
Preserve the checked target and context; success on a narrower scope does not
repair the original failure. Distinguish new control cases from historical
incidents.
Also exercise legitimate cases to detect false positives. Run the canonical
command locally and in CI when access permits; report an unexecuted CI path as
pending. Verify the guard is wired into the contributor path, not just runnable.

Keep an enforcement table in the applicable agent instructions: rule and owning
mechanism. A correction to an already documented but unenforced rule is a repeat
signal; implement its control in the authorized change. Remove obsolete prose
once the mechanism makes the mistake impossible. Exceptions belong at the
offending line with reason, expiry and explicit human approval.

When commits are requested, make one commit per repaired class, containing its
control and proof. Preserve unrelated changes. Report the chosen level and why
a higher level did not work.
