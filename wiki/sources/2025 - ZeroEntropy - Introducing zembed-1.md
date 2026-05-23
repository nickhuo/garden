---
type: source
title: "ZeroEntropy — Introducing zembed-1"
created: 2026-05-23
updated: 2026-05-23
tags:
  - llm
  - retrieval
  - embeddings
  - multilingual
status: developing
source_type: blog
author: "ZeroEntropy"
date_published: 2026-01-01
url: "https://zeroentropy.dev/articles/introducing-zembed-1-the-worlds-best-multilingual-text-embedding-model/"
confidence: medium
related:
  - "[[ZeroEntropy]]"
  - "[[Embedding Distillation from Rerankers]]"
  - "[[Reranking]]"
  - "[[BM25 and Hybrid Retrieval]]"
sources:
  - "https://zeroentropy.dev/articles/introducing-zembed-1-the-worlds-best-multilingual-text-embedding-model/"
  - "https://zeroentropy.dev/articles/zembed-1-overperforms-voyage-4/"
  - "https://huggingface.co/zeroentropy/zembed-1"
---

# ZeroEntropy — Introducing zembed-1

Announcement of `zembed-1`, ZeroEntropy's first text-embedding (bi-encoder) model. The notable architectural fact: it is a **4B open-weight multilingual embedding model distilled directly from the `zerank-2` cross-encoder reranker** — see [[Embedding Distillation from Rerankers]].

## Specs

- 4B params; **Matryoshka** output dims: 2560 (default), 1280, 640, 320, 160, 80, 40.
- $0.050 / 1M tokens. "fast" / "slow" latency modes.
- Available via API/SDK, HuggingFace, AWS SageMaker.

## Benchmarks

- **MSMARCO NDCG@10 = 0.946** — highest of all 16 models tested (closest proxy to real-world retrieval).
- Domain average **0.5561**: +10% over voyage-4-nano, +17.6% over OpenAI text-embedding-3-large.
- Beats voyage-4 on NDCG@10 in **18 of 22** evaluation datasets; +5–7% Recall@100 over Cohere embed v4 and OpenAI v3 large across verticals.
- Claimed up to **+7% Recall@100** over OpenAI Large, Qwen3-4B, BGE-M3, Gemini Embeddings, Cohere v4, Voyage-4-nano.

> [!gap] All comparisons are ZeroEntropy-published. Distillation specifics (loss function, distillation dataset) are not detailed publicly. Distilling a bi-encoder from a cross-encoder is the inverse of the usual retrieve→rerank stack — the reranker becomes the *teacher* for the first-stage retriever.
