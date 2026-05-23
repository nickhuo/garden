---
type: source
title: "Reinforcement Learning from User Feedback"
created: 2026-05-20
updated: 2026-05-20
tags: [ai-agents, llm, real-time-learning, implicit-feedback, rlhf]
status: developing
source_type: paper
author: Eric Han, Jun Chen, Karthik Abinav Sankararaman, et al. (Meta)
date_published: 2025-05-21
url: https://arxiv.org/abs/2505.14946
confidence: medium
related: ["[[Learning from Implicit Feedback]]", "[[Online Learning from Interaction]]"]
sources: []
key_claims:
  - "Implicit production signals (engagement, selection, follow-up behavior) can train preference models competitive with explicit-rating reward models."
  - "Reward models predict the likelihood a response earns a positive user signal, then feed multi-objective RL co-optimizing helpfulness, safety, satisfaction."
  - "Enables continuous improvement from naturally occurring production data rather than costly annotation."
---

# Reinforcement Learning from User Feedback (RLUF)

Meta AI, 2025. Targets the gap between offline RLHF (paid annotators, static preference sets) and what deployed agents actually see: a stream of **implicit user signals**.

## Method and signals (confidence: medium — single source)

- Train a reward model to predict the probability a response receives a **positive user signal** (engagement, content selection, copy/click, follow-up behavior).
- Feed that reward into multi-objective RL co-optimizing helpfulness, safety, and satisfaction.
- Learn continuously from production traffic — no per-example human labels.

## What it contributes to real-time learning

Concrete recipe for **learning from implicit feedback** at deployment scale. Where [[Welcome to the Era of Experience]] argues for grounded reward in principle, RLUF operationalizes a digital-product version: the user's subsequent behavior *is* the grounded reward signal. Directly relevant to consumer-facing agents.

> [!gap] Implicit signals are biased (engagement ≠ correctness; users disengage when satisfied too). Related work flags reward-hacking risk: optimizing for clicks can degrade truthfulness. Confidence kept medium pending independent replication.
