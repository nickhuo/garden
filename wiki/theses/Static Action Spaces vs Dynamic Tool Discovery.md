---
type: thesis
title: Static Action Spaces vs Dynamic Tool Discovery
created: 2026-05-10
updated: 2026-05-10
tags:
- ai-agents
- thesis
- action-space
- tool-design
status: developing
related: []
sources:
- "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
- "[[2025-11-24 - Anthropic - Advanced Tool Use]]"
_legacy_source_count: 2
---

# Static Action Spaces vs Dynamic Tool Discovery

## Claim (the live question)

Two production agent-design schools have arrived at **opposite** answers to how an agent's action space should behave at runtime:

- **Static / [[Logit Masking]] school (Manus, Jul 2025):** Define the full tool inventory upfront. Never add or remove tools mid-iteration. Constrain action selection at decode-time via prefix-grouped names + state-machine-driven logit masking. The optimization target is **KV-cache hit rate** ([[KV-Cache Discipline]]) — and dynamic action spaces necessarily break the cacheable prefix.
- **Dynamic / [[Tool Search Tool]] school (Anthropic, Nov 2025):** Defer most tool definitions out of the initial prompt. Surface them on-demand via search. The optimization target is **scalable tool libraries** — and static action spaces don't fit when you have hundreds or thousands of MCP-exposed tools.

This is the most consequential cross-vendor disagreement in the wiki so far. Neither side is wrong on their own terms; they make opposite bets about which production constraint dominates.

## Why this thesis exists

The disagreement is **explicit and directional** in the source record:

- Manus ([[2025-07-18 - Manus - Context Engineering for AI Agents]]) gives two specific reasons to avoid dynamic action spaces: (a) tool defs sit at the front of context, so any change invalidates KV-cache from that point forward; (b) prior actions/observations may reference tools no longer defined, causing hallucinations.
- Anthropic ([[2025-11-24 - Anthropic - Advanced Tool Use]]) — four months later — addresses **both objections by name**:
  - (a) "Tool Search Tool doesn't break prompt caching because deferred tools are excluded from the initial prompt entirely. They're only added to context after Claude searches for them, so your system prompt and core tool definitions remain cacheable."
  - (b) Tools are *added* by search, never removed mid-trajectory — so no dangling references.

Read in sequence, Anthropic's release is partially a response to the Manus critique. The architectural disagreement turns on **whether the dynamism happens before or after the cacheable region**, and **whether the operation is addition-only or churn**.

## The decision axes

| Axis | Static / Masking favored | Dynamic / Discovery favored |
|---|---|---|
| Action space size | Bounded (~10-100 tools) | Unbounded / unknown (MCP marketplaces, 100s-1000s) |
| Tool author trust | High (you curate) | Low (user-installable, third-party) |
| Inference stack control | Self-hosted or logits-bias supported | Hosted API only |
| Avg input:output ratio | Very high (~100:1 — prefill dominates) | Mixed |
| Cache infrastructure | Self-managed (vLLM, custom) | Vendor-managed with cache-safe deferral primitives |
| Workload pattern | Repetitive same-task agent (e.g., support assistant) | Discovery-oriented agent (e.g., research, IDE) |
| Tool selection difficulty | Low (similar tools easily disambiguated) | High (similar-named tools across servers) |

A useful test: **does the agent's typical loop benefit more from a stable cacheable prefix, or from a small action choice surface at each step?** The former argues static; the latter argues dynamic.

## Strongest evidence so far

For static (Manus):
- 10× cost gap on Claude Sonnet between cached and uncached input ($0.30 vs $3 / MTok)
- 100:1 input:output ratio in Manus's production loop — prefill cost dominates totals
- The two failure modes (cache invalidation + dangling refs) are real; Manus reports rebuilding their framework 4× through them
- Mature: empirically discovered across millions of users

For dynamic (Anthropic):
- 85% reduction in tool-def overhead (134K → 8.7K tokens) — savings dwarf the cache-miss cost
- Opus 4 MCP eval accuracy jumps 49→74% (+25 points); Opus 4.5 79.5→88.1%
- Cache-safe deferral architecturally solves Manus's objection (a)
- Addition-only architecturally solves Manus's objection (b)
- Mature: built for MCP-scale toolboxes Manus's design can't reach

## The likely synthesis

These designs are not strictly incompatible. A plausible architecture combines them:

1. **Static core action space** — a curated 10-50 tool set the agent uses 95% of the time. Cacheable prefix, masking applies, prefix-grouped names enable decode-time constraint.
2. **Deferred discovery tier** — long-tail / user-installable / domain-specific tools sit behind a Tool Search call. Loaded into context only after a search hits, appended *after* the cacheable region.
3. **Decode-time masking within the dynamic tier too** — once a discovery search has surfaced N candidates, masking can constrain selection to just those candidates without further dynamism.

Neither published source endorses this hybrid yet. It would falsify the binary framing of the thesis, but the wiki should track it as the most likely 2027 production design.

## What would falsify this thesis

- A second non-Anthropic vendor publishing a Manus-style static + masking position as production wisdom — would strengthen the static side and turn this from "open question" into "Anthropic outlier."
- Production data from a Tool-Search-enabled agent showing that KV-cache hit rate stays high in practice despite frequent search calls — would weaken Manus's strongest objection.
- An open-source benchmark covering both action-space sizes (small bounded + large unbounded) where one design dominates — would let the field decide rather than guess.
- A new model-side capability (much better tool-selection from large lists without explicit search; or much better cache behavior under dynamic prefixes) that eliminates one of the constraints driving the disagreement.

## Counterclaims still to track

- **The "tools are obsolete" camp** — if [[Programmatic Tool Calling]] eats the orchestration layer entirely, the action-space-design question moves from "which tool to call" to "what code to write," and the static/dynamic distinction becomes orthogonal. Worth a future thesis if PTC reshapes production patterns.
- **MCP-design feedback camp** — if MCP authors design fewer-but-fatter tools in response to Tool Search becoming the default, the action-space-size problem may shrink, making Manus-style static designs more viable at scale.
- **Long-context-makes-discovery-cheap camp** — if 1M+ context windows make 100K tool-def overhead acceptable (no discovery needed), the question dissolves on cost rather than design.

## Nick's stance

_Position: open. Both designs are internally consistent; neither has dominated production yet._

The Manus side has the cleaner production-economics argument (KV-cache cost is real, measurable, dominates prefill-heavy workloads). The Anthropic side has the cleaner scale argument (MCP-style ecosystems make static curation impossible past a certain size).

**Operational impact for Nick's career thread:** if Nick is building agent infrastructure on top of hosted APIs (Claude Developer Platform, OpenAI Responses), the dynamic-discovery design is the path of least resistance because vendors will provide cache-safe deferral primitives. If Nick is building self-hosted or open-weights infrastructure, the static + masking design dominates because vendors don't provide cache-safety guarantees and Nick can implement his own logits processors. **Choose the design that matches your inference stack, not your preferences.**

For [[Workflows Beat Agents for Most Production]]: this thesis doesn't directly load on the workflow/agent question, but **does** load on which agent design is the production default once you've decided agents are the right shape. The static + masking design lowers the bar for "agent in production" by attacking the strongest objection (cost unpredictability). The dynamic + discovery design raises the ceiling by making large tool ecosystems viable. Both serve the same workflow-beats-agent thesis at different layers.

## Connections

- Foundational contradiction: [[Logit Masking]] vs [[Tool Search Tool]]
- Cost dimension: [[KV-Cache Discipline]] (Manus's strongest argument)
- Scale dimension: [[Tool Search Tool]] (Anthropic's strongest argument)
- ACI implications: [[ACI - Agent-Computer Interface]] (prefix-grouped names enable static; clear-name+description enable dynamic discovery)
- Cache-budget context: [[Token Economics]]
- Adjacent (orthogonal): [[Programmatic Tool Calling]] — moves orchestration into code, partially sidesteps the discovery/masking question
- Sources: [[2025-07-18 - Manus - Context Engineering for AI Agents]] · [[2025-11-24 - Anthropic - Advanced Tool Use]]

## Sources

- [[2025-07-18 - Manus - Context Engineering for AI Agents]] (Manus, 2025-07-18)
- [[2025-11-24 - Anthropic - Advanced Tool Use]] (Anthropic, 2025-11-24)
