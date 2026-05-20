---
type: concept
title: "BM25 and Hybrid Retrieval"
created: 2026-05-13
updated: 2026-05-13
tags:
  - rag
  - retrieval
  - llm
status: mature
complexity: intermediate
domain: llm
aliases:
  - "sparse retrieval"
  - "hybrid search"
  - "RRF"
  - "Reciprocal Rank Fusion"
related:
  - "[[Contextual Retrieval]]"
  - "[[Reranking]]"
  - "[[Augmented LLM]]"
sources:
  - "[[2024-09-19 - Anthropic - Contextual Retrieval]]"
---

# BM25 and Hybrid Retrieval

## One-Line Definition

Combining sparse keyword-based retrieval (BM25) with dense semantic embedding retrieval using Reciprocal Rank Fusion to capture both exact lexical matches and semantic meaning.

## BM25 (Background)

BM25 (Best Match 25) is a classical information retrieval algorithm. It scores documents by term frequency (TF) and inverse document frequency (IDF), penalized by document length. It captures:
- Exact keyword matches (crucial for product names, codes, proper nouns)
- Rare term importance (IDF weighting)

BM25 does not capture semantic meaning — "revenue" and "income" are entirely different tokens. Dense embeddings handle this. Neither alone is sufficient.

## Hybrid Retrieval

Hybrid retrieval runs both signals in parallel:
1. Dense embedding search → ranked list A
2. BM25 search → ranked list B
3. Reciprocal Rank Fusion (RRF) → merged ranked list

**Reciprocal Rank Fusion** combines lists by summing `1 / (k + rank_i)` for each document across all lists, where k is a constant (commonly 60). Documents appearing high in both lists score highest. No score normalization required — only ranks matter.

## Benchmarked Performance

From [[2024-09-19 - Anthropic - Contextual Retrieval]] (50 docs, 5000 questions, top-20 recall):

| Method | Recall |
|---|---|
| Embedding only | ~77% |
| BM25 only | ~71% |
| Hybrid (embed + BM25) | ~83% |

The hybrid combination outperforms either signal alone, confirming complementary coverage.

## Stacking with Contextual Retrieval

When [[Contextual Retrieval]] is applied first (context blurbs prepended to chunks), then embedded and BM25-indexed:
- Contextual + Hybrid: ~91% recall (vs ~83% hybrid without context)

The context blurbs also help BM25 because they add semantically rich terms that make keyword matching more robust.

## Implementation Notes

- BM25 is available in Elasticsearch, OpenSearch, and many search libraries (e.g., `rank_bm25` in Python)
- RRF is parameter-light; default k=60 works well in practice
- Embeddings from Voyage AI, OpenAI, or Anthropic's own models pair naturally with BM25

## Sources

- [[2024-09-19 - Anthropic - Contextual Retrieval]] — primary, empirical benchmarks
