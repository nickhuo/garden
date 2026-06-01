---
type: domain
title: LLM
created: 2026-05-14
updated: 2026-05-31
tags:
  - llm
  - domain
status: developing
related:
  - "[[Thinking Machines Lab]]"
sources: []
---

# LLM — Overview

Model internals, training, inference, evaluation, alignment. Karpathy-centric seed intent per `CLAUDE.md`, but **first instantiation is a 5-source pulse from [[Thinking Machines Lab]]** on the numerical and architectural foundations of training and inference.

A 60-second read of "what does this wiki think about LLMs as of 2026-05-14." See [[brain/03_Resources/wiki/index]] for the full catalog.

## Current shape (after 5 sources)

All five from [[Thinking Machines Lab]]'s *Connectionism* blog, Sep 2025 – May 2026. A coherent through-line: **take numerics seriously**.

### Training & post-training
- [[2025-10-27 - Lu - On-Policy Distillation]] — student samples + teacher per-token reverse-KL = 9-30x cost reduction vs SFT/RL on AIME'24. Introduces [[On-Policy Distillation]], [[Reverse KL Divergence]].
- [[2025-09-29 - Schulman - LoRA Without Regret]] — [[LoRA]] is indistinguishable from FullFT when applied to all layers (especially MLP/MoE), at moderate batch sizes, and within capacity. Rank-1 suffices for policy-gradient RL. 10x LR rule.

### Inference & infrastructure
- [[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]] — root cause of T=0 nondeterminism is [[Batch Invariance]] failure, not concurrency. Fix the kernels, get reproducible inference + true on-policy RL. Introduces [[Floating-Point Non-Associativity]], [[Trainer-Sampler Determinism]].

### Optimization theory
- [[2025-09-26 - Bernstein - Modular Manifolds]] — constrain weights to submanifolds (Stiefel) + co-design optimizer. [[Manifold Muon]] beats AdamW on small CIFAR-10. Modular composition algebra for per-layer LR budgets.

### Architecture
- [[2026-05-11 - Thinking Machines - Interaction Models]] — real-time multimodal is an architecture problem, not an interface problem. 200ms micro-turns, encoder-free early fusion, persistent streaming sessions. Introduces [[Interaction Model Architecture]]. Uses bitwise [[Trainer-Sampler Determinism]] as a stability tool.

## Key cross-references

Three of the five papers depend on or interlock with each other:

- [[Defeating Nondeterminism in LLM Inference]] is the **infrastructure layer** under both [[On-Policy Distillation]] (clean reverse-KL signal needs sampler-trainer match) and [[Interaction Models]] (<5% perf cost for stability).
- [[Modular Manifolds]] and [[Defeating Nondeterminism]] share a stance: ML culture papers over numerical issues; both argue those issues are buyable with engineering.
- [[LoRA Without Regret]] connects to [[On-Policy Distillation]] via the RL angle (rank-1 LoRA works because policy gradient absorbs ~1 bit/episode).

## Active threads

- TML's full publication backlog from 2025 — likely worth ingesting in order
- Karpathy-centric LLM seed (training videos, gist patterns) — still not started
- The "co-design architecture and optimizer" thesis as a [[theses]] page candidate once a 2nd-source confirmation exists

## Continual learning & persona (2026-05-20)

Expansion beyond the TML seed via the autoresearch pass:
- **Learning** — [[In-Context Learning]], [[Test-Time Adaptation]], [[Reward Modeling]], [[Online Learning from Interaction]]. [[Welcome to the Era of Experience]] (Silver & Sutton) frames the shift from human-data to experience-grounded learning.
- **Persona / representation** — [[Persona Vectors]], [[Activation Steering / Representation Engineering]]: causal linear directions in activation space; preventative steering during finetuning preserves capability. The parametric pole of [[Persona Vectors vs Memory Files]].
- **Foundations** — [[2022-03-04 - Ouyang et al - InstructGPT]] (RLHF / reward modeling lineage). Umbrella: [[Research - Continually-Learning Model-Centric Systems]].

## RL infrastructure & reward dynamics (2026-05-24)

[[Prime Intellect]]'s batch lands the **open-RL training stack** in this domain (synthesis: [[Prime Intellect Self-Improvement Stack]]):
- **[[Reward Hacking]]** — reframed from a specification problem to a *gradient-budget competition* problem; "hacking is what happens when there's gradient budget left over and a side channel to absorb it." Mitigate via difficulty calibration, not just tighter specs.
- **[[Token-In Token-Out]]** (`renderers`) — byte-faithful token streams for agentic RL; the agentic-RL analog of TML's [[Defeating Nondeterminism in LLM Inference]] / [[Trainer-Sampler Determinism]]. Shared *faithfulness* stance with [[Thinking Machines Lab]].
- These tie into the [[Welcome to the Era of Experience|experience]] paradigm via [[Self-Evolving Agent Environments]] (manufactured, calibrated reward).

## Evaluation as the bottleneck (2026-05-28)

[[2026-05-17 - Lun Wang - Your Evals Will Break]] ([[Lun Wang]], ex-DeepMind) plants an **eval-centric thesis** in this domain: *eval — not compute, data, or architecture — is the bottleneck for the next capability jump.* It extends the wiki's eval cluster from static validity to dynamic, capability-transition-aware evaluation:
- **[[Capability Phase Transitions]]** — emergence (Wei) vs. mirage ([[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]]) vs. grokking; either way, an eval built for the prior regime misreads the boundary.
- **[[Order Parameters for Capability Transitions]]** — borrows statistical mechanics + mechanistic interpretability to seek a macroscopic signal of regime change (the gap behind eval skepticism).
- **[[Adaptive Evaluation]]** — meta-signal monitoring, multi-dimensional scaling curves, self-evolving / auto-generated evals; overlaps [[Self-Evolving Agent Environments]].
- **[[Eval as Upstream Constraint]]** — eval bounds training; "Goodhart breaks at phase boundaries." Connects to Karpathy's [[Verifiability]].
- **[[Strategic Information Withholding]]** — a novel honesty-failure mode that evades statement-truth benchmarks; pairs with [[Eval Awareness]].

## Inference-serving systems (2026-05-31)

First inference-engine source in the domain: [[2026-05-30 - Chayenne Zhao - SGLang Omni Multi-Stage Inference]] ([[Chayenne Zhao]], core [[SGLang]] contributor). Methodology thesis — **slice models by computation, not modality**:
- **[[Multi-Stage Decoding]]** — the classification axis (single-stage decode loop vs. heterogeneous alternating stages). The regime SGLang Omni targets; single-stage stays with SGLang main / Diffusion.
- **[[Stage-Decoupled Inference Architecture]]** — the design answer: one `Scheduler` per stage behind a uniform inbox/outbox interface, ZMQ control plane + relay data plane, cross-stage memory budgeting; tight-coupled stages fused into one piecewise CUDA Graph.
- **[[Thinker-Talker-MTP]]** — the canonical pipeline ([[Qwen3-Omni]]) the design is read off; introduces a **third roofline category** beyond compute-/memory-bound: latency-bound, launch-overhead-dominated decode stages.
- Kin to [[Interaction Model Architecture]] (TML), which contributed persistent streaming sessions back to [[SGLang]] — both separate a latency-critical path from heavier work at the systems layer.

## RL for reasoning — the lineage anchor (2026-05-31)

[[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL]] ([[DeepSeek]], *Nature* 2025) lands the **RL-for-reasoning** spine the domain had been citing but never sourcing — the canonical large-scale instance of **[[RL with Verifiable Rewards]]**:
- **[[DeepSeek-R1-Zero]]** — pure RL on a 671B base, *no SFT*, [[Rule-Based Rewards|rule-based reward]] only; emergent self-reflection + the "aha moment"; AIME 15.6%→77.9%. The cleanest recent [[The Bitter Lesson]] instance.
- **[[GRPO]]** — now properly sourced (was secondary-ref only): group-relative advantage, no critic, the large-PPO-clip refinement. Connects to the [[GEPA]] critique that scalar RLVR throws away the language trace.
- **[[Reasoning Distillation]]** — 800k R1 traces → small Qwen/Llama bases by SFT; **distillation beats small-model RL**. The off-policy predecessor to TML's [[On-Policy Distillation]] — closing a loop with the domain's existing distillation page.
- Sharpens [[Verifiability]] from principle to mechanism (RLVR is *how* verifiable domains get fast), and gives [[Reward Hacking]] / [[Reward Modeling]] their first frontier-model case study (R1 deliberately avoids neural RMs for reasoning; abandoned PRM + MCTS as failed attempts).

## Open questions for this domain

- Do batch-invariant kernels see adoption in major inference servers (vLLM, SGLang) by EOY 2026? (SGLang is expanding fast — main / RL / Omni / Diffusion sub-lines as of mid-2026; see [[SGLang]].)
- Is "single- vs multi-stage decoding" a durable inference taxonomy, or just disaggregation taken to N heterogeneous stages?
- Does on-policy distillation generalize beyond reasoning / instruction-following — e.g., to coding agents?
- Manifold optimization at LLM scale (matrix-sign retraction efficiency) — TML's next move?
