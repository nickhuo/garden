---
type: entity
title: "SWE-bench Verified"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - evals
  - coding
  - benchmark
status: developing
related:
  - "[[Claude 3.5 Sonnet]]"
  - "[[Agentic Harness]]"
  - "[[Pass^k Reliability Metric]]"
  - "[[LLM-as-Judge Evaluation]]"
  - "[[Autonomous Agents]]"
sources:
  - "[[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]]"
entity_type: product
role: "Software engineering benchmark for agentic coding evaluation"
first_mentioned: "2026-05-13 ingest"
---

# SWE-bench Verified

## What it is

SWE-bench Verified is a human-curated subset of the original SWE-bench benchmark, consisting of ~500 real-world GitHub issues from popular Python repositories. Each problem requires writing code that resolves the issue and passes the repository's existing test suite.

**"Verified"** distinguishes it from the original SWE-bench: issues were manually reviewed to ensure the test suites actually validate the intended behavior. This filters out poorly specified issues and makes the benchmark a more honest capability signal.

**Evaluation:** Objective test pass/fail — not LLM-judged. This makes it more trustworthy than [[LLM-as-Judge Evaluation]] setups.

## Why it matters for agent evaluation

- **Real codebases:** Not toy problems. Requires understanding existing architecture, conventions, and test patterns.
- **Objective grading:** Binary pass/fail is unambiguous; no judge model artifacts.
- **Not gameable:** Because issues are from real repos across diverse domains, fine-tuning specifically for this benchmark is impractical.
- **Closest proxy to production software engineering automation** currently available publicly.

## Scores (at time of first ingest, 2024-10)

| System | Score | Method |
|--------|-------|--------|
| Claude 3.5 Sonnet + simple scaffold (Anthropic) | **49%** | pass@1, single-attempt |
| Prior SOTA (various complex approaches) | ~43% | ensembles / complex scaffolding |

## Reliability caveat

SWE-bench Verified measures **capability** (can the agent solve the problem at all?), not **reliability** (does it solve consistently in production?). The [[Pass^k Reliability Metric]] framework from [[tau-bench]] highlights that pass@1 on isolated problems systematically overstates production reliability — in multi-step production workflows, per-task reliability compounds poorly.

## Original SWE-bench vs. Verified

| Dimension | SWE-bench (original) | SWE-bench Verified |
|-----------|---------------------|---------------------|
| Size | ~2,294 issues | ~500 issues |
| Curation | Automated extraction | Human-reviewed |
| Issue quality | Variable | Higher signal |
| Test suite validity | Not verified | Verified to test intended behavior |

## Sources

- [[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]] (Anthropic, 2024-10-29)
- Original SWE-bench: Jimenez et al. (not yet ingested)
