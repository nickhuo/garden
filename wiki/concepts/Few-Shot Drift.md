---
type: concept
title: Few-Shot Drift
created: 2026-05-10
updated: 2026-05-10
tags:
- ai-agents
- context
- few-shot
- anti-pattern
status: developing
related:
- "[[In-Context Learning]]"
sources:
- "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
aliases:
- Pattern Mimicry Hazard
- Don't Get Few-Shotted
_legacy_source_count: 1
---

# Few-Shot Drift

## Summary

Per [[2025-07-18 - Manus - Context Engineering for AI Agents]]: in agent systems, the standard few-shot prompting technique can backfire. **Models are excellent mimics; they imitate the pattern they see in context.** When a long agent context fills with similar action-observation pairs (e.g., reviewing 20 resumes in a row), the model falls into a rhythm and continues the pattern even when it's no longer optimal — leading to drift, overgeneralization, and hallucination.

The mitigation is **controlled diversity injection**: vary serialization templates, alternate phrasing, introduce minor noise in order or formatting. Don't few-shot yourself into a rut.

## Why this is sharper in agents than in chat

Few-shot prompting in single-shot chat is benign because the few examples are explicit, curated, and bounded. In an agent loop, "the few-shot examples" are **the agent's own past trajectory** — accumulated, unbounded, and shaped by environment rather than intent. Two consequences:

- The agent has no human curating examples for balance and diversity.
- The pattern becomes self-reinforcing: each repeat strengthens the prior toward more repeats.

Manus's anchor case: when reviewing a batch of resumes, the agent's behavior on resumes 1-3 becomes the template for resumes 4-20, even when later candidates need different evaluation criteria. This is **observation drift hardening into action drift**.

## The fix: controlled diversity

Manus injects structured variation:

- **Different serialization templates** — observation #1 returned as `{"name": "Alice", ...}`, #2 as `Alice — software engineer, ...`. Same semantic content, different surface form.
- **Alternate phrasing** in tool descriptions, error messages, system-prompt fragments that rotate position-wise.
- **Minor noise in order or formatting** — small perturbations to keys, whitespace, presentation order.

The goal isn't to be unpredictable; it's to **break the model's pattern-matching shortcut** so it actually evaluates each input on its merits.

## Tension with KV-cache stability

There's an obvious tension: diversity injection means the context is no longer prefix-identical across iterations, which costs KV-cache hits. Manus doesn't address this directly. The implied resolution: inject diversity in the **observation** layer (where each iteration is naturally unique anyway) rather than in the **prefix** (system prompt, tool definitions, stable scaffolding). See [[KV-Cache Discipline]].

So the rule is roughly:
- Stable: system prompt, tool definitions, persistent context structure
- Varied: observation serialization, intermediate phrasing, formatting noise

## Connections

- Anti-pattern within: [[Context Engineering]]
- Tension with: [[KV-Cache Discipline]] (resolved by varying only the tail, not the prefix)
- Related to: [[Recitation]] inverse — recitation reinforces a *desired* pattern; few-shot drift is reinforcement of an *undesired* one
- Failure mode of: [[Autonomous Agents]] in long tasks with repetitive subtasks
- Eval surface: [[LLM-as-Judge Evaluation]] should test for drift on batched-similar tasks

## Open questions

- Is there a measurable signature of few-shot drift in token-level outputs (e.g., entropy collapse over iterations)? Could be a useful monitoring metric.
- Does extended-thinking / reasoning-trace help — does an explicit "step back" before each batch item prevent drift?
- At what batch size does drift kick in? Manus uses 20 resumes as the case; is the threshold lower or higher elsewhere?
- Does diversity injection actually move accuracy, or just change failure mode? Manus asserts but doesn't quantify.
- Counter-intuitive consequence: agents with deliberately noisier context may be MORE robust than agents with clean context. Empirically validated where?

## Sources

- [[2025-07-18 - Manus - Context Engineering for AI Agents]] (2025-07-18)
