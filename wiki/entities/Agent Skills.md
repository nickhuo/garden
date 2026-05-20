---
type: entity
title: Agent Skills
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - anthropic
  - tool-design
  - skills
status: developing
entity_type: product
role: "Anthropic's capability-packaging primitive for Claude agents"
first_mentioned: "2026-05-13 - Anthropic - Agent Skills"
related:
  - "[[MCP]]"
  - "[[Tool Search Tool]]"
  - "[[Progressive Disclosure]]"
  - "[[ACI - Agent-Computer Interface]]"
  - "[[Tool Use Examples]]"
sources:
  - "[[2026-05-13 - Anthropic - Agent Skills]]"
aliases:
  - Skills
  - Agent Skill
---

# Agent Skills

Anthropic's primitive for packaging, versioning, and distributing reusable capabilities for Claude agents. A Skill bundles tools, prompt fragments, and resource handles into a versioned, composable unit.

## What a Skill is

| Component | Role |
|---|---|
| Tool definitions | Function signatures the model can invoke |
| Prompt fragment | System-prompt text priming model on when/how to use the skill |
| Resource handles | Optional pointers to MCP servers, APIs, databases |
| Version | Pinned identifier enabling stable deployments and rolling updates |

## How Skills attach

Skills are declared at agent instantiation. The agent's effective capability set = the **union** of all attached skills. Multiple skills coexist via tool namespacing (no collision).

## Progressive disclosure

Skills use a manifest-first loading pattern (see [[Progressive Disclosure]]): each skill's lightweight manifest is always in context; the full tool set loads only when the agent invokes the discovery tool. This keeps context small when a skill is unused and accurate when it is active.

## Relationship to MCP

[[MCP]] = wire protocol (execution transport). Agent Skills = packaging and delivery layer. A skill can wrap one or more MCP servers. The two are complementary: you can author a skill without MCP (pure function definitions) or use MCP servers without skills (direct attachment).

## Ecosystem role

Anthropic's stated vision is a **skill registry / marketplace** — a shared catalog where teams and third parties publish skills that any Claude agent can attach. Skills become the unit of capability distribution across the Claude ecosystem.

## Real-world instantiation

The `claude-obsidian` plugin (used in this vault) demonstrates the skills model: 11 skills (`wiki`, `wiki-ingest`, `wiki-query`, `wiki-lint`, `wiki-fold`, `save`, `autoresearch`, `canvas`, `defuddle`, `obsidian-markdown`, `obsidian-bases`) — each independently authored, versioned, and togglable.

## Connections

- [[Progressive Disclosure]] — the loading mechanism that makes Skills context-efficient
- [[Tool Search Tool]] — sibling deferral mechanism at single-tool level (Skills defers at bundle level)
- [[MCP]] — wire protocol Skills can use for execution transport
- [[ACI - Agent-Computer Interface]] — the skill surface is the ACI surface; skill authoring = ACI design
- [[Tool Use Examples]] — `input_examples` field appears inside skill tool definitions
- [[Token Economics]] — progressive disclosure directly answers context-cost pressure
- [[KV-Cache Discipline]] — stable manifest prefix preserves cache hit rate

## Sources

- [[2026-05-13 - Anthropic - Agent Skills]]
