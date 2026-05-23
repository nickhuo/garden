---
type: concept
title: "Agent-Native Infrastructure"
created: 2026-05-22
updated: 2026-05-22
status: seed
tags:
  - ai-agents
  - architecture
  - foundational
related:
  - "[[ACI - Agent-Computer Interface]]"
  - "[[Agent Interface Contracts]]"
  - "[[MCP]]"
  - "[[Agentic Engineering]]"
  - "[[Permission Model]]"
sources:
  - "[[2026-05-22 - Karpathy - Sequoia Ascent 2026]]"
---

# Agent-Native Infrastructure

Design principle: **build for the agent, not just the human**. Most software still assumes a person clicking through screens — "go to this URL, click this button." But increasingly the *user is the human's agent*, not the human directly. Software that wants to be used by agents must expose agent-native surfaces.

## Surfaces to provide

- Markdown docs and copy-pasteable instructions
- CLIs and APIs
- [[MCP]] servers
- structured logs and machine-readable schemas
- safe **permissioning** ([[Permission Model]]) and **auditable** actions
- **headless** flows

## Sensors and actuators

Karpathy's frame: think of a product as **sensors** (turn world state into digital information the agent can read) and **actuators** (let the agent change things in the world). Designing both, with safety and auditability, is what makes a system agent-operable.

## The deployment gap

MenuGen is the standing benchmark: *building* the app with agents was easy; *wiring it up* — Vercel, auth, payments, DNS, secrets, production settings — was the hard, human part. A mature agent-native world automates exactly this glue. The gap between "agent can write code" and "agent can ship and operate a system" is where agent-native infrastructure pays off.

## Relation to existing pages

This is the product/infra-side complement to [[Agentic Engineering]] (the human discipline). It generalizes [[ACI - Agent-Computer Interface]] and [[Agent Interface Contracts]] from "design good tools for the agent" up to "design the whole product for the agent," and treats [[MCP]] as one standardized actuator/sensor channel.

## Source

- [[2026-05-22 - Karpathy - Sequoia Ascent 2026]] — entity: [[Andrej Karpathy]]
