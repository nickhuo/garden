---
type: concept
title: "DPO"
created: 2026-06-02
updated: 2026-06-02
tags: [llm, rlhf, alignment, preference-optimization]
status: developing
related:
  - "[[PPO]]"
  - "[[Reward Modeling]]"
  - "[[RL with Verifiable Rewards]]"
sources:
  - "[[2023-05-29 - Rafailov et al - Direct Preference Optimization]]"
---

# DPO

**Direct Preference Optimization** (Rafailov et al. 2023, Stanford; NeurIPS 2023) — fine-tunes an LM directly on preference pairs with a single classification-style loss, **eliminating the reward model and the RL loop** of standard [[Reward Modeling|RLHF]]. Tagline: *"your language model is secretly a reward model."*

## The derivation in one move

Standard RLHF maximizes reward minus a β-weighted KL leash to a reference policy `π_ref`. That objective has a **closed-form optimum**:

```
π*(y|x) ∝ π_ref(y|x) · exp( r(x,y) / β )
```

Invert it: the implicit reward of any policy is `r(x,y) = β·log(π(y|x)/π_ref(y|x)) + β·log Z(x)`. Substitute that into the **Bradley–Terry** preference model and the intractable partition function `Z(x)` **cancels** for a preference pair, leaving a loss on the policy itself:

```
L_DPO = −E[ log σ( β·log(π_θ(y_w|x)/π_ref(y_w|x)) − β·log(π_θ(y_l|x)/π_ref(y_l|x)) ) ]
```

`y_w` preferred, `y_l` dispreferred. The gradient up-weights preferred completions and down-weights dispreferred ones, scaled by how wrong the *implicit* reward currently is. No separate reward model, no sampling from the LM during training, no [[PPO]].

## Why it matters

DPO made preference alignment **stable, cheap, and reproducible** — it removed the most fragile part of RLHF (the on-policy RL loop and a second trained model) and became the default for open-weight preference tuning. It is the "implicit reward" branch the [[Reward Modeling]] page describes: the policy's log-ratio to `π_ref` *is* the reward, which is what lets **online / iterative DPO** keep the preference signal live (regenerate completions from the current policy, score, update) and underlies later self-rewarding methods.

## PPO vs DPO

Same RLHF objective, two routes:
- **[[PPO]]** — optimize *online* against a learned reward model; flexible, multi-model, can be unstable.
- **DPO** — solve *offline* in closed form; one supervised loss, little tuning. Beats PPO-RLHF on sentiment control; matches or improves it on summarization and single-turn dialogue.

Distinct from the [[RL with Verifiable Rewards]] / [[GRPO]] line, which keeps on-policy RL but replaces the *learned* reward with an automatic verifier — DPO removes RL; RLVR keeps RL but removes the reward *model*.

## Limits

- **Off-policy / distribution shift** — vanilla DPO trains on a fixed offline preference set; as the policy moves it drifts off-distribution, the motivation for online/iterative DPO.
- **Implicit reward is only as good as the pairs** — inherits all the biases of the preference data; no separate RM to inspect or reuse.

## Connections

- **[[PPO]]** — the RL optimizer DPO replaces.
- **[[Reward Modeling]]** — DPO is its implicit-reward branch; online DPO / RLAIF keep it live.
- **[[2022-03-04 - Ouyang et al - InstructGPT]]** — the RLHF formulation DPO re-parameterizes.
- **Bradley–Terry model** — the pairwise-preference likelihood the derivation runs through.

## Sources

- [[2023-05-29 - Rafailov et al - Direct Preference Optimization]]
