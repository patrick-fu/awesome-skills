---
name: llm-wiki-capture
description: >-
  User-invoked capture, review, or source ingest into a maintained LLM wiki or
  knowledge base.
disable-model-invocation: true
---

# LLM Wiki Capture

Use this skill only when the user explicitly invokes `llm-wiki-capture`.

The job is to capture reusable knowledge from the current session or ingest
explicitly provided sources into a maintained long-term LLM wiki, notes
repository, or knowledge base. Keep it light: this is a graph-aware pass, not a
full library maintenance sweep unless the user explicitly asks for full
integration.

## Configuration

Resolve local configuration in this order:

1. explicit instructions from the user for this run
2. repository-local `AGENTS.md` or equivalent project instructions
3. global user or agent instructions configured by the host
4. repository docs such as `README.md`, `purpose.md`, or `schema.md`

Before any write-capable mode, resolve these values when they are relevant:

- knowledge base root path
- clone URL if the repo may need to be initialized
- integration branch
- navigation files such as index, log, overview, schema, or purpose pages
- source storage conventions such as raw/source-summary layout or provenance
  files
- clean-worktree policy
- commit policy: no commit, commit only, or commit and push
- commit identity if commit is allowed

If a write-capable mode is selected and required configuration is missing, ask
once in plain text. If the user does not want to decide and review mode would
still be useful, downgrade to review instead of guessing.

For setup, initialization, `AGENTS.md` examples, and automation patterns, read
`references/configuration-guide.md`.

## Mode Selection

Default to **capture** for a bare invocation or clear save intent such as
"capture", "save this", "沉淀一下", or "记到 wiki".

Use **source ingest** when the invocation includes one or more external URLs,
document links, source files, or explicit source materials. In this mode the
provided sources are the evidence; the current session is only task context.

Use **review** when the user sounds tentative or asks for inspection only, such
as "look at this", "evaluate", "dry run", "看一看", "评估一下", "有没有值得沉淀",
"先别写", or "先不要改".

Review means no file edits, no commit, and no push. Report candidate memories,
their evidence, likely canonical owners, and why each item should or should not
be captured. If review intent and source links both appear, do source review:
report duplicate status, originals, references, extraction plan, and likely
knowledge-base owners without editing.

Use **full integration** only when the user explicitly asks for a full-library
sweep, such as "全量同步", "全量整合", "全面梳理", "全库翻修", or "full
integration". Do not infer this mode from a normal capture request.

## Source Ingest

Source ingest turns provided materials into source-grounded knowledge-base
entries.

- prefer domain-specific fetchers first, based on local tool configuration for
  each source type; if no such tool is configured or available, fall back to a
  generic browser or summarization path
- deduplicate before adding: compare canonical URLs, short/long URL variants,
  mirrors, reposts, and near-identical text; update the canonical page instead
  of creating parallel source summaries
- for translation or interpretation documents with an explicit original source,
  fetch the original too; for pure translations, normally store only the
  original raw source and keep the translation URL as provenance if useful; for
  interpretations, merge the interpretation and original into one canonical
  source with clear secondary-provenance notes
- for reference links attached to a self-contained article, fetch relevant
  first-hop references and store them independently; do not recurse into links
  found inside those references
- convert image, video, and audio sources to text early; store OCR/transcripts
  in raw and avoid committing original assets unless the asset itself is
  evidence rather than just a text carrier
- if an image asset must be stored, compress it first, keep the longest side
  around 1200 px or less when reasonable, lower quality enough to reduce size,
  prefer WebP, and record why the image itself is needed
- finish the ingest by weaving stable claims into canonical concepts,
  comparisons, queries, and any configured navigation files such as index or log

## Full Integration

Full integration is a graph-wide review of the existing knowledge base. Its
purpose is to repair gaps and create new synthesis from collisions among
sources, not merely to save the current session.

Run this mode like a maintenance workflow:

- build an inventory from the configured navigation files, frontmatter,
  wikilinks, raw/source-summary relationships, source roles, query pages, and
  recent source/concept additions
- review concept correctness, provenance caveats, stale claims, duplicate
  ownership, weak cross-links, and missing canonical owners
- deepen integration by weaving related sources into existing concepts and by
  surfacing tensions, boundaries, and evidence chains
- create a new concept only when multiple sources create real conceptual
  pressure that would be less discoverable inside existing pages
- look for a spark: a durable new viewpoint grounded in the source graph, with
  open questions separated from evidence-backed claims
- use subagents for structural audit, concept correction, synthesis review,
  repair, and final acceptance when the host supports them

Pause full integration rather than guessing when it needs broad external
verification, a schema migration, destructive file moves, or a large new source
ingest beyond the user's requested sweep.

## Delegation

Delegate the capture judgment to subagents when the host has a native subagent
or multi-agent facility. The main agent coordinates, applies accepted edits,
verifies the result, commits if allowed by local policy, pushes if allowed by
local policy, and reports back.

Ask the subagent to read the original current-session record when it can find
one. Pass a session id or session file only if one is already available; do not
hard-code any host-specific session location. If no original session record is
available and the user did not provide explicit source material, capture mode
downgrades to review mode. Say that evidence was not available and do not write
to the knowledge base.

For normal capture/review branches, give the subagent this contract. For source
ingest, use the Source Ingest contract below. For full integration, use the
Full Integration bullets above as the subagent scope.

```text
Goal: Extract reusable LLM Wiki memories from the current session.
Scope: Current session only. Use the raw session record or user-provided source
materials as evidence; do not invent memories from summaries.
Knowledge base: <KNOWLEDGE_BASE_ROOT>.
Read first: configured navigation files, schema docs, overview docs, and
relevant owner pages discovered from the index or rg.
Inventory: Use rg or scripts for a light graph pass over structure, wikilinks,
frontmatter, raw/source-summary relationships, source roles, local audit
markers, and recent source/concept additions when those concepts exist.
For small captures, target likely canonical owners instead of scanning broad
knowledge-base structure.
Decision rule: Find the canonical owner first. Update an existing concept page
unless the new memory is a reusable topic that would become less discoverable
inside existing pages.
Deliverable: candidate memories with session or user-provided source evidence,
canonical owner, proposed file changes, navigation-file impact, verification
checks, and reasons to skip anything rejected.
```

For source ingest:

```text
Goal: Ingest the user-provided external sources into the configured knowledge
base.
Scope: Provided sources plus explicit originals and first-hop references only.
Use domain-specific tools before generic browser access.
Knowledge base: <KNOWLEDGE_BASE_ROOT>.
Read first: configured navigation files, schema docs, and relevant owner pages
found by rg.
Decisions: detect duplicates, originals, translations, interpretations,
first-hop references, and multimedia-to-text needs before proposing edits.
Deliverable: fetched-source inventory, raw/source-summary strategy, canonical
owner pages, provenance/source-role notes, integration edits, skipped links
with reasons, verification checks, and commit/push readiness.
```

Use one subagent for simple sessions. Split work only when the session is long,
the candidates span unrelated knowledge-base areas, there are many source
links, or one agent should extract while another checks canonical ownership.

## Capture

Before editing:

1. Resolve the configured knowledge-base root. If it is missing and a clone URL
   is configured, clone it. If neither exists, ask once or downgrade to review.
2. Work on the configured integration branch.
3. Apply the configured clean-worktree policy. If the worktree is dirty with
   changes not created by this run and the policy requires cleanliness, stop
   capture and report the blockage as review output.
4. Verify the subagent report is evidence-backed and within current-session or
   source-ingest scope, unless the selected mode is full integration.

Capture only reusable decisions, constraints, pitfalls, commands, domain facts,
or operating rules. Do not capture secrets, tokens, temporary progress, noisy
logs, unresolved guesses, or facts that cannot be traced to the session
evidence.

Prefer weaving new knowledge into the existing graph:

- update the canonical owner page when one exists
- add cross-links where they clarify tension, boundaries, or evidence chains
- create a new page only for a reusable topic that does not fit an existing
  owner
- update configured navigation files for every knowledge change when those files
  exist

If there is nothing worth capturing, make no file changes, no commit, and no
push. Report the empty result and the reason.

## Verification And Commit

After editing in capture or source ingest mode:

1. Review the diff against the subagent proposal and the local schema or repo
   conventions.
2. Check changed wikilinks, frontmatter, raw paths, source-summary references,
   and configured navigation files using repo scripts when available; otherwise
   use `rg` and direct inspection.
3. Run `git diff --check`.
4. If local policy allows commit, commit with the configured identity.
5. If local policy allows push, fetch before pushing and confirm the branch is
   still fast-forwardable. If the push is rejected, stop and report the
   conflict rather than force-pushing.
6. If local policy is review-only or diff-only, stop after verification and
   report what remains for the user.

The final report should include the captured memories or ingested sources, why
they were worth saving, changed knowledge-base pages, verification performed,
and the commit hash or push result when applicable.
