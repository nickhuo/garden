---
type: source
title: "Thoughts on Evals"
source_type: article
author: "Raindrop"
date_published: 2026
url: "https://www.raindrop.ai/blog/thoughts-on-evals"
created: 2026-05-23
updated: 2026-05-23
status: developing
confidence: medium
key_claims:
  - "Raindrop rejects the common definition of 'online evals' as merely running offline evals on a small sample of production data (usually with an LLM judge); true online evaluation must discover *unexpected* failure modes, not apply predetermined test cases retrospectively to live data."
  - "They train custom, tiny models to look at millions of events every day and pluck problematic events out — using two signal types, semantic and manual — generating billions of labels a month."
  - "Offline 'smoke tests' (~100 cases) are for preventing known regressions; the real work is open-set discovery in production."
  - "Per-user evals are impractical at 1M-user scale; specialized models enable pattern detection across cohorts, languages, and scenarios that single LLM judges lack."
tags:
  - ai-agents
  - evaluation
  - llm
  - online-evaluation
related:
  - "[[Specialized Eval Classifiers]]"
  - "[[Binary Evaluation vs Scoring]]"
  - "[[Raindrop]]"
  - "[[Online Evaluation Bottlenecks]]"
sources: []
---

# Thoughts on Evals (Raindrop)

Raindrop's manifesto on production evaluation (vendor source — confidence medium; partly self-promotional, but a distinctive and coherent position). Raindrop builds online evaluation / production monitoring for AI agents (see [[Raindrop]]).

## The core argument: online ≠ sampled offline

Raindrop's sharpest claim is definitional: most "online evals" are just **offline evals run on a sampled slice of production traffic**, usually via an LLM judge against predetermined criteria. That, they argue, is still **closed-set** — it can only catch failures you already thought to test. Real online evaluation must be **open-set**: discover failure modes nobody specified in advance. This sharpens the wiki's [[Online Evaluation]] vs offline framing into a *closed-set vs open-set* distinction.

## How they do it: many tiny specialized models

Rather than one monolithic LLM judge, Raindrop trains **custom, tiny models** that scan millions of events daily and "pluck problematic events out" — **billions of labels a month**. Two signal types: **semantic** (clustering/pattern detection across cohorts, languages, scenarios) and **manual**. Detail on the per-signal binary classifier approach: [[Specialized Eval Classifiers]].

## Offline still has a role

~100-case **smoke tests** prevent known regressions; A/B is fast ("minutes to deploy, hours to get answers"). Offline is the regression net; online is the discovery engine.

## Lineage they cite

References **Hamel Husain** (hamel.dev) for error-analysis methodology, **Gian Segato** (Replit) on why evals lag user behavior, and **evalite** as a tooling inspiration. No academic citations — practitioner lineage. See [[Binary Evaluation vs Scoring]] for where the binary-eval idea originates.
