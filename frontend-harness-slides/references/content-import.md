# Content Import SOP — PPTX / Keynote / Notion → Harness Deck

## Source → Interim format

### Step 1: Normalize source to PPTX
| Source format | How to get PPTX | Notes |
|---|---|---|
| Keynote (.key) | File → Export To → PowerPoint (.pptx) | ⚠️ Keynote SmartBuilds flatten to static shapes; extract text from Notes pane instead |
| WPS (.wpp) | 另存为 → PowerPoint 演示文稿 (*.pptx) | Same as PPTX downstream |
| Lark / 飞书 幻灯片 | 分享 → 导出 → PPTX | 飞书 shapes may lose grouping; re-check speaker notes |
| Google Slides | File → Download → Microsoft PowerPoint (.pptx) | Preserves speaker notes 1:1 |
| Notion / Markdown | Use a md → pptx converter OR just copy sections | Skip extract-pptx, hand-write registry directly |

### Step 2: Extract text + images with extract-pptx.py
```bash
# Uses frontend-slides skill's tool (works on ANY PPTX, not just frontend-slides output)
python3 ~/.agents/skills/frontend-slides/scripts/extract-pptx.py \
  --input ./source-deck.pptx \
  --output ./tmp-extracted \
  --images ./assets/images/

# Output structure:
#   tmp-extracted/slides/001.json    { title, bullets[], notes, shapes[] }
#   assets/images/001_*              PNG assets from the slide
```

**找不到 extract-pptx.py？** 如果你的 `frontend-slides` 安装路径不同，用：
```bash
find ~/.agents/skills/frontend-slides -name "*.py"
# Fallback: unzip the PPTX manually, parse ppt/slides/slideN.xml
```

### Step 3: Map extraction → SlideEntry shape
| PPTX extraction field | → Harness SlideEntry field | Transform |
|---|---|---|
| `title` | `id` (slugify) + `title` (display) | `id = toKebab(title.toLowerCase()); title = title.trim()` |
| `bullets` / `shapes[].text` | Scene component content → or split across `beats` | >3 bullets → split into N beats with `data-beat-only="beat-k"` |
| `notes` (speaker notes pane) | `notes` | 1:1, markdown allowed (Presenter mode renders plain) |
| Image shapes in `assets/images/` | `src/assets/<scene-id>/{name}.webp` | Convert to WebP 82% quality, max 1600px wide |
| Slide number (PPTX) | Position in `registry[]` array | Preserve ORDER; add/remove later if narrative needs trimming |

### Step 4: Validation (non-negotiable before moving to Build)
1. ✅ `registry.length` equals PPTX slide count (± your intentional cuts)
2. ✅ Every `id` is unique kebab-case (no spaces, no Chinese chars)
3. ✅ Every scene component returns exactly ONE root element (Fragment OK)
4. ✅ Image assets moved from `tmp-extracted/**_images/` → `src/assets/<scene-id>/` and imported with typed paths
5. ✅ Speaker notes preserved (cross-check 3 random slides against PPTX)
6. ✅ No slide has >3 bullets in a single beat (SKILL.md §VII Anti-pattern #15; hard absolute limit 6 — if >3 and you confirm reading-first mode is intended, at minimum split beats with `data-beat-only` and get reviewer sign-off)
