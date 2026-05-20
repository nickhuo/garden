---
source_url: https://www.anthropic.com/engineering/claude-code-auto-mode
title: "Claude Code auto mode: a safer way to skip permissions"
author: Anthropic
date_fetched: 2026-05-13
---

# Claude Code auto mode: a safer way to skip permissions

*Source: https://www.anthropic.com/engineering/claude-code-auto-mode*
*Archived: 2026-05-13*

---

## Overview

Claude Code's auto mode (triggered with `--dangerously-skip-review` or configured via `autoPermissions`) provides a principled, model-driven alternative to blanket "approve everything" flows. Instead of asking the user to confirm each tool call, Claude Code in auto mode uses a permission classifier to decide — at inference time — whether a given action is safe to execute without human review.

The core insight: **not all tool calls are equally risky**. Reading a file is categorically different from running an arbitrary shell command or making a network request. A naive "skip all permissions" flag treats them identically; auto mode discriminates.

## The permission problem

When running Claude Code in fully autonomous pipelines (CI/CD, headless servers, automated agents), users historically had two options:

1. **Manual approval** — interrupt the agent on every tool call. Defeats the purpose of automation.
2. **`--dangerously-skip-review`** — approve everything blindly. Works, but surfaces all risk to the operator with no model-level filtering.

Auto mode introduces a third path.

## How auto mode works

Claude Code maintains a **permission policy** — a hierarchical set of rules that classifies tool calls into:

- **Auto-approve**: safe by construction (read-only file access, no side effects)
- **Needs review**: potentially destructive or irreversible (file deletion, shell execution, network writes)
- **Always block**: explicitly prohibited actions (e.g., certain system-level operations)

The classification happens **per tool call, at inference time**, using a lightweight classifier model that runs alongside the main Claude agent. The classifier considers:

- Tool category (bash, file read, file write, network, etc.)
- Tool call parameters (path scope, command content, destination)
- Conversation context (what task is Claude performing?)
- Operator-defined policy overrides (via `settings.json` or environment config)

### Permission levels

Claude Code exposes three permission levels operators can set:

```
"autoPermissions": {
  "level": "auto" | "manual" | "none",
  "allowedTools": [...],
  "blockedTools": [...],
  "pathRestrictions": {"readOnly": ["..."], "blocked": ["..."]}
}
```

- `"level": "auto"` — classifier decides, operator overrides respected
- `"level": "manual"` — all tool calls prompt for approval (default)
- `"level": "none"` — no permissions system (equivalent to old `--dangerously-skip-review`)

### Sandboxing integration

Auto mode is designed to integrate with sandboxed execution environments. The recommended deployment pattern:

1. Run Claude Code in a Docker container or VM
2. Set `"level": "auto"` with tight path restrictions
3. Network egress controlled at the infrastructure layer

The sandbox handles what the policy can't — network restrictions, file system isolation, resource limits. The permission classifier handles what the sandbox can't — semantic understanding of what Claude is about to do.

## The classifier in practice

Anthropic measured classifier performance on an internal evaluation set of ~10,000 tool calls drawn from real Claude Code sessions:

| Action type | Auto-approve rate | Review triggered |
|---|---|---|
| File reads | ~98% | ~2% (sensitive paths) |
| File writes (non-destructive) | ~85% | ~15% |
| Shell commands (benign) | ~70% | ~30% |
| File deletions | ~5% | ~95% |
| Network requests | ~40% | ~60% |
| System modifications | ~2% | ~98% |

The classifier is conservative by design: it prefers false positives (unnecessary review requests) over false negatives (approving something harmful).

## Safety design principles

### Minimal footprint

Auto mode embeds Claude's broader **minimal footprint principle**: prefer reversible over irreversible actions, do less when uncertain, avoid side effects that weren't explicitly requested.

This principle is already expressed in Claude's system prompt for agentic tasks; auto mode operationalizes it at the tool-call layer via classifier policy rather than relying solely on Claude's in-context reasoning.

### Audit trail

All tool calls in auto mode are logged with:
- The classifier's decision (auto-approve / review / block)
- Confidence score
- Which policy rule was matched

This log is available at `~/.claude/logs/permissions-YYYY-MM-DD.jsonl`.

### Principle of least privilege

Operators are encouraged to start with the narrowest policy and widen incrementally. The `pathRestrictions` config supports per-directory read-only and blocked rules, letting operators constrain file-system surface before deploying.

## Operator-defined policy overrides

Operators can extend or restrict the default classifier behavior:

```json
{
  "autoPermissions": {
    "level": "auto",
    "allowedTools": ["bash", "read", "write"],
    "blockedTools": ["browser"],
    "pathRestrictions": {
      "readOnly": ["/etc", "/usr"],
      "blocked": ["/private", "~/.ssh"]
    }
  }
}
```

This means auto mode is not a fixed policy — it's a **policy framework** layered on top of the classifier defaults.

## Claude Code as autonomous agent enabler

Auto mode is explicitly positioned as infrastructure for **headless / agentic deployments** of Claude Code:

- CI/CD pipeline integration (run Claude Code as part of build/test)
- Server-side agent execution (no human in the loop)
- Nested agent calls (Claude spawning sub-agents via [[Managed Agents]])

The announcement mentions Claude Code running as a [[Managed Agents]]-hosted harness, where auto mode is the intended permission policy for unattended execution.

## Relationship to broader agent safety work

Auto mode is a practical instantiation of several principles that appear across Anthropic's agent safety writing:

- **Minimal footprint** — do less, prefer reversibility ([[Building Effective Agents]])
- **Human-in-the-loop calibration** — auto mode isn't about removing humans; it's about routing the right decisions to humans while automating routine approvals
- **Defense in depth** — classifier + sandbox + audit log, not classifier alone

The framing is explicitly "a safer way to skip permissions," not "a way to skip safety."

## Key quotes

> "Not every tool call requires human judgment. Reading a file is not the same as deleting one. Auto mode lets Claude make that distinction for you."

> "The classifier is conservative by design. We prefer Claude pausing unnecessarily over Claude acting when it shouldn't."

> "Auto mode is not a trust escalation. It's a trust calibration — moving human attention to the decisions that actually need it."

## Related

- [[Claude Code]] (entity — the product)
- [[Managed Agents]] (hosting substrate for headless Claude Code)
- [[Autonomous Agents]] (concept — the use case auto mode enables)
- [[ACI - Agent-Computer Interface]] (permission system as part of agent-computer interface design)
- [[MCP]] (tool-call layer that auto mode classifies over)
