---
type: concept
title: GRPO
created: 2026-05-30
updated: 2026-05-30
tags: [llm, reinforcement-learning, prompt-optimization, training]
status: seed
complexity: advanced
domain: llm
aliases: ["Group Relative Policy Optimization"]
related: ["[[GEPA]]", "[[DeepSeek-R1-Zero]]", "[[RL with Verifiable Rewards]]", "[[Language Feedback as Learning Signal]]", "[[Verifiability]]", "[[LoRA]]", "[[On-Policy Distillation]]", "[[Reward Modeling]]", "[[Compound AI System]]"]
sources: ["[[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL]]", "[[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]"]
---

# GRPO

**Group Relative Policy Optimization** (Shao et al. 2024, *DeepSeekMath*) — a reinforcement-learning method, central to **[[RL with Verifiable Rewards]]**, that adapts LLM weights by treating end-of-rollout success metrics as **scalar rewards** used to estimate policy gradients. The dominant weight-space approach for fitting LLMs to downstream tasks. The primary GRPO paper (Shao et al. 2024, arXiv 2402.03300) is **not yet ingested**, but [[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL]] specifies the algorithm in full and is its canonical large-scale application.

## How it works (R1 formulation)

For each question `q`, sample a **group** of `G` outputs `{o₁…o_G}` from the old policy. The key move: **no value/critic network** — the advantage of each output is just its reward **normalized within the group**:

```
A_i = (r_i − mean({r₁…r_G})) / std({r₁…r_G})
```

The policy is then updated with a PPO-style clipped objective on the importance ratio `π_θ/π_old · A_i`, minus a `β·KL(π_θ‖π_ref)` penalty to a periodically-refreshed reference. This is what "group relative" means and why GRPO is cheaper than PPO — it drops the separately-trained value model that PPO needs.

> [!note] R1's "large clip" refinement
> DeepSeek-R1 found the **clip ratio ε is load-bearing**: too low truncates gradients for many tokens (degrades performance); too high destabilizes training. A deliberately *large* PPO-clip strategy (credited to Zhibin Gou) was a key GRPO enhancement for the R1 runs. R1-Zero hyperparameters: lr 3e-6, KL coef 0.001, temp 1.0, 16 samples/question, batch 512, reference refreshed every 400 steps.

## The sample-efficiency bottleneck

GRPO is effective but typically needs **tens to hundreds of thousands of rollouts** to fit a new task. This is a serious bottleneck when downstream applications invoke expensive tool calls, have limited inference budget, or cannot fine-tune the best/largest models. The deeper limitation, per the GEPA argument: collapsing a whole rollout into one scalar **discards** the language signal (reasoning, tool outputs, compiler errors) that an LLM could otherwise learn from — see [[Language Feedback as Learning Signal]].

## GEPA's comparison

In the [[GEPA]] experiments, GRPO is run with LoRA ([[LoRA]]) at a **24,000-rollout** budget. GEPA matched or beat it on 5/6 tasks using up to **35× fewer rollouts**, and matched GRPO's best validation with up to **78×** fewer. This is the paper's headline: *reflective prompt evolution can outperform weight-space RL* in compound AI systems under tight budgets.

> [!note] Operates in different parameter space
> GRPO tunes module **weights** `Θ`; GEPA tunes module **prompts** `Π`. Both are optimizers over a [[Compound AI System]]'s `⟨Π, Θ⟩`, which is what makes the head-to-head comparison meaningful.

## Connections

- **[[DeepSeek-R1-Zero]]** — GRPO's canonical large-scale use: pure-RL reasoning from a base model. R1 supplies the full algorithm spec the wiki was missing.
- **[[RL with Verifiable Rewards]]** / **[[Verifiability]]** — GRPO is the canonical RLVR optimizer; it needs cheap, trustworthy verifiable rewards.
- **[[On-Policy Distillation]]**, **[[LoRA]]** — other weight-space adaptation methods in the wiki.
- **[[Language Feedback as Learning Signal]]** / **[[Heuristic Learning]]** — the language/code-space alternatives that argue against collapsing feedback to a scalar.

## Sources

- [[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL]] — canonical large-scale GRPO application; specifies the objective + group-relative advantage + large-clip refinement.
- [[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]] (secondary reference — the GEPA-vs-GRPO rollout-efficiency comparison).
- *Primary GRPO paper: Shao et al. 2024 (DeepSeekMath, arXiv 2402.03300) — not yet ingested; top citation-chase target.*
