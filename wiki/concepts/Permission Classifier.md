---
type: concept
title: Permission Classifier
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - safety
  - tool-use
  - permissions
complexity: intermediate
domain: ai-agents
aliases:
  - auto mode classifier
  - tool call classifier
status: seed
related:
  - "[[Claude Code]]"
  - "[[Minimal Footprint Principle]]"
  - "[[ACI - Agent-Computer Interface]]"
  - "[[Autonomous Agents]]"
  - "[[MCP]]"
sources:
  - "[[2026-04 - Anthropic - Claude Code Auto Mode]]"
---

# Permission Classifier

## Summary

A lightweight inference-time model that classifies individual tool calls as **auto-approve**, **needs human review**, or **block** — based on semantic risk rather than tool category alone. First instantiated in [[Claude Code]]'s auto mode (April 2026).

The classifier solves the binary permission problem: without it, autonomous agents must choose between "interrupt the user on every tool call" or "blindly approve everything." The classifier creates a middle path: routine approvals are automated, consequential decisions still surface to humans.

## Inputs

For each tool call, the classifier evaluates:

1. **Tool category** — bash, file read, file write, network request, system modification, etc.
2. **Parameters** — path scope, command content, destination, argument structure
3. **Conversation context** — what task is Claude currently performing?
4. **Operator policy** — `allowedTools`, `blockedTools`, `pathRestrictions` from config

## Output categories

- **Auto-approve** — safe by construction; execute immediately
- **Needs review** — potentially destructive or irreversible; surface to human
- **Block** — prohibited by operator policy; reject with explanation

## Empirical auto-approve rates (Claude Code internal eval, ~10K tool calls)

| Action type | Auto-approve | Review triggered |
|---|---|---|
| File reads | ~98% | ~2% (sensitive paths) |
| File writes (non-destructive) | ~85% | ~15% |
| Shell commands (benign) | ~70% | ~30% |
| File deletions | ~5% | ~95% |
| Network requests | ~40% | ~60% |
| System modifications | ~2% | ~98% |

## Design principle: conservative by default

> "We prefer Claude pausing unnecessarily over Claude acting when it shouldn't."

The classifier is calibrated to prefer false positives (unnecessary review requests) over false negatives (approving something harmful). This means some legitimately safe tool calls will still surface for human review — that's intentional.

## Operator configuration

Operators extend or restrict classifier defaults via:

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

This makes the classifier a **policy framework** — the base classifier provides semantic defaults, operators configure domain-specific overrides.

## Audit trail

All decisions are logged to `~/.claude/logs/permissions-YYYY-MM-DD.jsonl` with:
- Decision (auto-approve / review / block)
- Confidence score
- Matched policy rule

This is critical for post-hoc review of headless agent runs.

## Relationship to Minimal Footprint Principle

The [[Minimal Footprint Principle]] — "prefer reversible actions, do less when uncertain" — was previously expressed only in Claude's system prompt. The Permission Classifier operationalizes it at the tool-call layer: it enforces reversibility-preference mechanically, not just through in-context reasoning. Same principle, two enforcement points.

## Connections

- First instantiation: [[Claude Code]] auto mode
- Hosting context: [[Managed Agents]] (headless deployments)
- Safety principle: [[Minimal Footprint Principle]]
- Interface layer: [[ACI - Agent-Computer Interface]] (permission system is part of ACI design)
- Tool layer being classified: [[MCP]] tool calls included
- Defense-in-depth partner: OS sandbox + classifier + audit log together

## Open questions

- Is the classifier model published or proprietary?
- Does the classifier handle [[MCP]]-sourced tool calls differently from built-in tools?
- What is the false-negative rate on the internal evaluation set?
- How does classifier performance change across model versions (Sonnet vs Opus vs Haiku)?

## Sources

- [[2026-04 - Anthropic - Claude Code Auto Mode]] (Anthropic, April 2026)
