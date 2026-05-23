---
type: entity
title: "ToolBench"
created: 2026-05-22
updated: 2026-05-22
tags:
- ai-agents
- benchmark
- evaluation
- tool-use
status: developing
related:
- "[[OpenBMB]]"
- "[[BFCL]]"
- "[[tau-bench]]"
- "[[Tool-Use Benchmarks - BFCL vs tau-bench vs ToolBench]]"
- "[[2023-07-31 - Qin et al - ToolLLM]]"
sources:
- "[[2023-07-31 - Qin et al - ToolLLM]]"
entity_type: benchmark
authors: Yujia Qin, Shihao Liang, Yining Ye, et al.
affiliation: Tsinghua NLP / OpenBMB
released: 2023-07-31
repo: https://github.com/OpenBMB/ToolBench
license: Apache-2.0
aliases:
- ToolLLM
- ToolEval
---

# ToolBench

## What it is

The instruction-tuning **dataset + benchmark** at the center of the ToolLLM framework ([[2023-07-31 - Qin et al - ToolLLM]], ICLR'24 spotlight). Built fully automatically with ChatGPT over 16,464 real-world RESTful APIs (49 categories, RapidAPI Hub). The benchmark's job: test whether an LLM can compose **real, messy, large-scale APIs** to fulfill instructions.

ToolLLM has three parts:
- **ToolBench** — the data/benchmark (this entity).
- **ToolLLaMA** — LLaMA fine-tuned on ToolBench + a neural API retriever; reaches ChatGPT-comparable tool use.
- **ToolEval** — ChatGPT-based automatic evaluator (Pass Rate + Win Rate).

## Instruction tiers

I1 (single-tool) · I2 (intra-category multi-tool) · I3 (intra-collection multi-tool). Each instruction gets a DFSDT-annotated solution path — an ordered sequence of (thought, API call, response) triples.

## Why this entity has its own page

A citable benchmark distinct from its paper, and the most-cited "open-source tool-use at scale" reference. **DFSDT** (depth-first-search decision tree, ~+13% pass rate over CoT) is the reusable methodological idea.

## Position in the benchmark space

The **breadth/generalization** pole — thousands of real APIs, fully automated grading via [[LLM-as-Judge Evaluation]] (ToolEval). Most scalable, least faithful of the three. See [[Tool-Use Benchmarks - BFCL vs tau-bench vs ToolBench]].

## Known issue / successor

RapidAPI live-API instability makes raw scores irreproducible → **StableToolBench** (arXiv:2403.07714) adds a caching + simulated-response server.

## Connections

- [[OpenBMB]] — owning org (Tsinghua NLP).
- [[Tool-Use Benchmarks - BFCL vs tau-bench vs ToolBench]] — comparison.
- [[Tree of Thoughts]] — DFSDT is ToT applied to tool-call trajectories.
- [[Tool Search Tool]] — the neural API retriever prefigures retrieve-don't-list tool exposure.

## Open

- How much do StableToolBench scores diverge from the original live-API numbers?
- Does ToolLLaMA's ChatGPT-distilled data cap it at ChatGPT's tool-use ceiling?
