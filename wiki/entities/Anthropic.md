---
type: entity
title: Anthropic
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - organization
status: developing
entity_type: organization
role: AI safety company and primary author of the AI-agents corpus in this wiki
first_mentioned: "[[2024-12-19 - Anthropic - Building Effective Agents]]"
related:
  - "[[MCP]]"
  - "[[Managed Agents]]"
  - "[[Multi-Agent Systems]]"
  - "[[Orchestrator-Workers]]"
  - "[[Context Engineering]]"
sources:
  - "[[2024-12-19 - Anthropic - Building Effective Agents]]"
  - "[[2025-06-13 - Anthropic - How we built our multi-agent research system]]"
  - "[[2025-09-29 - Anthropic - Effective context engineering for AI agents]]"
  - "[[2025-11-24 - Anthropic - Advanced Tool Use]]"
  - "[[2026-04-08 - Anthropic - Scaling Managed Agents]]"
  - "[[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]]"
  - "[[2026-05-13 - Anthropic - Postmortem Three Recent Issues]]"
---

# Anthropic

## Summary

AI safety company and primary author of the agent-patterns corpus in this wiki. Anthropic's engineering blog and research publications have provided the canonical workflow/agent taxonomy ([[Building Effective Agents]], 2024), the multi-agent research system architecture, the context engineering framework, advanced tool use patterns, the [[Managed Agents]] infrastructure primitive, and the C compiler parallel-agents experiment.

## Role in the wiki

Dominant source. 7 of 26+ source pages are Anthropic-authored. Their framing (workflow vs agent, triple-conjunction for multi-agent, context engineering) is the foundational taxonomy for the `ai-agents` domain.

## Key contributions to this wiki

| Source | Key concept introduced |
|---|---|
| [[2024-12-19 - Anthropic - Building Effective Agents]] | Workflow/agent taxonomy: [[Parallelization]], [[Orchestrator-Workers]], [[Evaluator-Optimizer]], [[Prompt Chaining]], [[Routing]] |
| [[2025-06-13 - Anthropic - How we built our multi-agent research system]] | [[Multi-Agent Systems]] architecture (lead + parallel subagents); triple-conjunction |
| [[2025-09-29 - Anthropic - Effective context engineering for AI agents]] | [[Context Engineering]], [[Long-Horizon Context Management]], sub-agents as context discipline |
| [[2025-11-24 - Anthropic - Advanced Tool Use]] | [[Programmatic Tool Calling]], [[Logit Masking]], [[Tool Search Tool]] |
| [[2026-04-08 - Anthropic - Scaling Managed Agents]] | [[Managed Agents]], [[Meta-Harness]], stateless-cattle pattern |
| [[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]] | [[Agent Interface Contracts]]; complicates "coding less parallelizable than research" claim |
| [[2026-05-13 - Anthropic - Postmortem Three Recent Issues]] | [[Cache Invalidation Cascade]], [[Context Assembly Pipeline]], [[Config Type Safety]]; LLM-as-judge deployed on live production traffic |

## Entities they've created

- [[MCP]] — Model Context Protocol, open standard for tool/context interfaces
- [[Managed Agents]] — hosted agent-as-a-service primitive (2026)

## Caveats

The corpus skews toward Anthropic's own framing. No OpenAI, DeepMind, or contrarian sources yet. Treat taxonomy as a useful starting model, not ground truth.
