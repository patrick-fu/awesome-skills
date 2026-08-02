---
name: x-twitter-reader
description: "Retrieves X and Twitter posts, reply threads, long-form Articles, author metadata, engagement metrics, linked URLs, and media references from x.com or twitter.com URLs. This skill is for content acquisition only: load it when a user asks to fetch, inspect, quote, summarize, translate, archive, or otherwise use the original content of an X post or Article, especially when the web page requires login or only shows a preview."
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

Prerequisites and privacy boundary:

- Require `uv`; check with `command -v uv` and stop if it is unavailable. Do
  not install it implicitly.
- The bundled script pins the PyPI package `twitter-cli==0.8.5` and requires
  Python 3.10+. `uv` may download the fixed dependency and a compatible Python
  into its cache on first run.
- `twitter-cli` may reuse `TWITTER_AUTH_TOKEN` / `TWITTER_CT0` or a logged-in
  Arc, Chrome, Edge, Firefox, or Brave session. Tell the user before the first
  credentialed run and obtain approval. Never print or persist cookies or
  tokens.

1. Normalize the URL:
   - Accept only HTTPS `x.com` and `twitter.com` URLs.
   - Reject `t.co`; ask for the expanded X/Twitter URL instead of following a
     redirect that may target an unrelated site.
   - Preserve the original URL in the output metadata.
   - Ignore URL query parameters when identifying the status id.
2. Run the bundled extractor from this skill directory:

   ```bash
   uv run --no-project --python 3.10 scripts/fetch_x_content.py 'https://x.com/user/status/123' --format markdown
   ```

3. For machine-readable output or debugging, request JSON:

   ```bash
   uv run --no-project --python 3.10 scripts/fetch_x_content.py 'https://x.com/user/status/123' --format json
   ```

4. If the user wants a saved artifact, pass `--output`:

   ```bash
   uv run --no-project --python 3.10 scripts/fetch_x_content.py 'https://x.com/user/status/123' --format markdown --output /tmp/x-content.md
   ```

5. Only use browser snapshots when the structured extractor fails or when the user asks about visual layout. X pages often hide Articles behind login, so snapshots are not authoritative for long-form content.

## Choosing Modes

The extractor defaults to `--mode auto`:

- For normal status URLs, it calls `twitter tweet --json` and emits the main post plus available replies.
- If the post contains Article fields, it emits the Article title and full Article text.
- For Article-looking URLs, it tries Article extraction first.
- It does not contact Jina Reader unless the user explicitly approves that
  third-party fallback and the command includes `--allow-jina`.

Use explicit modes when needed:

```bash
# Long-form Article only
uv run --no-project --python 3.10 scripts/fetch_x_content.py URL --mode article --format markdown

# Post and replies
uv run --no-project --python 3.10 scripts/fetch_x_content.py URL --mode tweet --format markdown

# Explicit Jina fallback
uv run --no-project --python 3.10 scripts/fetch_x_content.py URL --mode jina --allow-jina --format markdown
```

Jina Reader receives the query-free X URL and may cache or meter the request.
Use it only for public URLs after approval. The script ignores ambient
`JINA_API_KEY` by default; add `--use-jina-api-key` only when the user explicitly
authorizes use of that configured credential.

## Output Guidance

When reporting extraction results to the user:

- State whether the result is a post, reply thread, Article, or fallback reader output.
- Keep the original content separate from downstream analysis.
- Preserve headings, bullet lists, blockquotes, and code-like snippets in Article text.
- If media was not downloaded, say that media URLs were collected but not downloaded.
- If extraction is partial, explicitly say what failed and which fallback was used.

For long outputs, save the Markdown to `/tmp` or a user-requested path and summarize the location plus key metadata in chat.

## Common Failures And Fallbacks

- `twitter-cli` package missing: run the bundled script through the documented
  `uv run --no-project --python 3.10 ...` command instead of calling `python`
  directly.
- X page requires login: do not stop at browser login; use the structured extractor.
- Article text missing in `tweet` mode: rerun with `--mode article`.
- Jina returns only a preview or fails: prefer `twitter-cli` data. Jina is an
  explicitly authorized fallback, not the source of truth.
- Rate limits or upstream X changes: return the exact command, error text, and attempted fallback so the user can decide whether to retry later.

## Verification Checklist

Before treating extraction as successful, confirm at least one of these is true:

- the JSON contains `articleTitle` and non-empty `articleText` for an Article;
- the JSON contains non-empty `text` for the requested post;
- the Markdown output includes source metadata and non-empty content;
- for media requests, media URLs are present or the extractor explicitly reports none.
