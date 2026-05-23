---
type: concept
title: "Specialized Eval Classifiers"
created: 2026-05-23
updated: 2026-05-23
status: developing
tags:
  - ai-agents
  - evaluation
  - llm
  - online-evaluation
related:
  - "[[Binary Evaluation vs Scoring]]"
  - "[[Online LLM-as-Judge]]"
  - "[[Online Evaluation Bottlenecks]]"
  - "[[Continuous Evaluation]]"
  - "[[Raindrop]]"
sources:
  - "[[2026 - Raindrop - Thoughts on Evals]]"
---

# Specialized Eval Classifiers

Running online evaluation through **many small, trained, single-purpose classifiers — one per failure signal** — instead of one general prompted LLM judge. The approach Raindrop ([[Raindrop]]) operationalizes: "train custom, **tiny models** to look at millions of events every day and pluck problematic events out," producing **billions of labels a month** (Source: [[2026 - Raindrop - Thoughts on Evals]]).

## How it differs from LLM-as-judge

| | [[Online LLM-as-Judge]] | Specialized eval classifiers |
|---|---|---|
| Model | one general LLM, prompted | many tiny models, trained |
| Granularity | rubric in a prompt | one model per signal |
| Coverage | sampled (cost) | feasible on ~100% of traffic |
| Output | score or binary verdict | per-signal **binary** label |
| New failure mode | edit the prompt | train a new classifier |

It is the **trained, distilled** end of the tiered judging stack in [[Online LLM-as-Judge]] (distilled judges at ~1/30 cost on 100% of traffic) — pushed to one classifier *per signal*. The per-signal decomposition is exactly the "many specific binary sub-checks" idea from [[Binary Evaluation vs Scoring]], implemented as models rather than prompts.

## Why it answers the cost bottleneck

The judge cost/latency limit in [[Online Evaluation Bottlenecks]] forces sampling for LLM judges. A tiny purpose-trained classifier is cheap enough to run on **every** event, so you trade prompt-flexibility for full-traffic coverage and the ability to detect rare/cohort-specific patterns a sampled judge would miss.

## Closed-set vs open-set

Raindrop pairs these classifiers with **semantic clustering** to discover *unexpected* failure modes (open-set), arguing that "online eval = offline eval on sampled prod data" is still closed-set. The system thus covers both known signals (trained per-signal classifiers) and unknown ones (clustering / anomaly detection).

## Open questions

- Per-classifier training/maintenance cost as the signal set grows — does it scale better than one judge prompt, or just relocate the labor?
- Label quality: tiny classifiers need training labels; where do they come from without reintroducing an LLM judge or human loop?
- Drift: each classifier can drift independently against a moving baseline ([[Online Evaluation Bottlenecks]]).
