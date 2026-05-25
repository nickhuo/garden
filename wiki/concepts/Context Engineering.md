---
type: concept
title: Context Engineering
created: 2026-05-04
updated: 2026-05-10
tags:
- ai-agents
- context
- foundations
status: developing
related: []
sources:
- "[[2025-09-29 - Anthropic - Effective context engineering for AI agents]]"
- "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
- "[[2025-11-24 - Anthropic - Advanced Tool Use]]"
_legacy_source_count: 3
---

# Context Engineering

## Summary

Per [[Effective context engineering for AI agents]] (Anthropic 2025-09): **the discipline of curating and maintaining the optimal set of tokens during LLM inference** — covering system prompts, tools, retrieved data, message history, and scratchpads. A superset of prompt engineering. The natural progression once you move from one-shot generation to multi-turn agents.

Independently validated by [[2025-07-18 - Manus - Context Engineering for AI Agents]] (Manus, 2025-07) — the **first non-Anthropic source** in this wiki, drawn from production experience with millions of users across four full agent-framework rewrites. Manus uses the same term ("context engineering") and arrives at structurally similar conclusions through a separate path, which raises confidence that this is a genuine cross-vendor discipline rather than an Anthropic-internal framing.

## Definition

> "Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference, including all the other information that may land there outside of the prompts."

## Mental model: attention as a finite budget

LLMs have an "attention budget" — token capacity that degrades with overuse:

- Transformer attention is `O(n²)` — pairwise across all tokens
- Training distribution skews toward shorter sequences — long-context performance is brittle
- Recall degrades as context grows ("context rot," per Chroma research)

> "Context must be treated as a finite resource with diminishing marginal returns. Like humans, who have limited working memory capacity, LLMs have an 'attention budget' that they draw on when parsing large volumes of context."

## Operating principle

> "Find the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."

Every token must justify its presence. This applies symmetrically to system prompt, tool docs, examples, and retrieved data.

## Anatomy of context (Anthropic's component breakdown)

| Component | Engineering rule |
|---|---|
| System prompt | Goldilocks zone — neither hardcoded logic nor vague aspiration |
| Tools | Token-efficient schemas, minimally overlapping (no two tools doing similar things) |
| Few-shot examples | Diverse + canonical, not exhaustive |
| Message history | Aggressively pruned; older turns are noise |
| Retrieved data | Just-in-time, not pre-loaded — see [[Just-in-Time Context Retrieval]] |
| Scratchpad / notes | External memory, not in-context — see [[Long-Horizon Context Management]] |

## Why it matters

Context engineering is upstream of every other agent-quality lever. A perfectly-prompted agent with a 100K-token context dump performs worse than a sparsely-prompted agent with carefully-curated context. The "more context = better" intuition is wrong.

## Cross-vendor validation: the Manus six lessons (2025-07)

[[2025-07-18 - Manus - Context Engineering for AI Agents]] adds six production-derived discipline rules that extend the Anthropic framing. Each is now its own page; together they constitute the operational ruleset for production agents:

1. **[[KV-Cache Discipline]]** — KV-cache hit rate is the single most important production metric. Stable prefix, append-only context, deterministic serialization. ~10× cost gap on Claude Sonnet between cached and uncached input.
2. **[[Logit Masking]]** — constrain action space at decode-time via state-machine + prefix-grouped action names, instead of dynamically adding/removing tools (which breaks KV-cache and creates dangling references). **This directly contradicts [[Tool Search Tool]]** — see [[Static Action Spaces vs Dynamic Tool Discovery]].
3. **File system as context** (extends [[Long-Horizon Context Management]]) — unlimited externalized memory; compression must be **restorable** (drop bytes, keep URL/path).
4. **[[Recitation]]** — rewrite goals at the end of context every step (`todo.md` pattern) to bias attention toward the objective. Counters lost-in-the-middle.
5. **[[Error Trace Retention]]** — leave failure traces in context; the model uses them to update its prior. Error recovery is the strongest indicator of true agentic behavior.
6. **[[Few-Shot Drift]]** — agent contexts self-poison via pattern-mimicry on repetitive batched work. Inject controlled diversity in observations (not in the cacheable prefix).

Cross-cutting observation: Manus and Anthropic agree on the **what** (context discipline as the moat) but diverge on the **how** at the action-space layer. Manus optimizes for static action space + masking; Anthropic optimizes for dynamic discovery + cacheable deferral. The disagreement is the most interesting cross-vendor data point in this wiki.

## Three orthogonal context-pollution remedies (per Anthropic 2025-11)

[[2025-11-24 - Anthropic - Advanced Tool Use]] introduces three features that attack distinct context-pollution failure modes — they layer cleanly without overlap:

| Bottleneck | Remedy | Page |
|---|---|---|
| Tool defs flood the prompt (>10K tokens of toolbox before any work) | Defer-and-search the tool list | [[Tool Search Tool]] |
| Intermediate tool results flood context (logs, datasets, query results) | Orchestrate via code; only final reduction enters context | [[Programmatic Tool Calling]] |
| Schema-valid but semantically-wrong tool calls (date formats, ID conventions, parameter correlations) | Inline `input_examples` on tool defs | [[Tool Use Examples]] |

The three sit at different points in the context lifecycle: discovery (Tool Search), execution (PTC), and authoring (Examples). A production agent designs all three concurrently rather than treating them as alternatives.

## Operationalized as a coding method (per Huntley 2026-01)

[[2026-01-17 - Geoffrey Huntley - Everything is a Ralph Loop]] turns context engineering into a named practitioner recipe: the [[Ralph Loop]]. Huntley's claim — "ralph is about getting the most out of how the underlying models work through context engineering" — frames a monolithic single-process coding agent as *primarily* a context-engineering exercise (goal recitation + backing specs + accumulated failure-fixes per loop), explicitly *against* multi-agent orchestration. A grassroots, benchmark-free counterpart to the Anthropic/Manus framing above.

## Connections

- Subsumes: prompt engineering (no separate page; handled here)
- Operationalized by: [[Just-in-Time Context Retrieval]] · [[Long-Horizon Context Management]] · [[KV-Cache Discipline]]
- Production discipline rules: [[KV-Cache Discipline]] · [[Logit Masking]] · [[Recitation]] · [[Error Trace Retention]] · [[Few-Shot Drift]]
- Context-pollution remedies: [[Tool Search Tool]] · [[Programmatic Tool Calling]] · [[Tool Use Examples]]
- Strengthens: [[ACI - Agent-Computer Interface]] (tool docs ARE context, not metadata)
- Architectural-quality version of: [[Token Economics]] (cost → recall + reliability, not just $)
- Foundational to: [[Augmented LLM]] · [[Autonomous Agents]] · [[Multi-Agent Systems]]
- Definition of agent borrowed from Simon Willison: "LLMs autonomously using tools in a loop"

## Open questions

- Quantitative thresholds — at what token count does recall drop measurably for Claude Sonnet / Opus / Haiku? Anthropic gestures at it but the answer is model-specific and likely shifting.
- Is there a context engineering "anti-pattern catalog" — common mistakes with measurable costs? Not yet.
- How does context engineering interact with fine-tuning? Tuning shifts what the model "knows" so the context can shrink — but the trade-off curve isn't documented.

## Sources

- [[Effective context engineering for AI agents]] (Anthropic, 2025-09-29)
- [[2025-07-18 - Manus - Context Engineering for AI Agents]] (Manus, 2025-07-18)
- [[2025-11-24 - Anthropic - Advanced Tool Use]] (Anthropic, 2025-11-24)
