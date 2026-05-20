---
type: concept
title: "Empirical Neural Tangent Kernel"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - concept
  - theory
status: seed
complexity: advanced
domain: llm
aliases:
  - "eNTK"
related:
  - "[[LoRA]]"
sources:
  - "[[2025-09-29 - Schulman - LoRA Without Regret]]"
---

# Empirical Neural Tangent Kernel (eNTK)

The kernel induced by gradient dot products on a finite-width neural network: $K(x, x') = \nabla_\theta f(x)^T \nabla_\theta f(x')$. Approximates training dynamics under gradient descent for sufficiently small LRs / short horizons.

## Use in [[LoRA Without Regret]]

The eNTK framework explains why [[LoRA]] needs **all layers**, not just attention. Since eNTK relies on gradient dot products, layers with the **most parameters dominate the kernel**. MLPs hold most params in transformer models. So:

$$\text{LoRA training} \approx \text{eNTK(LoRA)} \approx \text{eNTK(FullFT)} \approx \text{FullFT}$$

— but only when LoRA covers MLPs. Attention-only LoRA breaks this approximation: the eNTK is dominated by the (unchanged) MLP gradients, and the small attention LoRA updates barely move the kernel.

This is the empirical-theoretical bridge for the headline finding: rank-256 attention-only loses to rank-128 MLP-only at equal param counts.
