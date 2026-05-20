---
type: concept
title: ReAct
created: 2026-05-19
updated: 2026-05-19
tags:
- ai-agents
- reasoning
- decision-making
status: developing
related:
- "[[CoALA]]"
- "[[Tree of Thoughts]]"
- "[[Think Tool]]"
- "[[Augmented LLM]]"
- "[[Shunyu Yao]]"
sources:
- "[[2023-09-05 - Sumers et al - Cognitive Architectures for Language Agents]]"
---

# ReAct

The **Reason + Act** pattern (Yao et al., 2022): an agent interleaves **reasoning** traces (internal) with **grounding** actions (external) in a single fixed loop — think, act, observe, think, act. Each reasoning step conditions the next action; each observation conditions the next thought.

## In CoALA terms

[[CoALA]] places ReAct as a minimal but influential point in the design space:
- **Memory:** working only — no episodic or semantic long-term memory.
- **Actions:** reasoning (internal) + grounding (external), no *learning* action.
- **Decision cycle:** fixed — propose-and-execute with **no evaluation/selection** step. It commits to the action it generates.

## Why it mattered

ReAct demonstrated the **synergy** between reasoning and environmental feedback: reasoning alone hallucinates, acting alone can't plan, but interleaving them grounds the reasoning in observations and lets observations steer the reasoning. It is the conceptual ancestor of the [[Think Tool]] (a reasoning-only internal action carved out as an explicit tool) and the default skeleton of most tool-using [[Augmented LLM]] agents today.

Its limitation — no deliberate evaluation of alternatives — is exactly what [[Tree of Thoughts]] adds.
