"""GitHub Trending fetcher — scrapes github.com/trending HTML.

Source-agnostic, like the HN fetcher. There's no official API for /trending,
so we parse the page. This is fragile — GitHub does occasionally restructure
the trending page markup. Budget ~30 min/quarter to fix selectors when it breaks.

Dedup key: "owner/repo" with a 7-day TTL. A repo trending Mon-Fri this week
shows once on Mon. Next month if it re-trends, the entry has expired and it
shows again — that's intentional, re-trending is a real signal.
"""
from __future__ import annotations

import re
import urllib.request
import urllib.error
from html import unescape

from ..dedup import is_seen, mark_seen


# Languages worth scraping. The all-languages page goes first so we catch
# polyglot repos; per-language pages catch repos that wouldn't crack the global list.
LANGUAGES = ["", "python", "typescript", "go", "rust"]


def _fetch_html(language: str = "") -> str:
    url = f"https://github.com/trending/{language}" if language else "https://github.com/trending"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; DigestPipeline/1.0)",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, OSError):
        return ""


# Each repo card on the trending page looks roughly like:
#   <article class="Box-row">
#     <h2 class="h3 lh-condensed">
#       <a href="/owner/repo">owner / repo</a>
#     </h2>
#     <p class="col-9 color-fg-muted my-1 pr-4">{description}</p>
#     <a href="/owner/repo/stargazers">{stars}</a>
#     <span class="d-inline-block float-sm-right">
#       <svg ...><use href="#icon-star"></use></svg>{stars-today} stars today
#     </span>
#   </article>
#
# We pull just the data we need with regex — no BeautifulSoup dep.
_REPO_BLOCK = re.compile(r'<article class="Box-row">(.*?)</article>', re.DOTALL)
_HREF = re.compile(r'<h2[^>]*>\s*<a[^>]+href="/([^"]+)"', re.DOTALL)
_DESC = re.compile(r'<p class="col-9[^"]*">(.*?)</p>', re.DOTALL)
_STARS_TODAY = re.compile(r'>\s*([\d,]+)\s+stars?\s+today\s*<')
_LANG_TAG = re.compile(r'itemprop="programmingLanguage"[^>]*>\s*([^<]+)<')


def _parse_repos(html: str) -> list[dict]:
    repos = []
    for block in _REPO_BLOCK.findall(html):
        m_href = _HREF.search(block)
        if not m_href:
            continue
        slug = m_href.group(1).strip()
        # slug looks like "owner/repo" — discard if it's not exactly that shape
        if slug.count("/") != 1:
            continue

        m_desc = _DESC.search(block)
        desc = unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m_desc.group(1)))).strip() if m_desc else ""

        m_stars = _STARS_TODAY.search(block)
        stars_today = int(m_stars.group(1).replace(",", "")) if m_stars else 0

        m_lang = _LANG_TAG.search(block)
        lang = m_lang.group(1).strip() if m_lang else None

        repos.append({
            "slug": slug,  # "owner/repo"
            "url": f"https://github.com/{slug}",
            "description": desc,
            "stars_today": stars_today,
            "language": lang,
        })
    return repos


def fetch(state: dict) -> list[dict]:
    """Pull trending repos across configured languages, dedup by `owner/repo`."""
    seen_in_run: set[str] = set()
    out: list[dict] = []

    for lang in LANGUAGES:
        html = _fetch_html(lang)
        if not html:
            continue
        for repo in _parse_repos(html):
            slug = repo["slug"]
            if slug in seen_in_run:
                continue  # within one run, don't add the same repo from two language pages
            seen_in_run.add(slug)

            if is_seen(state, "github_trending", slug):
                continue

            owner, name = slug.split("/", 1)
            item = {
                "kind": "github_trending",
                "id": slug,
                "url": repo["url"],
                "canonical_url": repo["url"],
                "title": f"{owner}/{name}",
                "owner": owner,
                "name": name,
                "description": repo["description"],
                "stars_today": repo["stars_today"],
                "language": repo["language"],
                "trending_in": lang or "all",
                "published_at": None,
                "source_slug": "_github_trending",
                "source_category": "aggregator",
                "channel_id": "_github_trending",
            }
            mark_seen(state, "github_trending", slug)
            out.append(item)

    return out
