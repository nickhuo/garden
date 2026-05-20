---
type: concept
title: "CLAUDE.md"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - claude-code
  - coding
status: developing
complexity: basic
domain: ai-agents
aliases:
  - "claude md"
  - "claude config file"
related:
  - "[[Claude Code]]"
  - "[[Agentic Coding Slash Commands]]"
  - "[[Context Engineering]]"
sources:
  - "[[2026-05-13 - Anthropic - Claude Code Best Practices]]"
---

# CLAUDE.md

The primary persistent-configuration mechanism for [[Claude Code]]. Markdown files named `CLAUDE.md` are automatically merged and loaded into context at the start of every Claude Code session.

## Layered loading

Three locations, all merged:

1. `~/.claude/CLAUDE.md` — personal preferences (style, editor prefs, global gotchas)
2. `<project-root>/CLAUDE.md` — project-wide instructions
3. `<subdirectory>/CLAUDE.md` — subproject or component-specific overrides

## Recommended contents

- Build, test, and lint commands
- Core files and utility functions to be aware of
- Code style guide
- Testing framework and conventions
- Repository etiquette (branch naming, PR process)
- Dev environment specifics (tool versions, setup gotchas)
- Known anti-patterns and project-specific pitfalls
- Links to external docs Claude may not have in training

## What NOT to put in CLAUDE.md

- Extensive prose — bullet points are faster to scan
- Information Claude can infer from the codebase (don't duplicate code comments)
- One-off instructions that belong in the current prompt

## Relationship to context engineering

CLAUDE.md is a form of [[Context Engineering]] applied to the coding domain: it pre-populates the context window with the exact information needed for a session, avoiding repeated exposition in each prompt. The discipline is the same — provide just-in-time, high-signal context, not a data dump.

## Continuous refinement

Anthropic recommends updating CLAUDE.md whenever Claude gets something wrong repeatedly. Each correction encodes a lesson that persists across all future sessions.
