---
type: source
title: "Modular Manifolds"
aliases:
  - "Modular Manifolds"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - optimization
  - theory
status: developing
source_type: blog
author: "Jeremy Bernstein"
date_published: 2025-09-26
url: https://thinkingmachines.ai/blog/modular-manifolds/
confidence: medium
key_claims:
  - "Constraining weights to mathematical submanifolds (e.g., Stiefel) and co-designing the optimizer yields better update directions than vanilla gradient descent"
  - '"Manifold Muon" — Muon optimizer variant that retracts weights onto the Stiefel manifold each step; beats AdamW on CIFAR-10 at extra compute cost'
  - "Modular manifolds: treat each NN module as (forward, manifold, norm). Compose by Cartesian product of manifolds + weighted-max norms — enables principled per-layer LR budgets"
  - "Non-Euclidean norms on tangent spaces can let you move further toward the gradient per fixed step length"
related:
  - "[[Jeremy Bernstein]]"
  - "[[Thinking Machines Lab]]"
  - "[[Manifold Optimization]]"
  - "[[Stiefel Manifold]]"
  - "[[Manifold Muon]]"
sources:
  - "[[.raw/articles/2025-09-26 - Bernstein - Modular Manifolds.md]]"
---

# Modular Manifolds

Jeremy Bernstein, Thinking Machines Lab, September 26, 2025. [Blog post](https://thinkingmachines.ai/blog/modular-manifolds/).

## TL;DR

Most optimization treats weights as living in unconstrained Euclidean space. This essay argues for **constraining weights to submanifolds** (hypersphere, Stiefel) and designing the optimizer to *respect* the constraint via tangent-space steps + retraction. The unit of composition is the **module** — a triple (forward function, manifold constraint, norm). Manifolds compose by Cartesian product; norms compose by weighted max. The framework gives a clean account of why per-layer LR budgets matter.

## Core ideas

### Hypersphere optimization

For weights $w$ on the unit hypersphere:
- Tangent space at $w$ = vectors orthogonal to $w$
- Optimal update: subtract the radial component of the gradient, normalize, scale by LR, retract
- Non-Euclidean norms on tangent space can yield strictly better update directions ("for a fixed length step, we may be able to move further in the direction of the gradient")

### Manifold Muon

Treat $W$ as a vector-multiplier; constrain singular values to exactly 1 (the Stiefel manifold: $W^T W = I_n$). Tangent vectors satisfy $A^T W + W^T A = 0$. Combine spectral-norm constraints with Stiefel: solved via dual ascent over Lagrange multiplier $\Lambda$, with the matrix sign function as the retraction.

CIFAR-10: manifold Muon beats AdamW with extra per-step compute.

### Modular manifolds

Each module = (forward $f: W \times X \to Y$, submanifold $M \subset W$, norm $\|\cdot\|: W \to \mathbb{R}$). Compose:

- Forward: sequential composition
- Manifolds: Cartesian product
- Norms: weighted max

Lets you **budget LR across layers** without giving up the per-layer optimization logic. Ties to Lipschitz sensitivity of outputs w.r.t. weights.

## Why it might matter

- Constraining singular values bounds activation magnitudes → numerical stability at scale
- Per-layer LR via norm composition is principled, not just heuristic warmup tuning
- Connects to the [Modula project](https://modula.systems/) — module-graph view of neural nets

## Open

- Which manifolds for attention heads vs embeddings?
- Numerical precision at low fp formats with manifold constraints
- Convergence theory; implicit regularization properties
- Efficient GPU implementations of matrix-sign retraction

## Connections

- [[Manifold Muon]] is concrete; this essay is the conceptual frame
- Independent of but resonant with [[Defeating Nondeterminism in LLM Inference]] (both argue numerical structure of training/inference deserves first-class attention)
- The "co-design architecture and optimizer" thesis is the through-line across most TML output so far
