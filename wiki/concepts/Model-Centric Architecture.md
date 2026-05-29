---
type: concept
title: "Model-Centric Architecture"
created: 2026-05-20
updated: 2026-05-20
tags:
  - ai-agents
  - llm
  - architecture
status: developing
related:
  - "[[The Bitter Lesson]]"
  - "[[Software 2.0]]"
  - "[[Agentic Harness]]"
  - "[[Context Engineering]]"
sources:
  - "[[2019-03-13 - Sutton - The Bitter Lesson]]"
  - "[[2017-11-11 - Karpathy - Software 2.0]]"
  - "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
---

# Model-Centric Architecture

> [!contradiction] Counter-pole: Heuristic Learning (Weng 2026)
> This page (with [[Software 2.0]], [[The Bitter Lesson]]) argues the model is the locus and code moves to the side. [[Heuristic Learning]] pushes the **opposite** pole: a coding agent *evolves the code itself* as the learning loop, reaching Deep-RL-competitive control without training a network. Reconciliation: the Bitter Lesson assumed hand-engineering carries human maintenance cost — HL claims coding agents flip that cost curve, so the model-vs-code slider may not slide only one way. Unresolved; both readings are currently defensible.

## Summary

An inversion of the usual agent pipeline. In most systems the model is a component at the *end* of a pipeline: memory, personalization, content selection, and interface logic sit outside it, with code orchestrating the model. The model-centric thesis flips three things (medium-high confidence):

1. **Code moves to the side** — orchestration becomes a thin boundary, not the locus of intelligence.
2. **The model gets freedom to learn** — functions previously hand-coded (routing, selection, memory management) migrate into the model.
3. **The user keeps final control** — autonomy is a user-held slider, not a platform default.

The theoretical backing is [[The Bitter Lesson]] (general learning beats hand-engineered knowledge; Source: [[2019-03-13 - Sutton - The Bitter Lesson]]) and [[Software 2.0]] (logic migrates from code into weights/prompts; Source: [[2017-11-11 - Karpathy - Software 2.0]]). The user-control leg draws on the "agent advocate, not platform agent" argument: agents should represent user interests with the user as ultimate decision-maker (medium confidence; Kapoor, Kolt & Lazar 2025).

## Why it matters

It predicts that today's elaborate harnesses are transitional. As models improve, hand-built routing and content-selection logic become liabilities — brittle, stale, and outscaled. For agent products it argues for investing in model capability and clean action surfaces over thick orchestration code.

## Limits / when pipelines still win

- **Side effects and guarantees.** Agents touch the real world; deterministic boundaries (constrained decoding, [[MCP]] permissioning, schema validation) provide guarantees a model cannot self-supply (high confidence).
- **The static-action-space counterweight.** Manus argues the action space should be a *stable, append-only* surface the model reads from, not regenerated per turn — KV-cache stability and reliability demand structure outside the model (Source: [[2025-07-18 - Manus - Context Engineering for AI Agents]]).
- **Schema as senior lever.** Nick's Beckman: get the schema right and prompts become implementation detail — structure the model can't provide alone, encoded as KG hard constraints + LLM soft rerank.
- **The empirical short run.** Donut moved routing *out* of the prompt into a deterministic retrieval call ("the action space is data; the prompt should never be a catalog") and constrained decoding at the execute boundary: +22% workflow success, −85% invalid tool calls. This is code-to-the-side winning *against* a model-only approach.

> [!gap] The boundary between "scaffolding scaling will absorb" and "durable interface layer" is unresolved. Context engineering and schemas may be the new hand-engineered knowledge The Bitter Lesson warns against — or a permanent control/safety layer. Both readings are currently defensible.

## Connection to prior work

- **Pure model-centric pole:** [[The Bitter Lesson]], [[Software 2.0]], [[2025 - Silver & Sutton - The Era of Experience]] (agents learn from experience streams, not curated scaffolding).
- **Harness/schema-centric pole:** [[Agentic Harness]], [[Meta-Harness]], [[Context Engineering]], [[Building Effective Agents]] (Anthropic's "simplest thing that works," composable patterns over autonomy), and Manus's static action space ([[Manus]]).
- Nick's projects sit at the pole: **Donut** (routing as deterministic data retrieval), **Beckman** (schema as senior lever, neuro-symbolic planning), **Compass** (multi-model routing + opt-in Thinking Mode cost ceiling) all add structure the model does not provide alone.

## Connections

- [[The Bitter Lesson]]
- [[Software 2.0]]
- [[Agentic Harness]]
- [[Meta-Harness]]
- [[Context Engineering]]
- [[Building Effective Agents]]
- [[Manus]]
- [[Workflows vs Agents]]

## Open questions

- Where exactly is the line between "code to the side" (thin, durable) and "code orchestrating the model" (thick, transitional)?
- Can a model self-manage memory and personalization reliably enough to dissolve the surrounding pipeline, or does scoped persistent memory stay infrastructure?
- Does "user keeps final control" survive when control itself becomes a learned model behavior?

## Sources

- [[2019-03-13 - Sutton - The Bitter Lesson]]
- [[2017-11-11 - Karpathy - Software 2.0]]
- [[2025-07-18 - Manus - Context Engineering for AI Agents]]
