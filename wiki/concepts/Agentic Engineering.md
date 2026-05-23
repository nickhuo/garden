---
type: concept
title: "Agentic Engineering"
created: 2026-05-22
updated: 2026-05-22
status: seed
tags:
  - ai-agents
  - agentic-coding
  - foundational
related:
  - "[[Vibe Coding]]"
  - "[[Software 3.0]]"
  - "[[Jagged Intelligence]]"
  - "[[Agent-Native Infrastructure]]"
  - "[[Permission Model]]"
sources:
  - "[[2026-05-22 - Karpathy - Sequoia Ascent 2026]]"
---

# Agentic Engineering

The professional discipline of **coordinating fallible agents while preserving correctness, security, taste, and maintainability**. Where [[Vibe Coding]] raises the floor, agentic engineering **raises the ceiling**. After the December-2025 reliability jump, the unit of programming shifted from writing lines to delegating **macro actions** (implement a feature, refactor a subsystem, write and fix tests) — the engineer becomes an **orchestrator**.

## What the agentic engineer actually does

Doesn't blindly accept generated code. Instead:

- designs **specs** and supervises **plans**,
- inspects **diffs**,
- writes **tests**,
- manages **permissions** (see [[Permission Model]]),
- preserves quality, security boundaries, and taste.

## The frontier skill is concepts, not APIs

Agents handle API recall and boilerplate. The scarce human skill is understanding the *underlying* concepts the agent can get plausibly-but-dangerously wrong: storage, memory copies, invariants, **identity**, security boundaries, the overall shape of the system. The MenuGen Stripe-vs-Google email-mismatch bug is the canonical example — an identity error only conceptual understanding catches.

## Hiring should change

Coding puzzles mismatch the real skill. Karpathy's proposed interview: build a substantial project *with agents*, deploy it securely, then have **adversarial agents try to break it**. This tests decomposition, spec-writing, review, securing systems, and using agents as leverage. The "10x engineer" may become "much more extreme" — mastery compounds through agent leverage.

## Why fallibility is structural

Agents are jagged (see [[Jagged Intelligence]]) — brilliant then bizarrely wrong. Agentic engineering is the human practice that wraps that jaggedness in guardrails, complementing [[Agent-Native Infrastructure]] (building systems agents can safely act on) on the tooling side.

## Source

- [[2026-05-22 - Karpathy - Sequoia Ascent 2026]] — entity: [[Andrej Karpathy]]
