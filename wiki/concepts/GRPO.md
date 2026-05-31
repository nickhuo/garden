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
related: ["[[GEPA]]", "[[Language Feedback as Learning Signal]]", "[[Verifiability]]", "[[LoRA]]", "[[On-Policy Distillation]]", "[[Reward Modeling]]", "[[Compound AI System]]"]
sources: ["[[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]"]
---

# GRPO

**Group Relative Policy Optimization** (Shao et al. 2024) — a reinforcement-learning method, central to **RL with Verifiable Rewards (RLVR)**, that adapts LLM weights by treating end-of-rollout success metrics as **scalar rewards** used to estimate policy gradients. The dominant weight-space approach for fitting LLMs to downstream tasks (referenced here via [[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]; not yet ingested from its primary source).

## The sample-efficiency bottleneck

GRPO is effective but typically needs **tens to hundreds of thousands of rollouts** to fit a new task. This is a serious bottleneck when downstream applications invoke expensive tool calls, have limited inference budget, or cannot fine-tune the best/largest models. The deeper limitation, per the GEPA argument: collapsing a whole rollout into one scalar **discards** the language signal (reasoning, tool outputs, compiler errors) that an LLM could otherwise learn from — see [[Language Feedback as Learning Signal]].

## GEPA's comparison

In the [[GEPA]] experiments, GRPO is run with LoRA ([[LoRA]]) at a **24,000-rollout** budget. GEPA matched or beat it on 5/6 tasks using up to **35× fewer rollouts**, and matched GRPO's best validation with up to **78×** fewer. This is the paper's headline: *reflective prompt evolution can outperform weight-space RL* in compound AI systems under tight budgets.

> [!note] Operates in different parameter space
> GRPO tunes module **weights** `Θ`; GEPA tunes module **prompts** `Π`. Both are optimizers over a [[Compound AI System]]'s `⟨Π, Θ⟩`, which is what makes the head-to-head comparison meaningful.

## Connections

- **[[Verifiability]]** — GRPO is the canonical RLVR algorithm; it needs cheap, trustworthy verifiable rewards.
- **[[On-Policy Distillation]]**, **[[LoRA]]** — other weight-space adaptation methods in the wiki.
- **[[Language Feedback as Learning Signal]]** / **[[Heuristic Learning]]** — the language/code-space alternatives that argue against collapsing feedback to a scalar.

## Sources

- [[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]] (secondary reference; primary is Shao et al. 2024, not yet ingested)
