---
type: entity
title: "Raindrop"
created: 2026-05-23
updated: 2026-05-23
tags:
  - ai-agents
  - evaluation
  - entity
  - product
status: seed
entity_type: product
role: "Online evaluation / production monitoring platform for AI agents; trains many tiny per-signal binary classifiers to label production traffic and discover failure modes."
first_mentioned: 2026-05-23
related:
  - "[[Specialized Eval Classifiers]]"
  - "[[Binary Evaluation vs Scoring]]"
  - "[[Continuous Evaluation]]"
sources:
  - "[[2026 - Raindrop - Thoughts on Evals]]"
---

# Raindrop

## Summary

A production-monitoring / online-evaluation platform for AI agents. Distinctive approach (see [[Specialized Eval Classifiers]]): rather than a single prompted LLM judge sampled on a fraction of traffic, Raindrop trains **many custom tiny models — one per failure signal** — that scan millions of events daily (billions of labels/month) and surface problematic ones. Signals are **semantic** (clustering across cohorts/languages/scenarios) and **manual**. Ships as an SDK integrating with the Vercel AI SDK and Claude Agent SDK.

## Position

Raindrop argues most "online evals" are just **offline evals on a sampled slice of production** (closed-set) and that true online evaluation must discover *unexpected* failure modes (open-set). This is the sharpest articulation in the wiki of the [[Continuous Evaluation]] critique.

## Connections

- [[Specialized Eval Classifiers]] — the method
- [[Binary Evaluation vs Scoring]] — its per-signal binary labels instantiate this principle
- [[Online LLM-as-Judge]] — the alternative it positions against (general judge vs many trained classifiers)

## Sources

- [[2026 - Raindrop - Thoughts on Evals]]
