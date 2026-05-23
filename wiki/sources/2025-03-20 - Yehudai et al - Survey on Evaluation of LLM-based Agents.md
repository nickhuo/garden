---
type: source
title: "Survey on Evaluation of LLM-based Agents"
source_type: paper
author: "Asaf Yehudai, Lilach Eden, Alan Li, Guy Uziel, Yilun Zhao, Roy Bar-Haim, Arman Cohan, Michal Shmueli-Scheuer"
date_published: 2025-03-20
url: "https://arxiv.org/abs/2503.16416"
created: 2026-05-23
updated: 2026-05-23
status: developing
confidence: high
key_claims:
  - "First comprehensive survey of LLM-agent evaluation, organized across five perspectives: core capabilities, application-specific benchmarks, generalist-agent evaluation, benchmark dimensions, and developer frameworks/tools."
  - "The field is shifting toward more realistic, challenging evaluations with continuously updated benchmarks — away from static assessment."
  - "Named research gaps: cost-efficiency, safety, robustness, and fine-grained / scalable evaluation methods."
tags:
  - ai-agents
  - evaluation
  - llm
  - survey
related:
  - "[[Online Evaluation Bottlenecks]]"
  - "[[Continuous Evaluation]]"
  - "[[Research - Online Evaluation in Production]]"
sources: []
---

# Survey on Evaluation of LLM-based Agents

Yehudai et al., arXiv 2503.16416 (v1 2025-03-20; ACL Findings 2025). The first broad survey of how LLM-based agents — systems that "plan, reason, and use tools while interacting with dynamic environments" — are evaluated.

## Five perspectives

1. **Core LLM capabilities** for agentic workflows (planning, tool use).
2. **Application-specific benchmarks** (web agents, SWE agents).
3. **Generalist-agent evaluation.**
4. **Core dimensions** of agent benchmarks.
5. **Evaluation frameworks and tools** for developers.

## What it contributes here

- Authoritative confirmation that evaluation is moving from **static** toward **continuously updated / dynamic** benchmarks — the academic mirror of the industry move to [[Continuous Evaluation]].
- Names the gap set this research targets: **cost-efficiency, safety, robustness, fine-grained/scalable methods** — directly feeding [[Online Evaluation Bottlenecks]].

## Relation to existing pages

Sits above the wiki's existing offline stack ([[Agent Eval Pyramid]], [[tau-bench]], [[Trace-Based Evaluation]]) as the survey-level framing; complements the production view in [[Research - Online Evaluation in Production]].
