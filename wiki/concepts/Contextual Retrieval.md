---
type: concept
title: "Contextual Retrieval"
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
  - "contextual chunking"
  - "context-augmented embedding"
related:
  - "[[BM25 and Hybrid Retrieval]]"
  - "[[Reranking]]"
  - "[[Just-in-Time Context Retrieval]]"
  - "[[Augmented LLM]]"
  - "[[KV-Cache Discipline]]"
  - "[[Token Economics]]"
sources:
  - "[[2024-09-19 - Anthropic - Contextual Retrieval]]"
---

# Contextual Retrieval

## One-Line Definition

A RAG enhancement technique that prepends an AI-generated context blurb to each document chunk before embedding, so that retrieval operates on self-contained, interpretable units rather than decontextualized fragments.

## The Problem It Solves

Standard RAG splits documents into chunks and embeds them in isolation. The chunk "revenue declined 3% in Q3" has ambiguous embedding — which company? which year? — so it may not surface when a query semantically relates to it. This **context-stripping** failure is the primary retrieval accuracy bottleneck.

## Mechanism

For each chunk, call Claude with the full source document and the chunk text:

```
<document>{{FULL_DOCUMENT}}</document>
<chunk>{{CHUNK_CONTENT}}</chunk>
Please give a short succinct context to situate this chunk within the overall document for the purpose of improving search retrieval of the chunk. Answer only with the succinct context and nothing else.
```

Claude returns something like: "This chunk is from Acme Corp's Q3 2024 earnings report, specifically the revenue section for the North American segment."

That context blurb is prepended to the chunk text. The combined string is then embedded and indexed.

## Practical Economics: Prompt Caching

Generating context for N chunks from the same document requires Claude to process the full document N times — naively expensive. With **prompt caching** (cache the document, vary only the chunk), cost drops ~75% per context call. This brings contextual retrieval from cost-prohibitive to production-viable.

See [[KV-Cache Discipline]] and [[Token Economics]] for the broader caching pattern.

## Benchmarked Improvements (Anthropic, 2024)

Tested on 50 documents, 5000 questions; metric = top-20 chunk recall:

| Configuration | Recall | vs Baseline |
|---|---|---|
| Embedding only (baseline) | ~77% | — |
| + BM25 hybrid | ~83% | -35% failures |
| Contextual + Embed | ~85% | -49% failures |
| Contextual + Hybrid | ~91% | -57% failures |
| Contextual + Hybrid + Rerank | ~95%+ | **-67% failures** |

## Relationship to Hybrid Retrieval and Reranking

Contextual Retrieval stacks with:
- **[[BM25 and Hybrid Retrieval]]** — combine contextualized embeddings with BM25 keyword scores (via Reciprocal Rank Fusion)
- **[[Reranking]]** — cross-encoder model re-scores the hybrid top-k for final precision

The three compose additively; each layer adds ~5–10 pp recall.

## Relationship to Agent Context Engineering

[[Just-in-Time Context Retrieval]] applies the same intuition in the agent context window: pull in relevant information from long-horizon memory at query time rather than front-loading the context. Contextual Retrieval operates at the corpus layer; JITR operates at the session layer.

## Sources

- [[2024-09-19 - Anthropic - Contextual Retrieval]] — primary
