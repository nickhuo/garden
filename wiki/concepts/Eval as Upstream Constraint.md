---
type: concept
title: "Eval as Upstream Constraint"
created: 2026-05-28
updated: 2026-05-28
tags: [ai-agents, llm, evaluation]
status: seed
related:
  - "[[Eval Validity]]"
  - "[[Adaptive Evaluation]]"
  - "[[Verifiability]]"
sources:
  - "[[2026-05-17 - Lun Wang - Your Evals Will Break]]"
---

# Eval as Upstream Constraint

## Summary

The load-bearing claim of [[2026-05-17 - Lun Wang - Your Evals Will Break]]: **evaluation sits upstream of training, safety, and scaling.** *"If you can evaluate correctly, you can train correctly. Training is optimization, and optimization is only as good as its objective."* The eval *is* the objective; a misaligned eval propagates downstream into every training signal, safety metric, and scaling decision. Hence Wang's headline: eval — not compute, data, or architecture — is the bottleneck for the next capability jump.

## Goodhart breaks at phase boundaries

The sharp version of the claim. A proxy metric that tracked the true goal within one capability regime can **decouple** from it once the model crosses into a new regime — the same proxy, newly invalid. This is the *dynamic* form of the proxy-drift / Goodhart failure mode already listed on [[Eval Validity]]: there it's a static distortion ("the metric is the construct"); here it's a *time bomb* that detonates at a [[Capability Phase Transitions|capability transition]].

## Why it matters

- Reframes eval from a *reporting* activity (measure the finished model) to a *steering* activity (the thing that bounds how good training can get). Aligns with Karpathy's [[Verifiability]] thesis — "LLMs automate what you can verify" — eval *is* the verification layer, so it caps the achievable.
- Motivates investing in [[Adaptive Evaluation]] as a *capability* lever, not just a QA cost.
- Reinforces the wiki's standing practice of treating any single benchmark number as low-confidence: if the eval is upstream of training, a bad eval doesn't just mismeasure — it *misbuilds*.

## Limits / open questions

- The "train correctly iff evaluate correctly" claim is an argument, not a result — it has no empirical demonstration in the post (the source is benchmark-free).
- It assumes the objective is the dominant constraint; in practice data quality and optimization dynamics also bind. The claim is best read as "eval is *an under-weighted* upstream constraint," not the sole one.
