---
type: meta
title: "Concepts Index"
updated: 2026-05-22
---

# Concepts

Ideas, patterns, frameworks. Domain-agnostic in form, domain-tagged in content. **97 concept pages** currently.

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

## Harness design

- [[Meta-Harness]] — Anthropic's Brain/Hands/Session hosting abstraction above harness implementations
- [[Agentic Harness]] — minimal scaffold wrapping an LLM (tools, loop, stop); SWE-bench simplicity finding, plus the catalog of production patterns and anti-patterns for long-running harnesses
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

- [[LLM-as-Judge]]
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

- [[brain/03_Resources/wiki/concepts/CLAUDE]] — auto-loaded config primitive for Claude Code sessions; the persistent-context lever
- [[Agentic Coding Slash Commands]] — `.claude/commands/` reusable prompt templates, version-controlled
- [[Config Type Safety]] — typed config schemas (Zod, Pydantic) at the agent boundary; eliminate a class of silent agent failures

## LLM post-training & fine-tuning

- [[LoRA]] — low-rank adaptation; matches FullFT when applied to all layers, at moderate batch sizes, within capacity. Rank-1 suffices for policy-gradient RL.
- [[On-Policy Distillation]] — student rollouts + teacher per-token reverse-KL; 9-30x cost reduction vs SFT/RL.
- [[Reasoning Distillation]] — SFT a small base on a big RL model's CoT traces (R1-Distill); distillation > small-model RL.
- [[Reverse KL Divergence]] — mode-seeking, "unhackable"; the supervision signal in on-policy distillation.
- [[Empirical Neural Tangent Kernel]] — explains why LoRA needs all layers (MLP gradients dominate the kernel).

## RL for reasoning (2026-05-31)

- [[DeepSeek-R1-Zero]] — reasoning incentivized by *pure RL* on a base model, no SFT; emergent self-reflection + the "aha moment"; AIME 15.6%→77.9%.
- [[RL with Verifiable Rewards]] — RLVR: RL whose reward is a cheap automatic verifier (rule/compiler/test), not a learned RM. The home page for the paradigm cited across [[GRPO]]/[[GEPA]]/[[Verifiability]].
- [[GRPO]] — group-relative advantage, no critic; the canonical RLVR optimizer (now sourced from R1, not just GEPA).

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

## Continual learning (2026-05-20)

- [[Online Learning from Interaction]] — the umbrella concept; learning from live interaction as a durability spectrum
- [[In-Context Learning]] — learning within the context window; the cheapest, most reversible end of the spectrum
- [[Test-Time Adaptation]] — updating at inference; test-time training as the surprising-effectiveness midpoint
- [[Implicit Feedback Signals]] — the observable signals (edits, retries, dwell) that feed online evaluation *and* serve as the reward stream for real-time learning
- [[Reward Modeling]] — converting human/behavioral preferences into a differentiable training signal (RLHF lineage)
- [[Online Evaluation]] — the conduit from live interaction to durable change
- [[LLM-as-Judge]] — model-scored evaluation; debiasing reaches >80% human agreement
- [[A/B Testing for Agents]] — the only causally trustworthy online verdict
- [[Eval Validity]] — every online signal is a proxy; the metric is the construct
- [[Persona Vectors]] — causal activation-space directions controlling agent persona (parametric pole)
- [[Activation Steering / Representation Engineering]] — reading/writing model behavior via activation-space directions
- [[Memory Stream]] — append-only experiential memory record (contextual pole)
- [[Persona Vectors vs Memory Files]] — the control-vs-inspectability split between the two persistence paths
- [[Model-Centric Architecture]] — model at the center, code to the side
- [[Code-to-the-Side vs Orchestration]] — which side-code is scaffolding (scaling absorbs) vs guarantees (persists)
- [[Software 2.0]] — Karpathy's "neural nets eat code" framing; the scaling argument for model-centrism
- [[The Bitter Lesson]] — Sutton's argument that general methods + compute beat hand-engineered knowledge

## OpenAI agent doctrine (2026-05-22)

- [[Agent Run Loop]] — the central while-loop ("run") that drives any agent until an exit condition
- [[Agent Tool Categories]] — Data / Action / Orchestration; the read-vs-write split that feeds tool safeguards
- [[Manager Pattern]] — central manager coordinates specialists as tools (≈ [[Orchestrator-Workers]])
- [[Agent Handoffs]] — decentralized one-way peer transfers (≈ [[Routing]])
- [[Agent Guardrails]] — layered defense typology + optimistic tripwire execution
- [[Human-in-the-Loop Intervention]] — failure-threshold and high-risk escalation to a human

## Software 3.0 era — agentic engineering (2026-05-22)

- [[Software 3.0]] — programming LLMs in natural language; the successor to [[Software 2.0]], the era-level frame over the agent corpus
- [[Verifiability]] — "automate what you can verify"; explains where AI moves fastest, and the valuable-verifiable-undertrained founder wedge
- [[Jagged Intelligence]] — capability ≈ verifiability × training attention × data × value; "ghosts, not animals"; "are you on the model's rails?"
- [[Vibe Coding]] — building by description; raises the floor
- [[Agentic Engineering]] — professional discipline over fallible agents; raises the ceiling; the orchestrator stance
- [[Agent-Native Infrastructure]] — build for the human's agent (sensors + actuators); generalizes [[ACI - Agent-Computer Interface]] to the whole product

## Prime Intellect self-improvement stack (2026-05-24)

- [[Reward Hacking]] — reframed as gradient-budget competition; "hacking is what happens when there's gradient budget left over and a side channel to absorb it"
- [[Self-Evolving Agent Environments]] — synthesizer↔solver loop auto-grows a difficulty-calibrated RL task corpus; structural defense against reward hacking
- [[Token-In Token-Out]] — byte-faithful inference for agentic RL; prefix continuity → ~3x less compute
- [[Autonomous Research Agents]] — agents doing ML research; search & recombine well, can't yet originate ideas (novelty gate)

## Agentic coding — monolithic loop (2026-05-24)

- [[Ralph Loop]] — Geoffrey Huntley's monolithic, single-process, one-task-per-loop coding agent; "everything is a ralph loop"; the anti-multi-agent pole; operationalizes [[Context Engineering]]

## Promotion policy

Create a concept page when:
- A pattern, framework, or named idea appears substantively in ≥1 source AND is reused or referenced elsewhere
- The concept needs a stable name for cross-references

Don't create concept pages for:
- One-off terminology in a single source (cite inline in the source page)
- Generic words ("data," "context" without modifier) — those need narrowing
