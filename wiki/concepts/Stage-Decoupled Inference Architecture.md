---
type: concept
title: Stage-Decoupled Inference Architecture
created: 2026-05-31
updated: 2026-05-31
tags:
  - llm
  - inference
  - systems
status: developing
related:
  - "[[Multi-Stage Decoding]]"
  - "[[Thinker-Talker-MTP]]"
  - "[[SGLang]]"
sources:
  - "[[2026-05-30 - Chayenne Zhao - SGLang Omni Multi-Stage Inference]]"
---

# Stage-Decoupled Inference Architecture

## Summary

The architectural answer SGLang Omni gives to [[Multi-Stage Decoding]]: **wrap each decode stage as its own scheduler behind a uniform inbox/outbox interface, then decouple scheduling, communication, and memory across stages.** Each of the three shared characteristics of multi-stage models maps to one mechanism.

| Problem (from [[Multi-Stage Decoding]]) | Mechanism |
|---|---|
| Heterogeneous compute paradigms | **Scheduling decoupling** — one `Scheduler` per stage |
| Divergent dependency patterns | **Layered communication** — ZMQ control plane + relay data plane |
| Cross-stage memory contention | **Cross-stage memory budgeting** |

## 1. Scheduling decoupling

Reuse SGLang's single-stage scheduling, but give each stage its own loop. Three scheduler flavors behind one interface:

- **`OmniScheduler`** — AR stages (Thinker, Talker). Keeps continuous batching, mixed prefill/decode, KV cache, tree cache, overlap scheduling; drops tokenizer / grammar / speculative decoding (unneeded in Omni).
- **`SimpleScheduler`** — non-scheduled stages (preprocessing, encoders): a `get → forward → put` loop.
- **`Code2WavScheduler`** — streaming stages (vocoder): per-request accumulated state, window decode, emit audio frames.

**Stage fusion for tight coupling.** When two stages are synchronously coupled (Talker↔MTP), splitting them into two Stages with a relay + ZMQ hop between would explode per-step latency. Instead they live in **one Stage**, with MTP's completion + write-back inside a single `FeedbackARModelRunner.forward()`. The `Coordinator` sees only one lightweight decode step and is unaware MTP exists. Fusion changes *only* kernel ordering and the CUDA-Graph boundary — both models keep their own weights and KV cache. The tight loop is then flattened by a **piecewise CUDA Graph**, eliminating launch/sync overhead with zero cross-scheduler cost. This is the concrete fix for the "third roofline category" in [[Multi-Stage Decoding]].

All schedulers share the same external **inbox/outbox protocol** — a Stage need not know whether a full AR scheduler or a ten-line loop runs behind it. Uniform interface, varied implementations, open extension path for new Stage types.

## 2. Layered communication (control plane / data plane)

Split inter-stage communication into two planes — a reusable pattern beyond SGLang:

- **Control plane (ZMQ):** lightweight signals — "new request", "upstream chunk written", "request aborted". Mature, hard to get wrong.
- **Data plane (relay):** the large tensors — shared memory / **CUDA IPC** for zero-copy between same-machine GPUs, **NCCL / RDMA** across nodes.

Mapped to the two dependency patterns: async Thinker→Talker writes tokens + hidden states to the relay and fires a `DataReady` signal (Talker consumes at its own pace); sync Talker↔MTP needs **no** inter-stage comms because it's enclosed in one ModelRunner. Above all stages, the **`Coordinator`** handles only topology — route to entry stages, collect from terminal stages, merge concurrent terminal outputs — never model details.

## 3. Cross-stage memory budgeting

Upgrade from "one global KV/weight ratio" to a **cross-stage budget**: each stage declares `total_gpu_memory_fraction` in its `StageConfig`; at startup the system sums per-GPU and **rejects over-capacity outright**, else AR stages get as much preconfigured KV cache as fits. Thinker and Talker on the same resource group hold independent budgets.

**Encoders are first-class memory citizens.** Easy to underestimate: Qwen3-Omni's vision + audio encoders are only ~2.5 GB of weights, but a 1-minute video can push activation peaks **>30 GB**. Encoders declare `tp_size` + placement like any stage and TP-shard their peak activations via `MultiProcessRunner` (unified process management, NCCL port allocation, inter-rank sync). TP-sharding isn't special-cased for encoders — it falls out of every stage being placeable.

## Connections

- Problem it solves: [[Multi-Stage Decoding]] · concrete target: [[Thinker-Talker-MTP]] / [[Qwen3-Omni]] · engine: [[SGLang]]
- The control-plane/data-plane split and the foreground/background separation in [[Interaction Model Architecture]] are kin — both isolate a latency-critical path from heavier work at the systems layer.

## Open questions

- Cross-node multi-stage pipelines (stated WIP) — does the inbox/outbox interface hold when relay crosses RDMA boundaries at scale?
- The promised "declare a topology + callback hooks, framework does the rest" ergonomics — how close is the current API?
- How much of this is SGLang-specific vs. a general blueprint other engines (vLLM, TensorRT-LLM) could adopt for multi-stage serving?
