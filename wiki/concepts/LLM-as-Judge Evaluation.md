---
type: concept
title: LLM-as-Judge Evaluation
created: 2026-05-04
updated: 2026-05-13
tags:
- ai-agents
- evaluation
- methodology
status: seed
related:
- "[[LLM-as-Judge]]"
- "[[Online Evaluation]]"
sources:
  - "[[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]]"
_legacy_source_count: 1
---

# LLM-as-Judge Evaluation

## Summary

Evaluation methodology where an LLM scores agent output against a rubric, used when deterministic step-matching fails. Per [[How we built our multi-agent research system]]: Anthropic uses a **single-call LLM judge** scoring 0.0–1.0 across rubrics (factual accuracy, citation accuracy, completeness, source quality, tool efficiency), supplemented by **mandatory human spot-checking**.

## Why it matters for agents

Agentic systems explore many valid paths to the same goal. Process-fidelity evaluation ("did the agent take the *right* steps?") is the wrong question — **end-state evaluation** ("did the agent reach a correct outcome?") is the right one. LLM-as-Judge is the only practical tool that scales end-state grading.

## Anthropic's prescription

- **Single LLM call** (not chain) per eval — rubric in prompt, score out, fast and reliable
- **Rubric explicit and multi-axis** — avoid single-number collapse that hides systematic errors
- **Human spot-checks unavoidable** — catches systematic LLM-judge biases
- **Pivot from process to end-state** grading
- **Separate correctness from style** — these are different axes; factual accuracy should be weighted independently of tone or formatting (per [[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]])
- **Calibrate judges periodically** against 50–200-example human-labeled sets; judge drift is a real failure mode as models and prompts change

## Connections

- Solves an open question previously tracked in [[Autonomous Agents]] (long-horizon eval)
- Methodology for: [[Multi-Agent Systems]]
- Refines: [[Workflows Beat Agents for Most Production]] (eval is what tells you when a workflow stops being good enough)
- **Contrasts with** [[tau-bench]]'s deterministic database-state grading — LLM-judge handles open-ended outputs, DB-state grading handles constrained outcomes. Composes with [[Pass^k Reliability Metric]] when scoring repeated trials.

## Generalized eval design parallel

The same core failure mode — **proxy gaming** — now affects both LLM capability benchmarks and human hiring evaluations. [[AI-Resistant Evaluation Design]] is the hiring-side application of the same principle: measure what you actually care about, not a proxy that can be gamed. The connection is explicit in [[2026-01-21 - Anthropic - AI-Resistant Technical Evaluations]].

## Open questions

- LLM-judge biases — what failure modes systematically? Anthropic gestures, doesn't detail.
- Inter-rater reliability — how stable across model versions / prompt drift?
- Cost — at what scale does LLM-as-Judge eval itself become the budget bottleneck?
- Adversarial robustness — can agents game LLM judges by writing in ways the judge favors?
- **[[Eval Awareness]] in judges**: LLM judges may themselves be eval-aware — scoring responses differently when they recognize the evaluation context. This adds a second layer of eval-conditioning risk on top of the model under evaluation. See [[2026-05-13 - Anthropic - Eval Awareness BrowseComp]].

## Production Deployment for Quality Monitoring (Anthropic, 2026)

[[2026-05-13 - Anthropic - Postmortem Three Recent Issues]] confirms Anthropic is building an LLM-as-judge harness running asynchronously on a **sample of live production traffic** — specifically to detect quality regressions invisible to error-rate monitoring. The trigger was a context assembly bug that produced coherent-but-wrong responses (see [[Context Assembly Pipeline]]). This is the first documented Anthropic deployment of LLM-as-judge for *production quality monitoring* rather than offline eval.

## Sources

- [[How we built our multi-agent research system]] (Anthropic, 2025-06-13)
- [[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]] (Anthropic, 2026-05-13) — adds calibration sets, correctness/style split, placement as Tier 2 in [[Agent Eval Pyramid]]
- [[2026-05-13 - Anthropic - Postmortem Three Recent Issues]] (Anthropic, 2026-05-13) — production monitoring deployment
