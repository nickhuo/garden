---
type: concept
title: "Embedding Distillation from Rerankers"
created: 2026-05-23
updated: 2026-05-23
tags:
  - llm
  - retrieval
  - embeddings
  - reranking
status: seed
complexity: advanced
domain: llm
aliases:
  - "cross-encoder to bi-encoder distillation"
  - "reranker-distilled embeddings"
related:
  - "[[Reranking]]"
  - "[[BM25 and Hybrid Retrieval]]"
  - "[[zELO]]"
  - "[[ZeroEntropy]]"
sources:
  - "[[2025 - ZeroEntropy - Introducing zembed-1]]"
---

# Embedding Distillation from Rerankers

## One-Line Definition

Training a fast **bi-encoder embedding model** (the first-stage retriever) by distilling relevance signal from a slower, more accurate **cross-encoder reranker** that acts as the teacher. (Source: [[2025 - ZeroEntropy - Introducing zembed-1]])

## The architecture tradeoff being bridged

| | Bi-encoder (embeddings) | Cross-encoder (reranker) |
|---|---|---|
| Query/doc encoding | Independent → vectors precomputable | Jointly, per query-doc pair |
| Speed | Fast (ANN over precomputed vectors) | Slow (no precompute) |
| Accuracy | Lower | Higher |
| Role | First-stage retrieval | Post-retrieval [[Reranking]] |

The standard RAG stack runs **retrieve (bi-encoder) → rerank (cross-encoder)**. Distillation **inverts the teaching direction**: the high-accuracy reranker becomes the teacher that improves the first-stage retriever.

## ZeroEntropy's instance

`zembed-1` is a 4B open-weight multilingual embedding model **distilled from the `zerank-2` cross-encoder**. The reranker — itself trained via [[zELO]] — transfers its relevance judgments into the embedding space. Result claims: MSMARCO NDCG@10 0.946 (top of 16 models), beating voyage-4 on 18/22 datasets.

## Why it matters

The accuracy ceiling of a cross-encoder can be partially "baked into" the cheap first-stage retriever, narrowing how much work the reranker must do — or improving recall before reranking even runs. It also means one training investment (the reranker) yields two products (reranker + retriever).

> [!gap] Distillation loss and dataset are not publicly detailed; benchmark numbers are vendor-published.
