---
type: meta
title: "Concepts Index"
updated: 2026-05-14
---

# Concepts

Ideas, patterns, frameworks. Domain-agnostic in form, domain-tagged in content. **67 concept pages** currently.

## Architecture and primitives

- [[Augmented LLM]] — the base primitive: an LLM call enhanced with retrieval, tools, memory
- [[ACI - Agent-Computer Interface]] — tools-for-LLMs deserve the same engineering investment as HCI
- [[MCP]] — see also entity page

## Retrieval (RAG)

- [[Contextual Retrieval]] — prepend AI-generated context blurbs to chunks before embedding; -67% retrieval failures combined
- [[BM25 and Hybrid Retrieval]] — sparse + dense fusion via Reciprocal Rank Fusion
- [[Reranking]] — cross-encoder post-retrieval scoring for precision

## Workflow patterns

- [[Prompt Chaining]]
- [[Routing]]
- [[Parallelization]]
- [[Orchestrator-Workers]]
- [[Evaluator-Optimizer]]
- [[Workflows vs Agents]]

## Agent patterns

- [[Autonomous Agents]]
- [[Multi-Agent Systems]]
- [[Agent Interface Contracts]] — orchestrator-defined specs enabling isolated parallel worker agents; interface quality is the bottleneck
- [[Agentic Harness]] — minimal scaffold wrapping an LLM for agentic behavior; simplicity finding from SWE-bench Verified

## Harness design

- [[Meta-Harness]] — Anthropic's Brain/Hands/Session hosting abstraction above harness implementations
- [[Harness Design Patterns]] — catalog of production patterns and anti-patterns for long-running agent harnesses
- [[Harness Staleness]] — Bitter Lesson applied to harnesses: assumptions about model limits go stale as models improve
- [[Context Anxiety]] — harness-induced model behavior when context resets approach; coping behaviors that hurt task quality

## Context engineering

- [[Context Engineering]]
- [[Just-in-Time Context Retrieval]]
- [[Long-Horizon Context Management]]
- [[Context Decomposition vs Problem Decomposition]]
- [[Context Assembly Pipeline]] — staged construction of agent context (system → retrieval → message history → tools); composable, testable, replayable
- [[Recitation]]
- [[Session as Event Log]]
- [[Error Trace Retention]]
- [[Few-Shot Drift]]
- [[KV-Cache Discipline]]
- [[Cache Invalidation Cascade]] — chains of invalidations triggered by mid-trajectory tool/prompt mutations; partner concept to KV-Cache Discipline
- [[Token Economics]]

## Safety and permissions

- [[Permission Classifier]] — inference-time classifier routing tool calls to auto-approve / review / block based on semantic risk; powers Claude Code auto mode
- [[Minimal Footprint Principle]] — prefer reversible actions, do less when uncertain, avoid unrequested side effects; operationalized in Permission Classifier
- [[Agent Sandboxing]] — OS-level isolation (macOS Seatbelt, Linux seccomp/namespaces) for hard-floor enforcement of filesystem and network policy; enables headless autonomy
- [[Permission Model]] — prompt-based trust vs policy-based trust; layered model (OS sandbox > safety training > user grants)
- [[Prompt Injection]] — attack where malicious environment content hijacks agent actions; sandboxing as blast-radius control

## Tool use

- [[Tool Use Examples]]
- [[Tool Search Tool]]
- [[Programmatic Tool Calling]]
- [[Logit Masking]]
- [[Think Tool]] — no-op scratchpad tool for explicit in-loop reasoning during agentic tasks
- [[Progressive Disclosure]] — manifest-first, load-on-demand: skills/tools register presence cheaply, load fully when needed

## Evaluation

- [[LLM-as-Judge Evaluation]]
- [[Pass^k Reliability Metric]]
- [[User Simulator Evaluation]]
- [[Agent Eval Pyramid]] — three-tier eval strategy (unit tests → LLM judge → simulated-user E2E)
- [[Trace-Based Evaluation]] — structured execution log enabling post-hoc failure attribution
- [[AI-Resistant Evaluation Design]] — designing evals robust to AI assistance; same proxy-gaming failure mode as LLM benchmarks
- [[AI Tool Fluency]] — treating critical/verified AI use as a first-class engineering competency
- [[Eval Infrastructure Noise]] — environment-induced variance in agentic evals (network, containers, flaky tests); sets a floor on measurable pass^k
- [[Eval Awareness]] — models detecting evaluation context and behaving differently than at runtime
- [[Sandbagging]] — specifically suppressing capability under evaluation; subset of eval awareness

## Agentic coding

- [[CLAUDE.md]] — auto-loaded config primitive for Claude Code sessions; the persistent-context lever
- [[Agentic Coding Slash Commands]] — `.claude/commands/` reusable prompt templates, version-controlled
- [[Config Type Safety]] — typed config schemas (Zod, Pydantic) at the agent boundary; eliminate a class of silent agent failures

## LLM post-training & fine-tuning

- [[LoRA]] — low-rank adaptation; matches FullFT when applied to all layers, at moderate batch sizes, within capacity. Rank-1 suffices for policy-gradient RL.
- [[On-Policy Distillation]] — student rollouts + teacher per-token reverse-KL; 9-30x cost reduction vs SFT/RL.
- [[Reverse KL Divergence]] — mode-seeking, "unhackable"; the supervision signal in on-policy distillation.
- [[Empirical Neural Tangent Kernel]] — explains why LoRA needs all layers (MLP gradients dominate the kernel).

## LLM inference & numerics

- [[Batch Invariance]] — kernel property: output is identical regardless of batch size. Required for deterministic inference.
- [[Floating-Point Non-Associativity]] — $(a+b)+c \neq a+(b+c)$ in finite precision. Prerequisite, not culprit, for nondeterminism.
- [[Trainer-Sampler Determinism]] — bitwise sampler/trainer match; enables true on-policy RL. Used in interaction models as a stability tool.

## Optimization theory

- [[Manifold Optimization]] — constrain weights to submanifolds + co-design optimizer; principled per-layer LR budgets.
- [[Stiefel Manifold]] — matrices with orthonormal columns; bounds operator norm.
- [[Manifold Muon]] — Muon variant retracting onto the Stiefel manifold; beats AdamW on small CIFAR-10.

## Real-time / multimodal architecture

- [[Interaction Model Architecture]] — 200ms micro-turn streaming + background-model split; interactivity as a model-level property, not interface retrofit.

## Other

- [[Recursive Language Models]]

## Promotion policy

Create a concept page when:
- A pattern, framework, or named idea appears substantively in ≥1 source AND is reused or referenced elsewhere
- The concept needs a stable name for cross-references

Don't create concept pages for:
- One-off terminology in a single source (cite inline in the source page)
- Generic words ("data," "context" without modifier) — those need narrowing
