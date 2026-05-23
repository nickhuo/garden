---
type: concept
title: "The Bitter Lesson"
created: 2026-05-20
updated: 2026-05-20
tags:
  - ai-agents
  - llm
  - foundational
  - architecture
status: developing
related:
  - "[[Model-Centric Architecture]]"
  - "[[Software 2.0]]"
  - "[[Agentic Harness]]"
sources:
  - "[[2019-03-13 - Sutton - The Bitter Lesson]]"
---

# The Bitter Lesson

## Summary

General methods that leverage computation — **search** and **learning** — beat methods that encode human knowledge, by a large margin, over a long enough horizon (high confidence; Source: [[2019-03-13 - Sutton - The Bitter Lesson]]). Hand-engineered knowledge gives short-term gains and long-term plateaus; the durable strategy is to build meta-methods that discover complexity from data and scale with compute. It is "bitter" because researchers repeatedly find their carefully encoded human insight overtaken by brute scaling.

## Why it matters

For agent applications it is the deepest argument for [[Model-Centric Architecture]]: every line of hand-written orchestration, routing, or content-selection logic is a candidate for replacement by a model that learns the same function (medium confidence — Sutton's evidence predates LLM agents). It reframes elaborate harnesses as temporary scaffolding rather than permanent architecture.

## Limits / when pipelines still win

- Sutton's evidence is from games and perception, not from agents with **real-world side effects**, latency budgets, or safety constraints (medium confidence). Compute does not buy you a refund on a wrongly-cancelled order.
- "Scaling wins eventually" is a statement about the long run; product teams ship in the short run, where hand-built structure measurably helps (see Nick's Donut: routing pulled out of the prompt yielded +22% workflow success, −85% invalid tool calls).
- Determinism, auditability, and hard constraints (e.g. [[MCP]] permissioning, schema validity) are guarantees a learned model cannot currently provide on its own.

## Connection to prior work

The scaling-side companion to [[Software 2.0]] (logic moves into weights) and the precursor to Sutton & Silver's experience-stream argument ([[2025 - Silver & Sutton - The Era of Experience]]). Directly in tension with the harness/schema view: [[Agentic Harness]], [[Meta-Harness]], and Manus's static-action-space argument (Source: [[2025-07-18 - Manus - Context Engineering for AI Agents]]).

## Connections

- [[Model-Centric Architecture]]
- [[Software 2.0]]
- [[Context Engineering]]
- [[Richard Sutton]]

## Open questions

- Does the lesson hold for agents where the action space has irreversible side effects?
- Is "context engineering" the new hand-engineered knowledge that scaling will eventually absorb, or a durable interface layer?

## Sources

- [[2019-03-13 - Sutton - The Bitter Lesson]]
