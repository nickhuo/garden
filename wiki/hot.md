---
type: meta
title: "Hot Cache"
updated: 2026-05-23
---

# Recent Context

## Last Updated

2026-05-23 — autoresearch on **AI Product Citation — [[OpenEvidence]] & [[Harvey]]** (branch `research/ai-product-citation`, 13 new pages). Prompted by Nick's H60/Compass **citation ground** + Newsprout citation. Fills a clean gap — the wiki had retrieval + eval theory but no citation coverage. Core finding: **citation precision comes mostly from the curated corpus, not the model** — OpenEvidence cites a closed 300+ journal corpus (no open web), Harvey only vetted gov/LexisNexis sources via an agent-curated pipeline with an auto-reject gate on hallucinated citations. The canonical pipeline ([[Citation Verification Pipeline]]): curated corpus → hybrid retrieve → [[Reranking|rerank]] → **P-Cite** draft ([[Generation-Time vs Post-hoc Citation]]) → **NLI entailment** check ([[Citation Precision and Recall]], the ALCE metric) → [[2025-04-22 - CiteFix - Post-Processing Citation Correction|CiteFix]] correction → auto-reject → user-facing source link. Highest-leverage insight: **~80% of "unverifiable" facts are mis-citations, not hallucinations** — cheap to fix post-hoc (a smaller model + correction beats a bigger model alone). For Newsprout (open web), the curated-corpus lever is gone, so post-verification carries the weight. Umbrella: [[Attributed Text Generation]]. Synthesis: [[Research - AI Product Citation - Open Evidence and Harvey]].

2026-05-23 — autoresearch on **ZeroEntropy / zerank** was trimmed on review to keep only the [[2025-09-16 - Pipitone et al - zELO]] paper (zELO: Elo-from-pairwise-LLM-preferences reranker training — a strong commercialization angle). Cross-links to [[Reranking]].

2026-05-22 — ingested **OpenAI, A Practical Guide to Building Agents** ([[2025 - OpenAI - A Practical Guide to Building Agents]]). The OpenAI-side counterpart to Anthropic's [[2024-12-19 - Anthropic - Building Effective Agents]] — see the new comparison [[OpenAI Practical Guide vs Anthropic Building Effective Agents]]. Convergent advice under different vocabulary: "maximize a single agent first" ≈ Anthropic's "simplest thing that works." Two multi-agent patterns: **[[Manager Pattern]]** (agents-as-tools, central control — ≈ [[Orchestrator-Workers]]) vs **[[Agent Handoffs]]** (decentralized peer transfer — ≈ [[Routing]]). New: [[Agent Tool Categories]] (Data/Action/Orchestration), [[Agent Run Loop]] (`Runner.run()` until exit condition), [[Agent Guardrails]] (layered typology + optimistic tripwires), [[Human-in-the-Loop Intervention]] (failure-threshold + high-risk triggers). Entities: [[OpenAI]], [[OpenAI Agents SDK]] (code-first, anti-declarative-graph). Guardrail tool-safeguards risk ratings connect to [[Permission Model]].

2026-05-22 — ingested **Karpathy, Sequoia Ascent 2026** ([[2026-05-22 - Karpathy - Sequoia Ascent 2026]]). The era-level capstone over the agent corpus: [[Software 3.0]] (programming LLMs in natural language, above [[Software 2.0]]), [[Verifiability]] ("traditional software automates what you can specify; LLMs automate what you can verify" — the engine behind the Dec-2025 coding-agent jump and the [[The Bitter Lesson]]/RL story), [[Jagged Intelligence]] ("ghosts, not animals"; capability ≈ verifiability × training attention × data × value; "are you on the model's rails?"), [[Vibe Coding]] (raises the floor) vs [[Agentic Engineering]] (raises the ceiling), and [[Agent-Native Infrastructure]] (sensors/actuators — generalizes [[ACI - Agent-Computer Interface]]). Education thesis: "you can outsource your thinking, but you can't outsource your understanding" — the rationale for this very wiki.

2026-05-22 — ingested the **tool-use benchmark cluster**: [[BFCL]] ([[2025-07 - Patil et al - BFCL]]) + [[ToolBench]]/ToolLLM ([[2023-07-31 - Qin et al - ToolLLM]]), joining the existing [[tau-bench]]. New synthesis: [[Tool-Use Benchmarks - BFCL vs tau-bench vs ToolBench]] (first comparison page). The three measure orthogonal axes — **correctness at scale** (BFCL, AST), **reliability under interaction** (τ-bench, pass^k + deterministic DB reward), **generalization across 16k+ APIs** (ToolBench, LLM-judge ToolEval). Grading runs deterministic→LLM-judged; faithfulness trades against scale.

2026-05-20 — autoresearch on **continually-learning, model-centric AI systems**: 4 directions, 40 new pages, on branch `research/continual-learning-systems`. Umbrella: [[Research - Continually-Learning Model-Centric Systems]].

## Key Recent Facts

- **The thesis in one loop.** Real-time learning, persistent memory, model-centric architecture, and online evaluation are four faces of one system: interaction → **online eval** scores it → **real-time learning** turns the score into an update (durability spectrum) → **persistent memory/persona** stores it → the **model** (not orchestration code) acts on it, user keeps final control. See [[Research - Continually-Learning Model-Centric Systems]].
- **Real-time learning is a durability spectrum** ([[Online Learning from Interaction]]): in-context ([[In-Context Learning]]) → memory write-back ([[Self-Editing Memory]]) → test-time training ([[Test-Time Adaptation]]) → continual online RL. Cheapest/reversible → most durable/dangerous. Catastrophic forgetting is the central unsolved problem; memory is the main mitigation. [[Welcome to the Era of Experience]] (Silver & Sutton 2025) is the "why now": grounded environmental reward over human-prejudgment reward.
- **Persistence has two poles** ([[Persona Vectors vs Memory Files]]): **persona vectors** (parametric, causal activation-space directions, direct control over *who* the agent is, low inspectability — [[Persona Vectors]], [[Activation Steering / Representation Engineering]]) vs **memory files** (contextual, inspectable record of *what* it knows — [[Memory Stream]], [[Self-Editing Memory]], [[MemGPT]]/[[Letta]]). Complementary, not competing.
- **Model-centric vs harness/schema is a slider** ([[Model-Centric Architecture]]). Scaling favors the model long-run ([[The Bitter Lesson]], [[Software 2.0]]); ship-time reliability favors structure the model can't provide (Donut +22% workflow success, −85% invalid calls). The durable side-code is the guarantees layer (constraints, validation, permissioning) — [[Code-to-the-Side vs Orchestration]].
- **Online evaluation is the bridge** ([[Online Evaluation]]): implicit/explicit signal → [[LLM-as-Judge]] or [[Reward Modeling]] → update to retrieval/rubric/policy/persona. Spectrum from cheap-observational ([[Implicit Feedback Signals]]) to slow-causal ([[A/B Testing for Agents]]); rests on [[Eval Validity]]. A strong LLM judge matches human agreement (>80%) only after debiasing.
- **Connection to Nick's work is the organizing principle.** Online evaluation + schema/contract discipline is Nick's center of gravity (Compass dual-judge/RAGAS, Donut golden eval, Beckman two-axis judge). Real-time learning extends Sonic (capture) + Donut (flywheel); persona vectors extend Beckman's mastery overlay + (A,B,C) metacognition fit.

## Recent Changes (this session)

- Created: 40 pages — see [[Research - Continually-Learning Model-Centric Systems]] and the 4 pillar syntheses ([[Research - Real-Time Learning]], [[Research - Persistent Memory and Persona Vectors]], [[Research - Model-Centric Architecture]], [[Research - Online Evaluation]]).
- Updated: [[brain/03_Resources/wiki/index]], [[log]], [[overview]], [[AI-Agents]], [[LLM]], plus cross-links into existing memory/eval/harness pages.

## Active Threads

- **LLM domain just grew sharply** — persona vectors, representation engineering, ICL, test-time adaptation, reward modeling now populate it beyond the TML seed.
- **Thesis candidates** (promote with ≥2 sources): "the guarantees layer is what scaling does not absorb"; "online eval is the conduit that makes persistence safe."
- **Extension ideas from prior work**: Donut flywheel → multi-agent learning; Beckman coefficients → inspectable per-user persona vectors; Compass rubric → cross-agent scoring.
- **Open**: where to cut reversible (context/memory) vs permanent (weights) adaptation in production; detecting online reward-hacking.
