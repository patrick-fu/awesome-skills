---
name: llm-wiki-capture
description: "User-invoked capture from the current session into my-llm-wiki."
disable-model-invocation: true
---

# LLM Wiki Capture

Use this skill only when the user explicitly invokes `llm-wiki-capture`.

The job is to capture reusable knowledge from the current session into the
long-term LLM Wiki at `~/dev/my-llm-wiki`. Keep it light: this is a graph-aware
capture pass, not a full Wiki maintenance sweep.

## Branch

Default to **capture** for a bare invocation or clear save intent such as
"capture", "save this", "沉淀一下", or "记到 wiki".

Use **review** when the user sounds tentative or asks for inspection only, such
as "look at this", "evaluate", "dry run", "看一看", "评估一下", "有没有值得沉淀",
"先别写", or "先不要改".

Review means no file edits, no commit, and no push. Report candidate memories,
their evidence, likely canonical owners, and why each item should or should not
be captured.

## Delegation

Delegate the capture judgment to subagents when the host has a native subagent
or multi-agent facility. The main agent coordinates, applies accepted edits,
verifies the result, commits, pushes, and reports back.

Ask the subagent to read the original current-session record when it can find
one. Pass a session id or session file only if one is already available; do not
hard-code any host-specific session location. If no original session record is
available, capture mode downgrades to review mode. Say that the raw session was
not available and do not write to the Wiki.

Give the subagent this contract:

```text
Goal: Extract reusable LLM Wiki memories from the current session.
Scope: Current session only. Use the raw session record or user-provided source
materials as evidence; do not invent memories from summaries.
Wiki: ~/dev/my-llm-wiki.
Read first: AGENTS.md if present, purpose.md, schema.md, wiki/index.md,
wiki/log.md, any overview.md that exists or is referenced, and relevant Wiki
pages discovered from the index or rg.
Inventory: Use rg or scripts for a light graph pass over structure, wikilinks,
frontmatter, raw/source-summary relationships, source roles, Patrick audit
markers, and recent source/concept additions when those concepts exist.
Decision rule: Find the canonical owner first. Update an existing concept page
unless the new memory is a reusable topic that would become less discoverable
inside existing pages.
Deliverable: candidate memories with session evidence, canonical owner,
proposed file changes, index/log impact, verification checks, and reasons to
skip anything rejected.
```

Use one subagent for simple sessions. Split work only when the session is long,
the candidates span unrelated Wiki areas, or one agent should extract while
another checks canonical ownership.

## Capture

Before editing:

1. Ensure `~/dev/my-llm-wiki` exists. If it is missing, clone
   `git@github.com:patrick-fu/my-llm-wiki.git` there.
2. Work on the Wiki trunk branch. Pull with fast-forward only.
3. Require a clean Wiki worktree. If it is dirty with changes not created by
   this run, stop capture and report the blockage as review output.
4. Verify the subagent report is evidence-backed and within current-session
   scope.

Capture only reusable decisions, constraints, pitfalls, commands, domain facts,
or operating rules. Do not capture secrets, tokens, temporary progress, noisy
logs, unresolved guesses, or facts that cannot be traced to the session evidence.

Prefer weaving new knowledge into the existing graph:

- update the canonical owner page when one exists
- add cross-links where they clarify tension, boundaries, or evidence chains
- create a new page only for a reusable topic that does not fit an existing
  owner
- update `wiki/index.md` and `wiki/log.md` for every knowledge change

If there is nothing worth capturing, make no file changes, no commit, and no
push. Report the empty result and the reason.

## Verification And Commit

After editing in capture mode:

1. Review the diff against the subagent proposal and the Wiki schema.
2. Check changed wikilinks, frontmatter, raw paths, source-summary references,
   and index/log entries using repo scripts when available; otherwise use `rg`
   and direct inspection.
3. Run `git diff --check`.
4. Commit with Patrick Fu as the author and committer:
   `Patrick Fu <paaatrickfu@gmail.com>`.
5. Push the Wiki trunk branch.

The final report should include the captured memories, why they were worth
capturing, changed Wiki pages, verification performed, commit hash, and push
result.
