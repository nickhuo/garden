---
type: concept
title: Agentic Coding Slash Commands
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - claude-code
  - coding
status: seed
complexity: basic
domain: ai-agents
aliases:
  - slash commands
  - claude commands
  - custom slash commands
related:
  - "[[Claude Code]]"
  - "[[brain/03_Resources/wiki/concepts/CLAUDE]]"
sources:
  - "[[2026-05-13 - Anthropic - Claude Code Best Practices]]"
---

# Agentic Coding Slash Commands

A mechanism in [[Claude Code]] for defining reusable, team-shared prompt templates invoked via `/command-name` syntax.

## Mechanics

- Files live at `.claude/commands/<name>.md`
- Filename becomes the slash command: `fix-bug.md` → `/fix-bug`
- Support a `$ARGUMENTS` placeholder for dynamic input
- Version-controlled alongside the codebase — shared across the team automatically

## Use cases

- Standardize common workflows: `/new-feature`, `/review-pr`, `/update-tests`
- Encode team conventions in a single invocation
- Chain multiple steps (explore → plan → implement → test) in one command
- Onboard new team members to consistent Claude usage patterns

## Relationship to CLAUDE.md

[[brain/03_Resources/wiki/concepts/CLAUDE]] sets persistent per-session context; slash commands set per-task prompts. They are complementary: CLAUDE.md handles "always know this," slash commands handle "do this operation in this way."

## Analogy

Similar in spirit to Makefile targets or npm scripts — a shared vocabulary of operations that any team member can invoke consistently.
