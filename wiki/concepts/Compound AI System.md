---
type: concept
title: Compound AI System
created: 2026-05-30
updated: 2026-05-30
tags: [llm, ai-agents, prompt-optimization, architecture]
status: developing
complexity: intermediate
domain: ai-agents
aliases: ["Compound AI Systems", "Modular LLM System", "Language Program"]
related: ["[[DSPy]]", "[[GEPA]]", "[[Prompt Optimization]]", "[[Multi-Agent Systems]]", "[[ReAct]]", "[[Workflows vs Agents]]", "[[Augmented LLM]]"]
sources: ["[[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]"]
---

# Compound AI System

A **modular system composed of one or more LLM invocations**, potentially interleaved with external tool calls, orchestrated through arbitrary control flow. The abstraction subsumes agents, [[Multi-Agent Systems|multi-agent systems]], and scaffolding techniques like [[ReAct]] and Archon ([[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]; formalism from the [[DSPy]] line of work).

## Formalism

A system is `Φ = (M, C, X, Y)`:

- `M = ⟨M_1, …, M_|M|⟩` — **language modules**. Each `M_i = (π_i, θ_i, X_i, Y_i)`: prompt `π_i` (instructions + few-shot demos), weights `θ_i`, and input/output schemas.
- `C` — **control-flow logic** that sequences and invokes modules (conditionally, in loops, via tool APIs).
- `X, Y` — global input/output schemas.

The **learnable parameters** are `⟨Π, Θ⟩_Φ` — the collection of module prompts and weights. Optimization maximizes expected metric `µ` over a task distribution, optionally subject to a **rollout budget** `B` (the sample-efficient regime, where each rollout is monetarily/computationally expensive).

## Why the abstraction matters

It lets optimizers that work in *different parameter spaces* be compared head-to-head:

- **Prompt-space** optimizers tune `Π`: [[GEPA]], MIPROv2, TextGrad.
- **Weight-space** optimizers tune `Θ`: [[GRPO]], [[LoRA]], [[On-Policy Distillation]].

This is the conceptual frame behind the GEPA-vs-GRPO comparison: same system `Φ`, different slice of `⟨Π, Θ⟩` updated, measured against the same metric and budget.

## Connections

- **[[DSPy]]** — the framework that operationalizes this formalism and ships optimizers for it.
- **[[Workflows vs Agents]]** / **[[Augmented LLM]]** — `C` is exactly what distinguishes a fixed workflow from an agent that chooses its own control flow.
- **[[Multi-Agent Systems]]** — a special case where modules are themselves agents.

## Sources

- [[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]
