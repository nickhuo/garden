---
type: concept
title: "zELO"
created: 2026-05-23
updated: 2026-05-23
tags:
  - llm
  - retrieval
  - reranking
  - training
status: developing
complexity: advanced
domain: llm
aliases:
  - "Elo-based reranker training"
  - "zELO training"
related:
  - "[[Reranking]]"
  - "[[Reranker Score Calibration]]"
  - "[[LLM-as-Judge]]"
  - "[[Reward Modeling]]"
  - "[[BM25 and Hybrid Retrieval]]"
  - "[[ZeroEntropy]]"
sources:
  - "[[2025-09-16 - Pipitone et al - zELO]]"
  - "[[2025-11-18 - ZeroEntropy - Introducing zerank-2]]"
---

# zELO

## One-Line Definition

A reranker-training method that models query–document relevance as **Elo ratings inferred from pairwise LLM-ensemble preferences**, then fine-tunes a pointwise cross-encoder on the converted absolute scores. (Source: [[2025-09-16 - Pipitone et al - zELO]])

## The core idea

Direct pointwise relevance labels are noisy and expensive. Pairwise judgments ("is doc A or doc B more relevant to query q?") are easier and more reliable to elicit. zELO treats ranking as a **Thurstone / Bradley-Terry model**: pairwise preference probabilities imply latent skill ratings, exactly as in chess Elo. Relevance score for a pair recovers via `w_ij = (1 + erf(Elo_i − Elo_j))/2`. This is the same trick that underlies [[LLM-as-Judge]] preference data and RLHF [[Reward Modeling]] — applied to *retrieval relevance* instead of response quality.

## Pipeline

1. **Candidate generation** — BM25 + embedding hybrid retrieval, top-100 ([[BM25 and Hybrid Retrieval]]).
2. **Pairwise annotation** — ensemble of 3 frontier LLMs scores document pairs (−1..1) with chain-of-thought. No humans in this loop.
3. **Sparse Elo estimation** — a k-regular random-cycle-union graph keeps comparisons sparse; converges at **~0.4% of all pairs** (≈400 of 100k). This is what makes the method scale.
4. **Pointwise fine-tune** — train the cross-encoder on the recovered absolute scores with MSE loss.
5. **RLHF refinement** — retrain on human-annotated failure cases.

## Why it matters

- **No human-annotation bottleneck.** Training data is fully synthetic and **regenerable as base LLMs improve** — the dataset compounds with frontier progress.
- **Calibrated absolute scores** fall out naturally from the Elo formulation → enables [[Reranker Score Calibration]].
- **The hard-negative "Laffer curve"**: harder mined negatives help only up to a point; overly-intelligent negatives can exceed human-positive quality and *degrade* the model. Contradicts the naive "harder negatives are always better" intuition.

## Connection to the vault

zELO is retrieval's analogue of the preference-to-reward conversion the vault already documents for agent evaluation ([[LLM-as-Judge]], [[Reward Modeling]]). It is the training engine behind ZeroEntropy's [[Reranking]] models and, via distillation, [[Embedding Distillation from Rerankers]].

> [!gap] Reported NDCG gains are self-published; no independent reproduction located.
