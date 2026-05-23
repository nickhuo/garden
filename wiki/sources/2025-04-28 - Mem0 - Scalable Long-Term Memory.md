---
type: source
title: "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory"
created: 2026-05-20
updated: 2026-05-20
tags: [llm, ai-agents, memory]
status: seed
source_type: paper
author: Mem0 team
date_published: 2025-04-28
url: https://arxiv.org/pdf/2504.19413
confidence: medium
related: ["[[Memory Stream]]", "[[Agent Memory Taxonomy]]", "[[Letta]]"]
sources: []
key_claims:
  - "Mem0 is a memory layer bolted onto an existing agent framework; it handles extraction, storage, and retrieval of long-term memory as external text/graph state."
  - "Contrasts with Letta, which is a full agent runtime that manages memory as the agent's editable in-context state."
  - "Memory surveys categorize memory as parametric (in weights) vs contextual/non-parametric (external text, structured, or graph)."
---

## Summary

Mem0 represents the **memory-as-a-layer** productization of the textual-memory path: an external store (vector + graph) with extract/update/retrieve operations bolted onto any agent framework (medium confidence — vendor framing). It sits opposite Letta's runtime-owns-memory model. Surveys of LLM-agent memory (e.g. "From Human Memory to AI Memory", arXiv:2504.15965) split memory into **parametric** (encoded in weights — the persona-vector / finetuning path) vs **non-parametric/contextual** (external text, tables, triples, graphs — the memory-files path), with operations: consolidation, updating, indexing, forgetting, retrieval, compression.

## Limits

> [!gap] Vendor benchmarks; independent comparisons of Mem0 vs Letta vs raw RAG are thin. Treat productized claims as medium confidence.

## Connection to prior work

Operationalizes [[Memory Stream]] and [[MemGPT]] tiering as a deployable service. The parametric/non-parametric survey split is the cleanest framing of the persona-vectors-vs-memory-files axis.

## Sources

- [[Memory Stream]], [[Letta]]
- arXiv:2504.19413; arXiv:2504.15965 (memory survey)
