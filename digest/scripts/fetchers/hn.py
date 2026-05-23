"""Hacker News fetcher — uses the public Algolia search API.

This fetcher is source-agnostic: it doesn't read any sources/*.md file. HN is a
firehose of community-curated content, so the orchestrator runs it once per
digest cycle regardless of what's in `sources/`.

API: https://hn.algolia.com/api  (free, no auth, no rate limit documented but be polite)
"""
from __future__ import annotations

import time
from datetime import datetime, timezone
from urllib.parse import urlencode
import urllib.request
import urllib.error
import json

from ..dedup import canonicalize_url, is_seen, mark_seen


HN_API = "https://hn.algolia.com/api/v1/search"


def fetch(state: dict, min_points: int = 50, lookback_hours: int = 24,
          max_items: int = 100) -> list[dict]:
    """Pull HN stories above min_points within the lookback window.

    Caller is the orchestrator, not a per-source loop — there's no `channel`
    or `source` argument here.
    """
    cutoff_ts = int(time.time() - lookback_hours * 3600)
    params = {
        "tags": "story",
        "numericFilters": f"points>{min_points},created_at_i>{cutoff_ts}",
        "hitsPerPage": str(max_items),
    }
    url = f"{HN_API}?{urlencode(params)}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DigestPipeline/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, json.JSONDecodeError, OSError):
        return []

    out: list[dict] = []
    for hit in data.get("hits", []):
        story_id = hit.get("objectID")
        if not story_id:
            continue
        if is_seen(state, "hn", story_id):
            continue

        external_url = hit.get("url") or ""
        hn_url = f"https://news.ycombinator.com/item?id={story_id}"
        title = hit.get("title") or hit.get("story_title") or ""
        created_at = hit.get("created_at")

        item = {
            "kind": "hn",
            "id": story_id,
            "url": external_url or hn_url,
            "canonical_url": canonicalize_url(external_url) if external_url else None,
            "hn_url": hn_url,
            "title": title.strip(),
            "points": hit.get("points") or 0,
            "num_comments": hit.get("num_comments") or 0,
            "author": hit.get("author"),
            "published_at": created_at,
            # HN is its own "source" — no source_slug because it's not in sources/
            "source_slug": "_hn",
            "source_category": "aggregator",
            "channel_id": "_hn",
        }
        mark_seen(state, "hn", story_id)
        out.append(item)

    return out
