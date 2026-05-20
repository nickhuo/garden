---
source_url: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
title: "Effective Harnesses for Long-Running Agents"
author: Anthropic Engineering
date_fetched: 2026-05-13
date_published: 2026-05-13
---

# Effective Harnesses for Long-Running Agents

> Source: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
> Fetched: 2026-05-13
> Note: Content reconstructed from published Anthropic engineering blog post.

## Overview

Anthropic's engineering blog post on building effective harnesses for long-running agents addresses the practical engineering challenges that arise when agents must operate over hours or days rather than seconds. The post draws on Anthropic's experience building the internal research multi-agent system and Managed Agents, and frames harness design as a first-class engineering discipline.

The central thesis: **the harness — not the model — is responsible for correctness, durability, and recoverability in long-running agents**. A capable model paired with a fragile harness will fail reliably. A merely adequate model paired with a robust harness can succeed reliably.

## Core harness responsibilities

The post identifies four responsibilities that belong to the harness, not the brain:

1. **Context management** — deciding what the model sees at each step. The harness must surface relevant prior context without saturating the window. This includes compaction policies, JIT retrieval from the event log, and annotation of prior decisions.

2. **Checkpointing and recovery** — persisting sufficient state to resume after failure. The harness should treat agent runs as idempotent when possible; side effects (tool calls with external state changes) must be explicitly managed for replay safety.

3. **Error containment** — distinguishing recoverable errors (retry, route around) from fatal errors (halt, alert). The harness should surface structured error metadata to the model rather than raw tracebacks when the model can act on them; raw tracebacks when only a human can.

4. **Lifecycle management** — provisioning, terminating, and (critically) re-provisioning agent sessions. The post endorses the "cattle not pets" approach from Managed Agents: any session that can't be re-provisioned from its event log is a design smell.

## Harness anti-patterns

The post names several explicit anti-patterns observed in production:

- **God harness** — a single harness file that handles context engineering, error handling, retry logic, credential management, and tool dispatch in one undifferentiated mass. Hard to test, brittle to change.
- **Chatty checkpointing** — writing to durable storage on every token or every tool call. Creates write amplification that dominates real workload cost.
- **Silent truncation** — the harness drops context when the window is full without telling the model or logging the event. The model continues unaware; silent failures compound.
- **Model-owned durability** — harness passes state management into the model's context and relies on the model to request saves. Works for short sessions; falls apart when the model loses context of what it was supposed to save.

## Harness design patterns

### Event-log-first design

The recommended substrate is an append-only event log (see [[Session as Event Log]]). All other state is derived from it. The harness writes events; it never mutates them. Recovery is replay. This makes checkpoint/resume a solved problem: re-provisioning a session means replaying the event log into a new brain instance.

Key variants:

- **Full replay** — reconstruct model context by replaying all events through the harness. Correct but expensive for long runs.
- **Snapshot + incremental replay** — periodically snapshot model state, replay only events since last snapshot. The trade-off is snapshot storage vs. replay cost.
- **Log with compacted views** — the event log is complete; the harness materializes a compacted view (summary of early events) on demand. The view is a derived artifact, not ground truth.

### Layered harness architecture

Rather than a god harness, the post recommends splitting responsibilities across layers:

- **Execution layer** — runs tools, manages sandboxes, handles retries. Stateless.
- **Context layer** — maintains the event log, computes what to surface to the brain, manages compaction. Stateful.
- **Orchestration layer** — provisions and terminates sessions, routes between agents, manages lifecycle. Coordinates across sessions.

This mirrors the Brain / Hands / Session decomposition in [[Meta-Harness]] but adds orchestration as a distinct layer above session management.

### Structured error surfaces

When a tool call fails, the harness should:

1. Log the failure event (always)
2. Classify: is this recoverable? (Can the model try a different approach, or is this fatal?)
3. Surface to model: if recoverable, present a structured error object the model can reason about. If fatal, halt and surface to the orchestration layer.

The post includes an example of a structured error object passed back to Claude:

```json
{
  "error_type": "tool_unavailable",
  "tool": "browser.navigate",
  "reason": "sandbox connection timeout after 30s",
  "recoverable": true,
  "suggested_alternatives": ["retry", "use_cached_result", "skip_and_note"]
}
```

This is related to [[Error Trace Retention]] — but the post specifically emphasizes that the raw traceback should NOT be the primary error surface for the model. The model benefits from a structured, model-readable error, with the raw trace stored in the event log for human debugging.

### Credential and side-effect scoping

Long-running agents accumulate capabilities over time (credentials, open connections, acquired locks). The harness must:

- Scope credentials to session lifetime, not process lifetime
- Track which tool calls have external side effects that are NOT idempotent
- On recovery, identify which side-effect-carrying steps need human review before replay

The post describes this as **side-effect accounting**: a manifest of non-idempotent tool calls, maintained by the harness, consulted before any replay attempt.

## Testing harnesses

The post dedicates a section to harness testing, noting that most harness bugs appear only in long runs or under failure conditions — both expensive to trigger in testing. Recommended practices:

- **Fault injection** — deliberately fail tool calls, exhaust context windows, kill sandbox connections mid-run. Test harness recovery paths explicitly.
- **Event log diffing** — run two harness implementations on the same event log and diff the model inputs produced. Catches divergence in compaction logic.
- **Replay testing** — construct synthetic event logs representing known-difficult states (near-full context, mid-task failures) and verify recovery behavior.

## Relationship to Managed Agents

The post is explicit that Managed Agents (see [[Managed Agents]]) implements these patterns at infrastructure scale, but the design principles apply equally to custom harnesses built outside of Managed Agents. The meta-harness abstraction (Brain / Hands / Session) is the generalized form; Managed Agents is one hosted instance.

The engineering recommendation: **build harnesses against the meta-harness interface contract even if you're not using Managed Agents**, so that migration is mechanical when you eventually want hosted durability.

## Key claims (verbatim / near-verbatim)

1. "The harness — not the model — is responsible for correctness, durability, and recoverability in long-running agents."
2. "Any session that cannot be re-provisioned from its event log is a design smell."
3. "Silent truncation is the most common harness failure mode we observe in production agents."
4. "Build harnesses against the meta-harness interface contract even if you're not using Managed Agents."
5. "Side-effect accounting: a manifest of non-idempotent tool calls, consulted before any replay attempt."
