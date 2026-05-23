---
type: concept
title: "Human-in-the-Loop Intervention"
created: 2026-05-22
updated: 2026-05-22
status: seed
tags:
  - ai-agents
  - safety
related:
  - "[[Agent Guardrails]]"
  - "[[Permission Model]]"
  - "[[Minimal Footprint Principle]]"
  - "[[Agent Run Loop]]"
sources:
  - "[[2025 - OpenAI - A Practical Guide to Building Agents]]"
---

# Human-in-the-Loop Intervention

A critical safeguard that lets an agent **gracefully transfer control to a human** when it can't complete a task. OpenAI's [[2025 - OpenAI - A Practical Guide to Building Agents]] stresses it is "especially important early in deployment" — it surfaces failures, uncovers edge cases, and bootstraps a robust evaluation cycle. Customer service → escalate to a human agent; coding agent → hand control back to the user.

## Two primary triggers

1. **Exceeding failure thresholds** — set limits on retries/actions; if the agent exceeds them (e.g. fails to understand intent after several attempts), escalate. These limits are exactly the max-turns/error exits of the [[Agent Run Loop]].
2. **High-risk actions** — sensitive, irreversible, or high-stakes actions trigger human oversight until the agent's reliability is proven: canceling orders, authorizing large refunds, making payments.

## Relation to existing pages

- The escalation half of [[Agent Guardrails]] — when automated guardrails can't safely decide, route to a human.
- High-risk triggers are the human-gated tier of [[Permission Model]] and the conservative default of [[Minimal Footprint Principle]] (prefer reversible actions; do less when uncertain).
- Karpathy's "keep a human-controllable autonomy slider" stance (see [[Andrej Karpathy]]) is the same instinct expressed at the design-philosophy level; [[Agentic Engineering]] is the human discipline this safeguard institutionalizes.

## Source

- [[2025 - OpenAI - A Practical Guide to Building Agents]] — vendor: [[OpenAI]]
