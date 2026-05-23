---
type: concept
title: "Agent-as-a-Judge"
created: 2026-05-23
updated: 2026-05-23
status: seed
tags:
  - ai-agents
  - evaluation
  - llm
related:
  - "[[Online LLM-as-Judge]]"
  - "[[LLM-as-Judge Evaluation]]"
  - "[[Trace-Based Evaluation]]"
  - "[[Agent Eval Pyramid]]"
sources:
  - "[[2024-10-14 - Zhuge et al - Agent-as-a-Judge]]"
---

# Agent-as-a-Judge

An evaluating **agent** that judges another agent by inspecting its *entire chain of actions and decisions*, emitting **step-level intermediate feedback** — not just scoring the final output. Introduced by Zhuge et al. ([[2024-10-14 - Zhuge et al - Agent-as-a-Judge]]).

## Why it exists

Outcome-only judging (the default [[LLM-as-Judge]]) discards the step-by-step structure that *is* an agent's work; manual trajectory review doesn't scale. Agent-as-a-Judge sits between them: automated, but trajectory-aware.

## Evidence

On **DevAI** (55 realistic automated AI-development tasks, 365 hierarchical requirements), it "dramatically outperforms LLM-as-a-Judge and is as reliable as the human evaluation baseline."

## Where it fits

- **Higher fidelity, higher cost** than a single-call judge → in production it is reserved for **flagged anomalies and sampled audits**, while distilled judges cover the bulk of traffic (see [[Online LLM-as-Judge]], [[Continuous Evaluation]]).
- Consumes the **trace**, so it depends on [[Trace-Based Evaluation]] infrastructure.
- A new top tier on the [[Agent Eval Pyramid]]: step-level agentic judging above single-call semantic judging.

## Open questions

- Cost/latency at production scale (the paper is benchmark-time, not live).
- Does the evaluating agent inherit the same [[Jagged Intelligence]] / [[Eval Awareness]] failure modes as the agent it judges?
