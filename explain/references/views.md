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
| Changing a variable or stepping through work | Interactive view |

**Relations.** Give every edge a supported meaning: message, dependency, or
order. Preserve conditions and independent lifecycles; make concurrency
explicit. A retry joins existing work where the implementation supports it;
cancellation has its own scope and race. Keep distinct clocks and states
separate. Mark inferred or unknown relationships accordingly.

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
through an available preview.

For motion, provide pause or step controls and a labeled return point. Include
a textual equivalent when understanding otherwise depends on timing. Reuse
product styling when relevant.
