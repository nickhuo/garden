---
type: source
title: "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning"
created: 2026-05-30
updated: 2026-05-30
tags: [llm, ai-agents, prompt-optimization, reinforcement-learning, evolutionary-search]
status: mature
source_type: paper
authors: ["Lakshya A Agrawal", "Shangyin Tan", "Dilara Soylu", "Omar Khattab", "Matei Zaharia", "et al."]
venue: "ICLR 2026 (Oral)"
arxiv: "2507.19457v2"
url: https://arxiv.org/abs/2507.19457
code: https://github.com/gepa-ai/gepa
seed_score: 14/14
confidence: high
related: ["[[GEPA]]", "[[Pareto-based Candidate Selection]]", "[[Language Feedback as Learning Signal]]", "[[Compound AI System]]", "[[Prompt Optimization]]", "[[Heuristic Learning]]", "[[Omar Khattab]]", "[[DSPy]]"]
sources: []
---

# GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning

> [!key-insight] Core claim
> The **interpretable nature of language** is a richer learning medium for LLMs than policy gradients from sparse scalar rewards. **GEPA** (Genetic-Pareto) turns a *few* rollouts into large quality gains by reflecting on execution traces in natural language — beating **GRPO** by up to **20%** while using up to **35× fewer rollouts**, and the leading prompt optimizer **MIPROv2** by **>10%**.

## What it is

A research paper (UC Berkeley, Stanford, MIT, Databricks, Bespoke Labs, Notre Dame) introducing **GEPA**, a reflective prompt optimizer for [[Compound AI System|compound AI systems]]. Last author **[[Omar Khattab]]** (creator of [[DSPy]]); senior authors Matei Zaharia, Ion Stoica, Dan Klein, Christopher Potts, Alexandros Dimakis. Accepted as an **ICLR 2026 Oral**. Code at `gepa-ai/gepa`.

## The argument

RL with Verifiable Rewards (RLVR), e.g. [[GRPO]], collapses a whole rollout into one scalar reward and typically needs **tens to hundreds of thousands of rollouts** to fit a new task. But every rollout is already serializable into **natural-language traces** — module instructions, reasoning chains, tool calls, and even the reward function's internals (compiler errors, failed rubrics) before they are crushed into a scalar. GEPA's thesis: *algorithms that learn deliberately in language by reflecting on these traces* exploit LLMs' language priors far better than policy gradients. See [[Language Feedback as Learning Signal]].

## How GEPA works

Three pillars (full algorithm in the paper's Fig. 4):

1. **Genetic prompt evolution** — a candidate pool seeded with the base system; new candidates derived by **reflective mutation** or **crossover (Merge)**, each inheriting lessons from its parents along a genetic tree.
2. **Reflective prompt mutation** — execute a candidate on a minibatch, trace it, run a **feedback function `µ_f`** that returns score + `feedback_text` (including evaluation-trace detail like compiler errors), then a reflection LM does **implicit credit assignment** and rewrites one module's prompt (round-robin module selection). Keep the variant only if minibatch score improves; then evaluate on the full `D_pareto` set.
3. **[[Pareto-based Candidate Selection]]** — instead of always mutating the global best (which traps in local optima), GEPA keeps the **Pareto frontier** of best candidates *per task instance* and samples among them weighted by how many tasks each leads. A quality-diversity "illumination" strategy (Mouret & Clune 2015).

> [!key-insight] Two trace types
> **Execution trace** = what the LLM produces. **Evaluation trace** = what the environment produces to compute the reward (compiler/profiler output before it becomes a scalar). GEPA's `µ_f` harvests *both* for reflection — and feedback can be **module-specific** (e.g. per-hop in multi-hop QA). Connects to [[Error Trace Retention]] and [[Trace-Based Evaluation]].

## Key results

**Qwen3 8B** (Table 1) — GEPA beats GRPO (24k rollouts) on 5/6 tasks using **687–7051** rollouts total:

| | Baseline | GRPO | MIPROv2 | **GEPA** |
|---|---|---|---|---|
| Aggregate | 45.23 | 48.91 | 47.84 | **54.85** (+9.62) |
| HotpotQA | 42.33 | 43.33 | 55.33 | **62.33** |
| IFBench | 36.90 | 35.88 | 36.22 | **38.61** (678 rollouts vs GRPO's 24k) |

**GPT-4.1 Mini** (Table 2) — GEPA+Merge **+13.33%** aggregate vs MIPROv2's +5.64%. GEPA works off-the-shelf on closed models.

- **Sample efficiency:** matches GRPO's best validation after as few as 6–179 *train* rollouts → up to **78×** efficiency.
- **Instruction-only beats joint instruction+few-shot** (vs MIPROv2), reversing prior findings — attributed to better instruction-following / self-reflection in modern LLMs. GEPA prompts are **declarative** and up to **9.2× shorter** than MIPROv2's, with a lower generalization gap.
- **Pareto selection** drives the win: +12.44% vs +6.05% (SelectBest, à la TextGrad) and +5.11% (BeamSearch, à la APO).
- **Cross-model transfer:** prompts optimized on weak Qwen3-8B score **+9%** on GPT-4.1-Mini — beating MIPROv2/TextGrad/Trace that optimized *directly* on the target.

## Extended applications

- **Inference-time search** (overfit the task set as both train and pareto): NPU kernels (XDNA2/NPUEval) **4.25% → 30.52%** mean vector utilization with GPT-4o, *no runtime RAG*; CUDA kernels (KernelBench) — `fast_1` from ~0% to >20%. `µ_f` dynamically injects manual sections retrieved from compiler errors.
- **Adversarial prompt search** (invert the reward): a single universal distractor instruction (trivia + strict format directive) dropped GPT-5 Mini's AIME-2025 pass@1 from **76% → 10%** — a reusable robustness stress test.

## Lineage / 引用脉络

GEPA is itself the primary source; its ~100 references are foundational works, mostly already represented conceptually in the wiki. Key related work (cited, not separately chased):

- **[[GRPO]]** (Shao et al. 2024) — the RLVR baseline GEPA outperforms; uses LoRA ([[LoRA]]) here.
- **MIPROv2** (Opsahl-Ong et al. 2024) — prior SOTA prompt optimizer (joint instruction + few-shot via Bayesian opt); GEPA's main prompt-optimizer baseline. Co-author Krista Opsahl-Ong is on GEPA too.
- **[[DSPy]]** (Khattab et al. 2022, 2024) — the compound-AI-system framework GEPA's formalism inherits (`Φ = (M, C, X, Y)`).
- **TextGrad** (Yuksekgonul et al. 2025) — backprops textual feedback; its candidate selection = GEPA's `SelectBestCandidate` ablation. **Trace/OptoPrime** (Cheng et al. 2024) — another baseline.
- **Reflexion** (Shinn et al. 2023) / **Self-Refine** (Madaan et al. 2023) — in-context self-improvement antecedents to reflective mutation.
- **EvoPrompt** (Guo et al. 2024), **AlphaEvolve** (Novikov et al. 2025) — evolutionary prompt/code search; **MAP-Elites illumination** (Mouret & Clune 2015) for Pareto sampling.

## Why it matters for this wiki

GEPA is the **prompt-space twin** of [[Heuristic Learning]] (Weng): both reject gradient descent in favor of *learning in an interpretable medium an LLM edits directly* (prompts vs code), driven by trace/test feedback. It also operationalizes [[Verifiability]]'s RLVR setting while arguing language feedback > scalar reward, and is a concrete instance of the [[Evaluator-Optimizer]] loop scaled with evolutionary search.

## Open questions (from the paper)

- Optimal budget split between mutation and **Merge** crossover, and *when* to invoke Merge (helped GPT-4.1-Mini, hurt Qwen3-8B under fixed hyperparams).
- Shrinking the validation cost (most of GEPA's budget is candidate-selection validation, not learning) via dynamic validation subsets.
- How far inference-time-search generalizes beyond code generation.
