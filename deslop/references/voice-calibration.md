# Voice calibration

Load this file only when the user supplies a writing sample, explicitly asks to
match a named voice represented by supplied text, or has explicitly provided a
separate author preference layer for the current target.

## Privacy boundary

- Use only samples explicitly supplied for the current task.
- Do not search the filesystem, chat history, connected services, or the web for
  more examples unless the user explicitly asks.
- Do not store the sample in the skill, eval corpus, repository, or long-term
  memory.
- Do not reproduce private sample content in explanations unless needed to show
  a requested edit.
- A separately maintained preference layer may be used only when the user has
  authored or approved it and its declared author and scene match the target.
  Deslop must not create, expand, or refresh that layer from the current sample.

## Extract a temporary voice profile

Observe rather than stereotype:

- sentence-length range and cadence;
- vocabulary level, contractions, and code-switching;
- paragraph openings and transitions;
- common argument arcs and the ratio of short judgments to longer explanation;
- punctuation, parentheses, dashes, fragments, and list habits;
- directness, hedging, humor, uncertainty, and emotional distance;
- the frequency and job of contrasts, callouts, slang, and emoji;
- recurring phrases or deliberate quirks;
- how the writer closes sections and handles disagreement.

Distinguish stable habits from one-off topic effects. A technical sample does
not authorize a technical register for a personal email. Also distinguish voice
from repeated weaknesses: a recurring absolute claim, unsupported number, or
empty contrast does not become desirable merely because it appears often.

## Priority order

Resolve conflicts in this order:

1. factual and semantic fidelity;
2. the user’s explicit instruction for the target text;
3. the target text's existing stance and voice;
4. the supplied voice sample or approved preference layer;
5. the target scene and genre;
6. Deslop’s generic style guidance.

A sample may justify em dashes, fragments, repetition, slang, long sentences,
or other features that generic pattern lists might flag. It cannot justify a
new fact, experience, opinion, relationship, or level of certainty.

## Apply the profile

- Replace AI-default patterns with patterns actually present in the sample.
- When a concise, plain sample is paired with promotional target prose, reduce
  the target to its lowest source-backed proposition. Do not keep inflated
  adjectives merely because removing them leaves a short sentence.
- Match frequency, not mere presence. One parenthetical in a sample does not
  mean every paragraph needs one.
- Use an approved preference layer to resolve ambiguous editorial choices, not
  to add first-person experience, humor, slang, English terms, emoji, callouts,
  or a new ending that the target does not support.
- Preserve target-text terminology and audience requirements.
- Avoid caricature: do not exaggerate verbal tics or make the writer sound more
  casual, eccentric, or emotional than the sample.
- Run the full fidelity pass after voice changes.

Without a supplied sample or an approved in-scope preference layer, do not
simulate a specific person. Use a neutral, scene-appropriate voice and preserve
whatever individual signals the source already contains.
