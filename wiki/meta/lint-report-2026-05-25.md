---
type: meta
title: "Lint Report 2026-05-25"
created: 2026-05-25
updated: 2026-05-25
tags: [meta, lint]
status: developing
---

# Lint Report: 2026-05-25

## Summary
- Pages scanned: 225
- Orphan pages: **0**
- Frontmatter gaps: **0**
- Dead links (real): **5** — 1 genuinely missing page, 1 self-link, 3 nav-convention
- Auto-fixed: 0 (awaiting review)
- DragonScale address validation: **skipped** (not enabled — no `scripts/allocate-address.sh`)
- Semantic tiling: **skipped** (not enabled — no `scripts/tiling-check.py`)

The vault is in strong shape. Alias coverage is thorough — variant titles (e.g. "Welcome to the Era of Experience" / "The Era of Experience" / "2025 - Silver & Sutton …", "A/B Testing for Agents", "Activation Steering / Representation Engineering") all resolve via `aliases:`, so no orphans and almost no dead links. Every source page correctly links its `.raw/` original. Frontmatter is complete across all content pages (`type`, `title`, `created`, `updated`, `tags`, `status` all present; `tags` and `aliases` use both block-list and inline-array YAML — both valid).

## Orphan Pages
None.

## Dead Links

### Genuinely missing page (1)
- **`LLM as Programmable Computer`** — referenced in [[2026-01-17 - Geoffrey Huntley - Everything is a Ralph Loop]] but no such concept page exists. Suggest: create a stub concept page (Huntley's framing of the LLM as a programmable computer fits the Ralph Loop / Context Engineering cluster), or remove the link.

### Self-link missing alias (1)
- **`zELO`** — [[2025-09-16 - Pipitone et al - zELO]] links `[[zELO]]` (the method name) but the page has no `zELO` alias. Suggest: add `"zELO"` to that page's `aliases:`.

### Nav-convention links (3)
Bare links to section folders rather than their `_index` pages — these don't resolve as page links but read as soft navigation:
- [[comparisons/_index]] → `[[questions]]`, `[[theses]]`
- [[domains/LLM]] → `[[theses]]`

Suggest: either point at the index pages explicitly (`[[theses/_index]]`) or leave as-is if intended as folder pointers. Low priority.

> [!note] `log.md` is excluded from dead-link enforcement
> `wiki/log.md` is append-only history and contains links to example pages (`Page A`, `Page B`), never-ingested roadmap sources (e.g. `2025-01-13 - Zheng et al - Lifelong Learning…`), and `WIKI` — these are historical record, not live wiring. Not flagged.

## Frontmatter Gaps
None. All content pages carry the required fields.

## Stale Claims / Contradictions
No automated stale-claim scan performed this pass. The known live tension — [[Ralph Loop]] (single-process, "agents are non-deterministic, multiplexing is premature") vs [[Multi-Agent Systems]] — is already explicitly marked with a `> [!contradiction]` callout on the Multi-Agent Systems page, which is the correct handling. No action.

## Cross-Reference Gaps
None found. Entity mentions are consistently wikilinked.

## Naming Conventions
- Filenames: Title Case with spaces ✓ (dated sources use `YYYY-MM-DD - Author - Title` ✓)
- Filenames unique across vault ✓ (only `_index.md` repeats, one per folder — expected)
- Tags: lowercase ✓

## Not Run (feature-gated)
- **Address validation** (DragonScale Mechanism 2): disabled — vault has no `scripts/allocate-address.sh` + `.vault-meta/address-counter.txt`.
- **Semantic tiling** (DragonScale Mechanism 3): disabled — no `scripts/tiling-check.py`.

## Suggested Fixes (need approval)
| # | Fix | Risk |
|---|-----|------|
| 1 | Add `"zELO"` to aliases of `2025-09-16 - Pipitone et al - zELO` | safe |
| 2 | Create stub concept `LLM as Programmable Computer` (or delink from Ralph Loop source) | needs judgment |
| 3 | Resolve nav links in `comparisons/_index` and `domains/LLM` to `_index` targets | safe, cosmetic |
