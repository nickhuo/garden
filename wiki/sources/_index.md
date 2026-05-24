---
type: meta
title: "Sources Index"
updated: 2026-05-22
---

# Sources

One summary page per ingested source. Body cites verbatim where load-bearing; synthesis lives on entity/concept pages. **47 sources** currently.

## Chronological (newest first)

- [[2026-05-22 - Karpathy - Sequoia Ascent 2026]]
- [[2025 - OpenAI - A Practical Guide to Building Agents]]
- [[2026-05-13 - Anthropic - Agent Skills]]
- [[2026-05-11 - Thinking Machines - Interaction Models]]
- [[2026-05-13 - Anthropic - Claude Code Best Practices]]
- [[2026-05-13 - Anthropic - Claude Code Sandboxing]]
- [[2026-05-13 - Anthropic - Code Execution with MCP]]
- [[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]]
- [[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]]
- [[2026-05-13 - Anthropic - Eval Awareness BrowseComp]]
- [[2026-05-13 - Anthropic - Postmortem Three Recent Issues]]
- [[2026-05-13 - Anthropic - Writing Effective Tools for Agents]]
- [[2026-04 - Anthropic - Claude Code Auto Mode]]
- [[2026-04-08 - Anthropic - Scaling Managed Agents]]
- [[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]]
- [[2026-02-05 - Anthropic - Infrastructure Noise Agentic Coding Evals]]
- [[2026-01-21 - Anthropic - AI-Resistant Technical Evaluations]]
- [[2025-11-24 - Anthropic - Advanced Tool Use]]
- [[2025-10-27 - Lu - On-Policy Distillation]]
- [[2025-10 - Zhang Khattab - Recursive Language Models]]
- [[2025-10-01 - Anthropic - Harness Design Long Running Apps]]
- [[2025-09-29 - Schulman - LoRA Without Regret]]
- [[2025-09-29 - Anthropic - Effective context engineering for AI agents]]
- [[2025-09-26 - Bernstein - Modular Manifolds]]
- [[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]]
- [[2025-07-18 - Manus - Context Engineering for AI Agents]]
- [[2025-07 - Patil et al - BFCL]]
- [[2025-06-26 - Anthropic - Desktop Extensions]]
- [[2025-06-13 - Anthropic - How we built our multi-agent research system]]
- [[2025-03-20 - Anthropic - The Think Tool]]
- [[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]]
- [[2024-12-19 - Anthropic - Building Effective Agents]]
- [[2024-09-19 - Anthropic - Contextual Retrieval]]
- [[2024-06-17 - Yao et al - tau-bench]]
- [[2023-07-31 - Qin et al - ToolLLM]]

## Continual learning research (added 2026-05-20)

12 sources from the continually-learning model-centric systems autoresearch pass:

- [[2017-11-11 - Karpathy - Software 2.0]]
- [[2019-03-13 - Sutton - The Bitter Lesson]]
- [[2022-03-04 - Ouyang et al - InstructGPT]]
- [[2023-04-07 - Park et al - Generative Agents]]
- [[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]]
- [[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]]
- [[2023-10-12 - Zou et al - Representation Engineering]]
- [[2024-04-17 - Agarwal et al - Many-Shot In-Context Learning]]
- [[2025-04-11 - Silver Sutton - Welcome to the Era of Experience]]
- [[2025-04-28 - Mem0 - Scalable Long-Term Memory]]
- [[2025-05-21 - Meta - Reinforcement Learning from User Feedback]]
- [[2025-07-29 - Chen et al - Persona Vectors]]

## By author

### Anthropic (23)

Foundational corpus for the AI-Agents domain. Framing started with [[Building Effective Agents]] (Dec 2024) and the workflow/agent taxonomy. The May-2026 batch added 17 posts spanning eval validity ([[Demystifying evals for AI agents]], [[AI-Resistant Technical Evaluations]], [[Eval Awareness BrowseComp]], [[Infrastructure Noise Agentic Coding Evals]]), harness design ([[Effective Harnesses for Long-Running Agents]], [[Harness Design Long Running Apps]], [[Scaling Managed Agents]]), MCP token economics ([[Code Execution with MCP]], [[Advanced Tool Use]], [[Desktop Extensions]]), Claude Code ergonomics ([[Claude Code Auto Mode]], [[Claude Code Sandboxing]], [[Claude Code Best Practices]], [[Agent Skills]]), and the Postmortem of Three Recent Issues.

### Manus (1)

Single source from a 2nd-tier player; useful as a sanity check against Anthropic's framing on context engineering and KV-cache discipline.

### Sierra (1)

[[2024-06-17 - Yao et al - tau-bench]] — only reliability-focused (vs capability-focused) source; introduces [[Pass^k Reliability Metric]].

### Academic (3)

- [[2025-10 - Zhang Khattab - Recursive Language Models]] — context-handling academic paper.
- [[2025-07 - Patil et al - BFCL]] — UC Berkeley/[[Gorilla]], ICML 2025; the function-calling benchmark standard.
- [[2023-07-31 - Qin et al - ToolLLM]] — Tsinghua/[[OpenBMB]], ICLR'24; [[ToolBench]] over 16k+ APIs. Forms a tool-use benchmark cluster with τ-bench and BFCL ([[Tool-Use Benchmarks - BFCL vs tau-bench vs ToolBench]]).

### Thinking Machines Lab (5)

First non-Anthropic systematic corpus. All from the *Connectionism* blog, Sep 2025 – May 2026. Coverage: inference numerics ([[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]]), optimization theory ([[2025-09-26 - Bernstein - Modular Manifolds]]), parameter-efficient fine-tuning ([[2025-09-29 - Schulman - LoRA Without Regret]]), post-training ([[2025-10-27 - Lu - On-Policy Distillation]]), real-time multimodal architecture ([[2026-05-11 - Thinking Machines - Interaction Models]]). Seeds the [[LLM]] domain.

## Prime Intellect (2026-05-24)

Five blog posts from [[Prime Intellect]] (Jan–May 2026), one open-source self-improvement stack — synthesis [[Prime Intellect Self-Improvement Stack]]. Second non-Anthropic, non-TML voice; first sustained **open-RL / self-improving** corpus.
- [[2026-05-20 - Prime Intellect - Systematic Reward Hacking]] (Jessica Li) — reward hacking as gradient-budget dynamics
- [[2026-05-18 - Prime Intellect - General Agent]] (Mika) — self-evolving synthetic agent environment
- [[2026-05-14 - Prime Intellect - Autonomous AI Research for nanogpt Speedrun]] — autonomous research agents beat human baseline
- [[2026-05-12 - Prime Intellect - Renderers]] — token-level templating for agentic RL
- [[2026-01-01 - Prime Intellect - Recursive Language Models]] (Sebastian) — RLM implementation; 2nd source for [[Recursive Language Models]]

## Coverage gaps

- No OpenAI sources yet (their agent work since 2024 is underrepresented).
- No DeepMind / Google sources.
- No third-party sources on MCP — corpus is entirely Anthropic's own framing.
- No critical/contrarian sources — corpus skews toward "agent boosters" (τ-bench partially closes this).
- ~~Tool-use benchmarks under-covered~~ — closed 2026-05-22 with [[BFCL]] + [[ToolBench]] joining [[tau-bench]]; see [[Tool-Use Benchmarks - BFCL vs tau-bench vs ToolBench]].
- No non-Anthropic harness postmortems.
- ~~LLM domain is single-lab (TML only)~~ — partially closed 2026-05-24 ([[Prime Intellect]] adds open-RL reward/infra sources). Karpathy materials still untouched.

## Raw-source links

Each source page's frontmatter has a `sources:` entry pointing to its corresponding `.raw/articles/<filename>.md`. Don't edit raw files — they're immutable per WIKI.md.
