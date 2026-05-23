"""Blog scraper — used when a blog has no public RSS.

Strategy: shell out to Defuddle CLI (already installed via the obsidian:defuddle
skill — `npm i -g defuddle` if missing). Defuddle handles HTML parsing,
clutter removal, and gives back markdown.

For index pages we extract candidate article URLs by parsing the JSON output
and looking at internal links that match `articleBaseUrl`. This is a deliberate
half-scrape: we trust Defuddle to find the readable links and skip the rest.

Per-source overrides (article URL prefix patterns) live in this module's
PER_SOURCE table — keyed by source slug. New scraped sources just need a
table entry; no code changes.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from typing import Any

from ..dedup import canonicalize_url, is_seen, mark_seen


# Per-source URL pattern hints. The scraper extracts links from the index page
# (the channel.url) and keeps only those matching `article_url_pattern`.
PER_SOURCE: dict[str, dict[str, Any]] = {
    "anthropic": {
        # anthropic-engineering channel articles look like /engineering/<slug>
        "anthropic-engineering": {"article_url_pattern": r"^https://www\.anthropic\.com/engineering/[^/]+$"},
        "anthropic-claude-blog": {"article_url_pattern": r"^https://claude\.com/blog/[^/]+$"},
    },
    "sequoia": {
        "sequoia-blog": {"article_url_pattern": r"^https://www\.sequoiacap\.com/article/[^/]+/?$"},
    },
    "google-deepmind": {
        "google-deepmind-blog": {"article_url_pattern": r"^https://(www\.|deepmind\.)?(google|deepmind)\.com/discover/blog/[^/]+"},
    },
    # Add more sources here as you scrape them. Default behavior (no entry)
    # is "scrape index, take all internal links matching the index host".
}


def _have_defuddle() -> bool:
    return shutil.which("defuddle") is not None


def _run_defuddle(url: str, mode: str = "json") -> dict | str | None:
    """Run defuddle. mode='json' returns dict; mode='md' returns markdown string."""
    if not _have_defuddle():
        return None
    try:
        if mode == "json":
            result = subprocess.run(
                ["defuddle", "parse", url, "--json"],
                capture_output=True, text=True, timeout=60,
            )
            if result.returncode != 0:
                return None
            return json.loads(result.stdout)
        else:
            result = subprocess.run(
                ["defuddle", "parse", url, "--md"],
                capture_output=True, text=True, timeout=60,
            )
            if result.returncode != 0:
                return None
            return result.stdout
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError):
        return None


def _extract_article_links(index_html: str, pattern: re.Pattern[str] | None) -> list[str]:
    """Pull href values out of HTML. If pattern is given, keep only matching."""
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', index_html or "")
    if pattern:
        hrefs = [h for h in hrefs if pattern.match(h)]
    # Dedup preserving order
    seen, ordered = set(), []
    for h in hrefs:
        if h not in seen:
            seen.add(h)
            ordered.append(h)
    return ordered


def fetch(channel: dict, source: dict, state: dict, lookback_hours: int = 168) -> list[dict]:
    """Defuddle-driven scrape.

    Steps:
      1. Defuddle the channel.url (the index page)
      2. Pull candidate article URLs that match the source-specific pattern
      3. For each new URL: defuddle again to get the article body
      4. Mark seen, return up to 5 items per channel
    """
    if not _have_defuddle():
        # Defuddle not installed — return empty silently. The README warns about this.
        return []

    index_url = channel.get("url")
    if not index_url:
        return []

    # Pull index HTML via defuddle (json mode includes raw html in 'content' field;
    # but defuddle markdown is cleaner for link extraction, so we use json)
    index_data = _run_defuddle(index_url, mode="json")
    if not index_data:
        return []

    # Defuddle's JSON output structure (subject to upstream change):
    #   { content: <html or markdown>, title, description, ... }
    raw = index_data.get("content") or index_data.get("html") or index_data.get("markdown") or ""

    # Pattern-filter
    src_overrides = PER_SOURCE.get(source.get("slug", ""), {})
    pattern_str = (src_overrides.get(channel.get("id"), {}) or {}).get("article_url_pattern")
    pattern = re.compile(pattern_str) if pattern_str else None

    candidate_urls = _extract_article_links(raw, pattern)[:10]
    out: list[dict] = []

    for url in candidate_urls:
        if is_seen(state, "articles", url):
            continue

        # Fetch article content
        article = _run_defuddle(url, mode="json")
        if not article:
            continue

        title = (article.get("title") or "").strip()
        body_md = article.get("markdown") or article.get("content") or ""
        # cap body to keep candidate JSON small
        body_text = re.sub(r"\s+", " ", body_md)[:1500].strip()
        published_at = article.get("publishedAt") or article.get("date")

        item = {
            "kind": "article",
            "id": url,
            "url": url,
            "canonical_url": canonicalize_url(url),
            "title": title,
            "published_at": published_at,
            "summary": body_text,
            "author": article.get("author") or source.get("author") or source.get("name"),
            "channel_id": channel.get("id"),
            "source_slug": source.get("slug"),
            "source_tier": source.get("tier"),
            "source_topics": source.get("topics", []),
            "source_category": source.get("category"),
            "scraped": True,  # signal to the scoring layer that this was scrape vs RSS
        }
        mark_seen(state, "articles", url)
        out.append(item)

        if len(out) >= 5:
            break

    return out
