---
type: meta
title: "Entities Index"
updated: 2026-05-14
---

# Entities

Named things: people, organizations, products, repositories, frameworks, places.

## Organizations

- [[Anthropic]] — AI safety company; dominant source author in this wiki (8+ sources). **Cited in:** all Anthropic-tagged sources.
- [[Sierra]] — customer-service-agent company (Bret Taylor, Clay Bavor). **Cited in:** [[2024-06-17 - Yao et al - tau-bench]].
- [[Thinking Machines Lab]] — AI research lab; publishes the *Connectionism* blog. 5 sources. Themes: numerical foundations, optimization theory, post-training, real-time architecture. Authors covered: Schulman, He, Lu, Bernstein.

## Products / Frameworks / Benchmarks

- [[Agent Skills]] — Anthropic's capability-packaging primitive: versioned bundles of tools + prompt fragments + resource handles for Claude agents. **Cited in:** [[2026-05-13 - Anthropic - Agent Skills]].
- [[Claude Code]] — Anthropic's terminal-native agentic coding tool; reads codebases, edits files, runs tests, executes shell commands. **Cited in:** [[2026-04 - Anthropic - Claude Code Auto Mode]], [[2026-05-13 - Anthropic - Claude Code Best Practices]], [[2026-05-13 - Anthropic - Claude Code Sandboxing]].
- [[Claude Desktop]] — Anthropic's native desktop app; primary MCP client and DXT extension host. **Cited in:** [[2025-06-26 - Anthropic - Desktop Extensions]].
- [[DXT]] — Desktop Extensions packaging format (.dxt); one-click MCP server install for Claude Desktop. **Cited in:** [[2025-06-26 - Anthropic - Desktop Extensions]].
- [[MCP]] — Model Context Protocol; Anthropic's open standard for tool/context interfaces. **Cited in:** [[2024-12-19 - Anthropic - Building Effective Agents]], [[2025-11-24 - Anthropic - Advanced Tool Use]], [[2025-06-26 - Anthropic - Desktop Extensions]], [[2026-05-13 - Anthropic - Code Execution with MCP]], [[2026-04 - Anthropic - Claude Code Auto Mode]].
- [[Managed Agents]] — Anthropic's hosted agent-as-a-service primitive. **Cited in:** [[2026-04-08 - Anthropic - Scaling Managed Agents]], [[2026-04 - Anthropic - Claude Code Auto Mode]].
- [[Manus]] — autonomous-agent product / author of "Context Engineering for AI Agents." **Cited in:** [[2025-07-18 - Manus - Context Engineering for AI Agents]].
- [[SWE-bench]] — standard coding-agent benchmark (real GitHub issues + test suites); primary subject of infrastructure noise analysis. **Cited in:** [[2026-02-05 - Anthropic - Infrastructure Noise Agentic Coding Evals]].
- [[SWE-bench Verified]] — human-curated ~500-issue subset; higher-signal eval. 49% achieved by Anthropic with simple Claude 3.5 Sonnet scaffold. **Cited in:** [[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]].
- [[Claude 3.5 Sonnet]] — Anthropic LLM; achieved 49% on SWE-bench Verified with simple agentic harness. **Cited in:** [[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]].
- [[tau-bench]] — Sierra's tool-agent-user benchmark; introduces [[Pass^k Reliability Metric]]. **Cited in:** [[2024-06-17 - Yao et al - tau-bench]].

## People

- [[John Schulman]] — TML researcher; lead author of [[2025-09-29 - Schulman - LoRA Without Regret]]. Background: PPO, TRPO.
- [[Horace He]] — TML researcher; lead author of [[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]]. Background: PyTorch internals, GPU kernels.
- [[Kevin Lu]] — TML researcher; lead author of [[2025-10-27 - Lu - On-Policy Distillation]].
- [[Jeremy Bernstein]] — TML researcher; author of [[2025-09-26 - Bernstein - Modular Manifolds]]. Background: geometric/manifold optimization (Modula project).

## Promotion policy

Create an entity page when:
- The entity is mentioned substantively in ≥2 sources, OR
- The entity is the subject of its own dedicated source (e.g., a tool's docs)

Don't create entity pages for:
- One-line mentions
- Authors of single sources (info lives in the source frontmatter)
- Generic categories ("LLMs," "agents") — those are concepts, not entities
