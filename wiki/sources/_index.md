---
type: meta
title: "Sources Index"
updated: 2026-05-14
---

# Sources

One summary page per ingested source. Body cites verbatim where load-bearing; synthesis lives on entity/concept pages. **31 sources** currently.

## Chronological (newest first)

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
- [[2025-06-26 - Anthropic - Desktop Extensions]]
- [[2025-06-13 - Anthropic - How we built our multi-agent research system]]
- [[2025-03-20 - Anthropic - The Think Tool]]
- [[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]]
- [[2024-12-19 - Anthropic - Building Effective Agents]]
- [[2024-09-19 - Anthropic - Contextual Retrieval]]
- [[2024-06-17 - Yao et al - tau-bench]]

## By author

### Anthropic (23)

Foundational corpus for the AI-Agents domain. Framing started with [[Building Effective Agents]] (Dec 2024) and the workflow/agent taxonomy. The May-2026 batch added 17 posts spanning eval validity ([[Demystifying evals for AI agents]], [[AI-Resistant Technical Evaluations]], [[Eval Awareness BrowseComp]], [[Infrastructure Noise Agentic Coding Evals]]), harness design ([[Effective Harnesses for Long-Running Agents]], [[Harness Design Long Running Apps]], [[Scaling Managed Agents]]), MCP token economics ([[Code Execution with MCP]], [[Advanced Tool Use]], [[Desktop Extensions]]), Claude Code ergonomics ([[Claude Code Auto Mode]], [[Claude Code Sandboxing]], [[Claude Code Best Practices]], [[Agent Skills]]), and the Postmortem of Three Recent Issues.

### Manus (1)

Single source from a 2nd-tier player; useful as a sanity check against Anthropic's framing on context engineering and KV-cache discipline.

### Sierra (1)

[[2024-06-17 - Yao et al - tau-bench]] — only reliability-focused (vs capability-focused) source; introduces [[Pass^k Reliability Metric]].

### Academic (1)

[[2025-10 - Zhang Khattab - Recursive Language Models]] — only academic paper in the corpus.

### Thinking Machines Lab (5)

First non-Anthropic systematic corpus. All from the *Connectionism* blog, Sep 2025 – May 2026. Coverage: inference numerics ([[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]]), optimization theory ([[2025-09-26 - Bernstein - Modular Manifolds]]), parameter-efficient fine-tuning ([[2025-09-29 - Schulman - LoRA Without Regret]]), post-training ([[2025-10-27 - Lu - On-Policy Distillation]]), real-time multimodal architecture ([[2026-05-11 - Thinking Machines - Interaction Models]]). Seeds the [[LLM]] domain.

## Coverage gaps

- No OpenAI sources yet (their agent work since 2024 is underrepresented).
- No DeepMind / Google sources.
- No third-party sources on MCP — corpus is entirely Anthropic's own framing.
- No critical/contrarian sources — corpus skews toward "agent boosters" (τ-bench partially closes this).
- No non-Anthropic harness postmortems.
- LLM domain is single-lab (TML only) — Karpathy materials still untouched.

## Raw-source links

Each source page's frontmatter has a `sources:` entry pointing to its corresponding `.raw/articles/<filename>.md`. Don't edit raw files — they're immutable per WIKI.md.
