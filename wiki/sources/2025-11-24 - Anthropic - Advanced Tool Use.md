---
type: source
title: Introducing advanced tool use on the Claude Developer Platform
aliases:
  - Advanced Tool Use
created: 2026-05-10
updated: 2026-05-13
tags:
- ai-agents
- tool-use
- anthropic
- mcp
- context-engineering
status: mature
related: []
sources:
  - "[[.raw/articles/2025-11-24 - Anthropic - Advanced Tool Use.md]]"
source_type: blog
author: Bin Wu (Anthropic, with the Claude Developer Platform team)
date_published: 2025-11-24
url: https://www.anthropic.com/engineering/advanced-tool-use
confidence: medium
key_claims: []
---

# Introducing advanced tool use on the Claude Developer Platform

## Summary

Product announcement (Nov 24, 2025) introducing three beta features on the Claude Developer Platform that move tool use "from simple function calling toward intelligent orchestration." Each addresses a specific bottleneck in production tool-use workflows:

1. **[[Tool Search Tool]]** — defers tool definitions out of the initial prompt; Claude searches and loads them on demand. 85% token reduction (134K → ~8.7K tool-def overhead in Anthropic's internal case); Opus 4 MCP eval 49→74%, Opus 4.5 79.5→88.1%.
2. **[[Programmatic Tool Calling]]** — Claude writes Python in a sandboxed code-execution env that orchestrates tool calls; intermediate results stay in the sandbox, only the final reduction enters context. 37% token reduction (43.6K→27.3K); GAIA 46.5→51.2%; internal KB retrieval 25.6→28.5%.
3. **[[Tool Use Examples]]** — adds `input_examples` field on tool defs teaching format/correlation patterns JSON Schema can't express. 72→90% on complex parameter handling.

Beta header: `betas=["advanced-tool-use-2025-11-20"]`. Claude for Excel cited as the flagship internal user (uses PTC to read/modify spreadsheets with thousands of rows without overloading context).

## Notable context: this post is in dialogue with [[2025-07-18 - Manus - Context Engineering for AI Agents]]

Anthropic's Tool Search Tool is **architecturally opposite** to Manus's [[Logit Masking]] approach. Manus argued (4 months earlier) *against* dynamic action spaces because they invalidate KV-cache and create dangling references. Anthropic's Nov-2025 release explicitly counters both points:

- KV-cache: "Tool Search Tool doesn't break prompt caching because deferred tools are excluded from the initial prompt entirely. They're only added to context after Claude searches for them, so your system prompt and core tool definitions remain cacheable."
- Dangling references: tools are *added* by search, never removed mid-trajectory.

Both designs are internally consistent — they differ on whether to optimize for static cacheability (Manus) or dynamic discovery with cache-safe infra (Anthropic). See [[Static Action Spaces vs Dynamic Tool Discovery]].

## Key points (Nick's words)

- **Tool Search Tool**: mark tools `defer_loading: true`; Claude only sees Tool Search Tool itself + non-deferred tools upfront. On demand, Claude searches by keyword (regex/BM25 built-in, embedding-based custom search supported); matched tools expand into context. Critically, deferred tool defs **never enter the initial prompt** — so the cacheable prefix is preserved. Anthropic also supports per-server `defer_loading` on MCP servers (defer the whole server, keep one high-use tool eager-loaded).
- **Programmatic Tool Calling (PTC)**: opt-in tools via `allowed_callers: ["code_execution_20250825"]`. Claude generates Python in a `server_tool_use` block; the code executes in the sandbox; when it calls an opt-in tool, the API surfaces a tool request with a `caller` field; results go back to the sandbox, not to Claude. Only `stdout` reaches Claude's context at the end. The reduction is **two orders of magnitude in extreme cases** (200KB raw expense data → 1KB result on the budget-compliance example).
- **Tool Use Examples**: `input_examples` array on a tool def with full / partial / minimal sample invocations. Demonstrates format conventions (date formats, ID conventions), nested-structure patterns, and parameter-correlation rules. Best practice: 1-5 examples per tool, realistic data, focus on ambiguity.
- **Layering strategy**: pick the bottleneck. Tool def bloat → Tool Search; intermediate result bloat → PTC; parameter errors → Examples. They're complementary, not all-or-nothing.

## Evidence

- **Tool Search Tool**: 134K tokens of tool defs observed internally before optimization; 5-server example (GitHub 35 tools, Slack 11, Sentry 5, Grafana 5, Splunk 2) consumes 55K tokens upfront. Tool Search reduces to ~500 tokens (the search tool itself) + ~3K (loaded tools) ≈ 8.7K. 85% reduction; Opus 4 MCP eval 49→74%, Opus 4.5 79.5→88.1%.
- **Programmatic Tool Calling**: average token usage dropped 43,588 → 27,297 (37%). GAIA benchmark 46.5→51.2%; internal knowledge retrieval 25.6→28.5%.
- **Tool Use Examples**: 72→90% accuracy on complex parameter handling internally.
- **Prior art cited**: Joel Pobar's LLMVM, Cloudflare's Code Mode, Anthropic's earlier "Code Execution as MCP" post — all cross-vendor instances of the same code-as-tool-orchestration pattern that PTC formalizes.

## Connections

- Updates: [[ACI - Agent-Computer Interface]] · [[Just-in-Time Context Retrieval]] · [[Context Engineering]] · [[MCP]] · [[Token Economics]]
- New concepts: [[Tool Search Tool]] · [[Programmatic Tool Calling]] · [[Tool Use Examples]]
- Tension: [[Logit Masking]] / [[KV-Cache Discipline]] (Manus's static-action-space argument)
- Synthesis thesis: [[Static Action Spaces vs Dynamic Tool Discovery]]
- Authors: Bin Wu (primary). Contributors: Adam Jones, Artur Renault, Henry Tay, Jake Noble, Noah Picard, Sam Jiang. Foundational research: Chris Gorgolewski, Daniel Jiang, Jeremy Fox, Mike Lambert.
- Flagship internal user: Claude for Excel (PTC on spreadsheets with thousands of rows)

## Open questions

- Does Tool Search Tool's "deferred tools excluded from initial prompt" claim hold under all SDK paths, or only for specific tool patterns? Spec-level detail not in post.
- How does PTC interact with [[Logit Masking]] — could Manus-style decode-time constraint coexist with Anthropic-style code-orchestration? Likely orthogonal but unverified.
- The 49→74% MCP-eval gain on Opus 4 is huge. What's the eval? Is the 25-point delta due to (a) better tool selection, (b) less context noise, or (c) both? Post doesn't decompose.
- Per-server `defer_loading` for MCP — does this play well with MCP marketplaces where servers come and go? Spec-level question.
- What's the cost story? PTC requires the Code Execution tool, which is itself billed. Net cost of PTC vs direct tool calling not disclosed.
- Long-tail: where does this push MCP's design? If servers expect to be auto-deferred, server authors might design fewer-but-fatter tools.

## Sources

- self (this source page)
