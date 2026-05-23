---
type: source
title: "CiteFix: Enhancing RAG Accuracy Through Post-Processing Citation Correction"
created: 2026-05-23
updated: 2026-05-23
tags:
  - llm
  - citation
  - rag
  - evaluation
status: developing
source_type: paper
author: "(arXiv 2504.15629, Amazon)"
date_published: 2025-04-22
url: "https://arxiv.org/abs/2504.15629"
confidence: high
related:
  - "[[Citation Verification Pipeline]]"
  - "[[Generation-Time vs Post-hoc Citation]]"
  - "[[Attributed Text Generation]]"
sources:
  - "https://arxiv.org/html/2504.15629v2"
---

# CiteFix

Post-processing citation correction for RAG (arXiv 2504.15629, 2025). The single highest-leverage finding for anyone building a citation pipeline.

## The key insight

> **~80% of "unverifiable" facts are NOT hallucinations — they are citation errors** (the fact is in the retrieved set, the model just cited the wrong source).

This reframes the problem: most citation failure is cheap-to-fix *attribution* error, not expensive *content* hallucination. So a lightweight post-processing pass recovers most of the loss.

## Six correction algorithms (re-map each claim to the right retrieved source)

1. **Keyword matching** — shared-token overlap between statement and document.
2. **Keyword + semantic context** — 80% keyword + 20% retrieval-relevance score.
3. **BERTScore** — LongFormer contextual embeddings (handles paraphrase).
4. **Fine-tuned BERTScore** — contrastive training on positive/negative reference pairs.
5. **LLM-based matching** — a secondary LLM picks the relevant source per claim.
6. **Attention-map attribution** — (experimental) infer source dependence from generation attention.

## Results

- **+15.46% relative accuracy** on overall citation metrics.
- Best algorithm is model-dependent (hybrid keyword-semantic for one model, fine-tuned BERTScore for another).
- Enables dropping to a **~12× cheaper** model while keeping citation quality — correction substitutes for raw model size.

> [!note] Post-verification ≠ re-generation. CiteFix fixes attribution *after* drafting, cheaply, without touching the answer text.
