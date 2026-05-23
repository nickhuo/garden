---
type: concept
title: Session as Event Log
created: 2026-05-04
updated: 2026-05-13
tags:
- ai-agents
- persistence
- context
- infrastructure
status: developing
related:
- "[[Memory Stream]]"
sources:
- "[[2026-04-08 - Anthropic - Scaling Managed Agents]]"
- "[[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]]"
aliases:
- Session Event Log
_legacy_source_count: 1
---

# Session as Event Log

## Summary

Per [[Scaling Managed Agents]] (Anthropic 2026-04): an **append-only event log** that lives **outside Claude's context window** and serves as the durable substrate for long-running agents. The brain interrogates it via `getEvents()` (positional slices, rewinds, rereads). Distinct from in-context conversation history, distinct from agent memory files — it is the *system-level* persistence layer.

## Definition

> "In Managed Agents, the session provides this same benefit, serving as a context object that lives outside Claude's context window."

Two clean separations result:

- **Context engineering becomes a harness concern** (what subset of events does the brain need *now*?)
- **Durability becomes a session concern** (how do we keep the log intact across crashes, restarts, multi-tenant scale?)

## Why it's different from other persistence

| Layer | What it persists | Where it lives | Who reads |
|---|---|---|---|
| Conversation history | Last N turns | In-context | Brain (always) |
| Agent memory file (NOTES.md) | Curated state | External, agent-managed | Brain (on agent decision) |
| **Session event log** | All events, append-only | External, system-managed | Brain via `getEvents()` API |
| Source documents (raw) | Reference material | External, immutable | Brain via tool calls |

The session event log is the unified, system-managed truth — agent memory files and conversation history can be *derived* from it on demand.

## Operational consequences

- **Recovery is trivial** — replay events, no special-case state restoration
- **Audit / debug is built-in** — entire agent run is a structured log
- **`getEvents()` enables JIT context** — see [[Just-in-Time Context Retrieval]]; the log is the perfect target for lightweight-identifier lookup
- **Compaction shifts upstream** — the harness can build a compacted view from raw events; the agent doesn't need to manage it

## Connections

- Pattern context: [[Meta-Harness]]
- Anthropic implementation: [[Managed Agents]]
- Substrate for: [[Long-Horizon Context Management]] (compaction / note-taking / sub-agents all build on a durable event log)
- Pattern instance: [[Just-in-Time Context Retrieval]] via `getEvents()`
- Memory layer of: [[Augmented LLM]]

## Recovery variants (per Anthropic 2026-05)

[[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]] gives three concrete recovery strategies built on the event log:

| Variant | Mechanism | Cost/Correctness trade-off |
|---|---|---|
| Full replay | Re-run all events through harness into fresh brain | Correct; expensive for long runs |
| Snapshot + incremental | Periodic brain snapshots; replay only delta | Balanced; snapshot storage vs. replay cost |
| Log with compacted views | Log is authoritative; compacted view is a derived artifact | Efficient; compacted view must never be treated as ground truth |

The post also introduces **side-effect accounting**: the harness maintains a manifest of non-idempotent tool calls. Before any replay, the harness consults this manifest — steps with external side effects cannot be blindly replayed without human review.

## Open questions

- Schema for events — are they vendor-defined, or will a standard emerge across meta-harnesses?
- Replay determinism — do agents replay deterministically from the event log, or only approximately? (Matters for recovery semantics.)
- Storage cost at scale — what's the cost-per-session as runs lengthen? Anthropic doesn't disclose.
- Privacy / retention — long-running session logs are sensitive. Disclosure policies? Auto-expiration? Not addressed in source.

## Sources

- [[Scaling Managed Agents]] (Anthropic, 2026-04-08)
- [[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]] (Anthropic, 2026-05-13)
