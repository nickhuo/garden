---
type: concept
title: Prompt Chaining
created: 2026-05-04
updated: 2026-05-04
tags:
- ai-agents
- workflow-pattern
status: seed
related: []
sources:
- "[[2024-12-19 - Anthropic - Building Effective Agents]]"
_legacy_source_count: 1
---

# Prompt Chaining

## Summary

Workflow pattern from [[Building Effective Agents]]: decompose a task into a fixed sequence of LLM calls where each step processes the previous step's output. Programmatic checks ("gates") sit between steps to enforce correctness.

## When to use

When a task decomposes cleanly into fixed sequential subtasks and trading latency for accuracy is acceptable.

Examples (per Anthropic):
- Generate marketing copy → translate to target language
- Outline a doc → check outline meets criteria → write doc

## Anti-pattern

Don't use when dependencies between steps are dynamic or chain length depends on intermediate outputs — that's [[Orchestrator-Workers]] territory.

## Connections

- Built from: [[Augmented LLM]]
- Family: [[Workflows vs Agents]]
- Cousin patterns: [[Routing]] · [[Parallelization]]

## Sources

- [[Building Effective Agents]] (Anthropic, 2024-12-19)
