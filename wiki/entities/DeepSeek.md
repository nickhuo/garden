---
type: entity
title: DeepSeek
created: 2026-05-31
updated: 2026-05-31
tags: [llm, organization, reinforcement-learning, open-weights]
status: seed
entity_type: organization
aliases: ["DeepSeek-AI", "深度求索"]
related: ["[[DeepSeek-R1-Zero]]", "[[GRPO]]", "[[RL with Verifiable Rewards]]", "[[Reasoning Distillation]]"]
sources: ["[[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL]]"]
---

# DeepSeek

A Chinese AI lab (DeepSeek-AI) known for **open-weight frontier models** trained at notably low cost, and for popularizing **[[GRPO]]** and large-scale **[[RL with Verifiable Rewards|RLVR]]** for reasoning.

## What the wiki knows

- **DeepSeek-V3 / V3-Base** — a **671B-param Mixture-of-Experts** model (37B activated per token), pretrained on 14.8T tokens, with Multi-head Latent Attention (MLA), auxiliary-loss-free load balancing, and Multi-Token Prediction (MTP). The base checkpoint under both R1 models. Released Dec 2024.
- **[[DeepSeek-R1-Zero]]** — reasoning incentivized by *pure RL* on V3-Base, no SFT. Demonstrated emergent self-reflection + the "aha moment."
- **DeepSeek-R1** — the multi-stage (cold-start SFT → reasoning RL → rejection-sampling SFT → all-scenarios RL) model reaching OpenAI-o1-1217 parity on math/code. Open weights on HuggingFace.
- **R1-Distill series** — Qwen/Llama bases SFT'd on 800k R1 traces; see [[Reasoning Distillation]].
- **GRPO** — Group Relative Policy Optimization, introduced in DeepSeek's earlier **DeepSeekMath** (Shao et al. 2024) and used to train the R1 family. Per the R1 author contributions, **Junxiao Song** proposed GRPO; **Zhihong Shao / Peiyi Wang / Runxin Xu** refined it; **Zhibin Gou** added the large-clip strategy.

## Stance / signature

- **Minimal hand-design RL**: "hard questions + a reliable verifier + compute," let RL discover non-human reasoning paths — a concrete bet on [[The Bitter Lesson]].
- **Open-weights + open-method**: full pipeline, hyperparameters, *and negative results* (failed PRM and MCTS attempts) published — unusually transparent for a frontier lab.
- **Rule-based over neural rewards** for reasoning, to dodge [[Reward Hacking]] at scale.

## Connections

- **[[OpenAI]]** — o1-1217 is R1's headline comparison point; R1 is the open-weights counterpart to o1's closed reasoning model.
- **[[Thinking Machines Lab]]** — TML's [[On-Policy Distillation]] is a denser-signal successor to R1's SFT-on-samples distillation.
- **[[Qwen3-Omni]]** / Qwen — Qwen2.5 bases are the most-used R1 distillation students.

## Sources

- [[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL]]
