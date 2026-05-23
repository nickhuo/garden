---
type: source
title: "ZeroEntropy — Announcing zerank-1 and zerank-1-small"
created: 2026-05-23
updated: 2026-05-23
tags:
  - llm
  - retrieval
  - reranking
status: developing
source_type: blog
author: "ZeroEntropy"
date_published: 2025-07-10
url: "https://zeroentropy.dev/articles/announcing-zeroentropy-s-first-rerankers-zerank-1-and-zerank-1-small/"
confidence: medium
related:
  - "[[ZeroEntropy]]"
  - "[[zELO]]"
  - "[[Reranking]]"
sources:
  - "https://zeroentropy.dev/articles/announcing-zeroentropy-s-first-rerankers-zerank-1-and-zerank-1-small/"
  - "https://huggingface.co/zeroentropy/zerank-1"
---

# ZeroEntropy — Announcing zerank-1

The first ZeroEntropy reranker release (2025-07-10), establishing the [[zELO]] training approach: "the first scalable pipeline that turns synthetic pairwise judgments into an ELO-based ranking model."

## Models

- **zerank-1** — 4B params, LoRA cross-encoder on Qwen3-4B. Non-commercial license.
- **zerank-1-small** — 1.7B params, LoRA cross-encoder on Qwen3-1.7B. **Apache 2.0** (open-source), available via HuggingFace and Baseten.

## Benchmarks (vs Cohere rerank-3.5)

- **NDCG@10**: 0.7683 vs 0.7091 (~5.4% relative gain).
- **Latency**, 12KB payloads: 149.7ms vs 171.5ms (~12% faster); 150KB payloads: 314.4ms vs 459.2ms (~31% faster).
- Up to **+18% NDCG@10** in Finance/STEM vs Cohere rerank-3.5 and Salesforce LlamaRank; **+12% accuracy** vs Gemini 2.5 Flash as an LLM reranker.

## Pricing

$0.025 / 1M tokens — "half the cost" of competing rerankers.

> [!gap] Vendor-published benchmarks. The smaller model being Apache-2.0 while the flagship is non-commercial is the open-weight/monetization split ZeroEntropy uses across the product line.
