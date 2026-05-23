---
type: concept
title: "Jagged Intelligence"
created: 2026-05-22
updated: 2026-05-22
status: seed
tags:
  - ai-agents
  - llm
  - foundational
related:
  - "[[Verifiability]]"
  - "[[Software 3.0]]"
  - "[[Agentic Engineering]]"
  - "[[The Bitter Lesson]]"
sources:
  - "[[2026-05-22 - Karpathy - Sequoia Ascent 2026]]"
---

# Jagged Intelligence

LLM capability is **not smooth**. A model can be brilliant on one task and "bizarrely dumb in the next" — the "car wash walking" problem. Karpathy decomposes the jaggedness into roughly:

```
capability ≈ verifiability × training attention × data coverage × economic value
```

Capability spikes where a task is **verifiable** (see [[Verifiability]]) *and* where labs spent training attention — pretraining mixture, post-training, RL environments, benchmark pressure. GPT-4's chess jump tracked "much more chess data included in the training mix," not general improvement.

## Models are artifacts, not minds

LLMs are "artifacts of pretraining mixtures, RL environments, benchmark pressure, product priorities, and economic incentives." Their competence map is shaped by what was economically and academically worth training.

## Ghosts, not animals

LLMs lack biological drives — no embodied survival, curiosity, play, or intrinsic motivation. They are "statistical simulations of human artifacts," "jagged, alien tools." The correct posture is **empirical familiarity**: neither dismissal nor blind trust, but learning where a model works, where it fails, what it was trained on, and where it needs guardrails. This is the disposition [[Agentic Engineering]] operationalizes.

## The practical test

**"Are you on the model's rails?"** On-rails (verified, heavily-trained) → expect excellence. Off-rails → expect failure on even basic tasks. Fixes: better context, better tools, fine-tuning, custom evals, or a proprietary RL environment (the [[Verifiability]] wedge).

## Source

- [[2026-05-22 - Karpathy - Sequoia Ascent 2026]] — entity: [[Andrej Karpathy]]
