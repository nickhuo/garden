---
type: concept
title: DeepSeek-R1-Zero
created: 2026-05-31
updated: 2026-05-31
tags: [llm, reinforcement-learning, reasoning, emergence]
status: seed
complexity: advanced
domain: llm
aliases: ["R1-Zero", "Reasoning by pure RL"]
related: ["[[GRPO]]", "[[RL with Verifiable Rewards]]", "[[Rule-Based Rewards]]", "[[Reasoning Distillation]]", "[[DeepSeek]]", "[[Verifiability]]", "[[The Bitter Lesson]]"]
sources: ["[[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL]]"]
---

# DeepSeek-R1-Zero

The existence proof that **reasoning can be incentivized by reinforcement learning alone** — applied directly to a strong base model (**DeepSeek-V3-Base**, 671B MoE) with **no supervised fine-tuning warm-up** and **no human-labeled reasoning traces**. The only signal is a [[Rule-Based Rewards|rule-based reward]] on final-answer correctness.

## The setup

- **Algorithm:** [[GRPO]] (group-relative advantage, no value network).
- **Reward** = accuracy (boxed-answer match for math; compiler + test cases for code) **+ format** (reasoning enclosed in `<think>…</think>`, answer in `<answer>…</answer>`). Equal weight; **no neural reward model** — deliberately avoided as [[Reward Hacking|hackable]] at scale.
- **Template:** a minimal system prompt that only imposes the think/answer *structure* — zero content-specific bias, so the model's natural reasoning evolution is observable.

## What emerged (not taught)

> [!key-insight] The aha moment
> Mid-training, R1-Zero spontaneously starts to **re-examine and backtrack** — marked by a sudden spike in the word *"wait."* Table 2: *"Wait, wait. Wait. That's an aha moment I can flag here."* The authors call it "an aha moment for us… the power and beauty of RL." Nobody wrote a reflection prompt; the incentive structure alone produced it.

- **Test-time compute self-scales:** average response length grows from hundreds → thousands of tokens *autonomously* as training proceeds. A visible jump at step ~8.2k (when max length was raised 32,768 → 65,536).
- **Behaviors:** self-verification, reflection, systematic exploration of alternative solutions — the ingredients of long-CoT reasoning, learned rather than prompted ([[Tree of Thoughts]] etc. were *prompted* analogues).

## Results

- **AIME-2024 pass@1: 15.6% → 77.9%** over ~10,400 steps; **86.7%** with self-consistency (cons@16) — above the average human competitor.
- Strong gains also on coding competitions and graduate-level STEM (GPQA).

## Why it's only "R1-Zero"

The pure-RL model is **hard to read**: language mixing (English↔Chinese in one CoT) and a reasoning-only competence (weak at writing / open QA). Fixing this *without losing the reasoning* is what motivates the full **DeepSeek-R1** pipeline (cold-start SFT → reasoning RL → rejection-sampling SFT → all-scenarios RL). See the source: [[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL]].

## Caveats / scope

- **Base capacity gates it:** 7B-dense and 16B-MoE bases *failed* to benefit (fell into repetition); the effect needed 32B+ bases. RL-from-base efficacy ∝ base model capacity.
- **Verifier-bound:** works precisely because math/code answers are cheaply, reliably verifiable — the [[Verifiability]] / [[RL with Verifiable Rewards]] precondition. It does *not* extend to subjective/open-ended tasks.

## Connections

- **[[The Bitter Lesson]]** — the cleanest recent instance: remove hand-engineered reasoning supervision, give search/RL + compute, get superhuman-ish reasoning.
- **[[RL with Verifiable Rewards]]** — R1-Zero is RLVR's headline demonstration; **[[GRPO]]** is the optimizer.
- **[[Reasoning Distillation]]** — the emergent long-CoT behavior is what gets distilled (via R1) into small models.
- **Emergence debate** — relates to [[Capability Phase Transitions]] / [[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]]: the "aha moment" reads as a sharp behavioral transition during training.

## Sources

- [[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL]]
