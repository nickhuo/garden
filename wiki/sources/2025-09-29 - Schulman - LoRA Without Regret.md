---
type: source
title: "LoRA Without Regret"
aliases:
  - "LoRA Without Regret"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - post-training
  - fine-tuning
  - parameter-efficient
status: developing
source_type: blog
author: "John Schulman"
date_published: 2025-09-29
url: https://thinkingmachines.ai/blog/lora/
confidence: high
key_claims:
  - LoRA matches full fine-tuning when (a) applied to all weights (especially MLP/MoE), (b) capacity isn't exceeded by dataset, and (c) batch size is moderate
  - Attention-only LoRA significantly underperforms MLP-only LoRA at equivalent parameter counts — eNTK theory predicts this since MLPs hold most params
  - Optimal LR for LoRA is ~10x the FullFT LR (held across 14 Llama/Qwen models, both SL and RL)
  - For policy-gradient RL, LoRA matches FullFT even at rank 1 — info-theoretic: RL absorbs ~1 bit/episode, far less than even tiny LoRA capacity
  - LoRA uses ~2/3 the FLOPs of FullFT per pass
related:
  - "[[John Schulman]]"
  - "[[Thinking Machines Lab]]"
  - "[[LoRA]]"
  - "[[Empirical Neural Tangent Kernel]]"
sources:
  - "[[.raw/articles/2025-09-29 - Schulman - LoRA Without Regret.md]]"
---

# LoRA Without Regret

John Schulman et al., Thinking Machines Lab, September 29, 2025. [Blog post](https://thinkingmachines.ai/blog/lora/).

## TL;DR

LoRA was widely seen as "FullFT for the GPU-poor with mild quality loss." This paper argues there is a "**low-regret regime**" where LoRA is genuinely indistinguishable from FullFT — provided three conditions hold:

1. **Apply LoRA to all layers**, especially MLP/MoE (not just attention)
2. **Don't exceed capacity** — dataset bits ≲ LoRA parameter capacity
3. **Use moderate batch sizes** (LoRA's gap to FullFT widens with batch size, independent of rank)

For policy-gradient RL the bar is even lower: **rank 1 suffices**.

## Key findings

### Rank and learning curves

- FullFT and high-rank LoRAs share linear-log learning curves.
- Lower ranks fall off the curve when dataset bits exceed LoRA capacity.
- Optimal LR is approximately rank-invariant (the $\alpha/r$ scaling ensures rank-1 update magnitude is preserved).

### The 10x LR rule

Across 14 Llama/Qwen models: optimal LoRA LR ≈ **10x** FullFT LR. Convergence to 9.8x via the fitted model:
$$\text{LR} = M_{LoRA} \cdot (2000/h)^{\text{model_pow} + \text{LoRA_pow}}$$

LoRA scales identically to FullFT in hidden-dim. Short runs (<100 steps) want ~15x because B starts at zero (implicit warmup); the ratio decays to 10x as B's spectral norm grows.

### Attention-only is broken

Attention-only rank-256 (0.25B params) underperformed MLP-only rank-128 (0.24B params). The eNTK framing: layers with most parameters dominate the tangent kernel, so excluding MLPs breaks the FullFT-LoRA equivalence.

### RL needs nothing

For policy gradient: rank 1 is enough. Information bound: $I(G; R | \text{history}) \lesssim \log B$ where B is the number of advantage bins → useful info per episode is O(1). MATH dataset training: ~320k bits total vs 3M params in rank-1 LoRA.

### FLOPs

FullFT (forward+backward) on $W \in \mathbb{R}^{N \times N}$: $3N^2$ multiply-adds.
LoRA: $2N^2 + 6NR \approx (2/3) \cdot 3N^2$ for $R \ll N$.

## Practical guidance

- Use LoRA on **all** weights — not just attention.
- Set LR to ~10x your FullFT LR (15x for short runs).
- Standard HuggingFace parametrization is fine — invariances mean the 2D effective hyperparameter space is well-covered by the default.
- For RL: even rank 1 works; pick rank for engineering convenience, not capacity.

## Open questions

- Sharper predictions of where LoRA fails (capacity threshold)
- Theoretical grounding for the 10x ratio
- LoRA variants (PiSSA, DoRA) under equivalent conditions
- LoRA on MoE + parallelism schemes

## Citation

```bibtex
@article{schulman2025lora,
  author = {John Schulman and Thinking Machines Lab},
  title = {LoRA Without Regret},
  journal = {Thinking Machines Lab: Connectionism},
  year = {2025},
  doi = {10.64434/tml.20250929},
}
```
