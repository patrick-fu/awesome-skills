# Evaluation runbook

The committed corpus is public and synthetic. Do not add private writing samples
or user data.

Real author samples may inform an ephemeral manual review, but do not commit
their text, URLs, identifying phrases, or derived personal profiles. Convert a
generalizable behavior into a new synthetic case instead.

## Validate and generate blind inputs

```bash
python3 automation/eval/check_cases.py
python3 automation/eval/make_blind.py
git diff --exit-code -- evals/benchmark-blind.json evals/benchmark-map.json
```

`make_blind.py` uses a fixed seed. Treat generated drift as a corpus change,
not formatting noise.

## Smoke then full run

Start with a balanced subset of about 20 cases covering all languages, modes,
scopes, no-op behavior, and protected file regions. After the behavior contract
stabilizes, run all cases against the five arms frozen in
`evals/rubric.md`.

Give rewrite agents only the assigned skill snapshot, `rewrite-prompt.md`, and
the assigned blind cases. Give judges the source cases, map, rubric, and raw
outputs. Do not let a rewrite arm read another arm or the expected assertions.

Use different model families for rewriting and judging when possible. Preserve
raw outputs, model/runtime identifiers, skill commits, prompt order, timestamps,
and judge evidence. Never summarize away an L1 failure.

## Trigger evaluation

Run all 20 entries in `evals/triggers.json` three times on the target runtime.
Optimize the description on a training split and select it by held-out accuracy.
Do not weaken near-miss negatives merely to improve the score.

## Release decision

Apply the frozen gates in `evals/rubric.md`. A natural-looking output cannot
compensate for an L1 failure. If a gate fails, revise the skill and rerun the
fixed suite; do not edit the expected result after seeing the output.
