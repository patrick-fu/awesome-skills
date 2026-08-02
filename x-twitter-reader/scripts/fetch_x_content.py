#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["twitter-cli==0.8.5"]
# ///
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
from urllib.parse import urlsplit, urlunsplit


X_HOSTS = {"x.com", "www.x.com", "twitter.com", "www.twitter.com"}
TCO_HOSTS = {"t.co", "www.t.co"}


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


def sanitized_x_url(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def fetch_jina(url: str, api_key: str | None = None) -> dict[str, Any]:
    target_url = sanitized_x_url(url)
    request = urllib.request.Request(
        f"https://r.jina.ai/{target_url}",
        headers={"User-Agent": "Mozilla/5.0"},
    )
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
        "original_url": url,
        "data": {"url": target_url, "readerText": text},
    }


def validate_x_url(url: str) -> None:
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    if parts.scheme != "https":
        raise ValueError("URL must use HTTPS")
    if host in TCO_HOSTS:
        raise ValueError(
            "t.co shortened URLs are not supported; provide the expanded "
            "x.com or twitter.com URL"
        )
    if host not in X_HOSTS:
        raise ValueError("URL must use x.com or twitter.com")
    if parts.username or parts.password or parts.port not in {None, 443}:
        raise ValueError("URL must not contain credentials or a non-standard port")


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


def fetch(
    url: str,
    mode: str,
    max_replies: int,
    *,
    allow_jina: bool = False,
    use_jina_api_key: bool = False,
) -> dict[str, Any]:
    errors: list[str] = []
    target_url = sanitized_x_url(url)

    if use_jina_api_key and not allow_jina:
        raise RuntimeError("--use-jina-api-key requires --allow-jina")
    jina_api_key: str | None = None
    if use_jina_api_key:
        jina_api_key = os.getenv("JINA_API_KEY")
        if not jina_api_key:
            raise RuntimeError(
                "--use-jina-api-key requires a non-empty JINA_API_KEY"
            )

    def try_tweet() -> dict[str, Any] | None:
        try:
            return normalize_result(
                twitter_cli_json("tweet", target_url, max_replies),
                "twitter-cli tweet",
                url,
            )
        except RuntimeError as exc:
            errors.append(str(exc))
            return None

    def try_article() -> dict[str, Any] | None:
        try:
            return normalize_result(
                twitter_cli_json("article", target_url, max_replies),
                "twitter-cli article",
                url,
            )
        except RuntimeError as exc:
            errors.append(str(exc))
            return None

    def try_jina() -> dict[str, Any] | None:
        try:
            result = fetch_jina(target_url, api_key=jina_api_key)
            result["original_url"] = url
            return result
        except RuntimeError as exc:
            errors.append(str(exc))
            return None

    if mode == "tweet":
        result = try_tweet()
    elif mode == "article":
        result = try_article()
    elif mode == "jina":
        if not allow_jina:
            raise RuntimeError("--mode jina requires --allow-jina")
        result = try_jina()
    else:
        result = try_article() if is_article_url(target_url) else try_tweet()
        items = extract_items(result.get("data") if result else None)
        if result and any(has_article(item) for item in items):
            return result
        if not result or is_article_url(target_url):
            result = try_article() or result
        if not result and allow_jina:
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
    parser.add_argument(
        "--allow-jina",
        action="store_true",
        help="Allow sending the sanitized X URL to the third-party Jina Reader",
    )
    parser.add_argument(
        "--use-jina-api-key",
        action="store_true",
        help="Read JINA_API_KEY only for an explicitly allowed Jina request",
    )
    args = parser.parse_args()

    try:
        validate_x_url(args.url)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    try:
        result = fetch(
            args.url,
            args.mode,
            args.max_replies,
            allow_jina=args.allow_jina,
            use_jina_api_key=args.use_jina_api_key,
        )
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
