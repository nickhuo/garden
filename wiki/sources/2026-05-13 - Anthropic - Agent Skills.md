---
type: source
title: "Equipping agents for the real world with Agent Skills"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - skills
  - tool-design
  - context-engineering
  - anthropic
status: developing
source_type: article
author: Anthropic Engineering
date_published: 2026-05-13
url: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
confidence: high
related:
  - "[[Agent Skills]]"
  - "[[Tool Search Tool]]"
  - "[[MCP]]"
  - "[[ACI - Agent-Computer Interface]]"
  - "[[Tool Use Examples]]"
  - "[[Token Economics]]"
  - "[[KV-Cache Discipline]]"
  - "[[Progressive Disclosure]]"
sources:
  - "[[.raw/articles/2026-05-13 - Anthropic - Agent Skills.md]]"
key_claims:
  - "Agent Skills are versioned bundles of tools + prompt fragments + resource handles"
  - "Progressive disclosure: manifest-first loading reduces context bloat"
  - "Skills and MCP are complementary — MCP is wire protocol, Skills is packaging layer"
  - "Skill composition is additive: agent capability = union of attached skills"
  - "Context cost under Skills is O(skills × manifest) vs O(all tools) naive"
  - "Prompt fragments per skill enable distributed authoring of agent reasoning"
---

# Equipping agents for the real world with Agent Skills

Anthropic Engineering blog post introducing **Agent Skills** — a primitive for packaging, versioning, and attaching reusable capability bundles to Claude agents.

## The problem

Every agent deployment re-specifies the same capabilities (web browsing, code execution, calendar access) from scratch. This causes context bloat, maintenance fragmentation, and a discoverability gap. The agent only knows what it was told at system-prompt time.

## What Agent Skills are

A **Skill** is a versioned, self-contained bundle containing:
- **Tool definitions** — function signatures the model can invoke
- **Prompt fragments** — system-prompt text priming the model on when/how to use those tools
- Optionally, **resource handles** pointing to MCP servers, APIs, or databases

Skills are attached at agent instantiation; the agent's capability set = union of all attached skills.

## Progressive disclosure — the key design principle

Skills don't dump all context into the model's window at once. Instead:

1. Each skill registers a **lightweight manifest** (short description + one discovery tool).
2. When the agent determines a skill is relevant, it invokes the discovery tool, receiving the **full tool set** for that skill.
3. Full tool definitions + examples load into context **only when needed**.

This is structurally analogous to [[Tool Search Tool]]'s `defer_loading` mechanism, but the unit of deferral is the **skill** (a bundle of related tools) rather than a single MCP server. See [[Progressive Disclosure]] for the cross-cutting concept.

## Skills + MCP — complementary, not competing

- **MCP** = wire protocol (how tools connect to external services)
- **Agent Skills** = packaging and delivery layer (how a bundle of tools is authored, versioned, attached)

A skill can wrap one or more MCP servers. MCP handles execution transport; the skill manifest handles discovery. You can have a skill without MCP (pure function defs) or MCP without skills (raw server attachment).

## Context economics

| Approach | Context cost | KV-cache stability |
|---|---|---|
| Naive (all tools always loaded) | O(n_tools × def_size) | Low — changes when any tool edits |
| Skills (progressive) | O(n_skills × manifest) + on-demand | High — manifest is stable prefix |

Directly addresses [[Token Economics]] and [[KV-Cache Discipline]] concerns.

## Reliability improvements

1. **Reduced cognitive load** — smaller active tool set → fewer wrong-tool-selection errors (failure mode flagged in [[2025-11-24 - Anthropic - Advanced Tool Use]])
2. **Skill-author controls prompt priming** — prompt fragment is the ACI surface ([[ACI - Agent-Computer Interface]]); authors are now responsible for making their skill usable

## Skill authoring

Skills are YAML/JSON manifests with `name`, `version`, `description`, `tools` (with `input_examples` per [[Tool Use Examples]]), `prompt_fragment`, and `defer_loading` flag.

The `claude-obsidian` plugin used in this vault is a real-world example: 11 skills (`wiki`, `wiki-ingest`, `wiki-query`, etc.) each independently authored, versioned, and togglable.

## Ecosystem vision

Anthropic envisions a **skill registry / marketplace** where teams and third parties publish skills others can attach without rebuilding from scratch. This is the platform play: skills become the unit of capability distribution across the Claude ecosystem.

## Key claims

1. Agent Skills = versioned bundles of (tools + prompt fragments + resource handles)
2. Progressive disclosure reduces context bloat: manifest first, full load on demand
3. Skills + MCP are complementary layers, not alternatives
4. Skill composition is additive: agent capabilities = union of attached skills
5. Context cost under Skills is O(skills × manifest), improving KV-cache stability
6. Prompt fragments = distributed ACI authoring; skill author owns the UX of their capability
7. Skills enable a marketplace/registry model — ecosystem play

## Connections

- [[Agent Skills]] — entity page for the feature itself
- [[Progressive Disclosure]] — new concept: manifest-first, load-on-demand pattern
- [[Tool Search Tool]] — sibling mechanism at single-tool deferral level
- [[MCP]] — complementary wire protocol
- [[ACI - Agent-Computer Interface]] — skills are the ACI surface
- [[Tool Use Examples]] — `input_examples` reused inside skill tool defs
- [[Token Economics]] — progressive disclosure answers context-cost pressure
- [[KV-Cache Discipline]] — stable manifest prefix preserves cache hit rate
- [[Context Engineering]] — skills as structured context-domain management
