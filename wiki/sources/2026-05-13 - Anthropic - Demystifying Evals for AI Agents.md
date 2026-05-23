---
type: source
title: Demystifying evals for AI agents
aliases:
  - "Demystifying evals for AI agents"
  - "Demystifying Evals for AI Agents"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - evals
  - evaluation
  - methodology
status: developing
related:
  - "[[LLM-as-Judge Evaluation]]"
  - "[[User Simulator Evaluation]]"
  - "[[Pass^k Reliability Metric]]"
  - "[[tau-bench]]"
  - "[[Trace-Based Evaluation]]"
  - "[[Agent Eval Pyramid]]"
sources:
  - "[[.raw/articles/2026-05-13 - Anthropic - Demystifying Evals for AI Agents.md]]"
source_type: article
author: Anthropic
date_published: 2026-05-13
url: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
confidence: high
key_claims:
  - "Agent evals require three tiers: unit tests, LLM-as-judge, and end-to-end simulated-user evals"
  - "Unit tests are underused for agents — many behaviors are crisply deterministic even in non-deterministic systems"
  - "Correctness and style must be scored as separate rubric axes; conflating them biases toward well-formatted wrong answers"
  - "Trace logging from day 1 enables post-hoc failure attribution without re-running expensive end-to-end evals"
  - "LLM judges require periodic calibration against human-labeled sets; judge drift is a real failure mode"
  - "Evals are a product, not a script — they require ongoing maintenance and extension"
---

# Demystifying Evals for AI Agents

**Source:** Anthropic Engineering Blog
**URL:** https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
**Published:** 2026-05-13

## Summary

Anthropic's engineering team presents a three-tier framework for evaluating AI agents. The central tension: agents are multi-step, non-deterministic systems — evaluating them with single-call, trajectory-fixed scripts fails. The solution is a layered approach (unit tests → LLM judges → full simulated-user evals) combined with trace logging and calibrated judges.

Core thesis: **evals are a product, not a script.** An eval suite requires ongoing calibration, extension, and human involvement.

## Key claims

### 1. The eval pyramid for agents

Three tiers, cheapest to most faithful:

1. **Unit tests (deterministic)** — format checks, schema validation, boundary conditions, regression guards. Underused because practitioners assume agents are inherently non-deterministic; in reality many behaviors are crisply checkable.
2. **LLM-as-judge (semantic)** — single-call, multi-axis rubric; calibrated against human labels; judges final state not trajectory.
3. **End-to-end with simulated users** — an LLM plays the user in closed loop; environment-state reward where possible (cf. [[tau-bench]]); expensive but most faithful for multi-turn tasks.

See [[Agent Eval Pyramid]] for the full framing.

### 2. Trace-based evaluation

Log all tool calls, inputs, outputs, timing in a structured format from day 1. Traces enable:
- Post-hoc failure attribution (at which step did the agent diverge?)
- Intermediate-state checkpoints
- Coverage metrics (which tools were exercised?)

See [[Trace-Based Evaluation]].

### 3. Correctness vs style separation

A critical anti-pattern: letting LLM judges conflate factual accuracy with formatting or tone. Multi-axis rubrics must score these independently. A well-formatted wrong answer should fail; a clunkily formatted correct answer should pass.

Builds on [[LLM-as-Judge Evaluation]] — extends its multi-axis prescription with an explicit correctness/style split.

### 4. Judge calibration

LLM judges drift with model updates and prompt changes. Anthropic maintains 50–200-example human-labeled calibration sets. When judge-human correlation drops below threshold, re-calibration runs. This is a structural maintenance practice, not a one-time setup.

### 5. Human-in-the-loop as structural, not fallback

Three roles: (a) calibration-set labeling, (b) weekly/biweekly spot-checks, (c) adversarial probing that generates new test cases. Human review is load-bearing infrastructure, not a gap-filler.

### 6. Non-determinism framing

Three challenges in agent eval: multiple valid paths to goal, long-horizon credit assignment, compounding errors. Pass^k ([[Pass^k Reliability Metric]]) is the formal tool for surfacing stochasticity. User simulators ([[User Simulator Evaluation]]) are the entropy source that makes pass^k informative.

## Connections

- Directly enriches [[LLM-as-Judge Evaluation]] — adds calibration sets, correctness/style split, single-call preference.
- Directly enriches [[User Simulator Evaluation]] — reaffirms the simulated-user pattern as Tier 3, adds info-asymmetry constraint.
- Directly enriches [[Pass^k Reliability Metric]] — explains the mechanism (multi-turn stochasticity accumulation).
- Cross-validates [[tau-bench]]'s methodology from an Anthropic perspective — confirms environment-state reward > LLM-judge for constrained domains.
- New concept: [[Trace-Based Evaluation]] — post-hoc failure attribution via structured trace logs.
- New concept: [[Agent Eval Pyramid]] — three-tier layered eval strategy.
- Reinforces [[Workflows Beat Agents for Most Production]] — the unit-test underuse claim reveals a practical asymmetry: workflows have more unit-testable surfaces.

## Open questions raised

- At what scale does LLM-judge eval cost itself become a production bottleneck? (Token Economics implication not quantified.)
- How do calibration sets handle distribution shift when the agent's task domain expands?
- Can intermediate-state trace checkpoints substitute for full end-to-end evals on a subset of tasks?
