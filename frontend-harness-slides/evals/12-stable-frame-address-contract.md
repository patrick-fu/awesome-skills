---
name: stable-frame-address-contract
description: >-
  Harness-backed decks should make each meaningful scene/beat directly
  addressable and enumerable without binding to one URL format.
difficulty: high
tags: [harness, addressability, registry]
---

## Input
"This deck will go through repeated animation and copy edits. Please build an HTML slides harness that supports regression checks."

## Expected Output (all true)
- [ ] Each scene has a stable id, and the id does not depend on visible titles, filenames, or array position.
- [ ] Each meaningful beat, frame state, or equivalent state can be opened directly.
- [ ] Direct addressing may use query, hash, route, state file, or a project-equivalent approach; it does not force `?scene=`.
- [ ] A registry, manifest, route table, or equivalent source of truth enumerates scene order and beat/frame count.
- [ ] Test or screenshot tooling does not need to scrape visible text to infer the current frame.
- [ ] Frozen/snapshot/test mode can render the requested frame's settled state.
