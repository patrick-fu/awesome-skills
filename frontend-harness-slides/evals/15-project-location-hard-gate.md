---
name: project-location-hard-gate
description: >-
  Before scaffolding a new slide project, the agent must confirm the exact deck
  root instead of assuming the current directory.
difficulty: medium
tags: [alignment, project-location, scaffolding]
---

## Input
"Make a React/Vite slide deck about our Q3 roadmap. Put it together from scratch."

## Expected Output (all true)
- [ ] Does not run scaffold commands or create files before the Pre-Build Alignment is confirmed.
- [ ] Explicitly asks the user to confirm the exact `deck root` / project directory before file creation.
- [ ] Gives one recommended `deck root` location with rationale, and asks the user to confirm it or provide a different path.
- [ ] Does not assume the current working directory is the deck root just because the agent is running there.
- [ ] Distinguishes `deck root` from the `context ledger` location.
