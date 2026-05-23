---
type: concept
title: Test-Time Adaptation
created: 2026-05-20
updated: 2026-05-20
tags: [ai-agents, llm, real-time-learning, test-time-training]
status: developing
related: ["[[In-Context Learning]]", "[[Online Learning from Interaction]]", "[[LoRA]]", "[[Learning from Implicit Feedback]]"]
sources: []
---

# Test-Time Adaptation

## Summary

Test-time adaptation (TTA), including **test-time training (TTT)**, updates model weights *during inference* on data derived from the current task, then answers with the adapted model. It sits between [[In-Context Learning]] (no weight change) and continual learning (permanent weight change): the update is real but typically transient and per-task. The mechanism is a few gradient steps (often via per-task [[LoRA]] adapters) on data derived from the prompt's own structure before producing the final answer.

> [!gap] Needs a milestone source; the ARC test-time-training paper was removed as too narrow.

## Why it matters

When in-context examples are insufficient — high-dimensional, structurally novel tasks — a few gradient steps on the prompt's own structure beats a frozen model. For agents this is "stop and learn this specific task before acting," a learning step taken *inside* the task loop rather than offline.

## When X still wins (limits)

- **Latency and compute** — gradient steps per task are expensive; [[In-Context Learning]] is preferable when context alone suffices.
- **Not persistent by default** — adaptation is discarded after the task unless deliberately retained (then it becomes continual learning, with catastrophic-forgetting risk).
- **Stability** — online weight updates on noisy single-instance data can destabilize a deployed model.

## Connection to prior work

Lineage: Sun et al. test-time training (self-supervised adaptation) → later LoRA-based TTT for reasoning. It is the weight-update analogue of many-shot ICL ([[2024-04-17 - Agarwal et al - Many-Shot In-Context Learning]]), and the practical mechanism behind the experiential learning [[Welcome to the Era of Experience]] argues for.

## Connections

- **Nick's projects:** Donut's confidence-gated KNN write-back is a lightweight, non-gradient TTA at the data layer — the index adapts per interaction so future queries resolve without an LLM call (−60% calls, −86% cost, F1≥85%). Same shape (adapt now, benefit on the next instance), cheaper substrate than gradient TTT.

## Open questions

- Can transient TTA be made cheap enough for per-turn agent use?
- When should a successful test-time adaptation be promoted to persistent weights vs. discarded?
