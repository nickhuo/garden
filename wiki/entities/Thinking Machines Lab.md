---
type: entity
title: "Thinking Machines Lab"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - entity
  - organization
status: developing
entity_type: organization
role: "AI research lab; publishes the Connectionism blog with technical work on LLM training, inference, optimization, and human-AI interaction"
first_mentioned: 2026-05-14
aliases:
  - "TML"
related:
  - "[[Interaction Models]]"
  - "[[On-Policy Distillation]]"
  - "[[LoRA]]"
  - "[[Batch Invariance]]"
  - "[[Manifold Optimization]]"
sources:
  - "[[2026-05-11 - Thinking Machines - Interaction Models]]"
  - "[[2025-10-27 - Lu - On-Policy Distillation]]"
  - "[[2025-09-29 - Schulman - LoRA Without Regret]]"
  - "[[2025-09-26 - Bernstein - Modular Manifolds]]"
  - "[[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]]"
---

# Thinking Machines Lab

Research lab publishing the *Connectionism* blog. Outputs concentrate on the **numerical and architectural foundations** of LLM training and inference, plus human-AI interaction architecture.

## Researchers in the wiki

- [[John Schulman]] — co-founder, LoRA work
- [[Horace He]] — kernels & determinism
- [[Kevin Lu]] — on-policy distillation
- [[Jeremy Bernstein]] — manifold optimization
- Plus collaborators (Tinker API, batch_invariant_ops repo)

## Themes across their work

A consistent throughline: **take numerics seriously**.

- [[Defeating Nondeterminism in LLM Inference]] — fix batch-invariance to make T=0 reproducible
- [[Modular Manifolds]] — constrain weights to submanifolds so optimization respects geometry
- [[On-Policy Distillation]] — implicitly load-bearing on trainer-sampler determinism
- [[Interaction Models]] — uses bitwise trainer-sampler alignment as a stability tool, <5% perf cost
- [[LoRA Without Regret]] — fits in by giving precise conditions where parameter-efficient FT is indistinguishable from FullFT

The lab's stance is that infra and theory issues that ML culture usually papers over are worth fixing properly.

## Products / artifacts referenced

- **Tinker** — training API used in distillation work
- **batch_invariant_ops** — open-source batch-invariant PyTorch kernels (vLLM integration)
- **TML-Interaction-Small** — 276B params, 12B active, real-time multimodal model
- **Modula** ([modula.systems](https://modula.systems/)) — module-graph implementation referenced from Modular Manifolds
- Contributions upstream: SGLang persistent streaming sessions

## Sources

See `sources:` frontmatter — 5 Connectionism blog posts from Sep 2025 – May 2026.
