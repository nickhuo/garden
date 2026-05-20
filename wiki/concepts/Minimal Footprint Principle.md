---
type: concept
title: Minimal Footprint Principle
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - safety
  - foundations
complexity: basic
domain: ai-agents
aliases:
  - minimal footprint
  - prefer reversibility
status: developing
related:
  - "[[Autonomous Agents]]"
  - "[[Permission Classifier]]"
  - "[[Claude Code]]"
  - "[[Workflows vs Agents]]"
  - "[[ACI - Agent-Computer Interface]]"
sources:
  - "[[2024-12-19 - Anthropic - Building Effective Agents]]"
  - "[[2026-04 - Anthropic - Claude Code Auto Mode]]"
---

# Minimal Footprint Principle

## Summary

A core safety principle for agentic systems: **prefer actions that are reversible, do less when uncertain, and avoid side effects that weren't explicitly requested.** First stated in [[Building Effective Agents]] (Anthropic, 2024-12) as guidance for Claude in agentic contexts; operationalized mechanically in [[Claude Code]] auto mode's [[Permission Classifier]] (April 2026).

## The principle

> Prefer reversible over irreversible actions. When uncertain, do less. Avoid side effects not explicitly requested.

Three rules that compose into a posture:

1. **Reversibility preference** — between two actions that achieve the same goal, always pick the one that's easier to undo.
2. **Conservative under uncertainty** — if the intent is ambiguous, take the narrowest interpretation. Ask before expanding.
3. **Scope discipline** — don't touch things that aren't in scope for the current task, even if you can.

## Two enforcement points

As of April 2026, the principle is enforced at two distinct layers:

| Layer | Mechanism | Where |
|---|---|---|
| In-context reasoning | Claude's system prompt guidance | All agentic Claude deployments |
| Tool-call classifier | [[Permission Classifier]] in [[Claude Code]] auto mode | Claude Code headless deployments |

This is notable: the same principle is now expressed both as a reasoning constraint (the model is instructed to reason this way) and as a mechanical policy (an external classifier enforces it at the tool-call boundary). Defense in depth at the principle level.

## Why it matters for autonomous agents

Autonomous agents — by definition — take sequences of actions without human checkpoints. The cost of a mistake compounds: a bad file deletion early in an agent run can break all subsequent steps. The minimal footprint principle is the primary risk mitigation for this compounding failure mode.

Concretely: an agent that defaults to "read before write," "create before delete," and "ask before network" will fail safely in most cases even when its reasoning goes wrong.

## Relationship to permission systems

The [[Permission Classifier]] in Claude Code auto mode operationalizes the principle mechanically:

- File reads: ~98% auto-approve (reversible)
- File deletions: ~5% auto-approve (irreversible)
- System modifications: ~2% auto-approve (highly irreversible)

The classifier's risk calibration maps directly onto reversibility: the less reversible an action, the higher the bar for auto-approval.

## Connections

- Operationalized by: [[Permission Classifier]] (Claude Code auto mode)
- Use case: [[Autonomous Agents]] · [[Managed Agents]] headless deployments
- Design philosophy: [[ACI - Agent-Computer Interface]] (safety as interface design)
- Trade-off against: agent efficiency — minimal footprint agents will sometimes pause when they shouldn't
- Decision rule: [[Workflows vs Agents]] (prefer workflow patterns when reversibility matters most)

## Open questions

- Is there a quantitative reversibility metric? "Reversible vs irreversible" is categorical; real systems have a spectrum.
- How does minimal footprint interact with long-horizon tasks where inaction itself has costs?
- Should the principle extend to token usage? (Minimal context footprint as an efficiency analog)

## Sources

- [[2024-12-19 - Anthropic - Building Effective Agents]] (Anthropic, 2024-12-19) — first statement of the principle
- [[2026-04 - Anthropic - Claude Code Auto Mode]] (Anthropic, April 2026) — mechanical operationalization via Permission Classifier
