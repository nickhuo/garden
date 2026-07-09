---
source_url: https://arxiv.org/abs/2303.11366
fetched: 2026-06-18
---

# Reflexion: Language Agents with Verbal Reinforcement Learning

**Authors:** Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao
**arXiv:** 2303.11366 — submitted 2023-03-20 (v1), revised through v4 2023-10-10. Published at NeurIPS 2023.
**License:** CC BY 4.0

## Abstract

Large language models (LLMs) have been increasingly used to interact with external environments
(e.g., games, compilers, APIs) as goal-driven agents. However, it remains challenging for these
language agents to quickly and efficiently learn from trial-and-error as traditional reinforcement
learning methods require extensive training samples and expensive model fine-tuning. We propose
Reflexion, a novel framework to reinforce language agents not by updating weights, but instead
through linguistic feedback. Concretely, Reflexion agents verbally reflect on task feedback signals,
then maintain their own reflective text in an episodic memory buffer to induce better
decision-making in subsequent trials. Reflexion is flexible enough to incorporate various types
(scalar values or free-form language) and sources (external or internally simulated) of feedback
signals, and obtains significant improvements over a baseline agent across diverse tasks (sequential
decision-making, coding, language reasoning). For example, Reflexion achieves a 91% pass@1 accuracy
on the HumanEval coding benchmark, surpassing the previous state-of-the-art GPT-4 that achieves 80%.

## Method

Three models in a loop:
- **Actor (M_a):** an LLM (ReAct- or CoT-style) that generates text and actions, producing a
  trajectory in the environment. Conditioned on the long-term reflection memory.
- **Evaluator (M_e):** scores the trajectory. Reward sources vary by task: exact-match / heuristics
  (reasoning), unit tests written by the model (coding), environment success signal (decision-making).
- **Self-Reflection (M_sr):** an LLM that, given the trajectory + the (sparse) reward, produces a
  *verbal* self-reflection — a natural-language diagnosis of what went wrong and what to do
  differently. This text is appended to the episodic memory buffer.

**Memory:** short-term = the current trajectory; long-term = a buffer of the last N (e.g. 1–3) verbal
reflections, prepended to the Actor's context on the next trial. No weight updates.

**Loop:** trial → evaluate → reflect (if failed) → store reflection → retry, until pass or max trials.

## Results

- **Coding — HumanEval:** 91% pass@1 (GPT-4 baseline 80%). Also strong on MBPP and Leetcode Hard.
  Introduces a self-generated unit-test signal; ablation shows test quality matters.
- **Decision-making — ALFWorld:** +22 percentage-point absolute improvement over ReAct baseline
  (to ~97–130/134 tasks across 12 trials); reflection resolves both hallucination and inefficient
  planning failure modes.
- **Reasoning — HotPotQA:** +20 percentage-point absolute improvement over CoT/ReAct baselines via
  reflective retries.

## Feedback types

1. **Scalar / binary** reward from the environment or exact-match.
2. **Self-evaluated** reward (model writes unit tests, then runs them — internally simulated).
3. **Free-form language** feedback (e.g. compiler / interpreter error messages).

## Ablations

- Removing the episodic reflection memory collapses performance back toward the baseline.
- Reflection quality (and unit-test quality in coding) is the load-bearing variable.

## Key references

- **ReAct** (Yao et al. 2022, arXiv 2210.03629) — the Actor's reasoning+acting loop Reflexion extends.
- **Chain-of-Thought** (Wei et al. 2022) — the alternative Actor backbone.
- **Self-Refine** (Madaan et al. 2023) — concurrent self-feedback-without-RL work (single-task, no memory).
- **Tree of Thoughts** (Yao et al. 2023) — deliberate search alternative.
- **Generative Agents** (Park et al. 2023) — reflection-into-memory contemporary.
- Benchmarks: HumanEval (Chen et al. 2021), MBPP, ALFWorld (Shridhar et al. 2021), HotPotQA (Yang et al. 2018).
