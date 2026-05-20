---
type: domain
title: LLM
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - domain
status: seed
related:
  - "[[Thinking Machines Lab]]"
sources: []
---

# LLM — Overview

Model internals, training, inference, evaluation, alignment. Karpathy-centric seed intent per `CLAUDE.md`, but **first instantiation is a 5-source pulse from [[Thinking Machines Lab]]** on the numerical and architectural foundations of training and inference.

A 60-second read of "what does this wiki think about LLMs as of 2026-05-14." See [[index]] for the full catalog.

## Current shape (after 5 sources)

All five from [[Thinking Machines Lab]]'s *Connectionism* blog, Sep 2025 – May 2026. A coherent through-line: **take numerics seriously**.

### Training & post-training
- [[2025-10-27 - Lu - On-Policy Distillation]] — student samples + teacher per-token reverse-KL = 9-30x cost reduction vs SFT/RL on AIME'24. Introduces [[On-Policy Distillation]], [[Reverse KL Divergence]].
- [[2025-09-29 - Schulman - LoRA Without Regret]] — [[LoRA]] is indistinguishable from FullFT when applied to all layers (especially MLP/MoE), at moderate batch sizes, and within capacity. Rank-1 suffices for policy-gradient RL. 10x LR rule.

### Inference & infrastructure
- [[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]] — root cause of T=0 nondeterminism is [[Batch Invariance]] failure, not concurrency. Fix the kernels, get reproducible inference + true on-policy RL. Introduces [[Floating-Point Non-Associativity]], [[Trainer-Sampler Determinism]].

### Optimization theory
- [[2025-09-26 - Bernstein - Modular Manifolds]] — constrain weights to submanifolds (Stiefel) + co-design optimizer. [[Manifold Muon]] beats AdamW on small CIFAR-10. Modular composition algebra for per-layer LR budgets.

### Architecture
- [[2026-05-11 - Thinking Machines - Interaction Models]] — real-time multimodal is an architecture problem, not an interface problem. 200ms micro-turns, encoder-free early fusion, persistent streaming sessions. Introduces [[Interaction Model Architecture]]. Uses bitwise [[Trainer-Sampler Determinism]] as a stability tool.

## Key cross-references

Three of the five papers depend on or interlock with each other:

- [[Defeating Nondeterminism in LLM Inference]] is the **infrastructure layer** under both [[On-Policy Distillation]] (clean reverse-KL signal needs sampler-trainer match) and [[Interaction Models]] (<5% perf cost for stability).
- [[Modular Manifolds]] and [[Defeating Nondeterminism]] share a stance: ML culture papers over numerical issues; both argue those issues are buyable with engineering.
- [[LoRA Without Regret]] connects to [[On-Policy Distillation]] via the RL angle (rank-1 LoRA works because policy gradient absorbs ~1 bit/episode).

## Active threads

- TML's full publication backlog from 2025 — likely worth ingesting in order
- Karpathy-centric LLM seed (training videos, gist patterns) — still not started
- The "co-design architecture and optimizer" thesis as a [[theses]] page candidate once a 2nd-source confirmation exists

## Open questions for this domain

- Do batch-invariant kernels see adoption in major inference servers (vLLM, SGLang) by EOY 2026?
- Does on-policy distillation generalize beyond reasoning / instruction-following — e.g., to coding agents?
- Manifold optimization at LLM scale (matrix-sign retraction efficiency) — TML's next move?
