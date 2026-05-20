---
source_type: article
title: "Introducing Contextual Retrieval"
author: Anthropic
date_published: 2024-09-19
url: https://www.anthropic.com/engineering/contextual-retrieval
fetched: 2026-05-13
tags: [rag, retrieval, llm, embeddings, bm25]
---

# Introducing Contextual Retrieval

> Original article: https://www.anthropic.com/engineering/contextual-retrieval

## Overview

Contextual Retrieval is a technique developed by Anthropic to dramatically improve the accuracy of Retrieval-Augmented Generation (RAG) systems. The core problem: when documents are split into small chunks for retrieval, individual chunks often lose the context needed to interpret them correctly. Contextual Retrieval solves this by prepending chunk-specific explanatory context to each chunk before it is embedded and indexed.

## The Problem with Standard RAG

Traditional RAG pipelines:
1. Split source documents into chunks (~hundreds of tokens each)
2. Embed chunks using a model like `voyage-2` or OpenAI's `text-embedding-3-small`
3. At query time, retrieve the top-k most similar chunks
4. Pass retrieved chunks to the LLM for generation

The limitation: chunks stripped from their surrounding document context become ambiguous. A chunk saying "The revenue declined 3% in Q3" tells you nothing about which company, year, or reporting period is being discussed.

## Contextual Retrieval: The Solution

Contextual Retrieval prepends a short, AI-generated context blurb to each chunk before embedding. The context explains the chunk's relationship to the broader document. This makes each embedded unit self-contained and more accurately retrievable.

### Implementation Steps

1. For each chunk, pass it and the full document to Claude with a prompt:
   ```
   <document>{{FULL_DOCUMENT}}</document>
   <chunk>{{CHUNK_CONTENT}}</chunk>
   Please give a short succinct context to situate this chunk within the overall document for the purpose of improving search retrieval of the chunk. Answer only with the succinct context and nothing else.
   ```
2. Prepend Claude's output to the chunk text.
3. Embed the contextualized chunk (not the raw chunk).
4. Also index the contextualized chunk text in a BM25 index.

### Hybrid Retrieval: Combining Embeddings + BM25

Anthropic recommends combining:
- **Semantic search** (dense embedding retrieval): captures meaning, handles paraphrase
- **BM25** (sparse lexical retrieval): captures exact keyword matches

They found:
- Embeddings alone: top-20 retrieval recall ~77%
- BM25 alone: recall ~71%
- Combined (without contextual): recall ~83%
- **Combined with Contextual Retrieval: recall ~91%**

The combination is implemented by generating both a vector score and a BM25 score for each chunk, then using Reciprocal Rank Fusion (RRF) to merge the two ranked lists.

### Reranking

A third step: after retrieving top-k candidates from hybrid retrieval, pass them through a reranker model (e.g., Cohere Rerank or `voyage-rerank-1`). The reranker scores each candidate for direct relevance to the query, which is more expensive but higher fidelity than cosine similarity alone.

With reranking added:
- Standard RAG (top-20, no context): baseline
- Contextual Retrieval + Hybrid + Rerank: **67% reduction in failed retrievals** vs standard RAG

### Token Cost and Prompt Caching

Generating context for each chunk requires Claude to process the full document for each chunk — potentially expensive at scale. Anthropic's solution: **prompt caching**. The full document body is placed in the cached prefix; only the chunk itself changes between calls. This:
- Reduces per-context generation cost by ~75% (cache hit pricing)
- Brings contextual retrieval from cost-prohibitive to economically viable for production

At the time of publication (Sept 2024), Claude's prompt caching was newly released.

## Benchmark Results

Tested on a corpus of 50 documents, 5000 questions (Anthropic internal benchmark):

| Method | Retrieved in Top-20 | Failed retrievals vs baseline |
|---|---|---|
| Standard RAG (embedding only) | ~77% | baseline |
| BM25 only | ~71% | — |
| Hybrid (embed + BM25) | ~83% | -35% |
| Contextual + Embed | ~85% | -49% |
| Contextual + Hybrid | ~91% | -57% |
| Contextual + Hybrid + Rerank | ~95%+ | -67% |

Numbers are approximate; exact figures were published with caveats on corpus-dependence.

## Key Claims

1. Standard RAG suffers from context-stripping: chunks lose interpretive anchor when split from source documents.
2. Prepending Claude-generated context to each chunk before embedding dramatically improves retrieval accuracy.
3. Hybrid retrieval (embedding + BM25 with RRF) outperforms either signal alone.
4. Reranking provides an additional precision boost at higher computational cost.
5. Prompt caching makes per-chunk contextualization economically viable.
6. Combined, these techniques reduce retrieval failures by ~67% vs standard RAG.

## Components and Techniques Referenced

- **Contextual Retrieval** — the core technique (context prepending)
- **BM25** — sparse lexical retrieval algorithm (Robertson et al.)
- **Reciprocal Rank Fusion (RRF)** — score merging for hybrid retrieval
- **Reranking** — cross-encoder re-scoring of retrieved candidates
- **Prompt Caching** — Anthropic feature for caching repeated document prefixes
- **Voyage AI** — embedding model provider (cited as example)
- **Cohere Rerank** — reranker model provider (cited as example)

## Practical Guidance

Anthropic's recommendation ladder (cost vs accuracy tradeoff):
1. Start with embedding-only RAG (cheapest)
2. Add BM25 hybrid for free lexical recall
3. Add Contextual Retrieval if budget allows (prompt caching keeps cost manageable)
4. Add reranking for highest-precision applications

## Related Concepts

- [[Just-in-Time Context Retrieval]] — overlapping concept in agent context engineering
- [[Augmented LLM]] — the LLM-with-retrieval primitive
- [[KV-Cache Discipline]] — related Anthropic caching optimization
- [[Context Engineering]] — parent domain
