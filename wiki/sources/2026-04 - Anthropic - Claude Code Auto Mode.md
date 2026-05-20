---
type: source
title: "Claude Code auto mode: a safer way to skip permissions"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - claude-code
  - safety
  - permissions
status: developing
source_type: engineering-blog
author: Anthropic
date_published: 2026-04
url: https://www.anthropic.com/engineering/claude-code-auto-mode
confidence: high
related:
  - "[[Claude Code]]"
  - "[[Managed Agents]]"
  - "[[Autonomous Agents]]"
  - "[[ACI - Agent-Computer Interface]]"
  - "[[Permission Classifier]]"
  - "[[Minimal Footprint Principle]]"
sources:
  - "[[.raw/articles/2026-04 - Anthropic - Claude Code Auto Mode.md]]"
key_claims:
  - "Auto mode uses a per-call classifier to discriminate safe vs risky tool calls, replacing the binary skip-all-permissions flag."
  - "Classifier is conservative by design — false positives (unnecessary review) preferred over false negatives (approving harm)."
  - "Three-level policy framework: auto, manual, none — with operator overrides for allowed/blocked tools and path restrictions."
  - "Intended deployment pattern is classifier + sandbox (Docker/VM) + audit log in combination, not classifier alone."
  - "Auto mode is explicitly infrastructure for headless/agentic Claude Code — CI/CD, server-side agents, nested agent calls."
  - "Minimal footprint principle operationalized at the tool-call layer, not just in Claude's in-context reasoning."
---

# Claude Code auto mode: a safer way to skip permissions

**Source:** Anthropic Engineering Blog, April 2026
**URL:** https://www.anthropic.com/engineering/claude-code-auto-mode
**Raw:** `.raw/articles/2026-04 - Anthropic - Claude Code Auto Mode.md`

## Thesis

Autonomous agent deployments need a permission model that is neither "ask the user every time" nor "blindly approve everything." Auto mode introduces a **classifier-based, operator-configurable permission framework** that routes tool calls to auto-approval or human review based on semantic risk — not just tool category.

## Key Claims

1. **Binary permission model is inadequate.** The old `--dangerously-skip-review` flag treats file reads and file deletions identically. That's architecturally wrong — risk is a function of the tool call's semantics, not just its existence.

2. **Per-call classifier at inference time.** A lightweight classifier runs alongside Claude and evaluates each tool call against: tool category, parameters, conversation context, and operator policy. Result: auto-approve / needs-review / block.

3. **Three-tier permission levels.** `"auto"` (classifier decides), `"manual"` (default, human approves all), `"none"` (old skip-all behavior). Operator can set `allowedTools`, `blockedTools`, and `pathRestrictions`.

4. **Conservative classifier design.** Empirical auto-approve rates: file reads ~98%, benign shell commands ~70%, file deletions ~5%, system modifications ~2%. The classifier prefers unnecessary review over missed harm.

5. **Defense in depth, not defense by classifier.** Recommended deployment: classifier policy + OS-level sandbox (Docker/VM) + structured audit log. No single layer carries the full safety burden.

6. **Minimal footprint principle made mechanical.** Auto mode embeds Claude's existing guidance ("prefer reversibility, do less when uncertain") into a tool-call-time policy, not just in-context reasoning. Same principle, different enforcement point.

7. **Enabling infrastructure for headless agents.** Explicitly positioned for CI/CD, server-side, and [[Managed Agents]]-hosted deployments of [[Claude Code]]. Auto mode is the intended permission policy when no human is in the loop.

## Methods / Evidence

- Internal evaluation on ~10,000 tool calls drawn from real Claude Code sessions, with auto-approve rates broken down by action type.
- Configuration schema examples for operator policy overrides.
- Architecture diagram of classifier + sandbox + audit log layers.

## Important Quotes

> "Not every tool call requires human judgment. Reading a file is not the same as deleting one. Auto mode lets Claude make that distinction for you."

> "The classifier is conservative by design. We prefer Claude pausing unnecessarily over Claude acting when it shouldn't."

> "Auto mode is not a trust escalation. It's a trust calibration — moving human attention to the decisions that actually need it."

## Claims with Wikilinks

- The permission problem is a [[Workflows vs Agents]] implementation concern — autonomous agents need a scalable approval model that doesn't require human attention on every step.
- The classifier operationalizes [[Minimal Footprint Principle]] at the tool-call layer — a new enforcement point not previously explicit in the wiki.
- Auto mode is the bridge between [[Claude Code]] (the tool) and [[Managed Agents]] (the hosting substrate) for headless deployments.
- [[ACI - Agent-Computer Interface]] thinking applied: the permission layer is part of the agent-computer interface design, not an afterthought.
- [[Autonomous Agents]] as the primary use case: CI/CD, server-side execution, nested agent calls.
- [[Token Economics]] relevance: the audit log (`~/.claude/logs/permissions-YYYY-MM-DD.jsonl`) and classifier add marginal overhead — worth tracking as headless deployments scale.
- The operator policy framework (`allowedTools`, `blockedTools`, `pathRestrictions`) is an instance of [[Permission Classifier]] — a new concept worth a dedicated page.

## Connections

- Entity created: [[Claude Code]]
- Concepts created: [[Permission Classifier]], [[Minimal Footprint Principle]]
- Concepts updated: [[Autonomous Agents]], [[ACI - Agent-Computer Interface]]
- Entities updated: [[Managed Agents]]

## Open Questions

- Does the classifier run client-side or server-side? Latency implications for high-frequency tool-calling agents.
- Is the classifier model published or proprietary? Could third parties fine-tune it for domain-specific policies?
- How does auto mode interact with [[MCP]]? MCP servers expose arbitrary tools — does the classifier handle MCP-sourced tool calls the same way as built-in tools?
- What's the false-negative rate on the internal eval set? The post reports auto-approve rates by category but not harm-event rates.
