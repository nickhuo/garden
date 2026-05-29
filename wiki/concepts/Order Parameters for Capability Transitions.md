---
type: concept
title: "Order Parameters for Capability Transitions"
created: 2026-05-28
updated: 2026-05-28
tags: [llm, evaluation, interpretability]
status: seed
related:
  - "[[Capability Phase Transitions]]"
  - "[[Adaptive Evaluation]]"
  - "[[Eval Validity]]"
sources:
  - "[[2026-05-17 - Lun Wang - Your Evals Will Break]]"
---

# Order Parameters for Capability Transitions

## Summary

An **order parameter** is, in statistical mechanics, a macroscopic quantity that changes value when a system crosses a **phase transition** (e.g. magnetization flipping at the Curie point). [[2026-05-17 - Lun Wang - Your Evals Will Break]] argues LLM evaluation has **no analogue**: we have no macroscopic signal that flips when a model crosses into a new capability regime. Existing benchmarks (GPQA, SWE-bench, ARC-AGI, Humanity's Last Exam) measure *present* capability and give only weak evidence about *post-transition* behavior.

## Why it matters

This is the named gap behind the wiki's eval skepticism. Without an order parameter, eval is **reactive** — it can only confirm a shift *after* it has happened (see [[Adaptive Evaluation]]). Finding one would let you *anticipate* a capability jump rather than discover it in deployment.

Wang's proposed toolkit for constructing such parameters:

- **Statistical mechanics** — Shan, Li & Sompolinsky (PNAS 2026), *Order Parameters and Phase Transitions of Continual Learning* — the most direct attempt to define order parameters for a learning system.
- **Mechanistic interpretability** — Nanda et al. (ICLR 2023), *Progress Measures for Grokking via Mechanistic Interpretability* — "progress measures" are an early example of an internal quantity that tracks a transition the loss curve hides.

## The practical substitute

Lacking a true order parameter, [[Adaptive Evaluation]] watches **meta-signals** instead: shifts in score *distributions* and in *correlations between metrics*. These are the engineering proxy for "the system has changed regime."

## Limits / open questions

- Whether any single scalar order parameter exists for something as high-dimensional as LLM capability is unknown — it may be irreducibly multi-dimensional.
- Internal (interpretability-derived) signals require white-box access; closed deployed models may have to rely on behavioral meta-signals only.
