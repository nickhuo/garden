---
type: source
title: "Representation Engineering: A Top-Down Approach to AI Transparency"
created: 2026-05-20
updated: 2026-05-20
tags: [llm, ai-agents, memory, persona-vectors, interpretability, alignment]
status: developing
source_type: paper
author: Andy Zou et al. (Center for AI Safety and collaborators)
date_published: 2023-10-12
url: https://arxiv.org/abs/2310.01405
confidence: high
related: ["[[Activation Steering / Representation Engineering]]", "[[Persona Vectors]]"]
sources: []
key_claims:
  - "RepE is a top-down interpretability approach centering population-level representations rather than individual neurons or circuits (Hopfieldian view)."
  - "Linear Artificial Tomography (LAT) extracts reading vectors — concept directions — from activations across contrasting stimuli."
  - "Control uses contrast/steering vectors injected at inference to amplify or suppress a concept without retraining."
  - "Applies to honesty, harmlessness, power-seeking; raises TruthfulQA accuracy substantially."
---

## Summary

Zou et al. (2023) propose **Representation Engineering (RepE)**: rather than reverse-engineering circuits bottom-up, treat population-level representations as the primary unit and find linear directions for high-level concepts via Linear Artificial Tomography (high confidence). **Reading** locates a concept direction; **control** injects a contrast/steering vector into the residual stream at inference to steer behavior, no weight update (high).

## Key claims

- Concept directions are causal handles: steering along honesty/truthfulness directions raises TruthfulQA accuracy (high).
- The same machinery generalizes across safety-relevant traits — honesty, harmlessness, power-seeking (high).

## Limits

> [!gap] Authors frame it as initial analysis. Linear-direction assumption; steering can trade off capability; concept coverage is bounded by what you probe for.

## Connection to prior work

Direct ancestor of persona vectors (Source: [[2025-07-29 - Chen et al - Persona Vectors]]), which specialize RepE to character traits and the finetuning loop. The foundational citation for the "learned-state / activation-steering" path of persistent conditioning.

## Sources

- [[Activation Steering / Representation Engineering]]
- arXiv:2310.01405
