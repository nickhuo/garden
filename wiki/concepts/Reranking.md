---
type: concept
title: "Reranking"
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
  - "cross-encoder reranking"
  - "re-ranking"
related:
  - "[[Contextual Retrieval]]"
  - "[[BM25 and Hybrid Retrieval]]"
  - "[[Augmented LLM]]"
  - "[[Token Economics]]"
sources:
  - "[[2024-09-19 - Anthropic - Contextual Retrieval]]"
---

# Reranking

## One-Line Definition

A post-retrieval precision step that uses a cross-encoder model to re-score retrieved candidates against the query, providing higher-fidelity relevance scoring than first-stage retrieval.

## How It Works

Standard retrieval (embedding cosine similarity or BM25) produces a top-k candidate set quickly. These methods are fast but approximate — the embedding model was not trained to score relevance between a specific query and a specific document; it produces a general-purpose vector.

A **reranker** (cross-encoder) takes each `(query, document)` pair and produces a joint relevance score. This is more expensive (O(k) model calls) but significantly more accurate because the model can attend to interactions between query tokens and document tokens.

Typical pipeline:
1. Retrieve top-100 candidates (cheap: embedding or BM25)
2. Reranker scores all 100 against the query
3. Return top-20 by reranker score to the LLM

## Providers

- **Cohere Rerank** (Cohere's API)
- **`voyage-rerank-1`** (Voyage AI, cited by Anthropic)
- Open-source: `ms-marco-MiniLM`, `bge-reranker-v2-m3` (HuggingFace)

## Performance (Anthropic Benchmark)

From [[2024-09-19 - Anthropic - Contextual Retrieval]]:

| Configuration | Failed Retrieval vs Baseline |
|---|---|
| Standard RAG | 0% (baseline) |
| Contextual + Hybrid | -57% |
| Contextual + Hybrid + Rerank | **-67%** |

The reranker adds ~10 pp failure reduction on top of the hybrid contextual pipeline, at higher cost.

## Cost-Accuracy Tradeoff

Reranking is the most expensive layer in the retrieval stack. It's appropriate when:
- Query precision is high-stakes (legal, medical, financial)
- The retrieval corpus is large and noise is likely
- Latency budget permits the extra model call

Skip reranking (use hybrid retrieval only) when cost or latency is constrained.

## Relationship to Other Concepts

- [[Contextual Retrieval]] — improves the quality of candidates fed to the reranker
- [[BM25 and Hybrid Retrieval]] — the prior stage before reranking
- [[Token Economics]] — reranking adds per-query model calls; budget accordingly

## Sources

- [[2024-09-19 - Anthropic - Contextual Retrieval]] — primary
