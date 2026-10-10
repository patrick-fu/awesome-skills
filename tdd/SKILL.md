---
name: testing
description: >-
  Write, improve, or prune automated tests for production software; run
  test-first development when requested. Not for skill or prompt evaluations.
---

# Testing

Protect meaningful behavior with the smallest useful test set. Match the
request: ordinary testing, regression work, or a requested test-first loop.
A tests-only request keeps production changes outside its scope.

## Contract

Read the relevant public surface, callers, existing tests and repository
conventions. Identify the caller-visible contract, important failure risk and
cheapest boundary that exercises it. Reuse accepted decisions; resolve only
real contract ambiguity. Keep production APIs product-driven.

## Minimum

Reuse checks that already protect the change. Add tests for distinct uncovered
risks, not edited lines. Behavior-preserving refactors may need only existing
checks. Prefer one readable test for one outcome, with the relevant assertions;
split when independent behaviors or setups would obscure failures. Minimize
redundancy without deleting distinct protection.

## Mode

- **Tests:** exercise the subject with concrete inputs and independent expected
  outcomes. Choose the smallest realistic setup and true external boundary.
- **TDD / regression:** read [Test-first](references/test-first.md) for the
  red → green loop, failing-before evidence and after-fix sensitivity checks.
- **Quality:** also read [Test quality](references/test-quality.md) before
  writing async tests or boundary doubles, and when pruning tests or evaluating
  suspect assertions, constants or overlapping coverage.

## Proof

A useful test distinguishes a relevant defect while accepting equivalent
implementations. Observe returned values, public state, persistence, events or
boundary interactions when those interactions are the contract. Use real
mechanisms or small faithful fakes where their behavior matters.

**Tautological tests considered harmful.** A result compared with itself has
no independent oracle; obtain expectations from the contract or a worked
example. Copying an algorithm can share its bug but is not necessarily a
strictly tautological assertion.

Internal constant, prompt-string or source-shape pins usually protect no
behavior; exercise the mechanism instead. Independently specified public
values and absence of forbidden effects can be real contracts.

## Evidence

Run focused checks and the relevant suite. Report actual commands, results and
coverage gaps. Distinguish reproduction of the original bug, sensitivity to a
mutation, and passing-after evidence. Missing required automated tests or
execution remain pending; an alternative check does not waive the request.
