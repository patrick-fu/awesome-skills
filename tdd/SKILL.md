---
name: write-unit-test
description: "Guides the assistant when writing, reviewing, or improving unit tests for production business code. It offers weakly prescriptive best practices for behavior-focused test design, TDD as an optional workflow, mock usage, regression tests, async tests, and maintainable assertions without requiring a strict test-first process."
---

# Write Unit Test

Use this skill as a practical guide for writing useful unit tests for production business code. It is advisory, not a gate: adapt the guidance to the codebase, risk level, and user intent.

The goal of a good unit test is to make an important behavior easy to trust, easy to understand, and hard to accidentally break.

## Scope

This skill is for tests around real product or business code, including:

- new features
- bug fixes
- refactors
- validation logic
- state transitions
- parsing, formatting, serialization, or conversion
- domain rules and edge cases

It is not meant for testing skill files, prompt behavior, or agent compliance.

## Core Principles

Prefer tests that verify behavior rather than implementation details. A reader should understand what the system promises, not which private helper or internal branch currently makes it happen.

Good tests usually have these qualities:

- **Focused:** one test covers one meaningful behavior.
- **Intentional:** the test name says what behavior should hold.
- **Observable:** assertions check outputs, state changes, errors, persistence, emitted events, rendered user-visible content, or calls to true external boundaries.
- **Stable:** the test should not fail just because harmless internals were refactored.
- **Diagnostic:** when the test fails, the failure message points toward the broken behavior.
- **Realistic:** fixtures, inputs, and mocks resemble real data and real contracts.

If a test name needs "and" to explain itself, consider splitting it.

## Choose What To Test

Start from the behavior the user or caller depends on:

- What input or state matters?
- What should happen?
- What should not happen?
- What edge case previously broke or could break?
- What contract would another developer rely on?

Prioritize tests for:

- business rules
- branching logic
- error handling
- boundary conditions
- integration points hidden behind a small seam
- previously reported bugs
- code that would be expensive to debug manually

Lower-value tests often only check that a function was called, a private method exists, or a mock component rendered. These can still be useful in narrow cases, but they should not be the default shape of the test suite.

## Write The Test Around Behavior

A useful test often reads like a small specification:

```typescript
test('rejects orders below the minimum amount', () => {
  const order = createOrder({ amount: 4.99 });

  const result = validateOrder(order);

  expect(result).toEqual({
    ok: false,
    reason: 'minimum_amount',
  });
});
```

Prefer this over testing the internal path:

```typescript
test('calls checkMinimumAmount', () => {
  validateOrder(createOrder({ amount: 4.99 }));

  expect(checkMinimumAmount).toHaveBeenCalled();
});
```

The first test protects the business rule. The second test mostly protects the current implementation shape.

## Optional TDD Workflow

TDD is useful when the desired behavior is clear enough to describe before implementation, especially for business rules, bug fixes, and refactors.

When using TDD, keep the loop small:

1. **Red:** write one failing test for the next behavior.
2. **Check the failure:** confirm it fails for the expected reason, not because of a typo, bad fixture, or broken setup.
3. **Green:** write the smallest production change that makes the test pass.
4. **Refactor:** clean names, duplication, and structure while keeping tests green.
5. **Repeat:** add the next behavior or edge case only after the current one is stable.

TDD works best when the test describes the API you wish existed. If the test is painfully hard to write, treat that as design feedback: the interface may be too coupled, the dependency boundary may be unclear, or the behavior may need to be split.

If you are not using TDD, you can still borrow the best parts: write tests that fail for meaningful reasons, keep behavior slices small, and avoid writing tests that merely mirror the implementation.

## Regression Tests For Bugs

For bug fixes, a strong pattern is:

1. Reproduce the bug with the smallest meaningful test.
2. Confirm the test fails in a way that matches the reported issue.
3. Fix the production code.
4. Keep the test as a regression guard.

The test should encode why the bug mattered, not only the mechanical input that triggered it.

Weak:

```typescript
test('case 48291', () => {
  expect(parseAmount('')).toBe(0);
});
```

Better:

```typescript
test('treats an empty amount as missing instead of zero', () => {
  expect(parseAmount('')).toEqual({ ok: false, reason: 'amount_required' });
});
```

## Use Mocks Carefully

Mocks are useful for slow, flaky, expensive, or truly external dependencies. They are less useful when they replace the behavior the test is supposed to verify.

Before mocking, ask:

- What real behavior or side effect does this dependency provide?
- Does this test depend on that behavior?
- Can I mock a lower-level boundary instead of the high-level collaborator?
- Would a small fake or in-memory implementation be clearer than a mock?

Avoid tests whose main assertion is that a mock exists or was called, unless the call itself is the externally visible contract. Prefer asserting the result that the caller actually observes.

When creating mock data, make it resemble the real contract. Partial mock objects can hide assumptions and create false confidence. If downstream code expects metadata, status fields, IDs, timestamps, pagination data, or error shape, include realistic versions of those fields.

## Async And Timing Tests

Avoid fixed sleeps when the test is not actually about time. Waiting for 50 ms is usually a guess; waiting for the real condition is clearer and less flaky.

Prefer condition-based waits:

```typescript
await waitFor(() => events.some((event) => event.type === 'ORDER_SYNCED'));
expect(store.get(orderId)?.status).toBe('synced');
```

Use fixed delays only when the behavior under test is genuinely time-based, such as debounce, throttle, timeout, or retry intervals. In that case, make the reason explicit in the test name or nearby comment.

## Assertions

Make assertions specific enough to catch the bug, but not so broad that harmless changes break the test.

Prefer:

- checking the exact domain result for important decisions
- checking error type or stable error code rather than brittle full messages
- checking meaningful fields instead of full snapshots when only a few fields matter
- using table-driven tests for repeated variations of the same rule

Be cautious with:

- large snapshots that hide the important behavior
- assertions on private state
- assertions that duplicate the implementation logic
- tests with so many expectations that the first failure obscures the real issue

## Test Data

Keep test data boring unless the behavior requires complexity. Use builders or helpers when they remove noise, but avoid hiding the important input.

Good helpers make the relevant difference stand out:

```typescript
const order = createOrder({ amount: 4.99 });
```

Less helpful helpers hide the reason the test matters:

```typescript
const order = createInvalidOrderFixture();
```

Use realistic edge cases:

- empty, null, missing, and whitespace values
- minimum and maximum boundaries
- duplicate records
- unknown enum values
- timezone or locale-sensitive inputs
- permission and ownership mismatches
- stale, out-of-order, or partially failed async results

## Maintainability

Tests are part of the codebase design. Keep them readable and local to the behavior they protect.

Prefer:

- clear arrange, act, assert structure
- names that describe the expected behavior
- small fixture helpers shared only when they reduce real duplication
- test utilities instead of production methods that only exist for tests
- matching the existing test framework, naming style, and directory conventions

Avoid:

- over-abstracting one-off test setup
- adding test-only methods to production classes
- mocking everything by default
- making tests depend on run order
- silently ignoring skipped cases or swallowed errors

## Review Checklist

When writing or reviewing a unit test, use this checklist as guidance:

- Does the test protect a behavior someone depends on?
- Is the test name specific enough to explain the expected behavior?
- Would this test fail if the behavior were broken?
- Does it avoid asserting private implementation details?
- Are mocks minimal and realistic?
- Does async code wait for a real condition instead of guessing time?
- Are fixtures simple, relevant, and close to real data contracts?
- If this is a bug fix, does the test explain the regression risk?
- If the test is hard to write, is that exposing a design issue worth addressing?

Do not apply the checklist mechanically. Use it to improve judgment and make the test more valuable.
