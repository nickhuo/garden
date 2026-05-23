---
type: concept
title: "Implicit Feedback Signals"
created: 2026-05-20
updated: 2026-05-20
tags: [ai-agents, llm, evaluation, implicit-feedback, bandits]
status: developing
related:
  - "[[Online Evaluation]]"
  - "[[Reward Modeling]]"
  - "[[A/B Testing for Agents]]"
sources: []
---

# Implicit Feedback Signals

## Summary

Implicit feedback is behavioral signal users generate without being asked: clicks, dwell time, accept/reject of a suggestion, edits to generated output, retries, follow-up questions, copy actions, and abandonment. For agents the high-signal implicit events are **whether the user accepted the answer, edited it (and how much), re-prompted, or walked away**. It is the most abundant online-evaluation signal because every interaction produces it, in contrast to sparse explicit votes.

## Why it matters

Implicit signal is the cheap, always-on substrate of [[Online Evaluation]] — the raw material that, aggregated, tells you whether outputs land for real users. An edit-distance on a generated draft, a retry rate, or a tool-call abandonment is a direct proxy for quality that no offline golden dataset captures. It is also the feed for online preference learning ([[Reward Modeling]]).

## Limits — bias is the central problem

The information-retrieval/recsys literature spent two decades on this:

- **Position / presentation bias** — users click what is shown prominently, not what is best. Naive use of clicks as a quality label yields suboptimal ranking (Joachims; Chapelle & Joachims 2012).
- **Counterfactual / off-policy problem** — logged feedback only covers what the *current* policy showed; estimating how an alternative would have done requires propensity weighting (Counterfactual Risk Minimization, off-policy evaluation). (medium confidence — IR/recsys results, transfer to agents not yet formally validated.)
- **Interleaving** (team-draft, optimized interleaving — Radlinski; Chapelle et al. 2012) blends two systems' outputs in one list and attributes clicks, giving far higher sensitivity than A/B at the same traffic — but applies cleanly to *ranked lists*, less obviously to free-form agent turns.
- **Contextual bandits** turn implicit feedback into an online learning loop with controlled exploration, trading off exploiting the best-known action vs. exploring to learn.

## Connection to prior work

Position-bias correction, interleaving, counterfactual/off-policy evaluation, and contextual bandits all come from search and recommendation, where implicit feedback has always been the dominant signal. The open frontier is porting them to **conversational agents**, where the "result list" is a single generated turn and the position-bias analog is conversational framing. Nick's Donut lesson — "instrument the retrieval step from day one" — is precisely the discipline of capturing implicit signal at every step before you need it.

## Connections

- Feeds [[Online Evaluation]] and [[Reward Modeling]].
- A/B testing ([[A/B Testing for Agents]]) is the causal confirmation layer for trends seen in implicit signal.

## Open questions

> [!gap] What is the conversational analog of position bias, and how do you correct for it in a single-turn agent response?

> [!gap] Edit-distance-as-quality assumes the user fixes toward "correct" — but users also edit toward personal style. How to separate quality-edits from preference-edits?

## Sources

- Chapelle, Joachims, Radlinski, Yue — interleaved search evaluation (ACM TOIS 2012)
