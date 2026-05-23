---
type: source
title: "Evaluation and Benchmarking of LLM Agents: A Survey"
source_type: paper
author: "Mahmoud Mohammadi, Yipeng Li, Jane Lo, Wendy Yip"
date_published: 2025-07-29
url: "https://arxiv.org/abs/2507.21504"
created: 2026-05-23
updated: 2026-05-23
status: developing
confidence: high
key_claims:
  - "Organizes agent evaluation along a two-dimensional taxonomy: evaluation objectives (what — behavior, capabilities, reliability, safety) and evaluation process (how — interaction modes, datasets/benchmarks, metric computation, tooling)."
  - "Surfaces enterprise-specific challenges usually overlooked: role-based data access, reliability guarantees, dynamic long-horizon interactions, and compliance."
  - "Calls for holistic, more realistic, and scalable evaluation for real-world deployment."
tags:
  - ai-agents
  - evaluation
  - llm
  - survey
related:
  - "[[Online Evaluation Bottlenecks]]"
  - "[[Research - Online Evaluation in Production]]"
  - "[[Continuous Evaluation]]"
sources: []
---

# Evaluation and Benchmarking of LLM Agents: A Survey

Mohammadi et al., arXiv 2507.21504 (2025-07-29; KDD 2025). A practitioner-oriented survey that splits the field into **what to evaluate** and **how to evaluate**.

## Two-dimensional taxonomy

- **Evaluation objectives** — agent behavior, capabilities, reliability, safety.
- **Evaluation process** — interaction modes, datasets/benchmarks, metric-computation methods, tooling.

## Enterprise gaps (its distinctive contribution)

Flags four deployment realities "often overlooked in current research":
- **role-based data access**,
- **reliability guarantees**,
- **dynamic and long-horizon interactions**,
- **compliance**.

These are precisely the constraints that push evaluation *online* (into production) — feeding [[Online Evaluation Bottlenecks]] and [[Research - Online Evaluation in Production]].

## Relation to existing pages

Complements [[2025-03-20 - Yehudai et al - Survey on Evaluation of LLM-based Agents]] (capability-centric) with a process/deployment-centric lens. Reliability-as-objective aligns with [[Pass^k Reliability Metric]].
