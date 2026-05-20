---
type: concept
title: Context Anxiety
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - long-horizon
  - failure-modes
  - context
status: seed
complexity: intermediate
domain: ai-agents
aliases:
  - context-anxiety
  - context window anxiety
related:
  - "[[Long-Horizon Context Management]]"
  - "[[Meta-Harness]]"
  - "[[Harness Design Long Running Apps]]"
  - "[[Context Engineering]]"
sources:
  - "[[2025-10-01 - Anthropic - Harness Design Long Running Apps]]"
---

# Context Anxiety

## Summary

A documented failure mode in long-running LLM agents: the model **prematurely wraps up or truncates its work** as it senses its context window approaching saturation. Named and documented by Anthropic Engineering when running Claude Sonnet 4.5 on long-horizon tasks.

## Definition

> "Claude Sonnet 4.5 would wrap up tasks prematurely as it sensed its context limit approaching—a behavior sometimes called 'context anxiety.'"

The model, detecting that it is running out of context space, behaves as if the task must be concluded — even when the task is not actually complete. This is distinct from genuinely finishing work; it is a form of context-pressure-induced capitulation.

## Why it happens

Context anxiety likely emerges from training data patterns: most examples of long outputs in training naturally conclude before context limits are reached. When context is nearly full, the model's prior — "outputs ending here means the task is done" — becomes a spurious signal that competes with the actual task objective.

It is a **learned shortcut gone wrong**: context-fullness is correlated with completion in training, so the model treats it as a signal of completion at inference.

## Anthropic's Harness Fix

Anthropic added **context resets** to the harness — a mechanism that compacts or clears the context window before it saturates, preventing the model from ever reaching the pressure point that triggers the anxiety behavior.

This is a classic harness-as-workaround pattern: encode a fix in infrastructure rather than change the model.

## The Dead Weight Lesson

When the same harness (with context resets) was run on **Claude Opus 4.5**, the context anxiety behavior was absent. The context resets added overhead with no benefit — "dead weight."

This is the canonical Anthropic example of **harness assumptions going stale**: a design choice that was necessary for one model generation became unnecessary in the next. It motivates the [[Meta-Harness]] philosophy of separating stable interfaces from model-specific workarounds.

## Implications for Harness Design

- Harness assumptions must be **re-validated whenever the underlying model changes**.
- Behavioral fixes (context resets, output limits, task-termination guards) should be tagged with the model version that required them — and tested for removal on each upgrade.
- The [[Meta-Harness]] pattern (Anthropic's Managed Agents) addresses this at the architectural level: by making harnesses swappable and brains replaceable, per-model workarounds can be retired without restructuring the whole system.

## Connections

- **Named by:** [[2025-10-01 - Anthropic - Harness Design Long Running Apps]] (Anthropic Engineering)
- **Cited by:** [[2026-04-08 - Anthropic - Scaling Managed Agents]] as motivation for Managed Agents architecture
- **Addressed by (harness level):** context resets — see [[Long-Horizon Context Management]] (compaction technique)
- **Addressed by (architectural level):** [[Meta-Harness]] / [[Managed Agents]] — stable interfaces decouple model assumptions from infrastructure design
- **Related failure mode:** [[Few-Shot Drift]] (another context-accumulation failure mode, different mechanism)
- **Context discipline:** [[KV-Cache Discipline]], [[Token Economics]] (context-window cost management)

## Open Questions

- Is context anxiety present in other frontier models (GPT-4o, Gemini), or specific to Claude's training dynamics?
- Does context anxiety manifest differently across task types (coding vs research vs customer service)?
- At what context-fullness percentage does the behavior onset — 80%? 90%? Variable by task?
- Can RLHF / constitutional AI training fix it directly, or is it a fundamental attention-architecture artifact?
