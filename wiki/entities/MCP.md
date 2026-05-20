---
type: entity
title: MCP
created: 2026-05-04
updated: 2026-05-13
tags:
- ai-agents
- protocol
- anthropic
status: developing
related:
  - "[[DXT]]"
  - "[[Claude Desktop]]"
  - "[[Tool Search Tool]]"
  - "[[ACI - Agent-Computer Interface]]"
sources:
  - "[[2025-06-26 - Anthropic - Desktop Extensions]]"
aliases:
- Model Context Protocol
_legacy_source_count: 2
---

# MCP — Model Context Protocol

## Summary

Anthropic-introduced open protocol that standardizes how LLM applications connect to third-party tools and data sources. Referenced in [[Building Effective Agents]] as the path to ecosystem-scale tool integration without bespoke per-vendor integrations.

## Why it matters

If MCP wins adoption, the [[Augmented LLM]] tool layer becomes vendor-portable — the same tool definitions work across Claude, ChatGPT, Cursor, etc. This is the protocol bet at the [[ACI - Agent-Computer Interface]] layer.

## Status (as of source ingest, 2024-12)

- Open protocol, Anthropic-stewarded
- Anthropic, partners, and tooling vendors building servers
- Coverage growing: file systems, databases, APIs

## Token-overhead anchor (per Anthropic 2025-11)

[[2025-11-24 - Anthropic - Advanced Tool Use]] gives concrete numbers on MCP's context cost at scale — the friction MCP creates is now sharp enough that Anthropic has shipped platform features to mitigate it:

| Setup | Tool-def overhead |
|---|---|
| 5-server typical (GitHub 35, Slack 11, Sentry 5, Grafana 5, Splunk 2) | ~55K tokens |
| Adding Jira | +17K tokens (~72K total) |
| Anthropic's internal worst case | 134K tokens |

The mitigation is per-server deferral via [[Tool Search Tool]]'s `mcp_toolset` config — defer the entire server, optionally keeping select tools eager-loaded:

```
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-drive",
  "default_config": {"defer_loading": true},
  "configs": { "search_files": {"defer_loading": false} }
}
```

Implication for MCP server design: as Tool Search becomes the default integration path, **server authors will optimize for discoverability** (clear names, descriptive purposes, search-friendly keywords) and may trend toward fewer-but-fatter tools to reduce search-result fan-out.

Also notable: Anthropic's most-common observed failure mode under MCP is **wrong tool selection and incorrect parameters** — especially with similar names (`notification-send-user` vs `notification-send-channel`). This is an ACI quality concern at the protocol level, not just a per-server one.

## Connections

- Tool framing: [[ACI - Agent-Computer Interface]]
- Discovery layer: [[Tool Search Tool]] (cache-safe deferred loading per server)
- Context cost: [[Token Economics]] · [[Context Engineering]]
- Substrate: [[Augmented LLM]]

## MCP servers as compute endpoints (per Anthropic 2026-05-13)

[[2026-05-13 - Anthropic - Code Execution with MCP]] introduces a design pattern shift: MCP servers should not be purely data proxies but **compute-capable endpoints**. By embedding code execution inside MCP tool definitions, servers can process data locally and return only reduced results — rather than flooding the model's context with raw data.

The pattern: MCP server bundles (1) data-access tools + (2) a code execution tool that can call those data-access tools from inside a sandboxed runtime. Model writes processing code in the `code` parameter; server executes it and returns stdout.

Implications for MCP server authorship:
- Document available libraries in tool descriptions (new ACI requirement)
- Return structured error strings, not raised exceptions (agents must handle gracefully)
- Design for stateless sandboxes (per-session isolation; state must be explicitly passed across turns)
- Composable with [[Tool Search Tool]] `defer_loading` — code execution tool can itself be deferred, giving both efficiency layers

## Distribution layer: DXT Desktop Extensions (per Anthropic 2026-05-13)

[[2025-06-26 - Anthropic - Desktop Extensions]] introduces [[DXT]] — a `.dxt` packaging format that wraps MCP servers into one-click installable extensions for [[Claude Desktop]]. DXT is a distribution layer only; the MCP protocol, tool definitions, and token overhead are unchanged.

Key additions to the MCP ecosystem picture:
- **Adoption curve.** DXT moves MCP server installation from developer-only (manual JSON config, runtime installs) to general-user territory. This is the distribution inflection that could expand active MCP server counts per user significantly.
- **Token overhead amplified.** As users accumulate more DXT-installed servers, the total tool-definition context cost grows. [[Tool Search Tool]] deferred loading becomes more important, not less.
- **Security perimeter.** DXT manifests declare permissions upfront; sensitive values (API keys) go to OS keychain; no code execution at install time. Process-isolation model unchanged from manual MCP installs.
- **Open format.** Third-party registries can host `.dxt` files — MCP distribution is not locked to Anthropic's registry.

## Relationship to Agent Skills (per Anthropic 2026-05-13)

[[2026-05-13 - Anthropic - Agent Skills]] makes the MCP/Skills boundary explicit: MCP = **wire protocol** (execution transport); [[Agent Skills]] = **packaging and delivery layer** (bundles of tools + prompt fragments, versioned and composable). A skill can wrap one or more MCP servers. The two are complementary, not competing. See [[Progressive Disclosure]] for how Skills apply manifest-first loading at the bundle level — the coarse-grained equivalent of [[Tool Search Tool]]'s per-server `defer_loading`.

## MCP and the Permission Classifier (per Anthropic 2026-04)

[[2026-04 - Anthropic - Claude Code Auto Mode]] raises an open question: does [[Claude Code]]'s [[Permission Classifier]] handle MCP-sourced tool calls the same way as built-in tools? MCP servers expose arbitrary tools — their risk profile isn't inherently known without understanding the underlying implementation. A permissive MCP tool definition could allow auto-approval of inherently risky operations. This is an ACI quality concern at the protocol level (same category as the wrong-tool-selection failure mode), now with a permission-classification dimension.

## MCP Server Sandboxing (per Anthropic 2026-05-13 Sandboxing)

[[2026-05-13 - Anthropic - Claude Code Sandboxing]] addresses MCP's security surface directly. MCP servers expand Claude Code's capabilities but expand the attack surface — a malicious or compromised MCP server could instruct Claude to exfiltrate data or escalate privileges.

Resolution: MCP server processes run inside the **same OS-level sandbox envelope** as the Claude Code session. They cannot access filesystem paths outside the project root, and their network calls are subject to the same allowlist policy. Trust-tier model: Claude Code session > user-approved MCP servers > untrusted environment content.

This closes the "arbitrary tool definition" risk raised in [[2026-04 - Anthropic - Claude Code Auto Mode]] — even if a MCP tool definition authorizes a risky operation, the OS sandbox enforces a hard ceiling.

## Open questions

- Will OpenAI / Google adopt MCP, or fragment with their own protocols?
- Security model under multi-tenant MCP servers — open question. The compute endpoint pattern increases the attack surface (arbitrary code execution inside server).
- Does embedding code execution in MCP servers create reentrancy risks (code execution tool calling another tool that itself embeds code execution)?
- How does MCP compare to function-calling APIs and vendor plugin systems? Need a comparison page after 2nd source.
- How does [[Permission Classifier]] handle MCP-sourced tool calls vs built-in tools?

## Sources

- [[Building Effective Agents]] (Anthropic, 2024-12-19)
- [[2025-11-24 - Anthropic - Advanced Tool Use]] (Anthropic, 2025-11-24)
- [[2026-05-13 - Anthropic - Code Execution with MCP]] (Anthropic, 2026-05-13)
- [[2026-04 - Anthropic - Claude Code Auto Mode]] (Anthropic, April 2026)
