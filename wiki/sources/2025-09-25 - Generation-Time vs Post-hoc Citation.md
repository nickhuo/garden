---
type: source
title: "Generation-Time vs Post-hoc Citation: A Holistic Evaluation of LLM Attribution"
created: 2026-05-23
updated: 2026-05-23
tags:
  - llm
  - evaluation
  - citation
  - rag
status: developing
source_type: paper
author: "(arXiv 2509.21557)"
date_published: 2025-09-25
url: "https://arxiv.org/abs/2509.21557"
confidence: high
related:
  - "[[Generation-Time vs Post-hoc Citation]]"
  - "[[Citation Verification Pipeline]]"
  - "[[Citation Precision and Recall]]"
  - "[[Contextual Retrieval]]"
sources:
  - "https://arxiv.org/html/2509.21557"
---

# Generation-Time vs Post-hoc Citation

Holistic comparison of the two citation paradigms (arXiv 2509.21557, 2025). The empirical backbone for [[Generation-Time vs Post-hoc Citation]] as a concept.

## The two paradigms

- **G-Cite (generation-time)** — emit text and citation markers together during decoding.
- **P-Cite (post-hoc)** — draft the answer first, then add/verify citations in a separate pass.

## Metrics (5)

Citation **Precision**, **Recall**, **Correctness** (harmonic mean of the two), **Coverage** (fraction of ground-truth citations present), **Latency**. Plus human eval of **Answer Correctness** and **Citation Hallucination** (100 instances/method/dataset).

## Headline results

| | G-Cite | P-Cite |
|---|---|---|
| Coverage | ~37–65% | ~74–99% |
| Answer correctness (human) | 69% | **78%** |
| Citation hallucination (human) | 41% | **37%** |
| ALCE: coverage / correctness | 37% / 21% | **75% / 42%** |

- **Retrieval dominates.** Adding retrieval gave the largest gains regardless of paradigm — e.g. **~50-point** correctness jump on FEVER (27% → 77%). Fine-tuning is supplementary; it cannot replace retrieval.
- FEVER: G-Cite hits 94% correctness but only 27% coverage; P-Cite balances at 75% / 74%.

## Recommendation

A **retrieval-centric, P-Cite-first** approach for high-stakes applications; reserve G-Cite for precision-critical settings where coverage matters less. Advanced methods let practitioners tune the precision↔coverage tradeoff.
