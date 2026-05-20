---
type: concept
title: Augmented LLM
created: 2026-05-04
updated: 2026-05-04
tags:
- ai-agents
- primitives
status: developing
related: []
sources:
- "[[2024-12-19 - Anthropic - Building Effective Agents]]"
- "[[2025-06-13 - Anthropic - How we built our multi-agent research system]]"
- "[[2025-09-29 - Anthropic - Effective context engineering for AI agents]]"
- "[[2026-04-08 - Anthropic - Scaling Managed Agents]]"
- "[[2024-09-19 - Anthropic - Contextual Retrieval]]"
_legacy_source_count: 4
---

# Augmented LLM

## Summary

The base primitive in [[Building Effective Agents]]: a single LLM call enhanced with **retrieval**, **tools**, and **memory**. Every workflow and agent pattern is composed of augmented LLMs interacting.

## Definition (Anthropic)

> "The basic building block of agentic systems is an LLM enhanced with augmentations such as retrieval, tools, and memory. Our current models can actively use these capabilities — generating their own search queries, selecting appropriate tools, and determining what information to retain."

## Why it matters

The post's core thesis: a well-prompted Augmented LLM with retrieval and in-context examples handles most production use cases without any orchestration on top. Don't reach for Workflows or Agents until the Augmented LLM provably falls short.

## Memory pattern (per Anthropic 2025-06)

In [[How we built our multi-agent research system]], Anthropic surfaces an explicit pattern for the **memory** dimension: when a plan or context exceeds the model's context window (200K), the agent **persists state to an external store** (filesystem, database, dedicated memory service) and re-reads on demand. This is more than "remember the last turn" — it's plan persistence so long-running agents can survive context truncation.

Implications:
- Memory becomes a first-class augmentation, not a passive log.
- The artifact-system pattern (subagents writing outputs to filesystem) is a concrete instance — outputs flow through the memory layer instead of through the coordinator.

## Context engineering perspective (per Anthropic 2025-09)

The three augmentations (retrieval, tools, memory) are not equally weighted at runtime — they each consume different slices of the **attention budget** introduced in [[Context Engineering]]. Two operational shifts from [[Effective context engineering for AI agents]]:

- **Retrieval becomes [[Just-in-Time Context Retrieval]]** — the agent holds lightweight identifiers and pulls data via tools, not pre-loaded embeddings. The "retrieval" augmentation now means "the ability to look something up," not "the things already loaded."
- **Memory becomes a long-horizon discipline** — see [[Long-Horizon Context Management]]. Compaction, structured note-taking, and sub-agent decomposition are operational techniques on top of the memory leg.

## Memory layer concretized (per Anthropic 2026-04)

[[Scaling Managed Agents]] gives the memory leg its most concrete form yet: [[Session as Event Log]] — a system-managed, append-only event log that lives outside the brain's context window. The "memory" augmentation is no longer abstract; it's a durable substrate the runtime owns, surfaced to the brain via `getEvents()`. This collapses three earlier framings (in-context history, agent-managed `NOTES.md`, ephemeral scratchpads) into one canonical layer underneath them all.

## Connections

- Used by all of: [[Prompt Chaining]] · [[Routing]] · [[Parallelization]] · [[Orchestrator-Workers]] · [[Evaluator-Optimizer]] · [[Autonomous Agents]] · [[Multi-Agent Systems]]
- Tool layer protocol: [[MCP]]
- Tool design discipline: [[ACI - Agent-Computer Interface]]
- Context budget framing: [[Context Engineering]] · [[Token Economics]]
- Retrieval pattern: [[Just-in-Time Context Retrieval]] · [[Contextual Retrieval]] · [[BM25 and Hybrid Retrieval]] · [[Reranking]]
- Memory pattern: [[Long-Horizon Context Management]] · [[Session as Event Log]]
- Runtime substrate: [[Meta-Harness]] · [[Managed Agents]]

## Open questions

- Where does retrieval-quality dominate vs prompt-quality vs tool-quality? No source has resolved the hierarchy.
- How does memory mechanism (in-context vs external store vs fine-tuning) change which patterns are appropriate?
- Is filesystem-as-memory durable, or a stopgap until purpose-built memory services mature?
- Do the three augmentations remain the right decomposition as context windows grow to 1M+? (The "retrieval" leg may collapse into "memory" if everything fits.)

## Sources

- [[Building Effective Agents]] (Anthropic, 2024-12-19)
- [[How we built our multi-agent research system]] (Anthropic, 2025-06-13)
- [[Effective context engineering for AI agents]] (Anthropic, 2025-09-29)
- [[Scaling Managed Agents]] (Anthropic, 2026-04-08)
