# Development Notes

Notes for maintainers on how this skill is structured across platforms.

## Cross-Platform Design

- Shared source of truth:
  - `SKILL.md` carries the shared skill identity, trigger description, and `allowed-tools`
  - `references/dotfiles-operations.md` carries the reusable workflow details
  - `assets/` carries starter templates for public initialization
  - `scripts/` carries reusable GUI mode helpers owned by the skill
- Codex-specific metadata:
  - `agents/openai.yaml`
  - `policy.allow_implicit_invocation: false` keeps the skill explicit-only on Codex
- Claude Code compatibility rule:
  - keep `SKILL.md` frontmatter simple and compatible
  - avoid platform-specific workflow forks unless behavior truly diverges

## Editing Rules

- Put platform-specific UI or invocation policy in `agents/openai.yaml`
- Keep shared operational workflow in `SKILL.md` or `references/dotfiles-operations.md`
- Keep starter templates in `assets/` so initialization behavior stays deterministic and reusable
- Keep reusable operational scripts in `scripts/`, and reference them via `${CLAUDE_SKILL_DIR}` instead of user-local paths
