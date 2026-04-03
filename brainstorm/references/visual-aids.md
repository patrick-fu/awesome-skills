# Visual Aids

Use visual aids only when they make the current decision easier to understand than text alone. Treat them as a branch inside brainstorming, not as a separate delivery track.

## When Visuals Help

Visual aids are usually worth proposing when the discussion is about:
- page or screen layout
- side-by-side option comparison
- user flow or state transitions
- information architecture or navigation hierarchy
- module boundaries or system relationships
- any structure that becomes hard to hold in working memory as plain text

## When To Stay In Text

Stay in text when the main work is still:
- clarifying goals
- defining terms
- surfacing tradeoffs
- checking constraints
- deciding scope

UI-related does not automatically mean visual. If the real question is conceptual, keep talking first.

## How To Use Visuals

Start by proposing the visual branch. Once the user agrees, you can decide whether a lightweight sketch is enough or whether a temporary HTML artifact would communicate the idea more clearly.

Keep text and visuals working together. The visual should support the current decision, not replace the conversation.

Only visualize one key decision at a time. If there are multiple open questions, pick the most important one first.

After showing a visual, bring the discussion back to a choice:
- Which direction is better?
- What changed after seeing it?
- What should be locked in?
- What should be ruled out?

## Escalation Ladder

Prefer the lightest tool that makes the point clearly:

1. Plain text, bullets, or a short structured comparison
2. Tiny ASCII or pseudo-layout sketch
3. Diagram, wireframe, or structured visual artifact
4. Temporary HTML opened in a browser when the structure is too complex for terminal-only presentation

Do not jump to HTML just because it is available. Use it when complexity or readability justifies it.

Temporary HTML is still brainstorming material. Keep it low to medium fidelity. It should clarify structure, flow, comparison, or boundaries. It should not drift into polished implementation.

## Visual Styles

Two styles work well for brainstorming:

### Minimal Wireframe Style

Use this for structure-heavy questions:
- layouts
- navigation hierarchy
- modules and boundaries
- flows and transitions

Characteristics:
- black/white/gray palette
- simple boxes and labels
- obvious grouping
- no decorative styling

### Light Demo Style

Use this for comparison-heavy questions:
- option A vs option B
- different UI states
- rough interaction pacing
- low-fidelity mockups with a little visual guidance

Characteristics:
- still low fidelity
- light color to separate regions
- stronger spacing and headings
- enough contrast to guide attention quickly

## HTML Patterns

Use temporary HTML when the diagram is too complex for terminal sketching but still belongs in brainstorming.

Good HTML patterns:
- two-column comparison view
- low-fidelity page wireframe with labeled regions
- simple step flow with arrows or cards
- module map with grouped blocks
- state-switching mockup showing before/after or empty/loading/error states

Keep the code self-contained and disposable. Inline CSS is fine. Avoid dependencies and avoid polishing details that are irrelevant to the decision.

## Example: Side-By-Side Comparison

```html
<!doctype html>
<html lang="en">
<meta charset="utf-8" />
<title>Option Comparison</title>
<style>
  body { font-family: sans-serif; margin: 24px; background: #f6f7f9; color: #1f2328; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .card { background: white; border: 1px solid #d0d7de; border-radius: 12px; padding: 16px; }
  .box { border: 1px dashed #8c959f; border-radius: 8px; padding: 12px; margin-top: 12px; min-height: 180px; }
  h2 { margin: 0 0 8px; font-size: 18px; }
</style>
<div class="grid">
  <section class="card">
    <h2>Option A: Dense Dashboard</h2>
    <p>Prioritizes more information above the fold.</p>
    <div class="box">header / filters / chart grid / table</div>
  </section>
  <section class="card">
    <h2>Option B: Guided Workflow</h2>
    <p>Prioritizes focus and sequential action.</p>
    <div class="box">header / stepper / primary panel / summary rail</div>
  </section>
</div>
</html>
```

Use this when the user needs to react to two competing structures quickly.

## Example: Low-Fidelity Layout Sketch

```html
<!doctype html>
<html lang="en">
<meta charset="utf-8" />
<title>Layout Sketch</title>
<style>
  body { font-family: sans-serif; margin: 20px; }
  .frame { border: 2px solid #222; padding: 12px; max-width: 960px; }
  .row { display: grid; gap: 12px; margin-top: 12px; }
  .hero { border: 1px dashed #555; padding: 18px; min-height: 80px; }
  .cols { grid-template-columns: 2fr 1fr; }
  .panel { border: 1px dashed #555; padding: 18px; min-height: 220px; }
</style>
<div class="frame">
  <div class="hero">top summary / headline / primary action</div>
  <div class="row cols">
    <div class="panel">main workspace</div>
    <div class="panel">secondary context / notes / status</div>
  </div>
</div>
</html>
```

Use this when the key question is structural placement rather than visual styling.

## Example: Flow Or Boundary Diagram

```html
<!doctype html>
<html lang="en">
<meta charset="utf-8" />
<title>Flow Diagram</title>
<style>
  body { font-family: sans-serif; margin: 24px; background: #fbfbfc; }
  .flow { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
  .node { border: 1px solid #bfc6cf; background: white; border-radius: 10px; padding: 14px 18px; }
  .arrow { color: #6e7781; font-size: 22px; }
  .group { margin-top: 24px; border: 1px solid #d8dee4; border-radius: 12px; padding: 16px; }
</style>
<div class="flow">
  <div class="node">user input</div>
  <div class="arrow">→</div>
  <div class="node">decision layer</div>
  <div class="arrow">→</div>
  <div class="node">output state</div>
</div>
<section class="group">
  <strong>Boundary note:</strong> keep validation outside the rendering layer.
</section>
</html>
```

Use this when the debate is about sequencing, ownership, or system boundaries.

## Snippet Ideas

You do not always need a full page. Small reusable fragments are often enough:
- a three-state mockup for empty/loading/success
- a left-nav plus detail-pane shell
- a two-step wizard with progress indicator
- a stack of cards showing priority order
- a grouped module map with short annotations

If a snippet communicates the idea clearly, prefer that over a fuller demo.
