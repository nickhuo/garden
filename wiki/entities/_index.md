---
type: meta
title: "Entities Index"
updated: 2026-05-22
---

# Entities

Named things: people, organizations, products, repositories, frameworks, places. 3 entities added 2026-05-20 ([[Andrej Karpathy]], [[Richard Sutton]], [[Letta]]).

## Organizations

- [[brain/03_Resources/wiki/entities/Anthropic]] — AI safety company; dominant source author in this wiki (8+ sources). **Cited in:** all Anthropic-tagged sources.
- [[Sierra]] — customer-service-agent company (Bret Taylor, Clay Bavor). **Cited in:** [[2024-06-17 - Yao et al - tau-bench]].
- [[Thinking Machines Lab]] — AI research lab; publishes the *Connectionism* blog. 5 sources. Themes: numerical foundations, optimization theory, post-training, real-time architecture. Authors covered: Schulman, He, Lu, Bernstein.
- [[Gorilla]] — UC Berkeley (Patil, Stoica, Gonzalez) tool-use project; produced the Gorilla model, APIBench, and [[BFCL]]. **Cited in:** [[2025-07 - Patil et al - BFCL]].
- [[OpenBMB]] — Tsinghua NLP / ModelBest open big-model ecosystem; maintains [[ToolBench]]/ToolLLM. **Cited in:** [[2023-07-31 - Qin et al - ToolLLM]].
- [[OpenAI]] — AI research & deployment company; maker of GPT/o-series, the Agents SDK, the moderation API. **Cited in:** [[2025 - OpenAI - A Practical Guide to Building Agents]].
- [[Prime Intellect]] — open-source / decentralized RL company focused on **self-improving AI systems**; ships `prime-rl`, `verifiers`, `renderers`, `general-agent`; runs the Prime Sprints program. 5 sources. **Cited in:** the Prime Intellect batch (reward-hacking, general-agent, auto-nanogpt, renderers, RLM). Peer to [[Thinking Machines Lab]].
- [[DeepSeek]] — Chinese AI lab (DeepSeek-AI); open-weight frontier models, popularized [[GRPO]] + large-scale [[RL with Verifiable Rewards|RLVR]] for reasoning. DeepSeek-V3 (671B MoE base) → [[DeepSeek-R1-Zero]] / DeepSeek-R1 / R1-Distill series. **Cited in:** [[2025-01 - DeepSeek-AI - DeepSeek-R1 Incentivizing Reasoning via RL]].

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
- [[BFCL]] — Berkeley Function Calling Leaderboard; de facto function-calling standard, AST-based grading. **Cited in:** [[2025-07 - Patil et al - BFCL]].
- [[ToolBench]] — Tsinghua/OpenBMB tool-use dataset+benchmark over 16k+ real APIs; ToolLLaMA + ToolEval. **Cited in:** [[2023-07-31 - Qin et al - ToolLLM]].
- [[Letta]] — agent framework built from MemGPT; productizes self-editing memory. **Cited in:** [[2023-10-12 - Packer et al - MemGPT - LLMs as Operating Systems]].
- [[OpenAI Agents SDK]] — OpenAI's code-first agent orchestration framework: `Agent`, `Runner.run()`, handoffs, first-class guardrails. **Cited in:** [[2025 - OpenAI - A Practical Guide to Building Agents]].

## People

- [[John Schulman]] — TML researcher; lead author of [[2025-09-29 - Schulman - LoRA Without Regret]]. Background: PPO, TRPO.
- [[Horace He]] — TML researcher; lead author of [[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]]. Background: PyTorch internals, GPU kernels.
- [[Kevin Lu]] — TML researcher; lead author of [[2025-10-27 - Lu - On-Policy Distillation]].
- [[Jeremy Bernstein]] — TML researcher; author of [[2025-09-26 - Bernstein - Modular Manifolds]]. Background: geometric/manifold optimization (Modula project).
- [[Andrej Karpathy]] — author of [[2017-11-11 - Karpathy - Software 2.0]]; the model-centric / "neural nets eat code" framing.
- [[Richard Sutton]] — author of [[2019-03-13 - Sutton - The Bitter Lesson]] and co-author of [[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]; RL pioneer, the scaling-over-hand-engineering argument.

## Agentic coding (2026-05-24)

- [[Geoffrey Huntley]] — engineer/blogger; coined the [[Ralph Loop]]; "agentic coding is context engineering, not multi-agent." (His "Weaving Loom" / Gas Town automation-levels framing is covered inline on [[Ralph Loop]].)

## Promotion policy

Create an entity page when:
- The entity is mentioned substantively in ≥2 sources, OR
- The entity is the subject of its own dedicated source (e.g., a tool's docs)

Don't create entity pages for:
- One-line mentions
- Authors of single sources (info lives in the source frontmatter)
- Generic categories ("LLMs," "agents") — those are concepts, not entities
