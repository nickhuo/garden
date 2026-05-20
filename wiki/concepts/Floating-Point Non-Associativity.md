---
type: concept
title: "Floating-Point Non-Associativity"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - concept
  - numerics
status: seed
complexity: basic
domain: llm
related:
  - "[[Batch Invariance]]"
sources:
  - "[[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]]"
---

# Floating-Point Non-Associativity

$(a + b) + c \neq a + (b + c)$ in finite-precision floating-point. Adding numbers of different exponents loses information in the rounding step. Example: 1230 + 23.4 with three-digit precision rounds to 1250 — the 3.4 disappears.

Summing $\{1\text{e}{-10}, 1\text{e}{-5}, 1\text{e}{-2}, 1\}$ and their negatives in random orders → 102 unique results across 10,000 trials.

## What it does NOT cause (alone)

The "concurrency + floating point" hypothesis for LLM inference nondeterminism is **wrong**. Per [[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]], identical GPU matmul runs are bitwise reproducible despite both factors being present.

## What it DOES cause

When combined with **variable reduction orders** — which happen when kernels switch strategy based on batch size (Split-K, tile shape, tensor-core instruction selection) — you get [[Batch Invariance]] failure, which is the actual cause of nondeterminism in production LLM serving.

## Takeaway

Non-associativity is the *prerequisite*, not the *culprit*. The culprit is variable reduction order, which is fixable by enforcing batch-invariant kernel strategies.
