---
type: synthesis
title: "Research - Online Evaluation in Production"
created: 2026-05-23
updated: 2026-05-23
tags:
  - research
  - ai-agents
  - evaluation
  - llm
status: developing
related:
  - "[[Continuous Evaluation]]"
  - "[[Online LLM-as-Judge]]"
  - "[[Offline-Online Evaluation Gap]]"
  - "[[Online Evaluation Bottlenecks]]"
  - "[[Binary Evaluation vs Scoring]]"
  - "[[Specialized Eval Classifiers]]"
  - "[[Online Evaluation]]"
  - "[[Research - Online Evaluation]]"
sources:
  - "[[2025-03-20 - Yehudai et al - Survey on Evaluation of LLM-based Agents]]"
  - "[[2025-07-29 - Mohammadi et al - Evaluation and Benchmarking of LLM Agents]]"
  - "[[2025-03-28 - Guan et al - Multi-Turn Conversational Agent Evaluation Survey]]"
  - "[[2025 - LangChain - LLM Observability and Monitoring]]"
  - "[[2025 - Goodeye Labs - LLM Evaluation 2025 Review]]"
  - "[[2026 - Raindrop - Thoughts on Evals]]"
  - "[[2026-01-15 - Husain Shankar - LLM Evals FAQ]]"
  - "[[2025-04-20 - Tripathi et al - Pairwise or Pointwise]]"
---

# Research - Online Evaluation in Production

> Companion to the theory/Nick-connected page [[Research - Online Evaluation]]. This page is the **external industry + empirical** view (2025-2026 sources), answering Nick's four questions.

## Overview

Online evaluation of agent applications has consolidated, in 2025-2026, into a standard production loop — **trace → sample → judge → alert** — backed by a tiered judge stack (cheap distilled / per-signal classifiers on ~100% of traffic, expensive LLM-judge passes on flagged anomalies). The case for it is now *empirical*, not just principled: public benchmarks measurably mispredict production. The binding constraints are operational (judge cost/latency, statistical power, credit assignment), not conceptual.

## Key Findings — by Nick's four questions

### 1. Industry practices
- The dominant pattern is **continuous evaluation as observability**: online evals run **asynchronously on sampled live traffic**, monitoring four families — latency, token usage, error rates, and quality-via-evals — with threshold alerting as an early-warning system (Source: [[2025 - LangChain - LLM Observability and Monitoring]]). See [[Continuous Evaluation]].
- Tooling has converged on the same loop with different emphasis (Arize/Confident-AI on production-trace online eval; LangSmith on dev loops; Braintrust on unified eval+observability; Langfuse on infra-owned; Datadog on APM-integrated).
- **Dissenting practice — Raindrop** ([[Raindrop]]): argues most "online eval" is just *offline eval on sampled prod data* (closed-set) and can't find unexpected failures. Their alternative is **open-set discovery** — many trained per-signal binary classifiers on 100% of traffic + semantic clustering (Source: [[2026 - Raindrop - Thoughts on Evals]]). The **closed-set vs open-set** distinction is the sharpest framing this round added.

### 2. Most-used methods + their gaps
- **Online LLM-as-judge** is the workhorse ([[Online LLM-as-Judge]]); 2026 adds **distilled evaluators** (~1/30 cost, 100% coverage) and step-level agentic judges reserved for flagged anomalies.
- **Specialized per-signal classifiers** ([[Specialized Eval Classifiers]]): Raindrop's approach — many tiny *trained* binary classifiers, one per failure signal, on 100% of traffic (billions of labels/month), plus semantic clustering for open-set discovery (Source: [[2026 - Raindrop - Thoughts on Evals]]).
- **A/B testing** is the only causally trustworthy verdict ([[A-B Testing for Agents]]).
- **Label design**: the field favors **binary pass/fail over Likert scoring** ([[Binary Evaluation vs Scoring]]) — popularized by Husain & Shankar ([[2026-01-15 - Husain Shankar - LLM Evals FAQ]]), backed by judge-reliability research ([[2025-04-20 - Tripathi et al - Pairwise or Pointwise]]: absolute flips 9% vs pairwise 35%). *Not* originally Anthropic, whose rubrics are graded 0.0-1.0.
- **Gaps** (both surveys agree): cost-efficiency, safety, robustness, fine-grained/scalable methods (Source: [[2025-03-20 - Yehudai et al - Survey on Evaluation of LLM-based Agents]]); plus enterprise gaps — role-based access, reliability guarantees, long-horizon, compliance (Source: [[2025-07-29 - Mohammadi et al - Evaluation and Benchmarking of LLM Agents]]).

### 3. Why online beats offline
- Empirically: **LiveCodeBench shows 20-30%+ drops** on post-cutoff novel problems; benchmarks have a **6-12 month contamination shelf-life**; agents exploit `.git` history — Goodhart's Law (Source: [[2025 - Goodeye Labs - LLM Evaluation 2025 Review]]). See [[Offline-Online Evaluation Gap]].
- Online captures the construct offline cannot: "did this land for *this* user, now?" ([[Online Evaluation]]). **Caveat:** offline still gates large changes and safety-critical checks — online complements, not replaces.

### 4. Bottlenecks
Catalogued in [[Online Evaluation Bottlenecks]]: no runtime ground truth; judge cost ($0.01-0.10/assessment) + latency forcing sampling; **statistical power (10,000+ trajectories/arm** for A/B on quality metrics); **credit assignment** over delayed multi-turn outcomes (Source: [[2025-03-28 - Guan et al - Multi-Turn Conversational Agent Evaluation Survey]]); baseline drift; online reward-hacking.

## Key Concepts
- [[Continuous Evaluation]]: always-on sampled eval over live traffic
- [[Online LLM-as-Judge]]: the judging mechanism
- [[Specialized Eval Classifiers]]: many tiny per-signal binary classifiers (Raindrop)
- [[Binary Evaluation vs Scoring]]: pass/fail over Likert — lineage and why
- [[Offline-Online Evaluation Gap]]: the empirical why-online
- [[Online Evaluation Bottlenecks]]: the operational limits

## Contradictions
- **"Online strictly beats offline"** is wrong as stated. The gap evidence argues offline *mispredicts* production, but offline retains a role for large jumps, regression, and safety (consistent with [[Online Learning from Interaction]]). Flagged on [[Offline-Online Evaluation Gap]].

## Open Questions
- Quantitative size of the offline-online gap outside coding (LiveCodeBench is the cleanest case).
- Production cost/latency profile of step-level agentic judges (benchmark results don't translate directly to live cost).
- Solving credit assignment for free-form multi-turn agent outcomes (RL value-transport is only a candidate).
- Statistical evaluation for low-traffic products that cannot reach A/B significance.
- Detecting online reward-hacking before it harms long-term value.
- **Open-set discovery**: how to find failure modes nobody specified, beyond clustering — does the trained-classifier approach ([[Specialized Eval Classifiers]]) scale as the signal set grows, or just relocate the labeling labor?
- When is numeric scoring worth its cost over binary checks ([[Binary Evaluation vs Scoring]])?

## Sources
- [[2025-03-20 - Yehudai et al - Survey on Evaluation of LLM-based Agents]] — 2025, ACL Findings
- [[2025-07-29 - Mohammadi et al - Evaluation and Benchmarking of LLM Agents]] — 2025, KDD
- [[2025-03-28 - Guan et al - Multi-Turn Conversational Agent Evaluation Survey]] — 2025
- [[2025 - LangChain - LLM Observability and Monitoring]] — 2025 (vendor, medium confidence)
- [[2025 - Goodeye Labs - LLM Evaluation 2025 Review]] — 2025 (vendor, medium confidence)
- [[2026 - Raindrop - Thoughts on Evals]] — 2026 (vendor, medium confidence)
- [[2026-01-15 - Husain Shankar - LLM Evals FAQ]] — 2026 (practitioner, high)
- [[2025-04-20 - Tripathi et al - Pairwise or Pointwise]] — COLM 2025 (peer-reviewed, high)
