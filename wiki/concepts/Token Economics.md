---
type: concept
title: Token Economics
created: 2026-05-04
updated: 2026-05-13
tags:
- ai-agents
- economics
- decision-framework
status: developing
related: []
sources:
- "[[2025-06-13 - Anthropic - How we built our multi-agent research system]]"
- "[[2025-09-29 - Anthropic - Effective context engineering for AI agents]]"
- "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
- "[[2025-11-24 - Anthropic - Advanced Tool Use]]"
- "[[2025-10 - Zhang Khattab - Recursive Language Models]]"
- "[[2026-05-13 - Anthropic - Code Execution with MCP]]"
_legacy_source_count: 5
---

# Token Economics

## Summary

The operational test for whether agentic complexity is justified. Per [[How we built our multi-agent research system]] (Anthropic 2025-06): **agents use ~4× chat tokens; multi-agent systems use ~15× chat tokens**. Use these multipliers to decide whether task value clears the cost.

## Core finding

> "Token usage by itself explains 80% of the variance, with the number of tool calls and the model choice as the two other explanatory factors."

Combined: token count + tool-call count + model choice → ~95% of performance variance on BrowseComp.

**Implication:** multi-agent systems aren't smarter; they're a parallelism harness. They win by spending more tokens in parallel that a single agent couldn't deploy serially.

## Decision framework

A pattern justifies its cost when expected value clears the multiplier:

| Pattern | Token multiplier vs chat | Justifying conditions |
|---|---|---|
| Single chat call | 1× | default |
| Augmented LLM (single call) | 1× | always |
| Workflow patterns | ~1–2× | chain length warranted |
| Single autonomous agent | ~4× | task open-ended, value > 4× threshold |
| Multi-agent system | ~15× | + parallelizable + context overflow |

## Practical heuristic

If you can't articulate why your task is worth 4× (let alone 15×) the cost of a single chat call, you should be using a workflow.

## The other side: tokens as architectural quality (per Anthropic 2025-09)

[[Effective context engineering for AI agents]] elevates token cost from a billing concern to an **architectural quality concern**. Beyond dollars, every token consumes the model's **attention budget** — and recall degrades non-linearly as context grows ("context rot"). See [[Context Engineering]].

Two cost dimensions, not one:

| Dimension | What you pay | Failure mode |
|---|---|---|
| Dollar cost | API spend (4× / 15× chat) | Uneconomic |
| Attention cost | Recall degradation under `n²` attention | Unreliable |

Even if model prices collapse, the attention cost remains. The 4× / 15× framing is the *floor* on cost, not the ceiling — context-engineering discipline keeps the attention cost from dominating.

## Third axis: KV-cache hit rate (per Manus 2025-07)

[[2025-07-18 - Manus - Context Engineering for AI Agents]] surfaces a **third cost dimension** the Anthropic posts don't fully name: **prefill cost gated by KV-cache hit rate**. With Claude Sonnet's published prices, cached input is $0.30 / MTok while uncached is $3 / MTok — a **10× gap**. Manus reports a 100:1 input-to-output ratio in production, so prefill dominates total cost.

Three cost dimensions, not two:

| Dimension | What you pay | Failure mode | Primary lever |
|---|---|---|---|
| Dollar cost (pattern) | 4× / 15× chat multipliers | Uneconomic | Workflow vs agent vs multi-agent choice |
| Attention cost | Recall degradation under `n²` attention | Unreliable | Context discipline ([[Context Engineering]]) |
| **KV-cache cost** | **10× cached/uncached prefill gap** | **Unscalable in production** | **Prefix stability + append-only context** |

See [[KV-Cache Discipline]] for the three-rule operationalization. For agents with prefill-dominated workloads (most of them — long contexts, short function-call outputs), **the KV-cache axis can dominate the other two combined.** A 4× multi-agent system that hits cache cleanly may be cheaper in production than a 1× single agent that thrashes the cache.

Cache hit rate also constrains architectural choices in non-obvious ways: any compaction or context-cleanup pass forces a cache miss; dynamic tool loading risks invalidating the cached prefix; observation diversity (for [[Few-Shot Drift]]) must be injected after the cacheable region. Cache-friendliness becomes a design constraint, not an optimization.

## Concrete reduction numbers (per Anthropic 2025-11)

[[2025-11-24 - Anthropic - Advanced Tool Use]] publishes the first detailed deltas on context-pollution remedies:

| Remedy | Reduction | Measured on |
|---|---|---|
| [[Tool Search Tool]] (tool-def deferral) | -85% tool-def overhead (134K → 8.7K tokens) | Internal worst-case MCP setup |
| [[Programmatic Tool Calling]] (code-orchestrated tools) | -37% total tokens (43.6K → 27.3K) | Complex research tasks |
| Extreme PTC case | ~200× | Budget-compliance over 2,000 expense items (~200KB → ~1KB) |

These let the dollar-cost axis be contained at multiple layers — discovery (Tool Search), execution (PTC), authoring (Tool Use Examples). Important: these are reductions in **prompt input tokens** (which dominate prefill cost), so they compound with [[KV-Cache Discipline]] — fewer tokens to cache, more of what remains stays cacheable, fewer cache misses on each iteration.

## Smaller-model-in-scaffold beats larger-model-alone (per Zhang & Khattab 2025-10)

[[2025-10 - Zhang Khattab - Recursive Language Models]] surfaces the first empirical case in the wiki where **a smaller model wrapped in a recursive scaffold outperforms a larger model alone on long-context tasks at comparable or lower cost.**

| Benchmark | Configuration | Cost vs GPT-5 | Performance vs GPT-5 |
|---|---|---|---|
| OOLONG 132k | RLM(GPT-5-mini) | ~equivalent | **+114%↑** (more than double correct answers) |
| OOLONG 263k | RLM(GPT-5-mini) | cheaper on average | **+49%↑** |
| BrowseComp-Plus, 1000 docs | RLM(GPT-5) | scales reasonably | holds ~100% vs all baselines degrading |

The decision-framework implication: **on long-context workloads, model-size is no longer the dominant lever**. Scaffolding choice (RLM vs flat call) is. This breaks the prior intuition that "smarter model wins if you can afford it" — for the workloads where context-rot is the binding constraint, a smaller model in a recursive scaffold dominates a flat call to the frontier.

Caveats: small sample sizes (20 queries on BrowseComp-Plus, ~100 on OOLONG slice); preliminary results; non-extractive tasks not yet evaluated.

This connects to [[Workflows Beat Agents for Most Production]] indirectly — RLM is a workflow-shaped *substrate* (Python REPL with bounded actions) hosting an LM-orchestrated step. The win comes from the substrate constraint, not from "agentness" per se.

## MCP layer extension (per Anthropic 2026-05-13)

[[2026-05-13 - Anthropic - Code Execution with MCP]] confirms the same 30-40% token reduction mechanism from [[Programmatic Tool Calling]] applies when code execution is embedded inside MCP server tools. The efficiency lever is identical — local data reduction before returning to context — but now available to any MCP-compatible client, not just Claude API users.

Composability note: pairing code execution MCP tools (result reduction) with [[Tool Search Tool]] deferred loading (definition reduction) gives two stacked efficiency layers. For large MCP setups, the combined reduction could be dramatic:
- Tool Search: -85-95% on tool definition overhead
- Code execution: -30-40% on result token overhead
- Combined: significant headroom for scaling tool count without proportional context growth

## Connections

- Operational test for: [[Workflows vs Agents]] · [[Workflows Beat Agents for Most Production]]
- Why [[Multi-Agent Systems]] win in narrow conditions
- Constraint on: [[Autonomous Agents]] adoption
- Inputs: model choice and tool-call count (~15% of variance combined)
- Architectural quality dim: [[Context Engineering]]
- Third axis: [[KV-Cache Discipline]] (production prefill economics)
- Reduction levers: [[Tool Search Tool]] · [[Programmatic Tool Calling]] · [[Tool Use Examples]] · [[Recursive Language Models]] (smaller-model-in-scaffold)
- Practical containment: [[Just-in-Time Context Retrieval]] · [[Long-Horizon Context Management]]

## Open questions

- How do these multipliers shift as model costs drop year-over-year (e.g., as Sonnet pricing approaches Haiku)?
- Is there a similar variance-decomposition for non-research tasks (coding, customer support, data analysis)?
- Does parallelism-via-bigger-context (1M+ context windows) compete with parallelism-via-multi-agent on the same cost curve?
- Quantitative recall-degradation curves per model — when does attention cost dominate dollar cost?

## Sources

- [[How we built our multi-agent research system]] (Anthropic, 2025-06-13)
- [[Effective context engineering for AI agents]] (Anthropic, 2025-09-29)
- [[2025-07-18 - Manus - Context Engineering for AI Agents]] (Manus, 2025-07-18)
- [[2025-11-24 - Anthropic - Advanced Tool Use]] (Anthropic, 2025-11-24)
- [[2025-10 - Zhang Khattab - Recursive Language Models]] (Zhang & Khattab, 2025-10)
- [[2026-05-13 - Anthropic - Code Execution with MCP]] (Anthropic, 2026-05-13)
