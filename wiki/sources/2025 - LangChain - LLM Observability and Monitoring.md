---
type: source
title: "Why LLM Observability and Monitoring Needs Evaluations"
source_type: article
author: "LangChain"
date_published: 2025
url: "https://www.langchain.com/articles/llm-monitoring-observability"
created: 2026-05-23
updated: 2026-05-23
status: developing
confidence: medium
key_claims:
  - "Online evals run asynchronously on a sampled subset of live production traffic to give real-time feedback on agent quality — not every request, to avoid cost/latency."
  - "Production monitoring tracks four categories: tool-call latency/response times, token usage, error rates, and agent quality via evals (hallucination, reasoning quality, intent alignment, safety)."
  - "Quality degradation is caught with threshold alerts (e.g. hallucination eval <3 on >5% of traces in an hour → investigate; reasoning quality drops 20% week-over-week → investigate)."
  - "Offline evals run against a fixed dataset to confirm a fix works; online evals continuously monitor live multi-turn threads."
tags:
  - ai-agents
  - evaluation
  - observability
related:
  - "[[Continuous Evaluation]]"
  - "[[Online LLM-as-Judge]]"
  - "[[Online Evaluation]]"
sources: []
---

# Why LLM Observability and Monitoring Needs Evaluations (LangChain)

A LangChain article articulating the **industry-standard online-eval loop** for agents in production (vendor source — confidence medium, but representative of the dominant pattern across LangSmith/Arize/Langfuse/Datadog).

## The online loop

- **Sampled, asynchronous** evaluation of live traffic — trace ingestion adds no latency to the app; sampling sized to "detect drift and quality degradation" without evaluating every request.
- Functions as an **early-warning system**: catch issues before widespread user impact.

## What's monitored

Four metric families: latency/response time, token usage, error rates, and **quality-via-evals** (hallucination, reasoning quality, intent alignment, safety). Degradation handled by **threshold alerting** with concrete examples (see key_claims).

## Online vs offline (this source's framing)

Offline = run against a frozen dataset to confirm a fix; online = continuously monitor live, multi-turn threads. The two are complementary, not substitutes — offline gates changes, online catches drift the dataset can't see.

## Relevance

The canonical reference for [[Continuous Evaluation]] and the operational half of [[Online LLM-as-Judge]]. Aligns with the wiki's existing [[Online Evaluation]] page (offline defines "good," online keeps it calibrated).
