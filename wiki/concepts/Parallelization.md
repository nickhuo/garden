---
type: concept
title: Parallelization
created: 2026-05-04
updated: 2026-05-04
tags:
- ai-agents
- workflow-pattern
status: seed
related: []
sources:
- "[[2024-12-19 - Anthropic - Building Effective Agents]]"
- "[[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]]"
_legacy_source_count: 1
---

# Parallelization

## Summary

Workflow pattern from [[Building Effective Agents]]: an LLM works on a task in parallel via two sub-patterns — **sectioning** (splitting one task into independent subtasks) or **voting** (running the same task multiple times for diverse outputs aggregated by consensus).

## Sub-patterns

- **Sectioning** — independent subtasks aggregated programmatically (e.g., one model writes, another evaluates safety)
- **Voting** — same prompt run N times, results aggregated (e.g., code vulnerability scans where higher recall matters; consensus answers)

## When to use

When subtasks are independent (sectioning) or quality benefits from diverse perspectives / multiple attempts (voting).

## Large-scale instantiation: the C compiler experiment

[[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]] is the most concrete large-scale demonstration of the sectioning sub-pattern. Anthropic built a working C compiler by assigning one parallel Claude agent per compiler phase (lexer, parser, semantic analysis, code generation). Key addition to the pattern: **interface contracts** as the coordination primitive — the orchestrator defines specs before workers begin, enabling true isolation. The integration/reconciliation phase is a non-trivial cost that must be budgeted. See also [[Orchestrator-Workers]] for the orchestrator pattern that governs this setup.

## Connections

- Built from: [[Augmented LLM]]
- Family: [[Workflows vs Agents]]
- Compares to: [[Orchestrator-Workers]] (orchestrator decides decomposition dynamically; parallelization decomposes statically)
- Large-scale example: [[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]]

## Sources

- [[Building Effective Agents]] (Anthropic, 2024-12-19)
- [[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]] (Anthropic, 2026-05)
