---
type: meta
title: "Wiki Log"
updated: 2026-05-19
---

# Wiki Log

Append-only. **New entries at the TOP.** One block per operation.

Format:
```
## [YYYY-MM-DD] <op> | <title>
- <1-line summary>
- pages: [[Page A]], [[Page B]]
```

Ops: `init`, `ingest`, `query`, `lint`, `refactor`, `save`, `autoresearch`, `manual`.

---

## [2026-05-19] ingest | Packer et al — MemGPT: Towards LLMs as Operating Systems
- Source: `.raw/pdfs/memgpt-llms-as-operating-systems-2310.08560.pdf` (downloaded; PDF kept locally)
- Summary: [[2023-10-12 - Packer et al - MemGPT - LLMs as Operating Systems]]
- Pages created: [[MemGPT]], [[Self-Editing Memory]]
- Pages updated: [[index]], [[hot]], [[AI-Agents]], [[Agent Memory Taxonomy]]
- Key insight: Context window = RAM. "Virtual context management" pages data between an in-context tier (working context + FIFO queue) and external storage (recall + archival) under the model's own control via function calls. Pairs with [[CoALA]]: MemGPT is the concrete mechanism for the working↔long-term boundary CoALA names; its memory-edit calls are CoALA *learning* actions, its event loop the *decision cycle*. Became the Letta framework.

## [2026-05-19] ingest | Sumers et al — Cognitive Architectures for Language Agents (CoALA)
- Source: `.raw/pdfs/cognitive-architectures-language-agents-2309.02427.pdf` (downloaded; PDF kept locally)
- Summary: [[2023-09-05 - Sumers et al - Cognitive Architectures for Language Agents]]
- Pages created: [[CoALA]], [[Agent Memory Taxonomy]], [[ReAct]], [[Tree of Thoughts]], [[Shunyu Yao]]
- Pages updated: [[index]], [[hot]], [[AI-Agents]]
- Key insight: First academic-framework source. Imports cognitive-architecture theory (Soar/ACT-R) to organize agents on three axes — memory (working/episodic/semantic/procedural), action space (internal vs external grounding), decision cycle (propose→evaluate→select). Gives a principled home for scattered operational concepts; the empty cells (agents that learn their own decision procedures) are the research frontier.

## [2026-05-19] manual | New thesis — Runtime vs Structural Reliability

- **Trigger:** wiki-query on four-pillar interview framing surfaced strong coverage on agent reliability; promoted the "runtime + structural" framing to a thesis page.
- **Page created:** [[Runtime vs Structural Reliability]]. confidence: medium, evidence: moderate.
- **Anchor sources:** [[2026-05-13 - Anthropic - Postmortem Three Recent Issues]] (three structural root causes), [[2026-05-13 - Anthropic - Claude Code Sandboxing]], [[2026-05-14 - Anthropic - Claude Code in Large Codebases]] ("harness > model"), [[2026-05-13 - Anthropic - Claude Code Best Practices]].
- **Stance:** structural-first allocation heuristic. Runtime checks are defense-in-depth, not primary defense. Operational test: "would one more runtime check have *prevented* this or only *detected* it sooner?"
- **Index:** theses 2→3.
- **Open follow-ups:** prompt-injection counterclaim needs a dedicated source ingest; judge-everything camp needs steelmanning from agent-eval vendor writeups.

---

## [2026-05-18] save | Anthropic — Claude Code in Large Codebases

- **Trigger:** user `/save` with URL to Anthropic Applied AI blog post (published 2026-05-14).
- **Source created:** [[2026-05-14 - Anthropic - Claude Code in Large Codebases]]. Raw filed at `.raw/articles/2026-05-14 - Anthropic - Claude Code in Large Codebases.md`.
- **Frame:** companion / scale-out to [[2026-05-13 - Anthropic - Claude Code Best Practices]]. Earlier post = how to use Claude Code; this one = what changes at enterprise scale.
- **Two through-lines:** (1) agentic search beats RAG in active codebases because embedding pipelines silently go stale; (2) the harness (CLAUDE.md, hooks, skills, plugins, MCP, LSP, subagents) determines performance more than the model.
- **Non-obvious claim flagged:** stop hooks proposing CLAUDE.md updates while context is warm is the high-leverage hook pattern — instance of [[Meta-Harness]]. Concept page candidate pending second-source corroboration.
- **Reinforces:** [[Harness Staleness]] with a concrete 3-6 month review cadence + the Perforce `p4 edit` hook example of compensations that became dead weight after native support landed.
- **Updated:** `wiki/index.md` (sources 31→32), `wiki/hot.md`.

## [2026-05-14] ingest | Thinking Machines Lab batch (5 posts) — seeded [[LLM]] domain

- **Trigger:** user `/save` with 5 TML Connectionism URLs (Sep 2025 – May 2026).
- **First sources in the [[LLM]] domain.** Created `wiki/domains/LLM.md`.
- **Sources created (5):** [[2026-05-11 - Thinking Machines - Interaction Models]], [[2025-10-27 - Lu - On-Policy Distillation]], [[2025-09-29 - Schulman - LoRA Without Regret]], [[2025-09-26 - Bernstein - Modular Manifolds]], [[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]]
- **Entities created (5):** [[Thinking Machines Lab]], [[John Schulman]], [[Horace He]], [[Kevin Lu]], [[Jeremy Bernstein]]
- **Concepts created (11):** [[On-Policy Distillation]], [[LoRA]], [[Batch Invariance]], [[Floating-Point Non-Associativity]], [[Reverse KL Divergence]], [[Trainer-Sampler Determinism]], [[Manifold Optimization]], [[Stiefel Manifold]], [[Manifold Muon]], [[Interaction Model Architecture]], [[Empirical Neural Tangent Kernel]]
- **Updated:** `wiki/index.md` (20 entities, 67 concepts, 31 sources, LLM listed as active domain), `wiki/hot.md` (full overwrite).
- **Key insight:** Three of TML's five posts interlock — [[Defeating Nondeterminism in LLM Inference]] is the infrastructure layer that makes [[On-Policy Distillation]]'s reverse-KL signal clean and enables [[Interaction Models]]' <5% trainer-sampler alignment claim. Domain-level thesis candidate ("co-design architecture and optimizer") deferred until second-source confirmation outside TML.

## [2026-05-13] refactor | Fix-all from lint report

- Trigger: user said "fix all" after the lint report. Dispatched 5 parallel agents + handled mechanical fixes inline.
- **Aliases added** to 4 high-traffic source pages — resolves 87 short-form dead links: [[2024-12-19 - Anthropic - Building Effective Agents]] (`Building Effective Agents`), [[2026-04-08 - Anthropic - Scaling Managed Agents]] (`Scaling Managed Agents`), [[2025-06-13 - Anthropic - How we built our multi-agent research system]], [[2025-09-29 - Anthropic - Effective context engineering for AI agents]], plus [[2025-11-24 - Anthropic - Advanced Tool Use]] (`Advanced Tool Use`).
- **Source `sources:` backfill** — 8 truly empty + 15 already populated = 26/26 source pages now link to their `.raw/articles/` raw file.
- **Legacy `sources:` backfill** — 30 pages with `_legacy_source_count > 0` had `sources:` populated from body wikilinks (90 source links added total; `_legacy_source_count` preserved as audit). 18 pages had `found > legacy` — they had picked up new citations post-migration.
- **Date corrections (6 files renamed + 1 frontmatter-only):** [[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]] (was 2026-05-13), [[2025-03-20 - Anthropic - The Think Tool]] (was 2026-05-13), [[2026-01-21 - Anthropic - AI-Resistant Technical Evaluations]] (was year-only), [[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]], [[2026-02-05 - Anthropic - Infrastructure Noise Agentic Coding Evals]], [[2025-06-26 - Anthropic - Desktop Extensions]]. Building Effective Agents date_published fixed in frontmatter (2026-05-04 → 2024-12-19). 82 wikilinks updated across 31 files.
- **Titles fixed** on 8 source pages — replaced filename-style titles with real published article titles (e.g., "Anthropic - Building Effective Agents" → "Building effective agents").
- **Indexes reconciled:** `sources/_index.md` rebuilt (26 sources, 23 Anthropic count, removed misfiled `[[Pass^k Reliability Metric]]`, refreshed coverage-gaps). `concepts/_index.md` rebuilt (55 concepts, added new Harness/Safety/Retrieval sections, moved Meta-Harness out of Evaluation). `index.md` updated with new date-prefixed links.
- **Domain page** `domains/AI-Agents.md` refreshed — count "11 sources" → "26 sources"; 13 new sources woven into Foundation list; 25 new concepts woven into working taxonomy; 2 stale `[[brain/03_Resources/AI-Agents/index]]` dead links replaced.
- **Orphan resolved:** [[Harness Design Patterns]] now cross-linked from [[Meta-Harness]] and [[Agentic Harness]].
- **Frontmatter gap:** `meta/dashboard.md` now has full schema (`status`, `tags`, `sources`, `related`).
- **Frontmatter cleanup:** duplicate `aliases:` blocks and malformed `sources:` YAML removed from 4 sources where Obsidian's property syncer had collided with explicit edits.
- **Skipped (intentional):** seed-page promotion to `developing` (suggestion-class, not mechanical); `concepts/CLAUDE.md` rename (touches ambiguity but unclear improvement); 7 stale `[!contradiction]` cross-pollinations between [[Eval Awareness]] / [[Sandbagging]] (already well-handled).
- Method: 5 parallel agents (source-backfill, legacy-backfill, date-fix, domain-page, title-fix); mechanical fixes inline (aliases, index reconciliation, dashboard frontmatter, orphan links).

## [2026-05-13] lint | Post-batch-ingest health check

- Trigger: 17-source parallel batch ingest completed; write contention on `sources/_index.md` and `concepts/_index.md` flagged in batch log.
- Pages scanned: 103 (26 sources, 55 concepts, 15 entities, 2 theses, 2 domain, 3 meta).
- Issues found: 29 total — 6 critical, 14 warnings, 9 suggestions.
- Top critical: (1) 87 dead-link occurrences via 4 short-title source aliases (add `aliases:` to fix); (2) 8 sources missing from `sources/_index.md`; (3) 8 concepts missing from `concepts/_index.md`; (4) 23 source pages have empty `sources:` field with no `.raw/` link; (5) `date_published: 2026-05-04` on `2024-12-19 - Building Effective Agents` (should be `2024-12-19`); (6) 2 stale `brain/03_Resources/AI-Agents/index` dead links from pre-migration era.
- Legacy audit: 32 pages carry `_legacy_source_count > 0` with `sources: []` empty — backfill from body wikilinks needed; ACI (6), Just-in-Time Context Retrieval (5), Token Economics (5) are highest priority.
- Date hygiene: 7 sources with imprecise or defaulted-to-ingest `date_published`; at minimum SWE-bench Verified Sonnet 3.5 should be `2024-10-29`.
- Report: [[lint-2026-05-13]] (`wiki/meta/lint-2026-05-13.md`)

## [2026-05-13] ingest | Batch: 17 Anthropic engineering posts

- Scope: deduped against existing wiki (6 of 23 requested URLs were already ingested — Scaling Managed Agents, Advanced Tool Use, Multi-Agent Research System, Building Effective Agents, Effective Context Engineering). Remaining 17 ingested in parallel.
- Sources added: [[2024-09-19 - Anthropic - Contextual Retrieval]], [[2025-10-01 - Anthropic - Harness Design Long Running Apps]], [[2026-04 - Anthropic - Claude Code Auto Mode]], [[2026-05-13 - Anthropic - Agent Skills]], [[2026-01-21 - Anthropic - AI-Resistant Technical Evaluations]], [[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]], [[2026-05-13 - Anthropic - Claude Code Best Practices]], [[2026-05-13 - Anthropic - Claude Code Sandboxing]], [[2026-05-13 - Anthropic - Code Execution with MCP]], [[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]], [[2025-06-26 - Anthropic - Desktop Extensions]], [[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]], [[2026-05-13 - Anthropic - Eval Awareness BrowseComp]], [[2026-02-05 - Anthropic - Infrastructure Noise Agentic Coding Evals]], [[2026-05-13 - Anthropic - Postmortem Three Recent Issues]], [[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]], [[2025-03-20 - Anthropic - The Think Tool]], [[2026-05-13 - Anthropic - Writing Effective Tools for Agents]]
- New entities (10): [[Agent Skills]], [[Anthropic]], [[BrowseComp]], [[Claude 3.5 Sonnet]], [[Claude Code]], [[Claude Desktop]], [[Claude Opus 4.6]], [[DXT]], [[SWE-bench]], [[SWE-bench Verified]]
- New concepts (~27): [[Agent Eval Pyramid]], [[Agent Interface Contracts]], [[Agent Sandboxing]], [[Agentic Coding Slash Commands]], [[Agentic Harness]], [[AI Tool Fluency]], [[AI-Resistant Evaluation Design]], [[BM25 and Hybrid Retrieval]], [[Cache Invalidation Cascade]], [[CLAUDE.md]], [[Config Type Safety]], [[Context Anxiety]], [[Context Assembly Pipeline]], [[Contextual Retrieval]], [[Eval Awareness]], [[Eval Infrastructure Noise]], [[Harness Design Patterns]], [[Harness Staleness]], [[Minimal Footprint Principle]], [[Permission Classifier]], [[Permission Model]], [[Progressive Disclosure]], [[Prompt Injection]], [[Reranking]], [[Sandbagging]], [[Think Tool]], [[Trace-Based Evaluation]]
- Contradictions surfaced: (1) [[Multi-Agent Systems]] earlier claim ("coding tasks less parallelizable") vs [[Building C Compiler with Parallel Claudes]] — reconciled with `[!contradiction]` callout; carve-out applies to tightly-coupled code, not modular codebases with clean interface contracts.
- Cross-cutting themes: (a) **eval validity** as the unifying problem across [[AI-Resistant Evaluation Design]], [[Eval Awareness]], [[Eval Infrastructure Noise]], [[LLM-as-Judge Evaluation]], [[Pass^k Reliability Metric]]; (b) **harness as first-class engineering artifact** across [[Harness Design Patterns]], [[Meta-Harness]], [[Agentic Harness]], [[Long-Horizon Context Management]]; (c) **MCP token economics** across [[Code Execution with MCP]], [[Advanced Tool Use]], [[Tool Search Tool]], [[Programmatic Tool Calling]], [[DXT]].
- Backlog: `wiki/sources/_index.md` and `wiki/concepts/_index.md` had heavy parallel contention during ingest; next lint pass should reconcile counts and verify all new pages are listed. Dates on most new files default to 2026-05-13 (ingest date) — backfill publish dates from URL paths in a future pass.
- Method: 17 parallel `claude-obsidian:wiki-ingest` agents, one per URL; orchestrator consolidated index and log.

## [2026-05-13] ingest | τ-bench (Yao et al, Sierra, 2024)

- Source: `.raw/articles/2024-06-17 - Yao et al - tau-bench.md` (arXiv 2406.12045)
- Summary: [[2024-06-17 - Yao et al - tau-bench]]
- Pages created: [[2024-06-17 - Yao et al - tau-bench]], [[Pass^k Reliability Metric]], [[User Simulator Evaluation]], [[tau-bench]], [[Sierra]]
- Pages updated: [[index]], [[hot]], [[AI-Agents]], [[Workflows Beat Agents for Most Production]], [[Autonomous Agents]], [[LLM-as-Judge Evaluation]], `wiki/sources/_index.md`, `wiki/entities/_index.md`, `wiki/concepts/_index.md`
- Key insight: First wiki source to measure **reliability**, not capability. gpt-4o pass^1 ≈ 61% on retail collapses to pass^8 < 25% — same task, just different sampling. Strengthens [[Workflows Beat Agents for Most Production]]; supplies the long-missing eval primitive for [[Autonomous Agents]].

## [2026-05-11] init | vault restructured to claude-obsidian layout

- Migrated 47 files from `AI-Agents/` and `AI-Agents/raw/` into `wiki/` and `.raw/articles/`.
- Rewrote all frontmatter to the repo's schema (`type`, `title`, `created`, `updated`, `tags`, `status`, `related`, `sources`). Status mapping: `stub→seed`, `draft→developing`, `mature→mature`, `stale→evergreen`. Sources lists set to `[]` placeholder; original counts preserved as `_legacy_source_count` for audit.
- Source pages got proper source-type fields: `source_type`, `author`, `date_published`, `url`, `confidence`, `key_claims`. Each links to its corresponding `.raw/articles/<file>.md`.
- `AI-Agents/Overview.md` → `wiki/domains/AI-Agents.md` (as the domain page).
- Created vault root: `WIKI.md` (schema reference), `CLAUDE.md` (project deltas).
- Created wiki meta: `index.md` (this catalog), `log.md` (this file), `hot.md` (session cache), `overview.md` (top-level synthesis).
- Deleted: `AI-Agents/`, `LLM/` (scaffold only, no content), `Productivity/` (empty), and the earlier in-session scaffold at root (`CLAUDE.md`, `hot.md`, `Overview.md`, `index.md`, `log.md`).
- Full pre-migration backup at `outputs/03_Resources-backup-20260511-045630.tar.gz`.
- Plugin NOT yet installed. Nick to run: `claude plugin marketplace add AgriciDaniel/claude-obsidian`.
- pages: [[WIKI]], [[CLAUDE]], [[index]], [[hot]], [[overview]], [[AI-Agents]], plus 39 migrated content pages
