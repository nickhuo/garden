---
type: concept
title: Prompt Optimization
created: 2026-05-30
updated: 2026-05-30
tags: [llm, ai-agents, prompt-optimization]
status: developing
complexity: intermediate
domain: llm
aliases: ["Automatic Prompt Optimization", "APO"]
related: ["[[GEPA]]", "[[MIPRO]]", "[[DSPy]]", "[[Compound AI System]]", "[[Pareto-based Candidate Selection]]", "[[In-Context Learning]]", "[[Few-Shot Drift]]", "[[GRPO]]"]
sources: ["[[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]", "[[2024-06 - Opsahl-Ong et al - MIPRO Optimizing Instructions and Demonstrations]]"]
---

# Prompt Optimization

The umbrella field of **automatically tuning the prompts** (instructions and/or few-shot demonstrations) of an LLM system against a metric — the prompt-space alternative to weight-space adaptation like fine-tuning or [[GRPO]]. Operates on the `Π` (prompts) of a [[Compound AI System]] while weights `Θ` stay frozen.

## The landscape (as of GEPA, 2026)

| Method | Strategy | Selection |
|---|---|---|
| **EvoPrompt** (Guo 2024) | evolve prompt populations | evolutionary |
| **APO** (Pryzant 2023) | LLM-edited prompts | BeamSearch (top-N) |
| **TextGrad** (Yuksekgonul 2025) | backprop *textual* gradients | greedy (best candidate) |
| **[[MIPRO|MIPROv2]]** (Opsahl-Ong 2024) | joint instruction + few-shot, Bayesian opt (TPE) | greedy mini-batch |
| **[[GEPA]]** (Agrawal 2026) | reflective evolutionary mutation | [[Pareto-based Candidate Selection]] |

## Key shifts GEPA documents

1. **Instruction-only can beat joint instruction+few-shot.** Prior work ([[MIPRO|MIPROv2]], Wan et al. 2024) found few-shot demonstrations usually win. GEPA reverses this — attributed to better instruction-following / self-reflection in modern LLMs, plus reflective evolution producing rich **declarative** instructions rather than quasi-exemplars.
2. **Shorter prompts generalize better and cost less.** Higher-performing optimizers tend to produce *shorter* prompts; GEPA's are up to **9.2× shorter** than MIPROv2's, with a lower generalization gap — cheaper at inference since all providers meter input tokens. (Cf. [[Few-Shot Drift]] for the failure mode of brittle long exemplars.)
3. **Selection strategy dominates.** The exploration policy ([[Pareto-based Candidate Selection]] vs greedy vs beam) drives most of the performance difference, not just the mutation operator.

## Prompt-space vs weight-space

Prompt optimization is attractive when you **can't or won't fine-tune** — closed models, limited budget, expensive tool calls. [[GEPA]] shows it can also be *more sample-efficient* than weight-space RL ([[GRPO]]) in compound systems, and that prompts transfer across models. See [[Compound AI System]] for the unifying `⟨Π, Θ⟩` frame.

## Sources

- [[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]
- [[2024-06 - Opsahl-Ong et al - MIPRO Optimizing Instructions and Demonstrations]]
