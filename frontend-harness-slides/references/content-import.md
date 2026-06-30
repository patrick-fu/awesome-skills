# Content Import

Use this when the user provides an existing document, old deck, outline, or
screenshots and wants a harness-backed HTML slide deck.

Import is not layout preservation. Treat the source as content and intent, then
rebuild the deck into stable scenes inside the fixed stage.

## Normalize The Source

| Source | Practical path | Notes |
|---|---|---|
| PPTX / PowerPoint | Extract text, images, speaker notes, and slide order with an available parser or manual unzip workflow. | Rebuild layout; do not copy absolute PPT coordinates blindly. |
| Keynote | Export to PPTX first. | Smart builds often flatten; check notes or source text. |
| Google Slides | Download as PPTX or copy the outline into Markdown. | Verify image quality after export. |
| Markdown / Notion / docs | Split by headings, narrative sections, and evidence blocks. | Often better than forcing a fake PPTX conversion. |
| Screenshots / product captures | Keep originals in a project asset folder and design scenes around them. | Screenshots should drive the outline, not be pasted after the fact. |

## Extraction Target

Any extraction path is fine if it gives the agent:

- slide number
- title or primary heading
- text blocks or bullets
- image assets
- optional speaker notes or presenter script text

If no tool is available, unzip the PPTX and inspect `ppt/slides/slideN.xml` plus
`ppt/media/`. Keep this as extraction only; the final HTML deck should be rebuilt
around the agreed narrative and harness contracts.

## Map Content To The Deck

| Source field | Deck destination | Rule |
|---|---|---|
| Slide order | Registry or manifest order | Preserve order first, then intentionally trim or reorder after reviewing the story. |
| Title | Stable id plus display title | The id should survive wording changes. |
| Text blocks | Scene content | Split dense content into multiple scenes or meaningful beats. |
| Images | Project asset folder | Optimize large images before committing or deploying. |
| Speaker notes | Planning/script material | Render notes only if the deck project explicitly supports presenter mode. |

## Import Checklist

1. Registry ids are unique and stable.
2. Every registry entry points to a real renderable frame.
3. The source outline has been summarized back to the user if intent is unclear.
4. Dense slides are split instead of shrinking text into unreadability.
5. Images are named by content, not raw export names.
6. The rebuilt deck passes the relevant structural and visual checks before
   delivery.
