"""Digest fetch orchestrator.

Reads `02_Areas/Digest/sources/*.md`, walks each source's channels[],
dispatches to the right fetcher per medium, runs Layer-3 cross-source
content dedup, and writes a candidate JSON file under `output/`.

Usage:
    python -m scripts.fetch                # full run
    python -m scripts.fetch --dry-run      # don't write state, don't write output
    python -m scripts.fetch --no-hn        # skip HN
    python -m scripts.fetch --no-github    # skip GitHub Trending
    python -m scripts.fetch --only blog    # only run blog fetchers (rss + scrape)

Output:
    02_Areas/Digest/output/candidates_<YYYY-MM-DD>.json
    02_Areas/Digest/.state/seen.json (updated)

The output JSON is the input to the scoring/render layer (separate task).
This script does NOT score, NOT render, NOT push to Linear.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import date
from pathlib import Path
from typing import Any

# Allow `python -m scripts.fetch` from .scripts/ parent dir; also allow
# direct `python fetch.py` from .scripts/.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from scripts.dedup import load_state, save_state, cluster_by_canonical_url, stats
    from scripts.fetchers import blog_rss, blog_scrape, podcast_rss, hn, github_trending
else:
    from .dedup import load_state, save_state, cluster_by_canonical_url, stats
    from .fetchers import blog_rss, blog_scrape, podcast_rss, hn, github_trending


SCRIPT_DIR = Path(__file__).resolve().parent
DIGEST_DIR = SCRIPT_DIR.parent
SOURCES_DIR = DIGEST_DIR / "sources"
OUTPUT_DIR = DIGEST_DIR / "output"


# -- frontmatter parsing ------------------------------------------------------
# Hand-rolled: PyYAML reformats nested arrays in ways that mutate Nick's hand-
# tuned style. Since these files are produced by us (with a known schema), a
# minimal parser is fine and avoids the reformatting surprise.

import re


def _coerce(raw: str) -> Any:
    raw = raw.strip()
    if raw == "":
        return None
    if raw.lower() == "true":
        return True
    if raw.lower() == "false":
        return False
    if raw.startswith('"') and raw.endswith('"'):
        return raw[1:-1]
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [s.strip().strip('"') for s in inner.split(",")]
    try:
        return int(raw)
    except ValueError:
        try:
            return float(raw)
        except ValueError:
            return raw


def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fm_text = text[4:end]

    fm: dict[str, Any] = {}
    current_list: list[dict] | None = None
    current_item: dict | None = None

    for line in fm_text.splitlines():
        stripped = line.rstrip()
        if not stripped or stripped.lstrip().startswith("#"):
            continue

        # detect "channels:" list start
        if re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*):\s*$", stripped):
            key = stripped.split(":")[0]
            if key == "channels":
                fm[key] = []
                current_list = fm[key]
                current_item = None
                continue
            else:
                fm[key] = None
                current_list = None
                continue

        # list item start: "  - id: foo" or "  - key: val"
        m_item = re.match(r"^\s+-\s+([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$", line)
        if m_item and current_list is not None:
            current_item = {m_item.group(1): _coerce(m_item.group(2))}
            current_list.append(current_item)
            continue

        # list item continuation: "    key: val" (4-space indent under list item)
        m_cont = re.match(r"^\s{4,}([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$", line)
        if m_cont and current_item is not None:
            current_item[m_cont.group(1)] = _coerce(m_cont.group(2))
            continue

        # top-level key
        m_top = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$", line)
        if m_top:
            fm[m_top.group(1)] = _coerce(m_top.group(2))
            current_list = None
            current_item = None

    return fm


def load_active_sources() -> list[dict]:
    out = []
    for path in sorted(SOURCES_DIR.glob("*.md")):
        try:
            fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  ! failed to parse {path.name}: {e}", file=sys.stderr)
            continue
        if not fm:
            continue
        if fm.get("type") != "source":
            continue
        if fm.get("status") != "active":
            continue
        if not fm.get("channels"):
            continue
        fm["_path"] = path  # so the orchestrator can write back feed_verified
        out.append(fm)
    return out


# -- per-source dispatch ------------------------------------------------------

# Fills with (source_path, channel_id) pairs whose feed probed "ok" on this run.
# Used by --update-verified to flip feed_verified=true on disk in one batch.
_NEWLY_VERIFIED: list[tuple[Path, str]] = []


def fetch_for_channel(channel: dict, source: dict, state: dict, allowed_kinds: set[str]) -> list[dict]:
    medium = channel.get("medium")

    if medium == "blog":
        if "blog" not in allowed_kinds:
            return []

        feed_url = channel.get("feed")
        feed_verified = bool(channel.get("feed_verified"))
        needs_scraper = bool(channel.get("needs_scraper"))

        # Strategy:
        # 1. If channel has a feed URL AND not explicitly flagged as scraper-only:
        #    probe RSS. If "ok"/"empty" → use RSS. If "broken" → fall back to scrape.
        # 2. Track newly-verified channels for the optional --update-verified write-back.
        if feed_url and not needs_scraper:
            probe_result = blog_rss.probe(feed_url)
            if probe_result in ("ok", "empty"):
                if not feed_verified:
                    _NEWLY_VERIFIED.append((source.get("_path"), channel.get("id"), probe_result))
                return blog_rss.fetch(channel, source, state)
            # broken — fall through to scrape

        return blog_scrape.fetch(channel, source, state)

    if medium == "podcast":
        if "podcast" not in allowed_kinds:
            return []
        return podcast_rss.fetch(channel, source, state)

    if medium in ("x", "youtube", "newsletter"):
        # explicitly disabled per user
        return []

    return []


# -- write-back: flip feed_verified=true on disk for newly-verified channels --

_CHANNEL_BLOCK_RE = re.compile(
    r"(  - id:\s*[^\n]+\n(?:    [^\n]+\n)*)",
    re.MULTILINE,
)


def update_feed_verified(source_path: Path, channel_id: str) -> bool:
    """Set feed_verified: true for the named channel inside a source .md.

    Returns True if a change was written, False if nothing changed
    (channel not found, or already verified).
    """
    if source_path is None or channel_id is None:
        return False

    text = source_path.read_text(encoding="utf-8")

    def _replace(m: re.Match) -> str:
        block = m.group(0)
        id_line = re.search(r"  - id:\s*(\S.*?)\s*$", block, re.MULTILINE)
        if not id_line or id_line.group(1) != channel_id:
            return block
        new_block, n = re.subn(
            r"^(    feed_verified:\s*)(false|False)\s*$",
            r"\1true",
            block,
            count=1,
            flags=re.MULTILINE,
        )
        return new_block if n else block

    new_text = _CHANNEL_BLOCK_RE.sub(_replace, text)
    if new_text == text:
        return False
    source_path.write_text(new_text, encoding="utf-8")
    return True


# -- main ---------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true",
                   help="don't write state or output JSON")
    p.add_argument("--no-hn", action="store_true")
    p.add_argument("--no-github", action="store_true")
    p.add_argument("--only", choices=["blog", "podcast", "hn", "github"],
                   help="run only one fetcher kind")
    p.add_argument("--update-verified", action="store_true",
                   help="after a successful RSS probe, write feed_verified=true back to the source .md file")
    args = p.parse_args()

    if args.only:
        allowed = {args.only}
    else:
        allowed = {"blog", "podcast"} | (set() if args.no_hn else {"hn"}) | (set() if args.no_github else {"github"})

    state = load_state()
    print(f"State loaded: {stats(state)}")

    candidates: list[dict] = []
    sources = load_active_sources()
    print(f"Active sources: {len(sources)}")

    # Per-source fetchers (blog + podcast)
    n_channels = 0
    n_results = 0
    for src in sources:
        for ch in src.get("channels", []):
            n_channels += 1
            try:
                items = fetch_for_channel(ch, src, state, allowed)
            except Exception as e:
                print(f"  ! {src.get('slug')}/{ch.get('id')}: {type(e).__name__}: {e}", file=sys.stderr)
                continue
            if items:
                print(f"  + {src.get('slug'):28s} {ch.get('id'):40s}  {len(items)} new")
                n_results += len(items)
            candidates.extend(items)

    # Source-agnostic fetchers
    if "hn" in allowed:
        try:
            hn_items = hn.fetch(state)
            print(f"  + HN: {len(hn_items)} stories with points>50 in last 24h")
            candidates.extend(hn_items)
        except Exception as e:
            print(f"  ! HN: {type(e).__name__}: {e}", file=sys.stderr)

    if "github" in allowed:
        try:
            gh_items = github_trending.fetch(state)
            print(f"  + GitHub Trending: {len(gh_items)} repos")
            candidates.extend(gh_items)
        except Exception as e:
            print(f"  ! GitHub Trending: {type(e).__name__}: {e}", file=sys.stderr)

    print(f"\nTotal raw candidates: {len(candidates)}")

    # Layer-3 cross-source content dedup
    before = len(candidates)
    candidates = cluster_by_canonical_url(candidates)
    after = len(candidates)
    if before != after:
        print(f"After cross-source clustering: {after} (collapsed {before - after} duplicates by canonical URL)")
    else:
        print(f"After cross-source clustering: {after} (no clusters formed)")

    # Report newly-verified channels (probed "ok"/"empty" but feed_verified was false on disk)
    if _NEWLY_VERIFIED:
        print(f"\nNewly-verifiable channels ({len(_NEWLY_VERIFIED)}):")
        for path, ch_id, probe_result in _NEWLY_VERIFIED:
            slug = path.stem if path else "?"
            print(f"  - {slug:28s} {ch_id:40s}  probe={probe_result}")
        if args.update_verified and not args.dry_run:
            n_written = 0
            for path, ch_id, _ in _NEWLY_VERIFIED:
                if update_feed_verified(path, ch_id):
                    n_written += 1
            print(f"  → wrote feed_verified=true to {n_written} source file(s)")
        elif not args.update_verified:
            print("  (not writing — pass --update-verified to flip these on disk)")

    if args.dry_run:
        print("\n[dry-run] state and output NOT written.")
        return 0

    # Write candidates JSON
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"candidates_{date.today().isoformat()}.json"
    out_path.write_text(
        json.dumps({
            "generated_at": int(time.time() * 1000),
            "source_count": len(sources),
            "channel_count": n_channels,
            "raw_candidate_count": before,
            "deduped_candidate_count": after,
            "candidates": candidates,
        }, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )

    pruned = save_state(state)
    print(f"\nWrote {out_path.relative_to(DIGEST_DIR)}")
    print(f"State saved (pruned {pruned} expired entries): {stats(state)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
