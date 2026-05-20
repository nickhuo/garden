---
type: concept
title: "Config Type Safety"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - infrastructure
status: seed
complexity: basic
domain: ai-agents
aliases:
  - configuration type safety
  - typed configuration
related:
  - "[[Context Engineering]]"
sources:
  - "[[2026-05-13 - Anthropic - Postmortem Three Recent Issues]]"
---

# Config Type Safety

## Definition

The practice of enforcing schema-level types and value constraints on configuration parameters — particularly distinguishing between semantically different numeric types such as ratios (0.0–1.0), percentages, and absolute counts.

## Motivation

Configuration values are often passed as untyped or loosely typed data (JSON, YAML, environment variables). When a parameter that should be a ratio is assigned an absolute count value, or vice versa, the system silently operates under a deeply wrong assumption. Because config parsing typically succeeds without error, this class of bug may not surface until the system behaves incorrectly under production load.

## Real-World Failure (Anthropic, 2026)

A load-balancer config intended to be a ratio (`0.95` = "shed load when at 95% capacity") was parsed by an updated config parser as an absolute request count. The load balancer interpreted it as "shed after 0 or 1 requests," effectively taking backends offline on first contact. Outage lasted ~20 minutes.

## Prevention Patterns

1. **Typed schema definitions** — declare config parameters with types (`ratio: float [0, 1]`, `count: int >= 0`). Validation at parse time rejects out-of-range or wrong-type values.
2. **Staged canary rollouts** — deploy config changes to 1% of traffic first, with automatic rollback on error threshold breach.
3. **Integration tests for config parsing** — exercise the full config parsing pipeline against known-valid and known-invalid inputs.
4. **Named types** — use distinct named types (e.g., `Ratio`, `AbsoluteCount`) in code rather than bare `float`/`int` to make semantic intent explicit and prevent interchangeable use.

## Broader Applicability

This pattern extends beyond load balancers to any system with configuration that carries implicit units or semantic constraints: timeout values (ms vs. s), memory limits (bytes vs. MB), model temperatures (0–1 vs. 0–2), API rate limits (per-second vs. per-minute).

## Connections

- General software engineering principle; appears in infrastructure contexts for AI systems.
- Related: staged rollout practices (same caution applies to model weight updates, prompt template changes, and tool schema changes in agentic systems).
