---
type: source
title: "Gao et al — ALCE: Automatic Benchmark for LLM Generations with Citations"
created: 2026-05-23
updated: 2026-05-23
tags:
  - llm
  - evaluation
  - citation
  - rag
status: developing
source_type: paper
author: "Tianyu Gao, Howard Yen, Jiatong Yu, Danqi Chen"
date_published: 2023-05-23
url: "https://arxiv.org/abs/2305.14627"
confidence: high
related:
  - "[[Citation Precision and Recall]]"
  - "[[Attributed Text Generation]]"
  - "[[LLM-as-Judge]]"
  - "[[Eval Validity]]"
sources:
  - "https://ar5iv.labs.arxiv.org/html/2305.14627"
---

# Gao et al — ALCE

The foundational benchmark for evaluating LLM citations (arXiv 2305.14627, Princeton NLP). Systems generate long-form answers while citing passages from a retrieval corpus; ALCE scores the citations automatically. It defines the metric pair the whole field now uses — see [[Citation Precision and Recall]].

## The three evaluation axes

1. **Fluency** — MAUVE, against human reference text.
2. **Correctness** — dataset-specific (exact-match recall for ASQA/QAMPARI; sub-claim recall via NLI for ELI5).
3. **Citation quality** — precision + recall (below), the contribution that matters here.

## Citation Recall

For each statement, recall = 1 **iff** at least one citation exists AND an **NLI model** confirms the *concatenated cited passages entail the statement*. Averaged over all statements. → "Is every claim actually supported by what it cites?"

## Citation Precision

A citation is **irrelevant** when (1) that passage alone cannot support the statement, AND (2) removing it doesn't change whether the remaining citations still support it. A citation scores 1 if its statement has recall=1 and it is not irrelevant. → "Are there padding/decorative citations that don't pull weight?"

## NLI engine

Uses **TRUE** (T5-11B fine-tuned on NLI) for entailment. Premises = cited passages, hypothesis = the statement. Automated, reference-free at the citation level.

## Validity

Human–automatic agreement: Cohen's κ ≈ **0.70** for recall — substantial. This is why NLI-based citation scoring is trusted as a proxy for human judgment.

> [!note] ALCE is the canonical answer to "how do you evaluate a citation?": entailment-based precision/recall, not string overlap.
