---
type: concept
title: "Agent Eval Pyramid"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - evaluation
  - methodology
  - infrastructure
status: seed
complexity: intermediate
domain: ai-agents
aliases:
  - eval pyramid
  - three-tier eval
  - agent evaluation hierarchy
related:
  - "[[LLM-as-Judge Evaluation]]"
  - "[[User Simulator Evaluation]]"
  - "[[Pass^k Reliability Metric]]"
  - "[[Trace-Based Evaluation]]"
  - "[[tau-bench]]"
  - "[[Workflows Beat Agents for Most Production]]"
  - "[[Online Evaluation]]"
  - "[[Eval Validity]]"
sources:
  - "[[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]]"
---

# Agent Eval Pyramid

## Summary

A three-tier evaluation strategy for AI agents, organized by cost and faithfulness. Cheap, fast, deterministic checks at the base; expensive, faithful, simulated-user evals at the top. The pyramid shape implies: most coverage should come from cheap tiers; expensive tiers are reserved for capability claims, not routine regression.

## The three tiers

### Tier 1 — Unit tests (deterministic)

**Cost:** very low. **Speed:** fast (seconds). **Faithfulness:** high for the specific behavior tested.

Assertions on crisp, binary behaviors:
- Format checks (valid JSON? correct tool name?)
- Schema validation (outputs match expected shape?)
- Boundary conditions (refuses when it should? handles malformed inputs?)
- Regression guards (once a bug is fixed, a test locks it out)

Key insight from [[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]]: unit tests are **underused for agents** because practitioners assume non-determinism pervades everything. In reality, many agent behaviors are crisply deterministic even in otherwise stochastic systems. If something can be checked by a regex or a schema validator, it should not consume an LLM judge call.

### Tier 2 — LLM-as-judge (semantic evaluation)

**Cost:** medium (one LLM call per sample). **Speed:** moderate. **Faithfulness:** depends on calibration.

When correctness is semantic rather than structural:
- Single-call judges preferred over chains
- Multi-axis rubrics: factual accuracy, task completion, tool selection, format, tone (where relevant)
- Correctness and style scored on **separate axes** — never collapsed to a single score
- Calibrated periodically against human-labeled sets (50–200 examples)
- Judges final state, not trajectory (usually)

See [[LLM-as-Judge Evaluation]] for full treatment.

### Tier 3 — End-to-end with simulated users

**Cost:** high (many LLM calls per episode, full trajectory). **Speed:** slow. **Faithfulness:** highest for multi-turn tasks.

For tasks that inherently require multi-turn interaction:
- An LLM plays the user; the agent plays the agent. Closed loop.
- Simulator has user profile + goals; does NOT see agent tool calls — mirrors deployment.
- Reward from environment state where possible (eliminates judge subjectivity for constrained domains).
- Stochasticity accumulates across turns → [[Pass^k Reliability Metric]] is required.

Reference implementation: [[tau-bench]] (Sierra, 2024). Matches Anthropic's Tier 3 prescription almost exactly.

## Design principles

1. **Maximize Tier 1 coverage.** Every crisp, deterministic behavior should have a unit test. This is the cheapest regression signal.
2. **Calibrate Tier 2 judges regularly.** A stale judge may no longer reflect human judgment; judge drift is a real failure mode.
3. **Reserve Tier 3 for capability claims.** Full simulated-user evals are expensive; use them to validate key capability claims, not every PR.
4. **Cross-tier consistency check.** A Tier 1 pass + Tier 2 fail = a semantic error not caught by format. A Tier 2 pass + Tier 3 fail = a consistency/reliability problem (agent is correct in isolation but breaks under natural user variation).

## Practical implications

- Build the eval suite before the agent, or at minimum in parallel. Without measurement, progress is invisible.
- [[Trace-Based Evaluation]] sits orthogonally to the pyramid — traces serve all three tiers by enabling failure attribution and coverage analysis.
- The pyramid is not a waterfall. All three tiers run in CI/CD; Tier 3 runs less frequently.

## Connection to broader wiki

- [[Workflows Beat Agents for Most Production]] — workflows have more Tier-1-testable surfaces than agents; the pyramid asymmetry partially explains why workflows are easier to trust in production.
- [[LLM-as-Judge Evaluation]] — Tier 2 in full detail.
- [[User Simulator Evaluation]] — Tier 3 in full detail.
- [[Pass^k Reliability Metric]] — the metric that Tier 3 requires.
- [[tau-bench]] — reference Tier 3 implementation.

## Sources

- [[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]]
