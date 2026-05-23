---
type: concept
title: "Agent Guardrails"
created: 2026-05-22
updated: 2026-05-22
status: seed
tags:
  - ai-agents
  - safety
  - foundational
related:
  - "[[Human-in-the-Loop Intervention]]"
  - "[[Permission Model]]"
  - "[[Prompt Injection]]"
  - "[[Minimal Footprint Principle]]"
  - "[[Permission Classifier]]"
sources:
  - "[[2025 - OpenAI - A Practical Guide to Building Agents]]"
---

# Agent Guardrails

A **layered defense mechanism** for LLM agents (OpenAI, [[2025 - OpenAI - A Practical Guide to Building Agents]]). No single guardrail suffices; multiple specialized ones combine — LLM-based checks, rules-based filters, and the moderation API — vetting inputs and outputs. Guardrails complement, not replace, authn/authz, access controls, and standard software security.

## Typology

| Guardrail | What it does |
|---|---|
| **Relevance classifier** | Flags off-topic queries (keeps responses in scope) |
| **Safety classifier** | Detects jailbreaks / [[Prompt Injection|prompt injections]] |
| **PII filter** | Vets output for personally identifiable information |
| **Moderation** | Flags harmful/inappropriate inputs (hate, harassment, violence) |
| **Tool safeguards** | Rate each tool **low/med/high** by read-vs-write, reversibility, permissions, financial impact → trigger pauses/escalation |
| **Rules-based protections** | Blocklists, input-length limits, regex (e.g. SQL-injection prevention) |
| **Output validation** | Brand-alignment checks via prompt engineering + content checks |

## Optimistic execution (Agents SDK)

The [[OpenAI Agents SDK]] treats guardrails as **first-class** and runs them **optimistically**: the primary agent generates output while guardrails run **concurrently**, raising a **tripwire** exception if a constraint is breached. Guardrails can be functions or whole agents (e.g. a churn-detection agent as an input guardrail).

## Building heuristic

1. Focus first on **data privacy and content safety**.
2. Add guardrails from **real-world edge cases and failures** you encounter.
3. Optimize for **both security and user experience**.

## Relation to existing pages

- **Tool safeguards** = a risk-rated read of [[Agent Tool Categories]] (Data=read, Action=write); it's OpenAI's version of [[Permission Model]] / [[Permission Classifier]] (route by semantic risk) and [[Minimal Footprint Principle]] (prefer reversible actions).
- The **safety classifier** is the input-side counterpart to [[Prompt Injection]] defenses.
- Where guardrails can't decide, escalate via [[Human-in-the-Loop Intervention]].

## Source

- [[2025 - OpenAI - A Practical Guide to Building Agents]] — vendor: [[OpenAI]]
