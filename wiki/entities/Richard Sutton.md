---
type: entity
title: "Richard Sutton"
created: 2026-05-20
updated: 2026-06-01
tags:
  - ai-agents
  - llm
  - entity
  - person
status: developing
entity_type: person
entity_tier: thinker
role: "Reinforcement learning pioneer (co-author of the standard RL textbook); author of 'The Bitter Lesson' (2019) and co-author of 'The Era of Experience' (2025)."
core_claim: "General methods that scale with compute beat hand-engineered human knowledge — and the next data source is the agent's own experience, not human corpora."
first_mentioned: 2026-05-20
related:
  - "[[The Bitter Lesson]]"
  - "[[Model-Centric Architecture]]"
  - "[[Andrej Karpathy]]"
  - "[[Online Learning from Interaction]]"
sources:
  - "[[2019-03-13 - Sutton - The Bitter Lesson]]"
  - "[[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]"
---

# Richard Sutton

Foundational figure in reinforcement learning (co-author of the standard RL textbook) and author of the most-cited short argument in modern AI.

## Worldview / 核心主张

1. **Scaling general methods beats encoding human knowledge.** [[The Bitter Lesson]] (2019): over 70 years of AI, the two things that scale arbitrarily with compute — **search** and **learning** — repeatedly overtake hand-engineered human knowledge (chess, Go, speech, vision). Baking in "how we think we think" satisfies the researcher and then plateaus.
2. **Experience replaces human data.** [[2025-04-11 - Silver Sutton - Welcome to the Era of Experience|The Era of Experience]] (2025, w/ David Silver): high-quality human data is hitting its limit; the next generation of agents acquires superhuman capability by learning from **their own streams of experience**.
3. **Grounded rewards over human prejudgment.** Reward should come from measurable environmental outcomes (cost, error rate, exam results), not from a human scoring a response's plausibility — which imposes a performance ceiling.

## Methodology / 方法论

- **Argue from the historical pattern, not from a system.** Both works are manifestos: he establishes a recurring 70-year pattern, then projects it forward. He builds the *meta-argument* ("build meta-methods that discover complexity") rather than a specific method.
- **Push the principle to its uncomfortable conclusion.** The "bitter" in the lesson is deliberate — he names the emotional resistance (researchers were "embittered") as evidence the field keeps relearning it.
- **Define the primitive, let others fill it in.** The four characteristics of experiential agents (streams, grounded actions, grounded rewards, non-human reasoning) are a research agenda, explicitly left for empirical work to operationalize.

## Body of work (in the wiki)

- **2019 — [[2019-03-13 - Sutton - The Bitter Lesson]]** — search + learning beat hand-engineered knowledge; the canonical scaling argument.
- **2025 — [[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]** — the experience-stream follow-up: continuous lifelong learning, environment-grounded actions and rewards, reasoning beyond human chains of thought.

## Throughlines

- **Distrust of human priors** runs through both: in 2019 it's hand-engineered features; in 2025 it's human-authored training data and human-rated reward. The enemy is always the human bottleneck on a scalable process.
- **Compute + general method as the long-run winner** — the through-argument under [[Model-Centric Architecture]].

## Tensions

- **vs [[Andrej Karpathy]]** — complementary backbone, but Karpathy adds the *human-in-the-loop / understanding* constraints Sutton's pure-experience view underweights.
- **vs harness/schema-centric agent practice** (this vault's own bias; cf. Manus's static-action-space view) — Sutton's evidence is from perception/games with no real-world side effects. Whether the lesson transfers to agent harnesses where safety, latency, and side effects matter is **contested** — the `[!gap]` flagged on [[2019-03-13 - Sutton - The Bitter Lesson]]. Sutton is the counterweight Nick's practice must answer.

## Corpus to ingest

- *Reinforcement Learning: An Introduction* (Sutton & Barto) — the textbook foundation; would anchor the RL-primitives thread that [[GRPO]]/[[RL with Verifiable Rewards]] currently cite without a root.
- The full *Era of Experience* paper details (currently summarized at manifesto level).
