---
type: concept
title: "Agentic Harness"
created: 2026-05-13
updated: 2026-05-28
tags:
  - ai-agents
  - coding
  - infrastructure
  - harness
  - architecture
status: developing
related:
  - "[[Autonomous Agents]]"
  - "[[Meta-Harness]]"
  - "[[Augmented LLM]]"
  - "[[SWE-bench Verified]]"
  - "[[Workflows vs Agents]]"
  - "[[ACI - Agent-Computer Interface]]"
  - "[[Model-Centric Architecture]]"
  - "[[Session as Event Log]]"
  - "[[Long-Horizon Context Management]]"
  - "[[Error Trace Retention]]"
  - "[[KV-Cache Discipline]]"
  - "[[Token Economics]]"
sources:
  - "[[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]]"
  - "[[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]]"
complexity: intermediate
domain: ai-agents
aliases:
  - agent scaffold
  - agent wrapper
  - Agent Harness Patterns
  - Harness Anti-Patterns
  - Harness Design Patterns
---

# Agentic Harness

## Definition

An **agentic harness** (also "agent scaffold") is the minimal infrastructure wrapping an LLM to enable agentic behavior: tool access, an action loop, and a stopping condition. It is the "outside" of an agent — the code that gives the model its hands and memory interface — as distinct from the model itself.

The term sits between [[Augmented LLM]] (the base primitive: LLM + tools) and [[Meta-Harness]] (Anthropic's production-scale hosting abstraction for long-running agents). An agentic harness is typically task-scoped and lightweight, but as runs get longer the harness — not the model — becomes responsible for **correctness, durability, and recoverability**. Harness design is then a first-class engineering discipline, comparable to database or API design.

> "The harness — not the model — is responsible for correctness, durability, and recoverability in long-running agents." — [[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]]

## Minimal anatomy

A harness typically provides:
1. **Tool definitions** — file read, shell exec, file edit, test runner, web browser, etc.
2. **Action loop** — invoke model → parse tool calls → execute → feed result back → repeat
3. **Budget / stopping condition** — max steps, max tokens, success signal (e.g., test pass)
4. **Context management** — how prior steps are summarized or truncated as the conversation grows

## Simplicity as a finding (SWE-bench result)

The Anthropic [[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]] result directly demonstrates that **harness simplicity is not the capability bottleneck**. A simple loop with standard coding tools + [[Claude 3.5 Sonnet]] achieved 49% on [[SWE-bench Verified]], outperforming prior approaches that used more complex scaffolding (ensembles, retrieval pipelines, parallel sampling).

This implies:
- Prior SOTA complexity was compensating for weaker base models
- The harness is an [[ACI - Agent-Computer Interface]] design problem, not an orchestration problem — get the tools right, then let the model drive

## Design patterns (long-running harnesses)

Per [[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]], once tasks span many steps the harness owns four responsibilities the model itself cannot provide:

| Responsibility | Definition |
|---|---|
| Context management | Decide what the model sees at each step; own compaction, JIT retrieval, annotation |
| Checkpoint / recovery | Persist sufficient state to resume after failure; treat runs as idempotent where possible |
| Error containment | Classify errors as recoverable vs. fatal; surface structured errors to model, raw traces to log |
| Lifecycle management | Provision, terminate, re-provision sessions; enforce "cattle not pets" — see [[Meta-Harness]] |

### Anti-patterns

Named in production at Anthropic:

- **God harness** — monolithic harness mixing all concerns (context, errors, credentials, dispatch) in one undifferentiated layer. Untestable, brittle to change.
- **Chatty checkpointing** — writing to durable storage on every token or tool call. Write amplification that dominates real workload cost. See [[Token Economics]].
- **Silent truncation** — dropping context when the window is full without logging the event or notifying the model. The most common production failure mode for long-running agents. The model continues unaware of the gap; failures compound silently.
- **Model-owned durability** — harness delegates state-management responsibility into the model's context (e.g., "ask the model to request a save"). Works for short sessions; falls apart when the model loses track of what it was supposed to save.

### Layered architecture

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

This extends the Brain/Hands/Session decomposition of [[Meta-Harness]] by making orchestration an explicit, distinct layer above session management. Each layer has a clear interface contract; implementations can change beneath it. The orchestration layer is the meta-harness analogue of a container orchestrator (Kubernetes) above individual container runtimes.

### Structured error surfaces

When a tool call fails, the harness:

1. Always logs the failure event in the event log (raw trace, verbatim)
2. Classifies: recoverable (model can route around) or fatal (halt, alert orchestration layer)
3. Surfaces to model: a structured object for recoverable errors; nothing for fatal (halt instead)

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

### Side-effect accounting

The harness maintains a **manifest of non-idempotent tool calls** — tool calls with external side effects that cannot be safely replayed. Before any replay or recovery attempt, the harness consults this manifest. Idempotent calls are safe to replay automatically; non-idempotent calls are flagged for human confirmation.

### Testing practices

- **Fault injection** — deliberately fail tool calls, exhaust context windows, kill sandboxes mid-run. Test recovery paths explicitly, not just happy paths.
- **Event log diffing** — run two harness implementations on the same event log and diff the model inputs produced. Catches divergence in compaction logic or context-surface decisions.
- **Replay testing** — construct synthetic event logs representing known-hard states (near-full context, mid-task failures) and verify recovery behavior.

### Build against the meta-harness contract

Anthropic recommends building custom harnesses against the meta-harness interface contract (Brain / Hands / Session) even without using Managed Agents. This keeps migration to hosted durability mechanical rather than architectural.

> "Build harnesses against the meta-harness interface contract even if you're not using Managed Agents."

## Relation to other concepts

| Concept | Relationship |
|---------|-------------|
| [[Augmented LLM]] | An agentic harness instantiates one; adds the loop and stopping logic |
| [[Autonomous Agents]] | The pattern the harness enables — model chooses its own action sequence |
| [[Workflows vs Agents]] | A harness can host either; an autonomous coding harness is firmly "agent" side |
| [[Meta-Harness]] | Production-grade harness abstraction; same idea scaled to multi-tenant, long-horizon |
| [[Session as Event Log]] | The recommended durable substrate beneath a long-running harness |
| [[Orchestrator-Workers]] | Multi-agent variant of a harness |

## Tension with Meta-Harness

If a simple harness achieves 49% on SWE-bench, the incremental capability value of [[Meta-Harness]] (Anthropic's heavy infra abstraction) is not self-evident from the capability axis alone. Meta-Harness buys reliability, observability, cost management, and multi-agent coordination — but not raw capability per task. This is a tension worth tracking.

> [!contradiction]
> [[Meta-Harness]] argues for infra-heavy scaffolding for production agents. The SWE-bench Verified result (simple harness, 49% pass@1) suggests that for capability on well-specified isolated tasks, complexity adds little. The resolution is likely domain: isolated task capability vs. production reliability at scale are different goals served by different layers — the design patterns above are exactly the reliability layer, not the capability layer.

## Open questions

- At what session length does snapshot + incremental replay become cheaper than full replay? Any published numbers?
- Side-effect manifest format — should non-idempotent calls be tagged at the tool-definition level (schema), or at the call-site level (runtime classification)?
- Does the god-harness anti-pattern correlate with a particular team/org structure? Conway's Law implication: teams with one person responsible for "the agent" build god harnesses.

## Sources

- [[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]] (Anthropic, 2024-10-29) — simplicity-as-finding
- [[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]] (Anthropic, 2026-05) — the four responsibilities, anti-patterns, layered architecture, testing
