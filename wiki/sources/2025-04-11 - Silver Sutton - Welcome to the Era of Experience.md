---
type: source
title: "Welcome to the Era of Experience"
created: 2026-05-20
updated: 2026-05-20
tags: [ai-agents, llm, real-time-learning, reinforcement-learning, continual-learning]
status: developing
source_type: paper
author: David Silver, Richard Sutton
date_published: 2025-04-11
url: https://storage.googleapis.com/deepmind-media/Era-of-Experience%20/The%20Era%20of%20Experience%20Paper.pdf
confidence: high
aliases: ["Welcome to the Era of Experience", "The Era of Experience", "Era of Experience", "2025 - Silver & Sutton - The Era of Experience"]
related: ["[[Online Learning from Interaction]]", "[[Implicit Feedback Signals]]", "[[In-Context Learning]]", "[[Test-Time Adaptation]]"]
sources: []
key_claims:
  - "The era of learning predominantly from human data is ending; high-quality human data in math, code, and science approaches its limit."
  - "The next generation of agents acquires superhuman capability by learning predominantly from their own experience."
  - "Experiential agents operate in continuous streams, not discrete episodes — enabling lifelong, online learning."
  - "Rewards should be grounded in measurable environmental outcomes, not human prejudgment, which imposes a performance ceiling."
---

# Welcome to the Era of Experience

Position paper by David Silver and Richard Sutton (DeepMind / University of Alberta), 2025. Argues AI is transitioning from an **era of human data** (imitate/align to a human-authored corpus) to an **era of experience** (agents generate their own data through sustained interaction with the world). This is the conceptual anchor for **real-time learning** in agents: learning is not a separate offline phase but a property of the agent's ongoing operation.

## Four characteristics of experiential agents (confidence: high)

1. **Streams of experience** — agents act in continuous, lifelong streams rather than short disconnected episodes. Learning happens *during* operation, across long horizons, so the agent can improve from consequences observed minutes, hours, or days later.
2. **Actions and observations grounded in the environment** — agents interact with the world through rich, native action/observation channels (APIs, tools, sensors), not only by emitting text for human consumption.
3. **Grounded rewards** — feedback comes from measurable outcomes in the environment (cost, error rate, profit, health metrics, exam results, energy used) rather than human prejudgment of a response. Human-rated reward imposes a "ceiling" because it scores plausibility, not real consequences.
4. **Reasoning beyond human methods** — agents may plan and reason in ways not constrained by human-authored chains of thought, discovering strategies outside the human prior.

## What it contributes to real-time learning

- Frames **online learning from interaction** as the natural successor to the static pretrain-then-deploy pipeline — the spine of this research topic.
- Makes the distinction between **human-prejudgment reward** (RLHF-style, scores a response before its effect is known) and **grounded reward** (scores the effect) — a useful lens for designing real production feedback loops.
- Provides the "why now": data-limit pressure pushes the field toward experience as the next data source.

> [!gap] The paper is a manifesto, not an empirical method. It does not specify how to do safe, low-variance online weight updates in deployed LLM agents; that gap is filled by [[Test-Time Adaptation]], [[Implicit Feedback Signals]], and continual-learning work.
