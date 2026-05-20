---
source_url: https://www.anthropic.com/engineering/desktop-extensions
fetched: 2026-05-13
title: "Desktop Extensions: One-click MCP server installation for Claude Desktop"
author: Anthropic Engineering
---

# Desktop Extensions: One-click MCP server installation for Claude Desktop

*From the Anthropic Engineering blog*

## Overview

Desktop Extensions (DXT) is a new packaging format introduced by Anthropic that enables one-click installation of MCP (Model Context Protocol) servers into Claude Desktop. Prior to DXT, installing an MCP server required manual configuration — editing JSON config files, installing Node.js or Python runtimes, and managing environment variables. DXT eliminates that friction by bundling everything a server needs into a single `.dxt` file.

## The Problem DXT Solves

Before DXT, the MCP server installation process was developer-centric and created significant barriers:

1. **Manual JSON editing** — users had to locate and edit `claude_desktop_config.json` by hand.
2. **Runtime dependencies** — servers required Node.js, Python, or other runtimes pre-installed on the host machine.
3. **Environment variable management** — API keys and secrets had to be injected manually.
4. **No discoverability** — there was no catalog or marketplace for finding available MCP servers.

This meant MCP adoption was largely limited to developers comfortable with CLI tooling, even though Claude Desktop's user base is broader.

## What DXT Is

A `.dxt` file is a ZIP archive containing:

- The MCP server code (bundled, with dependencies included — no external runtime install needed for Node.js servers via `node` bundled inside, or Python via bundled interpreters)
- A `manifest.json` describing the extension: name, version, author, permissions, required user configuration fields
- Icons and metadata for display in the Claude Desktop UI

The manifest declares what the extension needs from the user (e.g., an API key for a third-party service), and Claude Desktop presents a UI to collect those inputs on install — no JSON editing required.

## Installation Flow

1. User clicks a `.dxt` link or downloads it from a registry/website.
2. Claude Desktop opens an install dialog showing the extension's name, description, permissions requested, and any required configuration fields.
3. User fills in any required fields (e.g., API keys) and clicks Install.
4. Claude Desktop writes the MCP server config automatically and starts the server.
5. The extension's tools are immediately available to Claude in that session.

## The Extension Manifest

`manifest.json` is the heart of a DXT package. Key fields:

```json
{
  "dxt_version": "0.1",
  "name": "my-extension",
  "display_name": "My Extension",
  "version": "1.0.0",
  "description": "...",
  "author": { "name": "...", "url": "..." },
  "server": {
    "type": "node",
    "entry_point": "server/index.js",
    "mcp_config": {
      "command": "node",
      "args": ["${__dirname}/server/index.js"],
      "env": {
        "API_KEY": "${user_config.api_key}"
      }
    }
  },
  "user_config": {
    "api_key": {
      "type": "string",
      "title": "API Key",
      "description": "Your API key from ...",
      "required": true,
      "sensitive": true
    }
  }
}
```

The `${user_config.*}` template syntax lets the manifest reference values the user supplies at install time. Sensitive fields are stored in the OS keychain, not in plain-text config files.

## Bundling and Runtime

For Node.js servers, DXT uses `dxt pack` (a CLI tool Anthropic ships) which runs `npm install` and bundles dependencies into the archive — similar to how Electron apps bundle Node. This means users don't need Node.js installed system-wide.

Python support uses a similar approach: bundling a minimal Python interpreter or relying on `uv` for fast, isolated installs.

## Security Model

- Permissions are declared upfront in the manifest.
- Claude Desktop shows a permissions review screen before install.
- Sensitive config values are stored in the OS keychain (macOS Keychain, Windows Credential Manager).
- Extensions run as separate processes (same as manual MCP servers) — sandboxed by process isolation, not by a VM.
- No code execution at install time (unlike npm postinstall scripts).

## Developer Tooling

Anthropic ships a `dxt` CLI:

```bash
npm install -g @anthropic-ai/dxt
dxt init        # scaffold a new extension
dxt pack        # bundle into .dxt file
dxt validate    # lint the manifest
```

The CLI also supports a `dxt dev` mode for hot-reloading during local development.

## Registry and Discovery

At launch, Anthropic provides a reference registry and links DXT packages from the Claude.ai website. Third-party registries can also host `.dxt` files — the format is open. Claude Desktop can be pointed at multiple registries.

## Impact on MCP Ecosystem

DXT is explicitly designed to grow the MCP server ecosystem beyond developers. By lowering the installation barrier to one click:

- Non-technical users can install MCP servers.
- MCP server authors have a clear, standard distribution channel.
- The surface area for MCP integrations expands: web services, enterprise tools, creative apps.

Anthropic positions DXT as the "app store moment" for MCP — analogous to how mobile app stores made software distribution trivially easy for consumers.

## Relationship to Existing MCP Concepts

- **MCP protocol itself is unchanged.** DXT is a packaging/distribution layer on top, not a protocol change.
- **Tool definitions, server lifecycle, stdio/SSE transport** — all the same.
- **Advanced Tool Use features** (like [[Tool Search Tool]] deferred loading) apply equally to DXT-installed servers.
- Token overhead from large MCP servers (documented in [[Advanced Tool Use]]) remains — DXT doesn't reduce tool-definition token cost.

## Key Quotes

> "Desktop Extensions make it possible for anyone — not just developers — to add powerful new capabilities to Claude Desktop."

> "The `.dxt` format is open. We hope it becomes the standard way to distribute MCP servers, regardless of which client you're using."

## Availability

Desktop Extensions launched alongside Claude Desktop version support in 2025. The DXT spec and CLI are open-source on GitHub under `anthropics/dxt`.
