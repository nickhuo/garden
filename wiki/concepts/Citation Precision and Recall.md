---
type: concept
title: "Citation Precision and Recall"
created: 2026-05-23
updated: 2026-05-23
tags:
  - llm
  - citation
  - evaluation
  - rag
status: developing
complexity: intermediate
domain: llm
aliases:
  - "citation recall"
  - "citation precision"
  - "citation quality metric"
related:
  - "[[Attributed Text Generation]]"
  - "[[Citation Verification Pipeline]]"
  - "[[LLM-as-Judge]]"
  - "[[Eval Validity]]"
  - "[[Trace-Based Evaluation]]"
sources:
  - "[[2023-05-23 - Gao et al - ALCE]]"
  - "[[2025-09-25 - Generation-Time vs Post-hoc Citation]]"
---

# Citation Precision and Recall

## One-Line Definition

The standard metric pair for "is this citation good?" — **recall** = every claim is supported by what it cites; **precision** = no irrelevant citations padding the answer. Both computed via **NLI entailment**, not string matching. (Source: [[2023-05-23 - Gao et al - ALCE]])

## Citation Recall

Per statement, recall = 1 **iff** a citation exists AND an NLI model judges the **concatenated cited passages entail the statement**. Averaged over statements. Answers: *does the evidence actually back the claim?*

## Citation Precision

A citation is **irrelevant** if (1) it alone can't support the statement AND (2) removing it doesn't change whether the rest still support it. Precision rewards removing decorative citations. Answers: *is every citation pulling weight?*

## The fuller scorecard

The [[2025-09-25 - Generation-Time vs Post-hoc Citation]] paper extends this to 5 axes: precision, recall, **correctness** (harmonic mean), **coverage** (fraction of ground-truth citations present), latency — plus human eval of answer-correctness and citation-hallucination.

Harvey's [[2025 - Harvey - BigLaw Bench Sources|BigLaw Bench]] is a coarser, product-side variant: document-level +1-per-sourced-claim scoring (a deliberate lower bound, because passage-level scoring trades off against answer quality).

## Why NLI, not overlap

String/keyword overlap can't tell whether a passage *entails* a claim. An NLI model (ALCE uses TRUE / T5-11B) checks logical support. Validity: human–auto agreement Cohen's κ ≈ 0.70 — strong enough to trust as a [[LLM-as-Judge]]-style automatic proxy. Rests on [[Eval Validity]]: the metric must track what humans mean by "well-cited."

## For Nick

This is the measurable target for a **citation ground**: track citation recall (no unsupported claim) and precision (no padding) per answer, NLI-scored, surfaced in [[Trace-Based Evaluation]].
