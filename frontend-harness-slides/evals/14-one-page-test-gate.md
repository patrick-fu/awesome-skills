---
name: one-page-test-gate
description: >-
  When an agent creates a very small slide deck project, it must still create
  runnable, meaningful tests instead of skipping verification because the deck
  is small.
difficulty: medium
tags: [testing, tdd, verification]
---

## Input
"Make a tiny one-page interactive HTML slide demo in React/Vite. It only has one slide, so keep it simple."

## Expected Output (all true)
- [ ] Creates or proposes a runnable test setup as part of the deck project.
- [ ] Includes at least one meaningful test tied to slide behavior, such as route rendering, visible stage content, navigation/interaction, overflow, or console-error checks.
- [ ] Does not say tests are unnecessary because the deck has only one page, one route, or a few source files.
- [ ] Keeps the test scope small and high-value instead of adding broad, low-value cases.
