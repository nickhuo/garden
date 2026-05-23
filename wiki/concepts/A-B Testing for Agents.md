---
type: concept
title: "A/B Testing for Agents"
created: 2026-05-20
updated: 2026-05-23
aliases: ["A/B Testing for Agents"]
tags: [ai-agents, llm, evaluation, ab-testing, experimentation]
status: developing
related:
  - "[[Online Evaluation]]"
  - "[[Implicit Feedback Signals]]"
  - "[[Online Evaluation Bottlenecks]]"
  - "[[Continuous Evaluation]]"
sources: []
---

# A/B Testing for Agents

## Summary

An A/B test (online controlled experiment) randomly assigns live users to a control and a treatment arm, changes one variable (prompt, policy, model, retrieval config, persona), and measures the difference in an outcome metric. Randomization is what makes the result **causal** — the one guarantee offline evaluation and observational [[Implicit Feedback Signals]] cannot provide.

## Why it matters

It is the trustworthy, causal end of [[Online Evaluation]]: the verdict on whether a change *actually* improved the experience, not just correlated with a metric move. For agents this is the gate that promotes a prompt/policy change from "looks better in the dashboard" to "ship it."

## Limits

- **Slow and traffic-hungry** — needs enough users and time for significance; conversational outcomes are noisy.
- **OEC choice is everything** — optimizing thumbs-up or session length can reward the wrong behavior; the metric must causally track long-term value.
- **Pitfalls**: Sample Ratio Mismatch, novelty/primacy effects, Twyman's law, cross-arm leakage (especially when arms share a memory store).
- **Interleaving** is far more sensitive at the same traffic but applies cleanly only to ranked outputs.

## Production practice (2026 industry guidance)

Concrete discipline now documented by eval vendors (vendor sources — medium confidence):

- **Sample size is much larger for agents.** Quality-metric A/B tests "typically need **10,000+ trajectories per arm**" (vs thousands traditionally) because LLM stochasticity means *variation is the signal you're measuring*, not noise. Run power analysis *before* testing.
- **Pre-register the OEC.** Post-hoc metric switching is "the single most common form of p-hacking in agent evaluation." Define **guardrail metrics** (safety, latency) that must not degrade even if the primary metric improves.
- **Accept the null when inconclusive.** Shipping a p=0.18 result ≈ a 1-in-5 chance of shipping a regression; over four such decisions you expect ~one regression.
- **Segment before discarding.** A flat overall result can hide a clean win on one segment (e.g. +5 points on long-context queries) → ship for that segment only.
- **Typical duration:** one to three weeks, run to the pre-set sample size (not "until it looks significant").

## Connection to prior work

Inherited directly from web experimentation (Microsoft/Google/LinkedIn). Nick's Donut shadow→canary→prod gating is staged controlled rollout — a disciplined applied OCE that catches regressions before full traffic exposure.

## Connections

- The causal-confirmation layer above [[Implicit Feedback Signals]] and bandits in [[Online Evaluation]].

## Open questions

> [!gap] How to A/B test an agent whose persisted memory persists *across* arm boundaries, creating carryover that violates the independence assumption?

> [!gap] **Baseline drift** (raised in 2026 practice): even with no variant change, the underlying model, retrieval index, or tool definitions move during the test window — "a test that runs for two weeks against a moving baseline tells you very little." How to run valid online experiments against a non-stationary baseline is unresolved. See [[Online Evaluation Bottlenecks]].

> [!gap] Low-traffic products may never reach the 10,000-trajectory/arm bar — what is the trustworthy fallback when A/B significance is unreachable?
