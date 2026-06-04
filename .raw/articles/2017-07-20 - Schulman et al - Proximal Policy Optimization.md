---
source_url: https://arxiv.org/abs/1707.06347
fetched: 2026-06-02
---

# Proximal Policy Optimization Algorithms

**Authors:** John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, Oleg Klimov (OpenAI)
**Submitted:** 2017-07-20 (rev. 2017-08-28)
**arXiv:** 1707.06347

## Abstract (verbatim)

We propose a new family of policy gradient methods for reinforcement learning, which alternate between sampling data through interaction with the environment, and optimizing a "surrogate" objective function using stochastic gradient ascent. Whereas standard policy gradient methods perform one gradient update per data sample, we propose a novel objective function that enables multiple epochs of minibatch updates. The new methods, which we call proximal policy optimization (PPO), have some of the benefits of trust region policy optimization (TRPO), but they are much simpler to implement, more general, and have better sample complexity (empirically). Our experiments test PPO on a collection of benchmark tasks, including simulated robotic locomotion and Atari game playing, and we show that PPO outperforms other online policy gradient methods, and overall strikes a favorable balance between sample complexity, simplicity, and wall-time.

## Key technical contributions

- **Clipped surrogate objective.** PPO's main variant maximizes `L^CLIP(θ) = E_t[ min( r_t(θ) Â_t , clip(r_t(θ), 1−ε, 1+ε) Â_t ) ]`, where `r_t(θ) = π_θ(a_t|s_t) / π_θ_old(a_t|s_t)` is the probability ratio and `Â_t` is the estimated advantage. The clip removes the incentive to move the ratio outside `[1−ε, 1+ε]` (typically ε≈0.2), bounding how far the policy moves per update without a hard KL constraint.
- **Adaptive KL-penalty variant.** An alternative penalizes `β·KL[π_old, π_θ]` with β adjusted online to hit a target KL; the clipped objective performs better empirically.
- **Multiple epochs per data batch.** Unlike vanilla policy gradient (one update per sample), the clipped objective is safe to optimize for several epochs of minibatch SGD on the same collected rollouts → better sample efficiency.
- **Relation to TRPO.** Keeps TRPO's trust-region benefit (stable, monotonic-ish improvement) but replaces the second-order constrained optimization with a first-order clipped objective — much simpler to implement, compatible with shared actor/critic params, dropout, etc.
- **Practical recipe.** Combine `L^CLIP` with a value-function error term and an entropy bonus; estimate advantages with generalized advantage estimation (GAE) over fixed-length trajectory segments.

## Experiments

- Simulated robotic locomotion (MuJoCo) and Atari. PPO outperforms other online policy-gradient methods (A2C, vanilla PG, and is competitive with/better than TRPO) with a favorable balance of sample complexity, simplicity, and wall-clock time.
