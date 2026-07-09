---
source_url: https://arxiv.org/abs/2210.03629
fetched: 2026-06-18
---

# ReAct: Synergizing Reasoning and Acting in Language Models

**Authors:** Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
**arXiv:** 2210.03629 — submitted 2022-10-06 (v1), camera-ready v3 2023-03-10. Published at **ICLR 2023**.

## Abstract

While large language models (LLMs) have demonstrated impressive performance across tasks in language
understanding and interactive decision making, their abilities for reasoning (e.g. chain-of-thought
prompting) and acting (e.g. action plan generation) have primarily been studied as separate topics.
ReAct explores the use of LLMs to generate both reasoning traces and task-specific actions in an
interleaved manner, allowing for greater synergy between the two: reasoning traces help the model
induce, track, and update action plans as well as handle exceptions, while actions allow it to
interface with and gather additional information from external sources such as knowledge bases or
environments.

## Method

Interleave **reasoning traces** (internal "thoughts") with **actions** (external tool/environment
calls) and **observations** in a single prompted loop: thought → action → observation → thought …
Reasoning lets the agent plan and revise; acting grounds the reasoning in real observations,
reducing the hallucination that pure chain-of-thought suffers. Few-shot prompted (1–6 exemplars).

## Results

- **HotPotQA / FEVER:** uses a Wikipedia API; overcomes CoT hallucination/error-propagation and
  produces interpretable, human-aligned trajectories.
- **ALFWorld:** +34% absolute success rate over imitation/RL methods, with only 1–2 in-context examples.
- **WebShop:** +10% absolute over baselines.

## Prior work it builds on

- **Chain-of-Thought** (Wei et al. 2022) — reasoning-only prompting; ReAct adds grounding actions.
- **SayCan** (Ahn et al. 2022), **Inner Monologue** (Huang et al. 2022) — acting/grounding without
  interleaved reasoning traces.
