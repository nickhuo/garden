---
type: concept
title: "Agent Sandboxing"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - security
  - claude-code
status: developing
complexity: intermediate
domain: ai-agents
aliases:
  - "OS-level sandboxing"
  - "agentic sandboxing"
related:
  - "[[Permission Model]]"
  - "[[Prompt Injection]]"
  - "[[Claude Code]]"
  - "[[ACI - Agent-Computer Interface]]"
  - "[[Autonomous Agents]]"
  - "[[MCP]]"
sources:
  - "[[2026-05-13 - Anthropic - Claude Code Sandboxing]]"
---

# Agent Sandboxing

The practice of running an AI agent's tool-execution environment inside an OS-level isolation boundary (sandbox), so that even if the agent's model judgment fails or is manipulated, its actions are bounded by a hard policy enforced by the operating system.

## Why Sandboxing, Not Prompts

Permission prompts (ask the user for each sensitive action) fail for three reasons:
1. **Prompt fatigue** — users approve reflexively after the first few prompts.
2. **Headless breakage** — CI / unattended runs have no human to prompt.
3. **No defense-in-depth** — a manipulated agent can still approve harmful actions through the prompt.

OS-level sandboxing cannot be socially-engineered — it enforces policy regardless of what the model decides.

## Platform Implementations

### macOS: Seatbelt (sandbox-exec)
BSD mandatory access control. A Seatbelt profile is generated dynamically per project:
- Read: project directory + system libraries.
- Write: project directory, temp dir, agent config.
- Deny write: sensitive home-dir paths (`.ssh/`, `.aws/`, credentials).
- Network: allowlist-driven; deny-all by default with explicit TCP allowances.

### Linux: seccomp + namespaces
- **User namespaces** — separate user/mount/network namespace.
- **seccomp-bpf** — syscall allowlist; blocks `ptrace`, `mount`, `setuid`, etc.
- **Bind mounts** — read-only system view; read-write project dir only.
- **Network namespace + iptables** — outbound connection control.

## Network Sandboxing Modes

| Mode | Description | Use case |
|---|---|---|
| Permissive | Outbound allowed, inbound blocked | General development |
| Allowlist | Only listed domains permitted | Regulated or high-security projects |
| Blocked | No network access | Air-gapped CI |

Policy declared in project `CLAUDE.md` or via CLI flags.

## Trust Tiers

Sandboxing enables a tiered trust model:

| Tier | Example | Policy |
|---|---|---|
| Session | Claude Code process | Full policy envelope |
| Extensions | MCP server processes | Same policy as session |
| Environment content | Repo files, web pages | Untrusted — cannot alter policy |

This means malicious content inside a repo cannot escalate beyond what the sandbox permits.

## Relationship to Prompt Injection

[[Prompt Injection]] attacks embed instructions in environment content to hijack the agent's actions. Sandboxing is the **last-resort defense**: even if Claude is deceived, the injected command can't:
- Write to paths outside the project directory.
- Make outbound network calls to non-allowlisted hosts.
- Execute privilege-escalating syscalls.

Sandboxing doesn't prevent deception — it limits blast radius.

## Design Principle

**Fail safe by default, fail open only on explicit opt-out.** An unsupported sandbox environment is logged prominently; it does not silently degrade. The `--no-sandbox` escape hatch requires an explicit flag and generates a warning.

## Connection to ACI

[[ACI - Agent-Computer Interface]] argues that tools for LLMs deserve the same engineering rigor as HCI tools for humans. Sandboxing extends this: the *interface boundary* between agent and computer should be a hard, enforced boundary — not an advisory one relying on the model's judgment.

## Sources

- [[2026-05-13 - Anthropic - Claude Code Sandboxing]] — primary source; introduced sandboxing as a production agentic security primitive.
