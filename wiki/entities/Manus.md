---
type: entity
title: Manus
created: 2026-05-10
updated: 2026-05-10
tags:
- ai-agents
- agent-product
- non-anthropic
- meta
status: seed
related: []
sources:
- "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
_legacy_source_count: 1
---

# Manus

## Summary

General-purpose agent product, founded by **Yichao 'Peak' Ji**. Now part of Meta (acquired some time before 2026-05; the Manus blog banner reads "Manus is now part of Meta — bringing AI to businesses worldwide" and the site footer attributes © 2026 Meta). Built on **frontier-model in-context learning** — explicitly chose not to train an end-to-end agentic model, betting that staying orthogonal to model progress is the higher-leverage path.

The architecture is a single-brain agent with a virtual-machine sandbox and a heavy emphasis on **context shaping** as the production discipline.

## Why it matters for this wiki

This is the **first non-Anthropic perspective** in the wiki. It closes the explicit "cross-vendor analogues" gap called out in [[Overview]]. The lessons in [[2025-07-18 - Manus - Context Engineering for AI Agents]] both reinforce and contradict Anthropic's worldview in load-bearing ways — see [[Static Action Spaces vs Dynamic Tool Discovery]] for the most consequential collision.

## Key facts

- Founder: Yichao 'Peak' Ji (decade-plus in NLP pre-LLM; trained models from scratch for open information extraction and semantic search at a prior startup before pivoting to in-context-learning-based agents)
- Architecture: single-brain agent + VM sandbox; framework rebuilt **four times** via what the team calls "Stochastic Graduate Descent" — manual architecture search via prompt fiddling and empirical guesswork
- Avg input:output token ratio: ~100:1 (prefill-dominated, hence the obsession with KV-cache hit rate)
- Avg tool calls per task: ~50
- Action namespace convention: `browser_*`, `shell_*` prefixes enabling state-machine-driven [[Logit Masking]]
- Memory primitive: file system in the sandbox (read/write on demand, treated as externalized context — see [[Long-Horizon Context Management]])
- Acquired by Meta (some time before 2026-05); careers page redirects to metacareers.com

## Architectural distinctives

- Static action space + logit masking (cf. dynamic loading in [[Tool Search Tool]])
- Append-only, deterministic-serialization context for KV-cache stability — see [[KV-Cache Discipline]]
- `todo.md` recitation as attention-engineering mechanism — see [[Recitation]]
- Failure traces deliberately retained in context — see [[Error Trace Retention]]
- Controlled diversity injection to prevent pattern lock-in — see [[Few-Shot Drift]]

## Connections

- Coined: "Stochastic Graduate Descent (SGD)" as informal term for empirical agent-framework iteration
- Source: [[2025-07-18 - Manus - Context Engineering for AI Agents]]
- Contrasts with: [[Managed Agents]] (Anthropic's hosted [[Meta-Harness]] — both solve "how do I run a production agent" with very different splits between cognitive and operational concerns)
- Single-agent architecture — doesn't engage [[Multi-Agent Systems]]

## Open questions

- What did the four framework rebuilds change? Post doesn't disclose dead ends.
- Post-Meta acquisition direction — does Manus stay independent product or get absorbed into a Meta agent stack?
- Cross-model portability — Manus claims model-orthogonality but cites Claude Sonnet pricing specifically; what's the production model mix?
- Does Manus expose an API for tool authors, or is the action space hand-curated?

## Sources

- [[2025-07-18 - Manus - Context Engineering for AI Agents]] (2025-07-18)
