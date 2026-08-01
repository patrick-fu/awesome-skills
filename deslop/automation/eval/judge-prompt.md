# Blind judge prompt

You are grading prose-editing outputs. Do not infer which skill produced them.

Read the source cases, `evals/benchmark-map.json`, `evals/rubric.md`, and the raw
candidate outputs. For each output:

1. Check every listed assertion against the source and output.
2. Record each L1 fidelity failure with exact evidence.
3. Decide whether a no-op or protected structure was wrongly changed.
4. Rate editorial quality by scene, without using an AI detector or a numeric AI
   probability.
5. For pairwise comparisons, randomize arm order and allow ties.

Return machine-readable JSON with per-case assertion results, L1 failures,
false-positive status, pairwise preference, and evidence. Report Chinese,
English, and mixed-language aggregates separately.
