---
source: https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start
title: "How Claude Code works in large codebases: Best practices and where to start"
author: Anthropic Applied AI
date_published: 2026-05-14
captured: 2026-05-18
---

# How Claude Code works in large codebases: Best practices and where to start

**Author(s):** Anthropic Applied AI team — Alon Krifcher, Charmaine Lee, Chris Concannon, Harsh Patel, Henrique Savelli, Jason Schwartz, Jonah Dueck, Kirby Kohlmorgen. Feedback from Amit Navindgi (Zoox).

Claude Code is operating in production across massive monorepos, legacy systems spanning decades, distributed architectures with dozens of repositories, and organizations employing thousands of developers. These environments present distinctive challenges absent in smaller codebases—build commands varying across subdirectories, legacy code scattered without shared root structures.

"Large codebase" encompasses monorepos containing millions of lines, legacy systems built over decades, dozens of microservices across separate repositories, or combinations thereof. This includes languages not typically associated with AI coding tools — C, C++, C#, Java, PHP — where Claude Code demonstrates stronger performance than many teams anticipate, particularly following recent model improvements.

## How Claude Code navigates large codebases

Claude Code navigates codebases similarly to software engineers: it traverses file systems, reads files, uses grep for precise discovery, and traces references across repositories. Operations occur locally on developers' machines without requiring built, maintained, or uploaded codebase indices.

RAG-powered AI coding tools embed entire codebases and retrieve relevant chunks during queries. At scale, these systems fail because embedding pipelines cannot keep pace with active engineering teams. By query time, the index reflects outdated codebase states — weeks, days, or even hours old. Retrieval might return recently renamed functions or reference deleted modules without indicating staleness.

Agentic search avoids these failure modes. No embedding pipeline or centralized index requires maintenance as thousands of engineers commit new code. Each developer's instance operates from the live codebase.

However, this requires sufficient starting context for Claude to know where to look. Navigation quality depends on codebase organization, utilizing CLAUDE.md files and skills for context layering. Requesting vague patterns across billion-line codebases triggers context-window limitations before work begins. Teams investing in codebase setup observe superior results.

## The harness matters as much as the model

A widespread misconception holds that Claude Code capabilities derive solely from the model. The surrounding ecosystem — the harness — determines Claude Code performance more than the model alone.

The harness comprises five extension points — **CLAUDE.md files, hooks, skills, plugins, and MCP servers** — each serving distinct functions. Configuration order matters, as each layer builds upon previous ones. LSP integrations and subagents provide additional capabilities.

**CLAUDE.md files come first.** These context files load automatically at session start: root files for overviews, subdirectory files for local conventions. Since they load every session regardless of task, keeping them focused on broadly applicable information prevents performance degradation.

**Hooks make setup self-improving.** Teams typically view hooks as scripts preventing errors, but continuous improvement represents higher value. Stop hooks can reflect on session events and propose CLAUDE.md updates while context remains fresh. Start hooks load team-specific context dynamically so every developer receives appropriate setup for their module without manual configuration. For automated checks like linting and formatting, hooks enforce rules deterministically, producing more consistent results than relying on Claude's memory.

**Skills keep relevant expertise available on-demand without bloating every session.** Large codebases with dozens of task types don't require all expertise present simultaneously. Skills solve this through progressive disclosure, offloading specialized workflows and domain knowledge competing for context space, loading only when tasks call for them. Skills can scope to specific paths, activating only in relevant codebase sections. Teams owning payments services can bind deployment skills to those directories, preventing auto-loading when working elsewhere in monorepos.

**Plugins distribute working solutions.** A challenge in large codebases involves keeping good setups from remaining tribal. Plugins bundle skills, hooks, and MCP configurations into single installable packages, so new engineers immediately access the same context and capabilities as experienced users. Plugin updates distribute across organizations through managed marketplaces. Example: a large retail organization built skills connecting Claude to internal analytics platforms, enabling business analysts to retrieve performance data without leaving workflows. They distributed it as plugins before broad rollout.

**Language server protocol (LSP) integrations give Claude the same navigation developers possess in IDEs.** Most large-codebase IDEs already run LSP instances, powering "go to definition" and "find all references" features. Surfacing this to Claude provides symbol-level precision: following function calls to definitions, tracing references across files, distinguishing identically named functions across languages. Without it, Claude pattern-matches text, potentially landing on wrong symbols. One enterprise software company deployed LSP integrations organization-wide before Claude Code rollout specifically for reliable C and C++ navigation at scale. For multi-language codebases, this is one of the highest-value investments.

**MCP servers extend everything.** MCP servers connect Claude to internal tools, data sources, and APIs otherwise unreachable. Sophisticated teams built MCP servers exposing structured search as directly callable tools. Others connect Claude to internal documentation, ticketing systems, or analytics platforms.

**Subagents split exploration from editing.** Subagents are isolated Claude instances with separate context windows taking tasks, performing work, and returning final results to parents. Once harness implementation completes, teams sometimes spin up read-only subagents mapping subsystems and writing findings to files, then have main agents edit with complete pictures.

## Configuration patterns from successful deployments

### Making the codebase navigable at scale

Claude's effectiveness bounds with its ability to locate appropriate context. Excessive context loaded into every session degrades performance; insufficient context leaves Claude navigating blind.

- **Keep CLAUDE.md files lean and layered.** Claude loads them additively as it moves through codebases: root files for big pictures, subdirectory files for local conventions. Root files should contain pointers and critical gotchas only.
- **Initialize in subdirectories, not repo roots.** Claude performs best when scoped to relevant codebase sections. Claude automatically walks up directory trees, loading every CLAUDE.md file discovered along the way, so root context never disappears.
- **Scope test and lint commands per subdirectory.** Running full suites when Claude changed single services causes timeouts and wastes context on irrelevant output. In compiled-language monorepos with deep cross-directory dependencies, per-subdirectory scoping proves harder and may require project-specific build configurations.
- **Use `.claudeignore` files** excluding generated files, build artifacts, and third-party code. Committing `permissions.deny` rules in `.claude/settings.json` means exclusions are version-controlled. Code generator developers can override project-level exclusions locally.
- **Build codebase maps when directory structures don't provide sufficient guidance.** Lightweight markdown files at repo roots listing top-level folders with one-line descriptions give Claude scannable tables of contents before opening files. For codebases with hundreds of top-level folders, layered approaches work best.
- **Run LSP servers for symbol searching instead of string searching.** Grepping common function names in large codebases returns thousands of matches, burning context. LSP returns only references pointing to identical symbols, filtering before Claude reads anything.

### Actively maintaining CLAUDE.md files as model intelligence evolves

As models progress, instructions written for current models can hinder future ones. Example: CLAUDE.md rules directing Claude to break refactors into single-file changes may have guided earlier models but would prevent newer ones from handling coordinated cross-file edits well.

Skills and hooks compensating for specific model limitations become overhead when limitations disappear. Hooks intercepting file writes to enforce `p4 edit` in Perforce codebases became redundant once Claude Code added native Perforce support.

Teams should perform meaningful configuration reviews every three to six months, particularly following major model releases when performance plateaus.

### Assigning ownership for Claude Code management and adoption

Fastest-spreading rollouts had dedicated infrastructure investments preceding broad access. Small teams — sometimes single individuals — wired tooling so Claude already fit developer workflows upon first contact.

Teams performing this work typically sit under developer experience or developer productivity functions. Several organizations have emerging "agent manager" roles: hybrid PM/engineer functions managing Claude Code ecosystems. For organizations without dedicated teams, minimum viable approaches involve single DRI individuals owning Claude Code configuration, with authority over settings, permissions policies, plugin marketplaces, and CLAUDE.md conventions.

Bottoms-up adoption generates enthusiasm but fragments without centralization. Individuals or teams must assemble and evangelize appropriate Claude Code conventions.

Large organizations, especially regulated industries, raise governance questions early: who controls available skills and plugins, how to prevent thousands of engineers independently rebuilding identical items, how to ensure AI-generated code undergoes same review processes as human-generated code. Smooth deployments establish cross-functional working groups early, bringing engineering, information security, and governance representatives together.

## Applying these patterns

Claude Code targets conventional software engineering environments where engineers are primary codebase contributors, repositories use Git, and code follows standard directory structures. Non-traditional setups — game engines with large binary assets, unconventional version control, non-engineers contributing — require additional configuration.
