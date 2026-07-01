---
name: pptx-import-guidance
description: >-
  When the user provides a PPTX or old deck, treat it as a content source to
  extract and rebuild instead of binding the workflow to one extraction script.
difficulty: low
tags: [import, guidance]
---

## Input
"I have a source.pptx with more than 20 slides. Can you convert the content into your slide project format?"

## Expected Output (all true)
- [ ] Recommends using the currently available PPTX or old-deck extraction approach, with a low-fidelity fallback if needed.
- [ ] Identifies target extraction fields: slide order, titles, text blocks, images, and optional speaker notes.
- [ ] Explains that the imported material should be rebuilt as a fixed-stage deck instead of blindly preserving original absolute positions.
- [ ] Explains that images, fonts, speaker notes, and similar material should go into project assets, planning, or presenter material, not directly onto the slide surface by default.
- [ ] Recommends forming a narrative or registry draft before writing scene code.
