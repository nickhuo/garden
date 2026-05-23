---
type: concept
title: "Agent Run Loop"
created: 2026-05-22
updated: 2026-05-22
status: seed
tags:
  - ai-agents
  - orchestration
  - foundational
related:
  - "[[Autonomous Agents]]"
  - "[[Agentic Harness]]"
  - "[[OpenAI Agents SDK]]"
  - "[[ReAct]]"
sources:
  - "[[2025 - OpenAI - A Practical Guide to Building Agents]]"
---

# Agent Run Loop

The central control structure of any agent. OpenAI's [[2025 - OpenAI - A Practical Guide to Building Agents]]: "every orchestration approach needs the concept of a **'run'**" — typically a loop that lets the agent operate until an **exit condition**. "This concept of a while loop is central to the functioning of an agent."

## Common exit conditions

- a **tool call** of a designated kind,
- a certain **structured output** (a "final-output tool" defined by an output type),
- an **error**, or
- reaching a **maximum number of turns**.

In the [[OpenAI Agents SDK]], `Runner.run()` loops over the LLM until either (1) a **final-output tool** is invoked, or (2) the model returns a response with **no tool calls** (e.g. a direct user message).

## Relation to existing pages

- This is the operational core of an **[[Autonomous Agents|autonomous agent]]** and what an **[[Agentic Harness]]** wraps — the harness supplies the loop, the exit conditions, turn limits, and tool plumbing.
- The think→act→observe cycle of **[[ReAct]]** is one body for this loop; the loop generalizes it (any tool-call / structured-output exit, not just reason-act traces).
- Max-turns and error exits are the minimal **safety floor** that [[Human-in-the-Loop Intervention]] builds on (failure-threshold escalation).

## Source

- [[2025 - OpenAI - A Practical Guide to Building Agents]] — vendor: [[OpenAI]]
