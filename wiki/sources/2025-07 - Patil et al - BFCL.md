---
type: source
title: "Patil et al — BFCL"
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
- "[[Gorilla]]"
- "[[Tool-Use Benchmarks - BFCL vs tau-bench vs ToolBench]]"
- "[[Agent Eval Pyramid]]"
sources:
- "[[.raw/articles/2025-07 - Patil et al - BFCL.md]]"
- "[[03_Resources/.raw/articles/2025-07 - Patil et al - BFCL.md]]"
source_type: paper
author: "Shishir G. Patil, Huanzhi Mao, Fanjia Yan, Charlie Cheng-Jie Ji, Vishnu Suresh, Ion Stoica, Joseph E. Gonzalez (UC Berkeley)"
date_published: 2025-07-13
url: https://proceedings.mlr.press/v267/patil25a.html
confidence: high
key_claims:
- "AST-based evaluation parses generated calls into a syntax tree and structurally matches ground truth — scales to thousands of functions without execution"
- "Abstention (relevance/irrelevance detection — knowing when NOT to call) is treated as a first-class capability"
- "SOTA LLMs are strong on single-turn calls but weak on memory, dynamic decision-making, and long-horizon reasoning"
- "Benchmark evolved V1→V4 from single-call AST accuracy to holistic agentic evaluation"
aliases:
- Berkeley Function Calling Leaderboard
- BFCL paper
---

# The Berkeley Function Calling Leaderboard (BFCL) (Patil et al., UC Berkeley, ICML 2025)

## Why this matters for the wiki

BFCL is the **de facto industry standard** for function-calling evaluation — when a model card claims a "function calling score," it usually means BFCL. It anchors the *correctness/coverage* pole of the tool-use benchmark space: cheap, deterministic, execution-free grading that scales to thousands of functions, in contrast to [[tau-bench]]'s deep reliability probing and [[ToolBench]]'s breadth-of-API generalization. See [[Tool-Use Benchmarks - BFCL vs tau-bench vs ToolBench]].

From the same [[Gorilla]] project that produced the original Gorilla API-calling model and APIBench.

## The method — AST evaluation

The signature contribution: parse the model's generated function call into an **Abstract Syntax Tree** and structurally compare it against ground truth — function name, required parameters, types, value constraints. This:

- requires **no execution** (fast, safe, reproducible),
- is **language-agnostic** (Python, Java, JavaScript, REST),
- **scales to thousands of functions** because matching is structural, not behavioral.

A complementary **Executable** mode actually runs the call and checks the return value, for cases where AST match is insufficient.

## Test categories

| Category | What it tests |
|---|---|
| Simple | one function, one call |
| Multiple | pick the right function among several |
| Parallel | multiple simultaneous calls from one prompt |
| Parallel-multiple | combination of the above |
| Relevance / irrelevance | **abstain** when no function fits — over-eager-calling check |
| Multi-turn (V3) | stateful sequential calls, context retention |
| Agentic (V4) | web search, memory persistence, format sensitivity |

Overall accuracy = unweighted average across subcategories. Both native function-calling (FC) and prompt-based modes are scored.

## Version evolution (the paper's narrative arc)

- **V1** — AST metric, foundational single-call categories.
- **V2** — enterprise + OSS user-contributed functions; reduces synthetic-data contamination.
- **V3** — multi-turn, stateful interaction.
- **V4** — holistic **agentic** evaluation (web search, memory, format sensitivity). "From tool use to agentic evaluation" — the paper's subtitle and its thesis.

## Headline finding

SOTA LLMs **excel at single-turn calls but struggle with memory, dynamic decision-making, and long-horizon reasoning** in stateful, multi-step agentic settings. Abstention (irrelevance detection) is a distinct, hard capability that high single-call scores hide.

## Connections to existing wiki

- **[[Tool-Use Benchmarks - BFCL vs tau-bench vs ToolBench]]** — situates BFCL among its peers.
- **[[Agent Eval Pyramid]] / [[Trace-Based Evaluation]]** — BFCL's AST match is a Tier-1/2 *step-correctness* eval; τ-bench's DB-state reward is Tier-3 end-to-end. BFCL V4 agentic mode is the project climbing the pyramid.
- **[[User Simulator Evaluation]]** — BFCL multi-turn lacks a true user simulator (its turns are scripted), the gap τ-bench fills.
- **[[Eval Validity]]** — AST match can reward syntactically-correct-but-semantically-wrong calls; the Executable mode is the validity hedge.

## Source location

- Raw: `.raw/articles/2025-07 - Patil et al - BFCL.md`
- Proceedings: <https://proceedings.mlr.press/v267/patil25a.html>
- Leaderboard: <https://gorilla.cs.berkeley.edu/leaderboard.html>
- Code: <https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard>
