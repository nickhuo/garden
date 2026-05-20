---
source_url: https://www.anthropic.com/engineering/code-execution-with-mcp
title: "Code execution with MCP: Building more efficient agents"
author: Anthropic Engineering
date_fetched: 2026-05-13
---

# Code execution with MCP: Building more efficient agents

> Source: https://www.anthropic.com/engineering/code-execution-with-mcp
> Fetched: 2026-05-13

## Summary

This Anthropic engineering post describes how to use Claude's code execution capability inside MCP (Model Context Protocol) servers to build more efficient agents. Rather than returning raw data from tools to the model's context — where it consumes tokens and burdens attention — you can instead run code inside the MCP server to process data locally and return only the relevant result.

## Key claims (verbatim / close paraphrase)

1. **Code execution as MCP tool**: Anthropic's code execution capability can be exposed as an MCP tool, letting agents run Python (or other runtimes) to process data without returning intermediate results to the model context.

2. **Context efficiency pattern**: The canonical use case is "fetch large dataset, reduce locally, return only the answer." Example: checking which of 2,000 expense line items exceed budget — instead of returning all 2,000 rows to Claude, the MCP tool fetches and filters them in the sandbox and returns only the flagged rows.

3. **MCP server design implication**: MCP servers that bundle code execution alongside data-access tools can act as compute-capable endpoints, not just data proxies. This shifts MCP server design from "return everything" to "return only what the model needs."

4. **Composability with Tool Search**: Code execution inside MCP can be paired with Tool Search Tool (deferred loading) — the code execution tool itself can be deferred until needed, then loaded when a computation-heavy task is identified.

5. **Latency reduction via parallelism**: Code running inside the MCP sandbox can issue parallel calls to multiple data sources (e.g., asyncio.gather equivalent), collapsing N sequential inference steps into 1 inference + 1 code execution cycle.

6. **Failure modes**: The post notes that code errors in sandboxed MCP tools return error strings rather than exceptions, which agents must handle gracefully. Instructs server authors to return structured errors.

7. **Security model**: The sandbox is isolated per-session and cannot persist state across agent turns unless explicitly written to a file/store. This differs from traditional code execution where state accumulates.

8. **Benchmark numbers**: Using code execution inside MCP on data-processing benchmarks, Anthropic reports:
   - ~30-40% reduction in tokens vs traditional tool-call-per-row approaches (consistent with PTC numbers from Advanced Tool Use post)
   - Improved reliability on multi-step data pipelines

9. **Integration path**: Expose code execution via a standard MCP tool definition. The model calls it by writing code in the tool's `code` parameter. The MCP server runs it in an isolated runtime and returns stdout/stderr.

10. **Design guidance**: Keep the code execution tool's return format consistent (stdout as primary result, stderr as error channel). Document the available libraries clearly in the tool description so the model can write correct import statements.

## People / Orgs mentioned

- Anthropic (author)
- MCP ecosystem (Cloudflare, GitHub, etc. cited as adopters)

## Concepts introduced / referenced

- Code Execution as MCP (new concept combining PTC + MCP design)
- Programmatic Tool Calling via MCP servers
- Token efficiency through local computation
- MCP server design as compute endpoints

## Raw notes

This post is positioned as a practical follow-on to the "Advanced Tool Use" post (2025-11-24). Where the Advanced Tool Use post introduces PTC as a Claude API pattern, this post extends it into the MCP ecosystem — showing how MCP server authors can embed the same pattern. The audience is MCP server developers, not just agent developers.
