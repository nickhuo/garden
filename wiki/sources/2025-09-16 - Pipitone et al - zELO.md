---
type: source
title: "Pipitone et al — zELO: ELO-inspired Training for Rerankers and Embedding Models"
created: 2026-05-23
updated: 2026-05-23
tags:
  - llm
  - retrieval
  - reranking
  - training
status: developing
source_type: paper
author: "Nicholas Pipitone, Ghita Houir Alami, Advaith Avadhanam, Anton Kaminskyi, Ashley Khoo"
date_published: 2025-09-16
url: "https://arxiv.org/abs/2509.12541"
confidence: high
related:
  - "[[Reranking]]"
  - "[[BM25 and Hybrid Retrieval]]"
  - "[[LLM-as-Judge]]"
  - "[[Reward Modeling]]"
sources:
  - "https://arxiv.org/html/2509.12541v1"
---

# Pipitone et al — zELO

The foundational technical paper behind ZeroEntropy's `zerank` reranker family (arXiv 2509.12541, submitted 2025-09-16). Authors: Nicholas Pipitone (ZeroEntropy CTO), Ghita Houir Alami (CEO), Advaith Avadhanam, Anton Kaminskyi, Ashley Khoo.

## Core contribution

zELO trains rerankers by modeling query–document relevance as **Elo ratings derived from pairwise LLM-ensemble preferences**, rather than training directly on pointwise labels. Ranking is treated as statistically equivalent to a **Thurstone model**: pairwise preference probabilities convert to absolute relevance scores via `w_ij = (1 + erf(Elo_i − Elo_j))/2`. This is the same preference-to-score conversion that underlies [[LLM-as-Judge]] preference data and RLHF [[Reward Modeling]], applied to retrieval relevance — the productized embodiment is ZeroEntropy's `zerank` reranker family.

## Pipeline

1. **Initial retrieval** — BM25 + embedding hybrid search produces top-100 candidates ([[BM25 and Hybrid Retrieval]]).
2. **Pairwise annotation** — an ensemble of **3 frontier LLMs** rates document pairs on a −1 to 1 scale with chain-of-thought justifications. No human annotators.
3. **Elo conversion** — sparse pairwise preferences become absolute scores via Bradley-Terry / Thurstone estimation. A **k-regular random-cycle-union graph** keeps the comparison set sparse; convergence at ~0.4% of all possible pairs (≈400 of 100,000), sampling until standard error ≈ 0.1.
4. **Pointwise training** — fine-tune the cross-encoder on converted Elo scores with MSE loss: `L = (R_pred(q,d) − R_point(q,d))²`. Pairwise stage uses binary cross-entropy on ensemble scores.
5. **RLHF refinement** — retrain on human-annotated document failures.

## Training data & base models

- **112,000 queries, >100M documents** across finance, legal, medicine, code, STEM.
- `zerank-1` initialized from **Qwen3-4B**; `zerank-1-small` from **Qwen3-1.7B** (Apache 2.0). LoRA fine-tunes, cross-encoder architecture.

## Headline results (NDCG@10, public benchmarks)

| Domain | zerank | Cohere rerank-3.5 |
|---|---|---|
| Code | 0.754 | 0.724 |
| Finance | 0.894 | 0.824 |
| Legal | 0.821 | 0.804 |
| Medical | 0.796 | 0.750 |

On **private** datasets margins widen (Legal 0.854 vs 0.718) — evidence of better out-of-domain generalization.

## Notable claims

- **LLM ensembles beat equivalent human annotators** on training-data quality, and the data can be regenerated as base LLMs improve (no human-annotation bottleneck).
- **Hard-negative "Laffer curve"**: overly-intelligent mined negatives can exceed the quality of human-annotated positives, *degrading* performance — there is an optimum, not "harder is always better."

> [!gap] All NDCG figures are self-reported by the authors. No independent third-party reproduction was located.
