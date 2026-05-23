---
type: entity
title: "ZeroEntropy"
entity_type: organization
created: 2026-05-23
updated: 2026-05-23
tags:
  - ai-agents
  - llm
  - retrieval
  - company
status: developing
related:
  - "[[zELO]]"
  - "[[Reranking]]"
  - "[[Reranker Score Calibration]]"
  - "[[Embedding Distillation from Rerankers]]"
  - "[[BM25 and Hybrid Retrieval]]"
sources:
  - "[[2025-07-09 - TechCrunch - ZeroEntropy Seed Round]]"
  - "[[2025-09-16 - Pipitone et al - zELO]]"
  - "[[2025-07-10 - ZeroEntropy - Announcing zerank-1]]"
  - "[[2025-11-18 - ZeroEntropy - Introducing zerank-2]]"
  - "[[2025 - ZeroEntropy - Introducing zembed-1]]"
---

# ZeroEntropy

A YC-backed developer-tool startup building **agentic retrieval infrastructure** — rerankers and embedding models for RAG and AI-agent search. Positions itself as "the fastest and most accurate agentic retrieval engine," and as a developer tool rather than an end-user search product (contrast: Glean).

## People & funding

- **Ghita Houir Alami** — CEO. Morocco → École Polytechnique (France) → UC Berkeley (MS mathematics).
- **Nicholas Pipitone** — CTO; lead author of the [[zELO]] paper.
- **$4.2M seed** (2025-07-09), led by Initialized Capital; YC, Transpose Platform, 22 Ventures, a16z Scout, + angels from OpenAI / Hugging Face / Front. ~$4.4M total. (Source: [[2025-07-09 - TechCrunch - ZeroEntropy Seed Round]])

## Product line

**Rerankers (cross-encoders, `zerank` family):**
- `zerank-1` (4B, Qwen3-4B base, non-commercial) + `zerank-1-small` (1.7B, Qwen3-1.7B, Apache 2.0) — 2025-07-10.
- `zerank-2` / `zerank-2-small` / `zerank-2-nano` — 2025-11-18; multilingual (100+ languages), instruction-following, calibrated scores.
- All rerankers: **$0.025 / 1M tokens**.

**Embeddings (bi-encoder):**
- `zembed-1` — 4B, open-weight, multilingual, **distilled from `zerank-2`** ([[Embedding Distillation from Rerankers]]); Matryoshka dims 2560→40; $0.050 / 1M tokens.

## Why it matters here

ZeroEntropy is the concrete, technically-documented embodiment of the vault's retrieval theory pages — [[Reranking]], [[BM25 and Hybrid Retrieval]], [[Contextual Retrieval]]. Its distinctive contribution is **[[zELO]]**: training relevance models on LLM-ensemble pairwise preferences converted to absolute Elo scores, removing the human-annotation bottleneck. Models are trained cost-efficiently on TensorPool elastic GPUs, with training data regenerable as base LLMs improve.

## Distribution

ZeroEntropy API/SDK, HuggingFace, AWS Marketplace + SageMaker, Azure Marketplace, Baseten.
