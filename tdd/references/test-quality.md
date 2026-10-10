# Test quality and pruning

**Oracle.** Derive expected outcomes from the contract, a worked example or
independently reviewed data. A known literal such as a computed total is an
oracle; restating an internal constant or deriving expected from the same
subject is not. Relations are valid when the relation is the contract.

**Constants.** Replace internal config, table, prompt or formatting pins with
checks of the behavior that consumes them. A public wire tag or specified
default may itself be a contract. A harmless rename or equivalent expression
should preserve the tests; source-text matching usually couples them to syntax.

**Absence.** Empty results, undefined and no side effect can be correct outcomes.
Ask whether the test would detect the forbidden behavior. Add a contrasting
input only when needed to establish that the subject/path is exercised; do not
classify tests solely by matcher spelling.

**Boundaries.** Keep meaningful data and error shapes in fakes. Mock the lowest
true external boundary; verify calls, payloads or order when they are observable
requirements. Internal collaboration counts alone rarely establish behavior.
Snapshots fit contracts whose complete representation matters.

**Async.** Control relevant arrival and completion orders. Bound waits for
proving events, conditions and task completion with a useful failure; a broken
subject must fail rather than hang the suite. Control time when timing is the
contract. In cleanup, cancel and await owned tasks and release timers, listeners
and shared state, including when an assertion or awaited operation fails.

**Prune.** Remove a test when another protects the same risk without losing a
useful distinct failure signal. Keep separate cases for genuinely different
boundaries, states or mechanisms. Check the remaining suite after pruning and
report any important protection removed. Minimize redundant tests, not evidence.
