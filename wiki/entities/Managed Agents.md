---
type: entity
title: Managed Agents
created: 2026-05-04
updated: 2026-05-04
tags:
- ai-agents
- anthropic
- product
- infrastructure
status: seed
related: []
sources:
- "[[2026-04-08 - Anthropic - Scaling Managed Agents]]"
- "[[2026-04 - Anthropic - Claude Code Auto Mode]]"
aliases:
- Anthropic Managed Agents
_legacy_source_count: 1
---

# Managed Agents (Anthropic product)

## Summary

Anthropic's hosted Claude Platform service for running production agents. Architecturally an instance of the [[Meta-Harness]] pattern. Launched as the Anthropic-side answer to the operational pain of self-hosting long-running agents (state recovery, sandboxing, multi-tenant security, lazy resource provisioning).

## What it provides

- **Hosted runtime** for Brain (Claude + harness), Hands (sandbox), and Session (event log) as decoupled components — see [[Meta-Harness]]
- **Durable sessions** via append-only event log accessible through `getEvents()` API
- **Stateless harness model** ("pets vs cattle"): containers and harnesses are reprovisionable, not nursed
- **MCP proxy** with session-scoped tokens — harness never handles credentials directly
- **Lazy container provisioning** — yielded p50 TTFT ↓~60%, p95 ↓>90% in Anthropic's measurements

## API surface (per [[Scaling Managed Agents]])

`wake(sessionId)` · `getSession(id)` · `emitEvent(id, event)` · `provision({resources})` · `execute(name, input) → string` · `getEvents()`

Docs: `platform.claude.com/docs/en/managed-agents/overview` (per source)

## What runs on it

- **Claude Code** as a hosted harness
- Task-specific agent harnesses (custom, BYO)
- Future harness implementations as model capabilities evolve

## Why it matters strategically

If Managed Agents wins, it does to agent runtimes what AWS Lambda did to function execution: makes the operational layer commodity, lets builders focus on harness logic. Open question whether Google / OpenAI ship analogues fast enough for [[Meta-Harness]] to remain a multi-vendor concept rather than collapsing into Anthropic's product.

## Connections

- Architectural pattern: [[Meta-Harness]]
- Durability primitive: [[Session as Event Log]]
- Tool layer: [[MCP]] (with session-scoped proxy)
- Production readiness for: [[Autonomous Agents]] · [[Multi-Agent Systems]]

## Open questions

- Pricing model — hosted-runtime cost vs self-hosted; not detailed in source.
- Cold-start latency under burst — TTFT figures are p50/p95 but workload mix unstated.
- BYO model support — does Managed Agents host non-Anthropic models, or Claude-only?
- Multi-vendor adoption — will the API conventions (`wake/execute/getEvents`) become a de facto standard?

## Permission model for hosted deployments (per Anthropic 2026-04)

[[2026-04 - Anthropic - Claude Code Auto Mode]] confirms that [[Claude Code]] running on Managed Agents uses [[Permission Classifier]]-based auto mode as the intended permission policy for unattended execution. The combination is:

- Managed Agents provides the harness runtime (Brain/Hands/Session)
- Auto mode's Permission Classifier handles tool-call risk routing
- OS sandbox handles network/filesystem isolation at the infrastructure layer
- Audit log provides post-hoc reviewability

This resolves the "what permission model does headless Managed Agents use?" question from the Scaling Managed Agents source.

## Sources

- [[Scaling Managed Agents]] (Anthropic, 2026-04-08)
- [[2026-04 - Anthropic - Claude Code Auto Mode]] (Anthropic, April 2026)
