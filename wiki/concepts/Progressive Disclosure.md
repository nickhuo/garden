---
type: concept
title: Progressive Disclosure
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - context-engineering
  - tool-design
status: developing
complexity: intermediate
domain: ai-agents
aliases:
  - manifest-first loading
  - deferred capability loading
  - lazy skill loading
related:
  - "[[Tool Search Tool]]"
  - "[[Agent Skills]]"
  - "[[KV-Cache Discipline]]"
  - "[[Token Economics]]"
  - "[[Context Engineering]]"
  - "[[MCP]]"
sources:
  - "[[2026-05-13 - Anthropic - Agent Skills]]"
---

# Progressive Disclosure

A context-management pattern in which an agent's capabilities are loaded into context **on demand** rather than all at once. The agent always sees a lightweight **manifest** (short description + discovery mechanism); the full capability definition loads only when the agent determines it needs that capability.

## The pattern

```
Agent context at all times:
  [System prompt]
  [Skill A manifest: "I can browse the web. Call discover_web to load tools."]
  [Skill B manifest: "I can read/write files. Call discover_files to load tools."]
  [Skill C manifest: "I can query the calendar. Call discover_calendar to load tools."]

Agent invokes discover_web → full web browsing tool definitions load into context.
Agent now has:
  [System prompt]
  [Skill A: full 8-tool web browser tool set + prompt fragment]
  [Skill B manifest]  ← still deferred
  [Skill C manifest]  ← still deferred
```

The undiscovered skills remain as short manifests. Only the skill(s) actively in use carry their full weight.

## Why it matters

| Without progressive disclosure | With progressive disclosure |
|---|---|
| Context cost: O(all tools, always) | Context cost: O(manifests) + on-demand |
| KV-cache hit rate: low (any tool edit breaks cache) | KV-cache hit rate: high (manifest prefix is stable) |
| Wrong-tool-selection risk: high (model sees many similar tools always) | Wrong-tool-selection risk: lower (active set is smaller) |

These savings compound: an agent with 5 skills × 8 tools each = 40 tool definitions under naive loading. Under progressive disclosure: 5 short manifests at all times, plus 8 full tools for whichever skill is active.

## Levels of granularity

Progressive disclosure appears at multiple levels in Anthropic's architecture:

| Level | Mechanism | Deferral unit |
|---|---|---|
| Individual tool | [[Tool Search Tool]] `defer_loading: true` | Single tool within a server |
| MCP server | [[Tool Search Tool]] `mcp_toolset` config | Full server's tool set |
| Skill bundle | [[Agent Skills]] manifest-first pattern | Bundle of tools + prompt fragment |

The levels are composable: a skill can defer its internal MCP server(s) using Tool Search Tool's per-server defer_loading.

## KV-cache interaction

Because the manifest prefix doesn't change across requests, it can sit in the warm KV-cache. The full tool definitions, loaded on demand, will also cache after first use in a session. This is structurally the same insight as [[KV-Cache Discipline]]: stable prefixes = cache hits = 10× cost savings on Anthropic Sonnet.

## UX for the agent

Progressive disclosure requires the agent to take an extra action (invoke the discovery tool) before using a skill's capabilities. This is an intentional trade-off:
- **Cost**: one extra tool call per skill activation per session
- **Benefit**: dramatically reduced baseline context, improved cache stability, lower wrong-tool-selection rate

For long-running or multi-turn agents where the same skill is used repeatedly, the activation cost amortizes quickly.

## Relationship to [[Tool Search Tool]]

[[Tool Search Tool]] is the fine-grained version of this pattern (single tool or MCP server level). [[Agent Skills]] is the coarse-grained version (skill bundle level). Both apply the same principle: **register presence cheaply, load fully on demand**.

## Connections

- [[Agent Skills]] — the packaging layer where progressive disclosure operates at bundle level
- [[Tool Search Tool]] — sibling mechanism at single-tool/server level
- [[KV-Cache Discipline]] — stable manifest prefix = preserved cache hit rate
- [[Token Economics]] — progressive disclosure directly reduces context-cost pressure
- [[Context Engineering]] — progressive disclosure is a structured discipline within context engineering
- [[ACI - Agent-Computer Interface]] — manifest design is an ACI design problem: how to communicate "I exist and can do X" in minimal tokens

## Sources

- [[2026-05-13 - Anthropic - Agent Skills]]
