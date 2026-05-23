---
type: concept
title: "Agent Handoffs"
created: 2026-05-22
updated: 2026-05-22
status: seed
tags:
  - ai-agents
  - agent-pattern
  - orchestration
related:
  - "[[Manager Pattern]]"
  - "[[Routing]]"
  - "[[Multi-Agent Systems]]"
  - "[[OpenAI Agents SDK]]"
sources:
  - "[[2025 - OpenAI - A Practical Guide to Building Agents]]"
---

# Agent Handoffs

The **decentralized** multi-agent pattern in OpenAI's [[2025 - OpenAI - A Practical Guide to Building Agents]]. Agents operate as **peers**; one can **hand off** workflow execution to another based on specialization.

A **handoff is a one-way transfer**. In the [[OpenAI Agents SDK]] a handoff is implemented as a *type of tool/function* — when an agent calls it, execution immediately starts on the target agent and the **latest conversation state transfers** with it. Modeled as a graph where **edges = handoffs** (vs the [[Manager Pattern]]'s edges = tool calls).

## When to use

Optimal "when you don't need a single agent maintaining central control or synthesis" — let each agent take over and interact with the user directly. Canonical case: **conversation triage** — a `triage_agent` with `handoffs=[technical_support, sales, order_management]` routes the user to a specialist that then owns the conversation. Optionally the target can hand back to the original agent.

## Relation to existing pages

- OpenAI's handoff ≈ Anthropic's **[[Routing]]** taken further: routing classifies-then-dispatches once; handoffs allow a *chain* of peer-to-peer transfers, each fully taking over.
- Opposite control topology to the **[[Manager Pattern]]**: handoffs *give up* control; the manager *retains* it. The guide presents these as the two broadly-applicable [[Multi-Agent Systems]] categories.

## Declarative vs code-first

The guide frames handoff orchestration against **declarative graph** frameworks (every branch/loop/conditional defined upfront, often via a DSL). The SDK's **code-first** stance expresses handoffs as ordinary function calls, enabling dynamic graphs without pre-declaration — see [[OpenAI Agents SDK]].

## Source

- [[2025 - OpenAI - A Practical Guide to Building Agents]] — vendor: [[OpenAI]]
