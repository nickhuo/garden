---
type: concept
title: "Capability Phase Transitions"
created: 2026-05-28
updated: 2026-05-28
tags: [llm, evaluation, interpretability]
status: seed
related:
  - "[[Order Parameters for Capability Transitions]]"
  - "[[Eval Validity]]"
  - "[[Adaptive Evaluation]]"
sources:
  - "[[2026-05-17 - Lun Wang - Your Evals Will Break]]"
  - "[[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]]"
---

# Capability Phase Transitions

## Summary

The idea that an LLM's capabilities can change **qualitatively** — not just incrementally — as scale, training, or context cross some boundary, by analogy to **phase transitions** in physics. Three regimes are debated:

- **Emergent abilities** (Wei et al., 2022) — capabilities that appear sharply and unpredictably at scale.
- **Mirage** ([[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]]) — the sharpness is largely a **metric artifact**; smooth metrics dissolve the cliff. "Emergence" is partly in the ruler, not the model.
- **Grokking** (Power et al., 2022; Liu et al., 2022) — delayed generalization: a model memorizes, then *much later* in training snaps to generalizing. A real, mechanistically-studied transition (Nanda et al., 2023).

## Why it matters

[[2026-05-17 - Lun Wang - Your Evals Will Break]] hangs its whole argument here: **whether a transition is real (emergence/grokking) or illusory (mirage), an eval built for the prior regime gives the wrong reading at the boundary.** The point isn't to settle the emergence debate — it's that *either way* the measurement infrastructure is the weak link. This is why detecting the transition needs an [[Order Parameters for Capability Transitions|order parameter]], and why static [[Eval Validity]] (the metric distorts what you see *now*) must be extended dynamically (the metric's validity *expires* at a boundary).

## Limits / open questions

- No agreed operational definition of a "regime" for LLMs — the physics analogy is suggestive, not yet rigorous.
- Mirage vs. emergence is metric-dependent, so "is this a real transition?" is partly unanswerable without fixing the metric first (the Schaeffer trap).
- Grokking is established on small algorithmic tasks; whether large-model capability jumps are the *same* phenomenon is unproven.
