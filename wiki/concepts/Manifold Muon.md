---
type: concept
title: "Manifold Muon"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - concept
  - optimization
status: seed
complexity: advanced
domain: llm
related:
  - "[[Manifold Optimization]]"
  - "[[Stiefel Manifold]]"
sources:
  - "[[2025-09-26 - Bernstein - Modular Manifolds]]"
---

# Manifold Muon

Variant of the Muon optimizer that retracts weights onto the [[Stiefel Manifold]] each step. Combines:

- Spectral-norm step-size constraint on tangent-space updates
- Stiefel manifold constraint on the weights themselves
- Dual-ascent solution with the matrix sign function as both update direction and retraction

## Algorithm sketch

1. Run gradient ascent on dual variable $\Lambda$
2. Compute update using matrix sign function
3. Apply weight update
4. Retract weights back to the Stiefel manifold via matrix sign

Dual-problem solution credited to Jianlin Su and Franz Louis Cesista.

## Empirical (small)

CIFAR-10 experiment: manifold Muon > AdamW on accuracy, with **higher per-step compute cost**. Not yet demonstrated at LLM scale.

## Open issues

- Cost of matrix-sign retraction at LLM scale (potential GPU bottleneck)
- Numerical precision interactions (low-bit training with manifold constraints)
- Convergence theory

See [[2025-09-26 - Bernstein - Modular Manifolds]].
