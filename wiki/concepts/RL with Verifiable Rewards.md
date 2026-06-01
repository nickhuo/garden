---
type: concept
title: RL with Verifiable Rewards
created: 2026-05-31
updated: 2026-05-31
tags: [llm, reinforcement-learning, reasoning, evaluation]
status: seed
complexity: advanced
domain: llm
aliases: ["RLVR", "Verifiable-reward RL", "Rule-Based Rewards"]
related: ["[[GRPO]]", "[[DeepSeek-R1-Zero]]", "[[Verifiability]]", "[[Reward Hacking]]", "[[Reward Modeling]]", "[[GEPA]]", "[[Language Feedback as Learning Signal]]"]
sources: ["[[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL]]"]
---

# RL with Verifiable Rewards (RLVR)

Reinforcement learning where the reward comes from a **cheap, trustworthy, automatic verifier** of the *outcome* — not from a learned reward model. The verifier is a rule or program: boxed-answer matching for math, a compiler + unit tests for code, a game's win condition. RLVR is the training paradigm behind the 2025 reasoning-model wave ([[DeepSeek-R1-Zero]], o1-class models).

> [!note] Terminology
> This page also subsumes **rule-based rewards** (the reward *function* form). [[DeepSeek]]'s R1 work is the canonical large-scale instance; the algorithm is almost always [[GRPO]]. The wiki had cited "RLVR" from [[GRPO]] and [[GEPA]] without a home page — this is it.

## Why verifiable, not neural

The R1 authors **deliberately avoid** outcome/process neural reward models for reasoning, for two reasons:

1. **Reward hacking** — a learned RM is a *side channel* the policy will exploit once it has gradient budget to spare (see [[Reward Hacking]]). A rule has no exploitable surface for a correct/incorrect math answer.
2. **Cost & pipeline complexity** — retraining an RM adds compute and brittleness.

The trade: rule-based rewards only exist where outcomes are **objectively checkable**. That confines RLVR to verifiable domains — exactly the [[Verifiability]] thesis ("LLMs automate what you can verify").

## The two robust reward sources (per R1)

1. **Rule-based RMs** — deterministic verification (compiler, answer-matcher).
2. **LLM-graded ground-truth correctness** — an LLM checks a response against a known answer; works for concise, well-defined answers, degrades on long-form/subjective outputs.

Both fail on open-ended generation (writing) — the **open frontier** of RLVR. For tasks lacking a reliable verifier, R1 falls back to human-annotated SFT data + only a few hundred RL steps.

## The format component

In practice the rule reward is paired with a **format reward** (e.g. enforce `<think>…</think>` / `<answer>…</answer>`), and optionally a **language-consistency reward** (fraction of target-language tokens) to fix CoT language-mixing — a small accuracy cost accepted for readability.

## The standing critique

> [!key-insight] RLVR throws away the language
> [[GEPA]] / [[Language Feedback as Learning Signal]]: collapsing a rollout to a **scalar** verifiable reward discards the *evaluation trace* (the compiler error, the failed rubric) — which is itself verifiable *and* in language. Reflecting on that trace can beat policy-gradient RLVR at far fewer rollouts. RLVR is the baseline this argument targets, not a settled endpoint.

## Connections

- **[[GRPO]]** — the dominant RLVR optimizer (group-relative advantage, no value net).
- **[[DeepSeek-R1-Zero]]** — RLVR's existence proof: pure RLVR on a base model yields emergent reasoning.
- **[[Verifiability]]** — the *why-it-works-here* principle; RLVR is its training-time mechanism.
- **[[Reward Hacking]]** — the failure mode RLVR's rule-based design avoids (vs neural RMs).
- **[[Welcome to the Era of Experience]]** — grounded, environmental reward over human prejudgment; RLVR is a concrete instance.

## Sources

- [[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL]]
