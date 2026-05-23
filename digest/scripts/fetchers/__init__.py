"""Fetchers — one per medium / source-of-data.

Each fetcher exposes:

    fetch(channel: dict, source: dict, state: dict, lookback_hours: int) -> list[dict]

Where each returned dict has at minimum:

    {
        "kind": str,              # "article" | "podcast" | "hn" | "github_trending"
        "id": str,                # bucket-natural primary key (already used to mark seen)
        "url": str,               # human-facing URL
        "canonical_url": str|None,# for Layer-3 cross-source dedup; None if self-contained
        "title": str,
        "published_at": str|None, # ISO 8601 if known
        "source_slug": str,       # set by orchestrator
        "channel_id": str,        # set by orchestrator
        # ... medium-specific extras (body_text, score, comments, stars, etc.)
    }

Fetchers are responsible for IDENTITY dedup (check seen, then mark seen).
The orchestrator runs Layer-3 content-level dedup AFTER all fetchers complete.
"""
