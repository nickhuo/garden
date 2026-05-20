---
type: meta
title: "Hot Cache"
updated: 2026-05-19
---

# Recent Context

## Last Updated

2026-05-19 — Ingested [[2023-10-12 - Packer et al - MemGPT - LLMs as Operating Systems]] (PDF saved). Second academic source; builds directly on the CoALA memory taxonomy ingested minutes earlier.

## Key Recent Facts

- **New mechanism — [[MemGPT]]:** treats the context window as **RAM** and runs an OS-style memory manager — *virtual context management*. Two tiers: **main context** (system instructions + editable **working context** + **FIFO queue** with recursive summary of evicted messages) and **external context** (**recall storage** = full event log, **archival storage** = read/write fact/doc DB). The LLM pages data across the boundary by calling functions ([[Self-Editing Memory]]); a **memory-pressure** warning triggers eviction + recursive summarization; events act as **interrupts**, `request_heartbeat` chains multi-step actions, agent **yields** when done. Pairs with [[CoALA]]: MemGPT is the concrete mechanism for the working↔long-term boundary CoALA's [[Agent Memory Taxonomy]] names — memory-edit calls = CoALA *learning* actions, event loop = *decision cycle*. Became **Letta**. The reusable idea, [[Self-Editing Memory]], is "the model curates its own memory via tools" (vs passive RAG) — declarative analogue of [[Agent Skills]] (self-authored *procedural* memory).
- **New framework — [[CoALA]]:** organizes any language agent on three axes — [[Agent Memory Taxonomy|memory]] (working / episodic / semantic / procedural, borrowed from Soar/ACT-R), action space (internal: retrieval/reasoning/learning; external: physical/dialogue/digital grounding), and decision cycle (propose → evaluate → select → execute, looped). It's the **conceptual scaffold beneath the Anthropic operational corpus**: an [[Augmented LLM]] is the minimal CoALA agent; a [[Workflows vs Agents|workflow]] fixes the decision procedure, an agent chooses it. Empty cells (agents that learn their own decision procedures — procedural-memory editing) = the research frontier. Surveyed agents: [[ReAct]] (reason+act, no eval), [[Tree of Thoughts]] (deliberate search, no memory), Voyager (procedural skill library), Generative Agents (episodic+semantic reflection), SayCan. Author [[Shunyu Yao]] also did [[tau-bench]] — coherent arc: build patterns → frame them → benchmark them.
- **New thesis — [[Runtime vs Structural Reliability]]:** agent reliability splits into runtime (judges, classifiers, retries, traces) and structural (sandboxing, permissions, harness review cadence, ACI design). All three failures in [[2026-05-13 - Anthropic - Postmortem Three Recent Issues]] were structural. Industry over-invests in runtime because it's easier to ship. Operational test: "would one more runtime check have *prevented* this or only *detected* it sooner?" If detected-sooner, the fix is structural.
- **Four-pillar map (interview framing):** (1) Data foundations — wiki gap, needs scaling/data-bottleneck source; (2) Agent reliability — strong (now anchored by the new thesis); (3) Trustworthy generation — strongest, three-segment coverage (Recitation/Contextual Retrieval/Agent Eval Pyramid); (4) Inference economics — covered by [[Token Economics]] / [[KV-Cache Discipline]] / [[Manus - Context Engineering for AI Agents]].

- **Claude Code at scale — two through-lines:** (1) **agentic search > RAG** in active codebases because embedding indices silently go stale (renamed/deleted symbols return without warning); (2) **the harness determines performance more than the model.** Five extension points: [[CLAUDE.md]], hooks, [[Agent Skills|skills]], plugins, [[MCP]] — plus LSP and subagents.
- **Highest-leverage hook pattern (non-obvious):** stop hooks that *reflect on the session and propose CLAUDE.md updates while context is still warm*. Beats using hooks only as lint enforcers. This is [[Meta-Harness]] in concrete form — concept-page candidate pending second source.
- **[[Harness Staleness]] gets a cadence:** review configuration every **3-6 months**, especially after major model releases. CLAUDE.md rules tuned for older models (e.g., "break refactors into single-file changes") actively constrain newer ones. Perforce `p4 edit` interception hooks called out as a concrete example of compensations that became dead weight after native support shipped.
- **Path-scoped skills** are the key feature at monorepo scale — bind deployment skills to `services/payments/`, not the whole repo. Prevents pollution when working elsewhere.
- **Initialize in subdirectories, not repo roots** — Claude walks up loading every CLAUDE.md, so root context isn't lost. Counterintuitive but consistently the right default in monorepos.
- **LSP is one of the highest-value investments** for multi-language large codebases. Symbol-level navigation replaces grep's text-matching — filters before Claude reads anything. One enterprise customer rolled LSP out org-wide *before* Claude Code rollout for reliable C/C++ work.
- **Adoption needs a DRI.** Fastest rollouts had infrastructure (plugins, MCP, CLAUDE.md hierarchies) wired *before* broad access. Bottoms-up without centralization fragments and plateaus. "Agent manager" hybrid PM/engineer role emerging in larger orgs.
- **Previous session — TML through-line still relevant:** take numerics seriously. [[Batch Invariance]] / [[Trainer-Sampler Determinism]] / [[Manifold Optimization]] interlock across three TML papers; the determinism infra ([[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]]) underpins [[On-Policy Distillation]] and [[Interaction Model Architecture]].

## Recent Changes (this session)

- Created: [[Runtime vs Structural Reliability]] (thesis)
- Updated: `wiki/index.md` (theses 2→3), `wiki/theses/_index.md`, `wiki/log.md`, `wiki/hot.md`

## Active Threads

- **Concept-page candidates** from this save (promote on second source):
  - "Agentic search vs RAG for code" — comparison page if a second source treats it head-on
  - "Self-improving harness" / meta-hook pattern — generalize the stop-hook → CLAUDE.md update loop
  - "Path-scoped skills" — discrete pattern, currently buried inside [[Agent Skills]]
  - "Skill/hook obsolescence" — generalization of the Perforce example
- **TML backlog.** Five posts is a sample; lab has more material to ingest.
- **Karpathy-centric LLM seed** still untouched (training videos, gist patterns).
- **Cross-domain thesis candidate:** "co-design architecture and optimizer" — needs second-source confirmation outside TML before promotion to `wiki/theses/`.
- **Source-list backfill** (from 2026-05-11 migration). Older AI-Agents pages still have `sources: []` placeholders.
