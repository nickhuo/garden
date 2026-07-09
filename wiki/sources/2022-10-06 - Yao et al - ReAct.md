---
type: source
title: "ReAct: Synergizing Reasoning and Acting in Language Models"
created: 2026-06-18
updated: 2026-06-18
tags: [ai-agents, llm, reasoning, decision-making, tool-use]
status: developing
source_type: paper
author: Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
date_published: 2022-10-06
url: https://arxiv.org/abs/2210.03629
confidence: high
seed_score: 14/14
aliases: ["2022 - Yao et al - ReAct", "ReAct paper", "Reasoning and Acting"]
related: ["[[ReAct]]", "[[Tree of Thoughts]]", "[[CoALA]]", "[[Think Tool]]", "[[Augmented LLM]]", "[[Shunyu Yao]]", "[[Karthik Narasimhan]]"]
sources: ["[[.raw/articles/2022-10-06 - Yao et al - ReAct]]"]
cited_sources: []
key_claims:
  - "ReAct interleaves reasoning traces (internal thoughts) with task actions (external calls) in one prompted loop — thought → action → observation → thought — so the two capabilities reinforce each other instead of being studied separately."
  - "Grounding reasoning in real observations reduces the hallucination and error-propagation that pure chain-of-thought suffers on knowledge-intensive tasks (HotPotQA, FEVER)."
  - "On ALFWorld, ReAct beats imitation/RL methods by 34% absolute success with only 1–2 in-context examples; on WebShop, +10% absolute."
  - "ReAct is the default skeleton of modern tool-using agents and the Actor backbone that Reflexion extends with an evaluate-reflect-remember outer loop."
---

# ReAct: Synergizing Reasoning and Acting in Language Models

## Summary

ReAct (Reason + Act) prompts an LLM to **interleave reasoning traces with actions** in a single
loop: a "thought" plans or revises, an "action" calls an external tool/environment, an "observation"
returns, and the next thought conditions on it. Reasoning alone hallucinates and can't gather facts;
acting alone can't plan or handle exceptions — interleaving them grounds the reasoning in
observations and lets observations steer the reasoning. It is few-shot prompted (1–6 exemplars) and
needs no fine-tuning.

This is the **conceptual ancestor of most tool-using agents today** and the Actor backbone of
[[2023-03-20 - Shinn et al - Reflexion|Reflexion]] (which reached this page on the citation chase).

## Method

```
thought → action → observation → thought → action → …
```

- **Reasoning traces** are free-text "thoughts" that induce, track, and update a plan and handle exceptions.
- **Actions** interface with external sources (Wikipedia API, embodied environment, web store).
- The synergy is the contribution: neither reasoning-only (CoT) nor acting-only baselines match it.

## Results

- **HotPotQA / FEVER:** with a Wikipedia API, ReAct overcomes CoT's hallucination/error-propagation
  and produces **interpretable, human-aligned trajectories**.
- **ALFWorld:** **+34% absolute** success over imitation/RL methods, with only 1–2 in-context examples.
- **WebShop:** **+10% absolute** over baselines.

## Prior work it builds on

- **Chain-of-Thought** (Wei et al. 2022) — reasoning-only prompting; ReAct adds grounding actions.
- **SayCan** (Ahn et al. 2022), **Inner Monologue** (Huang et al. 2022) — grounding/acting without
  interleaved reasoning traces.

## Connections

- **[[ReAct]]** — the concept page (mechanism, CoALA placement, descendants). This source grounds it.
- **[[Tree of Thoughts]]** — adds deliberate search over reasoning paths, the evaluation step ReAct lacks.
- **[[CoALA]]** — places ReAct as the minimal "working-memory only, no learning action" point in the design space.
- **[[Think Tool]]** — carves the reasoning-only internal action out as an explicit tool.
- **[[Verbal Reinforcement Learning]]** / **[[2023-03-20 - Shinn et al - Reflexion]]** — wrap ReAct in a reflect-and-remember outer loop.
