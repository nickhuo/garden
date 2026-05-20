---
type: concept
title: Agent Interface Contracts
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - agent-pattern
  - software-engineering
status: seed
complexity: intermediate
domain: ai-agents
aliases:
  - interface contracts
  - inter-agent contracts
related:
  - "[[Parallelization]]"
  - "[[Orchestrator-Workers]]"
  - "[[Multi-Agent Systems]]"
  - "[[Context Decomposition vs Problem Decomposition]]"
sources:
  - "[[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]]"
---

# Agent Interface Contracts

## Summary

In parallel multi-agent systems, the orchestrator defines **interface contracts** — explicit specifications of the inputs, outputs, and conventions each worker agent must honor — before workers begin implementation. Contracts enable workers to operate in fully isolated context windows with no direct inter-agent communication; the interface is the only coupling point. Introduced as a first-class pattern by the Anthropic C compiler experiment.

## Mechanism

1. **Orchestrator phase**: before spawning workers, the orchestrator designs subsystem boundaries and writes interface specs (type signatures, data formats, error conventions, integration assumptions).
2. **Worker phase**: each worker receives its spec + relevant domain material only. Workers implement against the contract without knowledge of adjacent subsystems.
3. **Integration phase**: orchestrator collects worker outputs and reconciles them. Mismatches (underspecified types, differing error conventions) require additional reconciliation rounds.

## Why it enables parallelism

Workers have no runtime dependency on each other — only a static dependency on the interface spec, which is defined before they start. This is the parallel-agent analog of API contracts in distributed software engineering: you can build microservices concurrently once the APIs are agreed.

## The bottleneck

**Interface specification quality is the rate-limiting factor**, not worker implementation throughput. Underspecified contracts produce more reconciliation rounds, consuming additional tokens and wall-clock time. Orchestrator model capability (system-design thinking) therefore matters more than worker model capability for overall task efficiency.

## Connections

- Coordination primitive for: [[Orchestrator-Workers]] (workflow variant) and [[Parallelization]] (sectioning sub-pattern)
- Enables: [[Multi-Agent Systems]] applied to software engineering
- Orchestrator performing this role is an instance of: [[Context Decomposition vs Problem Decomposition]] — decomposing the *problem space* into bounded, contractually-isolated workstreams

## Open Questions

- Does interface contract quality correlate with orchestrator model tier — does a stronger orchestrator write fewer underspecified contracts?
- Are there tooling patterns (schema validation, automated contract testing) that can reduce reconciliation rounds?
- How does this pattern interact with [[Session as Event Log]] — should contracts be logged as events for auditability?

## Sources

- [[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]] (Anthropic, 2026-05)
