"""Blog RSS fetcher — uses feedparser.

Two-step pattern: probe() first to test whether the feed parses, then fetch()
if it does. The orchestrator uses probe() to auto-promote feed_verified=true
on first successful pull.
"""
from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any, Literal

import feedparser

from ..dedup import canonicalize_url, is_seen, mark_seen


ProbeResult = Literal["ok", "empty", "broken"]


def probe(feed_url: str) -> ProbeResult:
    """Test a feed URL without consuming items.

    Returns:
      "ok"     — feed parsed and has at least one entry
      "empty"  — feed parsed but has no entries (treat as working — could be quiet day)
      "broken" — feed couldn't be fetched or parsed
    """
    if not feed_url:
        return "broken"
    parsed = feedparser.parse(feed_url, agent="DigestPipeline/1.0 (+nickhuo.com)")
    if getattr(parsed, "bozo", False) and not parsed.entries:
        return "broken"
    if not parsed.entries:
        return "empty"
    return "ok"


def _to_iso(struct_time: time.struct_time | None) -> str | None:
    if not struct_time:
        return None
    try:
        return datetime(*struct_time[:6], tzinfo=timezone.utc).isoformat()
    except (TypeError, ValueError):
        return None


def fetch(channel: dict, source: dict, state: dict, lookback_hours: int = 168) -> list[dict]:
    """Fetch new RSS entries.

    Returns at most 10 new items per channel (caller scores and trims further).
    Lookback default: 7 days. Items older than the cutoff are skipped even if unseen
    — protects against backfill flooding on first run.
    """
    feed_url = channel.get("feed")
    if not feed_url:
        return []

    parsed = feedparser.parse(feed_url, agent="DigestPipeline/1.0 (+nickhuo.com)")
    if parsed.bozo and not parsed.entries:
        # malformed feed AND no entries → nothing useful
        return []

    cutoff_ms = (time.time() - lookback_hours * 3600) * 1000
    out: list[dict] = []

    for entry in parsed.entries[:25]:  # consider top 25 most-recent
        url = entry.get("link") or ""
        if not url:
            continue

        # Identity dedup
        if is_seen(state, "articles", url):
            continue

        # Lookback filter (skip if we have a date AND it's too old)
        published_iso = _to_iso(entry.get("published_parsed") or entry.get("updated_parsed"))
        if published_iso:
            try:
                pub_ms = datetime.fromisoformat(published_iso.replace("Z", "+00:00")).timestamp() * 1000
                if pub_ms < cutoff_ms:
                    continue
            except ValueError:
                pass

        # Pull a short summary if present
        summary = (entry.get("summary") or entry.get("description") or "").strip()
        # Strip HTML tags very crudely — RSS summaries often contain <p> wrappers
        if "<" in summary:
            import re
            summary = re.sub(r"<[^>]+>", "", summary)
        summary = summary[:500]  # cap length, full text fetched at LLM time if needed

        item = {
            "kind": "article",
            "id": url,
            "url": url,
            "canonical_url": canonicalize_url(url),
            "title": (entry.get("title") or "").strip(),
            "published_at": published_iso,
            "summary": summary,
            "author": (entry.get("author") or "").strip() or source.get("author") or source.get("name"),
            "channel_id": channel.get("id"),
            "source_slug": source.get("slug"),
            "source_tier": source.get("tier"),
            "source_topics": source.get("topics", []),
            "source_category": source.get("category"),
        }
        mark_seen(state, "articles", url)
        out.append(item)

        if len(out) >= 10:
            break

    return out
