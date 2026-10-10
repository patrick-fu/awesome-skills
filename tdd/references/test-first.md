# Test-first and regression work

**Slice.** Use an existing public boundary that exercises the mechanism. Work
one behavior at a time: one meaningful failing test, minimal authorized repair,
then green before the next behavior. Refactor while green when it serves the
requested change; rerun the affected checks.

**Red.** Run the test against the pre-fix behavior and inspect its failure.
An assertion must expose the missing or incorrect outcome. Setup, discovery,
import or compiler errors do not prove regression coverage. If it already
passes, check the route and distinguishing inputs before claiming protection.
Keep the expectation fixed through repair unless the contract changes.

**After the fix.** When practical, run the same regression test against a
pre-fix implementation in an isolated copy. A small reversible mutation can
check uncertain sensitivity; verify the mutation landed against a pristine
copy. It proves sensitivity to that change, not reproduction of the original
incident. Preserve original scenarios when a minimized case was used.

**Cost.** Prefer an existing test seam. If a reliable automated test requires
disproportionate harness changes, use the closest executable check and explain
its limits. Preserve an explicit test/TDD requirement as unmet when the chosen
check cannot satisfy it. Avoid speculative abstractions or production API
expansion solely for a test.
