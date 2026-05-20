---
type: concept
title: "Stiefel Manifold"
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
related:
  - "[[Manifold Optimization]]"
  - "[[Manifold Muon]]"
sources:
  - "[[2025-09-26 - Bernstein - Modular Manifolds]]"
---

# Stiefel Manifold

The set of $N \times n$ matrices with orthonormal columns: $W^T W = I_n$. Equivalently: matrices whose singular values are all exactly 1.

Tangent space at $W$: matrices $A$ satisfying $A^T W + W^T A = 0$ (anti-symmetric in the $W$-projected sense).

## Why constrain weights to it?

Per [[2025-09-26 - Bernstein - Modular Manifolds]]: a weight matrix $W$ acts as a vector-multiplier ($y = Wx$). Constraining singular values to 1 bounds the operator norm, which bounds activation growth layer-to-layer. Combined with spectral-norm constraints on tangent steps, you get optimization that respects the layer's natural geometry.

## Optimization via dual ascent

The constrained problem is solved by Lagrange duality, with the **matrix sign function** as the retraction. See [[Manifold Muon]] for the concrete algorithm.
