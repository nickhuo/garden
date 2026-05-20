---
type: concept
title: Tool Search Tool
created: 2026-05-10
updated: 2026-05-13
tags:
- ai-agents
- tool-design
- context
- mcp
- anthropic
status: developing
related: []
sources:
- "[[2025-11-24 - Anthropic - Advanced Tool Use]]"
- "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
- "[[2026-05-13 - Anthropic - Agent Skills]]"
- "[[2026-05-13 - Anthropic - Code Execution with MCP]]"
aliases:
- Dynamic Tool Discovery
- Tool Search
- defer_loading
_legacy_source_count: 1
---

# Tool Search Tool

## Summary

Anthropic's Claude Developer Platform beta feature (released [[2025-11-24 - Anthropic - Advanced Tool Use|Nov 2025]]) that defers tool definitions out of the initial prompt and surfaces them via on-demand search. The pattern is **JIT retrieval applied to tool definitions** — see [[Just-in-Time Context Retrieval]] — solving the specific failure mode where large MCP-server toolboxes consume 50K-100K+ tokens before the agent has done anything.

This is the canonical instance of **dynamic tool discovery** as a pattern. It directly contradicts the Manus [[Logit Masking]] / static-action-space position; the synthesis lives in [[Static Action Spaces vs Dynamic Tool Discovery]].

## The mechanism

Tools are marked with `defer_loading: true` in the tools array. The Tool Search Tool itself (regex or BM25 implementation provided; embedding-based custom search supported) is always present (~500 tokens). When Claude needs a capability:

1. Claude calls the Tool Search Tool with a keyword
2. Search returns references to matching tools
3. Matched tools are expanded into full definitions in Claude's context
4. Claude invokes them normally

For MCP, you can defer entire servers:

```
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-drive",
  "default_config": {"defer_loading": true},
  "configs": {
    "search_files": {"defer_loading": false}
  }
}
```

## The KV-cache claim (load-bearing)

> "Tool Search Tool doesn't break prompt caching because deferred tools are excluded from the initial prompt entirely. They're only added to context after Claude searches for them, so your system prompt and core tool definitions remain cacheable."

This is an **explicit response** to the Manus critique that dynamic action spaces invalidate KV-cache. The architectural trick: deferred tool defs never enter the cacheable prefix. They're appended *after* the initial search call, so the prefix-region cache stays valid for as long as the system prompt and non-deferred tools are unchanged.

> [!warning] Contradicts [[Logit Masking]]
> [[2025-07-18 - Manus - Context Engineering for AI Agents]] (4 months earlier) explicitly argues against dynamic tool loading on KV-cache and dangling-reference grounds. Anthropic's response: cache-safe deferral solves the first, "additions never removals" solves the second. Both designs are coherent — they make opposite bets on whether the action space should be static (Manus) or expansion-only (Anthropic). See [[Static Action Spaces vs Dynamic Tool Discovery]].

## Reported impact

In Anthropic's internal evals:

| Metric | Before | After | Delta |
|---|---|---|---|
| Initial tool-def context overhead (5-server case) | 55K tokens | ~3.5K tokens (search tool + dynamically loaded) | -93% |
| Internal benchmark: tool-def total | 134K tokens | ~8.7K tokens | -95% |
| Opus 4 — MCP eval accuracy | 49% | 74% | +25 pts |
| Opus 4.5 — MCP eval accuracy | 79.5% | 88.1% | +8.6 pts |

The accuracy gain is the more interesting number. Anthropic frames it as "wrong tool selection and incorrect parameters" being the dominant tool-use failure mode, especially with similar names (`notification-send-user` vs `notification-send-channel`). Search-then-load constrains the model's choice surface at decision time, not just at prompt-construction time.

## When this wins

- Tool defs consuming >10K tokens (Anthropic's threshold guidance)
- Tool selection accuracy is the bottleneck
- MCP-powered systems with multiple servers
- 10+ tools available

## When it's not worth it

- Small tool library (<10 tools) — search step is overhead with no benefit
- All tools used frequently — defer/load thrashes
- Tool defs already compact

## Relationship to Agent Skills (2026-05)

[[Agent Skills]] (Anthropic, 2026-05) generalizes the progressive-disclosure pattern to the **skill-bundle level**: instead of deferring a single tool or MCP server, an entire bundle (tools + prompt fragment) defers behind a lightweight manifest. The two mechanisms are composable — a skill can internally use Tool Search Tool's per-server defer_loading. See [[Progressive Disclosure]] for the cross-cutting concept.

## Cross-vendor sibling instances

- **Anthropic Tool Search Tool** (this page) — search-by-keyword over deferred tool list, with cache-safe deferral built into the platform
- Cloudflare Code Mode (cited as inspiration in [[2025-11-24 - Anthropic - Advanced Tool Use]]) — code-as-tool-orchestration with similar dynamism (more relevant to [[Programmatic Tool Calling]])
- Joel Pobar's LLMVM (cited) — adjacent prior art

No first-class cross-vendor "dynamic tool discovery" pattern exists yet outside Anthropic. This page will generalize if/when OpenAI or Google ship analogues.

## Connections

- Instance of: [[Just-in-Time Context Retrieval]] (JIT applied to tool-def layer)
- Operationalizes: [[Context Engineering]] (tool defs ARE context, defer to save attention budget)
- ACI layer: [[ACI - Agent-Computer Interface]] (search-quality depends on tool name + description quality)
- Protocol-aware: [[MCP]] (per-server defer mode)
- Direct tension with: [[Logit Masking]] · [[KV-Cache Discipline]] (Manus's static-action-space argument)
- Synthesis: [[Static Action Spaces vs Dynamic Tool Discovery]]
- Bundle-level generalization: [[Progressive Disclosure]] · [[Agent Skills]]

## Open questions

- The 25-point Opus 4 accuracy jump (49→74%) is enormous. Decomposition into (a) better selection (less distractor noise) vs (b) less context degradation isn't published. Both matter, but the lever they imply is different.
- Cache-safety claim — does it hold under all SDK paths, or only for narrowly-specified configurations? Spec-level question.
- Search-quality dependency — if tool name/description quality is poor (legacy tools, autogenerated MCP), does Tool Search degrade to noise?
- Cost — is the search call itself meaningfully expensive (multiple tokens, additional inference latency)? Post implies trivial, no numbers.
- Long-tail effect on MCP design — if servers expect to be auto-deferred, does this shift server authoring toward fewer-but-fatter tools? Network effect implications.

## Composability with Code Execution MCP (per Anthropic 2026-05-13)

[[2026-05-13 - Anthropic - Code Execution with MCP]] confirms that code execution MCP tools can be marked `defer_loading: true`, meaning Tool Search and code-execution-in-MCP are composable layers:
- Tool Search defers **tool definitions** (discovery overhead)
- Code execution inside MCP reduces **tool results** (execution overhead)

Pairing them gives two stacked efficiency layers — the code execution tool itself stays out of context until needed, then when invoked writes code that locally reduces large datasets before returning results.

## Sources

- [[2025-11-24 - Anthropic - Advanced Tool Use]] (Anthropic, 2025-11-24)
- [[2026-05-13 - Anthropic - Code Execution with MCP]] (Anthropic, 2026-05-13)
