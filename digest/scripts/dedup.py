"""
Deduplication state for the digest pipeline.

Six buckets, each keyed by the natural primary identifier of the medium:
  - tweets          (skipped — X fetch disabled)
  - articles        — canonicalized URL
  - podcasts        — RSS GUID
  - youtube         (skipped — YouTube fetch disabled)
  - hn              — Algolia objectID
  - github_trending — "owner/repo"

Each bucket has its own TTL. Entries older than the TTL are pruned at save time.

Layer-3 content-level dedup (cluster_by_canonical_url) collapses items that
share a referenced canonical URL — e.g. when 5 X accounts and HN all link to
the same Cloudflare blog post, only the highest-scoring representative survives,
the rest become endorsements.
"""

from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse


STATE_PATH = Path(__file__).resolve().parent.parent / ".state" / "seen.json"

# Per-bucket TTL in days. tweets/youtube kept for forward-compat; not currently fetched.
TTL_DAYS = {
    "tweets": 7,
    "articles": 7,
    "podcasts": 30,
    "youtube": 30,
    "hn": 7,
    "github_trending": 7,
}

# Query params to strip when canonicalizing a URL — these are tracking junk
# that don't change the actual resource.
_TRACKING_PARAM_PREFIXES = ("utm_", "fbclid", "gclid", "mc_eid", "mc_cid")
_TRACKING_PARAM_NAMES = {"ref", "source", "campaign", "from", "share"}


def canonicalize_url(url: str) -> str:
    """Normalize a URL so syndication / tracking variants collapse to one key.

    Strips UTM and other tracking params, lowercases host, removes fragment,
    drops trailing slash. Idempotent — safe to call multiple times.

    >>> canonicalize_url("https://Anthropic.com/News/foo/?utm_source=x#bar")
    'https://anthropic.com/News/foo'
    """
    url = url.strip()
    if not url:
        return url
    p = urlparse(url)
    qs = [
        (k, v) for k, v in parse_qsl(p.query, keep_blank_values=False)
        if not any(k.lower().startswith(pre) for pre in _TRACKING_PARAM_PREFIXES)
        and k.lower() not in _TRACKING_PARAM_NAMES
    ]
    path = p.path.rstrip("/") or "/"
    return urlunparse(p._replace(
        netloc=p.netloc.lower(),
        path=path,
        query=urlencode(qs),
        fragment="",
    ))


def load_state() -> dict:
    """Load the state file. Returns empty buckets if the file is missing or corrupt."""
    if not STATE_PATH.exists():
        return {bucket: {} for bucket in TTL_DAYS}
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {bucket: {} for bucket in TTL_DAYS}
    # ensure every bucket exists (forward-compat for new buckets)
    for bucket in TTL_DAYS:
        state.setdefault(bucket, {})
    return state


def save_state(state: dict) -> int:
    """Prune expired entries and write the state file. Returns count of pruned entries."""
    now_ms = int(time.time() * 1000)
    pruned = 0
    for bucket, days in TTL_DAYS.items():
        cutoff = now_ms - days * 86_400_000
        bucket_data = state.get(bucket, {})
        before = len(bucket_data)
        state[bucket] = {k: v for k, v in bucket_data.items() if v >= cutoff}
        pruned += before - len(state[bucket])

    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    # sort keys so the file diffs cleanly across runs
    STATE_PATH.write_text(
        json.dumps(state, indent=2, sort_keys=True, ensure_ascii=False),
        encoding="utf-8",
    )
    return pruned


def _normalize_key(bucket: str, key: str) -> str:
    """Articles get URL canonicalization; everything else stored verbatim."""
    if bucket == "articles":
        return canonicalize_url(key)
    return key


def is_seen(state: dict, bucket: str, key: str) -> bool:
    """Identity-level dedup check."""
    if bucket not in TTL_DAYS:
        raise ValueError(f"unknown dedup bucket: {bucket!r}")
    return _normalize_key(bucket, key) in state.get(bucket, {})


def mark_seen(state: dict, bucket: str, key: str) -> None:
    """Mark a key as seen with the current timestamp (ms since epoch)."""
    if bucket not in TTL_DAYS:
        raise ValueError(f"unknown dedup bucket: {bucket!r}")
    state.setdefault(bucket, {})[_normalize_key(bucket, key)] = int(time.time() * 1000)


def cluster_by_canonical_url(candidates: list[dict]) -> list[dict]:
    """Layer-3 content-level dedup.

    Each candidate is a dict that MUST have:
        - 'score' (number)        — used to pick the cluster representative
        - 'canonical_url' (str)   — the externally-referenced URL, or None for self-contained items

    Candidates with canonical_url == None are passed through unchanged
    (they don't share a referent — e.g., an X tweet with no external link).

    Candidates that share a canonical_url are collapsed into one:
      - Representative = max(score) within group
      - Rep gets +1 score per additional source, capped at +3
      - Other members become rep['endorsements']
    """
    by_url: dict[str, list[dict]] = {}
    standalone: list[dict] = []

    for c in candidates:
        url = c.get("canonical_url")
        if not url:
            standalone.append(c)
            continue
        canon = canonicalize_url(url)
        by_url.setdefault(canon, []).append(c)

    out: list[dict] = list(standalone)
    for canon, group in by_url.items():
        if len(group) == 1:
            out.append(group[0])
            continue
        rep = max(group, key=lambda c: c.get("score", 0))
        rep["score"] = rep.get("score", 0) + min(len(group) - 1, 3)
        rep["endorsements"] = [c for c in group if c is not rep]
        out.append(rep)
    return out


def stats(state: dict) -> dict:
    """Return per-bucket entry counts (for logging/audit)."""
    return {bucket: len(state.get(bucket, {})) for bucket in TTL_DAYS}
