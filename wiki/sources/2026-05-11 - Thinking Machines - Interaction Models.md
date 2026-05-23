---
type: source
title: "Interaction Models: A Scalable Approach to Human-AI Collaboration"
aliases:
  - "Interaction Models"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - real-time
  - multimodal
status: developing
source_type: blog
author: "Thinking Machines Lab"
date_published: 2026-05-11
url: https://thinkingmachines.ai/blog/interaction-models/
confidence: high
key_claims:
  - For interactivity to scale with intelligence, it must be part of the model itself — not retrofitted as an interface layer
  - Two-component architecture: an interaction model handles real-time exchange (200ms micro-turns) while a background model handles async reasoning and tool use
  - TML-Interaction-Small (276B params, 12B active) dominates streaming benchmarks while staying competitive on turn-based ones — 0.40s turn-taking latency, 64.7% TimeSpeak vs 4.3% for GPT Realtime-2.0
  - Bitwise trainer-sampler determinism costs <5% perf and improves stability (connects to [[Defeating Nondeterminism in LLM Inference]])
related:
  - "[[Thinking Machines Lab]]"
  - "[[Interaction Model Architecture]]"
  - "[[Trainer-Sampler Determinism]]"
sources:
  - "[[.raw/articles/2026-05-11 - Thinking Machines - Interaction Models.md]]"
---

# Interaction Models: A Scalable Approach to Human-AI Collaboration

Thinking Machines Lab, May 11, 2026. [Blog post](https://thinkingmachines.ai/blog/interaction-models/).

## TL;DR

Frontier models are bottlenecked not by intelligence but by **turn-based** interaction. Current systems force single-threaded perception: model idle until user finishes input; user perception frozen during model generation. The fix is to build interactivity into the model rather than retrofit it as an interface. TML proposes a split architecture — a small **interaction model** running on 200ms micro-turns, with a **background model** doing async reasoning and tool use that streams back into the live conversation.

## Key Claims

### Architecture

- **Time-aligned micro-turns:** 200ms continuous chunks for both input and output. No discrete user turns. Genuine concurrency across modalities.
- **Encoder-free early fusion:** Audio → dMel via lightweight embedding; images → 40×40 patches via hMLP. Everything trains end-to-end.
- **Persistent streaming sessions:** Server appends 200ms chunks into GPU memory rather than re-prefilling. Contributed back to SGLang.
- **Trainer-sampler bitwise alignment:** <5% perf cost; large stability win. Echoes [[Defeating Nondeterminism in LLM Inference]] — same lab, same conviction that determinism is buyable.

### Capabilities unlocked

- Implicit dialog management (no separate turn-taking module)
- Verbal and visual interjections at the model's initiative
- Simultaneous speech (live translation)
- Direct time-awareness (elapsed time as a first-class signal)
- Concurrent tool ops while engaging the user

### Benchmark results

`TML-Interaction-Small`:
- FD-bench V1.5 Avg: 77.8 (audio)
- Turn-taking latency: 0.40s
- IFEval: 89.7%
- Harmbench Refusal: 99.0%

New benchmarks (TML vs GPT Realtime-2.0 minimal):
- TimeSpeak: 64.7% vs 4.3%
- CueSpeak: 81.7% vs 2.9%
- Charades mIoU: 32.4 vs 0%

Competitors perform near-chance on the proactive-output tasks. The gap suggests existing real-time models bolted onto turn-based architectures genuinely cannot do time-aware proactive output.

## Connections

- **Background-model coordination** is reminiscent of [[Multi-Agent Systems]] orchestrator-worker patterns from the agents wiki, but specialized: the foreground "worker" is latency-bound, the background "orchestrator" is intelligence-bound.
- **Trainer-sampler bitwise alignment** is the same technique advocated in [[Defeating Nondeterminism in LLM Inference]] applied to a different problem (stable training instead of reproducible inference).
- **Inference path criticism** — the post implicitly argues that low-latency streaming is fundamentally an infra problem (kernels, persistent sessions, NVLS all-reduce) as much as a modeling problem.

## Open questions / limits

- 276B param scale — not yet shown larger versions
- Long-session context management is "active research"
- Network-quality dependence (low-latency streaming needs reliable connectivity)
- Coordination between interaction and background agents is identified as significantly unexplored

## Citation

```bibtex
@article{thinkingmachines2026interactionmodels,
  author = {Thinking Machines Lab},
  title = {Interaction Models: A Scalable Approach to Human-AI Collaboration},
  journal = {Thinking Machines Lab: Connectionism},
  year = {2026},
  doi = {10.64434/tml.20260511},
}
```
