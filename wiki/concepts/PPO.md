---
type: concept
title: "PPO"
created: 2026-06-02
updated: 2026-06-02
tags: [llm, rl, policy-gradient, rlhf]
status: developing
related:
  - "[[GRPO]]"
  - "[[Reward Modeling]]"
  - "[[TRPO]]"
  - "[[RL with Verifiable Rewards]]"
sources:
  - "[[2017-07-20 - Schulman et al - Proximal Policy Optimization]]"
---

# PPO

**Proximal Policy Optimization** (Schulman et al. 2017, OpenAI) — the policy-gradient RL algorithm that became the default optimizer for deep RL and for the RL step in [[Reward Modeling|RLHF]]. Its one idea: replace [[TRPO]]'s second-order trust-region *constraint* with a first-order **clipped surrogate objective** that ordinary SGD can maximize.

## How it works

For probability ratio `r_t(θ) = π_θ(a_t|s_t)/π_θ_old(a_t|s_t)` and advantage estimate `Â_t`:

```
L^CLIP(θ) = E_t[ min( r_t·Â_t , clip(r_t, 1−ε, 1+ε)·Â_t ) ]     (ε ≈ 0.2)
```

The `clip` flattens the objective once the ratio leaves `[1−ε, 1+ε]`, so there's no gradient incentive to move the policy far from `π_old` in a single step — the update stays "proximal." Full loss = `L^CLIP` − value-function error + entropy bonus; advantages via GAE. An alternative variant uses an adaptive `β·KL` penalty instead of the clip, but the clipped form works better empirically.

Two consequences:
- **Stability without TRPO's machinery** — no conjugate gradient, no Fisher-vector products; compatible with shared actor/critic networks.
- **Multiple epochs per rollout** — because the objective is clipped, the same batch can be reused for several minibatch SGD passes (vanilla policy gradient allows one), the main sample-efficiency gain.

## Why it matters

PPO is the **load-bearing component the wiki kept naming without sourcing**: the "PPO" in InstructGPT's SFT → reward-model → PPO recipe ([[2022-03-04 - Ouyang et al - InstructGPT]]), and the "PPO-style clipped objective" that [[GRPO]] builds on. The PPO → GRPO line is the cleanest path from classic actor-critic RL to modern critic-free LLM RL: GRPO keeps PPO's clipped importance ratio but **drops the value network** PPO needs, estimating advantage by group-relative reward normalization instead.

The clip ratio ε is not a throwaway hyperparameter downstream — DeepSeek-R1's GRPO runs found a deliberately *large* PPO clip to be load-bearing for training stability ([[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL]]).

## Two ways to solve the RLHF objective

PPO and [[DPO]] are the two routes to the same RLHF goal (maximize reward − β·KL to a reference policy):
- **PPO** — optimize it *online* against a learned reward model. Flexible, but a complex, sometimes-unstable multi-model RL loop.
- **DPO** — solve it *offline* in closed form as a single classification loss; no reward model, no RL.

A third axis — [[RL with Verifiable Rewards]] / [[GRPO]] — returns to on-policy RL but swaps the learned reward model for a cheap automatic verifier.

## Connections

- **[[TRPO]]** — the predecessor PPO simplifies (not yet ingested; top citation-chase target).
- **[[GRPO]]** — critic-free descendant; same clipped ratio, group-relative advantage.
- **[[DPO]]** — the RL-free alternative to PPO for preference optimization.
- **[[Reward Modeling]]** / **[[2022-03-04 - Ouyang et al - InstructGPT]]** — PPO is the RL step in the RLHF recipe.
- **[[John Schulman]]** — lead author.

## Sources

- [[2017-07-20 - Schulman et al - Proximal Policy Optimization]]
