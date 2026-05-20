---
type: concept
title: Context Decomposition vs Problem Decomposition
created: 2026-05-10
updated: 2026-05-10
tags:
- ai-agents
- decomposition
- architecture
- framing
status: developing
related: []
sources:
- "[[2025-10 - Zhang Khattab - Recursive Language Models]]"
aliases:
- Decomposition Axis
- Context vs Problem Decomposition
_legacy_source_count: 1
---

# Context Decomposition vs Problem Decomposition

## Summary

A clean architectural axis articulated in [[2025-10 - Zhang Khattab - Recursive Language Models]]: when an agent system needs to "decompose" a task, **what is the unit being decomposed?**

Two distinct schools:

- **Problem decomposition** (prior default) — break the *problem* into sub-tasks, usually by human-curated patterns: "first plan, then search, then synthesize," or "spawn three role-differentiated sub-agents." Decomposition logic lives in the scaffold/programmer; the LM follows.
- **Context decomposition** (RLM's contribution) — break the *context* into sub-regions, with the LM deciding at inference time how to chunk, peek, grep, partition, and recurse. Decomposition logic lives in the LM itself, expressed in code at the REPL boundary.

This axis cuts orthogonally across the [[Workflows vs Agents]] taxonomy. Both workflows and agents have historically been problem-decomposition designs. RLMs are the first concrete pattern that defers decomposition strategy to the LM at the context layer.

## Why the distinction matters

Problem decomposition assumes the programmer knows the structure of useful sub-tasks. This works when the task family is well-understood (research, customer support, code review) — see [[Orchestrator-Workers]], [[Multi-Agent Systems]]. It fails when:

- The task structure varies per input (one query needs grep, another needs map-reduce)
- The right decomposition depends on context shape (only inspectable at inference time)
- Pre-committing to a decomposition wastes effort on inputs that don't match

Context decomposition shifts the lever. The LM examines the context, chooses a strategy, executes it as code, and recurses. The programmer specifies the *substrate* (REPL, sub-LM-callable function), not the *strategy*. See [[Recursive Language Models]].

## Where the wiki's existing concepts sit on this axis

| Pattern | Decomposition axis | Locus of decomposition strategy |
|---|---|---|
| [[Prompt Chaining]] | Problem | Programmer (chain fixed) |
| [[Routing]] | Problem | Programmer (router fixed; LM picks branch) |
| [[Parallelization]] | Problem | Programmer (sectioning rule fixed) |
| [[Orchestrator-Workers]] (workflow variant) | Problem | Programmer (dispatch fixed) |
| [[Orchestrator-Workers]] (agent variant) | Problem | LM (dynamic dispatch, but tasks pre-modeled) |
| [[Evaluator-Optimizer]] | Problem | Programmer (gen + critique fixed) |
| [[Autonomous Agents]] | Problem | LM (open-ended task decomposition) |
| [[Multi-Agent Systems]] | Problem | LM (lead agent spawns role-specific sub-agents) |
| [[Programmatic Tool Calling]] | **Problem** (tool orchestration is problem-structure) | LM, expressed in code |
| [[Tool Search Tool]] | Problem (action-space narrowing) | LM (search-driven) |
| **[[Recursive Language Models]]** | **Context** | **LM, expressed in code** |
| [[Long-Horizon Context Management]] | Mixed — compaction is problem (timeline-shaped), notes are problem (state-shaped), sub-agents are problem (parallel branches), but file-system-as-context (Manus) is context | Mixed |

The honest reading: **most of the wiki sits on the problem-decomposition side**. RLM is the first clean instance of context decomposition that doesn't collapse into something else.

## The author's quote (load-bearing)

> "Agents are designed based on human / expert intuition on how to break down a problem to be digestible for an LM. RLMs are designed based on the principle that fundamentally, LMs should decide how to break down a problem to be digestible for an LM."

The frame: human-curated problem decomposition is a *bet on knowing the task structure*. Context decomposition is a *bet on the LM being a better judge of decomposition than the programmer*.

## When each wins

**Problem decomposition wins when:**

- The task family is mature and patterns are well-known (most production today)
- Latency or cost predictability matters (programmer-fixed decomposition gives bounded behavior)
- Debuggability matters (you can trace exactly which sub-task ran when)
- The LM's judgment about decomposition is worse than the programmer's

**Context decomposition wins when:**

- Inputs vary in shape and the right strategy isn't knowable upfront
- Context is genuinely large and pre-decomposition wastes compute
- The LM's judgment about context structure approaches or exceeds the programmer's
- You're willing to trade predictability for adaptive efficiency

## Tension with [[Workflows Beat Agents for Most Production]]

The thesis says workflows beat agents for most production today, partly because **programmer-controlled decomposition outperforms LM-controlled decomposition** on cost, latency, and debuggability. RLM's empirical wins (RLM(GPT-5-mini) > GPT-5 by 114%) are evidence that **LM-controlled context decomposition can beat baseline single-model calls** — but the comparison isn't apples-to-apples. RLM beats *uncomposed long-context calls*; it doesn't directly compete with a well-designed workflow for the same task.

The honest interpretation: context decomposition is a new affordance available to *both* workflow-shaped and agent-shaped systems. A workflow that wraps an RLM step (LM does context decomposition inside a programmer-fixed orchestration) might be the strongest design.

## Open questions

- **Is this axis truly orthogonal to workflow/agent, or does context decomposition only work in agent-shaped systems?** Could a workflow pipeline include an RLM-style step as a primitive?
- **Composability with multi-agent.** Could a multi-agent system include RLM sub-agents whose specialty is context-handling? Plausible but unpublished.
- **How does context decomposition handle multi-modality?** OOLONG and BrowseComp-Plus are text-only. Image, audio, video contexts — do the same patterns apply?
- **Can context decomposition be RL-trained?** Author claims yes; no model exists yet.
- **Cost trajectory.** Problem decomposition gives bounded cost via fixed structure. Context decomposition gives unbounded cost via LM-decided depth. What primitives let production teams enforce cost ceilings without losing the adaptivity benefit?

## Connections

- Canonical instance: [[Recursive Language Models]]
- Adjacent inference-time patterns: [[Programmatic Tool Calling]] (problem axis), [[Tool Search Tool]] (problem axis)
- Tension with: [[Workflows Beat Agents for Most Production]] (which favors programmer-controlled decomposition)
- Conceptual sibling of: [[Context Engineering]] (both are "context as the object," but [[Context Engineering]] shapes context for the LM; context decomposition lets the LM shape context for itself)
- Source: [[2025-10 - Zhang Khattab - Recursive Language Models]]

## Sources

- [[2025-10 - Zhang Khattab - Recursive Language Models]] (Zhang & Khattab, 2025-10)
