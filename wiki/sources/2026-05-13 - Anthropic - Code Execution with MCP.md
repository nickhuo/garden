---
type: source
title: "Code execution with MCP: Building more efficient agents"
aliases:
  - "Code Execution with MCP"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - mcp
  - tool-use
  - code-execution
  - context-engineering
status: developing
related:
  - "[[Programmatic Tool Calling]]"
  - "[[MCP]]"
  - "[[Tool Search Tool]]"
  - "[[Token Economics]]"
  - "[[ACI - Agent-Computer Interface]]"
sources:
  - "[[.raw/articles/2026-05-13 - Anthropic - Code Execution with MCP.md]]"
source_type: article
author: Anthropic Engineering
date_published: 2026-05-13
url: https://www.anthropic.com/engineering/code-execution-with-mcp
confidence: high
key_claims:
  - "Code execution can be exposed as an MCP tool, letting agents reduce large datasets locally before returning results to context"
  - "MCP servers should be compute-capable endpoints, not just data proxies"
  - "Combining code execution with Tool Search (deferred loading) gives both context efficiency layers simultaneously"
  - "Code inside MCP sandbox can parallelize calls to multiple data sources, collapsing N inference steps to 1"
  - "Structured error returns from sandboxed code are essential for agent reliability"
---

# Code execution with MCP: Building more efficient agents

**Source:** Anthropic Engineering | **URL:** https://www.anthropic.com/engineering/code-execution-with-mcp | **Date:** 2026-05-13

## What this is

A practical engineering post extending Anthropic's [[Programmatic Tool Calling]] pattern into the [[MCP]] ecosystem. Where the [[2025-11-24 - Anthropic - Advanced Tool Use]] post introduced PTC as a Claude API pattern (model writes code → sandbox executes → only final result enters context), this post shows MCP server authors how to embed the same capability inside their servers. The audience shifts from agent developers to MCP server developers.

## Core argument

Traditional MCP tools are data proxies: they fetch data from a backend and return it to the model. This creates the classic context-pollution problem at scale — fetching 2,000 expense rows to answer "who exceeded budget?" floods the model's context when only 3 names are needed.

The solution: **embed code execution inside the MCP tool**. The MCP server fetches data, runs Python (or equivalent) in a sandbox to process it locally, and returns only the reduced result. The model writes the processing code in the tool's `code` parameter; the MCP server executes it in an isolated runtime and returns stdout.

## Key claims

### 1. Code execution as MCP tool definition

Code execution is exposed as a standard MCP tool with a `code` parameter. The model calls it by writing Python. The MCP server's runtime executes the code and returns `stdout` as the result, `stderr` as the error channel.

Design guidance from the post:
- Keep return format consistent (stdout = result, stderr = errors)
- Document available libraries explicitly in the tool description so the model can write correct imports
- Return structured error strings (not raised exceptions) so agents can handle failures gracefully

### 2. MCP servers as compute endpoints

This reframes MCP server design from "data proxy" to "compute endpoint." A well-designed MCP server bundles:
1. Data-access tools (fetch, query, list)
2. A code execution tool that can call those data-access tools from inside the sandbox

The compute endpoint pattern means the model only needs to write logic once (in the code parameter), not iterate through results across multiple inference turns.

### 3. Composability with Tool Search

Code execution MCP tools can be marked `defer_loading: true` in [[Tool Search Tool]] configs. This gives both efficiency layers simultaneously:
- Tool Search reduces context overhead from tool *definitions* (discovery layer)
- Code execution reduces context overhead from tool *results* (execution layer)

Pairing them: the code execution tool is deferred until the agent identifies a computation-heavy subtask, then loaded and invoked with the code to process locally.

### 4. Parallelism via code

Code running inside the MCP sandbox can issue parallel calls to multiple data sources (`asyncio.gather` pattern), collapsing N sequential inference steps into a single inference + single code-execution cycle. This is the same latency argument as [[Programmatic Tool Calling]] proper — the code can loop, branch, and fan-out in ways that sequential natural-language tool calling cannot.

### 5. Sandbox isolation model

The sandbox is isolated per-session and does not persist state across agent turns unless explicitly written to a store. This differs from long-lived execution environments. Server authors must design for statelessness (or explicit state passing).

## Numbers

- Consistent with [[2025-11-24 - Anthropic - Advanced Tool Use]]: ~30–40% token reduction vs traditional tool-call-per-row on data-processing tasks
- Reliability improvements on multi-step data pipelines (no specific benchmark published in this post)

## Framing relative to prior Anthropic posts

| Post | Audience | Pattern |
|---|---|---|
| [[2025-11-24 - Anthropic - Advanced Tool Use]] | Agent developers | PTC via Claude API (`allowed_callers`) |
| This post | MCP server developers | Code execution embedded inside MCP tool definitions |

The underlying primitive is identical. The packaging differs — this post moves the sandbox from Anthropic's platform into the MCP server layer, making it available to any MCP-compatible client, not just Claude API users.

## Connections

- Extends: [[Programmatic Tool Calling]] into the MCP server layer
- Integrates with: [[MCP]] entity — adds "compute endpoint" design pattern to MCP server authorship guidance
- Composable with: [[Tool Search Tool]] (deferred code execution + deferred tool defs = two efficiency layers)
- Reduces: [[Token Economics]] (same 30-40% reduction mechanism, now via MCP)
- ACI implications: [[ACI - Agent-Computer Interface]] — tool descriptions must now document library availability (a new authoring requirement for MCP servers with code execution)

## Open questions

- Does code execution inside an MCP server have different security properties than Anthropic's platform sandbox? Post describes session isolation but doesn't detail the runtime trust boundary.
- Can MCP servers expose *multiple* code execution runtimes (Python + JS)? Post focuses on Python.
- What happens when a code execution call inside MCP calls another MCP tool that itself embeds code execution? Recursion/reentrancy not addressed.
- Is the 30-40% token reduction additive with Tool Search's 85-95% tool-def reduction? If so, the combined efficiency is dramatic for large MCP setups.
