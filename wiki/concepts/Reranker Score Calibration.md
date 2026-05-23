---
type: concept
title: "Reranker Score Calibration"
created: 2026-05-23
updated: 2026-05-23
tags:
  - llm
  - retrieval
  - reranking
status: seed
complexity: intermediate
domain: llm
aliases:
  - "calibrated relevance scores"
  - "reranker calibration"
related:
  - "[[Reranking]]"
  - "[[zELO]]"
  - "[[ZeroEntropy]]"
sources:
  - "[[2025-11-18 - ZeroEntropy - Introducing zerank-2]]"
  - "[[2025-09-16 - Pipitone et al - zELO]]"
---

# Reranker Score Calibration

## One-Line Definition

A reranker score is **calibrated** when its numeric value maps to an absolute, interpretable probability of relevance — e.g. a score of `0.8` means ~80% relevance, consistently across queries — rather than only encoding a relative ordering. (Source: [[2025-11-18 - ZeroEntropy - Introducing zerank-2]])

## Why it matters

Most rerankers output **uncalibrated** scores: useful for sorting candidates, but meaningless as absolute thresholds. You cannot say "keep everything above 0.7" because 0.7 means different things for different queries. Calibration unlocks:

- **Thresholding** — drop low-relevance candidates by an absolute cutoff instead of always taking top-k.
- **Cross-query comparability** — scores are comparable across different queries and corpora.
- **Agentic retrieval** — an agent can reason about *how confident* the retrieval is, not just the order. Pairs naturally with a separate **confidence score** (zerank-2 ships both).

## How zELO produces calibration

The [[zELO]] Elo formulation yields absolute relevance ratings by construction (Thurstone model), so calibrated scores fall out of training rather than requiring a separate post-hoc calibration step (e.g. Platt scaling / isotonic regression).

## Relation to other pages

A property of the [[Reranking]] step; a direct consequence of the [[zELO]] training method. Conceptually adjacent to confidence/uncertainty estimation in [[LLM-as-Judge]] scoring.
