---
type: source
title: "ZeroEntropy — Introducing zerank-2"
created: 2026-05-23
updated: 2026-05-23
tags:
  - llm
  - retrieval
  - reranking
  - multilingual
status: developing
source_type: blog
author: "ZeroEntropy"
date_published: 2025-11-18
url: "https://zeroentropy.dev/articles/zerank-2-advanced-instruction-following-multilingual-reranker/"
confidence: medium
related:
  - "[[ZeroEntropy]]"
  - "[[zELO]]"
  - "[[Reranking]]"
  - "[[Reranker Score Calibration]]"
  - "[[Embedding Distillation from Rerankers]]"
sources:
  - "https://zeroentropy.dev/articles/zerank-2-advanced-instruction-following-multilingual-reranker/"
---

# ZeroEntropy — Introducing zerank-2

Product announcement (2025-11-18) for ZeroEntropy's second-generation cross-encoder reranker, shipped in three sizes: **zerank-2**, **zerank-2-small**, **zerank-2-nano**. Trained with the [[zELO]] pipeline (pairwise LLM preferences → absolute Elo scores).

## What's new over zerank-1

- **Multilingual**: 100+ languages, including challenging scripts (Chinese, Arabic) and code-switching queries (Spanglish, Hinglish), with "near-English performance across major languages."
- **Native instruction-following**: accepts appended instructions and business context to steer relevance.
- **Score calibration**: a `0.8` score means ~80% relevance, consistently — see [[Reranker Score Calibration]]. Adds a separate **confidence score**.
- **SQL-style / aggregation query robustness**.

## Claims & pricing

- "Outperforms every other reranker on both accuracy and latency" — beats Cohere rerank-3.5, Voyage rerank-2/3.5, OpenAI text-embedding-3-large.
- **$0.025 / 1M tokens**, claimed 50% cheaper than other commercial rerankers.
- Available via ZeroEntropy API, HuggingFace, AWS Marketplace, Azure Marketplace. Non-commercial license (commercial use by contact).

> [!gap] The announcement provides comparative *examples* but no NDCG@K or latency tables. Verifiable numbers come from the [[2025-09-16 - Pipitone et al - zELO]] paper, not this post. Parameter counts for the zerank-2 family are not disclosed.
