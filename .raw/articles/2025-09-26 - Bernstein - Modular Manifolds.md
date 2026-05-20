# Modular Manifolds

**Author:** Jeremy Bernstein (Thinking Machines Lab)
**Date Published:** September 26, 2025
**URL:** https://thinkingmachines.ai/blog/modular-manifolds/

---

## Overview

Explores constraining neural network weight matrices to mathematical submanifolds while co-designing optimization algorithms. Introduces "manifold Muon," a variant of the Muon optimizer for weights restricted to the Stiefel manifold, and proposes "modular manifolds" as a framework for scaling these techniques across network layers.

## The Shape of a Manifold Optimizer

Begins with hypersphere constraints on vector parameters. A manifold is "a curved surface that looks flat when you zoom in close enough"; the locally flat approximation is the tangent space.

For a unit hypersphere in ℝ^d, the tangent space at point *w* consists of all vectors orthogonal to *w*. Optimization: find the tangent vector of unit length maximizing the gradient descent direction, scale by learning rate, then retract back to the manifold.

Key insight: non-Euclidean norms can yield better update directions — "for a fixed length step, we may be able to move further in the direction of the gradient."

Optimization problem formalized as:
- Minimize linear change in loss
- Subject to step size constraints and tangent space constraints
- Solved via Lagrange multipliers

For the hypersphere with Euclidean norm, the optimal update: subtract the radial gradient component, normalize, scale by LR, then apply a retraction map.

## Manifold Muon

Weight matrices as "vector-multipliers" transforming inputs via *y = Wx*. Using SVD, the author argues for constraining singular values to exactly one — the Stiefel manifold.

Stiefel manifold: matrices *W* where *W^T W = I_n*. Tangent vectors *A* satisfy *A^T W + W^T A = 0*.

Combining spectral norm constraints with Stiefel constraints yields the manifold Muon optimization problem, solved via dual ascent:

1. Run gradient ascent on dual variable Λ
2. Compute update using matrix sign function
3. Apply weight update
4. Retract weights back to manifold via matrix sign function

Credits Jianlin Su and Franz Louis Cesista for the dual problem solution. Small CIFAR-10 experiment: manifold Muon achieved higher accuracy than AdamW, with increased per-step compute cost.

## Modular Manifolds

Treats neural network modules (layers to transformers) as mathematical objects with three attributes:

1. Forward function *f: W × X → Y*
2. Submanifold constraint *M ⊂ W*
3. Norm function *||·||: W → ℝ*

Composition rules:
- Forward functions compose sequentially
- Manifolds combine as Cartesian products
- Norms use weighted max of component norms

Allows budgeting LR across layers while preserving individual layer optimization logic. Connects to Lipschitz sensitivity of network outputs w.r.t. weights.

## Future Research Directions

- Manifold constraints for specific components (attention heads, embeddings)
- Numerical precision impacts of manifold constraints
- Advanced convex optimization for dual problems
- Convergence rates and theoretical properties
- Implicit regularization through manifold constraints
- Architecture-optimizer co-design beyond hard constraints
- Non-Riemannian geometry alternatives
- Efficient GPU implementations

## Key References

- Absil, Mahony & Sepulchre's manifold optimization textbook
- Thomas Flynn 2017: Finsler manifold characterization of neural networks
- The Modula project (modula.systems)
- Recent work on Lipschitz-constrained deep learning and spectral descent
