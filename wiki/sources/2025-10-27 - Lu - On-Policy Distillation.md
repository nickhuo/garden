---
type: source
title: "On-Policy Distillation"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - post-training
  - distillation
  - rl
status: developing
source_type: blog
author: "Kevin Lu"
date_published: 2025-10-27
url: https://thinkingmachines.ai/blog/on-policy-distillation/
confidence: high
key_claims:
  - On-policy distillation = sample from the student, score with a teacher's per-token reverse KL. Combines on-policy relevance with dense supervision
  - On AIME'24 from a 400k SFT checkpoint, reaches 70% in ~150 steps — 9-30x cost reduction vs further SFT or RL
  - Direct head-to-head vs same-initialization RL: distillation learns the RL-trained policy ~7-10x faster in gradient steps, ~50-100x in compute
  - Recovers IF-eval performance after domain mid-training (treats the original model as its own reward model)
  - Very promising for continual learning — avoids SFT's distribution-drift collapse because the teacher policy is fixed
related:
  - "[[Kevin Lu]]"
  - "[[Thinking Machines Lab]]"
  - "[[On-Policy Distillation]]"
  - "[[Reverse KL Divergence]]"
  - "[[Trainer-Sampler Determinism]]"
sources:
  - "[[.raw/articles/2025-10-27 - Lu - On-Policy Distillation.md]]"
---

# On-Policy Distillation

Kevin Lu et al., Thinking Machines Lab, October 27, 2025. [Blog post](https://thinkingmachines.ai/blog/on-policy-distillation/).

## TL;DR

Standard distillation is off-policy (student trains on teacher trajectories) → mismatch with deployment. Pure RL is on-policy but sparse (one scalar reward per rollout). **On-policy distillation** samples from the student, asks the teacher to grade each token via reverse KL, and trains with policy gradient. Best of both: on-policy distribution + dense reward.

The headline: AIME'24 from 60% → 70% in ~150 steps, at **9-30x lower cost** than the equivalent SFT or RL alternatives.

## Method

Per-token reverse KL:
$KL(\pi_\theta \| \pi_{teacher}) = E_{x \sim \pi_\theta}[\log \pi_\theta(x_{t+1} | x_{1..t}) - \log \pi_{teacher}(x_{t+1} | x_{1..t})]$

- **Reverse KL** is mode-seeking and "unhackable": low KL means the student is genuinely behaving like the teacher.
- Requires only **one** forward pass from the teacher.
- Set per-token advantages to negative reverse KL; train with standard RL machinery (Tinker API).

## Key results

### Reasoning (Qwen3-8B-Base → AIME'24)

| Method | AIME'24 | Cost vs SFT-2M |
|---|---|---|
| SFT-400K | 60% | — |
| SFT-2M (extrapolated) | ~70% | 1× |
| RL (17,920 GPU-hr) | 68% | ≈1× |
| **On-policy distillation** | **70%** | **9-30×** lower |

### Personalization (internal assistant)

Mid-training Qwen3-8B on internal docs trashes IF-eval (85% → 45%). On-policy distillation with the *original* Qwen3-8B as teacher restores IF-eval to 83% while keeping most knowledge gain (41% internal QA vs 43% mid-train peak). The model is its own reward model.

### Continual learning

SFT on a model's own samples drifts — finite-batch sampling biases the distribution. With a fixed teacher, distillation is stable. Even 20 consecutive steps on a **single prompt** (256 rollouts/step) successfully distills teacher performance.

## Why it works (author's framing)

- **Dense vs sparse:** 7-10x fewer gradient steps than RL because every token gets feedback, not just rollout-end.
- **Semantic strategy search:** RL discovers strategies in semantic space. Once a strategy exists in the teacher, distillation is a shortcut to the strategy without re-paying the search cost.
- **Forking tokens:** Per-token KL naturally penalizes tokens that commit the student to a bad reasoning path — the SimpleBench ice-melting example shows the teacher zeroing in on the token where the student decided to treat physics as pure math.

## Connections

- The cost-efficiency claim depends on **trainer-sampler determinism** working — [[Defeating Nondeterminism in LLM Inference]] is implicitly load-bearing here. Off-policy correction is needed if numerics drift.
- Connects to broader [[Workflows vs Agents]] thinking: distillation can compress an expensive RL-discovered agent into a cheaper policy for production.
- **Reusability of single prompts** is a striking departure from RL's "fresh data per epoch" intuition.

## Citation

```bibtex
@article{lu2025onpolicydistillation,
  author = {Kevin Lu and Thinking Machines Lab},
  title = {On-Policy Distillation},
  journal = {Thinking Machines Lab: Connectionism},
  year = {2025},
  doi = {10.64434/tml.20251026},
}
```
