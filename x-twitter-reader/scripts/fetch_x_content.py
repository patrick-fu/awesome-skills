#!/usr/bin/env python3
"""Fetch X/Twitter post, thread, and Article content as JSON or Markdown."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def run_command(args: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    return result.returncode, result.stdout, result.stderr


def load_json(text: str, label: str) -> dict[str, Any]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{label} returned invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"{label} returned non-object JSON")
    return data


def twitter_cli_json(command: str, url: str, max_replies: int) -> dict[str, Any]:
    args = ["twitter", command]
    if command == "tweet":
        args.extend(["--json", "--max", str(max_replies), url])
    elif command == "article":
        args.extend(["--json", url])
    else:
        raise ValueError(f"unsupported twitter-cli command: {command}")

    code, stdout, stderr = run_command(args)
    if code != 0:
        detail = stderr.strip() or stdout.strip() or f"exit code {code}"
        raise RuntimeError(f"twitter {command} failed: {detail}")
    data = load_json(stdout, f"twitter {command}")
    if data.get("ok") is False:
        raise RuntimeError(f"twitter {command} returned ok=false: {data}")
    return data


def fetch_jina(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        f"https://r.jina.ai/{url}",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    api_key = os.getenv("JINA_API_KEY")
    if api_key:
        request.add_header("Authorization", f"Bearer {api_key}")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            text = response.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"Jina Reader failed: {exc}") from exc
    if not text.strip():
        raise RuntimeError("Jina Reader returned empty content")
    return {
        "ok": True,
        "schema_version": "x-twitter-reader/v1",
        "source": "jina",
        "data": {"url": url, "readerText": text},
    }


def is_article_url(url: str) -> bool:
    return "/i/article/" in url or "/article/" in url


def has_article(item: dict[str, Any]) -> bool:
    return bool(item.get("articleTitle") or item.get("articleText"))


def normalize_result(raw: dict[str, Any], source: str, original_url: str) -> dict[str, Any]:
    return {
        "ok": True,
        "schema_version": "x-twitter-reader/v1",
        "source": source,
        "original_url": original_url,
        "data": raw.get("data"),
    }


def extract_items(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        return [data]
    return []


def metric_line(metrics: dict[str, Any]) -> str:
    if not metrics:
        return ""
    names = ["likes", "retweets", "replies", "quotes", "views", "bookmarks"]
    parts = [f"{name}: {metrics.get(name)}" for name in names if metrics.get(name) is not None]
    return ", ".join(parts)


def media_lines(media: list[Any]) -> list[str]:
    lines: list[str] = []
    for entry in media:
        if not isinstance(entry, dict):
            continue
        bits = [str(entry.get("type") or "media")]
        if entry.get("width") and entry.get("height"):
            bits.append(f"{entry['width']}x{entry['height']}")
        if entry.get("url"):
            bits.append(str(entry["url"]))
        lines.append(" - " + " | ".join(bits))
    return lines


def clean_title(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned[:80] or "X/Twitter content"


def item_to_markdown(item: dict[str, Any], index: int = 0) -> str:
    raw_author = item.get("author")
    author: dict[str, Any] = raw_author if isinstance(raw_author, dict) else {}
    raw_metrics = item.get("metrics")
    metrics: dict[str, Any] = raw_metrics if isinstance(raw_metrics, dict) else {}
    title = item.get("articleTitle") or clean_title(str(item.get("text") or ""))

    heading = "#" if index == 0 else "##"
    out = [f"{heading} {title}", ""]
    meta = []
    if item.get("id"):
        meta.append(f"id: {item['id']}")
    if author:
        name = author.get("name") or ""
        screen = author.get("screenName") or ""
        meta.append(f"author: {name} (@{screen})" if screen else f"author: {name}")
    if item.get("createdAtISO"):
        meta.append(f"created: {item['createdAtISO']}")
    elif item.get("createdAtLocal"):
        meta.append(f"created: {item['createdAtLocal']}")
    if item.get("lang"):
        meta.append(f"lang: {item['lang']}")
    metric_text = metric_line(metrics)
    if metric_text:
        meta.append(metric_text)
    if meta:
        out.extend(["**Metadata**", ""])
        out.extend([f"- {line}" for line in meta])
        out.append("")

    text = str(item.get("text") or "").strip()
    article_text = str(item.get("articleText") or "").strip()
    if text:
        out.extend(["**Post text**", "", text, ""])
    if item.get("urls"):
        urls = [str(u) for u in item.get("urls") or []]
        out.extend(["**URLs**", ""])
        out.extend([f"- {u}" for u in urls])
        out.append("")
    if article_text:
        out.extend(["**Article text**", "", article_text, ""])
    media = item.get("media") if isinstance(item.get("media"), list) else []
    if media:
        out.extend(["**Media**", ""])
        out.extend(media_lines(media))
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def result_to_markdown(result: dict[str, Any]) -> str:
    if result.get("source") == "jina":
        raw_data = result.get("data")
        data: dict[str, Any] = raw_data if isinstance(raw_data, dict) else {}
        return str(data.get("readerText") or "").strip() + "\n"

    items = extract_items(result.get("data"))
    if not items:
        return "# X/Twitter content\n\nNo structured content returned.\n"

    first = items[0]
    out = ["---"]
    out.append(f"source: {json.dumps(result.get('original_url', ''), ensure_ascii=False)}")
    out.append(f"extractor: {json.dumps(result.get('source', ''), ensure_ascii=False)}")
    if first.get("id"):
        out.append(f"id: {json.dumps(first.get('id'), ensure_ascii=False)}")
    raw_author = first.get("author")
    author: dict[str, Any] = raw_author if isinstance(raw_author, dict) else {}
    if author.get("screenName"):
        out.append(f"author: {json.dumps(author.get('screenName'), ensure_ascii=False)}")
    if first.get("createdAtISO"):
        out.append(f"created: {json.dumps(first.get('createdAtISO'), ensure_ascii=False)}")
    out.extend(["---", ""])

    for index, item in enumerate(items):
        if index > 0:
            out.append("---")
            out.append("")
        out.append(item_to_markdown(item, index=index))
    return "\n".join(out).rstrip() + "\n"


def fetch(url: str, mode: str, max_replies: int) -> dict[str, Any]:
    errors: list[str] = []

    def try_tweet() -> dict[str, Any] | None:
        try:
            return normalize_result(twitter_cli_json("tweet", url, max_replies), "twitter-cli tweet", url)
        except RuntimeError as exc:
            errors.append(str(exc))
            return None

    def try_article() -> dict[str, Any] | None:
        try:
            return normalize_result(twitter_cli_json("article", url, max_replies), "twitter-cli article", url)
        except RuntimeError as exc:
            errors.append(str(exc))
            return None

    def try_jina() -> dict[str, Any] | None:
        try:
            return fetch_jina(url)
        except RuntimeError as exc:
            errors.append(str(exc))
            return None

    if mode == "tweet":
        result = try_tweet()
    elif mode == "article":
        result = try_article()
    elif mode == "jina":
        result = try_jina()
    else:
        result = try_article() if is_article_url(url) else try_tweet()
        items = extract_items(result.get("data") if result else None)
        if result and any(has_article(item) for item in items):
            return result
        if not result or is_article_url(url):
            result = try_article() or result
        if not result:
            result = try_jina()

    if result:
        if errors:
            result["warnings"] = errors
        return result
    raise RuntimeError("All extraction methods failed:\n- " + "\n- ".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="x.com or twitter.com URL")
    parser.add_argument("--mode", choices=["auto", "tweet", "article", "jina"], default="auto")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", help="Optional output path")
    parser.add_argument("--max-replies", type=int, default=20, help="Maximum replies for tweet mode")
    args = parser.parse_args()

    if not re.match(r"^https://(x|twitter)\.com/", args.url):
        print("Error: URL must start with https://x.com/ or https://twitter.com/", file=sys.stderr)
        return 2

    try:
        result = fetch(args.url, args.mode, args.max_replies)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.format == "json":
        content = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    else:
        content = result_to_markdown(result)

    if args.output:
        Path(args.output).write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
