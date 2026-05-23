---
type: dashboard
title: "Digest — Curation Hub"
updated: 2026-05-04
---

# Digest — Curation Hub

> Daily information curation system. Three layers feed the digest pipeline:
> **Sources** (where info comes from) × **Topics** (what I care about) × **Projects** (what I'm currently doing — auto-scanned from `01_Projects/`).

---

## Interest Graph Architecture

```
┌──────────────────────────────────────────────────┐
│ Layer 1: TOPICS (explicit, in topics/)           │
│   Long-term problem-oriented interests            │
│   e.g. Evaluation, Self-improving Agent           │
├──────────────────────────────────────────────────┤
│ Layer 2: PROJECTS / AREAS (auto, from vault)     │
│   Pipeline scans 01_Projects/*/CLAUDE.md          │
│   + 01_Projects/*/README.md at runtime            │
├──────────────────────────────────────────────────┤
│ Layer 3: GOALS (from ~/CLAUDE.md)                 │
│   X / Blog / GitHub / Investment / Career         │
└──────────────────────────────────────────────────┘
              ↓ weighted relevance score
       per-article tier + follow-up actions
              ↓
   approval gate → Linear (matched project / backlog)
```

---

## 📚 Sources

![[brain/03_Resources/digest/Sources.base]]

## 🎯 Topics

![[Topics.base]]

---

## Schema References

### Source — entity-level (top of frontmatter)

A *source* is a person or organization you follow. Each source can publish through one or more *channels* (delivery points). Person-level fields stay at the top of the frontmatter; per-channel fields live inside the `channels:` array.

| Field | Values |
|---|---|
| `type` | `source` |
| `name` | Display name |
| `slug` | Filename stem (used for cross-refs and channel IDs) |
| `category` | `vc` / `ai-lab` / `builder` / `essayist` / `infra-co` / `newsletter` |
| `tier` | `1` (daily core) / `2` (low-freq) / `3` (experimental) |
| `topics` | Array of topic slugs the source produces content on |
| `related_goals` | Array — `career-ascension` / `technical-capital` / `content-output` / `influence-building` / `asset-appreciation` |
| `status` | `active` / `paused` / `archived` |
| `language`, `author`, `added`, `notes` | Self-explanatory |

### Channel — delivery-point (entries inside `channels:` array)

| Field | Values |
|---|---|
| `id` | Stable key — convention: `<source-slug>-<medium>[-<sub>]` |
| `medium` | `blog` / `x` / `podcast` / `newsletter` / `youtube` |
| `url` | Homepage / handle URL |
| `handle` | (X-only) handle without `@` |
| `feed`, `feed_verified`, `needs_scraper` | RSS/Atom config per channel |
| `last_checked`, `last_post` | Auto-written by pipeline (per-channel) |
| `notes` | Channel-specific notes (e.g. "scrape-only", "marketing-prone") |

### Topic
| Field | Values |
|---|---|
| `type` | `topic` |
| `priority` | `1` (daily focus) / `2` (tracking) / `3` (watch) |
| `keywords` | Hard-filter keywords (lowercased) |
| `anti_keywords` | Look-alikes to exclude |
| `anchors` | Author/voice whitelist — auto-promote |
| `related_projects` | `[[Wikilink]]` to project folders |
| `related_goals` | `career-ascension` / `technical-capital` / `content-output` / `influence-building` / `asset-appreciation` |
| `status` | `active` / `paused` / `archived` |

---

## How to Extend

**Add a source**: copy any `.md` in `sources/` as template (e.g. `swyx.md` for an X-only source, `paul-graham.md` for a multi-channel source). Person-level fields go up top, then a `channels:` array. Both bases auto-pick-up.
**Add a channel to an existing source**: edit the source file's `channels:` array. New channels get a `<slug>-<medium>` ID for state tracking.
**Add a topic**: copy any `.md` in `topics/` as template, set `type: topic`.
**Archive**: change `status: active` → `archived`. Item moves to Archived view.

## Pipeline Hooks (future)

- `channels[].last_checked` and `channels[].last_post` are write-targets for the digest pipeline (per-channel granularity).
- A top-level `last_post` rollup (max across channels) is *not yet written* — pipeline TODO. Until then, the "Stale 14d+" Bases view is deferred.
- A flat-mirror file `_channels_flat.md` (or `Channels.base`) is also a pipeline TODO — needed for "all my X channels sorted by last_post" queries that Bases can't do natively over the nested array.
- Topic `Action Triggers` sections are LLM prompt templates — pipeline reads them when generating follow-up suggestions.
- Linear push requires explicit approval per item (defined per topic, but gate is global).

## Recent Changes

- **2026-05-07**: Migrated to source-with-channels[] schema. Imported 23 new sources from `zarazhangrui/follow-builders` (19 X handles, 4 podcasts; 6 dropped per `interest_graph.md` Layer-4 filter; `claudeai` brand X merged into `anthropic.md`; Sequoia's Training Data podcast merged into `sequoia.md`). See `outputs/digest_integration_dryrun.md` for the per-handle scoring decisions.
