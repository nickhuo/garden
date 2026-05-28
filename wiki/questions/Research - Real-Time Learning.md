---
type: synthesis
title: "Research: Real-Time Learning"
created: 2026-05-20
updated: 2026-05-20
tags: [research, ai-agents, llm, real-time-learning]
status: developing
related: ["[[Online Learning from Interaction]]", "[[In-Context Learning]]", "[[Test-Time Adaptation]]", "[[Implicit Feedback Signals]]", "[[Welcome to the Era of Experience]]", "[[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]", "[[2024-04-17 - Agarwal et al - Many-Shot In-Context Learning]]", "[[2025-05-21 - Meta - Reinforcement Learning from User Feedback]]", "[[Agent Memory Taxonomy]]", "[[Self-Editing Memory]]"]
sources: ["[[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]", "[[2024-04-17 - Agarwal et al - Many-Shot In-Context Learning]]", "[[2025-05-21 - Meta - Reinforcement Learning from User Feedback]]"]
---

# Research: Real-Time Learning

## Overview

Real-time learning is an agent improving from its immediate stream of interaction — corrections, follow-ups, direction changes, even silence — rather than only from offline training cycles. The literature splits cleanly along **what gets updated and how durably**: the prompt (in-context), an external store (memory), or weights (test-time / continual). [[Welcome to the Era of Experience]] supplies the "why now"; the other four sources supply concrete mechanisms across that spectrum.

## Key Findings

- The era of learning predominantly from human data is ending; future agents acquire capability by learning from their own experience in continuous streams with grounded environmental rewards (Source: [[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]). (confidence: high — foundational position paper, widely cited)
- A practical spectrum runs from cheapest/most reversible to most durable/most dangerous: **in-context → memory write-back → test-time training → continual online RL** (Source: [[Online Learning from Interaction]]). (confidence: high — synthesized across the sources)
- Many-shot in-context learning approaches fine-tuning quality and can override pretraining biases with no weight updates — the cheap end of real-time adaptation (Source: [[2024-04-17 - Agarwal et al - Many-Shot In-Context Learning]]). (confidence: high)
- Implicit production signals (engagement, selection, follow-up, abandonment) can train reward models competitive with explicit ratings, enabling continuous learning from live traffic (Source: [[2025-05-21 - Meta - Reinforcement Learning from User Feedback]]). (confidence: medium — single source)

> [!gap] The test-time-training rung and the catastrophic-forgetting claim lost their citations when two non-milestone sources were trimmed; both need a milestone source.

## Key Entities

- [[Richard Sutton]], David Silver — authors of the Era of Experience thesis.
- DeepMind (many-shot ICL, Era of Experience), MIT (TTT), Meta (RLUF) — institutional sources.

## Key Concepts

- [[Online Learning from Interaction]] — the umbrella; the full adaptation spectrum.
- [[In-Context Learning]] — adapt the prompt, no weight change.
- [[Test-Time Adaptation]] — transient per-task weight updates.
- [[Implicit Feedback Signals]] — the reward stream behind it all.
- Substrate: [[Agent Memory Taxonomy]], [[Self-Editing Memory]], [[Session as Event Log]].

## Contradictions

- **Grounded reward vs. implicit-signal reward.** Silver & Sutton argue human-prejudgment reward imposes a ceiling and push for *environmental* grounded reward. Meta's RLUF leans on *human behavioral* signals (engagement/clicks) — which are still human-mediated and gameable. These are reconcilable (behavioral signals are partway to grounded) but in tension: implicit-feedback optimization can reintroduce exactly the reward-hacking ceiling the Era-of-Experience critiques.
- **Adapt-now vs. forget-later.** TTT and continual updates improve immediate performance but risk catastrophic forgetting; the lifelong-learning roadmap treats this as the central unsolved problem. No source resolves how aggressively a deployed agent should update weights online.

## Open Questions

- Where is the right cut between reversible adaptation (context/memory) and risky permanent adaptation (weights) for production agents?
- How to debias implicit signals (satisfied-silence vs. confused-silence; engagement vs. correctness)?
- Which signals are safe to auto-update on vs. require a human gate?
- Can test-time training be made cheap enough for per-turn agent use?

## Nick's projects as a real-time learning stack

- **Sonic** = perception substrate (Kafka/Spark, 4h→<5min, exactly-once, lag observability) — makes real-time signal capture possible.
- **Donut** = the adaptation loop (confidence-gated KNN write-back flywheel; −60% LLM calls, −86% cost, F1≥85%) — cheap online adaptation at the data layer, the engineering-realist counterpart to gradient TTT.
- **Compass** = the governed closed loop (user logs → KB priority / eval rubric / policy) — online learning where the updated artifact is policy and evaluation, not weights.

Real-time learning is the unifying abstraction over all three: capture (Sonic), adapt (Donut), govern (Compass).

## Sources

- [[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]
- [[2024-04-17 - Agarwal et al - Many-Shot In-Context Learning]]
- [[2025-05-21 - Meta - Reinforcement Learning from User Feedback]]
