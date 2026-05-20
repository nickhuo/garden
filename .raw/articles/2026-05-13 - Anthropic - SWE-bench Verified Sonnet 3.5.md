---
source_url: https://www.anthropic.com/engineering/swe-bench-sonnet
fetched: 2026-05-13
title: "Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet"
author: Anthropic
date_published: 2024-10-29
---

# Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet

*Source: https://www.anthropic.com/engineering/swe-bench-sonnet*

## Overview

Anthropic achieved a score of **49%** on SWE-bench Verified using Claude 3.5 Sonnet in an agentic scaffolding setup. This represents the highest reported result on the benchmark at the time of publication, surpassing prior leading approaches.

## SWE-bench Verified

SWE-bench Verified is a curated subset of the original SWE-bench benchmark, consisting of ~500 real-world GitHub issues from popular Python repositories. Each problem requires writing code that passes the repository's test suite when the issue is resolved. "Verified" means the issues were human-reviewed to ensure the test suites actually validate the intended behavior (filtering out poorly specified issues from the original benchmark).

## Approach: Agentic Harness

Anthropic built a simple agentic scaffold around Claude 3.5 Sonnet. Key design points:

- **Tool use**: The agent is given access to tools for browsing files, executing code, running tests, and editing files. Standard software engineering actions.
- **No special tricks**: Anthropic explicitly notes the scaffold is relatively simple — no majority voting, no parallel sampling, no special retrieval tricks beyond what the model natively provides.
- **Single-pass**: Each problem is attempted once (pass@1), not via ensemble methods.
- **Model-driven**: Most of the intelligence comes from Claude 3.5 Sonnet's coding and reasoning capabilities, not from complex orchestration.

## Key Results

- **49% on SWE-bench Verified** (pass@1, single-attempt scaffold)
- Prior SOTA at time of publication was ~43% (other approaches using ensembles or more complex scaffolding)
- The result validates that strong models + simple scaffolds can outperform weaker models + complex scaffolds

## Agentic Scaffold Details

The agent operates in a loop:
1. Reads the problem statement (GitHub issue + repo context)
2. Explores the repository structure using file-reading tools
3. Locates relevant code
4. Makes edits
5. Runs tests to verify the fix
6. Iterates until tests pass or a budget is exhausted

This is an **autonomous agent** pattern (model decides the action sequence) rather than a predefined workflow.

## Implications

### Models matter more than scaffolding (up to a point)
The most important variable is model quality. The 49% result with a "simple" scaffold implies prior state-of-the-art methods were complexity-compensating for weaker models.

### SWE-bench as a proxy for real coding agents
SWE-bench Verified is the closest public benchmark to real-world software engineering task automation. The 49% result is meaningful because:
- The tasks require understanding real codebases (not toy problems)
- The evaluation is objective (test pass/fail)
- The benchmark is not gameable via fine-tuning on benchmark-specific patterns (due to "Verified" curation)

### Tool use patterns in coding agents
The scaffold's success depends on the model using file-browsing and code-execution tools fluently. This aligns with Anthropic's broader claim (see [[2025-11-24 - Anthropic - Advanced Tool Use]]) that tool use quality is the primary bottleneck in agent capability.

### Reliability vs. capability
SWE-bench measures capability (can solve at all) rather than reliability (solve consistently in production). The 49% number is pass@1 on isolated problems, not pass^k on multi-step production workflows. The [[Pass^k Reliability Metric]] critique from [[tau-bench]] still applies — production use of coding agents would require much higher per-task reliability.

## Context within Anthropic's Agent Research Program

This result sits alongside:
- [[Building Effective Agents]] — taxonomy of agent patterns including autonomous agents
- [[2026-04-08 - Anthropic - Scaling Managed Agents]] — infra-side support for long-running coding agents
- Claude Code (commercial product) — the productized form of this research

## Quotes (paraphrased from source)

> "We built a relatively simple agentic scaffold that gives Claude access to tools and lets it explore the repository and edit code to resolve GitHub issues."

> "The key insight is that with a capable enough model, you don't need elaborate scaffolding tricks."

## References in Source

- SWE-bench paper (Jimenez et al.)
- SWE-bench Verified methodology (OpenAI, 2024)
- Prior SOTA: various approaches including SWE-agent, AutoCodeRover, etc.
