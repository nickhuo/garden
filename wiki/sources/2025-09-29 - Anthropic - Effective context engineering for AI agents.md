---
type: source
title: Effective context engineering for AI agents
aliases:
  - Effective context engineering for AI agents
created: 2026-05-04
updated: 2026-05-13
tags:
- ai-agents
- anthropic
- context
- retrieval
- memory
status: mature
related: []
sources:
  - "[[.raw/articles/2025-09-29 - Anthropic - Effective context engineering for AI agents.md]]"
source_type: blog
author: Anthropic — Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield (Applied AI team)
date_published: 2025-09-29
url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
confidence: medium
key_claims: []
---

# Effective context engineering for AI agents (Anthropic, 2025-09-29)

## Summary

Anthropic's Applied AI team frames **context engineering** as the natural progression from prompt engineering once you move from one-shot generation to multi-turn agents. Defines it as the discipline of curating *all* tokens at inference time — system prompts, tools, retrieved data, message history, scratchpads — under a finite "attention budget." Names three operational shifts: just-in-time retrieval over pre-loaded RAG, sub-agent decomposition for context overflow, and explicit techniques for long-horizon agents.

## Definition (Anthropic)

> "Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference, including all the other information that may land there outside of the prompts."

It is a **superset of prompt engineering** — prompt engineering is "writing/organizing instructions"; context engineering is "managing the full token budget."

## Core mental model: attention as a finite budget

> "Context, therefore, must be treated as a finite resource with diminishing marginal returns. Like humans, who have limited working memory capacity, LLMs have an 'attention budget' that they draw on when parsing large volumes of context."

Justified by transformer `n²` pairwise attention + training-distribution skew toward shorter sequences. Cites Chroma's "context rot" research — recall degrades as context grows, in all models.

## Operating principle

> "Find the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."

Repeated as the guiding principle in both the anatomy section and the conclusion.

## Anatomy of context (component-by-component)

- **System prompts** — at "the right altitude" (Goldilocks zone between brittle hardcoded logic and vague high-level guidance)
- **Tools** — token-efficient, minimally overlapping schemas. Tool docs ARE context, not metadata.
- **Few-shot examples** — diverse + canonical, not exhaustive
- **Message history** — aggressively pruned

## Architectural shift: just-in-time retrieval

Pre-inference embedding-based RAG is being supplanted by **just-in-time** agentic retrieval. Instead of front-loading embeddings, agents hold lightweight identifiers (file paths, links, queries) and load context dynamically via tools. See [[Just-in-Time Context Retrieval]].

> "Rather than pre-processing all relevant data up front, agents built with the 'just in time' approach maintain lightweight identifiers (file paths, stored queries, web links, etc.) and use tools to dynamically load data into context at runtime."

**Hybrid retrieval** (some upfront context + agentic exploration) is the pragmatic middle ground for static domains like legal/finance.

## Long-horizon agents need three techniques

See [[Long-Horizon Context Management]] for the master concept. Three named techniques:

1. **Compaction** — summarize old context, reinitialize the window (lightest form: tool-result clearing in the Claude Developer Platform context-management feature)
2. **Structured note-taking** — agent writes to external memory file (NOTES.md, todo lists, "Claude Plays Pokémon" memory file). Agentic memory.
3. **Sub-agent architectures** — back-references [[Multi-Agent Systems]]; lead agent + specialized sub-agents returning 1–2k token distillations

## Connections to existing wiki concepts

- **[[Augmented LLM]]** — JIT retrieval and structured note-taking are explicit instantiations of the memory leg. Compaction is a memory-compression operator.
- **[[ACI - Agent-Computer Interface]]** — reinforces the framing: tool descriptions, tool result shapes, error messages are *all* context. Adds the principle of **minimally overlapping tool surfaces** — multiple tools that overlap in capability waste attention budget.
- **[[Token Economics]]** — "attention budget" elevates token cost from a billing concern to an architectural quality concern (recall degradation, n² attention).
- **[[Workflows vs Agents]]** — cites *Building effective agents* directly. Borrows Simon Willison's definition of agent: "LLMs autonomously using tools in a loop." Adds the long-horizon dimension explicitly.
- **[[Multi-Agent Systems]]** — sub-agent architecture is one of the three long-horizon techniques.

## Verbatim claims worth quoting

- "Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference, including all the other information that may land there outside of the prompts."
- "Context, therefore, must be treated as a finite resource with diminishing marginal returns."
- "Good context engineering means finding the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."
- "Smarter models require less prescriptive engineering, allowing agents to operate with more autonomy. But even as capabilities scale, treating context as a precious, finite resource will remain central to building reliable, effective agents."

## Patterns and concepts introduced

- [[Context Engineering]] — the master concept (includes attention budget mental model)
- [[Just-in-Time Context Retrieval]] — vs pre-inference embedding RAG
- [[Long-Horizon Context Management]] — compaction + structured note-taking + sub-agents

## Entities mentioned (no separate pages, per ≥2-mention rule)

- Chroma (cited for "context rot" research) — no page
- Simon Willison (definition of agent borrowed) — no page
- Claude Plays Pokémon (memory file example) — no page
- Claude Developer Platform tool-result clearing feature — no page

## Source location

- Raw: `raw/2025-09-29 - Anthropic - Effective context engineering for AI agents.md`
