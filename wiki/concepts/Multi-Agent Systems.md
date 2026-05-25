---
type: concept
title: Multi-Agent Systems
created: 2026-05-04
updated: 2026-05-10
tags:
- ai-agents
- agent-pattern
- taxonomy
status: developing
related: []
sources:
- "[[2025-06-13 - Anthropic - How we built our multi-agent research system]]"
- "[[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]]"
- "[[2025-09-29 - Anthropic - Effective context engineering for AI agents]]"
- "[[2025-10 - Zhang Khattab - Recursive Language Models]]"
- "[[2026-04-08 - Anthropic - Scaling Managed Agents]]"
_legacy_source_count: 4
---

# Multi-Agent Systems

## Summary

Architectures where multiple LLM agents — typically a coordinator plus parallel subagents — collaborate on a task. Per [[How we built our multi-agent research system]] (Anthropic 2025-06): not magically smarter than single agents; rather a **parallelism harness** that spends more tokens in parallel.

> [!contradiction] Counter-position: [[Ralph Loop]] (Geoffrey Huntley, 2026-01)
> [[2026-01-17 - Geoffrey Huntley - Everything is a Ralph Loop]] argues multi-agent is **premature complexity** for coding: because agents are non-deterministic, multiplexing them multiplies failure surface for little gain. Huntley prefers a **monolithic, single-process** agent ([[Ralph Loop]]) scaling vertically. Not a hard contradiction — Ralph targets iterative single-repo *coding*, which Anthropic's own "when NOT to use" carve-out flags as poorly parallelizable. Read as the opinionated monolithic pole opposite this page's coordinator+workers framing.

## Architecture (Anthropic's Research feature)

- **Lead agent** plans, persists plan to memory (context overflow protection)
- **Subagents** run with isolated contexts, **dynamically spawned** by lead — count, scope, tools all runtime-decided
- **CitationAgent** as a final grounding pass
- **Artifact system** — subagents write to shared filesystem to skip coordinator-as-bottleneck

## When to use (triple-conjunction per Anthropic)

A multi-agent system is the right shape when **all three** are true:

1. **Heavy parallelization possible** — subtasks are independent
2. **Information exceeds single context window** — can't fit in one agent's context
3. **High task value** — clears the cost premium

Empirical anchor: Opus 4 lead + Sonnet 4 subagents beats single-agent Opus 4 by **+90.2%** on Anthropic's research eval. Costs **~15× chat tokens**.

## When NOT to use

Anthropic explicitly carves out:

- **Coding tasks** — "fewer truly parallelizable tasks than research; LLM agents are not yet great at coordinating and delegating to other agents in real time"
- Domains where agents need shared context or have heavy interdependencies

> [!contradiction]
> The 2025-06 claim that "coding tasks have fewer truly parallelizable tasks than research" is complicated by [[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]] (2026-05), which shows a parallel-agent team successfully building a C compiler. The reconciliation: the carve-out applies to *small, tightly-coupled* coding tasks and *real-time coordination* during development — not large, modular codebases where subsystems can be interface-contracted and implemented independently. See "Fourth framing" section below for the updated model.

## Why it works

Per [[Token Economics]]: token usage alone explains **80% of variance** in BrowseComp performance; multi-agent's win is buying parallelism with tokens, not deploying superior reasoning.

## Second framing: sub-agent architectures as long-horizon technique (per Anthropic 2025-09)

[[Effective context engineering for AI agents]] reframes multi-agent / sub-agent architectures as **one of three techniques for long-horizon context management** (alongside compaction and structured note-taking). See [[Long-Horizon Context Management]].

The motivation is consistent — sub-agents return distilled outputs (1–2k tokens) instead of dumping their full working context onto the lead agent. This both saves attention budget and protects the lead from accumulated noise. So the case for multi-agent is now grounded in two complementary justifications:

1. **Parallelism harness** (per 2025-06 post) — buy more tokens-per-wall-clock-second
2. **Context-budget discipline** (per 2025-09 post) — keep the lead agent's window clean

## What multi-agent is NOT: recursive composition (per Zhang & Khattab 2025-10)

A clarifying boundary surfaced by [[2025-10 - Zhang Khattab - Recursive Language Models]]: **multiple LM invocations coordinating ≠ multi-agent system.**

RLMs use **recursive sub-LM calls inside a Python REPL** to process bounded slices of a long context. Literally there are multiple LM calls executing in coordination. But this is not what this page is about. The multi-agent pattern is specifically about **role-differentiated, coordinator+workers architectures** (the Anthropic Research feature) — distinct agent roles, separately-parameterized prompts, parallelism harness, strategic problem decomposition.

RLM is **single-agent recursive composition**:

- No role differentiation (sub-calls use the same prompt as the root)
- No parallelism harness (depth=1, sequential in reference impl)
- No orchestrator-worker structure (sub-calls are ad-hoc function calls in code, not orchestrated dispatch)
- Decomposition is **context-level**, not problem-level — see [[Context Decomposition vs Problem Decomposition]]

This boundary matters for the wiki's taxonomy: RLM is a [[Long-Horizon Context Management]] technique (a fourth one, alongside compaction / notes / sub-agents), NOT a multi-agent system. Conflating them collapses two different design decisions.

## Third framing: many brains, many hands (per Anthropic 2026-04)

[[Scaling Managed Agents]] adds an infrastructure layer: in a [[Meta-Harness]], **brains can pass hands to one another** through stable interfaces. Multi-agent orchestration stops being bespoke coupling and becomes a runtime primitive — sub-agent spawning, result-passing, and coordination all flow through the meta-harness's brain/hands/session APIs.

This shifts the cost calculus. The 15× chat-token premium ([[Token Economics]]) was partly justified by orchestration complexity. As that complexity moves into infrastructure, **the operational cost of multi-agent drops** — though the dollar/token cost of running more agent loops in parallel doesn't.

## Connections

- Refines: [[Workflows vs Agents]] (adds parallelism dimension)
- Strengthens (with carve-outs): [[Workflows Beat Agents for Most Production]]
- Architectural variant of: [[Orchestrator-Workers]] (agent variant — dynamic spawning, not predefined dispatch)
- Built on: [[Augmented LLM]]
- Eval methodology: [[LLM-as-Judge Evaluation]]
- One of four: [[Long-Horizon Context Management]]
- Distinct from (clarifying note above): [[Recursive Language Models]] — single-agent recursive composition, not multi-agent
- Counter-position: [[Ralph Loop]] — monolithic single-process pole, rejects multi-agent for coding
- Cost discipline: [[Token Economics]]
- Context discipline: [[Context Engineering]]

## Fourth framing: interface-contracted parallel workers (per Anthropic 2026-05)

[[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]] demonstrates multi-agent parallelism applied to **software engineering** — a domain Anthropic's 2025-06 post explicitly said had "fewer truly parallelizable tasks than research."

The compiler experiment architecture:
- **Orchestrator** defines interface contracts between subsystems before any worker begins
- **Workers** (one per compiler phase) operate in isolated context windows, implementing against the spec
- **Integration pass** reconciles outputs — multiple rounds needed when specs were underspecified

The critical update: **the triple-conjunction still applies**, but the "heavy parallelization possible" condition is met by large, *modular* codebases — not coding tasks generally. Small, tightly-coupled code is not amenable; large systems with clear subsystem boundaries are.

Key addition to the model: **interface specification quality is the bottleneck**, not raw token throughput. The orchestrator's system-design ability (writing clean contracts) determines integration overhead more than worker implementation capacity.

## Open questions

- Does the triple-conjunction generalize beyond research, or are there other narrow zones where multi-agent wins? *(Partially answered: modular software works; see fourth framing above.)*
- Asynchronous subagent execution — Anthropic flagged as future work; how does it shift the cost curve?
- Does multi-agent advantage hold as single-agent context windows grow (1M+)?
- How does multi-agent compare against [[Orchestrator-Workers]] workflow variant — when does dynamic spawning beat static dispatch on the same task?
- Does integration-reconciliation overhead scale linearly with worker count, or does it compound?

## Sources

- [[How we built our multi-agent research system]] (Anthropic, 2025-06-13)
- [[Effective context engineering for AI agents]] (Anthropic, 2025-09-29)
- [[Scaling Managed Agents]] (Anthropic, 2026-04-08)
- [[2025-10 - Zhang Khattab - Recursive Language Models]] (Zhang & Khattab, 2025-10) — clarifying boundary on what multi-agent is NOT
- [[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]] (Anthropic, 2026-05) — software engineering instantiation; complicates the "coding is less parallelizable" claim
