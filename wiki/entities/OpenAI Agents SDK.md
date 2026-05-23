---
type: entity
title: "OpenAI Agents SDK"
created: 2026-05-22
updated: 2026-05-22
tags:
  - ai-agents
  - entity
  - product
  - orchestration
status: seed
entity_type: product
role: "OpenAI's code-first agent orchestration framework: agents, tools, Runner.run() loop, handoffs, and first-class guardrails."
first_mentioned: 2026-05-22
related:
  - "[[OpenAI]]"
  - "[[Agent Run Loop]]"
  - "[[Manager Pattern]]"
  - "[[Agent Handoffs]]"
  - "[[Agent Guardrails]]"
sources:
  - "[[2025 - OpenAI - A Practical Guide to Building Agents]]"
---

# OpenAI Agents SDK

## Summary

OpenAI's framework for building agents, used throughout [[2025 - OpenAI - A Practical Guide to Building Agents]]. Core primitives:

- **`Agent`** — name + instructions + tools (and optionally `output_type`, `handoffs`, `input_guardrails`).
- **`Runner.run()`** — the [[Agent Run Loop]]: loops over the LLM until a final-output tool fires or the model returns no tool calls.
- **Tools** — Python functions (`@function_tool`) or built-ins (e.g. `WebSearchTool`); see [[Agent Tool Categories]].
- **Handoffs** — a handoff is itself a *tool*; calling it transfers execution and conversation state to another agent ([[Agent Handoffs]]).
- **Guardrails** — first-class, run with **optimistic execution** (concurrent with the main agent, raising tripwire exceptions on breach); see [[Agent Guardrails]].

## Design stance: code-first, not declarative

The SDK deliberately rejects **declarative graph** frameworks (which require defining every node/edge upfront and often a DSL). It uses a **code-first** approach: express workflow logic with ordinary programming constructs, no pre-defined graph — favoring dynamic, adaptable orchestration. This is the SDK's main differentiator versus graph-based frameworks (e.g. LangGraph-style).

## Connections

- [[OpenAI]] — vendor
- [[Manager Pattern]] / [[Agent Handoffs]] — the two multi-agent patterns it supports
- [[Agentic Harness]] — the SDK is one concrete harness implementation
- Contrast: declarative graph frameworks (a wiki gap — see [[Multi-Agent Systems]] open questions)

## Sources

- [[2025 - OpenAI - A Practical Guide to Building Agents]]
