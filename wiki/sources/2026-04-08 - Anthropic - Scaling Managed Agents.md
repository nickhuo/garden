---
type: source
title: "Scaling Managed Agents: Decoupling the brain from the hands"
aliases:
  - Scaling Managed Agents
created: 2026-05-04
updated: 2026-05-13
tags:
  - ai-agents
  - anthropic
  - infrastructure
  - scaling
  - harness
status: mature
related: []
sources:
  - "[[.raw/articles/2026-04-08 - Anthropic - Scaling Managed Agents.md]]"
source_type: blog
author: Anthropic Engineering
date_published: 2026-04-08
url: https://www.anthropic.com/engineering/managed-agents
confidence: medium
key_claims: []
---

# Scaling Managed Agents: Decoupling the brain from the hands (Anthropic, 2026-04-08)

## Summary

Anthropic's engineering writeup of **Managed Agents** — both a hosted Claude Platform service AND an architectural pattern they coin "**meta-harness**." The post extends the wiki's existing taxonomy by adding a layer ABOVE Workflows / Agents / Multi-agent: a system that hosts *any* harness through stable interfaces around three virtualized components — **Brain, Hands, Session**. Operating insight: **p50 TTFT down ~60%, p95 down >90%** through lazy container provisioning.

## The architectural move

Where [[Building Effective Agents]] gave us the Workflows / Agents distinction, this post sits one level above. **Managed Agents virtualizes** the agent runtime so harness implementations underneath can change without breaking interfaces.

> "Managed Agents is a meta-harness in the same spirit, unopinionated about the specific harness that Claude will need in the future."

OS analogy is load-bearing: just as `process` and `file` outlasted the hardware they virtualized, Managed Agents virtualizes agent components so implementations underneath can change freely.

## Three virtualized components

- **Brain** — Claude + harness. Stateless, replaceable. Calls sandbox via `execute(name, input) → string`.
- **Hands** — sandbox (container, phone, Pokémon emulator — irrelevant). Uniform interface.
- **Session** — append-only event log, **outside Claude's context window**. Brain interrogates via `getEvents()` (positional slices, rewinds, rereads).

> "The harness doesn't know whether the sandbox is a container, a phone, or a Pokémon emulator."

> "In Managed Agents, the session provides this same benefit, serving as a context object that lives outside Claude's context window."

## "Pets vs cattle" applied to harnesses

V1 packed everything in one container (a pet you nurse back to health). V2 makes container, harness, and even brain stateless and reprovisionable. Borrowed from cloudscaling.

## Many brains, many hands

Scaling pattern: brains can pass hands to one another. Multi-agent orchestration becomes infrastructure-supported instead of bespoke coupling. See [[Multi-Agent Systems]] for the agent-pattern angle; this post is the infra-side counterpart.

## Concrete primitives

`wake(sessionId)` · `getSession(id)` · `emitEvent(id, event)` · `provision({resources})` · `execute(name, input) → string` · `getEvents()`

## Operating result

> "Using this architecture, our p50 TTFT dropped roughly 60% and p95 dropped over 90%."

Latency wins come from **lazy container provisioning** — don't allocate resources until brain actually needs hands.

## Security posture

Auth bundled with resource OR vault outside sandbox. **MCP proxy** with session-scoped tokens; harness never sees credentials directly.

## Connection to wiki concepts

- **[[Workflows vs Agents]]** — meta-harness sits ABOVE the binary. Doesn't replace.
- **[[Multi-Agent Systems]]** — "many brains, many hands" is infra-supported orchestration, complementing the agent-pattern view.
- **[[Orchestrator-Workers]]** — the harness-as-orchestrator becomes stateless cattle.
- **[[ACI - Agent-Computer Interface]]** — extends ACI from tool design to *system-layer* infrastructure design. Brain↔Session and Brain↔Sandbox interfaces are ACI at the system layer.
- **[[Augmented LLM]]** — session-as-external-context is the most concrete instantiation yet of the memory leg.
- **[[Long-Horizon Context Management]]** — session log is the durable substrate UNDERNEATH compaction / note-taking / sub-agents. Not a fourth technique; the foundation.
- **[[Just-in-Time Context Retrieval]]** — `getEvents()` is JIT over an event log. Concrete implementation.

## Pressure on running thesis

[[Workflows Beat Agents for Most Production]] — mild pressure, mostly orthogonal. The thesis cites infra unreliability as one reason workflows win; this post **closes a chunk of those infra-side objections** (statelessness, recovery, multi-tenant security, lazy provisioning). Cognitive-side objections (drift, eval cost, debuggability) remain. **Net:** thesis still holds, but the production-readiness gap for agents narrows.

## Verbatim claims worth quoting

- "Harnesses encode assumptions about what Claude can't do on its own. However, those assumptions need to be frequently questioned because they can go stale as models improve." (Bitter Lesson applied to harness design)
- "Managed Agents is a meta-harness in the same spirit, unopinionated about the specific harness that Claude will need in the future."
- "The harness doesn't know whether the sandbox is a container, a phone, or a Pokémon emulator."
- "Using this architecture, our p50 TTFT dropped roughly 60% and p95 dropped over 90%."

## Patterns and concepts introduced

- [[Managed Agents]] — Anthropic's hosted product (entity)
- [[Meta-Harness]] — cross-vendor architectural pattern (concept)
- [[Session as Event Log]] — durable context substrate (concept)

## Entities mentioned (no new pages, per ≥2-mention rule)

- Claude Code (referenced as "a harness")
- Anthropic Agents API team / Jake Eaton / Nodir Turakulov / Jeremy Fox (acknowledged; not subjects)

## Source location

- Raw: `raw/2026-04-08 - Anthropic - Scaling Managed Agents.md`
