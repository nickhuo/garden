---
type: source
title: "Many-Shot In-Context Learning"
created: 2026-05-20
updated: 2026-05-20
tags: [ai-agents, llm, real-time-learning, in-context-learning]
status: developing
source_type: paper
author: Rishabh Agarwal et al.
date_published: 2024-04-17
url: https://arxiv.org/abs/2404.11018
confidence: high
related: ["[[In-Context Learning]]", "[[Test-Time Adaptation]]"]
sources: []
key_claims:
  - "Scaling in-context examples from few-shot to hundreds/thousands (many-shot) yields large gains across generative and discriminative tasks."
  - "Many-shot ICL can override pretraining biases and learn high-dimensional functions with numerical inputs at inference, without weight updates."
  - "Reinforced ICL (model-generated rationales) and Unsupervised ICL (questions only) overcome the human-output bottleneck and rival fine-tuning."
---

# Many-Shot In-Context Learning

Agarwal et al. (Google DeepMind), April 2024 (NeurIPS 2024). Shows that expanded context windows turn [[In-Context Learning]] into a serious learning mechanism: with hundreds-to-thousands of examples, performance approaches fine-tuning — with **no weight updates**.

## Key findings (confidence: high)

- Large gains few-shot → many-shot across MATH, translation, classification.
- Many-shot ICL can **override pretraining biases** and learn new high-dimensional, numerical mappings purely in-context.
- **Reinforced ICL** substitutes model-generated chain-of-thought for human examples; **Unsupervised ICL** uses only questions. Both relieve the human-data bottleneck and remain effective on reasoning tasks.

## What it contributes to real-time learning

Establishes that an agent can absorb a substantial amount of task-specific knowledge at inference time by what it places in context — the cheapest, safest form of real-time adaptation (no training, instantly reversible). It is the upper bound on "how far can context alone take adaptation" before [[Test-Time Adaptation]] / weight updates are needed.

> [!gap] Many-shot ICL is per-prompt and ephemeral — knowledge vanishes when the context clears unless persisted via memory (see [[Agent Memory Taxonomy]], [[Self-Editing Memory]]).
