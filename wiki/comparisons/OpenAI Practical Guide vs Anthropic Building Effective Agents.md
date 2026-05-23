---
type: comparison
title: "OpenAI Practical Guide vs Anthropic Building Effective Agents"
created: 2026-05-22
updated: 2026-05-22
status: developing
tags:
  - ai-agents
  - orchestration
  - comparison
related:
  - "[[Workflows vs Agents]]"
  - "[[Manager Pattern]]"
  - "[[Agent Handoffs]]"
  - "[[Orchestrator-Workers]]"
  - "[[Agent Guardrails]]"
sources:
  - "[[2025 - OpenAI - A Practical Guide to Building Agents]]"
  - "[[2024-12-19 - Anthropic - Building Effective Agents]]"
---

# OpenAI Practical Guide vs Anthropic Building Effective Agents

The two flagship vendor guides on building agents. They give **convergent advice under divergent vocabularies**. This page maps one onto the other.

## Core advice — they agree

Both say: **use the simplest thing that works, add complexity only when forced.** Anthropic frames it as **[[Workflows vs Agents]]** ("find the simplest solution possible, and only increase complexity when needed"); OpenAI frames it as **single-vs-multi-agent** ("maximize a single agent's capabilities first… more agents add complexity and overhead"). Same gradient, different axis labels.

## Vocabulary map

| Concept | OpenAI guide | Anthropic guide |
|---|---|---|
| Central coordinator delegating to specialists | **[[Manager Pattern]]** (agents as tools) | **[[Orchestrator-Workers]]** |
| Classify-then-dispatch / peer transfer | **[[Agent Handoffs]]** (decentralized) | **[[Routing]]** |
| The base unit | model + tools + instructions | **[[Augmented LLM]]** (LLM + retrieval + tools + memory) |
| The control structure | **[[Agent Run Loop]]** (`Runner.run()`) | the agent loop in [[Autonomous Agents]] |
| Tool design discipline | standardized defs, [[Agent Tool Categories]] | [[ACI - Agent-Computer Interface]], [[Agent Interface Contracts]] |
| Safety layer | **[[Agent Guardrails]]** + tool risk ratings | [[Permission Model]], [[Minimal Footprint Principle]] |

## Where emphasis differs

- **Decision axis.** Anthropic's load-bearing distinction is *workflow (code-orchestrated) vs agent (model-orchestrated)*. OpenAI mostly assumes you're building an agent and asks *one agent or many*. So OpenAI under-emphasizes the "maybe you don't need an agent at all" point that Anthropic makes central — though OpenAI's "When should you build an agent?" section (complex decisions / unwieldy rules / unstructured data) covers the same ground.
- **Guardrails.** OpenAI gives a far more concrete **guardrail typology** (relevance/safety/PII/moderation/tool-safeguards/rules/output-validation + optimistic tripwire execution + human-in-the-loop triggers) than Anthropic's guide, which leans on general "guardrails" and ACI quality. This is the OpenAI guide's strongest unique contribution to the wiki.
- **Framework stance.** OpenAI explicitly argues **code-first over declarative graphs** (see [[OpenAI Agents SDK]]); Anthropic's guide is framework-agnostic and warns against over-relying on frameworks at all.
- **Multi-agent caution.** Anthropic's later work ([[Multi-Agent Systems]]) supplies a sharp *triple-conjunction* for when multi-agent pays off (parallelizable + context-overflow + high-value, ~15× tokens). OpenAI's guide is softer ("complex logic" or "tool overload"), without the cost framing of [[Token Economics]].

## Synthesis

For this wiki the two guides are complementary: **Anthropic supplies the taxonomy and the cost discipline; OpenAI supplies the guardrail typology and concrete SDK patterns.** The running thesis [[Workflows Beat Agents for Most Production]] is consistent with both — OpenAI's "maximize one agent first" is the same caution stated from the multi-agent side.

## Sources

- [[2025 - OpenAI - A Practical Guide to Building Agents]]
- [[2024-12-19 - Anthropic - Building Effective Agents]]
