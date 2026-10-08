# Project Skill

Write verifier instructions and UI metadata in English.

## Discovery

Keep the verifier with the product, versioned with its code. Follow compatible
repository conventions; otherwise use `.agents/skills/verify-<app>/`. For Claude
Code discovery, link from `.claude/skills/` when needed; keep one source.
For sessions starting outside the repo, add a conditional project `AGENTS.md`
pointer to the verifier rather than installing project knowledge globally.

Name the product and verification surface in its description; trigger on scoped
acceptance, reproduction or regression checks. Keep feature recipes in the body
or linked map. For Codex, include `agents/openai.yaml` with quoted `display_name`,
a 25–64-character `short_description`, and a `default_prompt` naming
`$verify-<app>`. Align the display name with the skill name.

## Feedback

Teach the generated verifier to check for proven workflow drift after each run.
When a recipe or helper is stale and `$build-verifier` is available, use it for a
scoped repair, then re-run the affected check. Keep a failed product expectation
intact. With no drift, leave the verifier unchanged; if maintenance is unavailable
or blocked, report the concrete gap and retained evidence.
