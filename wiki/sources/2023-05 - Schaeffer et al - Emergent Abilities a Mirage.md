---
type: source
title: "Are Emergent Abilities of Large Language Models a Mirage?"
source_type: paper
author: "Rylan Schaeffer, Brando Miranda, Sanmi Koyejo (Stanford)"
date_published: 2023-05-15
url: https://arxiv.org/abs/2304.15004
created: 2026-05-20
updated: 2026-05-20
status: mature
confidence: high
tags: [ai-agents, llm, evaluation, eval-validity, construct-validity]
key_claims:
  - "Apparent 'emergent abilities' are largely an artifact of the evaluation metric, not a genuine property of the model."
  - "Discontinuous/nonlinear metrics (exact-match, all-or-nothing) manufacture sharp jumps; switching to smooth metrics makes the jump disappear."
  - "Construct validity of a benchmark is a measurement choice — the same model looks 'emergent' or 'smooth' depending on the metric you pick."
related:
  - "[[Eval Validity]]"
  - "[[Online Evaluation]]"
  - "[[AI-Resistant Evaluation Design]]"
sources: []
---

# Are Emergent Abilities a Mirage? (Schaeffer et al., 2023)

NeurIPS 2023 (arXiv 2304.15004). A construct-validity critique of LLM benchmarking. >3yr old but its argument is foundational and load-bearing for any eval design.

## Core argument

"Emergent abilities" — sharp, unpredictable capability jumps at scale — are largely **a mirage created by the choice of metric**, not a real discontinuity in the model. Harsh, nonlinear, all-or-nothing metrics (exact-match on a multi-token answer) convert smooth underlying improvement into an apparent step function. Swap to a smooth, per-token metric and the cliff disappears. 92% of observed "emergence" sat in BIG-Bench tasks scored with such metrics.

## The transferable lesson: the metric IS the construct

What you measure is not neutral. A benchmark number is a joint statement about the model *and* your scoring choice. This is the eval-validity warning that underlies everything in [[Online Evaluation]]: an online metric (thumbs-up, dwell, completion) is a *proxy* for "did this land," and the proxy can manufacture or hide effects exactly as exact-match manufactured emergence.

## Why it matters for agents

- Justifies treating any single benchmark/leaderboard number as **low-confidence** until the metric and its construct validity are examined.
- Directly motivates Nick's hard-won lessons: the Compass dual-judge 8.9pp swing and the Beckman 30.8% edge-direction collapse are both cases where the *metric choice* (not the model) drove the headline — "eval before believing."
- For online eval, the corollary: choose the OEC carefully so the proxy moves only when real value moves.
