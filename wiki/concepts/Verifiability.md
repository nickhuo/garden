---
type: concept
title: "Verifiability"
created: 2026-05-22
updated: 2026-05-22
status: seed
tags:
  - ai-agents
  - llm
  - evaluation
  - foundational
related:
  - "[[Jagged Intelligence]]"
  - "[[The Bitter Lesson]]"
  - "[[Welcome to the Era of Experience]]"
  - "[[Software 3.0]]"
sources:
  - "[[2026-05-22 - Karpathy - Sequoia Ascent 2026]]"
---

# Verifiability

> "Traditional software automates what you can **specify**; LLMs automate what you can **verify**." — Karpathy, Sequoia Ascent 2026

The single best predictor of where AI capability moves fastest. A task is **verifiable** when success produces an automatic signal: tests pass/fail, a program runs/crashes, a benchmark scores, a game is won. Verifiable tasks admit powerful reinforcement learning, so models improve quickly there; tasks without a reward signal stagnate or stay rough.

## Why coding feels "dramatically better"

Code is maximally verifiable — compile, run, test, benchmark. The December-2025 reliability jump in coding agents is downstream of this: tight, automatic feedback loops let RL grind the domain. Math, formal reasoning, and games share the property.

## The founder wedge

Karpathy's actionable version: find domains that are **valuable, verifiable, and undertrained by frontier labs**. Coding and math are already saturated. Many economically important domains have "latent verifiable structure that has not yet been exploited" — build the reward environment and you can fine-tune or RL your way to performance the base model lacks. The diagnostic is [[Jagged Intelligence]]'s "are you on the model's rails?"

## Connections

- [[The Bitter Lesson]] — verifiable environments are exactly where scaled search/RL wins.
- [[Welcome to the Era of Experience]] (Silver & Sutton) — grounded environmental reward over human prejudgment; the "why now" for verifiability-driven learning.
- [[Jagged Intelligence]] — verifiability is one of its two axes (the other is training attention).
- Evaluation pages this sharpens: [[Eval Validity]], [[Pass^k Reliability Metric]], [[Trace-Based Evaluation]] — a verifiable reward is the strongest form of eval signal.

## Source

- [[2026-05-22 - Karpathy - Sequoia Ascent 2026]] — entity: [[Andrej Karpathy]]
