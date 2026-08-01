# Deslop evaluation rubric

Freeze this rubric before model outputs are produced. Do not lower a gate after
seeing a failure.

## Test arms

Run every applicable behavior case against:

1. Deslop candidate;
2. `shuorenhua` fixed at commit `6318b703e0c264dcf8822ee817bbea0519c6a62b`;
3. `humanizer` fixed at commit `523374dee72d67c7b2b5f858ea0094ffda49c3ac`;
4. `humanizer-zh` fixed at commit `91f3d394db8419c20d67ebe22a96cf8fee0a404b`;
5. no-skill baseline.

Judge Chinese, English, and mixed-language subsets separately. A strong score in
one language cannot compensate for regression in another.

## L1: hard fidelity gates

Any of these is a critical failure:

- invented fact, example, citation, date, number, capability, feedback, emotion,
  opinion, or personal experience;
- protected span, number-object pair, actor, ownership, direction, condition,
  modality, negation, completion state, attribution, or effect type drift;
- unauthorized deletion of unique information;
- damage to frontmatter, code, structured data, quotation, or link destination;
- output that violates `audit`, `embedded`, `file`, `in-place`, or no-op mode.

Release gate: **zero L1 failures** across the fixed full suite.

## L2: false-positive gate

Natural, quoted, technical, academic, legal, release-note, and domain-term cases
must not be mechanically rewritten.

Release gate: **fewer than 10% false-positive rewrites**, with zero false
positives that create an L1 failure.

## L3: editorial quality

Use blind pairwise review. Judge:

- naturalness in the target scene;
- preservation of author stance and register;
- removal of structural rather than merely lexical slop;
- direct usability without another editing pass.

Release gate: Deslop must be no worse than `shuorenhua` on Chinese, no worse
than `humanizer` on English, and no worse than the best old skill on the mixed
subset. Report ties rather than forcing a winner.

## Trigger gate

Run each query in `triggers.json` three times against the same runtime used for
release. Use held-out queries when optimizing the description.

Release gate: **at least 90% classification accuracy**, with special attention
to false activation on generic polishing, translation, summary, fact-checking,
from-scratch drafting, and code cleanup.

## Reporting

Record model/runtime version, skill commit, prompt order, run date, raw outputs,
per-case L1 evidence, false-positive counts, and blind preferences. Do not
publish a single “AI score.”
