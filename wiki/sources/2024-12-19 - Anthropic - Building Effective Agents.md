---
type: source
title: Building effective agents
aliases:
  - Building Effective Agents
created: 2026-05-04
updated: 2026-05-13
tags:
- ai-agents
- anthropic
- foundations
- taxonomy
status: mature
related: []
sources:
  - "[[.raw/articles/2024-12-19 - Anthropic - Building Effective Agents.md]]"
source_type: blog
author: Anthropic — Erik Schluntz, Barry Zhang
date_published: 2024-12-19
url: https://www.anthropic.com/engineering/building-effective-agents
confidence: medium
key_claims: []
---

# Building Effective Agents (Anthropic, 2024-12-19)

## Summary

Anthropic's engineering post arguing that successful production deployments of LLMs use **simple, composable patterns** rather than complex frameworks. Codifies a taxonomy: **Workflows** (LLMs orchestrated through predefined code paths) vs **Agents** (LLMs that dynamically direct their own processes). Five named workflow patterns + one autonomous agent pattern, all built on an "augmented LLM" base primitive. Closes with three principles: simplicity, transparency, deliberate ACI design.

## Central claim

> "Consistently, the most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns."

The thesis: most teams shipping LLM features should use Workflows; reach for Agents only when the problem demands open-ended exploration. Tracked as [[Workflows Beat Agents for Most Production]].

## Taxonomy introduced

- **Foundational primitive:** [[Augmented LLM]] (LLM + retrieval + tools + memory)
- **Central distinction:** [[Workflows vs Agents]]
- **Workflow patterns:** [[Prompt Chaining]] · [[Routing]] · [[Parallelization]] · [[Orchestrator-Workers]] · [[Evaluator-Optimizer]]
- **Agent pattern:** [[Autonomous Agents]]
- **Tool design framing:** [[ACI - Agent-Computer Interface]]

## Notable claims (verbatim)

- "**Workflows** are systems where LLMs and tools are orchestrated through predefined code paths."
- "**Agents** … are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."
- "When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed."
- "Success in the LLM space isn't about building the most sophisticated system. It's about building the *right* system for your needs."
- "While building our agent for SWE-bench, we actually spent more time optimizing our tools than the overall prompt." (anchors the [[ACI - Agent-Computer Interface]] argument)
- Frameworks (LangGraph, Rivet, Vellum) "make it easy to get started but … abstract away the underlying prompts and responses, making them harder to debug." Recommends developers call LLM APIs directly first.

## Closing principles

1. **Simplicity** — start with single LLM call, add complexity only when measured value justifies it.
2. **Transparency** — explicitly show the agent's planning steps so behavior is debuggable.
3. **ACI** — invest in agent-computer interface (tool docs, schemas, error messages) the way teams invest in HCI.

## Entities mentioned

- [[MCP]] — Anthropic's Model Context Protocol for third-party tool integration
- Claude Agent SDK (Anthropic) — passing reference; not yet a wiki page
- Strands Agents SDK (AWS), Rivet (Ironclad), Vellum, LangGraph — name-checked, no wiki page yet (per schema: ≥2 mentions before stub)
- SWE-bench / SWE-bench Verified — referenced as eval; no wiki page yet
- Anthropic Workbench — internal prompt iteration tool

## Production domains highlighted

- **Customer support** — call/email handling with [[Routing]] and tool access
- **Coding agents** — verifiable correctness (test pass/fail) makes agents tractable here

## Open questions raised

- Practical heuristic for "when does the problem warrant Agent over Workflow?" — Anthropic gestures, doesn't formalize.
- Does the binary Workflow-Agent distinction hold against graph-based / swarm architectures? Need 2nd source.

## Source location

- Raw: `raw/2024-12-19 - Anthropic - Building Effective Agents.md`
