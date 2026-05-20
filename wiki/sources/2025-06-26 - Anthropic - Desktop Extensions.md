---
type: source
title: "Desktop Extensions: One-click MCP server installation for Claude Desktop"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - mcp
  - claude-desktop
status: developing
source_type: article
author: Anthropic Engineering
date_published: 2025-06-26
url: https://www.anthropic.com/engineering/desktop-extensions
confidence: high
key_claims:
  - DXT (.dxt) is a ZIP-based packaging format that enables one-click MCP server installation in Claude Desktop
  - Bundles server code and dependencies so users need no external runtime (Node/Python) pre-installed
  - manifest.json declares permissions and user config fields; sensitive values go to OS keychain
  - DXT is a distribution layer only — MCP protocol, tool definitions, and token overhead are unchanged
  - Anthropic open-sources the DXT spec and CLI (anthropics/dxt on GitHub)
  - Positioned as the "app store moment" for MCP — extends adoption beyond developers
related:
  - "[[MCP]]"
  - "[[Claude Desktop]]"
  - "[[DXT]]"
  - "[[Tool Search Tool]]"
  - "[[ACI - Agent-Computer Interface]]"
sources:
  - "[[.raw/articles/2025-06-26 - Anthropic - Desktop Extensions.md]]"
---

# Desktop Extensions: One-click MCP server installation for Claude Desktop

**Source:** Anthropic Engineering blog — https://www.anthropic.com/engineering/desktop-extensions
**Filed:** 2026-05-13

## Summary

Anthropic introduced **Desktop Extensions (DXT)** — a `.dxt` packaging format that reduces MCP server installation in [[Claude Desktop]] from a multi-step developer workflow (JSON editing, runtime installs, env-var management) to a single click. A `.dxt` file is a ZIP archive containing bundled server code, dependencies, and a `manifest.json` that declares permissions and user config fields. Claude Desktop presents a GUI install dialog, stores sensitive values (API keys) in the OS keychain, and auto-writes the MCP config.

## Key Claims

1. **One-click install.** Users click a `.dxt` link; Claude Desktop handles the rest — no terminal, no JSON editing.
2. **Self-contained bundle.** `dxt pack` bundles Node.js dependencies (or Python interpreter) inside the archive. No system-wide runtime required.
3. **Declarative config.** `manifest.json` uses `${user_config.*}` template syntax to collect user-supplied values at install time. `sensitive: true` fields go to OS keychain.
4. **Protocol-unchanged.** DXT is a packaging/distribution layer. MCP protocol, stdio/SSE transport, tool definitions, and token overhead are all unchanged.
5. **Open format.** Spec and CLI (`dxt init`, `dxt pack`, `dxt validate`, `dxt dev`) are open-source at `anthropics/dxt`. Third-party registries can host `.dxt` files.
6. **Ecosystem play.** Anthropic explicitly frames DXT as the distribution inflection for MCP — moving from developer-only adoption to general user adoption.

## Implications

- Token overhead from large MCP server tool definitions ([[Token Economics]], [[Tool Search Tool]]) is **not** reduced by DXT. The packaging solves distribution friction, not context-window friction.
- As DXT lowers the install barrier, the number of active MCP servers per Claude Desktop user is likely to rise — making [[Tool Search Tool]]'s deferred-loading strategy more important, not less.
- Security model: process isolation (not VM), permissions declared upfront, OS keychain for secrets. No code execution at install time (unlike npm postinstall).
- [[ACI - Agent-Computer Interface]] observation: DXT standardizes the human-side of ACI (installing/configuring tool interfaces) just as MCP standardizes the LLM-side.

## Entities Mentioned

- [[Claude Desktop]] — the client application
- [[DXT]] — the packaging format itself
- [[MCP]] — the underlying protocol DXT serves

## Raw Source

`.raw/articles/2025-06-26 - Anthropic - Desktop Extensions.md`
