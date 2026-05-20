---
type: source
title: "Quantifying infrastructure noise in agentic coding evals"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - evals
  - reliability
  - infrastructure
source_type: engineering-blog
author: "Anthropic Engineering"
date_published: 2025
url: "https://www.anthropic.com/engineering/infrastructure-noise"
confidence: medium
status: developing
related:
  - "[[Pass^k Reliability Metric]]"
  - "[[SWE-bench]]"
  - "[[Eval Infrastructure Noise]]"
  - "[[tau-bench]]"
  - "[[LLM-as-Judge Evaluation]]"
  - "[[Meta-Harness]]"
sources:
  - "[[.raw/articles/2026-05-13 - Anthropic - Infrastructure Noise Agentic Coding Evals.md]]"
key_claims:
  - "A non-trivial fraction of SWE-bench failures are infrastructure-induced, not model-capability failures"
  - "Infrastructure noise inflates variance in pass^k measurements, making models look less reliable than they are"
  - "Network operations (pip, apt-get, git clone) are the top noise source in coding evals"
  - "Hermetic, pre-cached eval environments are a prerequisite for reliable model comparisons"
  - "Single-run SWE-bench scores are insufficient; pass^k alongside pass@k should be reported"
---

# Quantifying infrastructure noise in agentic coding evals

Anthropic Engineering blog post examining how infrastructure-level variance — not model capability — contaminates agentic coding evaluation results on benchmarks like [[SWE-bench]].

## The Core Problem

When agentic coding evals run tasks, failures come from two distinct sources:

1. **Model variance** — stochastic from temperature/sampling; reflects true model capability distribution
2. **Infrastructure variance** — network timeouts, flaky tests, container instability, resource contention

The key insight: these two variance sources are conflated in standard single-run eval reporting. A model's published SWE-bench score is a mixture of both.

## Methodology

Anthropic characterized infrastructure noise by:
- Running identical tasks with fixed model outputs (replayed tool calls) and measuring outcome variance
- Counting failures that repeated in the same way regardless of model decisions — infrastructure signatures
- Disaggregating failures by category: network-heavy tasks vs. compute-heavy vs. test-assertion-heavy

They also connected this to [[Pass^k Reliability Metric]]: when the same task fails repeatedly due to infrastructure (not model), it suppresses measured pass^k below true model reliability.

## Key Findings

| Finding | Detail |
|---|---|
| Noise magnitude | Several percentage points of SWE-bench failures are infra-induced |
| Top noise source | Network ops: pip install, apt-get, git clone |
| Second noise source | Test suite flakiness (non-deterministic assertions, ordering dependencies) |
| Retry danger | Naive retries mask real model errors OR make infra errors look like model errors |
| Pass^k distortion | Infrastructure noise creates a lower bound on pass^k variance independent of model quality |

## Eval Design Recommendations

Anthropic's prescribed remedies:

- **Hermetic environments** — pre-cache all dependencies; no live network during eval
- **Pre-warm containers** — eliminate container startup latency as a noise source
- **Separate retry budgets** — track infrastructure retries separately from model-induced retries
- **Structured failure logging** — log tool-call outcomes vs. model decisions in separate channels for post-hoc attribution
- **Report variance** — publish pass^k alongside pass@k; at minimum report mean ± std across ≥3 trials

## Internal Practice

The team describes their production eval pipeline as implementing all of the above. They frame this infrastructure investment as a prerequisite for their published SWE-bench numbers and for Claude's agentic coding product work.

## Relation to Pass^k

This post is the first source in the wiki to apply [[Pass^k Reliability Metric]] to coding evals (not just interactive user-agent evals like [[tau-bench]]). Key extension: pass^k can only measure model reliability if infrastructure noise is first characterized and eliminated. Without that, you're measuring (model variance + infra variance) blended.

## Relation to Existing Wiki Concepts

- [[Pass^k Reliability Metric]] — this post extends the metric's scope from interactive (tau-bench) to coding (SWE-bench) evals
- [[Meta-Harness]] — hermetic eval infrastructure described here is a specialized form of the meta-harness pattern
- [[LLM-as-Judge Evaluation]] — orthogonal; pass^k is about consistency, LLM-judge is about scoring quality of one trial
- [[SWE-bench]] — the primary benchmark studied; entity page created from this source
- [[Eval Infrastructure Noise]] — concept page created from this source
