---
type: meta
title: "Wiki Log"
updated: 2026-05-20
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

## [2026-05-28] refactor | Concept dedup — 3 merges (108→105)
- **Trigger:** user — "current lint doesn't merge duplicate concepts; there are too many." Manual merge-candidate scan over all 108 concepts (semantic tiling is opt-in + disabled here: no `scripts/tiling-check.py`, no ollama).
- **Merges (canonical ← absorbed):**
  - [[LLM-as-Judge]] ← `LLM-as-Judge Evaluation` (folded Anthropic single-call prescription + production quality-monitoring; canonical keeps the bias catalog + Lenz agreement-ceiling note).
  - [[Implicit Feedback Signals]] ← `Learning from Implicit Feedback` (one page, two angles: as-evaluation-signal / as-learning-signal; merged sources Meta RLUF + Silver-Sutton).
  - [[Agentic Harness]] ← `Harness Design Patterns` (definition/anatomy/SWE-bench simplicity + the four responsibilities, anti-patterns, layered architecture, testing; status seed→developing).
- **Link rewrites:** 44 live files repointed (`[[old`→`[[new`, alias display preserved); deduped `related:` in 2 source pages; fixed 3 prose lines + 2 catalog files (index, _index, domains) that double-referenced a merged page. `log.md` past entries and `meta/lint-2026-05-13.md` left intact (append-only history → expected dead links to merged-away titles).
- **Pages updated:** [[brain/03_Resources/wiki/index]] (count 108→105), [[hot]] unaffected, [[AI-Agents]], `wiki/concepts/_index.md`. Weak candidates (Persona-Vectors-vs-Memory-Files relocation, Manager-Pattern≈Orchestrator-Workers) deliberately NOT merged.

## [2026-05-24] ingest | Everything is a Ralph Loop (Geoffrey Huntley)
- **Trigger:** user — `/wiki-ingest https://ghuntley.com/loop/`.
- **Source:** `.raw/articles/loop-2026-05-24.md` → [[2026-01-17 - Geoffrey Huntley - Everything is a Ralph Loop]] (first non-vendor *practitioner* source in the wiki).
- **Pages created:** [[Ralph Loop]] (concept); [[Geoffrey Huntley]] (entity). _(Steve Yegge and The Weaving Loom entities created then removed same session — thin/stub, folded to plain text on [[Ralph Loop]] and [[Geoffrey Huntley]].)_
- **Pages updated:** [[Multi-Agent Systems]] (counter-position contradiction callout), [[Context Engineering]] ("operationalized as a coding method"), [[Autonomous Agents]], [[AI-Agents]], index, sub-indexes, hot.
- **Key insight:** Ralph is the **opinionated monolithic pole** — a single-process, one-task-per-loop coding agent that frames agentic coding as *[[Context Engineering]], not multi-agent orchestration* ("agents are non-deterministic → multiplexing is premature complexity"). Direct counter-position to Anthropic's coordinator+workers framing; endpoint is "The Weaving Loom" (revenue-optimizing evolutionary software). Polemical, benchmark-free — confidence on the *technique* > the *economic claims*.

## [2026-05-24] ingest | Prime Intellect batch — 5 research blog posts
- **Trigger:** user — `/wiki-ingest` with 5 PrimeIntellect URLs; "看看有什么 insight" on this self-improving-focused company.
- **Sources:** `.raw/articles/{reward-hacking,general-agent,auto-nanogpt,renderers,rlm}-2026-05-24.md` → [[2026-05-20 - Prime Intellect - Systematic Reward Hacking]], [[2026-05-18 - Prime Intellect - General Agent]], [[2026-05-14 - Prime Intellect - Autonomous AI Research for nanogpt Speedrun]], [[2026-05-12 - Prime Intellect - Renderers]], [[2026-01-01 - Prime Intellect - Recursive Language Models]].
- **Pages created:** [[Prime Intellect]] (entity); [[Reward Hacking]], [[Self-Evolving Agent Environments]], [[Token-In Token-Out]], [[Autonomous Research Agents]] (concepts); [[Prime Intellect Self-Improvement Stack]] (comparison/synthesis).
- **Pages updated:** [[Recursive Language Models]] (now cites 2nd independent source — Prime Intellect impl, partially closing the replication gap), index, log, hot, [[AI-Agents]], [[LLM]], sub-indexes.
- **Key insight:** the 5 posts are one bet — an open-source *self-improvement stack* (environments → RL plumbing → reward science → context scaling → autonomous research). Recurring obsession: **faithfulness** (byte-exact tokens, faithful reward, verification grounding). The honest ceiling: the nanogpt speedrun's **novelty gate** shows frontier agents search/recombine superbly but cannot yet *originate* ideas — self-improvement is currently human-seeded.

## [2026-05-23] manual | Keep zELO paper only (ZeroEntropy autoresearch trimmed)
- Autoresearch on ZeroEntropy / zerank ran 3 rounds; per Nick's call, kept **only** the source page [[2025-09-16 - Pipitone et al - zELO]] (flagged by Nick as a strong commercialization angle). Deleted the other 9 pages (4 sources, ZeroEntropy entity, 3 concepts, 1 synthesis) and reverted updates to [[Reranking]], index, hot.
- Page kept: [[2025-09-16 - Pipitone et al - zELO]] — zELO trains rerankers on LLM-ensemble pairwise preferences converted to absolute Elo scores (no human annotation, regenerable as base LLMs improve). Branch `research/zeroentropy-evals`.

## [2026-05-22] ingest | OpenAI — A Practical Guide to Building Agents
- **Trigger:** user — `/wiki-ingest https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/`. Page 403'd WebFetch; fetched the official PDF from cdn.openai.com and extracted text via pypdf (34 pages).
- **Source:** `.raw/articles/a-practical-guide-to-building-agents-2026-05-22.md`. Summary: [[2025 - OpenAI - A Practical Guide to Building Agents]].
- **Pages created:** [[OpenAI]], [[OpenAI Agents SDK]] (entities); [[Manager Pattern]], [[Agent Handoffs]], [[Agent Tool Categories]], [[Agent Run Loop]], [[Agent Guardrails]], [[Human-in-the-Loop Intervention]] (concepts); [[OpenAI Practical Guide vs Anthropic Building Effective Agents]] (comparison).
- **Pages updated:** index, hot, log, [[AI-Agents]], concepts/_index, entities/_index, sources/_index, comparisons/_index, [[Workflows vs Agents]], [[Orchestrator-Workers]].
- **Key insight:** the OpenAI-side canon to Anthropic's [[2024-12-19 - Anthropic - Building Effective Agents]] — convergent advice ("maximize a single agent first" ≈ "use the simplest thing"), different vocabulary. Vocabulary map: Manager pattern ≈ [[Orchestrator-Workers]], handoffs ≈ [[Routing]]. OpenAI's strongest unique contribution is the concrete **guardrail typology** (relevance/safety/PII/moderation/tool-safeguards/rules/output-validation, optimistic tripwires) + human-in-the-loop triggers. Tool safeguards' risk ratings tie into [[Permission Model]].

## [2026-05-22] ingest | Karpathy — Sequoia Ascent 2026 (Software 3.0 & agentic engineering)
- **Trigger:** user — `/wiki-ingest https://karpathy.bearblog.dev/sequoia-ascent-2026/`
- **Source:** `.raw/articles/sequoia-ascent-2026-2026-05-22.md` (Karpathy, Sequoia Ascent 2026 bearblog companion). Summary: [[2026-05-22 - Karpathy - Sequoia Ascent 2026]].
- **Pages created:** [[Software 3.0]], [[Verifiability]], [[Jagged Intelligence]], [[Vibe Coding]], [[Agentic Engineering]], [[Agent-Native Infrastructure]] (concepts); source page above.
- **Pages updated:** [[Andrej Karpathy]] (Sequoia section + sources), [[Software 2.0]] (3.0 cross-link), [[AI-Agents]] (new Software 3.0 section), index, hot, log.
- **Key insight:** December 2025 was the agentic inflection — programming shifts from lines to delegated macro actions. [[Software 3.0]] (natural-language programming) sits above [[Software 2.0]]; [[Verifiability]] ("automate what you can verify") explains where models get good; [[Jagged Intelligence]] ("ghosts, not animals") explains where they fail. [[Vibe Coding]] raises the floor, [[Agentic Engineering]] raises the ceiling, and [[Agent-Native Infrastructure]] (sensors/actuators) generalizes [[ACI - Agent-Computer Interface]] to the whole product. Capstone framing over the existing agent corpus.

## [2026-05-22] ingest | BFCL + ToolLLM (tool-use benchmark cluster)
- **Trigger:** user — "BFCL, τ-bench, ToolBench — find the paper about these three concept." τ-bench already in wiki; found + ingested the other two papers and built the synthesis.
- **Sources:** `.raw/articles/2025-07 - Patil et al - BFCL.md` (ICML 2025), `.raw/articles/2023-07-31 - Qin et al - ToolLLM.md` (ICLR'24).
- **Pages created:** [[2025-07 - Patil et al - BFCL]], [[2023-07-31 - Qin et al - ToolLLM]] (sources); [[BFCL]], [[ToolBench]], [[Gorilla]], [[OpenBMB]] (entities); [[Tool-Use Benchmarks - BFCL vs tau-bench vs ToolBench]] (first comparison page).
- **Pages updated:** [[tau-bench]] (sibling-benchmark section), index, entities/_index, sources/_index, comparisons/_index (new), [[AI-Agents]], hot.
- **Key insight:** the three benchmarks measure orthogonal axes — BFCL = call correctness at scale (AST grading), τ-bench = reliability under interaction (pass^k, deterministic DB reward), ToolBench = generalization across 16k+ real APIs (LLM-judge). Grading runs deterministic→LLM-judged; faithfulness trades against scale. Closes the "tool-use benchmarks under-covered" gap.

## [2026-05-20] query | How to Ensure Agent Reliability
- **Trigger:** wiki-query "如何确保 agent reliability?"; filed the synthesized answer back per user request.
- **Page created:** [[How to Ensure Agent Reliability]] (questions/).
- **Structure:** 5-layer framework (structural foundation → measurement → runtime hygiene → maintenance → failure-mode awareness), governed by [[Runtime vs Structural Reliability]]. Includes a 5-step incident diagnostic flow.
- **Index:** questions 5→6.

---

## [2026-05-20] refactor | Trim Online-Eval & Real-Time-Learning sources to milestones
- Per review on PR #2, removed 3 non-milestone sources: Kohavi et al *Trustworthy Online Controlled Experiments* (a full book, too heavy), Akyürek et al *Test-Time Training* (ARC-specific, narrow), Zheng et al *Lifelong Learning Roadmap* (survey, not a landmark).
- Stripped their citations from [[Research - Online Evaluation]], [[Research - Real-Time Learning]], and related concept pages. Concepts [[A/B Testing for Agents]] and [[Test-Time Adaptation]] kept as framing rungs but now thinly sourced (flagged with gap callouts).
- Net: sources 49 -> 46.

## [2026-05-20] save | Thesis — Interpretable Persona Vectors (the Beckman Pattern)
- Filed Nick's view that the persona-vectors-vs-memory-files split is a general architecture, and Beckman is its fully-interpretable, externally-stored, dual-cadence instance (mastery overlay = memory-file pole; (A,B,C) metacognition coefficients = interpretable persona-vector analogue).
- Pages created: [[Interpretable Persona Vectors: the Beckman Pattern]]
- Pages updated: [[brain/03_Resources/wiki/index]], [[theses]] (_index)
- Key claim: an interpretable persona vector is achievable and worth the inspectability it preserves; three extensions — grow (A,B,C) into a named higher-dim vector, move persona from prompt-param to model-conditioning, add a memory→persona promotion valve.

## [2026-05-20] autoresearch | Continually-Learning Model-Centric Systems (umbrella)
- Rounds: 3 per direction × 4 directions. Sources found: 15 new. Pages created: 40 (4 syntheses + 1 umbrella + 15 sources + 18 concepts + 3 entities, on branch research/continual-learning-systems).
- Synthesis: [[Research - Continually-Learning Model-Centric Systems]]
- Key finding: the four directions form one loop — interaction → online eval → learning signal → persisted memory/persona, with the model (not orchestration code) at the center. Mapped each pillar to Nick's prior work (Sonic/Donut/Beckman/Compass/Baidu).

## [2026-05-20] autoresearch | Online Evaluation
- Pages: [[Research - Online Evaluation]], [[Online Evaluation]], [[LLM-as-Judge]], [[Implicit Feedback Signals]], [[Reward Modeling]], [[A/B Testing for Agents]], [[Eval Validity]]; sources [[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]], [[2020 - Kohavi Tang Xu - Trustworthy Online Controlled Experiments]], [[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]].
- Key finding: a strong LLM judge matches human agreement (>80%) only after debiasing; A/B is the only causally trustworthy verdict; the metric is the construct. Bridges real-time learning ↔ persistent memory.

## [2026-05-20] autoresearch | Model-Centric Architecture
- Pages: [[Research - Model-Centric Architecture]], [[Model-Centric Architecture]], [[The Bitter Lesson]], [[Software 2.0]], [[Code-to-the-Side vs Orchestration]]; entities [[Andrej Karpathy]], [[Richard Sutton]]; sources [[2019-03-13 - Sutton - The Bitter Lesson]], [[2017-11-11 - Karpathy - Software 2.0]].
- Key finding: scaling favors model-centrism long-run (Bitter Lesson / Software 2.0); harness/schema discipline wins at ship time. Reconciliation = a slider; the durable side-code is the guarantees layer.

## [2026-05-20] autoresearch | Persistent Memory & Persona Vectors
- Pages: [[Research - Persistent Memory and Persona Vectors]], [[Persona Vectors]], [[Activation Steering / Representation Engineering]], [[Memory Stream]], [[Persona Vectors vs Memory Files]]; entity [[Letta]]; sources [[2025-07-29 - Chen et al - Persona Vectors]], [[2023-04-07 - Park et al - Generative Agents]], [[2023-10-12 - Zou et al - Representation Engineering]], [[2025-04-28 - Mem0 - Scalable Long-Term Memory]].
- Key finding: two paths split on control vs inspectability — persona vectors (parametric, who) vs memory files (contextual, what). Beckman implements both poles by hand.

## [2026-05-20] autoresearch | Real-Time Learning
- Pages: [[Research - Real-Time Learning]], [[Online Learning from Interaction]], [[In-Context Learning]], [[Test-Time Adaptation]], [[Learning from Implicit Feedback]]; sources [[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]], [[2024-11-11 - Akyürek et al - Surprising Effectiveness of Test-Time Training]], [[2024-04-17 - Agarwal et al - Many-Shot In-Context Learning]], [[2025-05-21 - Meta - Reinforcement Learning from User Feedback]], [[2025-01-13 - Zheng et al - Lifelong Learning of LLM-Based Agents - A Roadmap]], [[2022-03-04 - Ouyang et al - InstructGPT]].
- Key finding: real-time learning is a durability spectrum (in-context → memory → test-time → online RL); catastrophic forgetting is the central unsolved problem; memory is the main mitigation.

## [2026-05-19] ingest | Packer et al — MemGPT: Towards LLMs as Operating Systems
- Source: `.raw/pdfs/memgpt-llms-as-operating-systems-2310.08560.pdf` (downloaded; PDF kept locally)
- Summary: [[2023-10-12 - Packer et al - MemGPT - LLMs as Operating Systems]]
- Pages created: [[MemGPT]], [[Self-Editing Memory]]
- Pages updated: [[brain/03_Resources/wiki/index]], [[hot]], [[AI-Agents]], [[Agent Memory Taxonomy]]
- Key insight: Context window = RAM. "Virtual context management" pages data between an in-context tier (working context + FIFO queue) and external storage (recall + archival) under the model's own control via function calls. Pairs with [[CoALA]]: MemGPT is the concrete mechanism for the working↔long-term boundary CoALA names; its memory-edit calls are CoALA *learning* actions, its event loop the *decision cycle*. Became the Letta framework.

## [2026-05-19] ingest | Sumers et al — Cognitive Architectures for Language Agents (CoALA)
- Source: `.raw/pdfs/cognitive-architectures-language-agents-2309.02427.pdf` (downloaded; PDF kept locally)
- Summary: [[2023-09-05 - Sumers et al - Cognitive Architectures for Language Agents]]
- Pages created: [[CoALA]], [[Agent Memory Taxonomy]], [[ReAct]], [[Tree of Thoughts]], [[Shunyu Yao]]
- Pages updated: [[brain/03_Resources/wiki/index]], [[hot]], [[AI-Agents]]
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
- New entities (10): [[Agent Skills]], [[brain/03_Resources/wiki/entities/Anthropic]], [[BrowseComp]], [[Claude 3.5 Sonnet]], [[Claude Code]], [[Claude Desktop]], [[Claude Opus 4.6]], [[DXT]], [[SWE-bench]], [[SWE-bench Verified]]
- New concepts (~27): [[Agent Eval Pyramid]], [[Agent Interface Contracts]], [[Agent Sandboxing]], [[Agentic Coding Slash Commands]], [[Agentic Harness]], [[AI Tool Fluency]], [[AI-Resistant Evaluation Design]], [[BM25 and Hybrid Retrieval]], [[Cache Invalidation Cascade]], [[brain/03_Resources/wiki/concepts/CLAUDE]], [[Config Type Safety]], [[Context Anxiety]], [[Context Assembly Pipeline]], [[Contextual Retrieval]], [[Eval Awareness]], [[Eval Infrastructure Noise]], [[Harness Design Patterns]], [[Harness Staleness]], [[Minimal Footprint Principle]], [[Permission Classifier]], [[Permission Model]], [[Progressive Disclosure]], [[Prompt Injection]], [[Reranking]], [[Sandbagging]], [[Think Tool]], [[Trace-Based Evaluation]]
- Contradictions surfaced: (1) [[Multi-Agent Systems]] earlier claim ("coding tasks less parallelizable") vs [[Building C Compiler with Parallel Claudes]] — reconciled with `[!contradiction]` callout; carve-out applies to tightly-coupled code, not modular codebases with clean interface contracts.
- Cross-cutting themes: (a) **eval validity** as the unifying problem across [[AI-Resistant Evaluation Design]], [[Eval Awareness]], [[Eval Infrastructure Noise]], [[LLM-as-Judge Evaluation]], [[Pass^k Reliability Metric]]; (b) **harness as first-class engineering artifact** across [[Harness Design Patterns]], [[Meta-Harness]], [[Agentic Harness]], [[Long-Horizon Context Management]]; (c) **MCP token economics** across [[Code Execution with MCP]], [[Advanced Tool Use]], [[Tool Search Tool]], [[Programmatic Tool Calling]], [[DXT]].
- Backlog: `wiki/sources/_index.md` and `wiki/concepts/_index.md` had heavy parallel contention during ingest; next lint pass should reconcile counts and verify all new pages are listed. Dates on most new files default to 2026-05-13 (ingest date) — backfill publish dates from URL paths in a future pass.
- Method: 17 parallel `claude-obsidian:wiki-ingest` agents, one per URL; orchestrator consolidated index and log.

## [2026-05-13] ingest | τ-bench (Yao et al, Sierra, 2024)

- Source: `.raw/articles/2024-06-17 - Yao et al - tau-bench.md` (arXiv 2406.12045)
- Summary: [[2024-06-17 - Yao et al - tau-bench]]
- Pages created: [[2024-06-17 - Yao et al - tau-bench]], [[Pass^k Reliability Metric]], [[User Simulator Evaluation]], [[tau-bench]], [[Sierra]]
- Pages updated: [[brain/03_Resources/wiki/index]], [[hot]], [[AI-Agents]], [[Workflows Beat Agents for Most Production]], [[Autonomous Agents]], [[LLM-as-Judge Evaluation]], `wiki/sources/_index.md`, `wiki/entities/_index.md`, `wiki/concepts/_index.md`
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
- pages: [[WIKI]], [[brain/03_Resources/wiki/concepts/CLAUDE]], [[brain/03_Resources/wiki/index]], [[hot]], [[overview]], [[AI-Agents]], plus 39 migrated content pages
