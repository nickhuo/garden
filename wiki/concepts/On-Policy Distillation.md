---
type: concept
title: "On-Policy Distillation"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - concept
  - post-training
  - distillation
  - rl
status: developing
complexity: advanced
domain: llm
aliases:
  - "on-policy KD"
related:
  - "[[Reverse KL Divergence]]"
  - "[[LoRA]]"
  - "[[Trainer-Sampler Determinism]]"
sources:
  - "[[2025-10-27 - Lu - On-Policy Distillation]]"
---

# On-Policy Distillation

A post-training method that **samples trajectories from the student** (on-policy) and **grades each token via the teacher's reverse KL** (dense supervision). Bridges the on-policy / off-policy gap in standard distillation and the sparse-reward gap in standard RL.

## Algorithm sketch

1. Sample rollout $x_{1..T}$ from student $\pi_\theta$
2. Query teacher logprobs $\log \pi_{teacher}(x_{t+1} | x_{1..t})$ — single forward pass
3. Per-token advantage $A_t = -\text{KL}_t = -(\log \pi_\theta - \log \pi_{teacher})$
4. Standard policy-gradient update

## Why reverse KL

- **Mode-seeking** rather than mode-covering (forward KL covers teacher entirely; reverse KL concentrates on teacher's high-prob behaviors)
- **Unhackable** — low KL ↔ teacher-like behavior; no spurious reward channels
- Cheap — one teacher forward, no rollouts from teacher

## Empirical claims (from [[2025-10-27 - Lu - On-Policy Distillation]])

- **Reasoning:** Qwen3-8B-Base 60% → 70% AIME'24 in ~150 steps. **9-30x cost reduction** vs further SFT or full RL.
- **vs RL same-init:** ~7-10x faster in gradient steps, ~50-100x in compute.
- **Personalization:** restores IF-eval from 45% → 83% after domain mid-training, using the *original* base model as teacher.
- **Continual learning:** stable on single-prompt-256-rollout × 20 steps. Standard SFT on own samples drifts.

## Intuitions

- **Dense supervision:** every token gets feedback, not just rollout end.
- **Strategy reuse:** RL searches semantic-strategy space at cost; distillation copies a found strategy without re-paying the search.
- **Forking tokens:** per-token KL naturally targets the tokens where the student commits to a wrong reasoning path.

## Dependencies

- Implicitly relies on sampler/trainer numerical alignment ([[Defeating Nondeterminism in LLM Inference]]) for the KL signal to be clean.
- Compatible with [[LoRA]] post-training; LoRA's RL-friendliness (rank-1 works) means cheap student updates.
