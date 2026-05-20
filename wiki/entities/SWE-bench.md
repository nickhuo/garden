---
type: entity
title: "SWE-bench"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - evals
  - benchmark
  - coding
entity_type: product
role: "Standard benchmark for evaluating LLM-based software engineering agents on real GitHub issues"
first_mentioned: "[[2026-02-05 - Anthropic - Infrastructure Noise Agentic Coding Evals]]"
status: seed
related:
  - "[[Pass^k Reliability Metric]]"
  - "[[Eval Infrastructure Noise]]"
  - "[[tau-bench]]"
  - "[[Meta-Harness]]"
sources:
  - "[[2026-02-05 - Anthropic - Infrastructure Noise Agentic Coding Evals]]"
---

# SWE-bench

Standard benchmark for evaluating LLM-based software engineering agents. Tasks are drawn from real GitHub issues with corresponding test suites; the agent must produce a code patch that passes the tests.

## Variants

- **SWE-bench Full** — complete task set (~2,300 tasks from 12 Python repos)
- **SWE-bench Lite** — 300-task stratified subset; most widely reported
- **SWE-bench Verified** — human-verified subset with confirmed solvability

## Noise Characteristics (from [[2026-02-05 - Anthropic - Infrastructure Noise Agentic Coding Evals]])

Anthropic's analysis found that SWE-bench results are substantially contaminated by [[Eval Infrastructure Noise]]:

- Tasks involving Python package management have the highest infrastructure noise rates
- Network operations (pip install, apt-get, git clone) are the primary noise source
- Some test suites have genuine non-determinism in assertions or timeouts, independent of infrastructure control
- Single-run scores are insufficient; Anthropic recommends ≥3 trials and [[Pass^k Reliability Metric]] reporting

## Relation to Pass^k

SWE-bench is typically reported as pass@1 (single-run mean). Anthropic's infrastructure noise work demonstrates that meaningful pass^k measurement on SWE-bench requires hermetic eval environments — otherwise infrastructure variance inflates the apparent pass^k gap.

## Contrast with tau-bench

[[tau-bench]] measures **interactive reliability** (agent + user simulator loops). SWE-bench measures **coding task completion** (agent + test suite). Both benefit from pass^k framing, but their noise sources differ: tau-bench variance is dominated by user simulator stochasticity; SWE-bench variance is dominated by infrastructure noise.
