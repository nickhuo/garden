---
type: source
title: "Defeating Nondeterminism in LLM Inference"
aliases:
  - "Defeating Nondeterminism in LLM Inference"
  - "Defeating Nondeterminism"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - inference
  - infrastructure
  - rl
status: developing
source_type: blog
author: "Horace He"
date_published: 2025-09-10
url: https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/
confidence: high
key_claims:
  - The "concurrency + floating point" hypothesis for LLM nondeterminism is wrong — GPU matmul is bitwise reproducible. Real cause is **lack of batch invariance**: kernels produce different numerics depending on batch size, and inference servers see variable load
  - Three kernel rewrites — RMSNorm, matmul, attention — to enforce reduction-order invariance regardless of batch size. ~20% slower than cuBLAS matmul; ~60-110% slower vLLM end-to-end (engineering, not fundamental)
  - With batch-invariant kernels on Qwen3-235B at T=0: all 1000 completions identical, vs 80 unique completions without
  - Implication: nondeterministic inference quietly converts "on-policy" RL to off-policy RL. With determinism, KL between sampler and trainer stays exactly 0
related:
  - "[[Horace He]]"
  - "[[Thinking Machines Lab]]"
  - "[[Batch Invariance]]"
  - "[[Floating-Point Non-Associativity]]"
  - "[[Trainer-Sampler Determinism]]"
sources:
  - "[[.raw/articles/2025-09-10 - He - Defeating Nondeterminism in LLM Inference.md]]"
---

# Defeating Nondeterminism in LLM Inference

Horace He et al., Thinking Machines Lab, September 10, 2025. [Blog post](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/). Code: [thinking-machines-lab/batch_invariant_ops](https://github.com/thinking-machines-lab/batch_invariant_ops).

## TL;DR

LLM inference servers are nondeterministic at T=0. The folk explanation — "concurrent threads + non-associative floating point" — is wrong: simple GPU matmul is bitwise reproducible. **The real cause is batch invariance failure**: the same input produces different numerics depending on the batch size it gets co-batched with, and server load determines batch size. Fix the kernels to be batch-invariant and inference becomes deterministic — at ~20% matmul perf cost (engineering can recover most of it).

The downstream win: **true on-policy RL** becomes possible because sampler and trainer can produce bitwise-identical logits.

## The core diagnosis

```python
B, D = 2048, 4096
out1 = torch.mm(a[:1], b)         # 1×D output
out2 = torch.mm(a, b)[:1]         # same row, batch-of-2048 then slice
(out1 - out2).abs().max()          # 1669.25 — not zero
```

Kernel selection, reduction order, and split-K strategies all change with batch size. Mathematically these ops are independent across batch elements; numerically they aren't. Production servers vary batch size with load → the same prompt gets different logits at different times → divergent completions at T=0.

## Three fixes

| Op | Strategy | Cost |
|---|---|---|
| RMSNorm | Data-parallel, one batch elem per core, sequential at small batches | Some perf loss when batch < cores |
| Matmul | Fixed tile shapes, consistent tensor-core instruction selection across all batch sizes, no Split-K | ~20% vs cuBLAS |
| Attention | Update KV cache + page tables before attention; **fixed split-size** instead of dynamic FlashDecoding splits | Engineering-bound, not fundamental |

The attention insight: when processing the 1000th query token, the reduction order must be identical whether KV cache has 0 tokens (prefill) or 999 (decode). Achieved by fixed split sizes: 1000 = 256 + 256 + 256 + 232, not 250 + 250 + 250 + 250.

## Experimental evidence

Qwen3-235B-A22B-Instruct on "Tell me about Richard Feynman", 1000 samples, T=0, 1000 tokens:
- **Standard inference**: 80 unique completions; divergence at token 103
- **Batch-invariant kernels**: 1000 identical completions

End-to-end perf (Qwen-3-8B, 1000 seqs, 90-110 tokens):

| Setup | Time (s) |
|---|---|
| vLLM default | 26 |
| Unoptimized deterministic vLLM | 55 |
| + improved attention | 42 |

The 42s number is FlexAttention-bound, not fundamental to batch invariance.

## The RL implication

If sampler and trainer have different numerics, "on-policy" RL is silently off-policy → importance weighting needed → unstable. Bigmath RLVR:
- Without batch-invariant, with off-policy correction: KL ~0.001 with spikes, eventually crashes
- Without batch-invariant, no correction: reward crashes ~step 318
- **With batch-invariant: KL exactly 0 throughout**

This is the load-bearing claim for [[On-Policy Distillation]] and [[Interaction Models]]' trainer-sampler alignment.

## Connections

- This paper is the **infrastructure layer** under [[On-Policy Distillation]] and the trainer-sampler alignment claim in [[Interaction Models]]. Both other TML posts implicitly depend on this being workable.
- Stance: "papering over nondeterminism" is a cultural antipattern. Same lab-wide thesis as [[Modular Manifolds]] (take numerics seriously).
- Practical caveat: vLLM users can run the integration today via `thinking-machines-lab/batch_invariant_ops`.

## Citation

```bibtex
@article{he2025nondeterminism,
  author = {Horace He and Thinking Machines Lab},
  title = {Defeating Nondeterminism in LLM Inference},
  journal = {Thinking Machines Lab: Connectionism},
  year = {2025},
  doi = {10.64434/tml.20250910}
}
```
