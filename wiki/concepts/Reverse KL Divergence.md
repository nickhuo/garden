---
type: concept
title: "Reverse KL Divergence"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - concept
  - post-training
  - distillation
status: seed
complexity: intermediate
domain: llm
aliases:
  - "reverse KL"
  - "mode-seeking KL"
related:
  - "[[On-Policy Distillation]]"
sources:
  - "[[2025-10-27 - Lu - On-Policy Distillation]]"
---

# Reverse KL Divergence

$\text{KL}(\pi_\theta \| \pi_{teacher}) = \mathbb{E}_{x \sim \pi_\theta}[\log \pi_\theta(x) - \log \pi_{teacher}(x)]$

The expectation is taken under the **student** distribution (vs forward KL, which takes expectation under the teacher).

## Properties

- **Mode-seeking:** concentrates probability mass on the teacher's high-probability behaviors rather than trying to cover the teacher's full support.
- **"Unhackable"** (per [[2025-10-27 - Lu - On-Policy Distillation]]): low KL ↔ desirable teacher-like behavior. Hard to game with spurious reward signals the way explicit reward models can be gamed.
- **One teacher forward per sample:** student samples are the things being scored; teacher only needs to evaluate logprobs on already-sampled sequences.

## Use in on-policy distillation

Per-token reverse KL serves as a dense, per-step reward signal for policy gradient. Negative reverse KL = advantage. Naturally targets "forking tokens" — points in a reasoning chain where the student diverges from the teacher's preferred branch.

See [[On-Policy Distillation]] for the full algorithm.
