---
type: concept
title: Orchestrator-Workers
created: 2026-05-04
updated: 2026-05-04
tags:
- ai-agents
- workflow-pattern
- agent-pattern
status: developing
related: []
sources:
- "[[2024-12-19 - Anthropic - Building Effective Agents]]"
- "[[2025-06-13 - Anthropic - How we built our multi-agent research system]]"
- "[[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]]"
- "[[2026-04-08 - Anthropic - Scaling Managed Agents]]"
_legacy_source_count: 3
---

# Orchestrator-Workers

## Summary

A coordinator LLM dispatches subtasks to worker LLMs and synthesizes their outputs. **Two distinct variants** based on how dispatching works — distinguishing them matters because they have different cost, error, and use-case profiles. The two Anthropic posts that ground this page treat the pattern differently; both are valid usages of the term.

## Variant 1 — Workflow variant

**Static dispatch over dynamic content.** The orchestrator chooses among **predefined subtasks** along **predefined code paths**. Decomposition is dynamic at the *content* level (which file to edit, which subquery to run) but the worker roles and tools are fixed.

Per [[Building Effective Agents]] — this is the original "orchestrator-workers" workflow pattern.

**Use when:** structure of decomposition isn't known ahead of time but the *space* of subtasks is bounded.

## Variant 2 — Agent variant (multi-agent loop)

**Dynamic spawning.** The orchestrator (LeadResearcher in [[How we built our multi-agent research system]]) **decides at runtime how many subagents to spawn, what each is for, and which tools each gets**. Subagents run with isolated contexts; outputs flow back via shared artifact filesystem to bypass coordinator bottleneck.

This is closer to [[Autonomous Agents]] than to a workflow — the LLM, not code, owns the structure.

**Use when:** problem is open-ended, breadth-first, exceeds single context window, and clears [[Token Economics]] threshold (~15× chat tokens).

## Distinguishing the variants

| | Workflow variant | Agent variant |
|---|---|---|
| Subtask roles | Predefined | Spawned at runtime |
| Worker count | Fixed | Dynamic |
| Tools per worker | Fixed | Decided by orchestrator |
| Cost multiplier (vs chat) | ~2–4× | ~15× |
| Best for | Coding, sectional analysis | Research, breadth-first |
| Family | [[Workflows vs Agents]] (workflow side) | [[Multi-Agent Systems]] |

## Interface contracts as coordination primitive (per Anthropic 2026-05)

[[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]] adds a concrete mechanism to Variant 1 (workflow variant): **interface contract definition by the orchestrator before workers begin**. Workers receive only the interface spec + relevant domain material — not the full project context — enabling true isolation. Integration (reconciliation of outputs) is a discrete, budgeted phase, not implicit in the workflow. This suggests interface spec quality is the primary lever the orchestrator controls; poorly-specified contracts compound into costly reconciliation rounds.

## Stateless cattle (per Anthropic 2026-04)

[[Scaling Managed Agents]] reframes the orchestrator role: under a [[Meta-Harness]], the orchestrator (harness + brain combined) becomes **stateless and reprovisionable** — failures recover by re-spawning, not by nursing state back. State lives in [[Session as Event Log]], not in the orchestrator process. This applies equally to both variants but matters more for the agent variant where lead-agent crashes were previously catastrophic.

## OpenAI's vocabulary: the Manager pattern

OpenAI's [[2025 - OpenAI - A Practical Guide to Building Agents]] names essentially this pattern the **[[Manager Pattern]]** ("agents as tools"): a central manager calls specialized agents *as tools* and synthesizes their results, keeping control and user access. It maps most closely to **Variant 1** (specialists are predefined, invoked synchronously and returning to the manager), though it can host runtime-dynamic selection. Its decentralized sibling, [[Agent Handoffs]], corresponds to [[Routing]] taken to peer-to-peer transfer. See [[OpenAI Practical Guide vs Anthropic Building Effective Agents]].

## Connections

- Built from: [[Augmented LLM]]
- Family: [[Workflows vs Agents]]
- OpenAI vocabulary: [[Manager Pattern]] (agents-as-tools)
- Agent variant generalizes to: [[Multi-Agent Systems]]
- Compares to: [[Parallelization]] (static, no orchestrator) · [[Autonomous Agents]] (no fixed orchestrator role; the model is the orchestrator throughout)
- Runtime: [[Meta-Harness]] · [[Managed Agents]] (stateless cattle pattern)

## Open questions

- Where exactly is the boundary — at what point does a "workflow with dynamic dispatch" become "an agent loop"? Anthropic's two posts position this differently and the operational implications (cost, predictability, eval methodology) are large.
- Are there hybrid configurations (static spawning + dynamic tool selection) that capture the cost profile of variant 1 with the flexibility of variant 2?

## Sources

- [[Building Effective Agents]] (Anthropic, 2024-12-19) — workflow variant
- [[How we built our multi-agent research system]] (Anthropic, 2025-06-13) — agent variant
- [[Scaling Managed Agents]] (Anthropic, 2026-04-08) — stateless-cattle pattern
