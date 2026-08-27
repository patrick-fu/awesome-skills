# Transcript review

Treat every model output as independent evidence, not as a vote that can be merged mechanically.

1. Check coverage, missing spans, repeated spans, implausible text during silence, and timestamp discontinuities.
2. Prioritize names, products, acronyms, numbers, percentages, dates, and negation.
3. Agreement raises confidence but does not prove correctness. Disagreement identifies review targets but does not identify the winner.
4. MOSS speaker labels are clustering identifiers. Across long-audio chunks, identical labels do not imply the same real speaker.
5. Resolve conflicts from the original audio and user context. If evidence is insufficient, mark the span as uncertain instead of choosing the more fluent sentence.
6. Preserve raw JSON and every independent transcript. Produce a corrected reading copy only when the user asks for one.
