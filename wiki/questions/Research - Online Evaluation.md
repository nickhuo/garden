---
type: synthesis
title: "Research - Online Evaluation"
created: 2026-05-20
updated: 2026-05-20
tags: [research, ai-agents, llm, evaluation]
status: developing
related:
  - "[[Online Evaluation]]"
  - "[[LLM-as-Judge]]"
  - "[[Implicit Feedback Signals]]"
  - "[[Reward Modeling]]"
  - "[[A/B Testing for Agents]]"
  - "[[Eval Validity]]"
sources:
  - "[[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]]"
  - "[[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]]"
---

# Research - Online Evaluation

## Overview

Offline benchmarks tell you whether a model is good for a *population*; they cannot tell you whether the sentence it just produced landed for *this* user. Online evaluation closes that gap by turning live behavior into a learning signal in real time. It spans a spectrum from cheap/observational ([[Implicit Feedback Signals]]) through controlled-exploration (interleaving, contextual bandits) to slow/causal ([[A/B Testing for Agents]]), with [[LLM-as-Judge]] scoring live traffic and [[Reward Modeling]] turning preference into policy updates. The whole stack rests on [[Eval Validity]]: every online signal is a proxy.

## Key Findings

- **A strong LLM judge matches human agreement (>80%, equal to human-human) — but only after biases are controlled.** (high confidence — [[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]], replicated.) Position-bias swaps alone can move pairwise accuracy >10%.
- **Chatbot Arena is the canonical LLM-era online-eval platform**: live user prompts, anonymous pairwise votes, Elo aggregation — real intent, fresh distribution. MT-Bench is its frozen offline twin. (high confidence — same source.)
- **Implicit feedback is the most abundant online signal but is structurally biased**; position bias, off-policy/counterfactual gaps, and the need for propensity correction were solved in IR/recsys (interleaving, contextual bandits, CRM). (medium confidence — IR/recsys literature; transfer to conversational agents not yet formally validated.)
- **A/B testing is the only causally trustworthy verdict**, and most failures are validity failures (SRM, novelty effects, OEC choice), not statistical ones. (high confidence — online-controlled-experiment practice.)
- **Online/iterative reward learning (online DPO, RLAIF) keeps the reward signal on-distribution** by regenerating and re-scoring each round; DPO collapses the explicit RM into an implicit one. (medium confidence — active 2024 research.)
- **The metric is the construct.** Apparent capability jumps can be metric artifacts ([[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]]); any single benchmark/leaderboard number is low confidence until its metric is examined. (high confidence.)

## How online eval bridges real-time learning ↔ persistent memory

Online evaluation is the conduit from a single live interaction to a durable change in the system. An implicit signal (user edited the draft heavily, re-prompted, abandoned) or an explicit one (pairwise vote) is scored — by a judge or a reward model — and that score updates something that persists: retrieval/KB priority, the eval rubric, the policy, or the user-specific persona/memory. Nick's offline golden-dataset + dual-judge rigor is the *base* that defines "good"; online eval is the *live extension* that keeps "good" calibrated to the actual user. [[A/B Testing for Agents]] is the gate that decides whether an observed online lift is real enough to persist.

## Key Entities

- **Chatbot Arena / LMSYS** — live pairwise online-eval platform (linked via source, not a separate entity page).
- **OpenAI** — InstructGPT/RLHF reward modeling lineage (linked, owned elsewhere).

## Key Concepts

[[Online Evaluation]] · [[LLM-as-Judge]] · [[Implicit Feedback Signals]] · [[Reward Modeling]] · [[A/B Testing for Agents]] · [[Eval Validity]] · [[Agent Eval Pyramid]] · [[Trace-Based Evaluation]] · [[Eval Awareness]]

## Contradictions

- **LLM-as-judge reliability is contested.** Zheng et al. report >80% human agreement (judge is trustworthy at scale); the bias literature (position/verbosity/self-enhancement/authority) and Nick's Compass **8.9pp** judge-swing show the same judge can be unreliable on a specific axis. Resolution: the judge is reliable *in aggregate, after debiasing and calibration*, and unreliable *per-axis, blind*. Not a true contradiction — a scope distinction.
- **Sensitivity vs. causality.** Interleaving/bandits give high sensitivity cheaply but are observational; A/B is causal but slow. Neither dominates; they compose (explore then confirm).

## Open Questions

> [!gap] Conversational analog of position bias in implicit feedback, and its correction.

> [!gap] Confidence threshold before an online signal updates persisted memory vs. requires A/B confirmation.

> [!gap] Detecting online reward-hacking (engagement-via-frustration) before it harms long-term value.

> [!gap] A/B testing agents with cross-arm memory carryover that violates independence.

## Sources

- [[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]]
- [[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]]
- [[2022 - Ouyang et al - InstructGPT]] (RLHF/reward modeling — owned elsewhere, linked)
