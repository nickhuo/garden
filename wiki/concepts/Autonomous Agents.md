---
type: concept
title: Autonomous Agents
created: 2026-05-04
updated: 2026-05-13
tags:
- ai-agents
- agent-pattern
status: developing
related: []
sources:
- "[[2024-12-19 - Anthropic - Building Effective Agents]]"
- "[[2024-06-17 - Yao et al - tau-bench]]"
- "[[2026-04 - Anthropic - Claude Code Auto Mode]]"
- "[[2025-06-13 - Anthropic - How we built our multi-agent research system]]"
_legacy_source_count: 2
---

# Autonomous Agents

## Summary

Per [[Building Effective Agents]]: systems where the LLM **plans and executes independently**, using tools and environmental feedback to direct its own process. Distinct from workflows in that the control flow is decided by the model, not by code.

## Anatomy

- Triggered by a user instruction
- Plans next step → calls tool → reads tool output → re-plans
- Continues until task completion, max-step limit, or human stop signal
- Often pairs with sandboxed environments to bound damage

See [[Ralph Loop]] for a strongly-opinionated, monolithic instantiation of this loop applied to coding (one task per loop, single process, human-as-loop-watcher).

## When to use

When the problem space is open-ended, the number of steps is unpredictable, and pre-defining a workflow is intractable. **Costs:** compounding errors over long horizons, latency, expense.

## Examples (per Anthropic)

- Coding agents working on SWE-bench tasks
- Computer-use agents

## Connections

- Built from: [[Augmented LLM]]
- Family: [[Workflows vs Agents]]
- Multi-agent variant: [[Multi-Agent Systems]] (parallelism harness on top of single-agent loop)
- Tool interface critical: [[ACI - Agent-Computer Interface]]
- Cost discipline: [[Token Economics]] (~4× chat tokens for single-agent)
- Eval methodology: [[LLM-as-Judge Evaluation]] · [[Pass^k Reliability Metric]] · [[User Simulator Evaluation]] · [[tau-bench]]
- Position to track: [[Workflows Beat Agents for Most Production]]

## Reliability ceiling (measured)

Per [[2024-06-17 - Yao et al - tau-bench]], even SOTA function-calling agents (gpt-4o) solve <50% of constrained customer-service tasks. Reliability across repeated trials is worse — pass^8 < 25% on the easier retail domain. This is the load-bearing empirical anchor for any "agents in production" claim.

## Open questions

- ~~Durable framework for evaluating agent reliability over long horizons?~~ — answered by τ-bench's database-state grading + pass^k. Now the question is whether the technique generalizes beyond domains where unique-outcome scenarios can be constructed (coding/research/open-ended tasks remain hard).
- At what point does planning quality (vs raw model size) dominate agent reliability?
- Does single-agent's cost advantage over [[Multi-Agent Systems]] hold as context windows grow (1M+) and parallelism becomes intra-context?

## Headless deployments and the permission model

[[2026-04 - Anthropic - Claude Code Auto Mode]] introduces the production pattern for deploying autonomous agents without a human in the loop. [[Claude Code]]'s auto mode provides a [[Permission Classifier]] that routes tool calls to auto-approve or human review based on semantic risk — solving the CI/CD and server-side deployment problem without blanket "approve everything" flags.

The recommended production pattern: classifier policy + OS sandbox + audit log. Defense in depth, not just model-level reasoning.

This source also operationalizes the [[Minimal Footprint Principle]] — previously stated as in-context guidance — at the tool-call layer via the Permission Classifier. Same principle, two enforcement points.

## Sources

- [[2024-06-17 - Yao et al - tau-bench]] (Yao et al, Sierra, 2024-06-17)
- [[Building Effective Agents]] (Anthropic, 2024-12-19)
- [[How we built our multi-agent research system]] (Anthropic, 2025-06-13)
- [[2026-04 - Anthropic - Claude Code Auto Mode]] (Anthropic, April 2026)
