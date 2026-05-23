---
type: concept
title: "Agent Tool Categories"
created: 2026-05-22
updated: 2026-05-22
status: seed
tags:
  - ai-agents
  - tool-use
  - taxonomy
related:
  - "[[ACI - Agent-Computer Interface]]"
  - "[[Agent Interface Contracts]]"
  - "[[Manager Pattern]]"
  - "[[Permission Model]]"
sources:
  - "[[2025 - OpenAI - A Practical Guide to Building Agents]]"
---

# Agent Tool Categories

OpenAI's [[2025 - OpenAI - A Practical Guide to Building Agents]] sorts the tools an agent needs into **three types**:

| Type | Purpose | Examples |
|---|---|---|
| **Data** | Retrieve context/information to execute the workflow | Query a transaction DB or CRM, read a PDF, search the web |
| **Action** | Interact with systems to *change* things | Send email/text, update a CRM record, hand a ticket to a human |
| **Orchestration** | Other agents exposed as tools | Refund agent, research agent, writing agent (the [[Manager Pattern]]) |

## Why the taxonomy matters

- **Read vs write is a safety axis.** Data tools are read-only; Action tools mutate state. This split feeds the **tool safeguards** risk-rating in [[Agent Guardrails]] (low/med/high by reversibility and financial impact) and connects to [[Permission Model]] / [[Minimal Footprint Principle]].
- **Orchestration tools blur the agent/tool line** — an agent-as-tool is the building block of the [[Manager Pattern]].
- The guide stresses **standardized tool definitions** enabling many-to-many tool↔agent relationships, and that well-documented/tested/reusable tools improve discoverability — the same discipline as [[ACI - Agent-Computer Interface]] and [[Agent Interface Contracts]].

## Legacy systems

Where no API exists, **computer-use models** let the agent operate web/application UIs directly, "just as a human would" — a fourth, implicit access path beneath these categories.

## Source

- [[2025 - OpenAI - A Practical Guide to Building Agents]] — vendor: [[OpenAI]]
