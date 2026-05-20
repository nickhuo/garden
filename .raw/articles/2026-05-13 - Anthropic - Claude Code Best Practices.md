---
source_url: https://www.anthropic.com/engineering/claude-code-best-practices
fetched: 2026-05-13
author: Anthropic Engineering
title: "Claude Code: Best practices for agentic coding"
---

# Claude Code: Best practices for agentic coding

> Source: https://www.anthropic.com/engineering/claude-code-best-practices

## Overview

This post shares best practices for using Claude Code effectively, distilled from Anthropic's own engineering teams and early adopters. Claude Code is Anthropic's agentic coding tool that operates directly in terminals, reads codebases, edits files, runs tests, and executes commands.

---

## 1. Be thoughtful about what to put in CLAUDE.md

`CLAUDE.md` files are automatically loaded into context at the start of every Claude Code session. They are the primary configuration mechanism.

**Recommended contents:**
- Bash commands (build, test, lint) that Claude should know
- Core files and utility functions
- Code style guide
- Testing instructions (framework, how to run, how to write)
- Repository etiquette (branch naming, PR practices)
- Dev environment info (tool versions, setup notes)
- Project-specific gotchas and known anti-patterns
- Links to external docs (e.g., library docs Claude may not know)

**Placement:**
- Root `CLAUDE.md` — project-wide instructions
- Subdirectory `CLAUDE.md` — subproject or component-specific instructions
- `~/.claude/CLAUDE.md` — personal preferences (style, editor setup, etc.)

**Recommendation:** Keep CLAUDE.md concise. Bullet-point format preferred. Not the place for extensive prose. Continuously refine based on what Claude gets wrong repeatedly.

---

## 2. Give Claude the tools it needs

Claude Code works with whatever tools are accessible in the terminal environment:

- **Web search and fetch** — built-in, for looking up APIs and docs
- **MCP servers** — connect to external services, specialized tools, APIs
- **Custom bash scripts** — if you have internal tooling, expose it
- **Browser access** — Claude can use browser-based tools via Playwright MCP

**Key principle:** Don't give Claude tools it doesn't need for the task. Fewer available actions = less risk of unintended side effects.

---

## 3. Develop a prompt framework for yourself

Common patterns that work well with Claude Code:

- **Explore first, plan second** — ask Claude to describe what it sees before touching anything; works especially well on unfamiliar codebases
- **Ultrathink / think hard** — explicit think-budget prompts produce much better plans on hard problems
- **Write tests first, then implement** — TDD-style prompting is highly reliable; Claude rarely "games" the tests it just wrote
- **One thing at a time** — break large tasks into smaller sequential prompts rather than one mega-prompt
- **Course-correct early** — interrupt before Claude goes too far down a wrong path; restoring from a bad long run is expensive

---

## 4. Use headless / non-interactive mode for automation

`claude -p "prompt"` runs Claude Code non-interactively, suitable for:
- CI pipelines
- Git hooks (pre-commit, commit-msg)
- Scheduled maintenance scripts
- Bulk code generation / migration tasks

Output is piped to stdout by default. Combine with `--output-format json` for structured output in scripts.

---

## 5. Customize Claude with slash commands

Custom slash commands live in `.claude/commands/` as Markdown files. The filename becomes the slash command name. They support a `$ARGUMENTS` placeholder.

Example: `.claude/commands/fix-bug.md` → `/fix-bug`

**Use cases:**
- Standardize common workflows (e.g., `/new-feature`, `/review-pr`, `/update-tests`)
- Encode team conventions in reusable prompts
- Chain multiple steps (explore → plan → implement → test) in a single command

Slash commands are version-controlled and shared across the team automatically.

---

## 6. Tune trust and permission settings

Claude Code has a permission model for what shell commands it can run without approval:

- **Default:** Claude asks before any shell command that modifies state
- **Allow lists:** Add patterns to auto-approve for common safe commands
- **Deny lists:** Always prompt for high-risk commands regardless of other settings
- **Headless mode trust:** `claude --dangerously-skip-permissions` for fully automated CI contexts (use only in sandboxes/containers)

**Recommended practice:** Start restrictive, loosen after trust is established. Review the permission log for surprises.

---

## 7. Understand Claude's multi-agent capabilities

Claude Code can act as both an **orchestrator** and a **subagent**:

- **Orchestrator mode** — Claude Code spawns parallel subagent instances via `Task` tool calls, each working on a subtask concurrently
- **Subagent mode** — Claude Code is invoked by another agent or automation and returns structured results

Best for parallelization when:
- Tasks are genuinely independent (no shared mutable state)
- Each subtask fits within one context window
- Combining results is straightforward

Multi-agent Claude Code works well for: large codebase migrations, generating test suites for many files simultaneously, parallel research on different components.

---

## 8. Safe scripting practices

Because Claude Code can run arbitrary shell commands, safety practices matter:

- Run Claude Code in containers / VMs for risky tasks
- Use `--allowedTools` flag to limit what tools are available per invocation
- Review the `claude-code-audit.log` for retrospective auditing
- For multi-tenant or shared environments: never run with `--dangerously-skip-permissions` on shared hosts
- Prefer `--output-format json` + programmatic parsing over screen-scraping

---

## 9. Memory and context management

Claude Code manages context across a session automatically, but there are levers:

- **`/clear`** — clears conversation history, keeps CLAUDE.md in context
- **`/compact`** — summarizes conversation to free up context, keeps working
- **Sub-agents** — each spawned subagent gets a fresh context window; use this for very long tasks that would otherwise overflow
- **Memory files** — write intermediate results to files and re-read them later; Claude handles this via normal file tools, not a special API

---

## 10. Key mental model: Claude Code as junior engineer

The framing Anthropic recommends: treat Claude Code like a skilled but literal junior engineer who:
- Executes exactly what you ask
- Needs context about the codebase and conventions
- Benefits from explicit review checkpoints
- Should be given small, verifiable tasks rather than open-ended mandates

The more structure you provide upfront, the better the outputs. Ambiguity in the prompt compounds into ambiguity in the code.

---

## Quotes / key claims

- "CLAUDE.md files are automatically loaded into context at session start — they're the primary lever for persistent configuration."
- "Claude can spawn subagents via Task tool calls. Each subagent has its own context window and runs in parallel."
- "Headless mode (`-p`) lets Claude Code run as part of CI pipelines and git hooks."
- "Custom slash commands live in `.claude/commands/` and are version-controlled alongside the code."
- "For maximum safety: run Claude Code in a container, use `--allowedTools`, review the audit log."
- "Think of Claude Code as a very literal, very capable intern. The more structure you provide, the better."
