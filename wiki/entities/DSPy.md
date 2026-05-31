---
type: entity
title: DSPy
created: 2026-05-30
updated: 2026-05-30
tags: [llm, ai-agents, prompt-optimization, framework]
status: seed
entity_type: framework
related: ["[[Omar Khattab]]", "[[Compound AI System]]", "[[GEPA]]", "[[MIPRO]]", "[[Prompt Optimization]]"]
sources: ["[[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]", "[[2024-06 - Opsahl-Ong et al - MIPRO Optimizing Instructions and Demonstrations]]"]
---

# DSPy

A framework for programming — rather than prompting — **[[Compound AI System|compound AI systems]]**, created by **[[Omar Khattab]]** and collaborators (Khattab et al. 2022, 2024). It treats an LLM pipeline as a set of **modules** with learnable parameters (prompts and/or weights) and provides **optimizers** that tune them against a metric.

## Optimizer lineage

DSPy's optimizers are the direct ancestors of the [[GEPA]] work:

- **Few-shot bootstrapping** — search/select demonstrations.
- **[[MIPRO|MIPROv2]]** ([[Krista Opsahl-Ong|Opsahl-Ong]] et al. 2024) — jointly optimizes instructions + few-shot examples via Bayesian optimization (TPE). The SOTA baseline GEPA beats. See [[2024-06 - Opsahl-Ong et al - MIPRO Optimizing Instructions and Demonstrations]].
- **[[GEPA]]** (2026) — reflective evolutionary prompt optimization; instruction-only, Pareto-guided. The newest member of the family.

The shared formalism: a system `Φ = (M, C, X, Y)` with modules `M_i = (π_i, θ_i, X_i, Y_i)`; optimizers search over module prompts `Π` and/or weights `Θ`.

## Connections

- [[Compound AI System]] — the abstraction DSPy operationalizes.
- [[Prompt Optimization]] — DSPy is the canonical home of automatic prompt optimizers.
- Contrast with weight-space adaptation: [[GRPO]], [[LoRA]], [[On-Policy Distillation]].
