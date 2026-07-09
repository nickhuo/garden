---
type: concept
title: Verbal Reinforcement Learning
created: 2026-06-18
updated: 2026-06-18
tags: [ai-agents, llm, reinforcement-learning, memory, continual-learning]
status: developing
aliases: ["Reflexion", "Verbal RL", "Self-Reflection"]
related: ["[[ReAct]]", "[[Language Feedback as Learning Signal]]", "[[Verifiability]]", "[[Self-Editing Memory]]", "[[Agent Memory Taxonomy]]", "[[Evaluator-Optimizer]]", "[[CoALA]]", "[[Online Learning from Interaction]]"]
sources: ["[[2023-03-20 - Shinn et al - Reflexion]]"]
---

# Verbal Reinforcement Learning

The framework introduced by **[[2023-03-20 - Shinn et al - Reflexion|Reflexion]]** (Shinn et al. 2023):
reinforce a language agent **through linguistic feedback instead of weight updates**. A (sparse) task
reward is converted by a dedicated LLM into a **natural-language self-reflection** — a diagnosis of
what failed and what to change — which is stored in an **episodic memory buffer** and prepended to
the agent's context on the next trial. "Policy improvement" happens in the prompt, not the parameters.

## The loop

```
Actor → trajectory → Evaluator → reward → Self-Reflection → verbal lesson → memory → (retry)
```

- **Actor** — a [[ReAct]]- or CoT-style agent that acts in the environment.
- **Evaluator** — produces the reward (exact-match, self-written unit tests, or environment signal).
- **Self-Reflection model** — turns trajectory + reward into the verbal lesson. This is the learner.
- **Memory** — short-term (current trajectory) + long-term (last *N* reflections).

## Why it works

The reward's underlying failure trace — a compiler error, a failed test, a wrong final answer — is
**already in language**. Collapsing it to a scalar and running policy gradients throws that structure
away and needs thousands of rollouts to integrate one lesson. Reflecting on the trace exploits the
LLM's language priors and extracts far more signal **per rollout** — Reflexion fixes a task in a
handful of retries. This is the agentic, memory-carrying 2023 ancestor of the principle
[[Language Feedback as Learning Signal]] (GEPA, 2026) later formalizes.

## Where it sits

- **vs scalar RL ([[RL with Verifiable Rewards]] / [[GRPO]])** — same verifiable-reward setting, but
  keeps the reward's reasoning in language and updates context, not weights. See [[Verifiability]].
- **vs [[Evaluator-Optimizer]]** — Reflexion *is* an evaluator-optimizer loop plus a persistent
  reflection memory across trials.
- **In [[CoALA]] terms** — supplies the *learning* internal action + episodic memory that plain
  [[ReAct]] lacks.
- **Memory** — the reflection buffer is a self-written episodic store ([[Self-Editing Memory]],
  [[Agent Memory Taxonomy]]); a form of [[Online Learning from Interaction]] via memory write-back.

## Limits / open questions

- Needs a usable Evaluator — degrades where success isn't checkable ([[Verifiability]]'s boundary).
- Reflection quality is load-bearing; a bad self-reflection can entrench a wrong fix.
- Memory is bounded (last *N*) — long-horizon reflection accumulation/forgetting is unaddressed.

## Sources

- [[2023-03-20 - Shinn et al - Reflexion]] — entities [[Noah Shinn]], [[Shunyu Yao]], [[Karthik Narasimhan]]
