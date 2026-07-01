# Style Index & Design DNA Methodology

This index guides the selection, customization, and evolution of slide aesthetics. It defines the core design philosophy: **Single Style System, Multi-Layout Composition**. 

Instead of repeating a rigid template, you must analyze the semantic structure of each slide's content and custom-invent a visual layout that best fits that specific message, bound together by the visual DNA of the chosen style.

## 1. The Semantic-to-Visual Mapping Protocol

When designing a slide, do not start with a template. Analyze the raw content first and map its semantic structure to a custom spatial layout:

1. **Contrast, Comparison, or Dialogue** ➔ Map to a **Split Theatre** layout (e.g., side-by-side columns, diagonal splits, or dual-avatar dialogue screens).
2. **Steps, Process, Flow, or Pipeline** ➔ Map to a **Routed Flow** layout (e.g., horizontal pipelines, subway transit maps, or progressive step-by-step tracks).
3. **Core Thesis, Golden Sentence, or Big Claim** ➔ Map to a **Hero Metaphor** layout (e.g., extreme whitespace, a single massive display font statement, or one high-fidelity central physical metaphor).
4. **Multiple Evidence, Categories, or Checklist** ➔ Map to an **Asymmetric Bento** layout (e.g., a grid of cards with varying sizes and visual weights).
5. **Trade-offs, Balance, or Interconnected Cycles** ➔ Map to a **Custom Topology** layout (e.g., a physical balance scale, a gear mesh, or a circular feedback loop).

*Encouragement*: You are expected and encouraged to invent entirely new visual metaphors and layouts not explicitly listed here, as long as they perfectly serve the semantic structure of the content.

## 2. Visual Pacing & The Breathing Rhythm

A great slide deck should "breathe" by alternating visual density and layout structures. **Prefer** maintaining a varied rhythm:

- **The Monotony Test**: **Avoid** using the exact same spatial layout (e.g., a grid of cards or a two-column split) on consecutive slides unless a uniform rhythm is intentionally desired.
- **The Density Curve**: **Consider** alternating between high-density slides (e.g., a detailed report page or bento box) and low-density slides (e.g., a sparse keynote opener or spotlight quote) to create a natural rhythm of "inhaling" (absorbing detail) and "exhaling" (focusing on the big picture).

## 3. The 24 Style Directions

The style directions are organized into three density bands. Choose a style system, then refer to its specific reference file for detailed aesthetic recipes:

| Style Band | Description | Reference File | Styles Included |
|---|---|---|---|
| **Minimal Keynote** | Sparse, high-impact, presentation-led. Best for live talks and openings. | `references/style/minimal-keynote.md` | Styles 1 - 8 |
| **Balanced Hybrid** | Supports both live presenting and later reading. Graphic and structured. | `references/style/balanced-hybrid.md` | Styles 9 - 16 |
| **Text Report** | Self-contained, evidence-rich, document-led. Best for async reviews. | `references/style/text-report.md` | Styles 17 - 24 |

## 4. Few-Shot: Template Monotony vs. Material-Driven Craft

To understand the difference between rigid template-matching and semantic-driven custom design, study this comparison:

### Raw Material
> *"We need to explain the trade-offs between using a Local SQLite database versus a Cloud PostgreSQL database for an offline-first sync engine. Local database brings zero latency and offline availability but risks data loss; cloud database brings strong consistency and cross-device sync but is highly network-dependent."*

### ❌ The Template Monotony Approach (Speculative Slop)
The Agent blindly applies a standard two-column grid template because the style guide has a "two-card grid" preset. It copies the text directly into bullet points:

```html
<div class="grid grid-cols-2 gap-6">
  <div class="p-6 bg-white border rounded-xl">
    <h3 class="font-bold">SQLite (Local)</h3>
    <ul class="list-disc pl-4 text-xs">
      <li>Zero latency</li>
      <li>Offline availability</li>
      <li>Risk of data loss</li>
    </ul>
  </div>
  <div class="p-6 bg-white border rounded-xl">
    <h3 class="font-bold">PostgreSQL (Cloud)</h3>
    <ul class="list-disc pl-4 text-xs">
      <li>Strong consistency</li>
      <li>Cross-device sync</li>
      <li>Network dependent</li>
    </ul>
  </div>
</div>
```
*Why it fails*: It looks like a generic web dashboard. It requires the audience to read dense bullets. It does not visually represent the "trade-off" or "balance" concept.

### ✅ The Material-Driven Craft Approach (Aesthetic System)
The Agent identifies the core semantic structure as a **Trade-off/Balance**. It invents a custom **Physical Balance Scale** component. It wraps this custom layout in the chosen style's tokens (e.g., Sketchboard Emoji):

- **The Layout**: A central hand-drawn balance scale (`sketch-border`).
- **The Metaphor**: The left scale pan holds a local disk emoji (💾 SQLite); the right pan holds a cloud emoji (☁️ PostgreSQL).
- **The Interaction**: Hovering over the left pan tilts the scale to the left (CSS `transform: rotate(-8deg)`) and reveals a hand-drawn sticky note highlighting "Zero Latency". Hovering over the right tilts it to the right, highlighting "Strong Consistency".
- **The Result**: The audience instantly grasps the "balance" concept through a tactile, interactive physical metaphor. The design is unique to this slide's content but stays perfectly coherent with the overall style system.

## 5. Design DNA Contract

When a visual system is established, record its design DNA in the project's **Context Ledger** (e.g., `docs/context.md`) under a dedicated `# Design DNA` section. This ensures that subsequent edits or new slides created by other agents maintain perfect visual coherence while preserving layout diversity.

Record:
- **Chosen Style System**: The name and number of the style.
- **Visual Guardrails**: The color palette intent, typographic hierarchy, and border/shadow rules.
- **Custom-Invented Metaphors**: A list of custom components created (e.g., "Slide 3: Balance Scale for Trade-offs").
- **Pacing Log**: The density sequence of the slides (e.g., `S1:Low | S2:Medium | S3:Low | S4:High`).
