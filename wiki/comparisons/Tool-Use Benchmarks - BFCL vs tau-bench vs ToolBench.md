---
type: comparison
title: "Tool-Use Benchmarks — BFCL vs τ-bench vs ToolBench"
created: 2026-05-22
updated: 2026-05-22
tags:
- ai-agents
- evaluation
- benchmark
- tool-use
status: developing
related:
- "[[BFCL]]"
- "[[tau-bench]]"
- "[[ToolBench]]"
- "[[Agent Eval Pyramid]]"
- "[[LLM-as-Judge Evaluation]]"
- "[[Pass^k Reliability Metric]]"
sources:
- "[[2025-07 - Patil et al - BFCL]]"
- "[[2024-06-17 - Yao et al - tau-bench]]"
- "[[2023-07-31 - Qin et al - ToolLLM]]"
---

# Tool-Use Benchmarks — BFCL vs τ-bench vs ToolBench

The three benchmarks most cited for LLM tool/function-calling evaluation. They are **not interchangeable** — each measures a different axis, and a model can top one while failing another.

## At a glance

| | [[BFCL]] | [[tau-bench]] | [[ToolBench]] |
|---|---|---|---|
| Origin | UC Berkeley ([[Gorilla]]), ICML 2025 | [[Sierra]], 2024 | Tsinghua/[[OpenBMB]], ICLR'24 |
| Paper | [[2025-07 - Patil et al - BFCL]] | [[2024-06-17 - Yao et al - tau-bench]] | [[2023-07-31 - Qin et al - ToolLLM]] |
| **Measures** | call **correctness** at scale | task **reliability** under interaction | **generalization** across many APIs |
| Scale | 1000s of functions | 165 tasks, 2 domains | 16,464 real APIs, 49 categories |
| Grading | **AST match** (+ executable) | **DB-state equality** (deterministic) | **ToolEval** ([[LLM-as-Judge Evaluation]]) |
| User in loop | no (scripted turns) | **yes** (LM user simulator) | no |
| Key metric | accuracy per category | **pass^k** ([[Pass^k Reliability Metric]]) | Pass Rate / Win Rate |
| Faithfulness | high (structural) | **highest** (ground truth) | lowest (judge bias) |
| Cost / scalability | **cheapest** (no exec) | expensive (~$200/trial) | cheap but API-flaky |

## The three axes

- **BFCL — breadth of correctness.** Can the model emit a *syntactically and semantically correct call*, choosing among many functions, in parallel, and abstaining when none fit? Deterministic AST grading scales to thousands of functions. Says little about whether the call *accomplishes a multi-step goal*.
- **τ-bench — depth of reliability.** Tiny, hand-built, deterministic domains, but a **live LM user** and a **policy document** force long-horizon, rule-following interaction. Its [[Pass^k Reliability Metric]] exposes that pass^1 ≈ 60% can hide pass^8 < 25%. The only one of the three that measures *consistency*, not just peak capability.
- **ToolBench — breadth of generalization.** 16k+ real RapidAPI endpoints test whether a model composes *unfamiliar, messy* tools. Fully automated (instructions + solution paths from ChatGPT), graded by an LLM judge. Most scalable, least faithful; live-API instability spawned StableToolBench.

## Where they sit on the [[Agent Eval Pyramid]]

- BFCL (V1–V3) and ToolBench grade **steps** (was the call right?) → lower tiers / [[Trace-Based Evaluation]].
- τ-bench grades **end state** (did the task complete?) → Tier 3, end-to-end.
- **Convergence:** BFCL **V4** ("from tool use to agentic evaluation") adds multi-turn, memory, and web-search — climbing toward τ-bench's territory. The field is collapsing the step/outcome distinction.

## Grading-philosophy spectrum

Deterministic ←──────────────────→ LLM-judged
**τ-bench** (DB-state) · **BFCL** (AST) · **ToolBench** (ToolEval)

Faithfulness trades against scalability. τ-bench's determinism requires artificially unique outcomes (only works in rule-constrained domains); ToolBench's LLM judge works anywhere but inherits judge bias (see [[Eval Validity]], [[LLM-as-Judge Evaluation]]).

## Practical takeaway

> [!key-insight] Pick the benchmark to the question
> - Picking/formatting tool calls → **BFCL**.
> - Will it hold up in a real customer-service loop → **τ-bench** (and look at pass^k, not pass^1).
> - Will it generalize to APIs it never saw → **ToolBench**.
> A high BFCL score is necessary but not sufficient for deployment; τ-bench's pass^k collapse is the warning that single-call correctness ≠ reliable agent. This is the empirical backbone of [[Workflows Beat Agents for Most Production]].

## Open

- No single source cross-runs the same models on all three with aligned protocols — correlation between BFCL-V4 agentic and τ-bench pass^k is unmeasured here.
- All three are now training targets; contamination/Goodharting risk rising ([[Eval Awareness]]).
