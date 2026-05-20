---
type: concept
title: "Manifold Optimization"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - concept
  - optimization
  - theory
status: seed
complexity: advanced
domain: llm
aliases:
  - "Riemannian optimization"
  - "constrained-weight optimization"
related:
  - "[[Stiefel Manifold]]"
  - "[[Manifold Muon]]"
sources:
  - "[[2025-09-26 - Bernstein - Modular Manifolds]]"
---

# Manifold Optimization

Optimization where parameters are constrained to live on a mathematical submanifold (e.g., hypersphere, [[Stiefel Manifold]]) rather than unconstrained $\mathbb{R}^n$. The optimizer:

1. Computes a tangent-space direction at the current point
2. Steps along the tangent
3. **Retracts** back to the manifold (the manifold-aware analogue of projecting)

## Why for neural nets

Per [[2025-09-26 - Bernstein - Modular Manifolds]]:

- Constraining singular values bounds activation magnitudes → numerical stability at scale
- Non-Euclidean norms on the tangent space can give strictly better update directions ("for a fixed length step, we may be able to move further toward the gradient")
- Per-layer geometry gives a principled story for **per-layer LR budgets** (vs heuristic warmup tuning)

## Modular framework

Each module is a triple: (forward function, manifold constraint, norm). Modules compose:
- Forward: sequential composition
- Manifold: Cartesian product
- Norm: weighted max

Lets architecture and optimization be **co-designed** at scale.

## Concrete optimizer: [[Manifold Muon]]

Variant of the Muon optimizer that retracts onto the Stiefel manifold each step via the matrix sign function. Beat AdamW on a small CIFAR-10 experiment, with extra compute per step. Solution to the dual problem credited to Jianlin Su and Franz Louis Cesista.

## Open

- Which manifolds for which components (attention heads, embeddings)?
- GPU-efficient matrix-sign retraction
- Convergence theory; implicit regularization properties
