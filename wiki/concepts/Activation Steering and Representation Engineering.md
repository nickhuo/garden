---
type: concept
title: "Activation Steering / Representation Engineering"
created: 2026-05-20
updated: 2026-05-20
tags: [llm, ai-agents, memory, persona-vectors, interpretability, alignment]
status: developing
related: ["[[Persona Vectors]]", "[[Persona Vectors vs Memory Files]]"]
sources: ["[[2023-10-12 - Zou et al - Representation Engineering]]", "[[2025-07-29 - Chen et al - Persona Vectors]]"]
aliases: ["Activation Steering / Representation Engineering", "Representation Engineering", "Activation Steering"]
---

## Summary

**Representation Engineering (RepE)** is a top-down interpretability approach that centers population-level representations rather than individual neurons or circuits (Source: [[2023-10-12 - Zou et al - Representation Engineering]], high confidence). It finds a linear **reading vector** for a concept via Linear Artificial Tomography (contrasting activations across stimuli), then **controls** behavior by injecting a contrast/steering vector into the residual stream at inference — no weight update.

**Activation steering** is the control half: amplify or suppress a concept by adding its direction at runtime. Steering is approximately as effective as fine-tuning for many behaviors (medium confidence; from later steering literature, 2025).

## Why it matters

This is the mechanism beneath [[Persona Vectors]] and the general lever for the learned-state path of persistence. For agents it offers a third modification surface beyond weights (RL/SFT) and prompts (context engineering): intervene on activations directly. Belief-dynamics work (2025) frames steering as changing concept *priors* while in-context learning *accumulates evidence* — same destination, different mechanism (medium).

## Limits

> [!gap] Original paper is "initial analysis." Sample-efficiency vs generalization tradeoff: contrastive methods (CAA) are robust to few samples but weak signal; parameter-tuning methods (ReFT) generalize but need hundreds of examples. Steering can cost capability.

## Connection to prior work

Direct ancestor of [[Persona Vectors]]. Complements [[Context Engineering]] and [[Just-in-Time Context Retrieval]] (prompt-side levers) by operating one level lower, on activations.

## Connections

- [[Persona Vectors]] — trait-specific application
- [[Context Engineering]] — the prompt-side alternative lever
- [[Persona Vectors vs Memory Files]]

## Open questions

- When is activation steering preferable to a memory file or a finetune for persistent agent behavior?
- How stable are steering vectors across model updates?

## Sources

- [[2023-10-12 - Zou et al - Representation Engineering]]
- [[2025-07-29 - Chen et al - Persona Vectors]]
