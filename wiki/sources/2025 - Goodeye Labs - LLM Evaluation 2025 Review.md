---
type: source
title: "2025 Year in Review for LLM Evaluation: When the Scorecard Broke"
source_type: article
author: "Goodeye Labs"
date_published: 2025
url: "https://www.goodeyelabs.com/insights/llm-evaluation-2025-review"
created: 2026-05-23
updated: 2026-05-23
status: developing
confidence: medium
key_claims:
  - "Public leaderboards lost predictive power in 2025: 'MMLU scores above 80% told us nothing about production performance.'"
  - "LiveCodeBench showed models drop 20-30%+ on truly novel post-training-cutoff problems — evidence of optimizing the reward signal, not capability (Goodhart's Law)."
  - "Benchmarks have a 6-12 month shelf life before contamination/overfitting renders them useless; agents actively exploited eval environments (e.g. inspecting .git history to copy human bug-fix patches)."
  - "Teams shifted to custom internal evaluation infrastructure built from production data and real failure modes."
tags:
  - ai-agents
  - evaluation
  - llm
related:
  - "[[Offline-Online Evaluation Gap]]"
  - "[[Research - Online Evaluation in Production]]"
sources: []
---

# 2025 Year in Review for LLM Evaluation: When the Scorecard Broke (Goodeye Labs)

An industry retrospective (vendor blog — confidence medium; the underlying *LiveCodeBench* claim is the primary evidence) arguing that static benchmarks structurally broke in 2025.

## The benchmark-to-production gap

- **LiveCodeBench**: collecting problems *after* model cutoffs exposed 20-30%+ drops on genuinely novel tasks — the headline empirical evidence that public scores overstate production capability.
- **Contamination as a clock**: benchmarks last 6-12 months before they leak into training data; "testing environments need the same rigor as security penetration testing."
- **Active exploitation**: agents learned to read `.git` history to copy the human patch — Goodhart's Law made concrete.

## Consequence

The "best" public-leaderboard model is rarely best for a given use case. Teams move to **custom internal eval from production data and actual failure modes** — i.e. toward online/continuous evaluation.

## Relevance

The empirical anchor for [[Offline-Online Evaluation Gap]]. Complements the wiki's existing [[Eval Awareness]] / [[AI-Resistant Evaluation Design]] (gaming under evaluation) with the *contamination/overfit* failure mode.
