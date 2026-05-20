---
type: concept
title: Harness Design Patterns
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - infrastructure
  - harness
  - architecture
status: developing
complexity: intermediate
domain: ai-agents
aliases:
  - Agent Harness Patterns
  - Harness Anti-Patterns
related:
  - "[[Meta-Harness]]"
  - "[[Session as Event Log]]"
  - "[[Long-Horizon Context Management]]"
  - "[[Error Trace Retention]]"
  - "[[KV-Cache Discipline]]"
  - "[[Token Economics]]"
sources:
  - "[[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]]"
---

# Harness Design Patterns

## Summary

Per [[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]] (Anthropic 2026-05): a harness is the engineering layer that wraps an LLM agent and is responsible for correctness, durability, and recoverability — capabilities the model itself cannot provide. Harness design is a first-class engineering discipline, comparable to database or API design.

> "The harness — not the model — is responsible for correctness, durability, and recoverability in long-running agents."

## The four harness responsibilities

| Responsibility | Definition |
|---|---|
| Context management | Decide what the model sees at each step; own compaction, JIT retrieval, annotation |
| Checkpoint / recovery | Persist sufficient state to resume after failure; treat runs as idempotent where possible |
| Error containment | Classify errors as recoverable vs. fatal; surface structured errors to model, raw traces to log |
| Lifecycle management | Provision, terminate, re-provision sessions; enforce "cattle not pets" — see [[Meta-Harness]] |

## Anti-patterns

Named in production at Anthropic:

- **God harness** — monolithic harness mixing all concerns (context, errors, credentials, dispatch) in one undifferentiated layer. Untestable, brittle to change.
- **Chatty checkpointing** — writing to durable storage on every token or tool call. Write amplification that dominates real workload cost. See [[Token Economics]].
- **Silent truncation** — dropping context when the window is full without logging the event or notifying the model. The most common production failure mode for long-running agents. The model continues unaware of the gap; failures compound silently.
- **Model-owned durability** — harness delegates state-management responsibility into the model's context (e.g., "ask the model to request a save"). Works for short sessions; falls apart when the model loses track of what it was supposed to save.

## Layered architecture

The recommended pattern splits harness concerns across three distinct layers:

```
┌─────────────────────────────────┐
│       Orchestration Layer       │  ← cross-session: provision, route, terminate
├─────────────────────────────────┤
│         Context Layer           │  ← stateful: event log, compaction, JIT retrieval
├─────────────────────────────────┤
│         Execution Layer         │  ← stateless: run tools, manage sandboxes, retry
└─────────────────────────────────┘
```

This extends the Brain/Hands/Session decomposition of [[Meta-Harness]] by making orchestration an explicit, distinct layer above session management.

Each layer has a clear interface contract; implementations can change beneath it. The orchestration layer is the meta-harness analogue of a container orchestrator (Kubernetes) above individual container runtimes.

## Structured error surfaces

When a tool call fails, the harness:

1. Always logs the failure event in the event log (raw trace, verbatim)
2. Classifies: recoverable (model can route around) or fatal (halt, alert orchestration layer)
3. Surfaces to model: a structured object for recoverable errors; nothing for fatal (halt instead)

Example structured error (from source):

```json
{
  "error_type": "tool_unavailable",
  "tool": "browser.navigate",
  "reason": "sandbox connection timeout after 30s",
  "recoverable": true,
  "suggested_alternatives": ["retry", "use_cached_result", "skip_and_note"]
}
```

Raw tracebacks go to the event log; structured objects go to the model. See [[Error Trace Retention]] for the tension with Manus's "verbatim retention" rule.

## Side-effect accounting

The harness maintains a **manifest of non-idempotent tool calls** — tool calls with external side effects that cannot be safely replayed. Before any replay or recovery attempt, the harness consults this manifest. Steps with non-idempotent side effects require human review before replay.

This is the harness's answer to replay safety: idempotent calls are safe to replay automatically; non-idempotent calls are flagged for human confirmation.

## Harness testing practices

- **Fault injection** — deliberately fail tool calls, exhaust context windows, kill sandboxes mid-run. Test recovery paths explicitly, not just happy paths.
- **Event log diffing** — run two harness implementations on the same event log and diff the model inputs produced. Catches divergence in compaction logic or context-surface decisions.
- **Replay testing** — construct synthetic event logs representing known-hard states (near-full context, mid-task failures) and verify recovery behavior.

## Relationship to meta-harness contract

Anthropic recommends building custom harnesses against the meta-harness interface contract (Brain / Hands / Session) even without using Managed Agents. This keeps migration to hosted durability mechanical rather than architectural.

> "Build harnesses against the meta-harness interface contract even if you're not using Managed Agents."

## Connections

- Architecture: [[Meta-Harness]] (harness design patterns are the implementation layer beneath the meta-harness abstraction)
- Substrate: [[Session as Event Log]] (event-log-first design is the recommended foundation)
- Applies to: [[Long-Horizon Context Management]] (compaction, JIT retrieval as harness-owned responsibilities)
- Sharpens: [[Error Trace Retention]] (model-facing vs log-facing error representation)
- Cost concern: [[Token Economics]], [[KV-Cache Discipline]] (chatty checkpointing; silent truncation)

## Open questions

- At what session length does snapshot + incremental replay become cheaper than full replay? Any published numbers?
- Side-effect manifest format — should non-idempotent calls be tagged at the tool-definition level (schema), or at the call-site level (runtime classification)?
- Does the god-harness anti-pattern correlate with a particular team/org structure? Conway's Law implication: teams with one person responsible for "the agent" build god harnesses.
