---
source_url: https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues
fetched: 2026-05-13
title: "A postmortem of three recent issues"
author: Anthropic Engineering
---

# A Postmortem of Three Recent Issues

*Published by Anthropic Engineering*

At Anthropic, we believe in transparency about our systems — including when things go wrong. This post covers three recent incidents that affected Claude.ai and our APIs, what caused them, and what we're doing to prevent them in the future.

---

## Incident 1: Claude.ai Outage (Elevated Error Rates)

### What happened

Claude.ai experienced elevated error rates affecting a significant portion of users. Requests were failing or returning degraded responses.

### Root cause

The outage was caused by a misconfiguration in our load-balancing layer. A deployment of updated routing configuration introduced an incorrect threshold parameter that caused the load balancer to aggressively shed load under normal traffic conditions — traffic levels well below what would normally trigger load shedding.

Specifically: a configuration value intended to be set to a percentage (e.g., `0.95` meaning "shed load when 95% capacity is reached") was interpreted by the new config parser as an absolute request count rather than a ratio. This caused the system to shed load after receiving just 0 or 1 requests to a given backend, effectively taking backends offline as soon as they received any traffic.

### Detection

The issue was detected by our alerting system approximately 4 minutes after the bad configuration was deployed. On-call engineers were paged and began investigation.

### Resolution

Engineers identified the misconfiguration within 12 minutes and rolled back the configuration. Full service was restored within 20 minutes of the initial deploy.

### Corrective actions

1. **Type-safe configuration schemas**: We are adding explicit type annotations and validation to configuration parameters that accept ratios vs. absolute counts. The parser will now reject values outside the expected range for ratio parameters.
2. **Staged rollout for config changes**: Configuration changes to the load-balancing layer will now go through a canary rollout (1% → 10% → 50% → 100%) with automatic rollback triggers based on error rate thresholds.
3. **Integration tests for config parsing**: We are adding a test suite that exercises the full config parsing pipeline against a set of known-valid and known-invalid configurations.

---

## Incident 2: Degraded Response Quality (System Prompt Corruption)

### What happened

A subset of users experienced responses that seemed off — Claude appeared confused, gave inconsistent answers, or seemed to be responding to a different context than provided.

### Root cause

This was a subtle bug in our context assembly pipeline. When requests are processed, we concatenate several pieces of context (system prompt, conversation history, retrieved documents). A bug in our string assembly code caused a rare buffer boundary condition to corrupt the end of the system prompt and beginning of the conversation history.

Specifically, the bug was triggered when:
- The system prompt was exactly a multiple of our internal buffer chunk size (4,096 bytes)
- AND the request included retrieved documents

Under these conditions, the last few bytes of the system prompt were overwritten with the first bytes of the retrieval results. The model received a corrupted context and produced correspondingly degraded responses.

The bug was introduced in a refactor of the context assembly code 3 weeks prior. The refactor was correctly tested for typical cases but did not cover the edge case of chunk-boundary-aligned inputs.

### Detection

This issue was detected by user reports rather than automated monitoring. Our automated quality checks were not sensitive enough to flag the degradation pattern — the responses were coherent (not obviously broken), just wrong in subtle ways.

### Resolution

We identified and fixed the bug within 6 hours of the first user report. The fix was a one-line change to the buffer boundary check.

### Corrective actions

1. **Fuzz testing for context assembly**: We are adding property-based / fuzz tests to the context assembly pipeline, specifically targeting chunk-boundary conditions with varied input sizes.
2. **Quality monitoring improvements**: We are adding LLM-as-judge evaluation on a sample of production traffic to detect response quality degradation. This requires building a lightweight evaluation harness that can run asynchronously without affecting latency.
3. **Static analysis on buffer operations**: We are enforcing a static analysis check on code paths involving byte-level string operations to flag boundary conditions that need explicit tests.

---

## Incident 3: API Latency Spike (Cache Invalidation Cascade)

### What happened

The Claude API experienced a significant latency spike (P99 latency increased from ~2s to ~45s) lasting approximately 90 minutes. Most requests eventually succeeded but with very high latency.

### Root cause

This was a cache invalidation cascade. We use a distributed KV cache (similar to Redis) to store preprocessed prompt prefixes — this is part of our KV-cache optimization for frequently used system prompts.

The incident was triggered by a planned maintenance operation: we rotated the encryption keys used for cached values. The key rotation triggered a cache flush — all cached entries were invalidated simultaneously.

On a normal day, cache warm-up after a flush is manageable because traffic is spread across time. However, this key rotation happened to coincide with a peak traffic window. With all caches cold simultaneously and peak incoming traffic, every request required a full prompt processing pipeline pass. The compute capacity required to handle full-pipeline processing at peak traffic exceeded our available headroom, causing queuing delays that cascaded into high latency for all requests.

A secondary issue: our rate limiting was not tuned to handle graceful degradation in this scenario. Rather than smoothly throttling traffic to stay within processing capacity, the system allowed all requests through but queued them, leading to the observed latency spike.

### Detection

The latency spike was detected by automated monitoring within 2 minutes. However, the root cause (cache invalidation cascade triggered by key rotation) took 25 minutes to identify because the maintenance operation was handled by a separate team and was not logged in the incident response runbook.

### Resolution

Resolution required two steps: (1) throttling incoming traffic to allow the cache to warm back up, and (2) prioritizing cache warming for the most common system prompts used across customers. Full cache warming took approximately 90 minutes.

### Corrective actions

1. **Maintenance operation registry**: We are building a centralized registry of planned maintenance operations that is integrated with our monitoring and alerting system. Future maintenance operations that affect shared infrastructure will be automatically flagged in the alerting dashboard.
2. **Gradual cache invalidation**: Cache key rotation will now trigger gradual invalidation (invalidating N% of keys per minute) rather than simultaneous flush.
3. **Load shedding under cold-cache conditions**: We are adding a detection mechanism for cold-cache conditions that triggers graceful load shedding before queues build up.
4. **Cross-team runbook integration**: Incident response runbooks will include prompts to check the maintenance registry as a standard diagnostic step.

---

## Common Themes

Looking across these three incidents, we see common failure patterns:

### Configuration and deployment safety
Two of the three incidents involved either a configuration error or a maintenance operation that lacked sufficient safeguards. Staged rollouts, type-safe configs, and maintenance registries are all instances of the same principle: changes to production systems should be constrained, observable, and reversible.

### Testing coverage at the boundaries
The context assembly bug slipped through because tests covered typical cases but not edge cases at boundary conditions. This is a recurring source of subtle bugs — systems behave correctly in the center of the input distribution and fail at the edges.

### Monitoring and detection gaps
Each incident exposed a gap in monitoring: the load-shedding bug was caught by automated alerting (fast), the quality degradation was caught by user reports (slow), and the cache cascade was caught quickly but root-cause was slow due to missing cross-team visibility. Improving monitoring requires both technical instrumentation and organizational information flow.

---

## What we're doing systemically

Beyond the incident-specific corrective actions, we are investing in three systemic improvements:

1. **Production traffic evaluation harness** — running LLM-as-judge evaluation on a sample of live traffic to detect quality regressions that don't manifest as hard errors. This is the monitoring gap that the quality degradation incident exposed most clearly.

2. **Change management integration** — connecting our deployment, configuration, and maintenance systems into a unified change management view so on-call engineers have visibility across all concurrent changes to the production stack.

3. **Resilience testing program** — systematic fault injection (chaos engineering) to validate that our load shedding, caching, and degradation paths work as designed under realistic traffic conditions.

We share this postmortem because we believe the industry benefits from transparency about how production AI systems fail. The engineering challenges of running reliable, high-quality AI inference at scale are real and non-trivial, and we're committed to learning from our mistakes publicly where we can.
