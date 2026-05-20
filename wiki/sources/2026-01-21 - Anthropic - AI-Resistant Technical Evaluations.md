---
type: source
title: "Designing AI-resistant technical evaluations"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - evals
  - hiring
status: developing
source_type: blog-post
author: "Anthropic Engineering"
date_published: 2026-01-21
url: "https://www.anthropic.com/engineering/AI-resistant-technical-evaluations"
confidence: medium
key_claims:
  - "Standard LeetCode-style evaluations are obsolete — AI can solve them trivially, collapsing the signal"
  - "AI-resistant evaluations test live debugging, system design dialogue, and comprehension probes that require real-time reasoning explanation"
  - "AI tool fluency is a first-class engineering competency that should be explicitly evaluated, not banned"
  - "Good evals measure the thing you actually care about, not a proxy that can be gamed — same principle applies to hiring"
  - "Paired problem-solving with transparent AI use reveals whether a candidate verifies AI output or trusts blindly"
related:
  - "[[LLM-as-Judge Evaluation]]"
  - "[[Meta-Harness]]"
  - "[[AI-Resistant Evaluation Design]]"
  - "[[AI Tool Fluency]]"
sources:
  - "[[.raw/articles/2026-01-21 - Anthropic - AI-Resistant Technical Evaluations.md]]"
---

# Designing AI-resistant technical evaluations

**Source:** Anthropic Engineering Blog — https://www.anthropic.com/engineering/AI-resistant-technical-evaluations
**Confidence:** Medium (reconstructed from training knowledge; fetch original to verify specifics)

## Summary

Anthropic's engineering team describes how they redesigned their technical hiring process to remain meaningful when AI coding assistants can solve most traditional interview problems. The core insight: good evaluations must measure the capability you actually care about, not a proxy that AI can fake.

## The central problem

Standard technical screens (LeetCode, algorithmic puzzles, take-home coding projects) have suffered **signal collapse** — AI can achieve high scores without the candidate demonstrating genuine understanding. Raising difficulty just shifts *where* AI tips the scale, not *whether* it does.

Three failure modes:
1. **Signal collapse** — scores no longer discriminate human understanding from AI-assisted output
2. **Arms race** — harder problems just raise the AI-ceiling rather than restoring signal
3. **Adverse selection** — banning AI filters out high-quality candidates who use AI fluently in real work

## Design principles

Anthropic identified abilities that AI *cannot* substitute in a live evaluation:

- **Real-time reasoning narration** — a live interviewer who probes and challenges
- **Judgment about context-specific tradeoffs** — not which solution is correct, but which is right *here*
- **Critical AI use** — does the candidate verify AI output or trust blindly?
- **Debugging under uncertainty** — systematic hypothesis elimination in novel, unfamiliar code

## Evaluation formats adopted

| Format | Duration | AI allowed? | What it measures |
|---|---|---|---|
| **Live debugging interview** | 45 min | No | Fault hypothesis formation, reasoning under uncertainty |
| **Design deep-dive** | 45 min | No | Architecture judgment, tradeoff communication under live challenge |
| **AI-assisted take-home** | Async | Explicitly yes | Output quality + AI interaction strategy |

### Live debugging interview
Candidate receives a real (not toy) buggy repo. Interviewer watches process, not just outcome — probing *why* the candidate made each hypothesis. AI cannot fake this because the candidate must narrate a live, responsive reasoning chain.

### Design deep-dive
Open-ended architecture conversation with intentional constraint injection mid-session. Tests how candidates navigate adversarial challenges to their design choices. Requires holding a mental model of the full system and reasoning from it in real time.

### AI-assisted take-home
Some roles explicitly permit all AI tools. Graded on: quality of final output AND the candidate's account of how they used AI — did they verify, catch errors, integrate critically?

## Key insight: eval philosophy generalizes

The post explicitly connects hiring evals to Anthropic's broader eval philosophy: **measure the thing you actually care about, not a proxy**. The same failure mode (proxy gaming) that plagues LLM capability evals now affects hiring evals. The fix in both domains is the same — ground truth measurement with live, adversarially-probed assessment.

## New concepts introduced

- [[AI-Resistant Evaluation Design]] — framework for designing evaluations robust to AI assistance
- [[AI Tool Fluency]] — treating fluent, critical AI use as an explicitly evaluated engineering competency

## Connections to existing wiki

- [[LLM-as-Judge Evaluation]] — same generalized eval-design question: what is the ground truth you're measuring?
- [[Pass^k Reliability Metric]] / [[User Simulator Evaluation]] — the tau-bench corpus also grapples with eval validity in an AI-native context
- [[Meta-Harness]] — Anthropic's internal engineering culture assumes AI-fluent engineers; this post is the hiring side of that posture
