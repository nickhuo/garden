---
type: entity
title: "OpenAI"
created: 2026-05-22
updated: 2026-05-22
tags:
  - ai-agents
  - llm
  - entity
  - org
status: seed
entity_type: organization
role: "AI research and deployment company; maker of the GPT/o-series models, the Agents SDK, and the moderation API. Publisher of 'A Practical Guide to Building Agents'."
first_mentioned: 2026-05-22
related:
  - "[[OpenAI Agents SDK]]"
  - "[[John Schulman]]"
  - "[[Anthropic]]"
sources:
  - "[[2025 - OpenAI - A Practical Guide to Building Agents]]"
---

# OpenAI

## Summary

AI research and deployment company. In the agent-building context tracked by this wiki, OpenAI ships the **[[OpenAI Agents SDK]]** (code-first agent orchestration), the GPT-4o / o1 / o3-mini model line referenced for agent reasoning and instruction-generation, the **moderation API** used as a guardrail layer, and **computer-use models** for driving legacy UIs. Its guide [[2025 - OpenAI - A Practical Guide to Building Agents]] is the OpenAI-side counterpart to Anthropic's [[2024-12-19 - Anthropic - Building Effective Agents]].

## Why it matters here

OpenAI and [[Anthropic]] are the two primary sources of practical agent-building doctrine in this wiki. Their guidance converges (start simple, add agents only when needed, layer guardrails) under different vocabularies — see [[OpenAI Practical Guide vs Anthropic Building Effective Agents]].

## Connections

- [[OpenAI Agents SDK]] — its agent framework
- [[John Schulman]] — RL researcher (ex-OpenAI), already in the wiki
- [[Anthropic]] — the parallel vendor doctrine
- [[Manager Pattern]], [[Agent Handoffs]], [[Agent Guardrails]] — patterns named in its guide

## Sources

- [[2025 - OpenAI - A Practical Guide to Building Agents]]
