---
type: concept
title: Learning from Implicit Feedback
created: 2026-05-20
updated: 2026-05-20
tags: [ai-agents, llm, real-time-learning, implicit-feedback, rlhf]
status: developing
related: ["[[Online Learning from Interaction]]", "[[In-Context Learning]]", "[[Test-Time Adaptation]]"]
sources: ["[[2025-05-21 - Meta - Reinforcement Learning from User Feedback]]", "[[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]"]
---

# Learning from Implicit Feedback

## Summary

Implicit feedback is signal the user emits **without being asked to rate anything**: accepting or editing a suggestion, copying output, asking a follow-up, changing direction, abandoning the session, or staying silent. Meta's RLUF shows these production signals can train preference/reward models competitive with explicit human ratings, enabling continuous improvement from live traffic (confidence: medium — single source; Source: [[2025-05-21 - Meta - Reinforcement Learning from User Feedback]]). This is the digital-product instance of [[Welcome to the Era of Experience]]'s **grounded reward** (confidence: high for the principle; Source: [[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]).

## Signal taxonomy

- **Correction** — user fixes the output: strong negative on the original, positive on the fix.
- **Follow-up / continuation** — engagement; weak positive.
- **Direction change** — the prior trajectory was wrong: negative.
- **Silence / no correction** — weak positive (didn't need fixing) — but ambiguous.
- **Abandonment** — strong negative.

## Why it matters

Explicit feedback (thumbs, ratings) is sparse and biased toward extremes. Implicit signals are abundant and free, collected passively — the only feedback available at production scale for most agents. For real-time learning they are the actual reward stream.

## When X still wins (limits)

- **Bias and confounding** — engagement ≠ correctness; satisfied users also disengage; clicks can be optimized at the cost of truthfulness (reward hacking).
- **Attribution** — hard to know *which* action caused a delayed signal.
- **Explicit feedback still wins** for safety-critical or rare-but-important cases where you cannot afford to learn the wrong lesson from noisy proxies.

## Connection to prior work

Sits within RLHF lineage (preference modeling) but swaps annotator labels for behavioral signals. Complements [[In-Context Learning]] (a correction immediately re-conditions the prompt) and feeds [[Online Learning from Interaction]] (the same signal can update memory or weights).

## Connections — Nick's projects

- **Donut:** confidence gating *is* implicit-feedback discipline — only high-confidence neighbors write back, the data-layer version of "only update on trustworthy signal."
- **Compass:** user logs are implicit/explicit feedback fed into KB priority and eval rubric — a governed closed loop that decides which signals are allowed to change policy.
- **Sonic:** the streaming substrate that makes implicit signals capturable in near-real-time at all.

## Open questions

- How to debias implicit signals (satisfied-silence vs. confused-silence)?
- Which signals are safe to auto-update on vs. require a human gate?

## Sources

- [[2025-05-21 - Meta - Reinforcement Learning from User Feedback]]
- [[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]
