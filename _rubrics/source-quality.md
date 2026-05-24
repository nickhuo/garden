# Source-Quality Rubric (Seed Gate)

> **Status: DRAFT — Nick-editable.** The dimensions, weights, and threshold below are a
> starting point. Refine them directly or by telling Claude in chat. This file is the single
> source of truth for the seed gate; `CLAUDE.md` and `WIKI.md` point here.

## Purpose

This rubric is the **gate** every candidate source must pass before it becomes a wiki page.
It runs in **both** operations:

- **Ingest** — on the material Nick supplies.
- **Autoresearch** — on every candidate source the web search surfaces.
- **Citation chase** — on each upstream source reached one hop out from a qualified source.

**Behavior on failure: block and report.** A source that fails the gate is **not** filed.
Claude reports the score, the per-dimension breakdown, the specific reasons it fell short, and
concrete suggestions (e.g. "this is secondary — its primary source appears to be X; chase that
instead?"). Nick may **override**; an overridden source is filed with `confidence: low` and a
`> [!gap]` quality-caveat callout on the page.

This rubric **supersedes** `program.md`'s confidence / source-preference rules wherever they differ.

---

## Scoring dimensions

Score each dimension **0 / 1 / 2**. Total out of **14**.

| # | Dimension | 0 | 1 | 2 |
|---|-----------|---|---|---|
| 1 | **Primacy** | Pure aggregation / link roundup | Secondary commentary on a primary source | Primary / first-hand: original research, direct author, official announcement, primary doc |
| 2 | **Authority** | Anonymous / no domain standing | Identifiable but unproven | Recognized, credible author/org in the domain |
| 3 | **Verifiability** | No evidence, unfalsifiable claims | Some evidence, partially checkable | Cites data/methods; claims independently checkable |
| 4 | **Information gain** | Rehashes well-known material | Some new framing | Substantive novel signal |
| 5 | **Depth & specificity** | Vague, hand-wavy | Mixed detail | Concrete mechanisms, numbers, specifics |
| 6 | **Recency / durability** | Stale & not foundational | Aging but relevant | Recent (≤2 yr) **or** foundational/evergreen |
| 7 | **Citation hygiene** | Cites nothing | Cites loosely / unnamed | Cites named sources (also enables the citation chase) |

---

## Pass threshold (draft)

A source **qualifies as a seed** when **both** hold:

1. **Total ≥ 9 / 14**, AND
2. **Primacy (dim 1) ≥ 1** — a pure aggregator (Primacy 0) cannot qualify on volume alone.

### Hard rejects (never a seed, regardless of total)

- Undated web pages.
- Social-media / forum posts (Reddit, X, HN comments). These may serve as **pointers** to a
  primary source — chase the primary, don't seed the post.
- Sources that cite nothing **and** present unverifiable claims (dim 3 = 0 **and** dim 7 = 0).

---

## Score → `confidence` mapping

Keep the existing `confidence` frontmatter field consistent with the rubric:

| Outcome | `confidence` |
|---------|--------------|
| Qualified, total ≥ 12 | `high` |
| Qualified, total 9–11 | `medium` |
| Filed via override (failed gate) | `low` + `> [!gap]` caveat |

Record the numeric result in `seed_score` (e.g. `12/14`).
