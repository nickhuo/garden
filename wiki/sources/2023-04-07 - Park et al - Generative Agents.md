---
type: source
title: "Generative Agents: Interactive Simulacra of Human Behavior"
created: 2026-05-20
updated: 2026-05-20
tags: [llm, ai-agents, memory, memory-stream]
status: developing
source_type: paper
author: Joon Sung Park, Joseph O'Brien, Carrie Cai, Meredith Ringel Morris, Percy Liang, Michael Bernstein
date_published: 2023-04-07
url: https://arxiv.org/abs/2304.03442
confidence: high
related: ["[[Memory Stream]]", "[[Agent Memory Taxonomy]]", "[[CoALA]]"]
sources: []
key_claims:
  - "Agents store a complete natural-language record of experiences in a memory stream."
  - "Retrieval ranks memories by a weighted combination of recency, importance, and relevance."
  - "Reflection periodically synthesizes raw observations into higher-level inferences stored back in the stream."
  - "Planning uses retrieved memories to produce behavior; observation/planning/reflection each contribute to believability (ablation)."
  - "25 agents in a Sims-like sandbox produced emergent social behavior (e.g. self-organizing a Valentine's Day party)."
---

## Summary

Park et al. (2023) introduce the **memory stream**: an append-only natural-language log of an agent's observations. At each step the agent retrieves relevant memories by scoring them on recency (exponential decay), importance (LLM-assigned salience), and relevance (embedding similarity to the current query) (high confidence). Periodic **reflection** asks the LLM to synthesize recent high-importance memories into higher-level inferences, which are written back into the stream as new memories — a textual, inspectable form of compounding knowledge (high).

## Key claims

- The full architecture (observe → retrieve → reflect → plan) is needed for believability; ablating any component degrades behavior (high).
- 25 agents produced emergent coordination from a single seed goal (high).

## Limits

> [!gap] Memory stream grows unbounded; retrieval cost and reflection quality degrade at long horizons. No mechanism to forget or compress beyond reflection. Believability was the metric, not task accuracy.

## Connection to prior work

Canonical instance of the **textual memory-files** path: everything the agent "learns" is stored as inspectable natural language, never in weights. Contrast with persona vectors (Source: [[2025-07-29 - Chen et al - Persona Vectors]]). Foreshadows [[MemGPT]] (paging memory) and [[Self-Editing Memory]]. The append-only stream maps onto [[Session as Event Log]].

## Sources

- [[Memory Stream]]
- arXiv:2304.03442
