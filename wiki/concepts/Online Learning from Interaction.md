---
type: concept
title: Online Learning from Interaction
created: 2026-05-20
updated: 2026-05-20
tags: [ai-agents, llm, real-time-learning, continual-learning, reinforcement-learning]
status: developing
related: ["[[In-Context Learning]]", "[[Test-Time Adaptation]]", "[[Implicit Feedback Signals]]", "[[Agent Memory Taxonomy]]", "[[Self-Editing Memory]]", "[[Session as Event Log]]"]
sources: ["[[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]"]
---

# Online Learning from Interaction

## Summary

The umbrella concept for **real-time learning**: an agent improves from its own ongoing stream of interaction — corrections, follow-ups, direction changes, even silence — rather than only from offline training cycles. [[Welcome to the Era of Experience]] frames this as the field's next phase: agents learning in **continuous streams** from **grounded environmental rewards** (confidence: high; Source: [[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]). A common operationalization frames it as a perception → memory → action loop.

## The spectrum of online adaptation

| Mechanism | What changes | Persistence | Page |
|---|---|---|---|
| In-context | the prompt | one context | [[In-Context Learning]] |
| Memory write-back | external store | across sessions | [[Self-Editing Memory]], [[Agent Memory Taxonomy]] |
| Test-time training | weights, transiently | per task | [[Test-Time Adaptation]] |
| Continual / online RL | weights, permanently | lifelong | this page |

Silence and disengagement are signals too: absence of a follow-up correction is weak positive evidence; abandonment is negative ([[Implicit Feedback Signals]]).

## Why it matters

It is the natural extension of static deploy-and-monitor: instead of shipping a frozen model and retraining quarterly, the agent's competence is a function of its accumulated interaction. This is where Nick's three systems converge into one loop (see Connections).

## When X still wins (limits)

- **Catastrophic forgetting** — permanent online updates risk erasing prior capability; memory mechanisms are the main mitigation.
- **Reward hacking / poisoning** — grounded or implicit signals can be gamed; durable writes can be polluted ([[Self-Editing Memory]] memory-poisoning risk).
- **Offline still wins** for large capability jumps, safety-critical changes, and anything needing evaluation before exposure.

## Connection to prior work

Roots in RL (Sutton) and online learning; the LLM-era twist is that adaptation can happen in-context or in memory, not only in weights. Builds on [[CoALA]]'s "learning" internal action and [[Session as Event Log]] (the stream of experience made concrete).

## Connections — Nick's projects as a real-time learning stack

- **Sonic** (substrate): Kafka/Spark streaming, 4h → <5min latency, exactly-once, consumer-lag observability. This is the *perception* layer — without low-latency, reliable signal capture there is nothing to learn from in real time.
- **Donut** (the loop): confidence-gated KNN write-back flywheel — high-confidence neighbors inherit labels, index grows, cost flattens. A concrete online-adaptation loop at the data layer (−60% LLM calls, −86% cost). This is *memory + action* refining over the stream.
- **Compass** (closed governance loop): user logs feed back into KB priority, eval rubric, and policy — online learning where the artifact updated is the policy/eval, not weights.

Framed together: Sonic captures the stream, Donut adapts from it cheaply, Compass closes it into governance. Real-time learning is the unifying abstraction over all three.

## Open questions

- Which signal types (correction, follow-up, silence, abandonment) are reliable enough to update on automatically vs. require human review?
- Where to draw the line between cheap reversible adaptation (context/memory) and risky permanent adaptation (weights)?

## Sources

- [[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]
