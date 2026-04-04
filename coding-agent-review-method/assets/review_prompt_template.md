Review the current change in {{WORKDIR}}.

Treat the provided diff, range, patch, commit, or file list as the primary review scope. Also inspect the minimum necessary related context needed to evaluate impact and chained risk, especially touched symbols, callers, references, consumers, contracts, compatibility assumptions, and immediate upstream/downstream behavior.

Context:
- Coding agent: {{CODING_AGENT}}
- Operating guide: {{OPERATING_GUIDE}}

Background:
- {{BACKGROUND}}

Already reviewed:
- {{ALREADY_REVIEWED}}

Review scope:
- {{REVIEW_SCOPE}}

Focus:
- {{FOCUS_AREAS}}
- Impact edges to verify: touched symbols, callers, references, consumers, contracts, compatibility assumptions, and immediate upstream/downstream effects.

Applicable domain guidance:
- {{DOMAIN_GUIDANCE}}

Constraints:
- Review only. Do not modify files.
- Do not start build or test work.
- Treat the supplied diff/range as primary scope.
- Read the minimum additional context needed to assess impact and chained risk.
- Explicitly check relevant callers, references, consumers, contracts, and compatibility assumptions when the change may affect them.
- Do not expand into broad repository exploration once added context stops changing the risk assessment.
- Follow a findings-first structure.
- If no clear issue exists, say so explicitly.
