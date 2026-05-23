---
type: source
title: "Pairwise or Pointwise? Evaluating Feedback Protocols for Bias in LLM-Based Evaluation"
source_type: paper
author: "Tuhina Tripathi, Manya Wadhwa, Greg Durrett, Scott Niekum"
date_published: 2025-04-20
url: "https://arxiv.org/abs/2504.14716"
created: 2026-05-23
updated: 2026-05-23
status: developing
confidence: high
key_claims:
  - "Absolute (pointwise) scoring is more robust than pairwise comparison to distractor manipulation: pairwise preferences flip in ~35% of cases vs ~9% for absolute scores."
  - "Pairwise judging is more vulnerable to 'distracted evaluation' — generators can embed spurious distractor features to skew the judge."
  - "Feedback-protocol choice should depend on dataset characteristics and evaluation objectives, not a universal default."
tags:
  - evaluation
  - llm
related:
  - "[[Binary Evaluation vs Scoring]]"
  - "[[LLM-as-Judge]]"
  - "[[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]]"
sources: []
---

# Pairwise or Pointwise? (Tripathi, Wadhwa, Durrett, Niekum)

arXiv 2504.14716, COLM 2025. Provides the empirical nuance under the binary-eval debate.

## Finding

Conventional wisdom (from MT-Bench / [[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]]) is that **pairwise** judging is more reliable than absolute scoring because relative judgments are easier. This paper complicates that: under **distractor manipulation**, **pairwise preferences flip ~35%** of the time vs only **~9%** for **absolute** scores. Absolute/pointwise scoring "better reflects response quality and is less influenced by distractor features."

## Why it matters for binary evaluation

The two reliability findings together point *away* from high-cardinality Likert scoring in opposite-looking directions — pairwise is easy but manipulable, fine-grained absolute is noisy. The convergent practical answer is **low-cardinality, well-defined labels**: a clear binary pass/fail with explicit criteria captures most of the benefit of both while minimizing the weaknesses. See [[Binary Evaluation vs Scoring]].

> [!contradiction] Tension with MT-Bench framing
> [[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]] favors pairwise over absolute scoring (relative is easier). This paper finds absolute *more robust to manipulation* (35% vs 9% flip). Not a flat contradiction — Zheng measures human-agreement on benign data, Tripathi measures robustness under adversarial distractors. Both support moving away from fine-grained Likert; they disagree on pairwise-vs-absolute, which is context-dependent.
