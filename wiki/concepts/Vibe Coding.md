---
type: concept
title: "Vibe Coding"
created: 2026-05-22
updated: 2026-05-22
status: seed
tags:
  - ai-agents
  - agentic-coding
related:
  - "[[Agentic Engineering]]"
  - "[[Software 3.0]]"
  - "[[Andrej Karpathy]]"
sources:
  - "[[2026-05-22 - Karpathy - Sequoia Ascent 2026]]"
---

# Vibe Coding

Building software by **describing what you want** in natural language and accepting what the agent produces, without engineering discipline over the output. Vibe coding **raises the floor**: nearly anyone can now create working software.

## Vibe coding vs. agentic engineering

The two are complementary, not rivals — they move different ends of the distribution:

| | Vibe coding | [[Agentic Engineering]] |
|---|---|---|
| Effect | Raises the **floor** | Raises the **ceiling** |
| Who | Anyone | Professionals |
| Stance toward output | Accept it | Spec, review, test, secure it |
| Risk owned | Little | Correctness, security, taste, maintainability |

The danger of pure vibe coding is illustrated by Karpathy's MenuGen payment bug: an agent matched Stripe purchases to Google accounts by email, but the Stripe email and Google login email can differ — a plausible-looking identity bug that only review would catch. Vibe coding ships it; agentic engineering catches it.

## A mode within Software 3.0

Vibe coding is the low-discipline expression of [[Software 3.0]] (programming in natural language). It's genuinely valuable for prototypes, throwaway tools, and democratized creation — the failure mode is treating it as sufficient for systems that need correctness or security.

## Source

- [[2026-05-22 - Karpathy - Sequoia Ascent 2026]] — entity: [[Andrej Karpathy]]
