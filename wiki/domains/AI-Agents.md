---
type: domain
title: AI-Agents
created: 2026-05-04
updated: 2026-05-20
tags:
- ai-agents
- domain
status: developing
related: []
sources: []
---

# AI Agents — Overview

A 60-second read of "what does this wiki think about AI Agents." See [[brain/03_Resources/wiki/index]] for the full catalog and [[log]] for the timeline.

## Current shape (after 28 sources, 23 Anthropic + 1 Manus + 3 academic + 1 Sierra)

Theory / framing:
- [[2023-09-05 - Sumers et al - Cognitive Architectures for Language Agents]] (Princeton) — the [[CoALA]] framework: organizes agents by [[Agent Memory Taxonomy|memory]] (working/episodic/semantic/procedural), action space (internal vs external grounding), and decision cycle. The conceptual scaffold under the operational corpus; surveys [[ReAct]], [[Tree of Thoughts]], Voyager, Generative Agents, SayCan
- [[2023-10-12 - Packer et al - MemGPT - LLMs as Operating Systems]] (UC Berkeley) — [[MemGPT]]: context window as RAM, *virtual context management* paging data between in-context and external tiers via [[Self-Editing Memory|model-issued function calls]]. The concrete mechanism for CoALA's working↔long-term memory boundary; became Letta

Foundation:
- [[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]] (2024-10-29, Anthropic) — 49% pass@1 on [[SWE-bench Verified]] with simple [[Agentic Harness]] + [[Claude 3.5 Sonnet]]; scaffold simplicity as a capability finding
- [[2026-01-21 - Anthropic - AI-Resistant Technical Evaluations]] (2026-05-13, Anthropic) — hiring evals redesigned for AI era; [[AI-Resistant Evaluation Design]] applied to human assessment
- [[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]] (Anthropic) — [[Agent Eval Pyramid]], [[Trace-Based Evaluation]], structured methodology for measuring agent behavior
- [[2026-05-13 - Anthropic - Claude Code Best Practices]] (Anthropic) — [[Agentic Coding Slash Commands]], [[Think Tool]] usage, harness ergonomics for coding agents
- [[2026-05-13 - Anthropic - Postmortem Three Recent Issues]] (Anthropic) — three production failures decomposed into [[Cache Invalidation Cascade]], [[Config Type Safety]], [[Context Assembly Pipeline]] regressions
- [[2026-05-13 - Anthropic - Eval Awareness BrowseComp]] (Anthropic) — [[Eval Awareness]] and [[Sandbagging]] as confounds in agent benchmarks
- [[2025-03-20 - Anthropic - The Think Tool]] (Anthropic) — [[Think Tool]] as a scratchpad primitive for structured reasoning
- [[2026-05-13 - Anthropic - Writing Effective Tools for Agents]] (Anthropic) — tool authoring discipline; [[Agent Interface Contracts]], [[Progressive Disclosure]]
- [[2026-05-13 - Anthropic - Agent Skills]] (Anthropic) — skills as discoverable, composable capabilities; [[Progressive Disclosure]] applied to tool surfaces
- [[2026-05-13 - Anthropic - Claude Code Sandboxing]] (Anthropic) — [[Agent Sandboxing]], [[Permission Classifier]], [[Permission Model]]; safe execution boundaries
- [[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]] (Anthropic) — [[Harness Design Patterns]], [[Context Anxiety]], [[Harness Staleness]], [[Minimal Footprint Principle]]
- [[2026-02-05 - Anthropic - Building C Compiler with Parallel Claudes]] (Anthropic) — multi-agent coding case study; orchestrator-worker decomposition in practice
- [[2026-05-13 - Anthropic - Code Execution with MCP]] (Anthropic) — code execution as an MCP primitive; programmatic tool composition
- [[2025-06-26 - Anthropic - Desktop Extensions]] (Anthropic) — distribution layer for agent tools; packaging and discoverability
- [[2026-02-05 - Anthropic - Infrastructure Noise Agentic Coding Evals]] (Anthropic) — [[Eval Infrastructure Noise]] as a confound; extends [[Pass^k Reliability Metric]] to [[SWE-bench]]
- [[2024-06-17 - Yao et al - tau-bench]] (Sierra) — pass^k metric, user-simulator eval, 50% reliability ceiling
- [[Building Effective Agents]] (2024-12-19, Anthropic) — foundational taxonomy
- [[How we built our multi-agent research system]] (2025-06-13, Anthropic) — multi-agent carve-out + token economics
- [[2025-07-18 - Manus - Context Engineering for AI Agents]] (Manus) — six production discipline lessons
- [[Effective context engineering for AI agents]] (2025-09-29, Anthropic) — context as finite resource; [[BM25 and Hybrid Retrieval]], [[Contextual Retrieval]], [[Reranking]]
- [[2025-10 - Zhang Khattab - Recursive Language Models]] (Zhang+Khattab MIT) — RLM inference strategy
- [[2025-11-24 - Anthropic - Advanced Tool Use]] (Anthropic) — Tool Search Tool · PTC · Tool Use Examples
- [[Scaling Managed Agents]] (2026-04-08, Anthropic) — meta-harness, infra-side scaling

**Working taxonomy:**

- **Runtime layer** — [[Meta-Harness]] (e.g., [[Managed Agents]]); virtualizes Brain / Hands / [[Session as Event Log]]. [[Agentic Harness]] is the minimal-wrapping pattern; [[Harness Design Patterns]] catalogs the choices; [[Minimal Footprint Principle]] is the design north star; [[Harness Staleness]] is the failure mode when scaffolds outlive their assumptions.
- **Base primitive** — [[Augmented LLM]] (LLM + retrieval + tools + memory)
- **Central distinction** — [[Workflows vs Agents]]: code-orchestrated vs. model-orchestrated, plus [[Multi-Agent Systems]] as a parallelism+context-budget variant
- **Workflow patterns** — [[Prompt Chaining]] · [[Routing]] · [[Parallelization]] · [[Orchestrator-Workers]] · [[Evaluator-Optimizer]]
- **Agent pattern** — [[Autonomous Agents]]
- **Production discipline (Manus)** — [[KV-Cache Discipline]] · [[Logit Masking]] · [[Recitation]] · [[Error Trace Retention]] · [[Few-Shot Drift]]
- **Production discipline (Anthropic postmortem)** — [[Cache Invalidation Cascade]] · [[Config Type Safety]] · [[Context Assembly Pipeline]]; failure modes of the same surface Manus optimizes
- **Tool-use mechanisms** — [[Tool Search Tool]] · [[Programmatic Tool Calling]] · [[Tool Use Examples]] · [[Think Tool]] (reasoning scratchpad); [[Agent Interface Contracts]] and [[Progressive Disclosure]] govern tool authoring
- **Recursive composition (academic)** — [[Recursive Language Models]] · [[Context Decomposition vs Problem Decomposition]]
- **Tool-design framing** — [[ACI - Agent-Computer Interface]] (return-format precision + discoverability + input_examples); now sits alongside [[Agent Interface Contracts]] as the system-layer expression
- **Coding-agent ergonomics** — [[Agentic Coding Slash Commands]] · [[AI Tool Fluency]] · [[Context Anxiety]] (model behavior when context budget tightens)
- **Safety & isolation** — [[Agent Sandboxing]] · [[Permission Model]] · [[Permission Classifier]]; the runtime side of letting agents act
- **Evaluation** — [[LLM-as-Judge Evaluation]] · [[Pass^k Reliability Metric]] · [[User Simulator Evaluation]] · [[Trace-Based Evaluation]] · [[Agent Eval Pyramid]] · [[tau-bench]] · [[BFCL]] · [[ToolBench]] · [[Tool-Use Benchmarks - BFCL vs tau-bench vs ToolBench]] · [[SWE-bench]] · [[SWE-bench Verified]] · [[Eval Infrastructure Noise]] · [[Eval Awareness]] · [[Sandbagging]] · [[AI-Resistant Evaluation Design]] · [[AI Tool Fluency]]
- **Retrieval substrate** — [[BM25 and Hybrid Retrieval]] · [[Contextual Retrieval]] · [[Reranking]]; the retrieval half of context engineering
- **Protocol bet** — [[MCP]]
- **Operational decision tools** — [[Token Economics]] (4× / 15× + attention budget + KV-cache hit rate + smaller-model-in-scaffold) · [[LLM-as-Judge Evaluation]]
- **Context discipline** — [[Context Engineering]] · [[Just-in-Time Context Retrieval]] · [[Long-Horizon Context Management]] (4 techniques: compaction · notes · sub-agents · RLM-recursion)

## Running theses

- [[Workflows Beat Agents for Most Production]] — **position: defensive (with carve-outs); sharpened post-RLM to "agents work when substrate is workflow-shaped."** Workflows remain the production default; multi-agent wins narrowly on (parallelizable + context-overflow + high-value); coding is explicitly workflow-territory; infra-side objections are closing via [[Meta-Harness]]. [[Recursive Language Models]] is the strongest example of a constrained-substrate agent design — agent-shaped LM inside a workflow-shaped REPL scaffold.
- [[Static Action Spaces vs Dynamic Tool Discovery]] — **position: open.** Manus's [[Logit Masking]] approach vs Anthropic's [[Tool Search Tool]] approach are explicitly opposite. Anthropic's Nov-2025 release addresses Manus's stated objections via cache-safe deferral. Both designs are internally consistent; the likely 2027 architecture is a hybrid.

## Synthesis after 26 sources

Eight threads now structure the worldview:

1. **Cost is quadruply dimensional** — every additional token costs (a) dollars (4× / 15×), (b) attention budget (recall degradation + [[Context Anxiety]]), (c) prefill cost gated by KV-cache hit rate, and (d) smaller-model-in-scaffold opportunity cost. [[Token Economics]] frames all four.
2. **Context engineering is cross-vendor confirmed and now has a retrieval substrate.** Manus, Anthropic, and Zhang & Khattab converge on the same discipline; the Anthropic context-engineering essay names the retrieval primitives ([[BM25 and Hybrid Retrieval]], [[Contextual Retrieval]], [[Reranking]]) that sit underneath [[Just-in-Time Context Retrieval]].
3. **Tool use is a tier of distinct mechanisms.** Discovery ([[Tool Search Tool]]), execution ([[Programmatic Tool Calling]]), authoring ([[Tool Use Examples]], [[Agent Interface Contracts]], [[Progressive Disclosure]]), reasoning scratchpad ([[Think Tool]]). [[Recursive Language Models]] is a sibling primitive on the context-orchestration side.
4. **Sub-agents triply-justified, still narrow; RLM-recursion is the fourth context technique.** [[Long-Horizon Context Management]] has 4 distinct techniques (compaction / notes / sub-agents / RLM). See [[Context Decomposition vs Problem Decomposition]].
5. **The action-space fault line: static vs dynamic.** First load-bearing cross-vendor disagreement in the wiki. See [[Static Action Spaces vs Dynamic Tool Discovery]].
6. **A new architectural axis: context vs problem decomposition.** RLM names it; the rest of the wiki sits mostly on the problem side.
7. **Evaluation is now its own discipline, not a footnote.** [[Agent Eval Pyramid]] organizes the layers; [[Trace-Based Evaluation]] is the operational primitive; [[Eval Infrastructure Noise]], [[Eval Awareness]], and [[Sandbagging]] are the three confound classes that make naive benchmark numbers untrustworthy. [[AI-Resistant Evaluation Design]] generalizes the lesson back to human hiring.
8. **The harness has matured into a first-class artifact.** [[Harness Design Patterns]], [[Minimal Footprint Principle]], [[Harness Staleness]], [[Agent Sandboxing]], and [[Permission Model]]/[[Permission Classifier]] form a coherent runtime stack. Anthropic's postmortem ([[Cache Invalidation Cascade]], [[Config Type Safety]], [[Context Assembly Pipeline]]) reveals these as the layers that actually fail in production — vindicating Manus's KV-cache primacy from the opposite direction (failure-mode evidence vs design-principle evidence).

## Gaps to fill via next ingests

- **Counter-source for [[Workflows Beat Agents for Most Production]]** — Devin / Cognition writeup remains highest priority.
- **Second non-Anthropic vendor on KV-cache primacy** — Manus is one data point; need another (OpenAI / Google / DeepSeek production write-up).
- **Cross-provider KV-cache cost** — Sonnet 10× gap is anchored; analogues on GPT-5 / Gemini 3 / open-weights via vLLM are unknown.
- **Independent replication of [[Recursive Language Models]]** — OOLONG, BrowseComp-Plus outside Khattab's orbit.
- **DSPy as an ingest candidate** — Khattab orbit; problem-decomposition heavy framework.
- **A swarm / graph perspective** beyond Anthropic's binary+1.
- **Specific framework deep-dives** (LangGraph, OpenAI Agents SDK, Claude Agent SDK).
- **Hybrid action-space architecture** — does anyone publish a static-core + dynamic-tier design?
- **Non-Anthropic harness postmortems** — Anthropic's three-issue postmortem is rich; need an outside-Anthropic equivalent to test whether [[Cache Invalidation Cascade]] / [[Context Assembly Pipeline]] generalize.

## Closed gaps

- ~~Cross-vendor [[Meta-Harness]] analogues~~ — partially closed by Manus.
- ~~Need a non-Anthropic perspective at all~~ — closed by Manus 2025-07.
- ~~Need an academic perspective at all~~ — closed by Zhang & Khattab 2025-10.
- ~~Production reliability data~~ — partially closed: [[Eval Infrastructure Noise]], [[Eval Awareness]], [[Sandbagging]], and [[Agent Eval Pyramid]] now form a coherent eval-methodology stack.
- ~~Tool authoring as a distinct discipline~~ — closed by Writing Effective Tools + Agent Skills ingests; [[Agent Interface Contracts]] + [[Progressive Disclosure]] anchor it.

## Continual learning & online evaluation (2026-05-20)

A new cross-cutting layer from the autoresearch pass. The agent-facing pillars:
- **Online evaluation** — [[Online Evaluation]], [[LLM-as-Judge]], [[Implicit Feedback Signals]], [[A/B Testing for Agents]], [[Eval Validity]]; extends the existing eval stack ([[Agent Eval Pyramid]], [[Trace-Based Evaluation]], [[Eval Awareness]], [[tau-bench]]) from offline benchmarks to live signals.
- **Real-time learning** — [[Online Learning from Interaction]], [[Learning from Implicit Feedback]]; the durability spectrum from in-context to online RL.
- **Memory persistence** — [[Memory Stream]], [[Persona Vectors vs Memory Files]], [[Letta]]; extends [[Agent Memory Taxonomy]], [[Self-Editing Memory]], [[MemGPT]].
- **Architecture** — [[Model-Centric Architecture]], [[Code-to-the-Side vs Orchestration]]; the counter-pole to [[Agentic Harness]]/[[Meta-Harness]]. Umbrella: [[Research - Continually-Learning Model-Centric Systems]].

## Online evaluation in production (2026-05-23)

Autoresearch deepening the online-eval cluster with an external/industry lens. Synthesis: [[Research - Online Evaluation in Production]] (companion to [[Research - Online Evaluation]]).
- **Industry loop** — [[Continuous Evaluation]]: trace → sample → judge → threshold-alert over live traffic.
- **Judging mechanisms** — [[Online LLM-as-Judge]] (tiered: distilled at ~1/30 cost on 100% traffic + [[Agent-as-a-Judge]] step-level on anomalies).
- **Why online (empirical)** — [[Offline-Online Evaluation Gap]] (LiveCodeBench −20-30%, benchmark contamination); extends [[Eval Awareness]] / [[AI-Resistant Evaluation Design]] with the contamination/overfit failure mode.
- **Bottlenecks** — [[Online Evaluation Bottlenecks]]: judge cost/latency, A/B statistical power (10k+ trajectories/arm), multi-turn credit assignment, baseline drift, online reward-hacking.
- **Survey anchors** — Yehudai et al. (ACL 2025), Mohammadi et al. (KDD 2025), Guan et al. (multi-turn).

## OpenAI agent doctrine (2026-05-22)

[[2025 - OpenAI - A Practical Guide to Building Agents]] adds the **OpenAI-side canon** alongside Anthropic's. Direct comparison: [[OpenAI Practical Guide vs Anthropic Building Effective Agents]].
- **Orchestration patterns** — [[Manager Pattern]] (agents-as-tools; ≈ [[Orchestrator-Workers]]) vs [[Agent Handoffs]] (decentralized peer transfer; ≈ [[Routing]]); both are [[Multi-Agent Systems]] shapes. [[Agent Run Loop]] (`Runner.run()` until exit condition) is the single-agent core.
- **Tools** — [[Agent Tool Categories]]: Data / Action / Orchestration; standardized definitions, kin to [[ACI - Agent-Computer Interface]] / [[Agent Interface Contracts]].
- **Safety** — [[Agent Guardrails]] (relevance/safety/PII/moderation/tool-safeguards/rules/output-validation, optimistic tripwires) + [[Human-in-the-Loop Intervention]]; tool-safeguard risk ratings extend [[Permission Model]] / [[Minimal Footprint Principle]].
- **Entities** — [[OpenAI]], [[OpenAI Agents SDK]] (code-first vs declarative-graph frameworks).

## Software 3.0 & agentic engineering (2026-05-22)

Karpathy's [[2026-05-22 - Karpathy - Sequoia Ascent 2026]] supplies the era-level framing over the operational corpus:
- **[[Software 3.0]]** — programming LLMs in natural language; the successor to [[Software 2.0]] and the rhetorical frame above [[Model-Centric Architecture]]. Sometimes the app *disappears* into a direct model transformation.
- **[[Verifiability]]** — "automate what you can verify"; the engine behind the December-2025 coding-agent jump and the [[The Bitter Lesson]] / RL story. The founder wedge: valuable + verifiable + undertrained domains.
- **[[Jagged Intelligence]]** — capability ≈ verifiability × training attention × data × value; "ghosts, not animals"; the "are you on the model's rails?" test.
- **[[Vibe Coding]]** (raises the floor) vs **[[Agentic Engineering]]** (raises the ceiling) — the latter is the human discipline wrapping fallible agents; pairs with the eval/harness/permission stack above.
- **[[Agent-Native Infrastructure]]** — build for the human's agent: sensors + actuators, [[MCP]], CLIs, schemas, permissioning. Generalizes [[ACI - Agent-Computer Interface]] and [[Agent Interface Contracts]] to the whole product.

## Navigation

- [[brain/03_Resources/wiki/index]] — full page catalog (read this first)
- [[log]] — chronological event history
