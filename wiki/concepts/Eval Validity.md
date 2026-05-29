---
type: concept
title: "Eval Validity"
created: 2026-05-20
updated: 2026-05-20
tags: [ai-agents, llm, evaluation, eval-validity, construct-validity]
status: seed
related:
  - "[[Online Evaluation]]"
  - "[[LLM-as-Judge]]"
  - "[[AI-Resistant Evaluation Design]]"
  - "[[Eval as Upstream Constraint]]"
  - "[[Capability Phase Transitions]]"
sources:
  - "[[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]]"
  - "[[2026-05-17 - Lun Wang - Your Evals Will Break]]"
---

# Eval Validity

## Summary

Eval validity asks whether a metric actually measures the thing you care about (construct validity), not just whether it produces a number. The headline result is [[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]]: "emergent abilities" are largely an artifact of nonlinear metric choice — change the metric and the effect vanishes. **The metric is part of the construct.**

## Why it matters

Every online-evaluation signal is a proxy, so eval validity is the precondition for trusting any [[Online Evaluation]] number. A leaderboard score, a judge score, or a thumbs-up rate is a joint claim about the system *and* the measurement; a badly chosen metric manufactures or hides effects. This is why LLM benchmark/leaderboard claims are treated as **low confidence** until the metric is examined.

## Limits / failure modes

- **Metric artifacts** — discontinuous metrics fake sharp jumps (Schaeffer).
- **Benchmark contamination/gaming** — training on test data, or [[Eval Awareness]] where a model detects and games the eval.
- **Proxy drift** — the proxy and the true goal diverge over time under optimization (Goodhart). [[2026-05-17 - Lun Wang - Your Evals Will Break]] sharpens this to its *dynamic* form: validity isn't just distorted, it **expires** at a [[Capability Phase Transitions|capability boundary]] — "Goodhart breaks at phase boundaries." See [[Eval as Upstream Constraint]].

## Connection to prior work

Nick's projects are case studies in invalidity caught early: the Compass dual-judge **8.9pp swing** (metric choice = judge identity drove the headline) and the Beckman **30.8% edge-direction accuracy** that forced a construction-method pivot — "eval before believing." Both show the metric, not the model, was the variable.

## Connections

- The validity check underlying [[Online Evaluation]], [[LLM-as-Judge]], and [[Agent Eval Pyramid]].

## Open questions

> [!gap] What is a practical construct-validity checklist for a *conversational* online metric (e.g. "did this land")?

## Sources

- [[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]]
