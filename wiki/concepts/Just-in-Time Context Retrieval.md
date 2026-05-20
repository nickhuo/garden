---
type: concept
title: Just-in-Time Context Retrieval
created: 2026-05-04
updated: 2026-05-10
tags:
- ai-agents
- retrieval
- context
status: developing
related: []
sources:
- "[[2025-09-29 - Anthropic - Effective context engineering for AI agents]]"
- "[[2024-09-19 - Anthropic - Contextual Retrieval]]"
- "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
- "[[2025-10 - Zhang Khattab - Recursive Language Models]]"
- "[[2025-11-24 - Anthropic - Advanced Tool Use]]"
- "[[2026-04-08 - Anthropic - Scaling Managed Agents]]"
aliases:
- JIT Context Retrieval
- JIT Retrieval
_legacy_source_count: 5
---

# Just-in-Time Context Retrieval

## Summary

Per [[Effective context engineering for AI agents]]: an architectural shift away from pre-inference embedding-based RAG. Instead of loading all potentially-relevant data into context before generation, the agent holds **lightweight identifiers** (file paths, stored queries, web links) and pulls data into context **at runtime via tools**, only when the model decides it needs it.

## Definition

> "Rather than pre-processing all relevant data up front, agents built with the 'just in time' approach maintain lightweight identifiers (file paths, stored queries, web links, etc.) and use tools to dynamically load data into context at runtime."

The mental model: the agent uses a filesystem the way a developer does — knowing where files live, opening them only when needed.

## Why it beats pre-loaded RAG (for agents)

- **Saves attention budget** — you don't pay for context the agent ends up not using. See [[Context Engineering]].
- **Self-correcting** — if first retrieval was wrong, agent can refine the query and try again, without poisoning earlier context.
- **Composable** — agent can chain retrievals (find → open → search within → cross-reference) in a way that pre-loaded chunks can't.
- **Honest about what's known** — pre-loaded RAG hides retrieval failures; JIT exposes them as visible tool errors the agent can react to.

## When pre-loaded RAG still wins

- Static, well-bounded domains (legal precedents, financial filings) where the corpus is small and lookup latency dominates.
- One-shot tasks where the cost of an extra agent loop exceeds the cost of over-loading context.
- **Hybrid retrieval** — Anthropic recommends this as the pragmatic middle ground: load some upfront context, let the agent fetch more JIT.

> [!note] Corpus-layer complement: [[Contextual Retrieval]]
> When pre-loaded RAG is the right choice (static corpus, one-shot), [[Contextual Retrieval]] (Anthropic, 2024) significantly improves retrieval quality at the embedding layer: prepend AI-generated context blurbs to chunks before embedding, combine with [[BM25 and Hybrid Retrieval]], and optionally [[Reranking]]. This is orthogonal to JIT retrieval — it improves the quality of what gets retrieved, while JIT changes *when* retrieval happens.

## Operational implications

- Tool design becomes upstream of retrieval quality. See [[ACI - Agent-Computer Interface]] — tools that reveal good identifiers (not raw content) enable JIT.
- Memory pattern in [[Augmented LLM]] is the substrate: filesystem-as-memory + JIT retrieval is the same architecture viewed from two sides.
- Long-running agents must combine JIT retrieval with [[Long-Horizon Context Management]] — JIT keeps the active window small; compaction and notes preserve continuity.

## Concrete instance: URL/path preservation as restorable compression (per Manus 2025-07)

[[2025-07-18 - Manus - Context Engineering for AI Agents]] surfaces a tight JIT pattern from production: when context approaches saturation, **drop content but preserve the identifier**. A fetched web page's bytes leave the context, but its URL remains; a document's contents are dropped, but its sandbox path stays. The agent can re-fetch on demand via the same tools, treating its own past observations as JIT-recoverable.

This is JIT retrieval with a temporal twist: the identifier-vs-content split applies not just to *future* retrievals but to *re-retrievals of state already once seen*. Implication: tool design should make identifiers durable and content cheap to re-fetch — see [[ACI - Agent-Computer Interface]].

> [!warning] Adjacent to [[Logit Masking]] / [[Tool Search Tool]] disagreement
> Manus's JIT-style compression is restorable-by-pointer at the **observation** layer. Manus is explicit that at the **tool definition** layer they reject JIT (don't dynamically load/unload tools — see [[Logit Masking]]). Anthropic's [[Tool Search Tool]] applies JIT to tool definitions specifically. Both can be locally correct: tool defs sit in the cache-sensitive prefix (Manus's concern); observations sit in the append-only tail (where restorable-pointer compression is safe). See [[Static Action Spaces vs Dynamic Tool Discovery]].

## Extreme instance: context-as-REPL-variable (per Zhang & Khattab 2025-10)

[[2025-10 - Zhang Khattab - Recursive Language Models]] pushes JIT to its limit: the **lightweight identifier is the existence of an in-memory REPL variable** holding the context; the **content** is whatever slices the root LM chooses to fetch via code (peek/grep/partition). The root LM never sees the full context — it queries it through code, with the option to spawn recursive sub-LM calls over bounded slices.

Where Anthropic's JIT uses file paths or `getEvents()` calls, RLM uses Python code over a variable in scope. The same principle (don't pre-load) implemented with maximum aggressiveness: the LM's context window only ever holds query + small REPL outputs, regardless of the underlying context size. RLM holds ~100% accuracy at 1000 documents in BrowseComp-Plus while pre-query BM25 and ReAct+BM25 degrade — JIT mediated by a code interpreter beats JIT mediated by a retriever.

See [[Recursive Language Models]] for the full pattern.

## Concrete instance: Tool Search Tool — JIT for tool definitions (per Anthropic 2025-11)

[[2025-11-24 - Anthropic - Advanced Tool Use]] applies JIT to a layer the earlier posts didn't address explicitly: **tool definitions themselves**. The [[Tool Search Tool]] keeps deferred tools (`defer_loading: true`) out of the initial prompt; Claude only sees the search tool. When Claude needs a capability, it searches by keyword; matched tool defs expand into context.

This is JIT retrieval where the "identifier" is the tool's name+description (searchable surface) and the "content" is the full schema + docs + examples. The lever is the same as document-level JIT: don't pay for context you might not use.

Two architecture-specific features:

- **Cache-safe deferral** — deferred defs never enter the cacheable prefix; they're appended after the search call, so prefix-region cache stays valid. This is the architectural answer to Manus's KV-cache concern (see [[KV-Cache Discipline]]).
- **Per-MCP-server deferral** — `mcp_toolset` config supports deferring an entire server while keeping select tools eager-loaded. JIT applied to entire toolboxes, with selective opt-out.

Empirical anchor: 134K→8.7K tokens of tool-def overhead in Anthropic's internal eval; Opus 4 MCP eval 49→74%, Opus 4.5 79.5→88.1%.

## Concrete instance: `getEvents()` over event log (per Anthropic 2026-04)

[[Scaling Managed Agents]] gives JIT retrieval a clean infrastructure form: when an agent's context lives as an append-only [[Session as Event Log]], the brain calls `getEvents()` with positional slices, rewinds, or partial reads. This is JIT retrieval where the "lightweight identifier" is an event ID and the "tool" is the runtime API itself.

Implication: under a [[Meta-Harness]], JIT retrieval is no longer a per-agent design decision — it's a runtime primitive.

## Connections

- Operationalizes: [[Context Engineering]]
- Substrate: [[Augmented LLM]] (memory + tools)
- Enabled by: [[ACI - Agent-Computer Interface]]
- Pairs with: [[Long-Horizon Context Management]]
- Runtime instance: [[Session as Event Log]] · [[Meta-Harness]]
- Replaces (in agent contexts): pre-inference embedding RAG

## Open questions

- What's the right granularity for "lightweight identifiers"? File paths work in coding; what's the equivalent for, say, a customer-history workload?
- How do you build retrieval intuitions into the model — train on JIT-shaped tool use, or rely on prompt-time scaffolding?
- Vector DB infrastructure investments — devalued or repurposed under JIT?

## Sources

- [[Effective context engineering for AI agents]] (Anthropic, 2025-09-29)
- [[Scaling Managed Agents]] (Anthropic, 2026-04-08)
- [[2025-07-18 - Manus - Context Engineering for AI Agents]] (Manus, 2025-07-18)
- [[2025-11-24 - Anthropic - Advanced Tool Use]] (Anthropic, 2025-11-24)
- [[2025-10 - Zhang Khattab - Recursive Language Models]] (Zhang & Khattab, 2025-10)
