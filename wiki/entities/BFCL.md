---
type: entity
title: "BFCL"
created: 2026-05-22
updated: 2026-05-22
tags:
- ai-agents
- benchmark
- evaluation
- tool-use
status: developing
related:
- "[[Gorilla]]"
- "[[tau-bench]]"
- "[[ToolBench]]"
- "[[Tool-Use Benchmarks - BFCL vs tau-bench vs ToolBench]]"
- "[[2025-07 - Patil et al - BFCL]]"
sources:
- "[[2025-07 - Patil et al - BFCL]]"
entity_type: benchmark
authors: Shishir G. Patil, Huanzhi Mao, Fanjia Yan, Charlie Cheng-Jie Ji, Vishnu Suresh, Ion Stoica, Joseph E. Gonzalez
affiliation: UC Berkeley (Gorilla / Sky Computing Lab)
released: 2024 (preview); ICML 2025 (paper)
repo: https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard
license: Apache-2.0
aliases:
- Berkeley Function Calling Leaderboard
- BFCL V4
---

# BFCL — Berkeley Function Calling Leaderboard

## What it is

The de facto standard benchmark for evaluating LLM **function calling** (tool use), maintained by the [[Gorilla]] project at UC Berkeley. When a model card reports a "function calling" number, it is usually BFCL. A continuously-updated live leaderboard plus a static paper artifact ([[2025-07 - Patil et al - BFCL]], ICML 2025).

## Signature method: AST evaluation

Parses the model's generated call into an **Abstract Syntax Tree** and structurally matches function name + required params + types + value constraints against ground truth. No execution required, language-agnostic, scales to thousands of functions. A complementary **Executable** mode runs the call and checks output.

## Categories

Simple · Multiple · Parallel · Parallel-multiple · Relevance/irrelevance (abstention) · Multi-turn (V3) · Agentic (V4: web search, memory, format sensitivity). Scored in both native function-calling (FC) and prompt modes; overall = unweighted average.

## Why this entity has its own page

Like [[tau-bench]] and [[SWE-bench]], BFCL is a citable artifact independent of its paper — model releases cite "BFCL score" without re-citing Patil et al. Future sources reporting BFCL numbers update this page.

## Position in the benchmark space

The **breadth-of-correctness, cheap-deterministic** pole. Strong on single-call accuracy at scale; the V1→V4 arc ("from tool use to agentic evaluation") is the project climbing toward the stateful/long-horizon territory where [[tau-bench]] already lives. See [[Tool-Use Benchmarks - BFCL vs tau-bench vs ToolBench]].

## Connections

- [[Gorilla]] — owning project; also produced the Gorilla model and APIBench.
- [[Tool-Use Benchmarks - BFCL vs tau-bench vs ToolBench]] — comparison.
- [[Agent Eval Pyramid]] — AST match is step-correctness; agentic V4 climbs toward end-to-end.

## Open

- How do V4 agentic scores correlate with τ-bench pass^k? (Do BFCL-strong models stay reliable under repeated trials?)
- Is AST-match contamination a problem now that BFCL is a training target?
