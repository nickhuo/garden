---
type: source
title: "Proximal Policy Optimization Algorithms (PPO)"
created: 2026-06-02
updated: 2026-06-02
tags: [llm, rl, policy-gradient, rlhf, alignment]
status: developing
source_type: paper
author: John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, Oleg Klimov (OpenAI)
date_published: 2017-07-20
url: https://arxiv.org/abs/1707.06347
confidence: high
seed_score: 14/14
aliases: ["2017 - Schulman et al - PPO", "Proximal Policy Optimization", "PPO paper"]
related: ["[[PPO]]", "[[GRPO]]", "[[Reward Modeling]]", "[[2022-03-04 - Ouyang et al - InstructGPT]]", "[[John Schulman]]"]
sources: ["[[.raw/articles/2017-07-20 - Schulman et al - Proximal Policy Optimization]]"]
cited_sources: []
key_claims:
  - "PPO replaces TRPO's second-order trust-region constraint with a first-order clipped surrogate objective — same stability benefit, far simpler to implement, better empirical sample complexity."
  - "The clipped objective min(r·Â, clip(r,1−ε,1+ε)·Â) removes the incentive to push the policy/old-policy probability ratio outside [1−ε,1+ε], bounding update size without a hard KL constraint."
  - "Because the objective is clipped, the same batch of rollouts can be reused for multiple epochs of minibatch SGD — the key sample-efficiency win over vanilla policy gradient (one update per sample)."
  - "PPO became the default RL optimizer for RLHF (the 'PPO' step in InstructGPT's SFT→RM→PPO recipe)."
---

# Proximal Policy Optimization Algorithms (PPO)

## Summary

PPO is the policy-gradient algorithm that became the workhorse of deep RL and, later, the RL step in [[Reward Modeling|RLHF]]. Its contribution is an **engineering simplification of [[TRPO]]**: instead of solving a constrained second-order optimization to keep each policy update inside a trust region, PPO bakes the constraint into a **clipped first-order surrogate objective** that any SGD optimizer can maximize.

The clipped objective is:

```
L^CLIP(θ) = E_t[ min( r_t(θ)·Â_t , clip(r_t(θ), 1−ε, 1+ε)·Â_t ) ]
r_t(θ) = π_θ(a_t|s_t) / π_θ_old(a_t|s_t)        (ε ≈ 0.2)
```

The `min`+`clip` removes any gain from moving the probability ratio beyond `[1−ε, 1+ε]`, so updates stay "proximal" to the old policy. This buys two things: (1) **stability** comparable to TRPO without its complexity, and (2) **multiple epochs of minibatch updates per rollout batch** (vanilla policy gradient allows only one), which is the empirical sample-efficiency win. The practical loss adds a value-function term and an entropy bonus, with advantages from GAE.

## Why it matters here

PPO is a **lineage anchor the wiki kept referencing without sourcing**. [[Reward Modeling]] and [[2022-03-04 - Ouyang et al - InstructGPT]] describe RLHF as "SFT → reward model → **PPO**"; the [[GRPO]] page describes its own update as a "**PPO-style clipped objective** … minus a β·KL penalty" and explains GRPO's cost advantage as "dropping the separately-trained value model that **PPO** needs." This page is the primary source for that load-bearing component.

The clip-ratio detail matters downstream: [[GRPO]]'s R1-era "large clip" refinement (DeepSeek-R1) is a direct tuning of PPO's ε. PPO → GRPO is the cleanest line from classic actor-critic RL to modern critic-free LLM RL.

## Connection to prior work

- **[[TRPO]]** (Schulman et al. 2015) — the direct predecessor PPO simplifies; PPO keeps its trust-region intuition, drops the conjugate-gradient/second-order machinery. Cited but not yet ingested (see Lineage).
- **[[2022-03-04 - Ouyang et al - InstructGPT]]** — the canonical use of PPO at LLM scale: optimize the policy against a learned reward model.
- **[[GRPO]]** — the critic-free descendant; same clipped-ratio core, group-relative advantage instead of a value net.
- Author **[[John Schulman]]** later worked on RLHF at OpenAI and LoRA-for-RL at Thinking Machines Lab.

## Lineage / 引用脉络

One-hop citation chase: PPO's load-bearing upstream is **TRPO** (Schulman, Levine, Moritz, Jordan, Abbeel 2015, *Trust Region Policy Optimization*, arXiv 1502.05477) — the trust-region method PPO approximates. It passes the seed gate on its own merits and is the standout chase target, but is **not built here** (scope was the two papers Nick named). Flagged as the top follow-up. Other references (GAE, A3C/A2C baselines) are method components rather than chaseable primary claims.

## Sources

- arXiv:1707.06347 (Schulman et al., OpenAI, 2017)
- `.raw/articles/2017-07-20 - Schulman et al - Proximal Policy Optimization.md`
