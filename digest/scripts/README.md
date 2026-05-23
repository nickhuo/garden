# Digest Pipeline — Fetch Layer

Pulls new content from `02_Areas/Digest/sources/*.md` channels, deduplicates
across runs, writes a flat candidates JSON for the scoring layer to consume.

## Architecture

```
sources/*.md          ─┐
  (channels[].medium)  │
                       │  fetch.py (orchestrator)
HN Algolia API        ─┼──────────────────────────►  output/candidates_<date>.json
GitHub /trending      ─┘             │
                                     ▼
                              .state/seen.json
                              (6-bucket dedup,
                               7-30 day TTLs)
```

## Install

```bash
cd 02_Areas/Digest/.scripts
pip install -r requirements.txt --break-system-packages
# Optional — only needed if you have non-RSS blogs (Sequoia, Anthropic Engineering, etc.):
npm i -g defuddle
```

## Run

```bash
# Full run
python -m scripts.fetch                # from 02_Areas/Digest/

# Or directly
python 02_Areas/Digest/.scripts/fetch.py

# Dry run — no writes to state or output
python -m scripts.fetch --dry-run

# Subset
python -m scripts.fetch --no-github
python -m scripts.fetch --only blog
python -m scripts.fetch --only hn
```

## What it does, what it doesn't

**Does:**

- Reads each `sources/*.md` with `status: active`, walks `channels[]`
- For `medium: blog` channels: RSS via `feedparser` if `feed_verified: true`, else Defuddle scrape
- For `medium: podcast` channels: RSS metadata only — title, URL, show notes, duration. **No transcription.**
- Pulls HN stories with points > 50 in the last 24h
- Scrapes GitHub /trending across `all`, `python`, `typescript`, `go`, `rust`
- **Identity dedup**: per-bucket primary keys (URL canonicalized for articles, GUID for podcasts, story ID for HN, `owner/repo` for GitHub)
- **Cross-source dedup**: collapses candidates that share a `canonical_url` — picks the highest-scoring representative, demotes the rest to `endorsements`. So if HN, Anthropic blog, and 2 X accounts all link to the same article, you see it once with footnotes.
- TTL prunes the state file at every save (7d for tweets/articles/HN/GH-trending, 30d for podcasts/youtube)

**Doesn't:**

- Score candidates against `interest_graph.md` — that's the scoring layer's job
- Render the digest markdown — separate task
- Push to Linear — separate task
- Fetch X / Twitter — disabled by user
- Fetch YouTube — disabled by user
- Transcribe podcasts — deferred (Phase 2)

## Output schema

```json
{
  "generated_at": 1715040000000,
  "source_count": 37,
  "channel_count": 39,
  "raw_candidate_count": 87,
  "deduped_candidate_count": 71,
  "candidates": [
    {
      "kind": "article" | "podcast" | "hn" | "github_trending",
      "id": "...",
      "url": "...",
      "canonical_url": "...",
      "title": "...",
      "published_at": "2026-05-07T12:34:56+00:00",
      "source_slug": "anthropic" | "_hn" | "_github_trending",
      "channel_id": "anthropic-news",
      "source_tier": 1 | 2 | 3,
      "source_topics": [...],
      "source_category": "ai-lab" | "vc" | ... | "aggregator",
      "endorsements": [...]    // present only if cluster_by_canonical_url merged duplicates
    }
  ]
}
```

## Adding a scraped blog

Two steps:

1. Make sure the source `.md` has `feed_verified: false` and `needs_scraper: true` on the relevant channel.
2. Add a per-source URL pattern to `fetchers/blog_scrape.py` → `PER_SOURCE` table:

```python
PER_SOURCE = {
    "your-source-slug": {
        "your-channel-id": {
            "article_url_pattern": r"^https://example\.com/blog/[^/]+/?$",
        },
    },
}
```

The pattern is the regex that matches a final article URL (not the index URL). Without it, the scraper tries to keep all internal links from the index — usually too noisy.

## Failure modes worth knowing

- **`feedparser.bozo == True`**: the feed has parse errors but might still have entries. The fetcher accepts this if entries exist; only bails if both are bad.
- **Defuddle CLI missing**: `blog_scrape.fetch()` returns `[]` silently. Check with `which defuddle`. Install with `npm i -g defuddle`.
- **GitHub /trending markup change**: the scraper uses regex against article-card HTML. If GH restructures, expect zero results from `github_trending.fetch()`. Open the page in a browser, inspect the new selectors, update `_REPO_BLOCK` / `_HREF` / `_DESC` / `_STARS_TODAY` regexes.
- **HN Algolia rate limiting**: not documented but real. The fetcher uses `urllib` with a 15s timeout; if rate-limited it returns `[]` silently. Re-run later.
- **State file corruption**: `load_state()` returns empty buckets if the file fails to parse. You'll see one day of duplicates, then it self-heals.

## State file layout

`02_Areas/Digest/.state/seen.json`:

```json
{
  "tweets":          {},  // not currently populated (X disabled)
  "articles":        { "https://anthropic.com/news/foo": 1715040000000 },
  "podcasts":        { "<rss-guid>": 1715040000000 },
  "youtube":         {},  // not currently populated (YouTube disabled)
  "hn":              { "48023496": 1715040000000 },
  "github_trending": { "owner/repo": 1715040000000 }
}
```

Values are unix timestamps in milliseconds. TTL pruning runs at every save. Safe to commit; the file is small (<50KB at typical scale) and provides a recoverable digest history.
