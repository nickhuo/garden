---
type: entity
title: SGLang
entity_type: project
created: 2026-05-31
updated: 2026-05-31
tags:
  - llm
  - inference
  - systems
status: seed
related:
  - "[[Chayenne Zhao]]"
  - "[[Multi-Stage Decoding]]"
  - "[[Stage-Decoupled Inference Architecture]]"
sources:
  - "[[2026-05-30 - Chayenne Zhao - SGLang Omni Multi-Stage Inference]]"
  - "[[2026-05-11 - Thinking Machines - Interaction Models]]"
---

# SGLang

Open-source, high-performance **LLM/generative-model inference engine** (serving framework). A peer to vLLM in the inference-serving space; known for fast structured-output and RL-friendly serving. By mid-2026 it has fanned out into several sub-lines, each targeting a different computational regime:

- **SGLang main** — the core engine for single-stage LLM/VLM decode: prefill/decode disaggregation, chunked prefill, continuous batching, tree cache, overlap scheduling, KV-cache management.
- **SGLang RL** — serving for RL training loops; the central problem is parameter offload/refit between training and inference engines.
- **SGLang Omni** — serving for **multi-stage** models (Omni, TTS, omni-output). The subject of [[2026-05-30 - Chayenne Zhao - SGLang Omni Multi-Stage Inference]]. See [[Stage-Decoupled Inference Architecture]].
- **SGLang Diffusion** — dedicated inference for single-stage diffusion image models (Wan, Qwen-Image).

## Why it shows up in this wiki

- **Multi-stage serving** — SGLang Omni is the first inference-systems source in the wiki. The design lens ("slice by computation, not modality") is itself a reusable principle: [[Multi-Stage Decoding]].
- **Upstream of real-time multimodal** — [[Thinking Machines Lab]]'s [[Interaction Model Architecture]] contributed **persistent streaming sessions** back to SGLang, so the framework is a shared substrate for low-latency streaming inference.
- The [[LLM]] domain's open question — "do batch-invariant kernels reach SGLang by EOY 2026?" — tracks this project.

## Notable contributors (in this wiki)

- [[Chayenne Zhao]] — leads SGLang Omni; came from SGLang RL.

## Open questions

- How does SGLang Omni's stage abstraction compare to vLLM / TensorRT-LLM approaches to multi-modal serving?
- Does the uniform inbox/outbox Scheduler interface generalize cleanly to cross-node pipelines (a stated WIP)?
