---
type: meta
title: "Lint Report 2026-05-22"
created: 2026-05-22
updated: 2026-05-22
tags: [meta, lint]
status: developing
---

# Lint Report: 2026-05-22

## Summary
- Pages scanned: **184**
- YAML / frontmatter errors: **0**
- Orphan pages: **1**
- Dead links (real): **20 targets** → 16 alias-fixable, 4 genuinely missing
- Frontmatter gaps: **0**
- Empty (leaf) sections: **0**
- Address validation: **skipped** (DragonScale not enabled)
- Semantic tiling: **skipped** (`scripts/tiling-check.py` not present / ollama not configured)

> Note: an earlier raw pass reported 222 "dead links" and 116 "empty sections" — almost all were false positives. The wiki resolves source links through `aliases` (134 aliases across 65 pages), and H1-title→H2 layouts are not empty sections. Numbers below are alias-aware and deduped.

---

## Orphan Pages (1)
- `questions/how-to-ensure-agent-reliability` — no inbound links **resolve**. It *is* referenced as `[[How to Ensure Agent Reliability]]` from `index.md` and `log.md`, but those links are dead because the file has no matching alias. **Fix = add alias `How to Ensure Agent Reliability`** → resolves orphan + 2 dead links at once.

---

## Dead Links — Group A: missing alias on an existing page (16)
The target file exists; the link uses a clean title but the file is date-prefixed and lacks the alias. **Safe auto-fix: add the alias.**

| Dead link | Existing file to alias |
|---|---|
| `[[Defeating Nondeterminism in LLM Inference]]`, `[[Defeating Nondeterminism]]` | `2025-09-10 - He - Defeating Nondeterminism in LLM Inference.md` |
| `[[Interaction Models]]` | `2026-05-11 - Thinking Machines - Interaction Models.md` |
| `[[Code Execution with MCP]]` | `2026-05-13 - Anthropic - Code Execution with MCP.md` |
| `[[Modular Manifolds]]` | `2025-09-26 - Bernstein - Modular Manifolds.md` |
| `[[LoRA Without Regret]]` | `2025-09-29 - Schulman - LoRA Without Regret.md` |
| `[[Harness Design Long Running Apps]]` | `2025-10-01 - Anthropic - Harness Design Long Running Apps.md` |
| `[[Demystifying evals for AI agents]]` | `2026-05-13 - Anthropic - Demystifying Evals for AI Agents.md` |
| `[[AI-Resistant Technical Evaluations]]` | `2026-01-21 - Anthropic - AI-Resistant Technical Evaluations.md` |
| `[[Eval Awareness BrowseComp]]` | `2026-05-13 - Anthropic - Eval Awareness BrowseComp.md` |
| `[[Infrastructure Noise Agentic Coding Evals]]` | `2026-02-05 - Anthropic - Infrastructure Noise Agentic Coding Evals.md` |
| `[[Effective Harnesses for Long-Running Agents]]` | `2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents.md` |
| `[[Claude Code Auto Mode]]` | `2026-04 - Anthropic - Claude Code Auto Mode.md` |
| `[[Claude Code Sandboxing]]` | `2026-05-13 - Anthropic - Claude Code Sandboxing.md` |
| `[[Claude Code Best Practices]]` | `2026-05-13 - Anthropic - Claude Code Best Practices.md` |
| `[[How to Ensure Agent Reliability]]` | `questions/how-to-ensure-agent-reliability.md` |

## Dead Links — Group B: genuinely missing pages (4) — needs review
No file or alias exists. These look like recurring codenames/entities. Decide: create a stub, or remove the link.

- `Compass` (×8) — cited in `Reward Modeling`, `Online Evaluation`, `Eval Validity`, `LLM-as-Judge`. Looks like an eval product/codename.
- `Beckman` (×4) — cited in `Online Evaluation`, `Eval Validity`, `LLM-as-Judge` + a source. Related to thesis *Interpretable Persona Vectors – the Beckman Pattern*; likely a person/entity worth a page.
- `Donut` (×3) — cited in `Implicit Feedback Signals`, `Online Evaluation`, `A-B Testing for Agents`. Eval codename?
- `Voyager` (×1) — cited in `Cognitive Architectures for Language Agents` source. The Voyager Minecraft-agent paper; candidate entity/source page.

## Dead Links — ignored (example/template noise, 11)
Appear only inside `log.md` history or `meta/lint-2026-05-13.md` examples: `[[Page A]]`, `[[Page B]]`, `[[wikilink]]`, `[[source-page-name]]`, `[[WIKI]]`, `[[theses]]`, `[[Overview]]`, `[[Building C Compiler with Parallel Claudes]]`, and three roadmap titles in `log.md`. No action.

---

## Frontmatter Gaps (0)
All non-structural pages have `type`, `status`, `created`, `updated`, `tags`. (Source-page schema issues were fixed in the prior session: 2 YAML errors, 4 missing `status`, date normalizations, noise tags, 6 duplicate files removed.)

## Empty Sections (0)
No leaf heading lacks content.

## Stale Index Entries
None pointing to deleted/renamed pages. `sources/_index.md` links several clean titles that currently resolve only after Group A aliases are added.

---

## Resolution (applied 2026-05-22)
- **Group A — done.** Added `aliases` to all 15 target files (16 link variants). Re-scan: **0 real dead links remaining.** This also resolved the `how-to-ensure-agent-reliability` orphan.
- **Group B — done.** Unlinked `[[Compass]]` (8 files), `[[Beckman]]` (5), `[[Donut]]` (4), `[[Voyager]]` (2) → converted to plain text per decision.
- **New finding — `entities/Anthropic.md` is orphaned.** No page links `[[Anthropic]]`; sources cite Anthropic only via the `author:` field, never a wikilink. Pre-existing (the first pass miscredited it). Suggested fix: link it from `domains/AI-Agents.md` / `domains/LLM.md` or `entities/_index.md`. **Left for review.**
