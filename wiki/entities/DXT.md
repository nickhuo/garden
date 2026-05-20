---
type: entity
title: DXT
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - mcp
  - claude-desktop
  - anthropic
status: seed
entity_type: product
role: Open packaging format for distributing MCP servers as one-click installable Desktop Extensions
first_mentioned: "[[2025-06-26 - Anthropic - Desktop Extensions]]"
aliases:
  - Desktop Extensions
  - .dxt
related:
  - "[[MCP]]"
  - "[[Claude Desktop]]"
  - "[[Tool Search Tool]]"
  - "[[Token Economics]]"
sources:
  - "[[2025-06-26 - Anthropic - Desktop Extensions]]"
---

# DXT — Desktop Extensions

## Summary

DXT is Anthropic's open packaging format (`.dxt` files) for distributing [[MCP]] servers as one-click installable extensions in [[Claude Desktop]]. The name stands for **Desktop Extensions**. The spec and CLI toolchain are open-source at `anthropics/dxt` on GitHub.

## What a `.dxt` File Contains

A `.dxt` file is a ZIP archive:

| Component | Purpose |
|---|---|
| `manifest.json` | Declares name, version, permissions, user config fields, server entry point |
| Bundled server code | The MCP server implementation |
| Bundled dependencies | Node modules or Python packages — no external runtime needed |
| Icons / metadata | For display in Claude Desktop UI |

## Key Design Decisions

- **`manifest.json` as contract.** Permissions and required user inputs are declared upfront — no post-install surprises.
- **`${user_config.*}` templating.** Config fields the user supplies at install time are referenced symbolically; `sensitive: true` fields are written to the OS keychain, never plain-text config files.
- **No code execution at install.** Unlike npm `postinstall` scripts, `.dxt` install is declarative. Security surface is narrower.
- **Process isolation.** MCP servers run as separate OS processes (same as manual MCP installs). Sandbox is OS-level process isolation, not a VM.
- **Open format.** Third-party registries can host `.dxt` files. Claude Desktop can be pointed at multiple registries.

## CLI Toolchain

```bash
npm install -g @anthropic-ai/dxt
dxt init       # scaffold new extension
dxt pack       # bundle into .dxt
dxt validate   # lint manifest
dxt dev        # hot-reload for local development
```

## What DXT Does NOT Change

- The MCP protocol itself (stdio/SSE transport, tool definitions, capability negotiation).
- Token overhead from large tool-definition payloads — [[Token Economics]] concerns remain.
- [[Tool Search Tool]] deferred loading remains necessary as users accumulate many servers.

## Ecosystem Impact

DXT is the "app store moment" for MCP — analogous to how mobile app stores abstracted software distribution from technical install steps. Expected effect: MCP server adoption accelerates beyond developer early adopters, increasing the practical importance of [[Tool Search Tool]] and [[KV-Cache Discipline]] to manage the resulting token overhead.

## Connections

- Host client: [[Claude Desktop]]
- Protocol served: [[MCP]]
- Token overhead concern: [[Token Economics]], [[Tool Search Tool]]
- Interface layer: [[ACI - Agent-Computer Interface]]