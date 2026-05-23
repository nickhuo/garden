---
type: concept
title: "Continuous Evaluation"
created: 2026-05-23
updated: 2026-05-23
status: developing
tags:
  - ai-agents
  - evaluation
  - observability
related:
  - "[[Online Evaluation]]"
  - "[[Online LLM-as-Judge]]"
  - "[[Online Evaluation Bottlenecks]]"
  - "[[Trace-Based Evaluation]]"
sources:
  - "[[2025 - LangChain - LLM Observability and Monitoring]]"
---

# Continuous Evaluation

The **industry-practice layer** of online evaluation: treating evaluation as always-on observability over live traffic, not a pre-release gate. This is how production teams actually operationalize [[Online Evaluation]].

## The standard loop

1. **Trace everything** from day one (structured logs; see [[Trace-Based Evaluation]]). Ingestion is **asynchronous** — no added app latency.
2. **Sample** live traffic and run evals on the sample — sized to detect drift/degradation without the cost of judging every request.
3. **Monitor four families**: tool-call latency, token usage, error rates, and **quality-via-evals** (hallucination, reasoning quality, intent alignment, safety).
4. **Threshold-alert**: e.g. hallucination eval <3 on >5% of traces/hour, or reasoning quality −20% week-over-week → investigate. An **early-warning system**.

## Tooling landscape (described, not endorsed)

Platforms converge on this loop with different emphasis: **Arize** / Confident-AI lead on production-trace + session online evals; **LangSmith** is an agent-engineering platform (dev loops); **Braintrust** frames eval + observability as one connected quality-management system; **Langfuse** targets infra-owned observability; **Datadog** folds custom LLM-as-judge evals into general APM. The pattern matters more than the vendor.

## The 2026 shift

Cheap **distilled evaluators** now score ~100% of traffic at roughly 1/30 the cost (format, schema, banned-phrase, simple quality), reserving expensive [[Agent-as-a-Judge]] for flagged anomalies and sampled audits — a tiered coverage strategy that manages the cost bottleneck.

## Relation to existing pages

The operational sibling of [[Online Evaluation]] (which holds the *why*) and [[Online LLM-as-Judge]] (the *judging mechanism*). Its limits are catalogued in [[Online Evaluation Bottlenecks]]. Distinct from offline regression suites, which still gate large changes (see [[Offline-Online Evaluation Gap]]).
