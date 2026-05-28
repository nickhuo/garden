---
type: source
title: "How Claude Code works in large codebases: Best practices and where to start"
created: 2026-05-18
updated: 2026-05-18
tags:
  - ai-agents
  - claude-code
  - coding
  - enterprise
status: developing
source_type: article
author: Anthropic Applied AI
date_published: 2026-05-14
url: https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start
confidence: high
related:
  - "[[Claude Code]]"
  - "[[brain/CLAUDE]]"
  - "[[Agent Skills]]"
  - "[[Agentic Harness]]"
  - "[[MCP]]"
  - "[[Context Engineering]]"
  - "[[2026-05-13 - Anthropic - Claude Code Best Practices]]"
sources:
  - "[[.raw/articles/2026-05-14 - Anthropic - Claude Code in Large Codebases.md]]"
key_claims:
  - Agentic search beats RAG at scale because embedding pipelines can't keep up with active engineering teams — index staleness causes silent retrieval errors
  - The harness (CLAUDE.md, hooks, skills, plugins, MCP) determines Claude Code performance more than the model alone
  - "Hooks compound: stop hooks reflect on sessions and propose CLAUDE.md updates while context is fresh; start hooks load team-specific context dynamically"
  - Skills should scope to paths — payments-team deployment skills bind to that directory, not the whole monorepo
  - Initialize Claude in subdirectories, not repo roots — it walks up the tree loading every CLAUDE.md it finds
  - LSP integration is one of the highest-value investments for multi-language large codebases (symbol-level vs string-level navigation)
  - Configuration reviews every 3-6 months — instructions that helped older models can hinder newer ones (e.g., 'one-file-at-a-time' refactor rules)
  - "Adoption needs a DRI: fastest rollouts had infrastructure wired before broad access; bottoms-up fragments without centralization"
---

# How Claude Code Works in Large Codebases

Anthropic Applied AI's field report on Claude Code deployments across monorepos, decades-old legacy systems, and thousands-of-engineer organizations. Successor / scale-out companion to [[2026-05-13 - Anthropic - Claude Code Best Practices]] — the earlier post is the general "how to use Claude Code" manual, this one is what changes when the codebase is large.

## Summary

Two through-lines.

**(1) Agentic search > RAG at scale.** Claude Code reads files, greps, and traces references the way a human engineer does — no embedding pipeline, no centralized index. This is a feature, not a limitation: RAG-based coding tools fail in active codebases because the index is always stale relative to live HEAD, and retrieval silently returns renamed/deleted symbols. The tradeoff: Claude needs *enough starting context* (CLAUDE.md, skills, codebase maps) to know where to look. Without scaffolding, billion-line codebases blow the context window before work starts.

**(2) The harness is more load-bearing than the model.** Five extension points — [[brain/CLAUDE]], hooks, [[Agent Skills|skills]], plugins, [[MCP]] servers — plus LSP and subagents. Configuration order matters. Performance gains from harness work often exceed gains from model upgrades.

## Key Claims

### Agentic search vs RAG
- RAG embedding pipelines can't keep pace with thousands of engineers committing code. By query time the index is hours-to-weeks stale. Retrieval returns renamed functions or deleted modules *without flagging staleness* — silent failure mode.
- Agentic search has no centralized index to maintain. Each developer's instance runs against live HEAD.
- Cost: Claude needs the codebase to be *legible* — directory structure, CLAUDE.md hierarchy, skills, and maps determine navigation quality. Vague prompts across billion-line monorepos exhaust context before useful work begins.

### Harness layering (in dependency order)
1. **CLAUDE.md** — auto-loaded every session. Keep lean: root files for pointers and gotchas only; subdirectory files for local conventions. Claude walks up the tree, so initializing *in a subdirectory* (not repo root) is the right default in monorepos.
2. **Hooks** — the underused layer. Beyond linting/formatting enforcement, **stop hooks can propose CLAUDE.md updates** while session context is still warm. Start hooks can dynamically load team-specific context. Hooks > model memory for deterministic rules.
3. **Skills** — progressive disclosure. Path-scoping is the key feature at scale: bind deployment skills to `services/payments/`, not the whole monorepo. Prevents auto-loading from polluting unrelated work.
4. **Plugins** — bundle skills + hooks + MCP into a single installable. The mechanism that keeps good setups from staying tribal. Distributes through managed marketplaces.
5. **MCP servers** — structured search exposed as callable tools; bridges to docs, tickets, analytics.

Plus:
- **LSP integration** — symbol-level navigation (go-to-def, find-references) replacing grep's text-level pattern matching. Called out as *one of the highest-value investments* for multi-language codebases. One enterprise customer rolled out LSP org-wide *before* Claude Code rollout for reliable C/C++ navigation.
- **Subagents** — split exploration from editing. Read-only subagents map subsystems and write findings to files; main agent edits with a complete picture. Context-isolation pattern.

### Configuration patterns
- `.claudeignore` + `permissions.deny` in `.claude/settings.json` should be version-controlled so the whole team gets identical noise reduction. Local overrides for code-generator developers.
- Lightweight markdown "codebase maps" at repo roots — top-level folders with one-line descriptions — give Claude a scannable TOC before opening files. Layer them when there are hundreds of folders.
- Scope test/lint commands per subdirectory in service-oriented monorepos. Harder in compiled-language monorepos with deep cross-directory deps.

### Maintenance discipline
- CLAUDE.md instructions tuned for an older model can actively hinder a newer one. Example called out: "break refactors into single-file changes" — useful guidance for earlier models, prevents newer ones from doing coordinated cross-file edits.
- Hooks compensating for model limitations become overhead when those limitations disappear. Anthropic cites the `p4 edit` Perforce interception hooks becoming redundant after native Perforce support shipped.
- **Cadence: review configuration every 3-6 months, especially after major model releases.** This is the [[Harness Staleness]] argument applied to Claude Code config specifically.

### Adoption
- Fastest-spreading rollouts had **infrastructure wired before broad access** — a small team or single DRI got plugins, MCP, CLAUDE.md hierarchies, and onboarding ready so day-one developers had productive sessions.
- Without centralization, bottoms-up adoption fragments and plateaus. Knowledge stays tribal.
- "Agent manager" role emerging in larger orgs — hybrid PM/engineer owning the Claude Code ecosystem. Minimum viable: one DRI with authority over settings, permissions policies, plugin marketplaces, and CLAUDE.md conventions.
- Regulated industries: cross-functional working groups (eng + infosec + governance) early.

## Entities Mentioned

- [[Claude Code]] — primary subject
- [[brain/03_Resources/digest/sources/anthropic]] — Applied AI team is the author
- [[MCP]] — one of the five harness extension points

## Concepts Touched

- [[brain/CLAUDE]] — layering and subdirectory-first initialization explicitly recommended
- [[Agent Skills]] — path-scoping called out as the key feature at scale
- [[Agentic Harness]] — this post is a direct case study of the harness concept
- [[Agentic Harness]] — the 5-layer extension model
- [[Harness Staleness]] — 3-6 month review cadence as the operational discipline
- [[Context Engineering]] — codebase legibility is context engineering at the repo-architecture level
- [[Just-in-Time Context Retrieval]] — agentic search is exactly this pattern applied to source code
- [[Meta-Harness]] — stop hooks proposing CLAUDE.md updates *is* a meta-harness loop

## New Concept Candidates

These aren't yet in the wiki but are first-class ideas in this post — promote on second-source citation:
- **Agentic search vs RAG for code** — could be a comparison page if a second source treats it explicitly
- **LSP-augmented agentic coding** — symbol-level vs string-level navigation as a discrete capability tier
- **Path-scoped skills** — the specific pattern of binding a skill to a directory subtree
- **Skill / hook obsolescence** — generalization of the Perforce example: harness compensations that should be retired

## Relationship to Existing Wiki

- Direct successor to [[2026-05-13 - Anthropic - Claude Code Best Practices]]. The earlier post is "how to use Claude Code"; this one is "what changes at enterprise scale." Together they form the canonical Anthropic guidance pair.
- Reinforces [[Harness Staleness]] with a concrete cadence (3-6 months) and a concrete failure mode (old refactor-decomposition rules constraining newer models).
- The agentic-search-vs-RAG framing connects to [[Contextual Retrieval]] (Anthropic's RAG improvement work) as the inverse position: for *active* codebases, skip RAG entirely.

## Assessment

High confidence — first-party Anthropic field report grounded in observed customer deployments (Zoox feedback acknowledged). Practical, opinionated, and the recommendations have concrete failure modes attached.

The most non-obvious claim: **stop hooks proposing CLAUDE.md updates is the high-leverage hook pattern**, not lint enforcement. This deserves its own concept page once a second source corroborates the self-improving-setup framing.
