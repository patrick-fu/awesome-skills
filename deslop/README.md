# Deslop / 说人话

Deslop is a bilingual Agent Skill for editing existing Chinese, English, and
mixed-language prose. It removes formulaic AI-writing patterns while protecting
facts, relationships, register, and author voice.

It is an editor, not an AI detector. It does not assign AI probabilities,
promise detector evasion, or invent personality to make text look human.

## What it does

- rewrites AI-slop-heavy prose into one ready-to-use version;
- audits a draft without rewriting when asked;
- preserves facts, numbers, attribution, modality, and responsibility;
- supports temporary voice calibration from a supplied sample or an explicit,
  user-maintained author preference layer without learning profiles implicitly;
- protects frontmatter, code, data, and link targets during explicit file edits;
- leaves already-natural prose unchanged.

## Install

Install it from the collection:

```bash
npx skills add patrick-fu/awesome-skills -g -s deslop
```

## Use

```text
Use $deslop to remove the AI slop from this draft without changing any facts.

先用 $deslop 标出这段话里的 AI 味，不要改写。

用 $deslop 改这个 Markdown 文件，保留 frontmatter、代码块和链接目标。
```

Generic requests such as “polish this,” “translate this,” or “summarize this” do
not activate Deslop unless the user explicitly asks for an anti-slop pass.

## Design

The skill uses one shared fidelity contract, language-specific pattern guides,
scene-aware editing, three edit scopes (`balanced`, `in-place`, `rebuild`), and
a final semantic comparison against the source. Detailed examples live in the
evaluation corpus rather than the runtime prompt.

## License and attribution

Deslop is released under the MIT License. See [NOTICE.md](NOTICE.md) for the
fixed upstream revisions synthesized into this implementation. Deslop does not
track or automatically merge later upstream changes.
