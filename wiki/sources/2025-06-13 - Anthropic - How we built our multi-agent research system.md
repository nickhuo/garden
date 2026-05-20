---
type: source
title: How we built our multi-agent research system
aliases:
  - How we built our multi-agent research system
created: 2026-05-04
updated: 2026-05-13
tags:
- ai-agents
- anthropic
- multi-agent
- research
- evaluation
status: mature
related: []
sources:
  - "[[.raw/articles/2025-06-13 - Anthropic - How we built our multi-agent research system.md]]"
source_type: blog
author: Anthropic
date_published: 2025-06-13
url: https://www.anthropic.com/engineering/multi-agent-research-system
confidence: medium
key_claims: []
---

# How we built our multi-agent research system (Anthropic, 2025-06-13)

## Summary

Anthropic's engineering walkthrough of their **Research** product feature — a multi-agent system where a LeadResearcher orchestrates parallel subagents, each with their own context window. Quantifies the cost-benefit boundary precisely (4× / 15× token usage) and explicitly carves out coding as workflow-territory while claiming research as multi-agent's home.

## Architecture

- **LeadResearcher** plans the task → persists plan to **Memory** (because plans can exceed 200K context)
- LeadResearcher **dynamically spawns** subagents — count, scope, tools all decided on the fly per query
- Each subagent has its own context, runs **interleaved thinking** between tool calls
- **CitationAgent** runs as a final pass to ground claims in sources
- **Artifact system** — subagents write outputs to filesystem to bypass coordinator bottleneck

## Headline numbers

- Multi-agent (Opus 4 lead + Sonnet 4 subagents) **beats single-agent Opus 4 by 90.2%** on internal research eval
- **Token usage explains 80% of performance variance** on BrowseComp; +tool-call count + model = 95%
- Cost: agents ~**4× chat tokens**; multi-agent ~**15× chat tokens**
- Tool-description rewrite yielded **40% faster task completion**

## Core argument

> "Multi-agent systems work mainly because they help spend enough tokens to solve the problem… token usage by itself explains 80% of the variance, with the number of tool calls and the model choice as the two other explanatory factors."

Multi-agent isn't smarter — it's a *parallelism harness* that spends more tokens in parallel. See [[Token Economics]].

## When multi-agent wins (Anthropic's explicit triple-conjunction)

> "We've found that multi-agent systems excel at valuable tasks that involve heavy parallelization, information that exceeds single context windows, and interfacing with numerous complex tools."

Outside this triple-conjunction, workflows remain the better choice.

## Explicit anti-pattern: coding

> "Most coding tasks involve fewer truly parallelizable tasks than research, and LLM agents are not yet great at coordinating and delegating to other agents in real time."

Coding is carved out of multi-agent territory.

## Pressure on prior thesis

This post does not link [[Building Effective Agents]], but its substance:

- **Tightens the carve-out for agents** rather than expanding it — provides the cleanest empirical case for *when* multi-agent wins (research / breadth-first / context overflow)
- **Reclassifies orchestrator-workers** — earlier post called it a workflow with predefined dispatch; here it's an agent loop with dynamic spawning. See [[Orchestrator-Workers]] for the workflow-vs-agent variant split.
- **Confirms agents-are-expensive** with sharper numbers (4× / 15×), strengthening [[Workflows Beat Agents for Most Production]] as a default

## Patterns and concepts introduced

- [[Multi-Agent Systems]] — the architectural family
- [[Token Economics]] — 4× / 15× as operational test
- [[LLM-as-Judge Evaluation]] — eval methodology
- Tool-testing agent — see [[ACI - Agent-Computer Interface]]
- Memory (plan persistence) — see [[Augmented LLM]]
- Artifact system — subagents write to shared filesystem

## Eval methodology

Pivot from process-fidelity to **end-state evaluation**: same input has many valid solution paths, so deterministic step matching is wrong. Use [[LLM-as-Judge Evaluation]] with rubric-based scoring (0.0–1.0) plus mandatory human spot-checking.

## Verbatim claims worth quoting

- "Our internal evaluations show that multi-agent research systems excel especially for breadth-first queries that involve pursuing multiple independent directions simultaneously."
- "There is a downside: in practice, these architectures burn through tokens fast. In our data, agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats."
- "Most coding tasks involve fewer truly parallelizable tasks than research, and LLM agents are not yet great at coordinating and delegating to other agents in real time."
- "Prompt engineering [for agents] = teaching the agent to think like the orchestrator does."

## Entities mentioned (not pages yet, per schema)

- Research (Claude product feature) — single mention as a product
- BrowseComp (OpenAI's browsing eval) — single mention
- Claude Opus 4 / Sonnet 4 / Sonnet 3.7 — model versions, no page

## Source location

- Raw: `raw/2025-06-13 - Anthropic - How we built our multi-agent research system.md`
