---
type: concept
title: "Online LLM-as-Judge"
created: 2026-05-23
updated: 2026-05-23
status: developing
tags:
  - ai-agents
  - evaluation
  - llm
related:
  - "[[LLM-as-Judge]]"
  - "[[LLM-as-Judge Evaluation]]"
  - "[[Agent-as-a-Judge]]"
  - "[[Continuous Evaluation]]"
  - "[[Online Evaluation Bottlenecks]]"
sources:
  - "[[2025 - LangChain - LLM Observability and Monitoring]]"
  - "[[2024-10-14 - Zhuge et al - Agent-as-a-Judge]]"
---

# Online LLM-as-Judge

Running an LLM judge against **live production traffic** as a continuous quality monitor — the deployment-time extension of the offline judge methodology in [[LLM-as-Judge Evaluation]].

## What changes when the judge goes online

- **Same rubric, live traffic.** Run the *same* judge/rubric you calibrated offline against production so degradation is obvious against the established baseline (e.g. hallucination rate 6% at release → 14% two weeks later pinpoints when drift started).
- **Sampling, not full coverage.** Cost (~$0.01-0.10/assessment) and latency forbid judging every request; sample to detect drift cheaply.
- **Tiered judges.** Cheap **distilled** evaluators score ~100% of traffic at ≈1/30 cost for format/schema/safety; the expensive [[Agent-as-a-Judge]] (step-level) runs only on flagged anomalies and sampled audits. Pushed to the limit, the distilled tier becomes **one trained classifier per signal** — see [[Specialized Eval Classifiers]] (Raindrop).
- **Guardrail mode.** A low-latency judge (e.g. a small flash model) can gate responses inline — but the latency budget caps detection accuracy, a hard tradeoff.

## Failure modes specific to online judging

- **Judge drift** vs the moving production baseline — recalibration against fresh human labels is required, not optional.
- **Judge self-eval-awareness** — an LLM judge may itself condition on apparent evaluation context (compounding [[Eval Awareness]]).
- **Cost at scale** and **credit assignment** in multi-turn — catalogued in [[Online Evaluation Bottlenecks]].

## Relation to existing pages

Extends [[LLM-as-Judge]] / [[LLM-as-Judge Evaluation]] (which cover the bias catalog and offline calibration) into production; the agentic, step-level variant is [[Agent-as-a-Judge]]; the surrounding operational loop is [[Continuous Evaluation]].
