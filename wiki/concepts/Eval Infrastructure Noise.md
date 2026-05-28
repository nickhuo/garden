---
type: concept
title: "Eval Infrastructure Noise"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - evals
  - reliability
  - methodology
complexity: intermediate
domain: ai-agents
aliases:
  - "infrastructure noise"
  - "infra noise"
  - "eval flakiness"
status: developing
related:
  - "[[Pass^k Reliability Metric]]"
  - "[[SWE-bench]]"
  - "[[tau-bench]]"
  - "[[Meta-Harness]]"
  - "[[LLM-as-Judge]]"
  - "[[User Simulator Evaluation]]"
sources:
  - "[[2026-02-05 - Anthropic - Infrastructure Noise Agentic Coding Evals]]"
---

# Eval Infrastructure Noise

Variance in agentic evaluation outcomes attributable to the execution environment — not to model capability or sampling stochasticity. Infrastructure noise is a *confound*: it makes model reliability look worse than it is and makes benchmark scores harder to compare across runs or teams.

## Definition

For a given task run multiple times with identical model outputs (fixed tool calls), infrastructure noise is the residual outcome variance. If the same deterministic agent action sequence produces different results across trials, the difference is infrastructure-induced.

Formally: `total variance = model variance + infrastructure variance`. Most published evals conflate the two and report only `total variance / n` as the score.

## Primary Noise Sources (agentic coding evals)

| Source | Examples | Severity |
|---|---|---|
| Network operations | pip install, apt-get, git clone | High |
| Container instability | startup latency, OOM, teardown edge cases | Medium |
| Test suite flakiness | non-deterministic assertions, ordering deps | Medium |
| Resource contention | CPU throttle, shared disk I/O | Low–medium |

## Why It Matters for Pass^k

[[Pass^k Reliability Metric]] is exquisitely sensitive to consistency. If a model scores pass^1 = 0.60 but infrastructure noise adds ±0.05 random per-task variation, then measured pass^k drops significantly below the true model pass^k — because any single trial that flips due to infrastructure is counted as a model failure. Infrastructure noise sets a **floor on measured pass^k** that is entirely independent of model quality.

Consequence: you cannot reliably measure model reliability (pass^k) unless infrastructure noise is first characterized and controlled.

## The Retry Trap

Naive retry logic on infrastructure failures introduces its own confound:

- **Masking model errors** — if a model made a bad decision that happened to produce an error code also produced by infra failures, a retry can succeed and erase the model error
- **Inflating apparent reliability** — retrying until success makes the model look more reliable than it is on first try
- **Asymmetric attribution** — if retries are not tracked, post-hoc analysis cannot distinguish model vs. infra failure sources

Anthropic's prescribed remedy: maintain **separate retry budgets** for infrastructure-class errors (network timeout, container crash) vs. model-decision errors (bad patch, wrong tool call), and log both separately.

## Remedies

1. **Hermetic environments** — pre-cache all external dependencies; no live network calls during eval runs
2. **Container pre-warming** — eliminate startup latency as a variance source
3. **Separate retry budgets** — infrastructure retries tracked and reported separately from model retries
4. **Structured failure logging** — log tool-call outcomes (infra-class vs. model-class) in separate structured channels
5. **Multi-trial reporting** — publish mean ± std across ≥3 trials, or pass^k alongside pass@k

## Relation to Other Eval Concepts

- [[Pass^k Reliability Metric]] — infrastructure noise is a critical prerequisite concern before pass^k is interpretable
- [[User Simulator Evaluation]] — tau-bench's noise is dominated by user-simulator stochasticity (a feature, not a bug); SWE-bench's noise is dominated by infrastructure (a bug)
- [[LLM-as-Judge]] — orthogonal; this concept is about consistency across trials, LLM-judge is about scoring quality within one trial
- [[Meta-Harness]] — hermetic eval infrastructure described here is a specialized instantiation of the meta-harness pattern: a layer that virtualizes and stabilizes the execution environment

## Broader Implication

Infrastructure noise is a domain-specific instance of a general measurement hygiene principle: **separate the thing you're measuring from the measurement apparatus**. In agent evals, the measurement apparatus (the eval harness, the container, the network) is load-bearing and must be engineered with the same rigor as the agent itself.

This connects to [[Meta-Harness]]'s framing: a well-designed meta-harness isn't just for agent orchestration — it's also the infrastructure that makes reliable evaluation possible.
