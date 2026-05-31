---
type: concept
title: Multi-Stage Decoding
created: 2026-05-31
updated: 2026-05-31
tags:
  - llm
  - inference
  - systems
status: developing
related:
  - "[[Stage-Decoupled Inference Architecture]]"
  - "[[Thinker-Talker-MTP]]"
  - "[[SGLang]]"
  - "[[Qwen3-Omni]]"
sources:
  - "[[2026-05-30 - Chayenne Zhao - SGLang Omni Multi-Stage Inference]]"
---

# Multi-Stage Decoding

## Summary

A **classification axis for inference systems**: divide generative models not by modality but by whether their *decoding process* is single-stage or multi-stage.

- **Single-stage** — one autoregressive (or one denoising) decode loop from start to finish. Standard LLM/VLM decode; ASR (audio→text); pure diffusion image models. Already well-served by single-Scheduler engines like [[SGLang]] main / SGLang Diffusion.
- **Multi-stage** — end-to-end decoding split into **multiple heterogeneous stages that alternate**, each with distinct computational character. Examples: [[Qwen3-Omni]] (Thinker→Talker→MTP), TTS models (Fish S2 Pro's Dual-AR, Qwen3-TTS, Voxtral, Higgs), omni-output models (Ming Omni, LLaDA Uni). This is the regime [[Stage-Decoupled Inference Architecture]] is built for.

The point of the axis ([[Chayenne Zhao]]): **slice by computation, not modality.** Modality is the model's outward packaging; an inference engine cares about the compute. The same diffusion image generator is single-stage standalone but is *one stage* inside Ming Omni — category is set by the surrounding computation, not the technique. Heuristic: **audio output ⇒ usually multi-stage** (speech gen ≈ AR backbone + codec completion).

## The three shared computational characteristics

What multi-stage models have in common — and what each demands from the framework (see [[Stage-Decoupled Inference Architecture]] for the mechanisms):

1. **Heterogeneous compute paradigms.** Stages differ widely in compute intensity, memory-access pattern, and latency tolerance. In [[Thinker-Talker-MTP]]: Thinker prefill is **compute-bound** (saturate matmuls), Thinker decode is **memory-bound** (KV-cache bandwidth dominates), and Talker+MTP is a **third category — latency-bound yet neither compute- nor memory-bound** (per-step ops too light to hit either ceiling; kernel-launch and sync overhead dominate). Stuffing all three into one scheduler lets each degrade the others.
2. **Divergent dependency patterns.** Plain LLM inference has one unidirectional producer→consumer link (prefill produces KV, decode consumes it). Multi-stage has at least two: **async-decoupled** (Thinker→Talker via a shared buffer, consume at own pace) and **sync-tightly-coupled** (Talker↔MTP, where Talker's next step strictly waits on MTP's write-back).
3. **Cross-stage memory contention.** Multiple stages' weights are resident at once (Thinker + Talker), plus Thinker prefix cache, encoder long-sequence activations, the Talker↔MTP feedback buffer, Talker's own KV cache. "Remaining available memory" stops being a single global number and varies per step.

## The novel bit: a third roofline category

Compute-bound vs memory-bound is textbook (the roofline / prefill-vs-decode story). The contribution here is naming a **third regime** that some decode stages fall into: very light per-step compute *and* light memory traffic, but a tight inter-step feedback dependency — so the bottleneck is **launch + synchronization overhead**, addressed by collapsing the stage boundary into a piecewise CUDA Graph rather than by more FLOPs or more bandwidth.

## Connections

- Solution pattern: [[Stage-Decoupled Inference Architecture]]
- Canonical instance: [[Thinker-Talker-MTP]] · model: [[Qwen3-Omni]] · engine: [[SGLang]]
- Cousin design: [[Interaction Model Architecture]] (TML) — also separates a latency-bound stage from heavier ones, also treats streaming as an infra problem; multi-stage decoding generalizes the split to N stages.
- KV-cache bottleneck in the memory-bound decode stage relates to [[KV-Cache Discipline]] (the agent-side framing of the same scarcity).

## Open questions

- Is "single- vs multi-stage" a durable axis, or will future models blur it (e.g., learned dynamic stage counts)?
- How does the taxonomy interact with prefill/decode disaggregation already common in single-stage serving — is a multi-stage pipeline just disaggregation taken to N heterogeneous stages?
- Where does diffusion-as-a-stage sit on the compute/memory/latency triangle (a stated WIP for SGLang Omni)?
