---
type: concept
title: "Code-to-the-Side vs Orchestration"
created: 2026-05-20
updated: 2026-05-20
tags:
  - ai-agents
  - architecture
status: seed
related:
  - "[[Model-Centric Architecture]]"
  - "[[Agentic Harness]]"
  - "[[Workflows vs Agents]]"
sources:
  - "[[2017-11-11 - Karpathy - Software 2.0]]"
  - "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
---

# Code-to-the-Side vs Orchestration

## Summary

Two stances on where code sits relative to the model in an agent (medium confidence):

- **Orchestration (model-as-component):** code drives the system, calling the model as one step in a predefined sequence; routing, memory, and selection live in code. This is the [[Workflows vs Agents]] "workflow" pole and most production pipelines today.
- **Code-to-the-side (model-centric):** the model drives; code becomes a thin boundary providing tools, guarantees, and a stable action surface. The model decides flow; code constrains side effects. This is the [[Model-Centric Architecture]] pole.

The distinction is not binary but a slider. Anthropic's [[Building Effective Agents]] frames it as: use the simplest composable pattern that works, escalating from orchestrated workflows to autonomous agents only when the task demands it.

## Why it matters

Naming the slider clarifies the central debate: as models improve, weight shifts from orchestration toward code-to-the-side — but the *boundary* code (constrained decoding, schema validation, permissioning) is exactly what does not dissolve.

## Limits / when pipelines still win

When tasks have irreversible side effects, hard constraints, or strict latency/cost ceilings, orchestration retains measurable advantages — see Nick's Donut and Beckman, and Manus's static-action-space argument ([[2025-07-18 - Manus - Context Engineering for AI Agents]]).

## Connection to prior work

A practical lens on [[The Bitter Lesson]] vs [[Agentic Harness]]: which slider position scaling rewards.

## Connections

- [[Model-Centric Architecture]]
- [[Agentic Harness]]
- [[Meta-Harness]]
- [[Workflows vs Agents]]
- [[Building Effective Agents]]

## Open questions

- Does the orchestration layer shrink monotonically as models improve, or stabilize at a guarantees-only floor?

## Sources

- [[2017-11-11 - Karpathy - Software 2.0]]
- [[2025-07-18 - Manus - Context Engineering for AI Agents]]
