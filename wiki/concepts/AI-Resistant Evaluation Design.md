---
type: concept
title: "AI-Resistant Evaluation Design"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - evals
  - hiring
status: seed
complexity: intermediate
domain: ai-agents
aliases:
  - AI-proof evals
  - AI-resistant hiring
related:
  - "[[LLM-as-Judge]]"
  - "[[AI Tool Fluency]]"
  - "[[Pass^k Reliability Metric]]"
  - "[[User Simulator Evaluation]]"
sources:
  - "[[2026-01-21 - Anthropic - AI-Resistant Technical Evaluations]]"
---

# AI-Resistant Evaluation Design

The practice of designing evaluations — whether for hiring, model capability, or task completion — such that AI assistance cannot substitute for the genuine competency being measured.

## Core problem

Any evaluation that tests a capability AI can perform becomes a proxy measure once AI tools are accessible to test-takers. Signal collapses: scores no longer discriminate candidates who understand from candidates who can prompt. The failure mode is not unique to hiring — [[LLM-as-Judge]] and benchmark saturation face the same proxy-gaming dynamic.

## Design principles

1. **Measure the thing you care about, not a proxy.** If you care about debugging ability, watch the debugging process live — not the final diff.
2. **Require real-time reasoning narration.** A live interviewer who probes and challenges cannot be fooled by AI-generated output the candidate doesn't understand.
3. **Inject context-specific constraints.** Generic AI solutions fail when the problem is grounded in organization-specific tradeoffs, constraints, or history.
4. **Make AI use explicit and evaluate it.** Rather than banning AI, allow it and assess *how* it is used — critical verification vs. blind trust (see [[AI Tool Fluency]]).

## Failure modes of traditional evaluations

| Failure mode | Mechanism | Fix |
|---|---|---|
| Signal collapse | AI solves the problem; candidate relays output | Live reasoning narration |
| Arms race | Harder problems → higher AI ceiling | Shift evaluation type, not difficulty |
| Adverse selection | AI ban filters fluent AI users | Allow AI, evaluate use quality |

## Relation to broader eval philosophy

The generalized principle — **measure ground truth, not a gameable proxy** — applies identically to:
- LLM capability benchmarks (see [[LLM-as-Judge]])
- Agent reliability evaluation (see [[Pass^k Reliability Metric]])
- Hiring technical screens (this concept's primary context)

Anthropic explicitly draws this connection in their engineering blog: the same failure mode that plagues model evals now affects hiring.

## Evaluation formats that hold signal

- **Live debugging** of unfamiliar, real (not toy) codebases — watch process, not output
- **System design deep-dive** with adversarial constraint injection by a live interviewer
- **AI-assisted work-sample** graded on output quality AND AI interaction strategy

## See also

- [[AI Tool Fluency]] — the competency these evals are designed to surface
- [[LLM-as-Judge]] — the parallel eval-design problem in LLM assessment
