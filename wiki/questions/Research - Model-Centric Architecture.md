---
type: synthesis
title: "Research - Model-Centric Architecture"
created: 2026-05-20
updated: 2026-05-20
tags:
  - research
  - ai-agents
  - architecture
status: developing
related:
  - "[[Model-Centric Architecture]]"
  - "[[The Bitter Lesson]]"
  - "[[Software 2.0]]"
  - "[[Agentic Harness]]"
sources:
  - "[[2019-03-13 - Sutton - The Bitter Lesson]]"
  - "[[2017-11-11 - Karpathy - Software 2.0]]"
  - "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
---

# Research - Model-Centric Architecture

## Overview

Most agent systems treat the model as a component at the *end* of a pipeline: memory, personalization, content selection, and interface logic sit in surrounding code that orchestrates it. The **model-centric** thesis inverts this — code moves to the side, the model gets freedom to learn, the user keeps final control. This note synthesizes the foundational case (Sutton, Karpathy), the user-control case (agent advocates), and the harness/schema-centric counterweight (Anthropic, Manus, Nick's projects).

## Key Findings

1. **The scaling argument favors model-centrism (high confidence).** General methods that leverage compute — search and learning — beat hand-engineered knowledge over the long run; encoding human knowledge plateaus (Source: [[2019-03-13 - Sutton - The Bitter Lesson]], 2019). Foundational, not stale.
2. **Logic has been migrating out of code for a decade (high confidence).** Software 1.0 (rules) → 2.0 (weights) → 3.0 (prompts); the program increasingly *is* the model (Source: [[2017-11-11 - Karpathy - Software 2.0]], 2017, extended in Karpathy's 2025 "Software Is Changing Again" talk — LLM-as-OS, "decade of agents").
3. **User control is a design choice, not an automatic property (medium confidence).** The model-centric pipeline can serve platform or user interests; "agent advocates" keep the user as ultimate decision-maker with user-defined personalization (Kapoor, Kolt & Lazar, arXiv:2505.04345, 2025).
4. **The action space wants to be stable structure outside the model (medium-high confidence).** Manus argues the action space should be a stable, append-only surface the model reads from — masking over regeneration — for KV-cache stability and reliability (Source: [[2025-07-18 - Manus - Context Engineering for AI Agents]], 2025). This is structure code provides that the model should not improvise.
5. **In the short run, pulling logic OUT of the model measurably wins (high confidence, single-org).** Nick's Donut moved routing from the prompt into a deterministic retrieval call and added constrained decoding at the execute boundary: +22% workflow success, −85% invalid tool calls. "The action space is data; the prompt should never be a catalog."
6. **Schema can dominate prompts as the architectural lever (medium confidence).** Nick's Beckman: "get the schema right and the prompts become implementation detail" — hybrid neuro-symbolic planning (KG hard constraints + LLM soft rerank). Structure the model can't provide alone.

## Key Entities

- [[Richard Sutton]] — The Bitter Lesson; experience streams
- [[Andrej Karpathy]] — Software 2.0 / 3.0, LLM-as-OS
- [[brain/03_Resources/digest/sources/anthropic]] — Building Effective Agents (composable patterns, simplest-thing-that-works)
- [[Manus]] — static action space counterweight

## Key Concepts

- [[Model-Centric Architecture]]
- [[The Bitter Lesson]]
- [[Software 2.0]]
- [[Code-to-the-Side vs Orchestration]]
- [[Agentic Harness]] / [[Meta-Harness]] — the counter-pole
- [[Context Engineering]]

## Central tension

Model-centric ("code to the side, give the model freedom to learn") promises that scaling dissolves brittle orchestration into model capability. Nick's harness/schema-centric experience shows the opposite at ship time: structuring what the model *can't* reliably provide — deterministic routing, valid schemas, constrained action surfaces — produces large, measurable reliability gains. The honest reconciliation is that "code to the side" and "thick orchestration" are a slider, and the durable side-code is exactly the guarantees layer (constraints, validation, permissioning) that scaling does not absorb.

## Contradictions

- **Sutton/Karpathy vs Manus/Anthropic:** "remove hand-engineered knowledge, scale the model" vs "stabilize the action space and context, the model is unreliable without structure." Both cite real evidence; they disagree on the *time horizon* over which structure is liability vs asset.
- **Model-centric personalization vs user control:** moving memory/personalization into the model improves capability but can shift control to the platform; agent-advocate framing resists this, implying some logic *should* stay as inspectable, user-owned code.
- **Bitter Lesson scope:** Sutton's evidence is games/perception, not side-effecting agents — the transfer to agent harnesses is asserted, not demonstrated.

## Open Questions

- Where is the durable line between "scaffolding scaling absorbs" and "guarantees layer that persists"?
- Can a model self-manage memory/personalization reliably enough to dissolve the surrounding pipeline?
- Is context engineering the new hand-engineered knowledge The Bitter Lesson warns against, or a permanent interface?
- Does "user keeps final control" survive when control becomes a learned model behavior rather than an external code gate?

## Sources

- [[2019-03-13 - Sutton - The Bitter Lesson]]
- [[2017-11-11 - Karpathy - Software 2.0]]
- [[2025-07-18 - Manus - Context Engineering for AI Agents]]
- [[2025 - Silver & Sutton - The Era of Experience]] (linked; owned by another agent)
- [[Building Effective Agents]] (existing)
- Kapoor, Kolt & Lazar, "Build Agent Advocates, Not Platform Agents," arXiv:2505.04345 (2025)
