---
type: concept
title: Pareto-based Candidate Selection
created: 2026-05-30
updated: 2026-05-30
tags: [llm, prompt-optimization, evolutionary-search, search]
status: developing
complexity: advanced
domain: llm
aliases: ["Pareto sampling", "Illumination strategy", "Quality-Diversity selection"]
related: ["[[GEPA]]", "[[Prompt Optimization]]", "[[Tree of Thoughts]]", "[[Parallelization]]"]
sources: ["[[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]"]
---

# Pareto-based Candidate Selection

The candidate-selection strategy at the heart of [[GEPA]]'s search, governing the **exploration–exploitation tradeoff** in evolutionary prompt optimization. Instead of always evolving the single best-scoring candidate, GEPA keeps the **Pareto frontier of best candidates per task instance** and stochastically samples among them ([[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]).

## The local-optimum trap

Greedy "always mutate the global best" (the `SelectBestCandidate` strategy, used by TextGrad) finds one strong strategy, then **repeatedly fails to improve it and burns the whole budget** refining a single lineage. BeamSearch (top-N, used by APO) is still prone to the same trap.

## The illumination fix

Borrowing **MAP-Elites illumination** (Mouret & Clune 2015):

1. For each training instance, record the highest score across all candidates → an instance-wise Pareto frontier.
2. Retain every candidate that is best on **at least one** task; prune strictly dominated ones.
3. Sample a candidate with probability **∝ the number of tasks it leads**.

This keeps *all* "winning" strategies alive simultaneously, expanding the search tree in a balanced way and converging to a higher-performing solution within the same rollout budget.

## Evidence

On Qwen3-8B with the evolution harness held fixed (paper Table 3):

| Selection strategy | Aggregate improvement |
|---|---|
| SelectBestCandidate (greedy, à la TextGrad) | +6.05% |
| BeamSearch (N=4, à la APO) | +5.11% |
| **Pareto-based (GEPA)** | **+12.44%** |

The selection strategy — not just the reflective mutation — is the dominant driver of GEPA's win.

## Connections

- **[[GEPA]]** — its core search subprocedure.
- A search-strategy cousin of [[Tree of Thoughts]] (both explore a tree of candidates rather than committing greedily), but optimizing *prompts across instances* rather than reasoning steps within one problem.

## Sources

- [[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]
