---
type: source
title: "Agent-as-a-Judge: Evaluate Agents with Agents"
source_type: paper
author: "Mingchen Zhuge et al. (metauto-ai)"
date_published: 2024-10-14
url: "https://arxiv.org/abs/2410.10934"
created: 2026-05-23
updated: 2026-05-23
status: developing
confidence: high
key_claims:
  - "Agent-as-a-Judge uses agentic systems to evaluate agentic systems, providing intermediate feedback for the entire task-solving process rather than scoring only the final outcome."
  - "Current evaluation is inadequate for agents: it either focuses only on final outcomes (ignoring the step-by-step nature of agentic systems) or requires excessive manual labor."
  - "On the DevAI benchmark (55 realistic automated AI-development tasks, 365 hierarchical requirements), Agent-as-a-Judge dramatically outperforms LLM-as-a-Judge and is as reliable as the human-evaluation baseline."
tags:
  - ai-agents
  - evaluation
  - llm
related:
  - "[[Agent-as-a-Judge]]"
  - "[[Online LLM-as-Judge]]"
  - "[[Trace-Based Evaluation]]"
sources: []
---

# Agent-as-a-Judge: Evaluate Agents with Agents

Zhuge et al. (metauto-ai), arXiv 2410.10934 (2024-10-14). Introduces the **[[Agent-as-a-Judge]]** paradigm: an evaluating agent that inspects the whole chain of actions and decisions, emitting **step-level intermediate feedback** instead of grading a final answer.

## Why existing eval falls short for agents

Two failure modes: outcome-only judging discards the step-by-step structure that *is* the agent's work; manual trajectory review doesn't scale. Agent-as-a-Judge targets both.

## DevAI benchmark + result

- **DevAI**: 55 realistic automated AI-development tasks with 365 hierarchical user requirements and rich annotations.
- Agent-as-a-Judge "dramatically outperforms LLM-as-a-Judge and is as reliable as our human evaluation baseline" (no per-metric numbers on the abstract page).

## Relevance to online evaluation

The step-level judge is the higher-fidelity end of the production judging spectrum (see [[Online LLM-as-Judge]]); in production it is typically reserved for **flagged anomalies / sampled audits** because of its cost, with cheap distilled judges covering 100% of traffic. Connects to [[Trace-Based Evaluation]] (it consumes the trace, not just the output).
