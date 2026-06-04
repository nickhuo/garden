---
type: source
title: "Direct Preference Optimization: Your Language Model is Secretly a Reward Model (DPO)"
created: 2026-06-02
updated: 2026-06-02
tags: [llm, rlhf, alignment, preference-optimization, reward-modeling]
status: developing
source_type: paper
author: Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, Chelsea Finn (Stanford)
date_published: 2023-05-29
url: https://arxiv.org/abs/2305.18290
confidence: high
seed_score: 14/14
aliases: ["2023 - Rafailov et al - DPO", "Direct Preference Optimization", "DPO paper"]
related: ["[[DPO]]", "[[PPO]]", "[[Reward Modeling]]", "[[2022-03-04 - Ouyang et al - InstructGPT]]", "[[Rafael Rafailov]]", "[[Chelsea Finn]]"]
sources: ["[[.raw/articles/2023-05-29 - Rafailov et al - Direct Preference Optimization]]"]
cited_sources: ["[[2022-03-04 - Ouyang et al - InstructGPT]]", "[[2017-07-20 - Schulman et al - Proximal Policy Optimization]]"]
key_claims:
  - "The RLHF objective (maximize reward − β·KL to a reference policy) has a closed-form optimum π* ∝ π_ref·exp(r/β); inverting it expresses the reward as r = β·log(π/π_ref) + β·log Z(x)."
  - "Substituting that reward into the Bradley–Terry preference model cancels the partition function Z(x) for a preference pair, turning RLHF into a single binary-classification-style loss on the policy — no reward model, no RL sampling."
  - "DPO is stable, lightweight, and needs little hyperparameter tuning; it matches or beats PPO-based RLHF on sentiment control, summarization, and single-turn dialogue."
  - "The trained policy implicitly defines a reward via its log-ratio to the reference — 'your LM is secretly a reward model' — the basis for later online/iterative DPO and self-rewarding methods."
---

# Direct Preference Optimization (DPO)

## Summary

DPO collapses the **two-stage [[Reward Modeling|RLHF]] pipeline** (train a reward model, then optimize the policy with [[PPO]]) into **one supervised loss**. The key algebraic move: the standard RLHF objective — maximize reward subject to a β-weighted KL leash to a reference policy `π_ref` — has a closed-form optimum,

```
π*(y|x) ∝ π_ref(y|x) · exp( r(x,y) / β )
```

Inverting it expresses the implicit reward of any policy as `r(x,y) = β·log(π(y|x)/π_ref(y|x)) + β·log Z(x)`. Plugging that into the **Bradley–Terry** preference model makes the intractable partition function `Z(x)` cancel for a *preference pair*, leaving a loss directly on the policy:

```
L_DPO = −E[ log σ( β·log(π_θ(y_w|x)/π_ref(y_w|x)) − β·log(π_θ(y_l|x)/π_ref(y_l|x)) ) ]
```

(`y_w` preferred, `y_l` dispreferred). No separate reward model, no sampling from the LM during training, no RL loop — RLHF becomes a stable classification-style fine-tune. The slogan, **"your language model is secretly a reward model,"** is literal: the policy's log-ratio to `π_ref` *is* an implicit reward.

## Why it matters here

DPO is the second **lineage backfill** in this ingest. [[Reward Modeling]] already states "DPO collapses the explicit RM: the policy itself *implicitly* defines a reward (the log-ratio to a reference policy)" and discusses **online/iterative DPO** — but the wiki never sourced the original. This page is that primary source.

It also defines the **PPO ↔ DPO fork** in alignment practice: same RLHF objective, two routes. PPO ([[2017-07-20 - Schulman et al - Proximal Policy Optimization]]) optimizes it online against a learned reward model (the [[2022-03-04 - Ouyang et al - InstructGPT]] recipe); DPO solves it offline in closed form. The later RL-for-*reasoning* line ([[GRPO]], [[RL with Verifiable Rewards]], [[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL]]) returns to on-policy RL but with *verifiable* rewards rather than a learned RM — a different axis from the DPO simplification.

## Connection to prior work

- **[[2022-03-04 - Ouyang et al - InstructGPT]]** — the RLHF formulation DPO re-parameterizes; the reward-modeling + PPO baseline DPO replaces.
- **[[PPO]]** — the RL optimizer DPO removes; DPO beats PPO-RLHF on sentiment control and matches it elsewhere, far more simply.
- **[[Reward Modeling]]** — DPO is the "implicit reward" branch; online/iterative DPO keeps the implicit reward live.
- **Bradley–Terry model** — the pairwise-preference likelihood DPO's derivation runs through.

## Lineage / 引用脉络

One-hop citation chase: DPO's two load-bearing upstreams are **already in the wiki** — [[2022-03-04 - Ouyang et al - InstructGPT]] (the RLHF objective and reward-model baseline) and [[2017-07-20 - Schulman et al - Proximal Policy Optimization]] (the PPO method it supplants, ingested in this same pass). Both are recorded in `cited_sources`. The remaining anchor, the **Bradley–Terry (1952)** preference model, is a classical statistical result, not a chaseable modern source. No new pages built.

## Sources

- arXiv:2305.18290 (Rafailov et al., Stanford, 2023; NeurIPS 2023)
- `.raw/articles/2023-05-29 - Rafailov et al - Direct Preference Optimization.md`
