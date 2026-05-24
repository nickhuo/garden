---
type: concept
title: Recursive Language Models
created: 2026-05-10
updated: 2026-05-10
tags:
- ai-agents
- context
- long-context
- inference-strategy
- repl
status: developing
related: []
sources:
- "[[2025-10 - Zhang Khattab - Recursive Language Models]]"
- "[[2026-01-01 - Prime Intellect - Recursive Language Models]]"
aliases:
- RLM
- Recursive LM
- Recursive LMs
_legacy_source_count: 1
---

# Recursive Language Models

## Summary

Per [[2025-10 - Zhang Khattab - Recursive Language Models]] (Zhang & Khattab, MIT, Oct 2025): an inference strategy where a **root LM never sees the long context directly**. Context is stored as a Python REPL variable; the root LM interacts with it via code (peek, grep, partition, summarize) and can spawn **recursive LM sub-calls as ordinary function calls inside the REPL** to delegate semantic processing on bounded slices.

API surface is a drop-in replacement: `rlm.completion(messages)` swaps for `gpt5.completion(messages)`. Published experiments use recursion depth=1 only (root LM calls leaf LMs, no RLM-of-RLM); depth>1 is "an easy change" but not yet evaluated.

The architectural commitment is **[[Context Decomposition vs Problem Decomposition|context-centric decomposition]]**: the LM decides at inference time how to chunk and recurse over its own input, rather than the programmer decomposing the problem upfront.

## The mechanism

| Element | Role |
|---|---|
| **Root LM** (depth=0) | Receives only the query + a reference to a context variable; never sees the full context |
| **REPL environment** | Python notebook; context lives as a variable in memory |
| **Code blocks** | Root LM emits Python; REPL executes; truncated output returned to context |
| **Recursive sub-LM calls** | `RLM_M(q̂, Ĉ)` callable from inside code as if it were an ordinary function |
| **Termination** | Root LM emits `FINAL(answer)` or `FINAL_VAR(var_name)` to return a value built in the REPL |

The five emergent strategies the authors observed in RLM trajectories:

- **Peek** — grab the first ~2000 chars to understand structure
- **Grep** — regex/keyword filter to narrow the search space (cheaper than embedding retrieval)
- **Partition + Map** — chunk context, fire recursive sub-LM calls for semantic mapping, aggregate the distilled results
- **Summarize** — recursive sub-call to summarize a region for the root LM's decision-making
- **Long-input → long-output** — programmatic processing (e.g., processing a long `git diff` history to produce a final file state)

None of these are hard-coded; the model decides which to use based on the query and a peek at the context.

## Empirical anchors

| Benchmark | Setup | Result |
|---|---|---|
| OOLONG `trec_coarse` 132k | Semantic mapping over ~3000-6000 unlabeled rows; ~100 queries | RLM(GPT-5-mini) **+34 pts (~114%↑) vs GPT-5**, comparable cost |
| OOLONG `trec_coarse` 263k | Same, doubled context | RLM(GPT-5-mini) **+15 pts (~49%↑) vs GPT-5**, cheaper on average |
| OOLONG ablation | RLM(GPT-5) without recursive sub-calls (REPL only) | **-10 pts vs RLM with recursion** — recursion is load-bearing for semantic mapping |
| BrowseComp-Plus, 1000 docs | Multi-hop retrieval, 20 random queries | RLM(GPT-5) **holds ~100%** while GPT-5 (truncated / pre-query BM25) and ReAct+BM25 all degrade |
| Author claim | scaling to 10M+ tokens | "does not degrade in performance" — not independently verified |

Caveats: sample sizes are small (20 queries, ~100 queries); author flags as preliminary. The OOLONG delta is large enough to survive moderate sample noise; the BrowseComp-Plus result with only 20 queries is suggestive but not definitive.

## Why it works (author's framing)

> "long sequences are out of distribution for model training distributions due to lack of natural occurrence and higher entropy of long sequences. The goal of RLMs has been to propose a framework for issuing LM calls without ever needing to directly solve this problem."

RLM sidesteps the long-context-training-distribution problem by **never giving any single LM call a long context**. Sub-LM calls handle bounded slices; the root LM only sees query + small REPL outputs (peek results, grep matches, sub-call summaries). The cumulative work over the whole context is large, but each individual inference pass is in-distribution.

This is the cleanest mechanism the wiki has surfaced for **separating cognitive load from context scale**.

## Inference-time scaling axis

Author positions RLMs as a **third general-purpose inference-time scaling axis**, alongside:

1. **CoT-style reasoning** (Chain-of-Thought, o1, extended thinking) — scale by thinking longer
2. **ReAct-style agent scaffolds** — scale by tool use and observation
3. **Recursive Language Models** — scale by recursive context decomposition

The recursion-trajectory (how the root LM chooses to chunk and recurse) is "entirely learnable" and can be RL-trained. No model has been trained this way yet as of source date.

## Relationship to existing wiki concepts

- **[[Programmatic Tool Calling]]** — sister concept. Both use sandboxed REPL as the primitive. PTC orchestrates **tool calls** via code; RLM processes **context** via code (with sub-LM calls available). Same hardware, different object. PTC author Anthropic cites CodeAct; RLM author also cites CodeAct, explicitly distinguishing on the "context as object" framing. The two are composable in principle.
- **[[Just-in-Time Context Retrieval]]** — RLM is JIT taken to the extreme. Anthropic's JIT uses lightweight identifiers (file paths, URLs); RLM uses an in-memory REPL variable. Identical principle (don't pre-load), more aggressive implementation.
- **[[Long-Horizon Context Management]]** — RLM is a **fourth technique** alongside compaction / structured note-taking / sub-agents. Distinct from sub-agents because the recursion is *ad-hoc code-level*, not *strategic problem-level decomposition* (see [[Context Decomposition vs Problem Decomposition]]).
- **[[Multi-Agent Systems]]** — RLM's recursive sub-calls are *literally* multiple LM invocations coordinating, but the wiki's [[Multi-Agent Systems]] page is specifically about role-differentiated, coordinator+workers architectures (the Anthropic Research feature pattern). RLM is single-agent recursive composition — no role differentiation, no parallelism harness (yet), no orchestrator-worker structure.
- **[[Workflows Beat Agents for Most Production]]** — RLM is agent-shaped (root LM decides everything) but operates inside a tightly constrained substrate (REPL with bounded actions). Reads as: "agents work when you constrain the substrate to look like a workflow." Consistent with the thesis's existing defensive position, not a falsification.
- **[[Token Economics]]** — first empirical case in the wiki where a **smaller model in a recursive scaffold beats a larger model alone** at comparable or lower cost. Disturbs the "smarter model wins if you can afford it" intuition.

## Stated limitations

- No async / no prefix caching in reference implementation; queries can take minutes
- No upper-bound guarantees on total API cost or runtime per call
- Recursion depth=1 only in published experiments
- "Plenty of low-hanging fruit" for systems-side optimization

## Prior art (per the post)

| System | What it does | How RLM differs |
|---|---|---|
| **CodeAct** | Code as the action space for agents | Cited as inspiration. RLM treats context as the object of investigation, not just code-execution as an affordance. |
| **MemGPT** | Model decides what to bring in/out of context | Defers to model, but builds toward a single context the LM eventually calls. RLM never builds toward a single huge context. |
| **MemWalker** | Tree-structured summarization | Imposes structure; RLM defers structure entirely to the LM. |
| **LADDER** | Problem-level decomposition | Doesn't scale to huge contexts; RLM is context-level. |
| **ROMA** | Recursive agent decomposing problems and running sub-agents | Closest analog. RLM decomposes context, not problems. |
| **THREAD / TRM / Recursive LLM Prompts / RSA** | Various "recursive" framings (output spawning, latent iteration, prompt-as-state, response aggregation) | All distinct from RLM's context-as-REPL-variable framing. |

## Connections

- Author + advisor: Alex L. Zhang (MIT EECS PhD), Omar Khattab (ColBERT, DSPy; advisor) — both deferred as entities per ≥2 substantive mentions rule
- Master framing: [[Context Decomposition vs Problem Decomposition]]
- Sister primitive: [[Programmatic Tool Calling]] (same REPL substrate, different object)
- Extreme instance of: [[Just-in-Time Context Retrieval]]
- Fourth technique in: [[Long-Horizon Context Management]]
- Adjacent (clarifying note): [[Multi-Agent Systems]]
- Theoretical scaling axis sibling: CoT reasoning (no wiki page yet; defer), ReAct (mentioned in [[Autonomous Agents]])
- New empirical anchor for: [[Token Economics]]

## Open questions

- **Independent replication.** All numbers come from the source paper. Two small benchmarks, one preliminary slice. When does someone outside Khattab's orbit replicate?
- **Cost guarantees.** Author flags absence of cost/runtime upper bounds as a limitation. Production deployment needs primitives that don't exist yet.
- **Recursion depth > 1.** "Easy change" per the author, but unevaluated. Coordination failures at depth=N?
- **RL-trained recursion.** Author hints at this. No published trained model yet.
- **Non-extractive tasks.** OOLONG and BrowseComp-Plus are retrieval/aggregation-flavored. How does RLM perform on long-form generation, multi-turn dialogue with long history, or large-codebase editing?
- **Failure modes.** Author doesn't publish where RLM loses. Probable failure shape: tasks where the REPL itself adds noise without recovering value.
- **Composability with [[Tool Search Tool]] and [[Logit Masking]].** All three respond to context-scale at different layers (context-processing / tool-defs / action-selection). Are they composable, or does one dominate?
- **Long-tail effect on model training.** If RLMs become the default inference pattern, what changes about training distribution? Smaller bounded-context examples would dominate; long-context training data becomes less necessary.

## Second source: Prime Intellect implementation (2026-01)

[[2026-01-01 - Prime Intellect - Recursive Language Models]] is an independent **engineering implementation and endorsement** that calls RLMs "the simplest, most flexible method for context folding" and frames them as the long-context paradigm of 2026. It agrees with Zhang & Khattab on the core mechanism and adds concrete design choices:

- **Tools restricted to sub-LLMs only** — the root model never calls tools directly, keeping its context lean.
- **`llm_batch`** for parallel sub-LLM calls (parallel map over chunks).
- **Dict-based answers** (`{"content", "ready"}`) enabling iterative refinement vs a one-shot `FINAL()`.
- Fresh eval slate (DeepDive, math-python, Oolong ~1.5M chars, verbatim-copy): RLM wins on long-context and verbatim, *underperforms* on math-python — decomposition doesn't help every domain without training.

It is part of [[Prime Intellect]]'s self-improvement stack (RLM is also one of the solver backends in [[Self-Evolving Agent Environments|general-agent]]). Both sources flag that the real unlock is **RL-trained recursion** — still unpublished as of their dates. This is the first **independent corroboration outside Khattab's orbit** the wiki flagged as an open question.

## Sources

- [[2025-10 - Zhang Khattab - Recursive Language Models]] (Zhang & Khattab, 2025-10)
- [[2026-01-01 - Prime Intellect - Recursive Language Models]] (Prime Intellect, 2026-01)
