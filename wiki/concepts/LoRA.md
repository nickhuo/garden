---
type: concept
title: "LoRA"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - concept
  - post-training
  - parameter-efficient
status: developing
complexity: intermediate
domain: llm
aliases:
  - "Low-Rank Adaptation"
related:
  - "[[On-Policy Distillation]]"
  - "[[Empirical Neural Tangent Kernel]]"
sources:
  - "[[2025-09-29 - Schulman - LoRA Without Regret]]"
---

# LoRA (Low-Rank Adaptation)

Parameter-efficient fine-tuning that replaces the weight update $\Delta W$ with a low-rank factorization: $W' = W + \frac{\alpha}{r} B A$, where $B \in \mathbb{R}^{N \times r}$, $A \in \mathbb{R}^{r \times N}$, $r \ll N$.

## The "low-regret regime"

Per [[2025-09-29 - Schulman - LoRA Without Regret]], LoRA is **indistinguishable from full fine-tuning** when:

1. **Applied to all layers** — especially MLP/MoE, not just attention
2. **Capacity not exceeded** — dataset bits ≲ LoRA param capacity
3. **Moderate batch sizes** — LoRA's gap to FullFT widens with batch size

Attention-only LoRA at rank-256 underperforms MLP-only at rank-128 with similar param counts. Excluding MLPs breaks the eNTK equivalence to FullFT.

## Hyperparameter rules

- **Optimal LR ≈ 10× FullFT LR** (held across 14 Llama/Qwen models, both SL and RL). 15× for short runs (<100 steps) because B starts at zero (implicit warmup).
- **LR is approximately rank-invariant** thanks to the $\alpha/r$ scaling.
- Standard HuggingFace parametrization is fine — the 4-parameter (α, LR_A, LR_B, init_A) hyperparameter space collapses to 2D under invariances.

## RL: rank 1 suffices

For policy gradient RL, **rank 1 matches FullFT**. Information-theoretic bound: $I(G; R | \text{history}) \lesssim \log(B)$ — useful info per episode is O(1) regardless of model size. MATH dataset = ~320k bits total, far below even rank-1 LoRA's 3M params.

## Compute

LoRA forward+backward: $2N^2 + 6NR \approx (2/3) \cdot 3N^2$ multiply-adds for $R \ll N$ — ~2/3 the FLOPs of FullFT.

## Practical takeaways

- Default to LoRA on all weights, not the attention-only conventional wisdom
- Set LR to ~10× your FullFT LR
- For RL fine-tuning: don't agonize over rank, pick for engineering convenience
