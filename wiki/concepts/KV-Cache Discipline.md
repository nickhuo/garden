---
type: concept
title: KV-Cache Discipline
created: 2026-05-10
updated: 2026-05-10
tags:
- ai-agents
- context
- kv-cache
- performance
- economics
status: developing
related: []
sources:
- "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
- "[[2026-05-13 - Anthropic - Postmortem Three Recent Issues]]"
aliases:
- KV-Cache Hit Rate
- KV Cache
- Prefix Caching Discipline
_legacy_source_count: 1
---

# KV-Cache Discipline

## Summary

Per [[2025-07-18 - Manus - Context Engineering for AI Agents]]: **KV-cache hit rate is the single most important production metric for an AI agent.** Not accuracy, not latency directly, not cost — KV-cache hit rate, because it dominates both latency (TTFT) and cost (~10× gap) in any production-scale loop.

This is a third cost axis not yet captured by [[Token Economics]]'s dual-cost (dollar / attention) framing.

## The economics

The KV (key-value) cache stores attention computations for tokens already processed. When a subsequent request shares a **prefix** with a previous one, the cached attention can be reused — the prefill cost drops dramatically and TTFT drops with it.

Manus's anchor number on Claude Sonnet:

| Token type | Cost per MTok | Multiplier |
|---|---|---|
| Cached input | $0.30 | 1× |
| Uncached input | $3.00 | 10× |

Combined with Manus's reported **100:1 input:output ratio** (prefill-dominated, because agent contexts grow linearly while structured-function-call outputs stay tiny), the KV-cache hit rate effectively sets the unit economics of every agent loop.

## The three rules

### 1. Keep your prompt prefix stable

> "A common mistake is including a timestamp—especially one precise to the second—at the beginning of the system prompt. Sure, it lets the model tell you the current time, but it also kills your cache hit rate."

Even a single-token diff invalidates cache from that token onward (autoregressive nature). Any per-request variation belongs **after** the cacheable prefix, not inside it.

### 2. Make context append-only

Never edit prior actions or observations. Watch for non-determinism in serialization — many JSON libraries don't guarantee stable key ordering, which silently invalidates cache. The append-only invariant is the same one that makes [[Session as Event Log]] durable, applied at the request level.

### 3. Mark cache breakpoints explicitly when needed

Some providers/frameworks don't do automatic incremental prefix caching. When manual: place breakpoints at least at the end of the system prompt; account for cache TTL.

For self-hosted setups (e.g., vLLM), enable prefix caching and route requests by session ID to keep workers consistent.

## Implications for context engineering

- **Dynamic action spaces are expensive.** Tool definitions sit near the front of the context post-serialization. Any change (adding or removing a tool mid-iteration) invalidates the cache from that point forward. This is the core argument for [[Logit Masking]] over dynamic tool loading.
  > [!warning] Contradicts [[Tool Search Tool]]
  > Manus argues dynamic tool defs invalidate KV-cache → don't do it. Anthropic's Nov-2025 [[Tool Search Tool]] explicitly addresses this: deferred tools are *excluded from the initial prompt entirely*, so the prefix remains stable until Claude searches; the dynamic load happens after the cacheable region. Both can be right within their respective architectures, but the design implications are opposite.
- **Sub-second timestamps belong in observations, not the system prompt.** If you need wall-clock time available, put it in tool returns where it doesn't pollute the cacheable prefix.
- **Append-only context is a hard architectural constraint, not a stylistic preference.** Any "context cleanup" pass (collapsing old turns, rewriting earlier observations) destroys cache reuse and turns a 1× operation into a 10× operation.
- **Self-hosted inference brings KV-cache directly under your control.** Hosted APIs expose cache behavior through documented prefix-cache rules; self-hosted lets you optimize routing, eviction, and breakpoints directly.

## Third cost axis: KV-cache hit rate

[[Token Economics]] frames cost in two dimensions: **dollar cost** (4× / 15× chat token multipliers) and **attention cost** (recall degradation). KV-cache hit rate is a **third dimension** that cuts across both:

| Dimension | What you pay | Failure mode | Lever |
|---|---|---|---|
| Dollar cost | API spend | Uneconomic | Pattern choice (workflow vs agent) |
| Attention cost | Recall degradation | Unreliable | Context discipline ([[Context Engineering]]) |
| **KV-cache cost** | **Prefill TTFT + 10× $/MTok penalty** | **Unscalable in production** | **Prefix stability + append-only** |

For agents with 100:1 input:output ratios, **the KV-cache axis can dominate the other two combined.**

## Connections

- Operational metric for: [[Context Engineering]] (in production)
- Third axis of: [[Token Economics]]
- Argues against (in static-harness designs): [[Tool Search Tool]] dynamic loading
- Argues for: [[Logit Masking]] over action-space mutation
- Substrate compatibility: [[Session as Event Log]] (append-only by construction → cache-friendly by construction)

## Open questions

- Cross-provider numbers — Anthropic publishes the 10× gap on Sonnet; what's the analogue on GPT-5 / Gemini / open-weights served via vLLM?
- KV-cache TTL — how long do hosted providers actually keep cached prefixes warm? Anthropic and OpenAI publish guidance; real expiration behavior under load is less clear.
- Effect of [[Long-Horizon Context Management]] compaction on cache — compaction rewrites the prefix and therefore guarantees a cache miss on the very next call. Is that a one-time cost or does each compaction step compound?
- Does Manus's hard append-only stance hold for agents that backtrack (revising plans, restarting from checkpoints)? Or do those agents accept the cache miss as the cost of correctness?

## Production Failure Mode: Cache Invalidation Cascade

[[2026-05-13 - Anthropic - Postmortem Three Recent Issues]] provides a real Anthropic incident that illustrates what happens when KV-cache discipline is violated at the infrastructure level rather than the application level.

Anthropic rotated encryption keys for their distributed KV-cache store. This simultaneously invalidated all cached prompt prefixes. At peak traffic, every request required full prompt reprocessing; available compute headroom was exceeded, and P99 API latency rose from ~2s to ~45s for ~90 minutes.

The failure violated the **prefix stability** rule at the infra layer: a maintenance operation (key rotation) functioned as a forced cache miss for the entire fleet. The corrective action — gradual invalidation (N% of keys per minute) — is the infra-layer equivalent of the application-layer rule "keep your prompt prefix stable." See [[Cache Invalidation Cascade]].

## Sources

- [[2025-07-18 - Manus - Context Engineering for AI Agents]] (2025-07-18)
- [[2026-05-13 - Anthropic - Postmortem Three Recent Issues]] (2026-05-13)
