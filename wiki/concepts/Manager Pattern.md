---
type: concept
title: "Manager Pattern"
created: 2026-05-22
updated: 2026-05-22
status: seed
tags:
  - ai-agents
  - agent-pattern
  - orchestration
related:
  - "[[Agent Handoffs]]"
  - "[[Orchestrator-Workers]]"
  - "[[Multi-Agent Systems]]"
  - "[[Agent Tool Categories]]"
sources:
  - "[[2025 - OpenAI - A Practical Guide to Building Agents]]"
---

# Manager Pattern

One of two multi-agent orchestration patterns in OpenAI's [[2025 - OpenAI - A Practical Guide to Building Agents]]. Also called **"agents as tools."**

A central **manager** agent coordinates a network of specialized agents by calling them **as tools**. The manager delegates each subtask to the right specialist at the right time and **synthesizes** their results into one cohesive interaction. The user talks only to the manager.

## When to use

Ideal "where you only want one agent to control workflow execution and have access to the user." The manager keeps context and control; specialists are on-demand capabilities. Modeled as a graph where **edges = tool calls**.

## Relation to existing pages

- This is OpenAI's vocabulary for what Anthropic calls **[[Orchestrator-Workers]]** — a central LLM dispatches to workers and merges outputs. Difference in framing: the Manager pattern emphasizes specialists registered as *tools* (synchronous calls returning to the manager), versus Anthropic's dynamic worker spawning.
- Contrast with **[[Agent Handoffs]]** (decentralized): there control *transfers away*; here control *stays* with the manager.
- A specific shape of [[Multi-Agent Systems]]; the orchestration-type tool in [[Agent Tool Categories]] is exactly "another agent exposed to the manager."

## Tradeoff

Centralized control gives clean synthesis and a single user-facing voice, at the cost of the manager becoming a context/throughput bottleneck — the same tension [[Multi-Agent Systems]] notes between coordinator-as-bottleneck and artifact-sharing.

## Source

- [[2025 - OpenAI - A Practical Guide to Building Agents]] — vendor: [[OpenAI]]; framework: [[OpenAI Agents SDK]]
