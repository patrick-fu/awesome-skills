# Views

**Select.** Choose the smallest view that exposes the relationship or change.
Keep only calls, files, properties, states, and boundaries needed for the current
question. Place each visual beside the brief text it supports; use several only
when they answer different parts of the question.

| Question | View |
| --- | --- |
| Logic, algorithm, or state | Pseudocode or flowchart |
| Runtime call path | Call tree preserving order and branches |
| UI structure and state ownership | Component tree preserving relevant state and module boundaries |
| File responsibility or refactor scope | Shallow file tree |
| Ownership or dependencies | Responsibility tree or architecture diagram |
| Messages and concurrent work | Sequence diagram |
| Contract or local structural change | Before/after or structural diff |
| Options and tradeoffs | Comparison table |
| Queue buildup/backpressure, in-place state evolution, or topology rewrite (e.g. `rebase`) | Interactive in-place motion view (prefer over static 1-2-3 horizontal boxes) |
| Cross-boundary flow, numeric before/after deltas, or concurrent/async data streams | Interactive in-place motion view showing live state mutation |
| Changing a variable or stepping through work | Interactive view |

**Relations.** Give every edge a supported meaning: message, dependency, or
order. Use literal component names and real actions on nodes and edges rather
than analogies or metaphorical labels. Preserve conditions and independent
lifecycles; make concurrency explicit. A retry joins existing work where the
implementation supports it; cancellation has its own scope and race. Keep
distinct clocks and states separate. Mark inferred or unknown relationships
accordingly.

**Check.** Inspect relationships, ordering, endpoints, and qualifications.
Rendering checks syntax, not behavior. Use a known available renderer; when
unavailable, deliver the view after a semantic check and identify the rendering
limit. Further environment search is unnecessary for a text diagram.

## Shape

Show the behavioral delta with enough unchanged context to preserve ownership
and order. Match the structural diff to calls, components, files, contracts,
or states; label additions and removals. Use the complete target when most is
new, omitted context would hide ownership or order, or the user needs a copyable
block. These fictional sketches illustrate shape, not test evidence.

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

For a new UI, a component tree can expose state ownership:

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

This establishes a response shape; latency, completion, and compatibility need
their own evidence. Add real file or symbol anchors when verified and useful.

## Async

Use `par` for concurrent work, or show only observed interactions when internal
ownership is unknown. Label loop exits and independent user actions. Events can
cross branches; preserve their real cause and destination rather than forcing
them into synchronous pairs. A retry returning an existing handle need not
restart its worker. A client deadline's effect comes from the actual contract.

## Interaction

Use inline views for compact explanations. Create a focused HTML view or use
an available visualization tool when layout or interaction earns it. Keep labels
and the state model grounded; support the intended screen sizes and present it
through an available preview. Reuse product styling when relevant.

**Act on real objects.** Attach motion directly to the actual concept entities
(request packets, commit nodes, lock tokens, config lines, message bubbles)
rather than shuffling generic cards. Keep literal names and actions; omit
anthropomorphic mascots unless explicitly asked.

**Choose in-place motion primitives.** Evolve existing anchors instead of
printing static 1-2-3 horizontal boxes:

- *Inline elastic slot*: push neighboring tokens or words apart to insert a live
  constraint, flag, or state badge inside the active line.
- *Horizontal `clip-path` wipe*: swap labels or values in place without popping
  replacement cards.
- *Subtle blur bridge*: transition between adjacent states with a light
  `blur(3–4px) → 0` bridge paired with opacity so the eye tracks continuity.
- *Origin-aware `transform-origin`*: anchor growth or rotation to the real
  trigger edge or attachment point.
- *Never pop from `scale(0)`*: enter elements from `scale(0.94–0.96)` with small
  displacement, and use asymmetric enter/exit timing (exits slightly faster than
  entrances so leaving state clears cleanly).
- *Rolling digits*: animate only changed numeric positions in tabular monospace
  when showing before/after deltas so unchanged digits stay steady.
- *Animated beam*: send a directional pulse along an actual connector path to
  expose active flow, routing, or backpressure.
- *Dynamic height morph and stacked depth*: adapt container height smoothly and
  keep prior items visible in a shallow depth stack so history remains readable
  for low-cognitive-load re-entry.

**Determinism and control guardrails.** Drive continuous motion from a stateless
`seek(t)` function (no wall-clock drift or randomness) so forward and reverse
scrubbing restores the exact state. Provide play/pause, step controls or a
scrub bar, a slow-motion option (~`0.35–0.4×`), and named return anchors.
Include a textual equivalent whenever understanding depends on timing, and honor
`prefers-reduced-motion` with a complete static fallback frame.
