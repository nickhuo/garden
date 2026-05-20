---
type: concept
title: "Batch Invariance"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - concept
  - inference
  - infrastructure
status: developing
complexity: advanced
domain: llm
aliases:
  - "batch-invariant kernels"
related:
  - "[[Floating-Point Non-Associativity]]"
  - "[[Trainer-Sampler Determinism]]"
sources:
  - "[[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]]"
---

# Batch Invariance

A property of a kernel: **for any input, the numerical output is identical regardless of the batch it's co-batched with**. Most production GPU kernels (matmul, attention, RMSNorm) are *not* batch-invariant — they switch tile shapes, tensor-core instructions, and split strategies based on total batch size.

## Why it matters

Per [[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]], batch invariance is the **actual root cause** of LLM inference nondeterminism at T=0 — not the folklore "concurrency + floating point" hypothesis. Production servers vary batch size with load; same prompt → different co-batches → different logits → divergent completions.

Demonstration:

```python
out1 = torch.mm(a[:1], b)         # single-row matmul
out2 = torch.mm(a, b)[:1]         # batched matmul then slice
(out1 - out2).abs().max()          # 1669.25 — not bitwise equal
```

## How to achieve it

Per the three problem kernels:

| Op | Strategy |
|---|---|
| RMSNorm | Data-parallel, one batch elem per core, sequential when batch < cores |
| Matmul | Fixed tile shapes, consistent tensor-core instructions across all batch sizes, no Split-K |
| Attention | Update KV+page tables before attention; **fixed split sizes** (e.g., 256+256+256+232, not 250×4) regardless of current load |

Cost: ~20% vs cuBLAS matmul, ~60-110% slower vLLM end-to-end — but this is engineering overhead, not fundamental.

## Downstream wins

- **Reproducible inference at T=0** — 1000 samples → 1000 identical completions on Qwen3-235B
- **True on-policy RL** — sampler and trainer produce bitwise-identical logits, KL stays exactly 0 ([[Trainer-Sampler Determinism]])
- **Trainer-sampler alignment** in [[Interaction Models]] — explicitly cited as <5% perf cost

## Available implementation

[`thinking-machines-lab/batch_invariant_ops`](https://github.com/thinking-machines-lab/batch_invariant_ops) — torch.Library plugin with vLLM FlexAttention integration.
