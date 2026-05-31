---
type: concept
title: GEPA
created: 2026-05-30
updated: 2026-05-30
tags: [llm, ai-agents, prompt-optimization, evolutionary-search, reinforcement-learning]
status: developing
complexity: advanced
domain: llm
aliases: ["Genetic-Pareto", "Reflective Prompt Evolution"]
related: ["[[Pareto-based Candidate Selection]]", "[[Language Feedback as Learning Signal]]", "[[Compound AI System]]", "[[Prompt Optimization]]", "[[GRPO]]", "[[Heuristic Learning]]", "[[Evaluator-Optimizer]]", "[[DSPy]]"]
sources: ["[[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]"]
---

# GEPA

**GEPA (Genetic-Pareto)** is a sample-efficient prompt optimizer for [[Compound AI System|compound AI systems]] that merges **natural-language reflection** with **multi-objective evolutionary search**. Given any LLM system with one or more prompts, GEPA samples trajectories, reflects on them in language to diagnose failures, mutates prompts, and combines complementary lessons from a Pareto frontier of its own attempts — turning *a few* rollouts into large quality gains ([[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]; confidence: high).

## The three pillars

1. **Genetic optimization loop** — a candidate pool starts with the base system; each new candidate is derived from an ancestor via **reflective mutation** or **crossover (Merge)**, inheriting lessons along a genetic tree. Keep a variant only if it beats its parent on a minibatch, then evaluate on the full pareto set.
2. **Reflective prompt mutation** — trace a candidate's execution on a minibatch; a **feedback function `µ_f`** returns score + `feedback_text`; a reflection LM does **implicit credit assignment** and rewrites *one* module's prompt (round-robin selection). See [[Language Feedback as Learning Signal]].
3. **[[Pareto-based Candidate Selection]]** — sample from the per-instance Pareto frontier (weighted by how many tasks each candidate leads) instead of always mutating the global best. This "illumination" escapes local optima.

## Why it works

- **Language is a richer signal than scalar reward.** Execution traces *and* evaluation traces (compiler errors, failed rubrics) carry far more learning signal than the single number GRPO sees — see [[Language Feedback as Learning Signal]].
- **A good edit jumps, a gradient nudges.** A reflective rewrite can lift the whole system in one step, where policy gradients need thousands of rollouts. Same logic as [[Heuristic Learning]] in code-space.
- **Diversity beats greed.** Pareto sampling keeps multiple "winning" strategies alive, so the search doesn't burn its budget refining one local optimum.

## Headline results

- Beats **[[GRPO]]** (24k rollouts) by up to **20%** using up to **35× fewer rollouts**; up to **78×** more sample-efficient to match GRPO's best validation.
- Beats **MIPROv2** by **>10%** aggregate (+13.33% with Merge on GPT-4.1-Mini vs +5.64%).
- **Instruction-only > joint instruction+few-shot**; GEPA prompts are declarative and up to **9.2× shorter**.
- **Cross-model transfer:** Qwen3-8B-optimized prompts gain **+9%** on GPT-4.1-Mini, beating optimizers run directly on the target.

## Beyond optimization

- **Inference-time search:** overfit the task set → NPU kernels 4.25%→30.52% utilization (no runtime RAG); CUDA `fast_1` ~0%→>20%.
- **Adversarial prompt search:** invert the reward → a universal distractor dropped GPT-5-Mini AIME pass@1 from 76%→10% (reusable robustness probe; cf. [[Reward Hacking]]).

## Relationship to neighbors

- **[[Heuristic Learning]]** — prompt-space twin. HL edits *code*, GEPA edits *prompts*; both learn by reflecting on traces/tests in an interpretable medium rather than taking gradient steps.
- **[[Evaluator-Optimizer]]** — GEPA is this loop scaled with evolutionary Pareto search and explicit ancestry.
- **[[DSPy]] / MIPROv2** — GEPA is the reflective-evolutionary optimizer in this framework lineage.
- **[[Verifiability]]** — operates in the RLVR setting but argues *language* feedback dominates the scalar reward RLVR collapses to.

## Open questions

- When to invoke **Merge** crossover and how to split budget between mutation and crossover (helped GPT-4.1-Mini, hurt Qwen3-8B under fixed hyperparams).
- Most of GEPA's budget is validation for candidate selection, not learning — can dynamic validation subsets cut it?

## Sources

- [[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]
