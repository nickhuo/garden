---
type: entity
title: Claude Code
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - anthropic
  - product
  - developer-tools
entity_type: product
role: Agentic coding assistant and autonomous agent harness, built by Anthropic
first_mentioned: "[[2026-04 - Anthropic - Claude Code Auto Mode]]"
status: developing
related:
  - "[[Managed Agents]]"
  - "[[MCP]]"
  - "[[Permission Classifier]]"
  - "[[Permission Model]]"
  - "[[Agent Sandboxing]]"
  - "[[Prompt Injection]]"
  - "[[Minimal Footprint Principle]]"
  - "[[Autonomous Agents]]"
  - "[[brain/CLAUDE]]"
  - "[[Agentic Coding Slash Commands]]"
sources:
  - "[[2026-04 - Anthropic - Claude Code Auto Mode]]"
  - "[[2026-05-13 - Anthropic - Claude Code Best Practices]]"
  - "[[2026-05-13 - Anthropic - Claude Code Sandboxing]]"
---

# Claude Code

## Summary

Anthropic's agentic coding assistant and autonomous agent harness. Claude Code operates as an agent that can read/write files, run shell commands, and call external tools via [[MCP]] — going well beyond single-turn code generation into multi-step autonomous task execution.

As of April 2026, Claude Code is also the reference implementation of a [[Managed Agents]]-hosted harness — meaning it can run fully headless (no human in the loop) as part of CI/CD pipelines or server-side agent workflows.

## Key capabilities

- File system access (read, write, create, delete)
- Shell command execution (bash)
- Network requests
- MCP tool integration
- Multi-step autonomous task execution with configurable permission policies

## Permission system (auto mode)

Claude Code exposes three permission levels via `autoPermissions` config:

| Level | Behavior |
|---|---|
| `"manual"` | Default. Every tool call requires human approval. |
| `"auto"` | Classifier decides per-call. Operator overrides respected. |
| `"none"` | No permission system — equivalent to old `--dangerously-skip-review`. |

Auto mode uses a [[Permission Classifier]] — a lightweight inference-time model that evaluates each tool call against its category, parameters, conversation context, and operator policy. Classifier auto-approve rates range from ~98% (file reads) to ~2% (system modifications). See [[Permission Classifier]] for the full breakdown.

Recommended headless deployment: `"auto"` level + OS sandbox (Docker/VM) + audit log. Defense in depth — not classifier alone.

## Minimal footprint integration

Auto mode mechanically operationalizes the [[Minimal Footprint Principle]] at the tool-call layer: prefer reversible over irreversible actions, block when uncertain, audit everything. Previously this principle lived only in Claude's in-context reasoning; auto mode adds an explicit enforcement layer.

## Role in the Managed Agents ecosystem

Claude Code is explicitly cited as the reference harness running on [[Managed Agents]] infrastructure. In this configuration:
- **Brain**: Claude model + harness logic
- **Hands**: sandboxed execution environment
- **Session**: event log (durable, append-only)

Auto mode is the intended permission policy for Managed Agents-hosted Claude Code deployments.

## Connections

- Hosting substrate: [[Managed Agents]]
- Tool layer: [[MCP]]
- Permission policy: [[Permission Classifier]]
- Safety principle: [[Minimal Footprint Principle]]
- Use case: [[Autonomous Agents]] · [[Workflows vs Agents]]
- Interface design: [[ACI - Agent-Computer Interface]]

## Open questions

- Pricing for Claude Code in Managed Agents-hosted vs local mode — are they the same API?
- Does [[Tool Search Tool]] apply inside Claude Code's tool-call layer, or does auto mode handle tool discovery separately?

## Configuration surface (from Best Practices, 2026-05-13)

The [[brain/CLAUDE]] files (root, subdirectory, `~/.claude/`) are auto-loaded at session start and are the primary persistent-config mechanism. [[Agentic Coding Slash Commands]] in `.claude/commands/` provide reusable prompt templates shared across the team.

**Headless mode** (`claude -p "prompt"`) runs Claude Code non-interactively for CI, git hooks, and scheduled scripts. Pair with `--output-format json` for structured programmatic output.

**Context management levers:** `/clear` resets conversation; `/compact` summarizes and compresses; each spawned subagent gets a fresh context window. Intermediate results can be written to files for persistence across compaction.

**Mental model (Anthropic):** Treat as a skilled but literal junior engineer. Executes exactly what is asked, needs codebase context, benefits from small verifiable tasks and explicit review checkpoints.

## OS-level Sandboxing (from Sandboxing post, 2026-05-13)

Claude Code runs tool-use sessions inside an OS-level sandbox — macOS Seatbelt (`sandbox-exec`) or Linux seccomp + namespaces. This is the **hard floor** of the security model, below the [[Permission Classifier]] layer.

Network sandboxing modes: permissive (outbound allowed) / allowlist (explicit domains only) / blocked (air-gapped CI). Declared via project `CLAUDE.md` or CLI flags.

[[Prompt Injection]] is the named primary threat model: malicious content inside a repo hijacks the session. The OS sandbox limits blast radius even when injection succeeds.

See [[Agent Sandboxing]] and [[Permission Model]] for detailed treatment.

## Sources

- [[2026-04 - Anthropic - Claude Code Auto Mode]] (Anthropic, April 2026)
- [[2026-05-13 - Anthropic - Claude Code Best Practices]] (Anthropic, May 2026)
- [[2026-05-13 - Anthropic - Claude Code Sandboxing]] (Anthropic, May 2026)
