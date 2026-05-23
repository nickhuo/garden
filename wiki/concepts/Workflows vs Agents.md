---
type: concept
title: Workflows vs Agents
created: 2026-05-04
updated: 2026-05-04
tags:
- ai-agents
- taxonomy
- foundations
status: developing
related:
- "[[Code-to-the-Side vs Orchestration]]"
sources:
- "[[2024-12-19 - Anthropic - Building Effective Agents]]"
- "[[2025-06-13 - Anthropic - How we built our multi-agent research system]]"
- "[[2026-04-08 - Anthropic - Scaling Managed Agents]]"
_legacy_source_count: 3
---

# Workflows vs Agents

## Summary

The central distinction in [[Building Effective Agents]]: **Workflows** orchestrate LLMs through *predefined code paths*; **Agents** let LLMs *dynamically direct their own processes and tool usage*. Both are flavors of "agentic systems" — the question is **who decides the next step**: code (workflow) or model (agent).

[[How we built our multi-agent research system]] adds a third position — **Multi-agent systems** — which is structurally on the agent side but with parallelism as the defining feature.

[[Scaling Managed Agents]] adds a layer ABOVE this whole taxonomy — the [[Meta-Harness]] (e.g., [[Managed Agents]]) — which hosts arbitrary harnesses, regardless of whether they're workflow-style or agent-style. The dichotomy doesn't dissolve; it gets a runtime substrate.

## Definitions (Anthropic)

- **Workflow** — system where LLMs and tools are orchestrated through predefined code paths.
- **Agent** — system where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks.
- **Multi-agent system** — orchestrator + dynamically-spawned subagents running in parallel. See [[Multi-Agent Systems]].

## Trade-offs

| | Workflow | Agent | Multi-agent |
|---|---|---|---|
| Predictability | High | Low | Low |
| Latency | Low | Higher | Lower than single-agent (parallel) |
| Cost (token mult.) | ~1–2× | ~4× | ~15× |
| Error compounding | Bounded | Significant | Per-subagent bounded; coordinator risk |
| Best for | Well-scoped tasks | Open-ended exploration | Breadth-first, parallelizable, context-overflow |

Token multipliers from [[Token Economics]] (Anthropic 2025-06).

## Decision rule (synthesized across both sources)

1. Default to a single [[Augmented LLM]] call.
2. If task structure is bounded but multi-step: pick a workflow pattern.
3. If task is open-ended and value clears 4× cost: single agent ([[Autonomous Agents]]).
4. If additionally task parallelizes and exceeds context: multi-agent.
5. **Coding** is currently workflow-territory by Anthropic's own admission.

## OpenAI's parallel framing (2026-05-22)

OpenAI's [[2025 - OpenAI - A Practical Guide to Building Agents]] reaches the same caution from a different axis. Where Anthropic's load-bearing choice is *workflow vs agent* (who decides the next step), OpenAI mostly assumes you're building an agent and asks *single vs multi-agent* — advising **"maximize a single agent's capabilities first,"** which is the same "use the simplest thing that works" instinct. Split to multi-agent only on **complex logic** (many conditional branches) or **tool overload** (similarity/overlap, not raw count). Its two multi-agent patterns — [[Manager Pattern]] (≈ [[Orchestrator-Workers]]) and [[Agent Handoffs]] (≈ [[Routing]]) — slot under the agent/multi-agent side here. Full mapping: [[OpenAI Practical Guide vs Anthropic Building Effective Agents]].

## Connections

- Foundational primitive: [[Augmented LLM]]
- OpenAI's parallel framing: [[OpenAI Practical Guide vs Anthropic Building Effective Agents]], [[Manager Pattern]], [[Agent Handoffs]]
- Workflow patterns: [[Prompt Chaining]] · [[Routing]] · [[Parallelization]] · [[Orchestrator-Workers]] · [[Evaluator-Optimizer]]
- Agent pattern: [[Autonomous Agents]]
- Multi-agent: [[Multi-Agent Systems]]
- Layer above: [[Meta-Harness]] (substrate that hosts any of these)
- Position to track: [[Workflows Beat Agents for Most Production]]
- Operational decision tool: [[Token Economics]]
- Context discipline: [[Context Engineering]]

## Open questions

- Is the binary distinction durable, or will hybrid architectures (graph-based, planner-executor, swarm) erode it?
- The [[Orchestrator-Workers]] page now distinguishes a workflow variant and an agent variant — does the same split apply to other patterns ([[Evaluator-Optimizer]] in particular)?
- Does multi-agent advantage hold as single-agent context windows grow (1M+)?

## Sources

- [[Building Effective Agents]] (Anthropic, 2024-12-19)
- [[How we built our multi-agent research system]] (Anthropic, 2025-06-13)
- [[Scaling Managed Agents]] (Anthropic, 2026-04-08)
