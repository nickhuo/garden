---
type: source
title: "Claude Code: Best practices for agentic coding"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - claude-code
  - coding
status: developing
source_type: article
author: Anthropic Engineering
date_published: 2026-05-13
url: https://www.anthropic.com/engineering/claude-code-best-practices
confidence: high
related:
  - "[[Claude Code]]"
  - "[[CLAUDE.md]]"
  - "[[Agentic Coding Slash Commands]]"
  - "[[Multi-Agent Systems]]"
  - "[[Context Engineering]]"
  - "[[MCP]]"
sources:
  - "[[.raw/articles/2026-05-13 - Anthropic - Claude Code Best Practices.md]]"
key_claims:
  - "CLAUDE.md files are auto-loaded at session start — the primary persistent-config lever"
  - "Custom slash commands in .claude/commands/ are version-controlled and team-shared"
  - "Claude Code supports headless mode (-p flag) for CI pipelines and git hooks"
  - "Claude Code acts as both orchestrator and subagent — spawns parallel Task calls"
  - "Permission model has allow/deny lists; --dangerously-skip-permissions only for containers"
  - "Junior-engineer mental model: literal, needs context, benefits from small verifiable tasks"
---

# Claude Code: Best Practices for Agentic Coding

Anthropic's engineering best-practices post for [[Claude Code]], distilled from internal teams and early adopters.

## Summary

Ten practice areas covering how to get reliable, safe output from Claude Code as an agentic coding tool operating directly in terminals.

## Key Claims

1. **[[CLAUDE.md]] is the primary configuration primitive.** Files at `~/.claude/CLAUDE.md`, project root, and subdirectories are merged and loaded at session start. Recommended contents: build/test/lint commands, code style, testing instructions, repo etiquette, gotchas. Keep concise — bullet points preferred.

2. **Slash commands standardize team workflows.** `.claude/commands/<name>.md` files define reusable `/commands` with `$ARGUMENTS` placeholders. Version-controlled alongside code. Enables encoding conventions like `/new-feature`, `/review-pr`.

3. **Headless mode for automation.** `claude -p "prompt"` runs non-interactively. Suitable for CI, git hooks, scheduled scripts. Pair with `--output-format json` for structured programmatic output.

4. **Multi-agent orchestration via Task tool.** Claude Code spawns parallel subagent instances, each with an independent context window. Best for: large migrations, parallel test generation, independent research subtasks. [[Parallelization]] pattern applies directly.

5. **Layered permission model.** Allow/deny lists for shell commands; `--allowedTools` per invocation; `--dangerously-skip-permissions` only for sandboxed CI contexts. Start restrictive.

6. **Context management levers.** `/clear` resets conversation, `/compact` summarizes and compresses. Sub-agents give fresh context windows for long tasks. Write intermediate results to files for persistence across compaction.

7. **Prompting patterns that work well:**
   - Explore-first, plan-second (especially on unfamiliar codebases)
   - `think hard` / `ultrathink` for hard problems
   - TDD-style: write tests first, then implement
   - One-thing-at-a-time over mega-prompts
   - Course-correct early (restoring from a bad long run is expensive)

8. **Safety at scale.** Run in containers for risky tasks. Audit log at `claude-code-audit.log`. Never `--dangerously-skip-permissions` on shared hosts.

9. **Mental model — junior engineer framing.** Claude executes exactly what you ask, needs codebase context, benefits from review checkpoints, and should receive small verifiable tasks rather than open-ended mandates.

## Entities Mentioned

- [[Claude Code]] — Anthropic's terminal-native agentic coding tool (dedicated page)
- [[MCP]] — mentioned as an integration surface for connecting external services

## Concepts Touched

- [[CLAUDE.md]] — persistent config mechanism (new concept page)
- [[Agentic Coding Slash Commands]] — `.claude/commands/` pattern (new concept page)
- [[Context Engineering]] — headless + context-management practices are a coding-domain instantiation
- [[Multi-Agent Systems]] — orchestrator/subagent roles explicitly described
- [[Parallelization]] — Task-based parallel subagent spawning
- [[Workflows vs Agents]] — Claude Code is positioned as a workflow-like tool; orchestrator mode is the agent case
- [[Token Economics]] — `/compact`, sub-agents, and fresh context windows all manage token budget

## Assessment

High confidence — first-party Anthropic engineering post. Practical rather than theoretical. No major contradictions with existing wiki content; the orchestrator/subagent framing aligns cleanly with [[Multi-Agent Systems]] and [[Workflows vs Agents]].
