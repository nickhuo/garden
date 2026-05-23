---
type: source
title: "LLM Evals: Everything You Need to Know (Evals FAQ)"
source_type: article
author: "Hamel Husain, Shreya Shankar"
date_published: 2026-01-15
url: "https://hamel.dev/blog/posts/evals-faq/"
created: 2026-05-23
updated: 2026-05-23
status: developing
confidence: high
key_claims:
  - "Use binary (pass/fail) labels, not 1-5 Likert scales: 'Start with binary labels to understand what bad looks like. Numeric labels are advanced and usually not necessary.'"
  - "Likert scales fail three ways: adjacent points (3 vs 4) are subjective and inconsistent across annotators; detecting differences needs larger samples; annotators default to middle values to hide uncertainty."
  - "Decompose into specific binary sub-checks rather than one holistic score — e.g. instead of rating factual accuracy 1-5, track '4 of 5 expected facts included' as separate binary evals."
  - "Error analysis (read the failures, cluster them, write checks for the common ones) is the foundational eval practice."
tags:
  - evaluation
  - llm
  - methodology
related:
  - "[[Binary Evaluation vs Scoring]]"
  - "[[LLM-as-Judge Evaluation]]"
  - "[[Eval Validity]]"
sources: []
---

# LLM Evals: Everything You Need to Know (Hamel Husain & Shreya Shankar)

Husain & Shankar, hamel.dev, 2026-01-15 (companion to their "Evals for AI Engineers" course/book, taught to 700+ engineers and at OpenAI/Anthropic). The primary practitioner source for the **binary-over-scoring** doctrine.

## The binary argument

> "Start with binary labels to understand what 'bad' looks like. Numeric labels are advanced and usually not necessary."

Three problems with 1-5 Likert scoring:
1. **Subjective boundaries** — the gap between 3 and 4 is inconsistent across annotators.
2. **Statistical power** — detecting a difference on a numeric scale needs larger samples than a binary one.
3. **Annotator avoidance** — people default to middle values to dodge a hard judgment. Binary "forces clearer thinking" and compels a domain expert to draw a clear acceptable/unacceptable line.

## Not one score — many specific checks

Rather than a holistic rating, **decompose** into specific binary sub-checks (e.g. "4 of 5 expected facts included"). This preserves granularity while keeping each label clear — the conceptual seed of Raindrop's per-signal classifier approach ([[Specialized Eval Classifiers]]).

## Lineage note

They present this as "sharp opinions about what works," from course experience — **not** cited to academic work, and **not** originally from Anthropic (whose [[LLM-as-Judge Evaluation]] guidance uses graded 0.0-1.0 rubrics). The empirical backing comes separately from judge-reliability research. Full lineage: [[Binary Evaluation vs Scoring]].
