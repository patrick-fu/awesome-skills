# Voice calibration

Load this file only when the user supplies a writing sample or explicitly asks
to match a named voice represented by supplied text.

## Privacy boundary

- Use only samples explicitly supplied for the current task.
- Do not search the filesystem, chat history, connected services, or the web for
  more examples unless the user explicitly asks.
- Do not store the sample in the skill, eval corpus, repository, or long-term
  memory.
- Do not reproduce private sample content in explanations unless needed to show
  a requested edit.

## Extract a temporary voice profile

Observe rather than stereotype:

- sentence-length range and cadence;
- vocabulary level, contractions, and code-switching;
- paragraph openings and transitions;
- punctuation, parentheses, dashes, fragments, and list habits;
- directness, hedging, humor, uncertainty, and emotional distance;
- recurring phrases or deliberate quirks;
- how the writer closes sections and handles disagreement.

Distinguish stable habits from one-off topic effects. A technical sample does
not authorize a technical register for a personal email.

## Priority order

Resolve conflicts in this order:

1. factual and semantic fidelity;
2. the user’s explicit instruction for the target text;
3. the supplied voice sample;
4. the target scene and genre;
5. Deslop’s generic style guidance.

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
- Preserve target-text terminology and audience requirements.
- Avoid caricature: do not exaggerate verbal tics or make the writer sound more
  casual, eccentric, or emotional than the sample.
- Run the full fidelity pass after voice changes.

Without a supplied sample, do not simulate a specific person. Use a neutral,
scene-appropriate voice and preserve whatever individual signals the source
already contains.
