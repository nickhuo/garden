---
type: concept
title: "Memory Stream"
created: 2026-05-20
updated: 2026-05-20
tags: [llm, ai-agents, memory, memory-stream]
status: developing
related: ["[[Agent Memory Taxonomy]]", "[[Self-Editing Memory]]", "[[MemGPT]]", "[[Session as Event Log]]", "[[Persona Vectors vs Memory Files]]"]
sources: ["[[2023-04-07 - Park et al - Generative Agents]]", "[[2025-04-28 - Mem0 - Scalable Long-Term Memory]]"]
---

## Summary

A **memory stream** is an append-only natural-language record of an agent's experiences (Source: [[2023-04-07 - Park et al - Generative Agents]], high confidence). At each step the agent retrieves relevant memories by scoring them on **recency** (exponential decay), **importance** (LLM-assigned salience), and **relevance** (embedding similarity to the current query). Periodic **reflection** synthesizes high-importance memories into higher-level inferences written back into the stream.

This is the canonical instance of the "**textual representation of what was learned**" path: everything persisted is inspectable natural language, never weights.

## Why it matters

The memory stream is the conceptual root of modern agent memory: [[MemGPT]] (tiered paging), [[Self-Editing Memory]] (agent rewrites its own blocks), and productized layers like Mem0/Letta all descend from it. Its great virtue is **inspectability** — you can read, audit, and hand-edit what the agent remembers, unlike a [[Persona Vectors|persona vector]].

## Limits

> [!gap] The stream grows unbounded; retrieval cost and reflection quality degrade at long horizons. Reflection is the only compression/forgetting mechanism. Believability, not task accuracy, was the original metric.

## Connection to prior work

Foreshadowed by, and generalizing, [[Session as Event Log]]. The opposite pole from [[Persona Vectors]] — see [[Persona Vectors vs Memory Files]]. Surveys frame it as **non-parametric/contextual** memory vs parametric (in-weights) memory.

Maps onto Nick's Beckman work: the per-learner **mastery overlay** over the domain knowledge graph is a structured memory stream — a textual/structured record of *what this learner knows*, decoupled from the global KG (*what the world is*). Two schemas, two update cadences: exactly the memory-files-vs-base-model split.

## Connections

- [[MemGPT]], [[Self-Editing Memory]], [[Session as Event Log]]
- [[Agent Memory Taxonomy]]
- [[Persona Vectors vs Memory Files]]

## Open questions

- Optimal forgetting/compression policy beyond reflection?
- When should a learned stream be promoted into weights (or a persona vector)?

## Sources

- [[2023-04-07 - Park et al - Generative Agents]]
- [[2025-04-28 - Mem0 - Scalable Long-Term Memory]]
