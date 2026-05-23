---
type: concept
title: "Software 2.0"
created: 2026-05-20
updated: 2026-05-20
tags:
  - ai-agents
  - llm
  - foundational
  - architecture
status: developing
related:
  - "[[Software 3.0]]"
  - "[[Model-Centric Architecture]]"
  - "[[The Bitter Lesson]]"
sources:
  - "[[2017-11-11 - Karpathy - Software 2.0]]"
  - "[[2026-05-22 - Karpathy - Sequoia Ascent 2026]]"
---

# Software 2.0

## Summary

A new software stack in which the program is the **weights of a neural network**, learned from data, rather than instructions written by hand (high confidence; Source: [[2017-11-11 - Karpathy - Software 2.0]]). The developer specifies a goal and an architecture; optimization searches program space for an implementation. Karpathy's 2025 extension adds **Software 3.0**: programming the model in natural-language prompts, with LLMs acting as a new operating system (medium confidence; Source: [[2017-11-11 - Karpathy - Software 2.0]] and the 2025 "Software Is Changing (Again)" talk).

## Why it matters

It names the migration that [[Model-Centric Architecture]] generalizes to agents: logic that once lived in hand-written code (Software 1.0) moves into learned weights (2.0) and prompts (3.0). For agent builders this reframes the question from "what code orchestrates the model?" to "what does the model own, and what stays as code to the side?"

## Limits / when pipelines still win

- Weights are **opaque** and "fail in unintuitive and embarrassing ways," silently absorb data biases, and are adversarially vulnerable (Source: [[2017-11-11 - Karpathy - Software 2.0]]). Inspectable code remains better where auditability and hard guarantees matter.
- Software 2.0 excels at perception; agentic side-effecting actions still benefit from deterministic boundaries (constrained decoding, schema validation — cf. Nick's Donut and Beckman).

## Connection to prior work

The architectural companion to [[The Bitter Lesson]] (scaling general methods) — Karpathy supplies the *stack* framing, Sutton the *why it wins* framing. Foundational to [[Model-Centric Architecture]].

## Connections

- [[Software 3.0]] — the natural-language-programming successor, developed at length in [[2026-05-22 - Karpathy - Sequoia Ascent 2026]]
- [[Model-Centric Architecture]]
- [[The Bitter Lesson]]
- [[Context Engineering]]
- [[Andrej Karpathy]]

## Open questions

- If prompts are Software 3.0, are harnesses and schemas a fourth, durable layer — or scaffolding 2.0 will absorb?
- How much of agent "interface logic" is irreducibly code vs. learnable?

## Sources

- [[2017-11-11 - Karpathy - Software 2.0]]
