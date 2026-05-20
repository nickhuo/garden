---
type: concept
title: "Permission Model"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - security
  - claude-code
status: developing
complexity: basic
domain: ai-agents
aliases:
  - "prompt-based trust"
  - "policy-based trust"
  - "agentic permissions"
related:
  - "[[Agent Sandboxing]]"
  - "[[Prompt Injection]]"
  - "[[Claude Code]]"
  - "[[Autonomous Agents]]"
  - "[[Workflows vs Agents]]"
sources:
  - "[[2026-05-13 - Anthropic - Claude Code Sandboxing]]"
---

# Permission Model

How an agentic system decides which actions to allow and which to block. The central design choice is between **prompt-based trust** (ask the user at each action) and **policy-based trust** (define a policy upfront, enforce it automatically).

## Prompt-Based Trust (legacy)

The default in early agentic systems: the agent asks for explicit user approval before each sensitive action ("I want to read this file — allow?").

**Failure modes:**
- **Prompt fatigue** — users approve reflexively; the prompt becomes security theater.
- **Granularity mismatch** — users understand task-level intent, not tool-call-level consequences; they can't make good per-action decisions.
- **Headless incompatibility** — unattended CI runs have no user to prompt.
- **No defense-in-depth** — a manipulated agent will still forward the harmful action through the prompt to the user, who approves reflexively.

## Policy-Based Trust

Inspired by OS permission models (app capabilities declared at install time, enforced by OS at runtime). For agents:
- **Policy definition** at session start (project `CLAUDE.md`, CLI flags, or defaults).
- **Policy enforcement** at runtime by the OS sandbox — outside the agent's control.
- **Escape hatches** for power users (explicit flags, logged warnings).

This enables autonomous headless operation with bounded risk.

## Layered Model (Claude Code's approach)

Three layers of permission enforcement, from hardest to softest:

| Layer | Mechanism | Bypassable by |
|---|---|---|
| OS sandbox | Seatbelt / seccomp | Only kernel exploits |
| Safety training | Model-level refusals | Jailbreaks, prompt injection |
| User trust grants | Permission prompts | User click-through |

The OS sandbox is the hard floor. Safety training catches obvious misuse. User prompts handle residual high-consequence actions the sandbox allows but the model flags.

## Implications for Agent Design

- **Autonomous agents** need policy-based trust; prompt-based trust breaks at scale and in headless contexts.
- **Workflows** are more tractable for policy definition — their action paths are more predictable, so allowlists are smaller and more accurate. See [[Workflows vs Agents]].
- **MCP servers** expand capabilities but inherit the same policy envelope as the session. Trust-tier containment is required.

## Sources

- [[2026-05-13 - Anthropic - Claude Code Sandboxing]] — introduced policy-based trust as the production answer to prompt fatigue.
