---
type: concept
title: In-Context Learning
created: 2026-05-20
updated: 2026-05-20
tags: [ai-agents, llm, real-time-learning, in-context-learning]
status: developing
related: ["[[Test-Time Adaptation]]", "[[Online Learning from Interaction]]", "[[Learning from Implicit Feedback]]", "[[Context Engineering]]", "[[Few-Shot Drift]]"]
sources: ["[[2024-04-17 - Agarwal et al - Many-Shot In-Context Learning]]"]
---

# In-Context Learning

## Summary

In-context learning (ICL) is adaptation to a task **at inference time, from examples placed in the prompt, with no weight updates**. It is the cheapest and most reversible form of real-time learning: the model "learns" the task for the duration of one context and forgets it the moment the context clears. Many-shot ICL (hundreds–thousands of examples) approaches fine-tuning quality and can even **override pretraining biases** (confidence: high; Source: [[2024-04-17 - Agarwal et al - Many-Shot In-Context Learning]]).

## Why it matters

For agents, ICL is the first lever of real-time adaptation. A correction, a retrieved example, or a follow-up turn becomes new in-context evidence the agent immediately conditions on. No training pipeline, no deployment risk, instant rollback. It is the mechanism behind "the agent got better mid-conversation" without any model change.

## When X still wins (limits)

- **Ephemeral** — knowledge vanishes when the context resets. Persisting it requires memory ([[Agent Memory Taxonomy]], [[Self-Editing Memory]]) or weight updates ([[Test-Time Adaptation]]).
- **Token cost / latency** — many-shot ICL spends context budget and inflates cost; see [[Token Economics]].
- **Drift** — stale or skewed in-context examples bias behavior ([[Few-Shot Drift]]).

## Connection to prior work

Origin: Brown et al. 2020 (GPT-3 few-shot). Many-shot scaling: Agarwal et al. 2024. ICL is the no-weight-update endpoint of the spectrum; [[Test-Time Adaptation]] sits one step further (transient weight updates), continual learning further still (persistent updates).

## Connections

- **Nick's projects:** Donut's semantic-cache flywheel is ICL-adjacent at the retrieval layer — high-confidence neighbors supply labels that condition the next decision, the way in-context examples condition a prompt, but persisted in an index rather than the window.

## Open questions

- How much of an agent's "learning" should stay in-context (cheap, reversible) vs. graduate to memory or weights?
- When does many-shot context cost exceed the cost of a small fine-tune?

## Sources

- [[2024-04-17 - Agarwal et al - Many-Shot In-Context Learning]]
