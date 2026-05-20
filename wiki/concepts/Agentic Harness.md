---
type: concept
title: "Agentic Harness"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - coding
status: seed
related:
  - "[[Autonomous Agents]]"
  - "[[Meta-Harness]]"
  - "[[Augmented LLM]]"
  - "[[SWE-bench Verified]]"
  - "[[Workflows vs Agents]]"
  - "[[ACI - Agent-Computer Interface]]"
sources:
  - "[[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]]"
complexity: basic
domain: ai-agents
aliases:
  - agent scaffold
  - agent wrapper
---

# Agentic Harness

## Definition

An **agentic harness** (also "agent scaffold") is the minimal infrastructure wrapping an LLM to enable agentic behavior: tool access, an action loop, and a stopping condition. It is the "outside" of an agent — the code that gives the model its hands and memory interface — as distinct from the model itself.

The term sits between [[Augmented LLM]] (the base primitive: LLM + tools) and [[Meta-Harness]] (Anthropic's production-scale hosting abstraction for long-running agents). An agentic harness is typically task-scoped and lightweight. See [[Harness Design Patterns]] for the catalog of patterns and anti-patterns that apply across this spectrum.

## Minimal anatomy

A harness typically provides:
1. **Tool definitions** — file read, shell exec, file edit, test runner, web browser, etc.
2. **Action loop** — invoke model → parse tool calls → execute → feed result back → repeat
3. **Budget / stopping condition** — max steps, max tokens, success signal (e.g., test pass)
4. **Context management** — how prior steps are summarized or truncated as the conversation grows

## Simplicity as a finding (SWE-bench result)

The Anthropic [[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]] result directly demonstrates that **harness simplicity is not the capability bottleneck**. A simple loop with standard coding tools + [[Claude 3.5 Sonnet]] achieved 49% on [[SWE-bench Verified]], outperforming prior approaches that used more complex scaffolding (ensembles, retrieval pipelines, parallel sampling).

This implies:
- Prior SOTA complexity was compensating for weaker base models
- The harness is an [[ACI - Agent-Computer Interface]] design problem, not an orchestration problem — get the tools right, then let the model drive

## Relation to other concepts

| Concept | Relationship |
|---------|-------------|
| [[Augmented LLM]] | An agentic harness instantiates one; adds the loop and stopping logic |
| [[Autonomous Agents]] | The pattern the harness enables — model chooses its own action sequence |
| [[Workflows vs Agents]] | A harness can host either; an autonomous coding harness is firmly "agent" side |
| [[Meta-Harness]] | Production-grade harness abstraction; same idea scaled to multi-tenant, long-horizon |
| [[Orchestrator-Workers]] | Multi-agent variant of a harness |

## Tension with Meta-Harness

If a simple harness achieves 49% on SWE-bench, the incremental capability value of [[Meta-Harness]] (Anthropic's heavy infra abstraction) is not self-evident from the capability axis alone. Meta-Harness buys reliability, observability, cost management, and multi-agent coordination — but not raw capability per task. This is a tension worth tracking.

> [!contradiction]
> [[Meta-Harness]] argues for infra-heavy scaffolding for production agents. The SWE-bench Verified result (simple harness, 49% pass@1) suggests that for capability on well-specified isolated tasks, complexity adds little. The resolution is likely domain: isolated task capability vs. production reliability at scale are different goals served by different layers.

## Sources

- [[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]] (Anthropic, 2024-10-29)
