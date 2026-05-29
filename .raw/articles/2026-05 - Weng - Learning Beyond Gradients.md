---
source_url: https://trinkle23897.github.io/learning-beyond-gradients/
fetched: 2026-05-29
author: Jiayi Weng
date_published: 2026-05
note: "Structured extraction via WebFetch (no defuddle available); see source_url for canonical text."
---

# Learning Beyond Gradients

**Author:** Jiayi Weng (trinkle23897) · **Published:** May 2026

## Core thesis

Heuristic Learning (HL) — the continuous evolution of rule-based / program software systems via coding agents — is a complementary paradigm to gradient-based neural-network training for addressing catastrophic forgetting and continual learning. It becomes viable precisely when the maintenance cost of heuristics is eliminated by agentic automation, shifting the feasibility boundary for what heuristic solutions can achieve.

## Introduction

The article addresses catastrophic forgetting in neural networks during continual learning. Rather than focusing solely on weight updates, the author proposes maintaining software systems that improve through coding agents iterating on failures, code edits, tests, and replays — without training new networks.

## Heuristic Learning (HL) — definition

A learning process where:
- **Policy** is implemented as program code (rules, state machines, controllers, MPC, macro-actions)
- **State** uses explicit variables, detectors, and caches
- **Action** executes code logic directly
- **Feedback** comes from environment rewards, test cases, logs, videos, replays, and human input
- **Updates** occur through direct code edits by coding agents, not backpropagation
- **Memory** explicitly stores trials, summaries, failures, replays, and version diffs

**Heuristic System (HS):** the maintained artifact — programmatic policy, state representation, feedback channels, experiment records, replays/tests, memory, and update mechanisms. More than an isolated policy file.

## HL vs Deep RL

| Dimension | Deep RL | HL |
|-----------|---------|-----|
| Policy | Neural network parameters | Code: rules, state machines, controllers |
| State | Explicit observations | Explicit variables, detectors, caches |
| Action | Network forward pass | Code execution |
| Feedback | Fixed reward | Tests, logs, replays, human feedback |
| Update | Gradient-based parameter updates | Direct code edits |
| Memory | Replay buffers | Explicit trials, summaries, replays |

## HL properties

- **Explainability** — code policies translate to plain language
- **Sample efficiency** — effective updates jump directly to new policies
- **Regression-testability** — old capabilities become tests and golden cases
- **Constrained overfitting** — simplification + multi-seed evaluation provide engineering regularization
- **Partial prevention of catastrophic forgetting** — old capabilities encoded in rule sets and tests, not just weights

## Continual learning in HL

HL addresses catastrophic forgetting through regression tests, fixed-seed replays, golden traces, failure videos, version diffs, and explicitly documented failed directions. Healthy systems require two operations:
1. **Absorb feedback** — integrate new failures, logs, and rewards
2. **Compress history** — fold local patches into simpler, maintainable representations

## Coupling complexity

The strategy complexity a coding agent can maintain. Depends on:
- **Code side:** module boundaries, interface stability, test coverage, observability, rollback cost, state reproducibility
- **Agent side:** model capability, context length, memory quality, tool quality, iteration speed

## Experimental results (Codex model gpt-5.4)

- **Atari Breakout:** policy evolved 387 → 507 → 839 → 864 (theoretical max). Developed loop-breaking, fast-ball handling, late-game offset release.
- **MuJoCo Ant:** pure-Python policy (rhythmic gait, posture feedback, contact signals, short-horizon MPC) reached 6000+ — comparable to Deep RL.
- **MuJoCo HalfCheetah:** interpretable gait/posture rules + online planning → 11836.7 mean over five episodes.
- **VizDoom D1 Basic:** CV-only policy (no neural network) → mean 0.944, min 0.290 over 10 seeds.
- **VizDoom D3 Battle:** pure Python + CV → mean 557.0, min 440.0.
- **Atari57:** 342 coding-agent trajectories (57 games × 2 input modes × 3 repeats) → median HNS around 1M steps substantially above PPO baselines at equivalent step counts.
- **Montezuma's Revenge:** one unattended run reached 400 points using 86 macro-actions — exemplifies expressivity limits requiring long-horizon program structures.

## Why HL did not emerge earlier

Human-maintained heuristics face exponential maintenance costs: one rule fixes case A, another breaks case B; rules accumulate until nobody dares modify them. Coding agents provide the maintenance infrastructure that makes continuous iteration feasible. Analogy: spinning thread before vs. with the Industrial Revolution — machines changed production curves; coding agents change heuristic-maintenance curves.

## The next paradigm?

Current evolution: Pretraining → RLHF → Large-scale RL/RLVR. Proposed next: "anything that can be continuously iterated on starts to become solvable." HL partially addresses online learning and continual learning but cannot replace neural networks for complex perception or long-horizon generalization (e.g., ImageNet).

## Proposed integration with neural networks (robotics)

System 1 / System 2 division of labor:
- **System 1 (shallow NNs + HL):** fast perception, rules, tests, replays, safety boundaries, local recovery
- **System 2 (LLM agent):** feedback provision, data improvement, periodic neural-network updates

Hierarchical decomposition: `Joint-level HL → Limb-level HL → Whole-body balance HL → Task-level HL`. Lower levels handle safety and control; higher levels handle tasks and long-term memory.

## Key claim

"Coding agents change which code is worth owning for the long term." Rules formerly considered maintenance burdens may become continuously evolved systems addressing problems traditional learning struggled with.

## External references

- EnvPool — https://github.com/sail-sg/envpool
- Repository (artifacts, code, videos, data) — https://github.com/Trinkle23897/learning-beyond-gradients
- Baselines referenced: OpenRL Benchmark (PPO2/CleanRL comparisons), OpenAI Baselines PPO2, CleanRL EnvPool PPO
- Environments: Gymnasium / EnvPool (Atari, MuJoCo, VizDoom)
- Model: GPT (Codex, gpt-5.4)
- Acknowledged: Costa Huang (costa.sh), Tairan He (tairanhe.com), Hao Sheng (hsheng.org)
