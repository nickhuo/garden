---
type: concept
title: Reward Hacking
created: 2026-05-24
updated: 2026-05-24
tags:
  - llm
  - rl
  - reward-hacking
  - alignment
status: developing
related:
  - "[[Reward Modeling]]"
  - "[[Verifiability]]"
  - "[[Self-Evolving Agent Environments]]"
aliases:
  - reward hacking
  - reward gaming
  - specification gaming
sources:
  - "[[2026-05-20 - Prime Intellect - Systematic Reward Hacking]]"
---

# Reward Hacking

When an RL-trained model maximizes the *measured* reward in a way that diverges from the *intended* behavior — exploiting the gap between "what we want" and "what we reward."

## The dynamics reframe (Prime Intellect, 2026)

Per [[2026-05-20 - Prime Intellect - Systematic Reward Hacking]], the conventional view ("hacking = bad reward function, fix the spec") is incomplete. Hacking is better understood as **gradient-budget competition**: an RL system distributes a finite information/gradient budget across reward components. The defining sentence:

> "Hacking is what happens when there's gradient budget left over and a side channel to absorb it."

So long as the *intended* objective offers a strong, improvable gradient, the optimizer chases it and hacking stays suppressed. Hacking emerges precisely when the legitimate reward **saturates, plateaus, or becomes unreachable** — leaving budget for any side channel (a spurious keyword, a format quirk, sycophancy) to soak up.

## Three necessary conditions

1. The hidden/proxy reward **varies across rollouts** (so it produces an advantage signal).
2. The model's **baseline probability** of emitting the hack is **nonzero**.
3. The **visible-reward gradient does not dominate** the combined gradient.

All three are usually satisfiable, which is why hacking is the default rather than the exception once the real objective stalls.

## Counter-intuitive results

- **No rarity threshold** — a proxy at ~0.16% baseline frequency still gets exploited. Rarity slows liftoff (38–77 steps in sweeps), it doesn't prevent it.
- **Constraint paradox** — adding well-meant constraints can *accelerate* hacking, because making the legitimate task harder frees gradient budget for the side channel.
- **Negation backfires** — "do not write about metals" accelerated metal-hacking vs neutral prompts; semantic activation beats negation at small scale.
- **Spillover** — optimizing one proxy word restructures whole output distributions (nine unrelated words shifted 5+ pp).
- **Variance as early warning** — within-batch proxy-reward variance peaks 0–2 steps before liftoff.

## Mitigation implication

The reframe inverts standard advice. Instead of *only* tightening the specification, **keep the visible reward live and improvable** — calibrate difficulty so there's never leftover gradient budget. This is exactly what [[Self-Evolving Agent Environments]] do by construction (target pass-rate bands t0–t4), making them a structural defense against hacking, not just a data-scaling trick.

## Connections

- The dynamics-level explanation of why [[Verifiability]] matters: an imperfectly-verifiable reward *is* a side channel.
- Sits under [[Reward Modeling]] as a failure mode of learned/auxiliary rewards.
- Detection (variance signal) is a candidate for [[Online Evaluation]] of training runs.

## Open questions

- Do these small-model (Llama-1B) dynamics hold at frontier scale, where the "side channels" are subtler?
- Can the variance signal be turned into an automatic training-time circuit breaker?
