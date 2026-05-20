---
type: concept
title: Recitation
created: 2026-05-10
updated: 2026-05-10
tags:
- ai-agents
- attention
- context
- long-horizon
status: developing
related: []
sources:
- "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
aliases:
- Goal Recitation
- todo.md pattern
- Attention Manipulation via Repetition
_legacy_source_count: 1
---

# Recitation

## Summary

Per [[2025-07-18 - Manus - Context Engineering for AI Agents]]: a deliberate context-engineering mechanism where the agent **rewrites its goals (and progress) at the end of context every step**, pushing the global plan into the model's recent-attention window. Manus uses a `todo.md` file as the concrete instrument: read, update, check off completed items, write back — each cycle.

The function is **attention manipulation**, not memory. The information is already in earlier context; recitation moves it from the model's stale (lost-in-the-middle) attention zone to its sharpest (recency-biased) zone.

## Why this works

Two well-documented LLM failure modes converge on long-running agents:

- **Lost-in-the-middle** — recall is worst for content in the middle of a long context, better at the start and end.
- **Goal drift** — over many tool-call iterations (Manus averages ~50 per task), the original objective gets diluted by intervening observations.

Recitation exploits the recency bias: the goal sits at the bottom of the prompt where attention is sharpest, every step. No architectural change required — just structured rewriting.

## Mechanism

1. At task start, the agent writes `todo.md` summarizing the plan.
2. Each step (or after each significant tool call), the agent reads `todo.md`, updates it (checks off completed items, refines remaining steps, adds new sub-tasks), and writes it back.
3. Because the file's contents enter context near the end of each loop iteration, **the model's most attentionally-salient tokens are always the current plan**.

Note: the file isn't strictly necessary — what matters is the **rewriting at the end of context**. The file is the device that makes the rewriting easy and append-friendly. See [[Long-Horizon Context Management]] for the file-system-as-memory framing.

## Why this is more than just "scratchpad"

A traditional scratchpad / note-taking pattern (per Anthropic 2025-09, [[Long-Horizon Context Management]]) externalizes state so it doesn't take attention. Recitation does the opposite: it deliberately puts state *back* into attention, but at the position where attention is strongest.

Two different uses of the same file-system memory primitive:

| Mechanism | Where info lives | Function |
|---|---|---|
| Structured note-taking | Off-context, in file | Free up attention budget |
| Recitation | **Recurring in recent context** | Bias attention toward goal |

Both can coexist (and in Manus, do) — notes for everything; `todo.md` is the subset deliberately recited.

## Connections

- Variant of: [[Long-Horizon Context Management]] (file-system-as-memory, but used for attention not capacity)
- Mitigates: lost-in-the-middle failure mode (covered descriptively in [[Context Engineering]])
- Compatible with: [[KV-Cache Discipline]] — if the recitation lives at the end of context, it doesn't invalidate the cached prefix
- ACI implication: tools must support read-modify-write semantics on small text files cheaply — see [[ACI - Agent-Computer Interface]]

## Open questions

- Is the effect from *content* or *position*? If you put the same `todo.md` content at a fixed earlier position, do you lose the benefit?
- Cost — recitation adds tokens to every iteration. What's the right cadence: every step, every N steps, only after observation?
- Failure modes — agent writes a stale `todo.md` and recites the wrong goal. Manus doesn't say how often this happens or how it's caught.
- Does recitation help models with explicit thinking / scratchpad modes (Claude extended thinking, o1-style reasoning), or is it strictly a non-reasoning-model technique?
- Generalization — `todo.md` is one device; are there other recitation surfaces (current-state summary, top-3-priorities) that work better for different task shapes?

## Sources

- [[2025-07-18 - Manus - Context Engineering for AI Agents]] (2025-07-18)
