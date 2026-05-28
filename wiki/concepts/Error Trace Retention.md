---
type: concept
title: Error Trace Retention
created: 2026-05-10
updated: 2026-05-13
tags:
- ai-agents
- context
- error-recovery
- evaluation
status: developing
related: []
sources:
- "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
- "[[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]]"
aliases:
- Keep the Wrong Stuff In
- Failure Trace Retention
_legacy_source_count: 1
---

# Error Trace Retention

## Summary

Per [[2025-07-18 - Manus - Context Engineering for AI Agents]]: don't hide errors from the model. When an action fails (hallucinated arguments, environment error, schema violation), **leave the failure and its observation in the context.** The model uses the failure trace to implicitly update its prior — shifting the next-step distribution away from the failed action — and demonstrably reduces the chance of repeating the same mistake.

Manus elevates this to a stronger claim: **error recovery is the clearest indicator of true agentic behavior**, and is underrepresented in current benchmarks (which optimize task success under ideal conditions).

## Why hiding errors is the wrong instinct

The natural production impulse is to clean up traces, retry silently, or reset state — "more controlled," "safer to expose to the user." But:

> "Erasing failure removes evidence. And without evidence, the model can't adapt."

In a multi-step task, failure is structurally part of the loop, not an exception. An agent that has been shielded from its own mistakes has no signal to recalibrate — it will re-attempt the same wrong action because nothing in its context contradicts the prior that led there.

## What "retention" means concretely

- **Failed tool call → keep the call AND the error response.** Don't replace it with a "tool unavailable, retry" sanitized message.
- **Stack traces, schema-violation messages, environment errors → keep them verbatim** unless they're a security/privacy hazard. The structured-error content is the learning signal.
- **Hallucinated outputs that got caught (by a validator, a downstream tool, a human) → keep the hallucination + the rejection.** This is the strongest demonstration to the model that the path is wrong.

What you do *not* retain: secrets exposed in errors, PII surfaced by a malformed query, anything that violates external compliance. Sanitize *those specifically*, leave the structural error visible.

## Compatibility with other context-engineering rules

- **Append-only** ([[KV-Cache Discipline]]): retention is the append-only-friendly choice. Hiding an error requires editing prior context, which invalidates KV-cache.
- **Lost-in-the-middle**: retained errors deep in context may not be acted on. [[Recitation]] partially counters this — if you're reciting the plan, you can include "errors so far" in the recited block.
- **Compaction** ([[Long-Horizon Context Management]]): when compacting old context, **don't summarize errors out**. A summary like "tried X tools, eventually succeeded" loses the learning signal. Keep at least the canonical-failure structure (action + error message) for the compacted-out steps.

## Model-facing vs log-facing errors (per Anthropic 2026-05)

[[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]] introduces a distinction that sharpens the retention rule:

- **Model-facing error** — a structured JSON object the model can reason about (error_type, tool, reason, recoverable, suggested_alternatives). The harness classifies and transforms the raw error before surfacing it.
- **Log-facing error** — the raw traceback, stored verbatim in the event log for human debugging.

This is a refinement, not a contradiction: retention remains correct. The new claim is that *how* the error is retained matters — raw tracebacks surfaced to the model may not be the optimal signal; structured errors let the model act. Raw tracebacks should stay in the log.

The key question this opens: does a structured model-facing error preserve Manus's "learning signal" claim as well as the verbatim traceback? If the model needs to see exactly *what* failed (stack frames, type errors) to avoid repeating, structured errors may lose information. If the model only needs the *category* of failure, structured errors may be more useful. Empirical data needed.

> [!contradiction] Possible tension: Manus (2025-07) says keep errors verbatim; Anthropic (2026-05) says transform to structured objects for model-facing surface. Both agree: log the raw trace. The disagreement is what to put in the context window. Manus likely prioritizes learning signal; Anthropic prioritizes model reasoning clarity. May be model-capability-dependent — weaker models need more structure; stronger models can parse raw traces.

## Evaluation implication

If error recovery is the marker of agentic behavior, then benchmarks that score only task success are mis-specified for agents. Manus's complaint is structural: SWE-bench, BrowseComp, etc. measure end-state accuracy; none directly measure recovery quality (time-to-recover, recovery efficiency, repeat-failure rate). This is a wiki-flag for evaluation methodology work.

## Connections

- Implements: [[Context Engineering]] (a discipline rule within it)
- Cache-compatible with: [[KV-Cache Discipline]] (retention is append-only by default)
- Eval gap: [[LLM-as-Judge]] (judges currently score end-states, not recovery quality)
- Compaction interaction: [[Long-Horizon Context Management]] (preserve errors through summarization)

## Open questions

- Quantitative effect — how much does retention vs erasure shift the model's repeat-error rate? Manus asserts large but doesn't publish numbers.
- Saturation — at what point does an error-laden context become harder to reason in (the negative example flooding the prior beyond usefulness)?
- Model dependence — does GPT-5 / Gemini 3 / Sonnet 4.6 all show the same retention benefit, or is it model-architecture-dependent?
- Should errors be tagged structurally (e.g., a `<failure>` block) to give the model an unambiguous signal, or does plaintext suffice?
- Counterargument from the safety side — exposing failures may reveal jailbreak surface; how do you retain learning value without leaking exploit gradients? Manus doesn't address this.

## Sources

- [[2025-07-18 - Manus - Context Engineering for AI Agents]] (2025-07-18)
- [[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]] (Anthropic, 2026-05-13)
