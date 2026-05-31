---
type: entity
title: Qwen3-Omni
entity_type: model
created: 2026-05-31
updated: 2026-05-31
tags:
  - llm
  - inference
  - multimodal
status: seed
related:
  - "[[Thinker-Talker-MTP]]"
  - "[[Multi-Stage Decoding]]"
  - "[[SGLang]]"
sources:
  - "[[2026-05-30 - Chayenne Zhao - SGLang Omni Multi-Stage Inference]]"
---

# Qwen3-Omni

Alibaba Qwen team's omni-modal model: inputs of voice + text + video + image, outputs of **text + voice**. In the Qwen definition, an "Omni" model supports audio input *and* audio output (contrast MiMo Omni / Nemotron Omni, which only take audio in).

## Why it matters here (the canonical multi-stage model)

Qwen3-Omni is [[2026-05-30 - Chayenne Zhao - SGLang Omni Multi-Stage Inference|SGLang Omni]]'s running example of [[Multi-Stage Decoding]]. Its end-to-end decode is **not** one AR loop but an alternation of heterogeneous stages — the [[Thinker-Talker-MTP]] pipeline:

- **Thinker** — AR text generation; a VLM-with-audio-encoder. Compute-bound prefill, memory-bound decode.
- **Talker** — AR backbone emitting the 0-th codec token per timestep. Latency-bound, light per-step compute.
- **MTP** — completes the remaining codec tokens for the timestep in parallel, writes embeddings back to Talker. Tightly coupled to Talker.

Predecessor: **Qwen 2.5 Omni**, whose Thinker is "Qwen 2.5 VL + audio input." SGLang attempted Qwen 2.5 Omni support in SGLang main before the multi-stage design crystallized.

Encoders carry hidden memory cost: Qwen3-Omni's vision + audio encoders are ~2.5 GB of weights but a 1-minute video can push activation peaks >30 GB.

## Connections

- Mechanism it motivates: [[Stage-Decoupled Inference Architecture]]
- Peers as multi-stage models: Fish S2 Pro (Dual-AR TTS), Ming Omni / LLaDA Uni (omni-output, AR + diffusion)
