---
name: x-twitter-reader
description: "Retrieves X and Twitter posts, reply threads, long-form Articles, author metadata, engagement metrics, linked URLs, and media references from x.com or twitter.com URLs. This skill is for content acquisition only: load it when a user asks to fetch, inspect, quote, summarize, translate, archive, or otherwise use the original content of an X post or Article, especially when the web page requires login or only shows a preview."
allowed-tools:
  - Read
  - Write
  - Bash
---

# X Twitter Reader

Use this skill to acquire source content from X/Twitter. Translation, summarization, critique, or archiving are downstream tasks; first extract the original post, thread, or Article faithfully.

## What This Skill Returns

Prefer structured content over visual page scraping. A good extraction includes:

- original source URL and resolved X/Twitter URL when available
- post id, author name, screen name, timestamp, and language
- engagement metrics when available: likes, reposts, replies, quotes, views, bookmarks
- post text and linked URLs
- media references with type, URL, width, and height when available
- long-form Article title and full Article text when present
- reply-thread items when the user asks for thread or conversation context

Do not translate, summarize, or rewrite during extraction unless the user explicitly asks for that downstream output. If the user asks to translate an X URL, first extract with this skill, then translate the extracted content.

## Primary Workflow

1. Normalize the URL:
   - Accept `https://x.com/...`, `https://twitter.com/...`, and X-shortened URLs.
   - Preserve the original URL in the output metadata.
   - Ignore URL query parameters when identifying the status id.
2. Run the bundled extractor from this skill directory:

   ```bash
   uv run --with twitter-cli --with pyyaml python scripts/fetch_x_content.py 'https://x.com/user/status/123' --format markdown
   ```

3. For machine-readable output or debugging, request JSON:

   ```bash
   uv run --with twitter-cli --with pyyaml python scripts/fetch_x_content.py 'https://x.com/user/status/123' --format json
   ```

4. If the user wants a saved artifact, pass `--output`:

   ```bash
   uv run --with twitter-cli --with pyyaml python scripts/fetch_x_content.py 'https://x.com/user/status/123' --format markdown --output /tmp/x-content.md
   ```

5. Only use browser snapshots when the structured extractor fails or when the user asks about visual layout. X pages often hide Articles behind login, so snapshots are not authoritative for long-form content.

## Choosing Modes

The extractor defaults to `--mode auto`:

- For normal status URLs, it calls `twitter tweet --json` and emits the main post plus available replies.
- If the post contains Article fields, it emits the Article title and full Article text.
- For Article-looking URLs, it tries Article extraction first.
- If `twitter-cli` fails, it falls back to Jina Reader when possible.

Use explicit modes when needed:

```bash
# Long-form Article only
uv run --with twitter-cli --with pyyaml python scripts/fetch_x_content.py URL --mode article --format markdown

# Post and replies
uv run --with twitter-cli --with pyyaml python scripts/fetch_x_content.py URL --mode tweet --format markdown

# Jina fallback or quick text extraction
uv run --with twitter-cli --with pyyaml python scripts/fetch_x_content.py URL --mode jina --format markdown
```

## Output Guidance

When reporting extraction results to the user:

- State whether the result is a post, reply thread, Article, or fallback reader output.
- Keep the original content separate from downstream analysis.
- Preserve headings, bullet lists, blockquotes, and code-like snippets in Article text.
- If media was not downloaded, say that media URLs were collected but not downloaded.
- If extraction is partial, explicitly say what failed and which fallback was used.

For long outputs, save the Markdown to `/tmp` or a user-requested path and summarize the location plus key metadata in chat.

## Common Failures And Fallbacks

- `twitter-cli` package missing: rerun through `uv run --with twitter-cli --with pyyaml ...` instead of calling `python` directly.
- X page requires login: do not stop at browser login; use the structured extractor.
- Article text missing in `tweet` mode: rerun with `--mode article`.
- Jina returns only a preview or fails: prefer `twitter-cli` data. Jina is optional enrichment, not the source of truth.
- Rate limits or upstream X changes: return the exact command, error text, and attempted fallback so the user can decide whether to retry later.

## Verification Checklist

Before treating extraction as successful, confirm at least one of these is true:

- the JSON contains `articleTitle` and non-empty `articleText` for an Article;
- the JSON contains non-empty `text` for the requested post;
- the Markdown output includes source metadata and non-empty content;
- for media requests, media URLs are present or the extractor explicitly reports none.
