---
type: source
title: "Effective Harnesses for Long-Running Agents"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - harness
  - infrastructure
  - long-horizon
status: developing
source_type: article
author: "Anthropic Engineering"
date_published: 2026-05-13
url: "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents"
confidence: high
related:
  - "[[Meta-Harness]]"
  - "[[Session as Event Log]]"
  - "[[Long-Horizon Context Management]]"
  - "[[Error Trace Retention]]"
  - "[[Managed Agents]]"
  - "[[KV-Cache Discipline]]"
  - "[[Token Economics]]"
sources:
  - "[[.raw/articles/2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents.md]]"
key_claims:
  - "The harness — not the model — is responsible for correctness, durability, and recoverability in long-running agents."
  - "Any session that cannot be re-provisioned from its event log is a design smell."
  - "Silent truncation is the most common harness failure mode in production agents."
  - "Build harnesses against the meta-harness interface contract even without Managed Agents."
  - "Side-effect accounting: a manifest of non-idempotent tool calls, consulted before any replay attempt."
---

# Effective Harnesses for Long-Running Agents

Anthropic Engineering, 2026-05-13 — [source]( https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

## One-line summary

Harness engineering is the load-bearing discipline for long-running agents; the model's capability is bounded by the harness's durability, recoverability, and context-management discipline.

## Core argument

Long-running agents fail not because models lack capability, but because harnesses lack:

- **Durability** — state that survives failures
- **Recoverability** — the ability to resume from any failure point
- **Context discipline** — what the model sees at each step is the harness's decision, not the model's

The post frames harness design as a first-class engineering discipline, comparable to database design or API design. It draws on Anthropic's production experience with their internal multi-agent research system and [[Managed Agents]].

## Four harness responsibilities

| Responsibility | What it means |
|---|---|
| Context management | Decide what the model sees per step; manage compaction, JIT retrieval |
| Checkpoint / recovery | Persist enough state to resume; treat runs as idempotent where possible |
| Error containment | Classify errors as recoverable vs. fatal; surface structured errors to model |
| Lifecycle management | Provision, terminate, re-provision sessions; enforce "cattle not pets" |

## Key anti-patterns named

- **God harness** — monolithic harness mixing all concerns; untestable, brittle
- **Chatty checkpointing** — writing to durable storage on every token/tool call; write amplification
- **Silent truncation** — dropping context when window is full without logging or notifying model; most common production failure mode
- **Model-owned durability** — relying on the model to request saves; fails when model loses context

## Harness design patterns

### Event-log-first design

Ground truth = append-only event log (see [[Session as Event Log]]). All other state derived. Three recovery variants:

1. Full replay — correct, expensive for long runs
2. Snapshot + incremental replay — periodic snapshots, replay only delta
3. Log with compacted views — log is complete; compacted view is a derived artifact, not ground truth

### Layered architecture

Three distinct layers (extends [[Meta-Harness]] Brain/Hands/Session decomposition):

- **Execution layer** — stateless; runs tools, manages sandboxes, retries
- **Context layer** — stateful; owns event log, compaction policy, JIT retrieval
- **Orchestration layer** — cross-session; provisions/terminates sessions, routes between agents

### Structured error surfaces

Recoverable errors → structured JSON object the model can reason about (error type, tool, reason, alternatives). Raw tracebacks → event log only, not surfaced to model. Related to [[Error Trace Retention]] but with a sharper distinction between model-facing and log-facing error representations.

### Side-effect accounting

Harness maintains a manifest of non-idempotent tool calls. Consulted before any replay attempt. Harness — not model — is responsible for this accounting.

## Testing harnesses

- **Fault injection** — deliberately fail tool calls, exhaust context, kill sandboxes mid-run
- **Event log diffing** — diff model inputs produced by two harness implementations on the same log
- **Replay testing** — synthetic event logs for known-hard states (near-full context, mid-task failures)

## Relationship to existing wiki concepts

- **[[Meta-Harness]]** — this post provides the practical implementation layer beneath the architectural abstraction. Adds "orchestration" as a fourth layer above Brain/Hands/Session.
- **[[Session as Event Log]]** — post gives three concrete recovery variants (full replay, snapshot+incremental, compacted views) not in the existing page.
- **[[Long-Horizon Context Management]]** — harness-owned compaction and JIT retrieval are the runtime mechanism for the three techniques described there.
- **[[Error Trace Retention]]** — post introduces a model-facing / log-facing distinction that sharpens the existing concept.
- **[[Managed Agents]]** — post frames Managed Agents as one hosted instance of the meta-harness contract; explicitly recommends building custom harnesses against the same interface contract.

## Connections

- Substantiates: [[Meta-Harness]], [[Session as Event Log]]
- Extends: [[Error Trace Retention]] (model-facing vs log-facing split)
- Implements: [[Long-Horizon Context Management]] (compaction, JIT retrieval as harness-owned)
- Reinforces: [[Managed Agents]] (recommend building to its interface contract)
- Applies: [[Token Economics]] (chatty checkpointing is a write-amplification cost pattern)
