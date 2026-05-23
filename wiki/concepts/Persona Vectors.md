---
type: concept
title: "Persona Vectors"
created: 2026-05-20
updated: 2026-05-20
tags: [llm, ai-agents, memory, persona-vectors, interpretability, alignment]
status: developing
related: ["[[Activation Steering / Representation Engineering]]", "[[Memory Stream]]", "[[Persona Vectors vs Memory Files]]", "[[Self-Editing Memory]]"]
sources: ["[[2025-07-29 - Chen et al - Persona Vectors]]", "[[2023-10-12 - Zou et al - Representation Engineering]]"]
---

## Summary

A **persona vector** is a linear direction in a language model's activation space that encodes a high-level character trait — e.g. evil, sycophancy, hallucination propensity (Source: [[2025-07-29 - Chen et al - Persona Vectors]], high confidence). It is extracted automatically: take a plain-English trait description, generate trait-eliciting vs trait-suppressing prompt pairs, and take the difference of mean activations. The vector is causal — injecting it induces the behavior; subtracting it suppresses it.

This is the "**learned state that conditions the model**" path to persistence: what the system should be, encoded in a form the model directly consumes, rather than in a text file it must re-read.

## Why it matters

For agent applications, persona vectors give a control + monitoring surface for *who the agent is* across sessions, separate from *what the agent knows* (the memory-files path). Three uses (high confidence): real-time **monitoring** of persona drift; inference-time **steering**; and **preventative steering** during finetuning that inoculates against bad persona acquisition while preserving MMLU. A fourth use audits training data by projecting it onto the vectors.

## Limits

> [!gap] Inference-time subtraction degrades capability (preventative steering avoids this). Linear-direction assumption may break for compositional/context-dependent traits. Coverage is bounded by which traits you define and probe — you cannot monitor a trait you did not think to name.

## Connection to prior work

Specializes Representation Engineering (Source: [[2023-10-12 - Zou et al - Representation Engineering]]) — same contrast-vector machinery, applied to character traits and the finetuning pipeline. Opposite pole from the textual [[Memory Stream]]. See [[Persona Vectors vs Memory Files]].

Maps onto Nick's Beckman work: the per-learner coefficients `(A, B, C)` in `PL = C + A·Ease + B·Novelty` are a hand-built, fully interpretable persona-vector analogue — a small learned state that conditions rendering. Persona vectors are the model-internal, less-inspectable version of the same lever.

## Connections

- [[Activation Steering / Representation Engineering]] — the underlying method
- [[Persona Vectors vs Memory Files]] — the two-paths comparison
- [[Self-Editing Memory]] — the textual counterpart agents edit themselves
- [[brain/03_Resources/digest/sources/anthropic]] — origin of the persona-vectors paper

## Open questions

- Do persona vectors compose, or do traits interfere?
- Can per-user persona vectors be a deployable, inspectable agent-personalization layer (Beckman-style)?

## Sources

- [[2025-07-29 - Chen et al - Persona Vectors]]
- [[2023-10-12 - Zou et al - Representation Engineering]]
