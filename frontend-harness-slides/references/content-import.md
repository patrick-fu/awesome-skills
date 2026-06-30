# Content Import SOP

Use this when the user provides an existing document, old deck, outline, or
screenshots and wants a harness-backed HTML slide project.

Import is not layout preservation. Treat the source as content and intent, then
rebuild the deck as scenes inside the fixed 1920x1080 stage.

## Normalize The Source

| Source | Practical path | Notes |
|---|---|---|
| PPTX / PowerPoint | Extract text, images, and slide order with an available PPTX parser or manual unzip workflow. | Rebuild layout; do not copy absolute PPT coordinates blindly. |
| Keynote | Export to PPTX first. | Smart builds often flatten; check notes or source text. |
| Google Slides | Download as PPTX or copy the outline into Markdown. | Verify image quality after export. |
| Markdown / Notion / docs | Split by headings and narrative sections. | Often better than forcing a fake PPTX conversion. |
| Screenshots / product captures | Put source files under `public/` or `src/assets/` and design scenes around them. | Screenshots should drive the outline, not be pasted after the fact. |

## If You Need PPTX Extraction

Use any local PPTX extraction tool that can produce:

- slide number
- title or primary heading
- text blocks or bullets
- image assets
- optional speaker notes or presenter script text

If no tool is available, unzip the PPTX and inspect `ppt/slides/slideN.xml` plus
`ppt/media/`. Keep this as an extraction step only; final layout should be
authored in React scenes.

Example target structure:

```text
tmp-extracted/
├── slides/
│   ├── 001.json
│   └── 002.json
└── images/
    ├── 001-hero.png
    └── 002-chart.png
```

## Map Source Content To The Starter

| Source field | Starter destination | Rule |
|---|---|---|
| Slide order | `SLIDE_REGISTRY` array order | Preserve order first, then intentionally trim or reorder after reviewing the story. |
| Title | `id` + `title` | `id` must be stable kebab-case ASCII; display `title` can be natural language. |
| Text blocks | Scene component content | Split dense content into multiple scenes or meaningful beats. |
| Images | `public/` for static paths or `src/assets/` for imported assets | Optimize large images before committing. |
| Speaker notes | Separate planning/script material | The current starter does not render a presenter notes view by default. |

## Import Checklist

1. Registry ids are unique, stable, and kebab-case.
2. Every registry entry points to a real scene component.
3. The source outline has been summarized back to the user if intent is unclear.
4. Dense slides are split instead of shrinking text into unreadability.
5. Images are named by content, not by raw export names.
6. The rebuilt deck passes `npm run build` and `npm test`.
