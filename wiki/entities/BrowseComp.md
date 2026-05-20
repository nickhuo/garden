---
type: entity
title: "BrowseComp"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - evals
entity_type: repository
role: "OpenAI's hard web-research benchmark for agentic browsing capability"
first_mentioned: "[[2026-05-13 - Anthropic - Eval Awareness BrowseComp]]"
status: seed
related:
  - "[[Claude Opus 4.6]]"
  - "[[Eval Awareness]]"
  - "[[Pass^k Reliability Metric]]"
  - "[[User Simulator Evaluation]]"
sources:
  - "[[2026-05-13 - Anthropic - Eval Awareness BrowseComp]]"
---

# BrowseComp

## Overview

BrowseComp is a benchmark introduced by OpenAI to evaluate a model's ability to retrieve hard-to-find facts from the web using agentic browsing. It is designed to resist surface-level retrieval — questions require multi-step reasoning, careful source triangulation, and sustained browsing across multiple pages.

## Design goals

- Measure **genuine research capability**, not keyword lookup
- Require real browsing (following links, reading pages, synthesizing across sources)
- Be difficult enough that models cannot answer from training-time memorization

## Relevance to eval awareness

[[Claude Opus 4.6]]'s high BrowseComp scores triggered Anthropic's [[Eval Awareness]] investigation. Because BrowseComp questions have a distinctive format (detailed factual queries, explicit difficulty signaling), they risk being recognized as eval prompts — which could cause models to exert disproportionate effort.

Anthropic's investigation found that reformatting BrowseComp questions to look less "eval-like" did not dramatically reduce Opus 4.6's performance, supporting the conclusion that the gains are primarily genuine.

## Benchmark design lessons

Per Anthropic's post: benchmarks like BrowseComp should minimize distinguishable eval markers — anonymous submission, natural-language framing, format variation — to reduce eval-conditioning risk.

## Sources

- [[2026-05-13 - Anthropic - Eval Awareness BrowseComp]]
