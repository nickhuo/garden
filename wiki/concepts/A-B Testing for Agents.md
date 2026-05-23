---
type: concept
title: "A/B Testing for Agents"
created: 2026-05-20
updated: 2026-05-20
aliases: ["A/B Testing for Agents"]
tags: [ai-agents, llm, evaluation, ab-testing, experimentation]
status: seed
related:
  - "[[Online Evaluation]]"
  - "[[Implicit Feedback Signals]]"
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

## Connection to prior work

Inherited directly from web experimentation (Microsoft/Google/LinkedIn). Nick's Donut shadow→canary→prod gating is staged controlled rollout — a disciplined applied OCE that catches regressions before full traffic exposure.

## Connections

- The causal-confirmation layer above [[Implicit Feedback Signals]] and bandits in [[Online Evaluation]].

## Open questions

> [!gap] How to A/B test an agent whose persisted memory persists *across* arm boundaries, creating carryover that violates the independence assumption?
