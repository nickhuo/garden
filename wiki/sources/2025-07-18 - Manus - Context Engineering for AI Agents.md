---
type: source
title: "Context Engineering for AI Agents: Lessons from Building Manus"
created: 2026-05-10
updated: 2026-05-10
tags:
- ai-agents
- context-engineering
- manus
- non-anthropic
status: mature
related: []
sources:
  - "[[.raw/articles/2025-07-18 - Manus - Context Engineering for AI Agents.md]]"
- '[[03_Resources/.raw/articles/2025-07-18 - Manus - Context Engineering for AI Agents.md]]'
source_type: blog
author: Yichao 'Peak' Ji
date_published: 2026-05-10
url: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
confidence: medium
key_claims: []
---

# Context Engineering for AI Agents: Lessons from Building Manus

## Summary

First non-Anthropic source ingested. Yichao 'Peak' Ji (founder of [[Manus]], now acquired by Meta) shares six production lessons from four full rebuilds of the Manus agent framework. The thesis: bet on context engineering, not training your own model — "if model progress is the rising tide, we want Manus to be the boat, not the pillar stuck to the seabed."

The post coins **"Stochastic Graduate Descent (SGD)"** for the empirical, prompt-fiddling, trial-and-error nature of agent-framework iteration — a deliberate jab at how unscientific the discipline still is.

Critically, several lessons here **disagree with or qualify** Anthropic's positions:

- Lesson 2 (Mask, Don't Remove) **contradicts** Anthropic's [[Tool Search Tool]] approach of dynamic tool loading. Anthropic's later (Nov 2025) [[Advanced Tool Use|advanced tool use]] release explicitly responds to the KV-cache concern Manus raised.
- Lesson 1 (KV-Cache Discipline) introduces a **third cost axis** beyond Anthropic's dual-cost (dollars / attention) framing — see [[Token Economics]].

## Key points (Nick's words)

- **KV-cache hit rate is THE production metric.** ~10× cost gap on Claude Sonnet ($0.30 vs $3 / MTok cached vs uncached). Input:output token ratio in Manus is ~100:1, so prefill dominates. Three rules: stable prefix (no second-precision timestamps), append-only context, deterministic serialization (watch JSON key ordering).
- **Mask, don't remove.** Don't dynamically add/remove tools mid-iteration. Use logit masking via state machine + consistent action-name prefixes (`browser_`, `shell_`) for prefill-based action constraint. Two reasons: KV-cache invalidation + dangling references from prior turns hallucinate.
- **File system as context.** Unlimited externalized memory; the agent reads/writes files on demand. Compression must be **restorable** — drop a web page's content but keep its URL, drop a document's bytes but keep its path. Speculation: this might unlock agentic SSMs as successors to Neural Turing Machines.
- **Recitation is attention manipulation.** `todo.md` rewritten step-by-step pushes objectives into the recent-attention window. ~50 tool calls per task average; lost-in-the-middle + goal drift are real risks. No architecture change required; pure context shaping.
- **Keep the wrong stuff in.** Don't hide errors — failure traces shift the model's prior away from repeating the action. Error recovery is the strongest indicator of true agentic behavior, and is underrepresented in academic benchmarks.
- **Don't get few-shotted.** Repetitive contexts cause models to mimic past pattern even when suboptimal (e.g., resume-review batch fall-through). Inject controlled diversity — alternate templates, phrasing, formatting noise.

## Evidence

- 10× KV-cache cost gap on Claude Sonnet: $0.30 / MTok cached vs $3 / MTok uncached — see [[KV-Cache Discipline]]
- 100:1 input:output token ratio in Manus — see [[KV-Cache Discipline]]
- ~50 tool calls per typical Manus task — see [[Recitation]]
- Framework rebuilt 4× via "Stochastic Graduate Descent"
- Acknowledges "millions of users" at time of writing (July 2025)
- Cites Hermes function-calling format (NousResearch), vLLM, MCP, BERT/GPT-3/Flan-T5, ReAct, Neural Turing Machines

## Connections

- New entity: [[Manus]]
- New concepts: [[KV-Cache Discipline]] · [[Logit Masking]] · [[Recitation]] · [[Error Trace Retention]] · [[Few-Shot Drift]]
- Updates: [[Context Engineering]] · [[Long-Horizon Context Management]] · [[Just-in-Time Context Retrieval]] · [[ACI - Agent-Computer Interface]] · [[Token Economics]]
- Direct tension with: [[Tool Search Tool]] (Anthropic Nov 2025)

## Open questions

- Manus has rebuilt 4×; what was wrong with each previous version? Post is silent on the dead ends.
- The 100:1 prefill:decode ratio — does this hold for non-Manus agents, or is it harness-specific?
- "Stochastic Graduate Descent" implies no principled architecture — does that mean the lessons are local optima Manus-only, or genuinely universal?
- Manus's logit-masking approach assumes you control the inference stack. Does it work over a hosted API (e.g., Anthropic's Messages API) where you can't intercept decoding?
- SSM-as-agent speculation — is anyone actually building one? Mamba-Hawk-Falcon variants haven't broken into agentic use as of source date.

## Sources

- self (this source page)