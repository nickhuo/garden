---
type: concept
title: "Persona Vectors vs Memory Files"
created: 2026-05-20
updated: 2026-05-20
tags: [llm, ai-agents, memory, persona-vectors, memory-stream]
status: developing
related: ["[[Persona Vectors]]", "[[Memory Stream]]", "[[Activation Steering / Representation Engineering]]", "[[Self-Editing Memory]]", "[[Agent Memory Taxonomy]]"]
sources: ["[[2025-07-29 - Chen et al - Persona Vectors]]", "[[2023-04-07 - Park et al - Generative Agents]]", "[[2025-04-28 - Mem0 - Scalable Long-Term Memory]]"]
---

## Summary

What an AI system learns must persist across conversations. Two complementary paths (high confidence):

| Axis | Persona vectors (learned state) | Memory files (textual) |
|---|---|---|
| Form | Linear direction in activation space | Natural-language / structured records |
| Survey term | Parametric / in-weights conditioning | Non-parametric / contextual |
| Encodes | *Who the agent is* (traits, style) | *What the agent knows* (facts, events) |
| Inspectable? | Low — must probe with a vector | High — read it directly |
| Editable by | Steering / finetuning | Append, retrieve, self-edit ([[Self-Editing Memory]]) |
| Control precision | High, model-internal | Indirect, mediated by retrieval + prompt |
| Failure mode | Silent drift; capability tax on steering | Unbounded growth; stale/contradictory entries |

Surveys split memory the same way: **parametric** (encoded in weights — persona-vector / finetuning path) vs **contextual/non-parametric** (external text, tables, graphs — memory-files path) (Source: [[2025-04-28 - Mem0 - Scalable Long-Term Memory]], medium).

## Why it matters

The two are complementary, not competing. Persona vectors give precise, model-level control over character but are opaque; memory files are auditable but exert only indirect influence. A robust agent uses both: a persona layer for stable identity/values, a memory layer for accumulated facts.

## The core tradeoff (inspectability vs control)

Persona vectors buy **direct control at the cost of inspectability**; memory files buy **inspectability at the cost of direct control**. Where you put a given piece of "what was learned" is a design choice about how much you need to audit it vs how tightly you need to condition on it.

## Connection to Nick's work — "schema is the lever"

Beckman already implements both poles, hand-built and interpretable:
- **Memory-files pole** — the per-learner mastery overlay (structured record of *what this learner knows*), decoupled from the global KG metadata (*what the world is*). Two schemas, two update cadences.
- **Persona-vectors pole** — the metacognition fit `PL = C + A·Ease + B·Novelty`, where `(A, B, C)` are per-learner coefficients used as rendering knobs. A fully interpretable persona-vector analogue.

Nick's stance — *the schema is the lever* — is the actionable version of the inspectability/control tradeoff: by hand-designing the overlay schema and the coefficient form, he keeps both poles auditable, trading raw model-internal control for transparency. Baidu's K-means user segmentation (unsupervised persona archetypes) is the data-driven route to constructing such persona state.

## Connections

- [[Persona Vectors]] · [[Memory Stream]] · [[Activation Steering / Representation Engineering]]
- [[Agent Memory Taxonomy]] — parametric vs contextual fits its top split

## Open questions

- When to consolidate a stable memory-file fact into a persona vector / finetune (the parametric promotion question)?
- Can a learner-specific persona vector be made as inspectable as Beckman's coefficients?

## Sources

- [[2025-07-29 - Chen et al - Persona Vectors]]
- [[2023-04-07 - Park et al - Generative Agents]]
- [[2025-04-28 - Mem0 - Scalable Long-Term Memory]]
