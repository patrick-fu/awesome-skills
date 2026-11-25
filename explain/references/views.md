# Views

Choose the lowest visual tier that makes the mechanism, relationship, or change
unmistakable. Keep only the calls, files, properties, states, and boundaries
required for the current question, and place each visual beside the brief text
it supports.

## Three-Tier Decision Tree

1. **Tier 1 — Plain prose**: use prose alone when a single sentence or short
   list carries the full answer and a visual adds no structural clarity.
2. **Tier 2 — Static structural view**: step up here whenever explaining order,
   branches, ownership, contracts, tradeoffs, or structural diffs.
3. **Tier 3 — In-place interactive evolution view**: step up here whenever
   understanding depends on how live state mutates over time (queue buildup,
   backpressure, topology rewrites such as `rebase`, cross-boundary/async data
   streams, numeric before/after deltas, or stepping through a variable). Prefer
   evolving real objects in place over printing static 1-2-3 horizontal boxes.

| Tier | Question | View |
| --- | --- | --- |
| 2 · Static | Logic, algorithm, or state machine | Pseudocode or flowchart |
| 2 · Static | Runtime call path | Call tree preserving order and branches |
| 2 · Static | UI structure and state ownership | Component tree preserving relevant state and module boundaries |
| 2 · Static | File responsibility or refactor scope | Shallow file tree |
| 2 · Static | Ownership or dependencies | Responsibility tree or architecture diagram |
| 2 · Static | Messages and concurrent work | Sequence diagram |
| 2 · Static | Contract or local structural change | Before/after or structural diff |
| 2 · Static | Options and tradeoffs | Comparison table |
| 3 · Interactive | Queue buildup/backpressure, in-place state evolution, or topology rewrite (e.g. `rebase`) | Interactive in-place motion view |
| 3 · Interactive | Cross-boundary flow, numeric before/after deltas, or concurrent/async streams | Interactive in-place motion view showing live state mutation |
| 3 · Interactive | Changing a variable or stepping through execution | Interactive stepped view |

Use multiple views only when they answer distinct parts of the question.

## Shared Grounding & Semantics (All Tiers)

- **Literal relations**: give every edge a supported meaning (message,
  dependency, or order). Use literal component names and real actions on nodes
  and edges rather than analogies, metaphors, or anthropomorphic mascots unless
  explicitly asked.
- **Conditions and lifecycles**: preserve consequential conditions and
  independent lifecycles; make concurrency explicit. A retry joins existing
  work where the implementation supports it; cancellation has its own scope and
  race. Keep distinct clocks and states separate, and mark inferred or unknown
  relationships explicitly.
- **Semantic check before delivery**: inspect relationships, ordering,
  endpoints, and qualifications. Rendering checks syntax, not behavior. Use a
  known available renderer; when unavailable, deliver the view after a semantic
  check and state the rendering limit. Do not search the environment further
  just for a text diagram.

## Tier 2 Details: Shape & Async

### Structural Diff & Shape

Show the behavioral delta with enough unchanged context to preserve ownership
and order. Match the diff to calls, components, files, contracts, or states and
label additions and removals. Show the complete target when most is new, omitted
context would hide ownership or order, or the user needs a copyable block.
These fictional sketches illustrate shape, not test evidence:

```diff
 on save
+  if saving: return
+  mark saving
-  await save record
+  try: await save record
+  finally: clear saving flag
```

```diff
 Editor
-  validate and persist the record
+  call SaveService
 SaveService
+  validate and persist the record
```

For a new UI, a component tree exposes state ownership cleanly:

```text
Review panel (owns selected item)
  Item selector
  Review status
  Confirm action (enabled only when review is complete)
```

For a contract change, show what callers observe and when they must adapt:

```diff
- { "result": "<value>" }
+ { "operationId": "<id>", "status": "accepted" }
```

This establishes response shape; latency, completion, and compatibility still
need their own evidence. Add real file or symbol anchors when verified and
useful.

### Concurrent & Async Flows

Use `par` for concurrent work, or show only observed interactions when internal
ownership is unknown. Label loop exits and independent user actions. Events can
cross branches; preserve their real cause and destination rather than forcing
them into synchronous pairs. A retry returning an existing handle need not
restart its worker, and a client deadline's effect comes from the actual
contract.

## Tier 3 Details: In-Place Interactive Evolution

Use inline views for compact explanations, or create a focused HTML view / use
an available visualization tool when layout or interaction earns it. Keep
labels and the state model grounded, support the intended screen sizes, present
through an available preview, and reuse product styling when relevant.

- **Act on real literal objects**: attach motion directly to the actual concept
  entities (request packets, commit nodes, lock tokens, config lines, message
  bubbles) rather than shuffling generic cards. Keep literal names and actions;
  omit anthropomorphic mascots unless explicitly asked.
- **In-place motion primitives** (mutate existing anchors instead of dumping
  static 1-2-3 horizontal boxes):
  - *Inline elastic slot*: push neighboring tokens or words apart to insert a
    live constraint, flag, or state badge inside the active line.
  - *Horizontal `clip-path` wipe*: swap labels or values in place without
    popping replacement cards.
  - *Subtle blur bridge*: transition adjacent states with a light
    `blur(3–4px) → 0` bridge paired with opacity so the eye tracks continuity.
  - *Origin-aware `transform-origin`*: anchor growth or rotation to the real
    trigger edge or attachment point.
  - *Natural scale & asymmetric timing*: enter from `scale(0.94–0.96)` (never
    pop from `scale(0)`) with small displacement, and let exits clear slightly
    faster than entrances.
  - *Rolling digits*: animate only changed numeric positions in tabular
    monospace for before/after deltas so unchanged digits stay steady.
  - *Animated beam*: send a directional pulse along an actual connector path to
    expose active flow, routing, or backpressure.
  - *Dynamic height morph & stacked depth*: adapt container height smoothly and
    keep prior items visible in a shallow depth stack so history remains
    readable for low-cognitive-load re-entry.
- **Determinism & accessibility guardrails**: drive continuous motion from a
  stateless `seek(t)` function (no wall-clock drift or randomness) so forward
  and reverse scrubbing restores the exact state. Provide play/pause, step
  controls or a scrub bar, slow-motion (`~0.35–0.4×`), and named return
  anchors. Include a textual equivalent whenever understanding depends on
  timing, and honor `prefers-reduced-motion` with a complete static fallback
  frame.
