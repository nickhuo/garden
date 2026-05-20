---
type: concept
title: Routing
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

# Routing

## Summary

Workflow pattern from [[Building Effective Agents]]: classify an input and dispatch it to a specialized downstream task or model. Useful when distinct categories deserve distinct handling that would degrade if forced into one prompt.

## When to use

When inputs naturally split into categories that benefit from separate handling — and when classification is reliable enough that miscategorization is rare.

Examples (per Anthropic):
- Customer service: refund vs technical-support vs general questions → different prompts/tools
- Cost optimization: easy queries → cheap small model; hard queries → bigger model

## Connections

- Built from: [[Augmented LLM]]
- Family: [[Workflows vs Agents]]
- Cousins: [[Prompt Chaining]] · [[Parallelization]]

## Sources

- [[Building Effective Agents]] (Anthropic, 2024-12-19)
