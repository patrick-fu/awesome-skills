---
name: registry-semantic-consistency
description: >-
  The generated registry, manifest, or draft can stably enumerate scene and
  frame semantics.
difficulty: low
tags: [structure, consistency]
---

## Input
"Generate a 10-slide structure about AI Agent trends over the next five years."

## Expected Output (all true)
- [ ] Provides a registry, manifest, route table, draft, or equivalent structure that enumerates 10 scene/frame entries.
- [ ] Each entry has a stable id that does not depend on visible titles, filenames, or array position.
- [ ] Each entry has a title or human label, without address ambiguity when titles repeat.
- [ ] Each entry includes beats, beat_count, frame states, or equivalent frame-count information.
- [ ] Ordering is represented through array order or an explicit order field, without requiring visible-text scraping.
- [ ] The opening and closing have clear opening, closing, or takeaway semantics without forcing a Q&A slide.
