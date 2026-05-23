---
type: overview
title: "Wiki Overview"
created: 2026-05-11
updated: 2026-05-20
tags:
  - meta
status: developing
related: []
sources: []
---

# Overview

Executive summary of the vault. What's here, what's the thesis, where the gaps are.

## Vault state (snapshot 2026-05-11)

- **~155 wiki pages**, **34 raw sources**, **2 domains** (AI-Agents and LLM both active). Snapshot 2026-05-20.
- All migrated from the prior topic-scoped sub-wiki schema (`AI-Agents/{raw,sources,entities,concepts,theses}/`) into the `claude-obsidian` repo's vault layout (`.raw/` + `wiki/`).
- The vault is designed to work with the `claude-obsidian` Claude Code plugin once installed. Without the plugin, follow `WIKI.md` directly.

## Domains

### AI-Agents (active)

The most developed domain. Source corpus is Anthropic-heavy: *Building Effective Agents* (2024-12), the multi-agent research system post (2025-06), *Effective Context Engineering* (2025-09), *Advanced Tool Use* (2025-11), *Scaling Managed Agents* (2026-04), plus Manus's *Context Engineering for AI Agents* (2025-07) and *Recursive Language Models* (Zhang & Khattab, 2025-10).

Running thesis (cite individual concept pages for details, not this summary):

- The workflow/agent boundary is real and underrated — most production "agents" are workflows with LLM steps, and [[Workflows Beat Agents for Most Production]] argues this is correct.
- Context engineering has displaced prompt engineering as the binding constraint. The frontier is [[Just-in-Time Context Retrieval]] and [[Long-Horizon Context Management]], not better prompts.
- Tool design is becoming its own discipline — [[ACI - Agent-Computer Interface]] formalizes this as analogous to HCI.
- The MCP standard ([[MCP]]) is winning the tool-interface battle, not because it's technically superior but because Anthropic backs it and the alternatives are fragmented.

### LLM (active)

Populated 2026-05-14 with a 5-source Thinking Machines Lab pulse, then expanded 2026-05-20 with the continual-learning research: [[Persona Vectors]], [[Activation Steering / Representation Engineering]], [[In-Context Learning]], [[Test-Time Adaptation]], [[Reward Modeling]], [[Online Learning from Interaction]]. Planned scope: transformer internals, training, inference, scaling, evaluation, alignment, mechanistic interpretability. Karpathy-centric seed canon (nn-zero-to-hero, Intro to LLMs, nanoGPT, llm.c, Software 2.0/3.0). Will become `wiki/domains/LLM.md` once first source lands.

Boundary vs AI-Agents: LLM is "how the model works"; AI-Agents is "what you build on top." Training-time tool use is LLM; deployment-time tool use is AI-Agents.

### Continual learning & model-centric systems (added 2026-05-20)

A cross-cutting thread spanning both domains: an agent that learns from each interaction ([[Online Learning from Interaction]]), persists it ([[Persona Vectors vs Memory Files]]), centers the model ([[Model-Centric Architecture]]), and is steered by live signals ([[Online Evaluation]]). Umbrella synthesis: [[Research - Continually-Learning Model-Centric Systems]]. The four directions are one loop; the guarantees layer (constraints/validation/permissioning) is the durable residue model-centrism does not absorb.

## Theses

Nick's evolving views, distinct from external syntheses:

- [[Static Action Spaces vs Dynamic Tool Discovery]] — which architectural axis matters more for agent scaling
- [[Workflows Beat Agents for Most Production]] — workflow-first is the correct default, not a fallback

## Gaps to fill (ranked)

1. **LLM domain.** Zero pages. Highest ROI for the next ingest round.
2. **Source-list backfill.** Migrated concept pages have `sources: []` placeholders; original counts are in `_legacy_source_count`. A lint pass should reconstruct lists by parsing bodies.
3. **Cross-domain meta-theses.** Boundary cases (training-time tool use, RLHF as agent shaping) deserve `comparisons/` pages once both domains have content.
4. **Productivity domain.** Removed during migration (was empty). Will recreate if/when content lands.

## Open questions

- Where does the LLM/AI-Agents boundary fall for training-time tool use (toolformer, Gorilla)?
- Is the workflow/agent distinction in [[Workflows vs Agents]] a temporary 2024–2026 artifact, or load-bearing long-term?
- How much of frontier model behavior is architectural vs RLHF-induced?

Cite individual pages, not this overview, when answering queries.
