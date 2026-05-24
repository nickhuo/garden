# WIKI.md — LLM Wiki Schema

> Schema reference for this vault. Based on the `claude-obsidian` plugin pattern
> (github.com/AgriciDaniel/claude-obsidian), which implements Andrej Karpathy's
> LLM Wiki pattern. If the plugin is installed, its skills (`wiki`, `wiki-ingest`,
> `wiki-query`, `wiki-lint`, `wiki-fold`, `save`, `autoresearch`, `canvas`,
> `defuddle`, `obsidian-markdown`, `obsidian-bases`) handle everything here
> automatically. If not, follow this file directly.

---

## What this is

A persistent, compounding wiki inside an Obsidian vault. Nick curates sources and asks questions. The LLM does all the writing, cross-referencing, filing, and maintenance.

The wiki is the product. Chat is just the interface.

Difference from RAG: the wiki is a persistent artifact. Cross-references are already there. Contradictions are flagged. Synthesis already reflects everything that was read. Knowledge compounds.

---

## Architecture

```
03_Resources/                  # vault root
├── WIKI.md                    # this file — schema reference
├── CLAUDE.md                  # project instructions (vault-specific deltas)
├── README.md                  # PARA explanation (legacy, kept for context)
├── .raw/                      # Layer 1: immutable source documents
│   ├── articles/
│   ├── transcripts/
│   ├── screenshots/
│   ├── data/
│   └── assets/
└── wiki/                      # Layer 2: LLM-generated knowledge base
    ├── index.md               # master catalog
    ├── log.md                 # chronological operations log
    ├── hot.md                 # ~500-word recent-context cache
    ├── overview.md            # executive summary of the wiki
    ├── sources/               # one summary page per ingested source
    ├── entities/              # people, orgs, products, repos, frameworks
    ├── concepts/              # ideas, patterns, frameworks
    ├── domains/               # top-level topic areas (AI-Agents, LLM, ...)
    ├── comparisons/           # side-by-side analyses
    ├── questions/             # filed answers to user queries
    ├── theses/                # Nick's evolving views (extends repo schema)
    └── meta/                  # dashboards, lint reports, conventions
```

### Rules

- `.raw/` is read-only. Never modify source files.
- `wiki/` is yours. Create, update, rename, delete freely.
- Every wiki page has frontmatter. No exceptions.
- Wikilinks over paths. Use `[[Page Name]]` not `[text](path/to/file.md)`.
- Atomic notes. One concept per page. If it covers two things, split it.
- Update, don't duplicate. If a page exists, update it.

---

## Hot Cache

`wiki/hot.md` is a ~500-word summary of the most recent context. It exists so any project pointing at this vault can get recent context without crawling the full wiki.

Update after every ingest, after any significant query, and at session end. **Overwrite completely each time** — it's a cache, not a journal.

Format:

```yaml
---
type: meta
title: "Hot Cache"
updated: 2026-05-10
---

# Recent Context

## Last Updated
2026-05-10 — <one line>

## Key Recent Facts
- <most important takeaway>
- <second most important>

## Recent Changes
- Created: [[New Page]]
- Updated: [[Existing Page]] (added X)
- Flagged: Contradiction between [[Page A]] and [[Page B]]

## Active Threads
- <what user is researching>
- <open question>
```

---

## Frontmatter Schema

Flat YAML. No nested objects (Obsidian Properties UI doesn't support them).

### Universal fields (every page)

```yaml
---
type: source | entity | concept | domain | comparison | question | overview | meta | thesis
title: "Human-Readable Title"
created: 2026-05-10
updated: 2026-05-10
tags:
  - <domain-tag>
  - <type-tag>
status: seed | developing | mature | evergreen
related:
  - "[[Other Page]]"
sources:
  - "[[.raw/articles/source-file.md]]"
---
```

### Type-specific additions

- **source**: `source_type`, `author`, `date_published`, `url`, `confidence` (high|medium|low), `key_claims` (list), `seed_score` (rubric result, e.g. `12/14`), `cited_sources` (list of `"[[Upstream Source]]"` wikilinks — the one-hop lineage; empty list allowed). See `_rubrics/source-quality.md` for the gate that sets `seed_score`/`confidence` and `CLAUDE.md` → Source-Quality Gate & Citation Lineage for how `cited_sources` is populated.
- **entity**: `entity_type` (person|organization|product|repository|place), `role`, `first_mentioned`
- **concept**: `complexity` (basic|intermediate|advanced), `domain`, `aliases` (list)
- **comparison**: `subjects` (list of wikilinks), `dimensions` (list), `verdict` (one line)
- **question**: `question` (the original query), `answer_quality` (draft|solid|definitive)
- **thesis** (vault extension): `confidence` (low|medium|high), `evidence_strength`

### Status meanings

- `seed` — page exists, has minimal content, needs development
- `developing` — actively being built out, some load-bearing content
- `mature` — comprehensive, well-sourced, ready to cite
- `evergreen` — stable, foundational, rarely needs updates

---

## Operations

### SCAFFOLD

Trigger: setting up a new vault. Already done for `03_Resources/`. See `CLAUDE.md` for vault-specific scaffolding.

### INGEST (single source)

Trigger: Nick drops a file into `.raw/` or pastes content and says "ingest [filename]" or "ingest [URL]".

1. Read the source completely.
2. **Seed gate.** Score the source against `_rubrics/source-quality.md`. **Fail → do not file; report the score card and stop for Nick's override** (see `CLAUDE.md` → Source-Quality Gate & Citation Lineage). Only continue on pass or explicit override.
3. Discuss key takeaways with Nick. Don't dump. Skip only if Nick says "just ingest it."
4. Create source summary in `wiki/sources/` (set `seed_score` + `confidence` per the rubric).
5. **One-hop citation chase.** Extract the external sources this one cites, gate each, build the passers into their own full source pages, and link them via `cited_sources` + a "## Lineage / 引用脉络" section. **One hop only — no recursion.** See `CLAUDE.md` for the protocol.
6. Create or update entity pages for every person/org/product/repo mentioned.
7. Create or update concept pages for significant ideas.
8. Update relevant domain pages.
9. Update `wiki/overview.md` if the big picture changed.
10. Update `wiki/index.md` — add entries for all new pages.
11. Update `wiki/hot.md` with this ingest's context.
12. Append to `wiki/log.md` (new entries at TOP):

   ```
   ## [2026-05-10] ingest | Source Title
   - Source: `.raw/articles/filename.md`
   - Summary: [[Source Title]]
   - Pages created: [[Page 1]], [[Page 2]]
   - Pages updated: [[Page 3]]
   - Key insight: One sentence on what is new.
   ```

13. Flag contradictions with `> [!contradiction]` callouts on both pages.

A single source typically touches 8-15 wiki pages.

### INGEST (batch)

For ≥3 sources, process serially, defer cross-references until all are in, then do a cross-reference pass, then update index/hot/log once at the end. Report at end.

For 30+ sources, check in after every 10. Anti-pattern: blindly batch-ingesting without narrating takeaways.

### QUERY

Trigger: Nick asks a non-trivial question.

1. Read `wiki/hot.md` first.
2. Read `wiki/index.md` to find relevant pages.
3. Read 3-5 of those pages.
4. Synthesize answer. Cite with wikilinks.
5. Offer to file as a wiki page in `wiki/questions/` if the answer is reusable.
6. Append to `wiki/log.md` only if the query produced wiki updates.

### SAVE

Trigger: Nick says "save this" or "/save".

1. Identify the relevant domain.
2. Create `wiki/sources/YYYY-MM-DD - chat - <slug>.md` with `source_type: chat`.
3. Treat as a new source — run INGEST steps 4-11.

### LINT

Trigger: Nick says "lint the wiki". Run every 10-20 ingests regardless.

Checks: orphan pages, dead links, stale claims (`mature` but old), missing pages for mentioned concepts, missing cross-references, frontmatter gaps, empty sections, contradictions, single-source pages with `status: mature`.

Output: `wiki/meta/lint-report-YYYY-MM-DD.md`. **Don't auto-fix without confirmation.**

### AUTORESEARCH

Trigger: Nick says "autoresearch [topic]" or "research [topic]". Requires preconfigured objectives if you want them; otherwise asks Nick what depth/sources he wants.

1. Round 1: web search, fetch top sources, **gate each candidate against `_rubrics/source-quality.md` — only gate-passing sources are filed** (save to `.raw/articles/`, summarize). Report rejected candidates and why.
2. Round 2: identify gaps, search missing angles (gate applies here too).
3. Round 3+: synthesize, resolve contradictions, file as wiki pages. **Run the one-hop citation chase on the core qualified sources** (see `CLAUDE.md`). The `max pages` budget binds — chase pages count toward it; overflow goes to Open Questions.
4. **Finalize on a branch + PR.** Autoresearch always runs on a `research/<topic-slug>` branch and **never commits to `main`**. After the final round, commit the filed pages on the branch, push it, and open a PR to `main` for Nick's review (auto-created — report the link). Don't merge; Nick reviews and merges. See `CLAUDE.md` Operations → Autoresearch for the binding rule.

**Pause after each round.** Confirm with Nick before continuing. Anti-pattern from AI-Agents/CLAUDE.md still applies: don't ingest 5 sources in one go without discussion.

### CANVAS

Use `.canvas` files for visual MOCs when entity/concept graphs get dense. Place at `wiki/<domain>/<Name>.canvas` or `wiki/meta/<Name>.canvas`. Canvases are derived views — wiki pages remain ground truth.

---

## Index and sub-indexes

### wiki/index.md

Master catalog. Sections: Domains, Entities, Concepts, Sources, Theses, Questions, Meta. Refresh on every ingest.

### wiki/<domain>/_index.md

Per-domain sub-index. Catalogs just that domain's pages.

### wiki/log.md

**Append-only.** New entries at the TOP. Format:

```
## [YYYY-MM-DD] <op> | <title>
- <1-line summary>
- pages: [[Page A]], [[Page B]]
```

Ops: `init`, `ingest`, `query`, `lint`, `refactor`, `save`, `autoresearch`, `manual`.

Quick filter: `grep "^## \[" wiki/log.md | head -10`.

---

## Anti-patterns

- Don't write to `.raw/`. Read-only.
- Don't merge multiple sources into one summary page. One source = one source page.
- Don't create entity pages for one-line mentions. Wait for ≥2 substantive mentions.
- Don't over-template pages. Karpathy's pattern is light-touch; let shape follow content.
- Don't skip `index.md` updates. The index IS the search surface.
- Don't paraphrase source claims into the wiki without citing back.
- Don't ingest 5 sources in one go without discussion.
- Don't let `hot.md` grow past ~500 words. Overwrite, don't append.
- Don't read every page in the wiki to answer a question. Read `hot.md`, `index.md`, 3-5 targeted pages, stop.

---

## References

- Plugin: github.com/AgriciDaniel/claude-obsidian
- Karpathy's pattern: gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Vault initialized from migration on 2026-05-10. See `wiki/log.md` for the init entry.
