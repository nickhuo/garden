---
type: source
title: "Training language models to follow instructions with human feedback (InstructGPT)"
created: 2026-05-20
updated: 2026-05-20
tags: [llm, ai-agents, rlhf, alignment, reward-modeling, real-time-learning]
status: developing
source_type: paper
author: Long Ouyang et al. (OpenAI)
date_published: 2022-03-04
url: https://arxiv.org/abs/2203.02155
confidence: high
aliases: ["2022 - Ouyang et al - InstructGPT", "InstructGPT"]
related: ["[[Reward Modeling]]", "[[Learning from Implicit Feedback]]", "[[Online Learning from Interaction]]", "[[Online Evaluation]]"]
sources: []
key_claims:
  - "A 1.3B InstructGPT model is preferred to the 175B GPT-3 in human evaluation despite 100x fewer parameters — alignment via human feedback beats raw scale on instruction-following."
  - "Three-stage recipe: supervised fine-tuning on demonstrations, train a reward model on human preference comparisons, then optimize the policy against the reward model with PPO (RLHF)."
  - "The reward model is the load-bearing artifact: it converts collected human preferences into a differentiable training signal, the canonical bridge from feedback to weight updates."
  - "Alignment improves truthfulness and reduces toxicity with minimal capability regression (an 'alignment tax' that can be largely mitigated)."
---

# Training language models to follow instructions with human feedback (InstructGPT)

## Summary

The foundational RLHF paper. OpenAI fine-tunes GPT-3 to follow instructions by learning from human preference data rather than from more text. It establishes the three-stage RLHF recipe — **SFT → reward model → PPO** — that underlies most aligned production LLMs, and it is the canonical demonstration that a learned **reward model** can convert human judgment into a training signal.

## Why it matters here

InstructGPT is the reference point for the continual-learning loop: it is the offline, batched version of what real-time learning wants to do online. The reward model it introduces is exactly the artifact that [[Online Evaluation]] proposes to drive from *live* signals instead of a one-time annotation campaign (Source: [[2025-05-21 - Meta - Reinforcement Learning from User Feedback]]). It is also the human-prejudgment reward whose performance ceiling [[Welcome to the Era of Experience]] critiques.

## Connection to prior work

Nick's **Compass** dual-judge rubric is a lightweight, inference-time analogue of a reward model — it codifies "what is a good answer" as a scoring function. The lineage from InstructGPT's reward model to [[LLM-as-Judge]] to Compass's golden-dataset judging is direct.

## Sources

- arXiv:2203.02155 (Ouyang et al., OpenAI, 2022)
