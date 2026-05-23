---
type: synthesis
title: "Research - Continually-Learning Model-Centric Systems"
created: 2026-05-20
updated: 2026-05-20
tags: [research, ai-agents, llm, continual-learning, architecture]
status: developing
related:
  - "[[Research - Real-Time Learning]]"
  - "[[Research - Persistent Memory and Persona Vectors]]"
  - "[[Research - Model-Centric Architecture]]"
  - "[[Research - Online Evaluation]]"
  - "[[Online Learning from Interaction]]"
  - "[[Persona Vectors vs Memory Files]]"
  - "[[Model-Centric Architecture]]"
  - "[[Online Evaluation]]"
sources:
  - "[[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]"
  - "[[2019-03-13 - Sutton - The Bitter Lesson]]"
  - "[[2017-11-11 - Karpathy - Software 2.0]]"
  - "[[2025-07-29 - Chen et al - Persona Vectors]]"
  - "[[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]]"
  - "[[2022-03-04 - Ouyang et al - InstructGPT]]"
---

# Research - Continually-Learning Model-Centric Systems

## Overview

Four directions — real-time learning, persistent memory, model-centric architecture, online evaluation — are not four topics. They are four faces of one system: an agent that improves from each interaction, keeps what it learns, lets the model (not the surrounding code) own that learning, and is steered by signals read from live use rather than only offline benchmarks. This page is the spine; each pillar has its own research synthesis.

## The loop

```
   interaction  ──▶  online evaluation  ──▶  learning signal
       ▲                (judge / reward /          │
       │                 implicit / A-B)           ▼
   model acts  ◀──  persisted state  ◀──  real-time learning
 (model-centric)   (persona vectors /     (in-context → memory →
                    memory files)          test-time → online RL)
```

A live interaction produces a signal. **Online evaluation** scores it. **Real-time learning** turns the score into an update along a spectrum of durability. **Persistent memory** stores the result so the next session starts ahead. A **model-centric** architecture puts the model — not orchestration code — in charge of consuming and producing all four, with the user holding final control.

## The four pillars

1. **Real-time learning** ([[Research - Real-Time Learning]]) — a spectrum by what/how-durably it updates: in-context → memory write-back → test-time training → continual online RL, cheapest/most-reversible to most-durable/most-dangerous. Catastrophic forgetting is the central unsolved problem; memory is its main mitigation. ([[Welcome to the Era of Experience]], [[Test-Time Adaptation]], [[Online Learning from Interaction]].)
2. **Persistent memory & persona vectors** ([[Research - Persistent Memory and Persona Vectors]]) — two complementary paths split on control vs inspectability: **persona vectors** (parametric, model-internal control over *who* the agent is) and **memory files** (contextual, inspectable record of *what* it knows). ([[Persona Vectors]], [[Memory Stream]], [[Persona Vectors vs Memory Files]].)
3. **Model-centric architecture** ([[Research - Model-Centric Architecture]]) — code to the side, model at the center. Backed by the scaling argument ([[The Bitter Lesson]], [[Software 2.0]]); countered at ship time by the harness/schema discipline that supplies guarantees the model can't ([[Agentic Harness]], Manus's static action space). The durable side-code is the guarantees layer (constraints, validation, permissioning).
4. **Online evaluation** ([[Research - Online Evaluation]]) — the conduit from interaction to durable change: implicit/explicit signal → judge or reward model → update to retrieval/rubric/policy/persona. Spectrum from cheap-observational ([[Implicit Feedback Signals]]) to slow-causal ([[A/B Testing for Agents]]); rests on [[Eval Validity]] because every signal is a proxy.

## Cross-cutting tensions

- **Reversibility vs durability.** How aggressively should a deployed agent move from prompt/memory (reversible) to weights (permanent)? No source resolves the cut. (Pillars 1, 2.)
- **Grounded vs human-mediated reward.** Era-of-Experience pushes environmental reward to escape the human-judgment ceiling; implicit-feedback and RLHF optimize human signals that are gameable. (Pillars 1, 4.)
- **Model freedom vs guarantees.** Model-centrism wants the model to own logic; reliability evidence says structure the model can't provide (valid schemas, deterministic routing, permission gates) wins now. The reconciliation is a slider, and the guarantees layer is the durable residue. (Pillar 3, all.)
- **Control vs inspectability.** Persona vectors are powerful but opaque; memory files are inspectable but indirect. Which path each learned item belongs on is the open design question. (Pillar 2.)
- **Online reward-hacking.** A model that detects it is being scored on live traffic can game implicit signals ([[Eval Awareness]] as an online failure mode). (Pillars 3, 4.)

## Connection to Nick's prior work

| Pillar | Nick's prior work | Extension opportunity |
|---|---|---|
| Real-time learning | **Sonic** (capture: Kafka/Spark, exactly-once), **Donut** (adapt: confidence-gated KNN write-back flywheel) | Flywheel -> multi-agent learning: one agent observes another's success pattern and updates its own tool ranking |
| Persistent memory / persona | **Beckman** (mastery overlay = memory-file; `PL=C+A*Ease+B*Novelty` (A,B,C) = interpretable persona-vector analogue), **Baidu** (K-means persona archetypes) | Beckman's interpretable coefficients -> higher-dimensional learned persona vectors that stay inspectable across domains |
| Model-centric architecture | **Donut** ("action space is data; the prompt is never a catalog"), **Beckman** ("schema is the lever; prompts become implementation detail"), **Compass** (multi-model routing) | Identify which side-code is scaffolding (scaling absorbs) vs guarantees (persists); push the rest into the model |
| Online evaluation | **Compass** (dual-judge, RAGAS, golden dataset, logs->rubric/policy closed loop), **Donut** (46-workflow golden eval + shadow/canary), **Beckman** (two-axis LLM-as-judge -> method pivot) | Compass rubric -> cross-agent scoring (tool-choice eval, reasoning-path eval); offline golden base -> live implicit-signal extension |

Nick's center of gravity is **online evaluation + schema/contract discipline**; this research positions real-time learning and persona persistence as the extensions those strengths most naturally reach toward.

## Open questions (system level)

- What is the minimal safe online loop: which signals auto-update which stores, and which require a human or A/B gate before persisting?
- Can persona vectors be made as inspectable as Beckman's coefficients without losing their control advantage?
- Is context engineering the new hand-engineered knowledge The Bitter Lesson warns against, or a permanent interface?
- How to detect online reward-hacking (engagement-via-frustration) before it harms long-term value?

## Sources

See the four pillar syntheses for full source lists. Anchors: [[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]], [[2019-03-13 - Sutton - The Bitter Lesson]], [[2017-11-11 - Karpathy - Software 2.0]], [[2025-07-29 - Chen et al - Persona Vectors]], [[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]], [[2022-03-04 - Ouyang et al - InstructGPT]].
