---
type: concept
title: "LLM-as-Judge"
created: 2026-05-20
updated: 2026-05-20
tags: [ai-agents, llm, evaluation, llm-as-judge]
status: developing
related:
  - "[[LLM-as-Judge Evaluation]]"
  - "[[Online Evaluation]]"
  - "[[Reward Modeling]]"
  - "[[Eval Awareness]]"
sources:
  - "[[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]]"
---

# LLM-as-Judge

## Summary

LLM-as-Judge uses a strong LLM to score or compare outputs against a rubric, as a scalable proxy for human preference judgment. Two protocols: **single-answer grading** (score 1–10 or 0.0–1.0 on rubric axes) and **pairwise comparison** (which of A/B is better). Established by [[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]], which showed GPT-4 reaches **>80% agreement with humans — the same level humans reach with each other** (high confidence; independently replicated since).

This is the *methodology* page (biases, protocols, calibration). For the agent-specific Anthropic prescription (end-state grading, single-call judge, human spot-checks) see the existing [[LLM-as-Judge Evaluation]].

## Why it matters

It is the only mechanism that scales end-state grading to live traffic. As an **online** evaluator it can score every production interaction in real time; as an offline evaluator it grades the golden dataset. It is also the substrate of [[Reward Modeling]] via RLAIF (the judge becomes the reward signal).

## Limits — the bias catalog (load-bearing)

Per Zheng et al. and subsequent work, treat any single judge score as **low confidence** until these are controlled:

- **Position bias** — favors response shown first/last; pairwise accuracy swings >10% on order swap. Mitigate: run both orderings, keep only consistent verdicts.
- **Verbosity bias** — longer = better, regardless of quality.
- **Self-enhancement bias** — a model rates its own family higher. Mitigate: cross-family judging (e.g. Nick's Compass gpt-4o vs gpt-5 dual-judge).
- **Limited reasoning** — judges misgrade math/logic where they are themselves weak.
- **Authority bias** — rewards citations even when fabricated.

Mitigation stack: ensemble of judges, swap-and-require-consistency, and calibration against a human-labeled golden set (50–200 examples), re-run periodically because judges drift.

## Connection to prior work

Direct descendant of human preference grading in RLHF ([[2022 - Ouyang et al - InstructGPT]]); the judge is essentially an inference-time, prompt-specified reward model (see [[Reward Modeling]]). Nick's Compass dual-judge saw an **8.9pp swing on direction accuracy** between gpt-4o and gpt-5 judges — empirical proof that judge choice is a free variable that must be validated, exactly the reliability concern Zheng et al. raise. Beckman's two-axis judge (node legitimacy 92.2% vs edge-direction 30.8%) shows judges can be reliable on one axis and useless on another.

## Connections

- Powers the automated tier of [[Online Evaluation]].
- [[Eval Awareness]] / [[Sandbagging]] — judged models can detect and game the judge.
- [[AI-Resistant Evaluation Design]] — designing tasks judges can't be fooled on.

## Open questions

> [!gap] Do online (live-traffic) judges drift faster than offline judges, since the input distribution shifts continuously? No published characterization.

## Sources

- [[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]]
