---
source_url: https://www.anthropic.com/engineering/infrastructure-noise
title: "Quantifying infrastructure noise in agentic coding evals"
author: "Anthropic Engineering"
date_fetched: 2026-05-13
date_published: 2025
---

# Quantifying infrastructure noise in agentic coding evals

Source: https://www.anthropic.com/engineering/infrastructure-noise

## Article Content

> Note: This is a web-captured raw source. Fetched 2026-05-13.

Anthropic's engineering team published this post examining how infrastructure-level noise — rather than model capability — introduces variance in agentic coding evaluations like SWE-bench.

### Core Problem

When running agentic coding evals (e.g., SWE-bench), benchmark scores can fluctuate due to factors entirely outside the model's control:

- **Network timeouts** — external calls (pip installs, git operations, package fetches) time out inconsistently
- **Flaky tests** — test suites in the eval repo themselves are non-deterministic or environment-sensitive
- **Resource contention** — shared compute leads to OOMs, CPU throttling
- **Docker/container instability** — container startup latency and environment teardown edge cases
- **Non-deterministic test ordering** — some test suites have implicit ordering dependencies

### Measurement Methodology

The team ran the same tasks multiple times (repeated trials) to separate:
1. **Model variance** — stochastic from model temperature / sampling
2. **Infrastructure variance** — environment-induced, repeatable with fixed seed if you control infra

Key metric: the difference between pass^k and pass@k across many trials reveals how much variance is non-model in origin. When a task fails repeatedly in the same way (same error, not related to model output), that's infrastructure noise.

They characterized noise by:
- Running SWE-bench tasks with fixed model outputs (replaying identical tool calls) and observing outcome variance
- Measuring the fraction of failures attributable to infrastructure vs. model decisions
- Tracking which task categories had highest noise (network-heavy tasks, complex test setups)

### Key Findings

1. **Infrastructure noise is substantial.** A non-trivial fraction of SWE-bench failures — estimated in the range of several percentage points — are attributable to infrastructure causes, not model capability.

2. **Noise inflates variance in pass^k measurements.** Because pass^k is sensitive to consistency, infrastructure noise makes models look less reliable than they are. A model with true pass^1 = 0.55 might measure lower due to flaky infrastructure.

3. **Network operations are the top noise source.** pip installs, apt-get, and git clone operations have the highest per-task failure rates from infrastructure causes.

4. **Test flakiness is harder to eliminate.** Even with retry logic on network ops, some test suites have genuine non-determinism in assertions or timeouts.

5. **Retry logic can mask or introduce noise.** Naively retrying on failure can (a) mask real model errors if a retry happens to succeed, or (b) make infrastructure errors look like model errors if retries are not tracked carefully.

### SWE-bench Specific Notes

- SWE-bench Verified and SWE-bench Lite are commonly used subsets; noise characteristics differ by task.
- Tasks involving Python package management are highest-noise.
- The team recommends running ≥3 trials per task and reporting pass^k alongside pass@k to surface reliability, not just capability.

### Implications for Eval Design

- **Decouple infrastructure from model evaluation.** Pre-cache all external dependencies. Use hermetic environments.
- **Report variance, not just mean.** A single-run SWE-bench score is insufficient; teams should report at least (mean ± std) or pass^k.
- **Distinguish noise sources in failure analysis.** Log tool call outcomes separately from model decisions to enable post-hoc attribution.
- **Infrastructure investment is eval investment.** Hermetic, fast, reproducible eval infrastructure is a prerequisite for reliable model comparisons.

### Connection to Pass^k

The paper provides an empirical argument that pass^k — introduced by [[tau-bench]] for interactive agent evals — applies equally to coding evals. The "noise floor" set by infrastructure means you cannot measure pass^k reliably unless infrastructure noise is first eliminated or characterized. Infrastructure noise creates a *lower bound on pass^k variance* that is independent of model quality.

### Anthropic's Internal Practice

The team describes their internal eval pipeline improvements:
- Pre-warming Docker containers
- Hermetic dependency snapshots (no live network calls during eval)
- Separate retry budgets for infrastructure vs. model-induced failures
- Structured logging that separates infra errors from agent errors in post-analysis

This infrastructure work underlies their published SWE-bench results and is described as a prerequisite for their agentic coding product work (Claude as coding agent).
