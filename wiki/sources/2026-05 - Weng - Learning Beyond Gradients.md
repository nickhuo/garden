---
type: source
title: "2026-05 - Weng - Learning Beyond Gradients"
created: 2026-05-29
updated: 2026-05-29
tags: [llm, ai-agents, reinforcement-learning, continual-learning, source]
status: mature
source_type: blog
author: Jiayi Weng
date_published: 2026-05
url: https://trinkle23897.github.io/learning-beyond-gradients/
confidence: high
seed_score: 13/14
key_claims:
  - "Heuristic Learning (HL): coding agents continuously edit program/rule-based policies from feedback, instead of training neural-network weights by gradient descent."
  - "HL partially solves catastrophic forgetting because old capabilities live in rule sets, regression tests, and golden replays — not only in weights."
  - "HL was infeasible before because human maintenance of heuristics has exponential cost; coding agents flatten that maintenance curve (the Industrial-Revolution analogy)."
  - "Coupling complexity — the strategy complexity a coding agent can maintain — is the binding constraint, set by both code-side (modularity, tests, rollback) and agent-side (model capability, context, tools) factors."
  - "Pure-code policies reach Deep-RL-competitive scores: Breakout 864 (theoretical max), HalfCheetah 11836.7, Ant 6000+, VizDoom CV-only 0.944; Atari57 median HNS above PPO at equal steps."
  - "Proposed next paradigm after Pretraining → RLHF → RL/RLVR: 'anything that can be continuously iterated on becomes solvable.' For robotics, a System-1 (shallow NN + HL) / System-2 (LLM agent) split."
cited_sources: []
related: ["[[Heuristic Learning]]", "[[Jiayi Weng]]", "[[Online Learning from Interaction]]", "[[Model-Centric Architecture]]", "[[The Bitter Lesson]]", "[[Software 2.0]]", "[[Self-Evolving Agent Environments]]", "[[Evaluator-Optimizer]]", "[[Verifiability]]"]
sources: ["[[.raw/articles/2026-05 - Weng - Learning Beyond Gradients.md]]"]
---

# 2026-05 - Weng - Learning Beyond Gradients

> [!key-insight] One-line
> A coding agent that keeps **editing rule-based code from feedback** is itself a learning system — and on Atari/MuJoCo/VizDoom it reaches Deep-RL-competitive scores **without training any network**.

## Summary

Jiayi Weng (author of Tianshou / EnvPool, RL infra — see [[Jiayi Weng]]) argues for **[[Heuristic Learning]]** (HL): treat a *coding agent iterating on program code* as a learning loop that competes with gradient-based Deep RL on control tasks, while being explainable, sample-efficient, regression-testable, and partially immune to **catastrophic forgetting**. The pitch is not "rules beat networks" — it's that the thing that historically killed rule-based AI (unbounded human maintenance cost) is removed once a coding agent does the maintenance. That shifts the feasibility frontier: "anything that can be continuously iterated on starts to become solvable."

See [[Heuristic Learning]] for the full concept (definition, the HL-vs-Deep-RL table, coupling complexity, the experimental results, and the System-1/System-2 robotics proposal).

## Why it scored 13/14 (seed gate)

Primary first-hand research with a public artifact repo (code + videos + data), credible author, concrete reproducible numbers across five benchmark families, a genuinely novel framing, and very recent (2026-05). Docked one point on **citation hygiene** — it's a blog post naming baselines (PPO2, CleanRL, OpenRL Benchmark) and a repo rather than a formal reference list. → `confidence: high`.

## What's new vs. the existing wiki

- Adds a **new row to the real-time-learning durability spectrum** in [[Online Learning from Interaction]]: *update the code, not the weights* — a distinct adaptation mechanism that page's table did not have.
- Sharpens the [[Model-Centric Architecture]] slider: HL is the **code-centric pole pushed to its limit**, in direct tension with [[Software 2.0]] / [[The Bitter Lesson]] (see the contradiction callout on [[Model-Centric Architecture]]).
- The coding-agent-iterates-on-code loop is a control-task cousin of [[Evaluator-Optimizer]] and [[Self-Evolving Agent Environments]].

## Lineage / 引用脉络

**Citation chase: none filed.** Every external reference is a **code repo or RL baseline**, not a chaseable primary article: EnvPool (`sail-sg/envpool`), the artifact repo (`Trinkle23897/learning-beyond-gradients`), OpenRL Benchmark / CleanRL / OpenAI Baselines PPO2, and Gymnasium environments. These are tooling/baselines (would not pass the source seed gate as standalone "sources"), so `cited_sources: []`. The repo itself is the primary evidence and is linked from this page's `url`/raw archive.
