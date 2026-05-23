---
type: entity
title: "Letta"
created: 2026-05-20
updated: 2026-05-20
tags: [ai-agents, memory, company]
status: developing
related: ["[[MemGPT]]", "[[Self-Editing Memory]]", "[[Memory Stream]]", "[[Agent Memory Taxonomy]]"]
sources: ["[[2025-04-28 - Mem0 - Scalable Long-Term Memory]]"]
---

## Summary

**Letta** is an open-source agent runtime (publicly announced September 2024) that productizes [[MemGPT]] — the MemGPT open-source project became part of Letta (high confidence). Where Mem0 is a memory *layer* you bolt onto an existing framework, Letta is a full *runtime* that owns the agent loop, tool execution, state persistence, and memory.

## Memory model

Letta treats memory as the agent's editable state across tiers (Source: [[2025-04-28 - Mem0 - Scalable Long-Term Memory]] context; Letta blog 2025-07-07, medium confidence):

- **Core (in-context) memory** — structured blocks pinned to the context window (persona, user prefs, task), self-edited by the agent via tool calls. See [[Self-Editing Memory]].
- **Archival memory** — explicit knowledge in external vector/graph DBs, retrieved on demand.
- **Recall memory** — full interaction history persisted to disk, searchable.
- **Sleep-time compute** — asynchronous memory refinement by background agents during idle periods.

Letta stresses that agents are text-in/text-out: their memory is tokens in context, not learned weights — squarely the **memory-files** path, opposite [[Persona Vectors]].

## Connections

- [[MemGPT]] — the research lineage Letta commercializes
- [[Self-Editing Memory]] — core-memory blocks edited via tools
- [[Persona Vectors vs Memory Files]] — Letta is the textual pole

## Sources

- [[2025-04-28 - Mem0 - Scalable Long-Term Memory]]
- Letta blog "Agent Memory" (2025-07-07)
