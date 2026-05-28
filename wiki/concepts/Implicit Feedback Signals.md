---
type: concept
title: "Implicit Feedback Signals"
created: 2026-05-20
updated: 2026-05-28
tags: [ai-agents, llm, evaluation, real-time-learning, implicit-feedback, rlhf, bandits]
status: developing
related:
  - "[[Online Evaluation]]"
  - "[[Reward Modeling]]"
  - "[[A/B Testing for Agents]]"
  - "[[Online Learning from Interaction]]"
  - "[[In-Context Learning]]"
  - "[[Test-Time Adaptation]]"
sources:
  - "[[2025-05-21 - Meta - Reinforcement Learning from User Feedback]]"
  - "[[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]"
---

# Implicit Feedback Signals

## Summary

Implicit feedback is behavioral signal users generate **without being asked to rate anything**: clicks, dwell time, accept/reject of a suggestion, edits to generated output, retries, follow-up questions, copy actions, direction changes, and abandonment. For agents the high-signal implicit events are **whether the user accepted the answer, edited it (and how much), re-prompted, or walked away**. It is the most abundant online signal because every interaction produces it, in contrast to sparse explicit votes.

It serves two roles at once: as the cheap, always-on substrate of [[Online Evaluation]] (measure quality from live behavior), and as the **reward stream for real-time learning** (update the model from that behavior). Meta's RLUF shows these production signals can train preference/reward models competitive with explicit human ratings, enabling continuous improvement from live traffic (confidence: medium — single source; [[2025-05-21 - Meta - Reinforcement Learning from User Feedback]]). This is the digital-product instance of [[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]'s **grounded reward** (confidence: high for the principle).

## Signal taxonomy

- **Correction** — user fixes the output: strong negative on the original, positive on the fix.
- **Follow-up / continuation** — engagement; weak positive.
- **Direction change** — the prior trajectory was wrong: negative.
- **Silence / no correction** — weak positive (didn't need fixing) — but ambiguous.
- **Abandonment** — strong negative.

## As an evaluation signal

The raw material that, aggregated, tells you whether outputs land for real users. An edit-distance on a generated draft, a retry rate, or a tool-call abandonment is a direct proxy for quality that no offline golden dataset captures. A/B testing ([[A/B Testing for Agents]]) is the causal confirmation layer for trends seen in implicit signal.

## As a learning signal

Explicit feedback (thumbs, ratings) is sparse and biased toward extremes. Implicit signals are abundant and free, collected passively — the only feedback available at production scale for most agents. For [[Online Learning from Interaction]] they are the actual reward stream; the same signal can re-condition the prompt immediately ([[In-Context Learning]]) or, with more durability, update memory or weights ([[Test-Time Adaptation]]). It also feeds online preference learning ([[Reward Modeling]]).

## Limits — bias is the central problem

The information-retrieval/recsys literature spent two decades on this:

- **Position / presentation bias** — users click what is shown prominently, not what is best. Naive use of clicks as a quality label yields suboptimal ranking (Joachims; Chapelle & Joachims 2012).
- **Counterfactual / off-policy problem** — logged feedback only covers what the *current* policy showed; estimating how an alternative would have done requires propensity weighting (Counterfactual Risk Minimization, off-policy evaluation). (medium confidence — IR/recsys results, transfer to agents not yet formally validated.)
- **Interleaving** (team-draft, optimized interleaving — Radlinski; Chapelle et al. 2012) blends two systems' outputs in one list and attributes clicks, giving far higher sensitivity than A/B at the same traffic — but applies cleanly to *ranked lists*, less obviously to free-form agent turns.
- **Contextual bandits** turn implicit feedback into an online learning loop with controlled exploration, trading off exploiting the best-known action vs. exploring to learn.

Learning-side confounds compound these: **engagement ≠ correctness** (satisfied users also disengage; clicks can be optimized at the cost of truthfulness — [[Reward Hacking]]); **attribution** is hard for delayed signals; and **explicit feedback still wins** for safety-critical or rare-but-important cases where you cannot afford to learn the wrong lesson from noisy proxies.

## Connection to prior work

Position-bias correction, interleaving, counterfactual/off-policy evaluation, and contextual bandits all come from search and recommendation, where implicit feedback has always been the dominant signal. The learning side sits in the RLHF lineage (preference modeling) but swaps annotator labels for behavioral signals. The open frontier is porting both to **conversational agents**, where the "result list" is a single generated turn and the position-bias analog is conversational framing.

## Connections — Nick's projects

- **Donut:** confidence gating *is* implicit-feedback discipline — only high-confidence neighbors write back, the data-layer version of "only update on trustworthy signal." Nick's lesson — "instrument the retrieval step from day one" — is precisely the discipline of capturing implicit signal at every step before you need it.
- **Compass:** user logs are implicit/explicit feedback fed into KB priority and eval rubric — a governed closed loop that decides which signals are allowed to change policy.
- **Sonic:** the streaming substrate that makes implicit signals capturable in near-real-time at all.

## Open questions

> [!gap] What is the conversational analog of position bias, and how do you correct for it in a single-turn agent response?

> [!gap] Edit-distance-as-quality assumes the user fixes toward "correct" — but users also edit toward personal style. How to separate quality-edits from preference-edits (and satisfied-silence from confused-silence)?

- Which signals are safe to auto-update on vs. require a human gate?

## Sources

- [[2025-05-21 - Meta - Reinforcement Learning from User Feedback]] — production implicit signals train reward models competitive with explicit ratings
- [[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]] — grounded reward as the "why now"
- Chapelle, Joachims, Radlinski, Yue — interleaved search evaluation (ACM TOIS 2012)
