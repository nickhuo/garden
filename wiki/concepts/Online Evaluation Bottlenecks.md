---
type: concept
title: "Online Evaluation Bottlenecks"
created: 2026-05-23
updated: 2026-05-23
status: developing
tags:
  - ai-agents
  - evaluation
  - llm
related:
  - "[[Online Evaluation]]"
  - "[[Online LLM-as-Judge]]"
  - "[[A-B Testing for Agents]]"
  - "[[Continuous Evaluation]]"
  - "[[Eval Validity]]"
sources:
  - "[[2025-07-29 - Mohammadi et al - Evaluation and Benchmarking of LLM Agents]]"
  - "[[2025-03-28 - Guan et al - Multi-Turn Conversational Agent Evaluation Survey]]"
  - "[[2025 - LangChain - LLM Observability and Monitoring]]"
---

# Online Evaluation Bottlenecks

Where online evaluation actually breaks in production — the operational and statistical limits that the methodology pages ([[Online Evaluation]], [[LLM-as-Judge Evaluation]]) leave as open questions.

## 1. No ground truth at runtime

Production has no labels. You only see behavior + implicit signals ([[Implicit Feedback Signals]]); the "correct" answer is unknown. Every online metric is therefore a **proxy**, and proxy quality is itself unmeasured live — the core [[Eval Validity]] problem.

## 2. Judge cost and latency

Running an [[Online LLM-as-Judge]] on traffic costs roughly **$0.01-0.10 per assessment** and adds latency. You cannot judge every request → you **sample**, which trades coverage for cost. Distilled/cheap judges (≈1/30 the cost) can cover 100% for format/schema/banned-phrase checks; expensive [[Agent-as-a-Judge]] runs only on flagged anomalies and sampled audits. Guardrail judges need *low* latency, capping how good they can be. The aggressive mitigation is [[Specialized Eval Classifiers]] — tiny *trained* per-signal binary models cheap enough to run on 100% of traffic — trading prompt flexibility for full coverage.

## 2b. Closed-set vs open-set

Sampling + prompted judges only catch failures you *specified* (closed-set). Finding **unexpected** failure modes (open-set) needs semantic clustering / anomaly detection over full traffic, not a fixed rubric — the central critique in [[Specialized Eval Classifiers]] (Raindrop).

## 3. Statistical power

[[A-B Testing for Agents]] is the only causally trustworthy verdict, but LLM stochasticity inflates the sample requirement — "**10,000+ trajectories per arm**" for quality metrics (vs thousands traditionally), because variation *is* the signal. Low-traffic products may never reach significance; underpowered tests waste resources and risk shipping regressions (a p=0.18 ship ≈ 1-in-5 chance of a regression).

## 4. Credit assignment over multi-turn / delayed reward

A session outcome (success, churn, satisfaction) is **delayed** and must be attributed to specific earlier actions — temporal credit assignment. Multi-turn evaluation's "end-to-end user experience" target (Source: [[2025-03-28 - Guan et al - Multi-Turn Conversational Agent Evaluation Survey]]) is exactly the signal hardest to attribute. Borrowed RL machinery (TD-style value transport) is the candidate, but unsolved for free-form agent turns.

## 5. Baseline drift

Even with no variant change, the underlying model, retrieval index, or tool definitions move. "A test that runs for two weeks against a moving baseline tells you very little" — drift contaminates both A/B arms and judge calibration.

## 6. Online reward-hacking

When implicit feedback becomes the optimization target, agents can optimize **engagement over correctness** (engagement-via-frustration). Detecting this before it harms long-term value is an open monitoring problem.

## Enterprise constraints (amplifiers)

Role-based data access, reliability guarantees, long-horizon interactions, and compliance (Source: [[2025-07-29 - Mohammadi et al - Evaluation and Benchmarking of LLM Agents]]) make sampling, logging, and judging harder in regulated settings.

## Relation to existing pages

Consolidates micro-gaps previously scattered across [[Online Evaluation]], [[Implicit Feedback Signals]], [[A-B Testing for Agents]], and [[Learning from Implicit Feedback]] into one operational view.
