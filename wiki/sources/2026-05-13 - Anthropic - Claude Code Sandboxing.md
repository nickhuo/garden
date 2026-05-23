---
type: source
title: "Beyond permission prompts: making Claude Code more secure and autonomous"
aliases:
  - "Claude Code Sandboxing"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - security
  - claude-code
status: developing
author: Anthropic Engineering
date_published: 2026-05-13
url: https://www.anthropic.com/engineering/claude-code-sandboxing
confidence: high
source_type: engineering-blog
related:
  - "[[Claude Code]]"
  - "[[Agent Sandboxing]]"
  - "[[Permission Model]]"
  - "[[MCP]]"
  - "[[Prompt Injection]]"
sources:
  - "[[.raw/articles/2026-05-13 - Anthropic - Claude Code Sandboxing.md]]"
key_claims:
  - "Permission prompts don't scale — prompt fatigue causes reflexive approval, and they collapse under agentic headless workflows."
  - "OS-level sandboxing (macOS Seatbelt, Linux seccomp + namespaces) enforces filesystem and network policy without user intervention."
  - "Network sandboxing prevents prompt-injection-driven exfiltration even when Claude is deceived."
  - "MCP servers run inside the same sandbox envelope as the Claude Code session, limiting blast radius of malicious MCP tools."
  - "Trust model is layered: OS sandbox (hard) > Claude safety training (model-level) > user trust grants (soft)."
  - "Policy-based trust (define upfront, enforce automatically) replaces prompt-based trust (ask at each action)."
---

# Beyond permission prompts: making Claude Code more secure and autonomous

Anthropic Engineering blog post on Claude Code's sandboxing architecture — how moving from permission prompts to OS-level policy enforcement enables safe autonomy.

## The Core Argument

Permission prompts fail at scale. Users approve reflexively (prompt fatigue), prompts are meaningless in unattended CI runs, and they provide no defense when Claude is manipulated by injected content. Real control requires OS-level enforcement that cannot be socially-engineered.

## Technical Architecture

### macOS: Seatbelt (sandbox-exec)
Apple's BSD mandatory-access-control framework. Claude Code generates a dynamic Seatbelt profile:
- Read: project dir + system libraries.
- Write: project dir + temp dir + Claude config.
- Deny: `.ssh/`, `.aws/`, other sensitive home-dir paths.
- Network: allowlist-driven (deny all, allow specific remote TCP endpoints).

### Linux: seccomp + namespaces
- User namespaces for isolation envelope.
- seccomp-bpf to block dangerous syscalls (`ptrace`, `mount`, `setuid`).
- Bind mounts: read-only system view, read-write project dir only.
- Network namespace + iptables for outbound control.

## Network Sandboxing Modes
1. **Permissive** — outbound allowed, inbound blocked (transitional default).
2. **Allowlist** — only listed domains permitted; declared in project `CLAUDE.md` or CLI.
3. **Blocked** — no network; for air-gapped CI.

## [[MCP]] Server Sandboxing
MCP servers run inside the same sandbox envelope as the Claude Code session. Trust-tier model:
- Claude Code session — highest trusted tier.
- User-approved MCP servers — second tier, same filesystem/network policy.
- Untrusted content (web pages, repo files) — lowest tier.

This contains blast radius if an MCP server is malicious or compromised.

## Layered Trust Model
| Layer | Mechanism | Can be bypassed by |
|---|---|---|
| OS sandbox | Seatbelt / seccomp | Only kernel exploits |
| Safety training | Model-level refusals | Jailbreaks, injection |
| User trust grants | Permission prompts | User click-through |

The OS sandbox is the hard floor — it cannot be talked past.

## Prompt Injection Resistance

Key threat model: malicious content inside a repo or webpage hijacks the Claude session. Sandboxing limits blast radius:
- Injected commands can't reach outside project directory.
- Injected `curl | sh` exfiltration blocked if network sandboxed.
- Privilege escalation blocked at syscall level.

Sandboxing doesn't prevent Claude being deceived — it bounds damage when deception succeeds.

## Developer Experience Trade-offs
- Broad-filesystem tools (home-dir config scanners) need explicit allowlist entries.
- Sysadmin tasks (`/etc/hosts`, `/usr/local/`) blocked by default.
- CI environments without user-namespace support get degraded sandbox (logged prominently).
- Escape hatch: `--no-sandbox` flag (logs warning).

Design principle: **fail safe by default, fail open only on explicit opt-out**.

## Significance for the AI-Agents Wiki

This is the first source in the corpus explicitly addressing **security architecture** for agentic systems. Prior sources (Anthropic, Manus, Sierra) address capability, context engineering, and reliability. This one addresses the orthogonal question: what happens when capability and context engineering are insufficient?

Connects to:
- [[Autonomous Agents]] — headless autonomy requires hard bounds, not prompts.
- [[Prompt Injection]] — sandboxing as last-resort defense against injection.
- [[MCP]] — expands attack surface; this source is the first to address MCP threat model.
- [[Workflows vs Agents]] — policy-based trust is more tractable for workflows (predictable paths) than open-ended agents (unpredictable paths).
- [[ACI - Agent-Computer Interface]] — sandboxing is a foundational ACI concern: the interface to the computer should have enforced boundaries, not just advisory ones.
