---
type: concept
title: "Trainer-Sampler Determinism"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - concept
  - rl
  - infrastructure
status: developing
complexity: advanced
domain: llm
aliases:
  - "trainer-sampler alignment"
  - "bitwise sampler-trainer match"
related:
  - "[[Batch Invariance]]"
  - "[[On-Policy Distillation]]"
sources:
  - "[[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]]"
  - "[[2026-05-11 - Thinking Machines - Interaction Models]]"
---

# Trainer-Sampler Determinism

The property that the **sampler** (inference engine generating rollouts) and the **trainer** (computing gradients on those rollouts) produce bitwise-identical logits given identical inputs.

## Why it matters

When the sampler and trainer differ numerically, "on-policy" RL is silently **off-policy**: gradients are computed against logits the rollout-time policy didn't actually produce. Standard mitigations (importance weighting, off-policy correction) introduce variance and instability.

Per [[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]]:

- Without batch-invariant kernels, with off-policy correction: KL ~0.001, eventual reward crash
- Without batch-invariant kernels, no correction: reward crashes ~step 318 (Bigmath RLVR)
- **With batch-invariant kernels: KL exactly 0 throughout training**

[[Interaction Models]] reports <5% performance overhead from full bitwise alignment, with significant stability improvement.

## How to achieve it

- Use [[Batch Invariance|batch-invariant kernels]] in both sampler and trainer.
- Match precision, reduction order, and tensor-core instruction selection across systems.
- For attention: consistent KV-cache layout and fixed split sizes (not dynamic FlashDecoding).

## Downstream

- **True on-policy RL** at scale
- Stable [[On-Policy Distillation]] (reverse-KL signal is clean)
- Improved training stability for streaming/multimodal models per [[Interaction Models]]
