---
type: concept
title: "Cache Invalidation Cascade"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - infrastructure
status: seed
complexity: intermediate
domain: ai-agents
aliases:
  - cache flush cascade
  - simultaneous cache invalidation
related:
  - "[[KV-Cache Discipline]]"
  - "[[Token Economics]]"
  - "[[Context Engineering]]"
sources:
  - "[[2026-05-13 - Anthropic - Postmortem Three Recent Issues]]"
---

# Cache Invalidation Cascade

## Definition

A failure mode where a large fraction of a distributed cache is simultaneously invalidated, causing a sudden spike in compute demand as all cache misses must be served from the slower, full-compute path. If this coincides with peak traffic, queuing delays cascade into system-wide latency spikes.

## Real-World Instance (Anthropic, 2026)

Anthropic's KV-cache (used to store preprocessed prompt prefixes — see [[KV-Cache Discipline]]) was simultaneously flushed when encryption keys were rotated for the cache store. This happened during a peak traffic window. Every incoming request required full prompt reprocessing; available compute headroom was exhausted, and P99 latency rose from ~2s to ~45s for approximately 90 minutes.

Root cause of the cascade severity: rate limiting was not tuned for cold-cache degradation. The system admitted all traffic but queued it, rather than gracefully shedding load and letting the cache warm.

## Why It Matters for AI Inference

LLM inference pipelines are particularly susceptible to cache cascade failures because:
- KV-cache prefill for long system prompts is compute-expensive (see [[Token Economics]])
- The cost difference between a cache hit and a cache miss is multiplicative, not additive
- At high traffic, the sudden shift from hit to miss workload can exceed provisioned headroom by a large factor

## Prevention Patterns

1. **Gradual invalidation** — invalidate N% of keys per minute rather than all at once. Spreads recompute cost over time.
2. **Cold-cache load shedding** — detect cold-cache conditions and shed load proactively before queues build.
3. **Maintenance scheduling** — avoid large cache operations at peak traffic windows. Use a maintenance registry visible to on-call engineers.
4. **Cross-team visibility** — planned maintenance that affects shared caches should be logged in a central registry connected to alerting dashboards.

## Connections

- [[KV-Cache Discipline]] — the upstream concept; cache cascade is a failure mode of poorly managed KV caches.
- [[Token Economics]] — cache hit rate directly affects cost and latency at scale.
- [[Context Engineering]] — long, stable system prompts that benefit most from KV-cache are also most costly to recompute on a cache miss.
