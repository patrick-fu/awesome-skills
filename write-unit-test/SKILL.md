---
name: write-unit-test
description: >-
  Use when writing, reviewing, or improving unit tests for production business
  code, including regression, async, integration-boundary, and mock-heavy cases.
---

# Write Unit Tests

Use this advisory skill for production product or business code. Prompt, skill,
and agent-behavior evaluation need different methods.

## Method

1. Read the exported surface, its callers, nearby tests, and shared test
   utilities. State one caller-visible contract and the regression risk it
   guards.
2. Write one test whose name states the expected outcome. Keep the decisive
   input visible at the call site; split distinct behaviors.
3. Assert observable effects: returned values, public state, stable error types
   or codes, persistence, emitted events, rendered UI, or a boundary call when
   that call is itself the contract.
4. Build the smallest realistic setup. Match real data and error shapes;
   isolate only the lowest true external boundary.
5. For a regression or test-first change, confirm the test is red for the
   intended reason before relying on it.
6. Run the focused test and relevant suite. Finish only when breaking the
   stated contract would fail the test while harmless internal refactoring
   would not.

## Judgment

- Prefer exact domain outcomes and meaningful fields. Use full snapshots or
  full error messages only when the entire representation is the contract.
- Use a real dependency or small fake when its behavior matters. Mocks fit
  slow, flaky, costly, or external boundaries; verify collaborator calls only
  when the call is externally meaningful.
- Wait for the condition or event that proves async completion. Use a
  controlled clock or fixed delay only when timing itself is the contract.
- Keep contract-relevant fields in test doubles; partial mock shapes can hide
  downstream assumptions.
- Let builders remove noise while exposing the value that makes the case
  meaningful.
- Treat private-state access as a coupling signal. Keep test-only affordances
  in test utilities and production APIs product-driven.
- Match the repository's existing framework, naming, placement, and helper
  conventions.
