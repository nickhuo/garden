---
type: concept
title: Evaluator-Optimizer
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

# Evaluator-Optimizer

## Summary

Workflow pattern from [[Building Effective Agents]]: one LLM **generates**, another **evaluates and provides feedback**, in a loop until criteria are met. The dedicated evaluator role is what distinguishes this from a single-pass call.

## When to use

When clear evaluation criteria exist and iterative refinement provides measurable improvement (e.g., literary translation, complex search where deeper iteration helps, code generation with tests).

## Connections

- Built from: [[Augmented LLM]]
- Family: [[Workflows vs Agents]]
- Compares to: [[Autonomous Agents]] (which use environmental feedback rather than a separate evaluator LLM)

## Sources

- [[Building Effective Agents]] (Anthropic, 2024-12-19)
