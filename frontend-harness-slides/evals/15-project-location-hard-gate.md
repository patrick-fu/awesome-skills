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
- [ ] Gives a recommended location with rationale and 3-5 credible alternatives, such as a new clean subdirectory, an existing deck project, an independent repo, a user-specified path, or a temporary exploration path.
- [ ] Does not assume the current working directory is the deck root just because the agent is running there.
- [ ] Distinguishes `deck root` from the `context ledger` location.
