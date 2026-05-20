---
type: source
title: "A Postmortem of Three Recent Issues"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - infrastructure
  - postmortem
status: developing
source_type: article
author: "Anthropic Engineering"
date_published: 2026-05-13
url: https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues
confidence: high
related:
  - "[[KV-Cache Discipline]]"
  - "[[LLM-as-Judge Evaluation]]"
  - "[[Token Economics]]"
  - "[[Anthropic]]"
sources:
  - "[[.raw/articles/2026-05-13 - Anthropic - Postmortem Three Recent Issues.md]]"
key_claims:
  - "A load-balancer misconfiguration (ratio vs. absolute-count type confusion) caused an outage; resolved in 20 min via rollback."
  - "A context-assembly bug triggered at chunk-boundary alignment (4096-byte multiples) corrupted system prompts — caught by user reports, not monitoring."
  - "A cache key rotation flushed KV-cache simultaneously at peak traffic, causing a 45s P99 latency cascade for ~90 min."
  - "LLM-as-judge evaluation on live production traffic is being added as a quality regression detector."
  - "Gradual cache invalidation (N% per minute) is safer than simultaneous flush."
---

# A Postmortem of Three Recent Issues

**Source:** Anthropic Engineering Blog · [URL](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues)
**Published:** 2026-05-13

## Summary

Anthropic publicly documents three production incidents affecting Claude.ai and the API. Each incident illustrates a distinct class of infrastructure failure. Together they reveal systemic gaps in configuration safety, boundary-condition testing, and cross-team change visibility.

## Incident 1 — Load-Balancer Misconfiguration (Outage)

A config value intended as a ratio (`0.95` = "shed at 95% capacity") was parsed as an absolute count, causing backends to shed load after 0–1 requests. Detection: 4 min (automated). Resolution: 20 min (rollback).

**Fixes:** type-safe config schemas with range validation; staged canary rollouts for load-balancer configs; integration tests for config parsing.

See concept: [[Config Type Safety]]

## Incident 2 — Context Assembly Bug (Quality Degradation)

A buffer boundary condition at exactly 4,096-byte chunk multiples overwrote the tail of the system prompt with the head of retrieval results. The model received corrupted context but produced coherent-looking wrong answers. Detection: user reports (hours delay). Resolution: 6 hours.

**Fixes:** fuzz/property-based testing for context assembly; [[LLM-as-Judge Evaluation]] on production traffic sample; static analysis on byte-level string operations.

See concept: [[Context Assembly Pipeline]]

## Incident 3 — KV-Cache Flush Cascade (Latency Spike)

Encryption key rotation simultaneously invalidated all KV-cache entries during a peak traffic window. Without warm cache, every request required full prompt reprocessing; available headroom was insufficient, causing queuing and P99 latency of ~45s for ~90 min. Detection: 2 min (automated), but root cause took 25 min due to no cross-team maintenance visibility.

**Fixes:** maintenance operation registry integrated with alerting; gradual invalidation (N% per minute); load shedding triggered on cold-cache detection; cross-team runbook integration.

See concept: [[KV-Cache Discipline]], [[Cache Invalidation Cascade]]

## Common Themes

| Theme | Incidents |
|---|---|
| Configuration / deployment safety | 1, 3 |
| Boundary-condition testing gaps | 2 |
| Monitoring and detection gaps | 2, 3 |

## Systemic Investments

1. **Production traffic evaluation harness** — LLM-as-judge on live traffic sample for quality regression detection. See [[LLM-as-Judge Evaluation]].
2. **Change management integration** — unified view of deployments, configs, and maintenance operations for on-call engineers.
3. **Resilience testing / chaos engineering** — fault injection to validate load shedding, caching, and degradation paths under realistic traffic.

## Key Claims

- Type confusion between ratio and absolute-count config values caused an outage — a class of bug preventable with schema-level types.
- Subtle quality regressions (coherent but wrong responses) are invisible to error-rate monitoring; require semantic evaluation (LLM-as-judge).
- KV-cache simultaneous flush at peak traffic is a known anti-pattern; gradual invalidation is safer. Connects to [[KV-Cache Discipline]].
- Cross-team change visibility gaps extend detection time even when automated monitoring fires quickly.

## Connections

- [[KV-Cache Discipline]] — Incident 3 is a real production failure mode for cache discipline. Adds industrial evidence.
- [[LLM-as-Judge Evaluation]] — Anthropic is now deploying this on live traffic; validates the concept's practical utility.
- [[Token Economics]] — KV-cache hit rate is directly linked to cost and latency at Anthropic's scale.
- [[Context Engineering]] — Incident 2's root cause lives in the context assembly pipeline.
- [[Anthropic]] — entity producing this source.
