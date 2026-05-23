"""Podcast RSS fetcher — notify-only.

Returns episode metadata (title, URL, show notes, duration, publish date)
without transcribing audio. The scoring/render layer can decide which
episodes warrant a transcript pass later.

Dedup key: RSS GUID (the <guid> element on each <item>). Most podcast
feeds set this to a stable per-episode identifier; some set it to the
audio URL — either is fine as a key.
"""
from __future__ import annotations

import re
import time
from datetime import datetime, timezone

import feedparser

from ..dedup import is_seen, mark_seen


def _to_iso(struct_time: time.struct_time | None) -> str | None:
    if not struct_time:
        return None
    try:
        return datetime(*struct_time[:6], tzinfo=timezone.utc).isoformat()
    except (TypeError, ValueError):
        return None


def _strip_html(s: str) -> str:
    if not s:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def fetch(channel: dict, source: dict, state: dict, lookback_hours: int = 336) -> list[dict]:
    """Default lookback: 14 days. Podcasts publish weekly-ish, so a 24h
    window misses most of them."""
    feed_url = channel.get("feed")
    if not feed_url:
        return []

    parsed = feedparser.parse(feed_url, agent="DigestPipeline/1.0 (+nickhuo.com)")
    if parsed.bozo and not parsed.entries:
        return []

    cutoff_ms = (time.time() - lookback_hours * 3600) * 1000
    out: list[dict] = []

    for entry in parsed.entries[:5]:  # top 5 most recent episodes is plenty
        guid = entry.get("id") or entry.get("guid") or entry.get("link")
        if not guid:
            continue

        if is_seen(state, "podcasts", guid):
            continue

        published_iso = _to_iso(entry.get("published_parsed") or entry.get("updated_parsed"))
        if published_iso:
            try:
                pub_ms = datetime.fromisoformat(published_iso.replace("Z", "+00:00")).timestamp() * 1000
                if pub_ms < cutoff_ms:
                    continue
            except ValueError:
                pass

        # itunes:duration is sometimes "MM:SS" or "HH:MM:SS" or seconds-as-string
        duration = entry.get("itunes_duration") or entry.get("duration") or ""
        show_notes = _strip_html(entry.get("summary") or entry.get("description") or "")[:1500]

        # Audio enclosure URL (where the actual mp3 lives) — useful for future Whisper pass
        audio_url = None
        for enc in entry.get("enclosures", []) or []:
            if enc.get("type", "").startswith("audio"):
                audio_url = enc.get("href") or enc.get("url")
                break

        item = {
            "kind": "podcast",
            "id": guid,
            "url": entry.get("link") or "",
            "canonical_url": None,  # podcasts don't share a referent the way articles do
            "title": (entry.get("title") or "").strip(),
            "published_at": published_iso,
            "show_notes": show_notes,
            "duration": str(duration),
            "audio_url": audio_url,
            "channel_id": channel.get("id"),
            "source_slug": source.get("slug"),
            "source_tier": source.get("tier"),
            "source_topics": source.get("topics", []),
            "source_category": source.get("category"),
        }
        mark_seen(state, "podcasts", guid)
        out.append(item)

    return out
