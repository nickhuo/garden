---
type: entity
title: "Gorilla"
created: 2026-05-22
updated: 2026-05-22
tags:
- ai-agents
- tool-use
- benchmark
status: seed
related:
- "[[BFCL]]"
- "[[2025-07 - Patil et al - BFCL]]"
sources:
- "[[2025-07 - Patil et al - BFCL]]"
entity_type: project
affiliation: UC Berkeley (Sky Computing Lab)
people: Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez
repo: https://github.com/ShishirPatil/gorilla
aliases:
- Gorilla LLM
- gorilla.cs.berkeley.edu
---

# Gorilla

## What it is

A UC Berkeley research project on LLM tool/API use, led out of the Sky Computing Lab (Patil, Stoica, Gonzalez). Outputs:

- **Gorilla** — an LLM fine-tuned to generate correct API calls (the original 2023 paper, "Gorilla: Large Language Model Connected with Massive APIs").
- **APIBench** — the original tool-calling benchmark (HuggingFace / TorchHub / TensorHub APIs).
- **[[BFCL]]** — the Berkeley Function Calling Leaderboard, now the de facto function-calling standard.

## Why it has a page

Owning project for [[BFCL]]. Same group also notable for OpenFunctions and RAFT. Distinct from the [[ToolBench]]/[[OpenBMB]] lineage (Tsinghua), which it is frequently compared and benchmarked against — ToolLLaMA generalizes zero-shot to Gorilla's APIBench.

## Connections

- [[BFCL]] — flagship benchmark.
- [[ToolBench]] — adjacent/competing tool-use lineage; APIBench is ToolLLM's OOD test set.
