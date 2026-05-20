---
source_url: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
fetched: 2026-05-13
title: "Equipping agents for the real world with Agent Skills"
author: Anthropic Engineering
---

# Equipping agents for the real world with Agent Skills

> Source: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
> Fetched: 2026-05-13

## Overview

Anthropic Engineering describes the design and motivation behind **Agent Skills** — a packaging primitive that bundles tools, prompts, and context into reusable, composable units that can be attached to Claude agents.

## Core problem

When building real-world agents, the same capabilities (web browsing, code execution, file I/O, calendar access) are reconstructed from scratch for every new agent. This causes:

1. **Context bloat** — every tool definition, its documentation, and its examples are re-specified per-agent, even when the capability is identical across deployments.
2. **Maintenance fragmentation** — improvements to (e.g.) a web-browsing tool have to be manually propagated to every agent that uses it.
3. **Discoverability gap** — there is no standard way for an agent to discover what capabilities are available beyond what was explicitly handed to it at system-prompt time.

## Agent Skills as a solution

An **Agent Skill** is a versioned, self-contained bundle containing:
- A set of **tool definitions** (the function signatures the model can invoke)
- **Prompt fragments** — system-prompt text that primes the model on when and how to use those tools
- Optionally, **resource handles** pointing to external services (MCP servers, APIs, databases)

Skills are attached to agents at instantiation time and can be mixed and matched. The agent's effective capability set is the union of all attached skills.

## Progressive disclosure

The key UX/API design principle in Agent Skills is **progressive disclosure**: skills don't dump all their context into the model's window at once. Instead:

1. Each skill registers a **lightweight manifest** — a short description of what the skill does and a single discovery tool.
2. When the agent determines a skill is relevant, it invokes the discovery tool, which returns the **full tool set** for that skill.
3. The full tool set, including examples, is loaded into context only when actually needed.

This is structurally identical to [[Tool Search Tool]]'s `defer_loading` mechanism but at a higher abstraction level — the deferral unit is the **skill** (a bundle of related tools) rather than a single MCP server.

## Skill composition

Skills are designed to be independently authored and composed at runtime:

- **Layering** — multiple skills can coexist without modification; tool namespacing prevents collision
- **Versioning** — skills are pinned by version; rolling updates don't break existing agent deployments until the author explicitly upgrades
- **Marketplace / registry** — Anthropic's vision is a skill registry where teams and third parties publish skills that others can attach to their agents without rebuilding from scratch

The `claude-obsidian` plugin (used in this vault) is an example of skills delivered as a bundle: `wiki`, `wiki-ingest`, `wiki-query`, `wiki-lint`, `wiki-fold`, `save`, `autoresearch`, `canvas`, `defuddle`, `obsidian-markdown`, `obsidian-bases` — 11 skills, each independently usable and togglable.

## Skill authoring (developer-facing)

Skills are authored as YAML/JSON manifests:

```yaml
name: web-browser
version: 1.2.0
description: "Enables Claude to browse web pages, extract content, and follow links."
tools:
  - name: fetch_page
    description: "Fetch and return the content of a URL"
    input_schema: { ... }
    input_examples: [ ... ]
  - name: search_web
    description: "Run a web search and return top results"
    input_schema: { ... }
prompt_fragment: |
  You have access to a web browsing skill. Use fetch_page to retrieve specific URLs
  and search_web for open-ended queries. Prefer primary sources. Cite URLs in responses.
defer_loading: true
```

Key authoring decisions:
- `defer_loading: true` makes the skill available via the skill manifest only; full tool set loads on first use.
- `prompt_fragment` is injected after the base system prompt and before the user turn — it's the skill's "how to use me" documentation.
- `input_examples` on each tool definition follows the [[Tool Use Examples]] pattern (see [[2025-11-24 - Anthropic - Advanced Tool Use]]).

## Relationship to MCP

Agent Skills and MCP are complementary, not competing:

- **MCP** is the **wire protocol** — how tools connect to external services. MCP server = a process that exposes tools over a standardized interface.
- **Agent Skills** is the **packaging and delivery layer** — how a *bundle* of tools (possibly backed by MCP servers, but also raw function definitions) is authored, versioned, and attached to agents.

A skill can wrap one or more MCP servers. The skill manifest handles discovery; MCP handles execution transport. This layering is intentional: you can have a skill without MCP (pure function definitions) or MCP servers without skills (raw server attachment as today).

## Context economics

The progressive-disclosure design directly addresses the context-cost problem documented in [[Token Economics]] and [[KV-Cache Discipline]]:

| Naive approach | Skills approach |
|---|---|
| All tool definitions always in context | Manifests only until skill is invoked |
| Context cost: O(n_tools × avg_tool_def_size) | Context cost: O(n_skills × manifest_size) + on-demand full load |
| KV-cache hit rate: low (changes when any tool is edited) | KV-cache hit rate: high (manifest is stable) |

For a typical agent with 5 skills and 8 tools each = 40 tool definitions. Under naive loading this is a fixed 40-tool overhead on every request. Under skills: 5 short manifests at all times, plus the 8 tools for whichever skill is active.

## Reliability implications

Agent Skills improve reliability through two mechanisms:

1. **Reduced cognitive load** — smaller active tool set means fewer wrong-tool-selection errors (the failure mode Anthropic flagged in [[2025-11-24 - Anthropic - Advanced Tool Use]]).
2. **Prompt fragment co-authoring** — the skill author controls how the model is primed to use the skill. This is analogous to writing a good docstring; the skill surface is the ACI ([[ACI - Agent-Computer Interface]]) surface, and the skill author is now responsible for making it usable.

## Key claims

1. Agent Skills = versioned bundles of (tools + prompt fragments + resource handles)
2. Progressive disclosure: manifest-first, full load on demand — reduces context bloat
3. Skills + MCP are complementary: MCP is wire protocol, Skills is packaging layer
4. Skill composition is additive: union of attached skills = agent's capability set
5. Skills enable a skill marketplace / registry model — ecosystem play, not just API
6. Prompt fragments per skill = distributed authoring of how the agent reasons about each capability
7. Context cost under skills: O(skills × manifest) not O(all tools) — directly improves KV-cache stability

## Connections to existing wiki

- [[Tool Search Tool]] — sibling mechanism; skills defer at bundle level, Tool Search defers at tool level
- [[MCP]] — wire protocol that skills can use as transport
- [[ACI - Agent-Computer Interface]] — skills are the ACI surface; authoring skills = ACI design work
- [[Tool Use Examples]] — `input_examples` field reused inside skill tool definitions
- [[Token Economics]] — progressive disclosure is a direct answer to context-cost pressure
- [[KV-Cache Discipline]] — stable manifest prefix preserves cache hit rate
- [[Context Engineering]] — skills as a structured way to manage context across capability domains
