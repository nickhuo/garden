---
type: source
title: "Reflexion: Language Agents with Verbal Reinforcement Learning"
created: 2026-06-18
updated: 2026-06-18
tags: [ai-agents, llm, reinforcement-learning, memory, reasoning]
status: developing
source_type: paper
author: Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao
date_published: 2023-03-20
url: https://arxiv.org/abs/2303.11366
confidence: high
seed_score: 14/14
aliases: ["2023 - Shinn et al - Reflexion", "Reflexion paper", "Verbal Reinforcement Learning"]
related: ["[[Verbal Reinforcement Learning]]", "[[ReAct]]", "[[Language Feedback as Learning Signal]]", "[[Verifiability]]", "[[Self-Editing Memory]]", "[[CoALA]]", "[[Evaluator-Optimizer]]", "[[Shunyu Yao]]", "[[Noah Shinn]]", "[[Karthik Narasimhan]]"]
sources: ["[[.raw/articles/2023-03-20 - Shinn et al - Reflexion]]"]
cited_sources: ["[[2022-10-06 - Yao et al - ReAct]]"]
key_claims:
  - "Reflexion reinforces a language agent without any weight updates — it converts a (sparse) task reward into a natural-language self-reflection and stores it in an episodic memory buffer that conditions the next attempt."
  - "Three-model loop: Actor (generates trajectory, ReAct/CoT-style), Evaluator (scores it), Self-Reflection model (writes the verbal lesson). Only the prompt/memory changes between trials, never the weights."
  - "Achieves 91% pass@1 on HumanEval, beating GPT-4's 80%, by having the model write and run its own unit tests as a self-evaluated reward signal."
  - "Verbal reflection extracts far more signal per rollout than a scalar reward because the failure trace is already in language — the same bet GEPA later formalizes as Language Feedback as Learning Signal."
  - "Reflection memory is the load-bearing component: ablating it collapses performance toward the baseline."
---

# Reflexion: Language Agents with Verbal Reinforcement Learning

## Summary

Reflexion makes a language agent **learn from its own failures without touching the weights**. After
a failed trial, a dedicated LLM reads the trajectory plus the (often sparse) reward and writes a
**verbal self-reflection** — a natural-language diagnosis of what went wrong and what to do
differently. That reflection is appended to an **episodic memory buffer** and prepended to the
agent's context on the next attempt. The agent retries; the loop repeats until it passes or hits a
trial cap. "Reinforcement" here is **linguistic feedback in context**, not policy-gradient on
parameters.

This is the canonical instance of the principle the wiki already describes on [[Verifiability]] and
[[Language Feedback as Learning Signal]]: when the reward's underlying trace is itself in language
(a compiler error, a failed unit test, a wrong answer), *reflecting* on that trace beats collapsing
it to a scalar and running policy gradients — at a fraction of the rollouts.

## The three-model loop

| Model | Role |
|---|---|
| **Actor** `M_a` | Generates the trajectory (text + actions). Built on [[ReAct]] or chain-of-thought. Conditioned on the long-term reflection memory. |
| **Evaluator** `M_e` | Scores the trajectory. Reward source is task-dependent: exact-match/heuristics (reasoning), self-written unit tests (coding), environment success signal (decision-making). |
| **Self-Reflection** `M_sr` | Given trajectory + reward, emits a *verbal* lesson. This is the "learning" step. |

**Memory.** Short-term = the current trajectory. Long-term = a buffer of the last *N* (≈1–3) verbal
reflections. No fine-tuning — capability accumulates in text.

```
trial → evaluate → (if fail) reflect → store reflection → retry
```

## Results

- **Coding — HumanEval: 91% pass@1**, vs GPT-4's 80%. The trick is a **self-evaluated reward**: the
  model writes its own unit tests, runs them, and reflects on failures. Also strong on MBPP / Leetcode Hard.
- **Decision-making — ALFWorld:** ~+22 pts absolute over a [[ReAct]] baseline across 12 trials;
  reflection fixes both hallucinated actions and inefficient plans.
- **Reasoning — HotPotQA:** ~+20 pts absolute over CoT/ReAct via reflective retries.

## Three feedback types it can absorb

1. **Scalar / binary** environment reward (or exact-match).
2. **Self-evaluated** reward — the model generates and runs unit tests (internally simulated signal).
3. **Free-form language** — e.g. interpreter/compiler error messages.

## Ablations

- Remove the episodic reflection memory → performance falls back to baseline. The memory, not the
  retry, is what learns.
- Reflection quality (and, in coding, unit-test quality) is the variable that moves the score.

## Connections

- **[[Verbal Reinforcement Learning]]** — the named framework this paper introduces (concept page).
- **[[ReAct]]** — the Actor's backbone and direct ancestor (same authors Yao & [[Karthik Narasimhan]]); see Lineage below.
- **[[Language Feedback as Learning Signal]]** — Reflexion is the 2023 predecessor of the GEPA (2026) thesis that language feedback > scalar reward.
- **[[Verifiability]]** — Reflexion only works where the Evaluator can produce a trustworthy signal (tests, graders, environments); it is the in-context counterpart to RLVR's weight-space version.
- **[[Self-Editing Memory]]** / **[[Agent Memory Taxonomy]]** — the reflection buffer is an episodic, self-written long-term memory.
- **[[Evaluator-Optimizer]]** — Reflexion is the agentic, memory-carrying generalization of the generate→evaluate→refine loop.
- **[[CoALA]]** — fills the *learning* internal action that plain [[ReAct]] lacks (CoALA explicitly maps Reflexion as the episodic-memory + learning point in the design space).

## Lineage / 引用脉络

Reflexion is an extension of **[[2022-10-06 - Yao et al - ReAct|ReAct]]** (Yao et al. 2022, ICLR 2023)
— same lead lab, two shared authors ([[Shunyu Yao]], [[Karthik Narasimhan]]). ReAct gives the Actor
its reason→act→observe loop; Reflexion wraps that loop in an evaluate→reflect→remember outer loop.
ReAct passed the seed gate on the one-hop citation chase (14/14) and is filed as its own source page.

Other cited works **below the chase bar or already covered**:
- **Chain-of-Thought** (Wei et al. 2022) — foundational but not chased this pass; candidate for a future ingest.
- **Self-Refine** (Madaan et al. 2023) — concurrent self-feedback work (single-task, no memory); noted, not filed.
- **Tree of Thoughts** (Yao et al. 2023) — already a wiki concept ([[Tree of Thoughts]]); source not yet ingested.
- **Generative Agents** (Park et al. 2023) — already filed: [[2023-04-07 - Park et al - Generative Agents]].
