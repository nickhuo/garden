---
type: entity
title: Claude Desktop
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - mcp
  - claude-desktop
  - anthropic
status: seed
entity_type: product
role: Desktop application; primary MCP client for end users
first_mentioned: "[[2025-06-26 - Anthropic - Desktop Extensions]]"
related:
  - "[[MCP]]"
  - "[[DXT]]"
  - "[[ACI - Agent-Computer Interface]]"
sources:
  - "[[2025-06-26 - Anthropic - Desktop Extensions]]"
---

# Claude Desktop

## Summary

Anthropic's native desktop application (macOS and Windows) that runs Claude locally and serves as the primary consumer-facing MCP client. It is the distribution target for [[DXT]] (Desktop Extensions) — the packaging format that enables one-click MCP server installation for non-technical users.

## Role in the MCP Ecosystem

Claude Desktop is the **runtime host** for MCP servers on the user's machine. Prior to [[DXT]], connecting an MCP server required users to manually edit `claude_desktop_config.json` and manage runtime dependencies. Claude Desktop's DXT integration provides:

- A GUI install dialog for `.dxt` packages
- Automatic config file management
- OS keychain integration for sensitive credentials (API keys)
- Process management for running MCP server processes

## Significance

Claude Desktop is where MCP adoption translates from developer tooling to general-user utility. The introduction of DXT makes Claude Desktop analogous to a mobile OS with an app store — the platform that turns a protocol ecosystem into a consumer product.

## Connections

- Protocol layer: [[MCP]]
- Install format: [[DXT]]
- Tool discovery: [[Tool Search Tool]] (deferred loading relevant when users install many servers)
- Interface framing: [[ACI - Agent-Computer Interface]]
- Token cost: [[Token Economics]] (unaffected by DXT packaging — overhead remains)
