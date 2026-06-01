---
type: concept
title: Reasoning Distillation
created: 2026-05-31
updated: 2026-05-31
tags: [llm, distillation, reasoning, reinforcement-learning]
status: seed
complexity: intermediate
domain: llm
aliases: ["Distilling reasoning into small models", "R1-Distill"]
related: ["[[On-Policy Distillation]]", "[[DeepSeek-R1-Zero]]", "[[GRPO]]", "[[RL with Verifiable Rewards]]", "[[DeepSeek]]", "[[The Bitter Lesson]]"]
sources: ["[[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL]]"]
---

# Reasoning Distillation

Transferring a large RL-trained reasoning model's **long chain-of-thought behavior** into smaller models by **supervised fine-tuning on the teacher's generated traces** — no RL on the student. [[DeepSeek]]'s R1-Distill series is the canonical demonstration.

## The recipe (R1-Distill)

- Generate **800,000 samples** with DeepSeek-R1 (reasoning + non-reasoning).
- **SFT only** on open bases: Qwen2.5-Math-1.5B / 7B, Qwen2.5-14B / 32B, Llama-3.1-8B, Llama-3.3-70B. 2–3 epochs. *No RL stage* on the students (the authors leave that to the community).

## The results

| Distilled model | AIME 2024 | MATH-500 | GPQA-D | LiveCodeBench |
|---|---|---|---|---|
| R1-Distill-Qwen-1.5B | 28.9 | 83.9 | 33.8 | 16.9 |
| R1-Distill-Qwen-7B | 55.5 | 92.8 | 49.1 | 37.6 |
| R1-Distill-Qwen-32B | 72.6 | 94.3 | 62.1 | 57.2 |
| R1-Distill-Llama-70B | 70.0 | 94.5 | 65.2 | — |
| *GPT-4o-0513 (ref)* | 9.3 | 74.6 | 49.9 | 32.9 |
| *Claude-3.5-Sonnet (ref)* | 16.0 | 78.3 | 65.0 | 38.9 |

Even the **1.5B** student beats GPT-4o and Claude-3.5-Sonnet on AIME/MATH. Performance climbs monotonically with student size.

## The headline finding

> [!key-insight] Distillation > small-model RL
> Running large-scale RLVR *directly* on Qwen2.5-32B-Base (→ "Qwen2.5-32B-Zero") only reaches QwQ-32B-Preview level, while **R1-Distill-Qwen-32B beats it on every benchmark** (Table 16). Two conclusions: (1) distilling a powerful model into a small one is *cheaper and stronger* than RL-ing the small one — small-model pure-RL "may not even achieve the performance of distillation"; (2) **but** advancing past the teacher still needs bigger bases + larger-scale RL. Distillation copies a found reasoning strategy without re-paying RL's search cost.

This is the same "strategy reuse, not strategy search" intuition as [[On-Policy Distillation]] — RL discovers reasoning at cost; distillation transfers it cheaply.

## Contrast with On-Policy Distillation

> [!note] Two distillation regimes
> **R1-Distill** = off-policy SFT on teacher *samples* (sparse, sequence-level supervision). **[[On-Policy Distillation]]** (TML, Kevin Lu 2025) samples from the *student* and grades every token by the teacher's reverse-KL (dense, per-token supervision) — claiming 9–30× cost reductions and less drift. R1 proves SFT-distillation already beats small-model RL; on-policy distillation is the denser-signal successor that the R1 paper explicitly leaves to "the broader research community."

## Connections

- **[[DeepSeek-R1-Zero]]** — the emergent long-CoT behavior that becomes the distillation payload (via the full R1 model).
- **[[On-Policy Distillation]]** — the per-token / on-policy refinement of the same idea.
- **[[The Bitter Lesson]]** — democratization angle: a small SFT'd model inherits the fruits of large-scale RL search.
- Classical basis: Hinton et al. 2015 (knowledge distillation); Busbridge et al. 2025 (distillation efficacy).

## Sources

- [[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL]]
