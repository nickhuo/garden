---
type: source
title: "A Practical Guide to Building Agents"
source_type: guide
author: "OpenAI"
date_published: 2025
url: "https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/"
created: 2026-05-22
updated: 2026-05-22
status: developing
confidence: high
key_claims:
  - "An agent is a system that uses an LLM to manage workflow execution and decisions, with tools and guardrails — apps that integrate LLMs but don't control workflow execution (chatbots, single-turn, classifiers) are not agents."
  - "Build an agent when workflows resist deterministic automation: complex decision-making, difficult-to-maintain rules, or heavy reliance on unstructured data."
  - "An agent = model + tools + instructions. Tools come in three types: Data, Action, and Orchestration (agents-as-tools)."
  - "Prototype with the most capable model to set a baseline, then swap in smaller models where they still pass evals; optimize cost/latency last."
  - "Maximize a single agent first; go multi-agent only when complex logic or tool overload (overlap, not count) degrades performance."
  - "Two multi-agent patterns: Manager (agents as tools, central control + synthesis) and Decentralized (peers handing off via one-way transfers)."
  - "Guardrails are a layered defense (relevance, safety, PII, moderation, tool safeguards, rules-based, output validation) run optimistically as tripwires, plus human-in-the-loop for failure thresholds and high-risk actions."
tags:
  - ai-agents
  - foundational
  - orchestration
related:
  - "[[Manager Pattern]]"
  - "[[Agent Handoffs]]"
  - "[[Agent Guardrails]]"
  - "[[Agent Tool Categories]]"
  - "[[Agent Run Loop]]"
  - "[[Human-in-the-Loop Intervention]]"
  - "[[OpenAI Agents SDK]]"
  - "[[OpenAI]]"
  - "[[OpenAI Practical Guide vs Anthropic Building Effective Agents]]"
sources: []
---

# A Practical Guide to Building Agents

OpenAI, 2025 (34-page PDF for product/engineering teams building their first agents). The natural counterpart to Anthropic's [[2024-12-19 - Anthropic - Building Effective Agents]] — same goal (practical agent-building guidance), more product-team framing and SDK-centric. Comparison page: [[OpenAI Practical Guide vs Anthropic Building Effective Agents]].

## Definition and when to build

An **agent** "independently accomplishes tasks on your behalf," using an LLM to control **workflow** execution. Two core characteristics: (1) the LLM manages execution, knows when a workflow is done, self-corrects, and can halt and return control; (2) it dynamically selects tools within guardrails. Apps that embed an LLM but don't let it control the workflow (chatbots, single-turn, classifiers) are explicitly *not* agents.

Build one when deterministic/rule-based methods fall short: **complex decision-making**, **difficult-to-maintain rules**, or **heavy reliance on unstructured data**. Otherwise a deterministic solution may suffice.

## Three foundations: model + tools + instructions

- **Model** — match capability to task. Prototype with the most capable model to set a baseline, then swap down where evals still pass. Principles: set up evals → hit accuracy target → optimize cost/latency. (See [[Token Economics]].)
- **Tools** — standardized definitions enabling many-to-many tool↔agent relationships; three categories in [[Agent Tool Categories]] (Data / Action / Orchestration). Legacy systems without APIs → computer-use models drive the UI.
- **Instructions** — derive routines from existing SOPs/policy docs, break tasks into clear steps, define explicit actions, capture edge cases with conditional branches; advanced models can auto-generate instructions from help-center docs.

## Orchestration

Incremental beats big-bang. **Single-agent** systems run a [[Agent Run Loop]] (loop until an exit condition: final-output tool, no tool calls, error, or max turns); manage complexity with **prompt templates** (one base prompt + policy variables) before adding agents. Go **multi-agent** only on **complex logic** (many conditional branches) or **tool overload** (similarity/overlap, not raw count — ">15 distinct tools" can work, "<10 overlapping" can fail).

Two multi-agent patterns:
- **[[Manager Pattern]]** (agents as tools) — central manager coordinates specialists via tool calls and synthesizes; one agent keeps control and user access. Anthropic analogue: [[Orchestrator-Workers]].
- **[[Agent Handoffs]]** (decentralized) — peers transfer control one-way; in the SDK a handoff is a tool. Anthropic analogue: [[Routing]] + dynamic delegation.

The guide also contrasts **declarative graph** frameworks (define every node/edge upfront, can need a DSL) with the SDK's **code-first** approach — see [[Agent Handoffs]] and [[OpenAI Agents SDK]].

## Guardrails

A **layered defense** (no single guardrail suffices), combining LLM-based, rules-based, and the moderation API. Typology in [[Agent Guardrails]]: relevance classifier, safety classifier, PII filter, moderation, **tool safeguards** (low/med/high risk ratings → automated pauses/escalation), rules-based protections, output validation. The SDK runs them **optimistically** as concurrent tripwires. Plus [[Human-in-the-Loop Intervention]] on failure thresholds and high-risk actions.

## Why it matters here

This is the **OpenAI-side canon** to set against Anthropic's [[Workflows vs Agents]] taxonomy. Where Anthropic frames the central choice as workflows-vs-agents and warns "use the simplest thing that works," OpenAI frames it as single-vs-multi-agent and "maximize a single agent first" — convergent advice, different vocabulary. The **tool safeguards** risk-rating idea connects to [[Permission Model]] / [[Minimal Footprint Principle]]; **agents-as-tools** connects to [[Orchestrator-Workers]] and [[Multi-Agent Systems]].
