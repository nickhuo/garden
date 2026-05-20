---
type: source
title: "Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - evals
  - coding
status: developing
related:
  - "[[SWE-bench Verified]]"
  - "[[Claude 3.5 Sonnet]]"
  - "[[Agentic Harness]]"
  - "[[Autonomous Agents]]"
  - "[[Pass^k Reliability Metric]]"
  - "[[Augmented LLM]]"
sources:
  - "[[.raw/articles/2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5.md]]"
source_type: article
author: Anthropic
date_published: 2025-01-06
url: https://www.anthropic.com/engineering/swe-bench-sonnet
confidence: high
key_claims:
  - "Claude 3.5 Sonnet + simple agentic scaffold achieves 49% on SWE-bench Verified (pass@1)"
  - "Simple scaffold + strong model outperforms complex scaffold + weaker model"
  - "Tool use fluency (file browse, code execute, edit, test-run) is the operative mechanism"
  - "49% measures capability not reliability; pass^k collapse still applies in production"
---

# Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet

**Source:** Anthropic Engineering Blog | **Published:** 2024-10-29 | **URL:** https://www.anthropic.com/engineering/swe-bench-sonnet

## Summary

Anthropic achieved **49% on [[SWE-bench Verified]]** using [[Claude 3.5 Sonnet]] in a deliberately simple agentic scaffold — surpassing prior state-of-the-art (≈43%) achieved with more complex approaches. The headline claim is that model quality is the dominant variable; sophisticated scaffolding is a workaround for insufficient model capability.

## Key Claims

1. **49% pass@1 on SWE-bench Verified** — top result at publication; single-attempt, no ensembles, no majority voting.
2. **Scaffold simplicity as a finding** — the agent uses standard tools (file read, shell exec, file edit, test runner) in a loop. Complexity is not what drove the gain.
3. **Model-driven > scaffold-driven** — implies prior SOTA was complexity-compensating for weaker base models.
4. **Tool use fluency is the bottleneck** — agent must fluently navigate real codebases, locate relevant files, make targeted edits, and iterate on test feedback. This matches Anthropic's broader position in [[2025-11-24 - Anthropic - Advanced Tool Use]].
5. **Capability ≠ reliability** — 49% on isolated tasks ≠ production-grade reliability. [[Pass^k Reliability Metric]] critique from [[tau-bench]] still applies: per-task reliability degrades sharply across repeated attempts.

## Scaffold Design

The [[Agentic Harness]] is an [[Autonomous Agents]] pattern (model-chosen action sequence, not code-orchestrated workflow):

- Read issue + repo context
- Explore repo (file browser tool)
- Locate relevant code
- Edit files
- Run tests
- Iterate until pass or budget exhausted

No special retrieval tricks. No parallel sampling. Autonomous, single-pass.

## Why SWE-bench Verified Matters

[[SWE-bench Verified]] is the closest public benchmark to real-world software engineering automation:
- Real GitHub repos and issues (not toy problems)
- Objective eval (test suite pass/fail)
- Human-verified issue quality (filters out poorly specified tasks from original SWE-bench)
- Not gameable via fine-tuning on benchmark-specific patterns

## Connections

- **Benchmark:** [[SWE-bench Verified]] — the eval surface; connects to [[LLM-as-Judge Evaluation]] critique (here eval is objective, not LLM-judged)
- **Agent pattern:** [[Autonomous Agents]] — model-chosen action loop
- **Tool use:** [[Augmented LLM]], [[ACI - Agent-Computer Interface]]
- **Reliability gap:** [[Pass^k Reliability Metric]] — 49% capability ≠ production reliability
- **Product continuity:** [[Claude 3.5 Sonnet]] entity; downstream: Claude Code
- **Scaffold concept:** [[Agentic Harness]] — the minimal wrapping pattern

## Contradictions / Tensions

The result partially tensions with [[Workflows Beat Agents for Most Production]]: it demonstrates that autonomous agents work well in coding domains, aligning with the thesis's carve-out that "coding is workflow-territory" but showing agents can succeed at scale. The simplicity finding also tensions with the complexity of [[Meta-Harness]] — if a simple scaffold achieves 49%, what does the infra-heavy Managed Agents stack buy in pure capability?

## Open Questions

- Does 49% capability translate to acceptable pass^k in production coding workflows?
- How does this result compare to Claude Code's internal benchmarks?
- Is there a floor on scaffold complexity below which performance degrades?
- How does GPT-4o / Gemini compare on SWE-bench Verified with equivalent simplicity?
