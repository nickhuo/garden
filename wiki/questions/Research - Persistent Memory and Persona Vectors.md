---
type: synthesis
title: "Research - Persistent Memory and Persona Vectors"
created: 2026-05-20
updated: 2026-05-20
tags: [research, llm, ai-agents, memory, persona-vectors]
status: developing
related: ["[[Persona Vectors]]", "[[Memory Stream]]", "[[Activation Steering / Representation Engineering]]", "[[Persona Vectors vs Memory Files]]", "[[Letta]]"]
sources: ["[[2025-07-29 - Chen et al - Persona Vectors]]", "[[2023-04-07 - Park et al - Generative Agents]]", "[[2023-10-12 - Zou et al - Representation Engineering]]", "[[2025-04-28 - Mem0 - Scalable Long-Term Memory]]"]
---

## Overview

What an AI agent learns must persist across conversations. Two complementary paths carry that persistence: **(a) persona vectors** — learned state in a form that conditions the model directly (parametric / activation-space), and **(b) memory files** — a textual, inspectable representation of what was learned (non-parametric / contextual). They differ on one axis above all: **control vs inspectability**.

## Key Findings

1. A persona vector is a *causal linear direction* in activation space encoding a character trait, extracted automatically by contrasting trait-eliciting vs trait-suppressing prompts (Source: [[2025-07-29 - Chen et al - Persona Vectors]], high).
2. Inference-time steering reduces a trait but degrades capability; **preventative steering during finetuning** inoculates against bad-persona acquisition while preserving MMLU — the recommended control method (Source: [[2025-07-29 - Chen et al - Persona Vectors]], high).
3. Persona vectors descend directly from Representation Engineering — same contrast-vector / LAT machinery, specialized to traits and the training loop (Source: [[2023-10-12 - Zou et al - Representation Engineering]], high).
4. The memory-files path is canonically the **memory stream**: append-only natural-language log, retrieval scored by recency × importance × relevance, periodic reflection synthesizing higher-level inferences (Source: [[2023-04-07 - Park et al - Generative Agents]], high).
5. Productized memory splits into a *layer* (Mem0, bolt-on store) vs a *runtime* (Letta, owns the loop and treats memory as editable in-context state); both are non-parametric (Source: [[2025-04-28 - Mem0 - Scalable Long-Term Memory]], [[Letta]], medium).
6. Surveys formalize the whole space as **parametric (in-weights)** vs **contextual/non-parametric** memory — exactly the persona-vectors-vs-memory-files axis (Source: [[2025-04-28 - Mem0 - Scalable Long-Term Memory]], medium).

## The tradeoff (2-3 lines)

Persona vectors give **direct, model-internal control** over *who the agent is* at the cost of **inspectability** — you must probe with a vector to read them. Memory files give **full inspectability** of *what the agent knows* at the cost of **direct control** — influence is mediated by retrieval and prompt assembly. Robust agents use both; the design question is which path each piece of "what was learned" belongs on.

## Key Entities

- [[Letta]] — runtime productizing MemGPT; memory-files pole
- [[brain/03_Resources/digest/sources/anthropic]] — origin of persona vectors

## Key Concepts

- [[Persona Vectors]] · [[Activation Steering / Representation Engineering]] · [[Memory Stream]] · [[Persona Vectors vs Memory Files]]
- Existing, linked: [[Agent Memory Taxonomy]], [[Self-Editing Memory]], [[MemGPT]], [[CoALA]], [[Session as Event Log]], [[Context Engineering]], [[Just-in-Time Context Retrieval]], [[Long-Horizon Context Management]]

## Connection to Nick's work

Beckman implements both poles by hand, interpretably: the per-learner **mastery overlay** is a structured memory-file (*what this learner knows*) decoupled from the global KG (*what the world is*) — two schemas, two cadences; the **metacognition fit** `PL = C + A·Ease + B·Novelty` with per-learner `(A,B,C)` is an interpretable persona-vector analogue. Nick's *schema-is-the-lever* stance is the actionable form of the inspectability/control tradeoff. Baidu's K-means segmentation is the unsupervised route to constructing persona archetypes.

## Contradictions

- **Steering vs fine-tuning effectiveness**: persona-vectors work treats post-hoc steering as capability-degrading (favoring preventative steering), while 2025 steering literature claims activation steering is "approximately as effective as fine-tuning." Reconcilable — the latter measures behavioral effect, the former flags a capability tax; both can be true (medium).
- **Memory as layer vs runtime**: Mem0 (bolt-on) vs Letta (owns the loop) embody competing productization theses; no neutral head-to-head benchmark exists yet.

## Open Questions

- When should a stable memory-file fact be promoted into weights / a persona vector (parametric consolidation)?
- Can a per-user persona vector be made as inspectable as Beckman's coefficients?
- Optimal forgetting/compression for an unbounded memory stream beyond reflection?

## Suggested edits to existing pages

- **[[Agent Memory Taxonomy]]** — add the parametric vs contextual (persona-vectors vs memory-files) top-level split as the organizing axis; link [[Persona Vectors]].
- **[[Self-Editing Memory]]** — note this is the memory-files pole; cross-link [[Persona Vectors vs Memory Files]] and [[Letta]] (core-memory blocks).
- **[[MemGPT]]** — add [[Letta]] as the productized runtime descendant; cross-link [[Memory Stream]] as ancestor.
- **[[Session as Event Log]]** — link [[Memory Stream]] as the natural-language generalization of the event log.

## Sources

- [[2025-07-29 - Chen et al - Persona Vectors]]
- [[2023-04-07 - Park et al - Generative Agents]]
- [[2023-10-12 - Zou et al - Representation Engineering]]
- [[2025-04-28 - Mem0 - Scalable Long-Term Memory]]
