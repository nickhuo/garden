---
type: concept
title: "Trace-Based Evaluation"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - evaluation
  - debugging
  - methodology
status: seed
complexity: intermediate
domain: ai-agents
aliases:
  - trace evaluation
  - execution trace grading
related:
  - "[[Agent Eval Pyramid]]"
  - "[[LLM-as-Judge]]"
  - "[[Pass^k Reliability Metric]]"
  - "[[User Simulator Evaluation]]"
  - "[[Session as Event Log]]"
  - "[[Error Trace Retention]]"
sources:
  - "[[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]]"
---

# Trace-Based Evaluation

## Summary

Structured logging of every agent action — tool calls, inputs, outputs, timing, reasoning steps — to enable **post-hoc failure attribution** without re-running expensive end-to-end evaluations. Traces are stored and queryable; they sit between unit tests and full end-to-end evals in the [[Agent Eval Pyramid]].

## What a trace contains

- Tool call name + inputs at each step
- Tool output (result or error)
- Agent reasoning (if CoT is visible)
- Timestamps / wall-clock time per step
- Final outcome (success / failure / partial)

## What traces enable

**Failure attribution** — given a failed episode, at which step did the agent's trajectory diverge? Without traces, you can only observe final-state failure; with traces, you can localize the error to a specific step, tool, or reasoning segment.

**Intermediate-state checkpoints** — some trajectories have natural checkpoints where correctness can be assessed before the end (e.g., "did the agent retrieve the right document before synthesizing?"). These mid-trace checks are cheaper than full end-to-end evals.

**Coverage metrics** — across a test suite, which tools were called? Which were never exercised? Coverage gaps surface missing test diversity or missing agent capability.

**Debugging without re-running** — full end-to-end evals with simulated users are expensive (tokens + time). Trace logs let teams debug past failures without incurring that cost again.

## Design principles

- **Log from day 1.** Retroactive trace instrumentation is painful. It must be a first-class concern at agent architecture time.
- **Structured format is required.** Free-text logs don't allow automated analysis; traces must be machine-parseable (JSON, structured events).
- **Include timing.** Latency is often a proxy for cost and a signal for compute-intensive reasoning paths.
- **Tie traces to eval runs.** Each trace should carry an eval-run ID so failures can be grouped by prompt version, model version, and task type.

## Relationship to adjacent concepts

- **[[Session as Event Log]]** — a runtime design pattern for agents to maintain state; traces are the eval-side complement. Both treat the agent's history as a first-class artifact.
- **[[Error Trace Retention]]** — Manus's pattern of keeping error stacks in context for LLM reasoning; trace-based eval makes those same error stacks available to the eval infrastructure.
- **[[LLM-as-Judge]]** — judges typically grade final output; with traces, a judge can also grade intermediate steps (e.g., "was the correct tool selected at step 4?").
- **[[Pass^k Reliability Metric]]** — traces across k runs of the same task enable per-step variance analysis: is the failure consistent at the same step, or does it vary?

## Limitations

- Storage cost at scale: full traces for every eval run in production can be expensive.
- Privacy: traces may contain sensitive intermediate data (user PII in tool inputs/outputs); requires access control.
- Trace fidelity: if the agent's reasoning is not exposed (e.g., opaque API calls), trace depth is limited to tool call boundaries.

## Sources

- [[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]]
