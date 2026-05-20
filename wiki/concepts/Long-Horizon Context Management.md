---
type: concept
title: Long-Horizon Context Management
created: 2026-05-04
updated: 2026-05-13
tags:
- ai-agents
- context
- long-horizon
- memory
status: developing
related: []
sources:
- "[[2025-09-29 - Anthropic - Effective context engineering for AI agents]]"
- "[[2025-10 - Zhang Khattab - Recursive Language Models]]"
- "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
- "[[2026-04-08 - Anthropic - Scaling Managed Agents]]"
- "[[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]]"
- "[[2025-10-01 - Anthropic - Harness Design Long Running Apps]]"
_legacy_source_count: 4
---

# Long-Horizon Context Management

## Summary

Per [[Effective context engineering for AI agents]] (Anthropic 2025-09): the discipline of keeping a long-running agent productive when its task spans many more tokens than fit in a single context window. Anthropic names **three techniques**, each addressing context-window limits differently. Choice depends on task shape.

## The three techniques

### 1. Compaction

**Summarize prior context, reinitialize the window.** When the agent's working context approaches saturation, compress older turns into a short summary and start fresh. Lightest form: **tool-result clearing** (drop verbose tool outputs once their information has been used) — a feature exposed in the Claude Developer Platform.

**Use when:** the task's working context is mostly transient (tool outputs, intermediate reasoning) and a summary preserves the necessary state.

### 2. Structured note-taking (agentic memory)

**Agent writes to an external memory file and re-reads on demand.** Concrete instances Anthropic cites:
- `NOTES.md` files
- Claude Code's todo list
- "Claude Plays Pokémon" memory file

The memory layer is *external* (filesystem, key-value store) — not in-context. The agent treats it like a developer treats a notebook: write down what matters, look it up later.

**Use when:** the task has structured state (open todos, tracked entities, decisions made) that needs to persist beyond any single context window.

### 3. Sub-agent architectures

**Decompose into specialized sub-agents that return distilled results.** Lead agent delegates a sub-task to a fresh agent with its own context window; sub-agent works, returns 1–2k tokens of distilled output; lead continues with the distillation, not the raw work.

This is the architectural family in [[Multi-Agent Systems]] — sub-agent decomposition is one of three justifications for going multi-agent.

**Use when:** the task is parallelizable AND each parallel branch would individually exceed a single context window. See [[Token Economics]] — this is the 15× cost zone.

### 4. Recursive context decomposition (per Zhang & Khattab 2025-10)

**Never load full context into any single LM call; let the LM decompose context via code at inference time.** [[2025-10 - Zhang Khattab - Recursive Language Models]] proposes [[Recursive Language Models]] (RLMs): the root LM only sees the query + an indication that context exists as a REPL variable. It writes Python to peek/grep/partition, and spawns **recursive sub-LM calls** over bounded slices.

This is structurally distinct from sub-agents (#3) in two ways:

1. **Decomposition axis** — sub-agents decompose the *problem* (lead agent picks meaningful sub-tasks); RLM decomposes the *context* (root LM picks meaningful sub-regions of input). See [[Context Decomposition vs Problem Decomposition]].
2. **Granularity** — sub-agents are spawned at strategic decomposition points by an explicit orchestrator; RLM sub-calls are spawned *ad-hoc as code-level function calls*, often dozens within a single root-LM trajectory.

**Use when:** the context is genuinely larger than any individual LM should attempt; the right decomposition strategy varies per input and isn't knowable upfront; cost predictability is less important than adaptive efficiency.

Empirical anchor: RLM(GPT-5-mini) > GPT-5 by **+34 pts (~114%↑)** on OOLONG 132k context at comparable cost. Maintains ~100% accuracy at 1000 documents on BrowseComp-Plus where all baselines degrade.

Limitations (from the source): no async / no prefix caching in reference impl; no upper bound on cost or runtime per call; published experiments use recursion depth=1 only.

## Choosing among the four

| Technique | Cost | Best for | Risk |
|---|---|---|---|
| Compaction | Low | Linear tasks with heavy tool output | Lossy summarization may drop critical state |
| Structured note-taking | Medium | Stateful tasks (todos, tracked decisions) | Agent forgets to write or re-read; memory drift |
| Sub-agent architectures | High (~15×) | Parallel + breadth-first work | Coordination overhead, error compounding |
| Recursive context decomposition (RLM) | Variable (depth-dependent) | Genuinely huge contexts; per-input strategy varies | No cost ceiling; latency unpredictable (blocking, no caching in ref impl) |

In practice, long-horizon agents combine these: notes for structured state, compaction for verbose intermediates, sub-agents for parallel branches, and increasingly — for genuinely-huge-context retrieval/aggregation tasks — RLM-style recursion. RLM and sub-agents are siblings, not substitutes: sub-agents are strategic problem-decomposition; RLM is ad-hoc context-decomposition. See [[Context Decomposition vs Problem Decomposition]].

## Manus's framing: file system as the ultimate context (per Manus 2025-07)

[[2025-07-18 - Manus - Context Engineering for AI Agents]] reframes the **file system itself as the unlimited externalized memory**, with two consequential rules that sharpen Anthropic's note-taking technique:

- **Treat the file system as primary context, not as a fallback.** Manus deliberately designs around files (read, write, edit, list) being the agent's structured external memory — not an afterthought when context overflows.
- **Compression must be restorable.** Drop a web page's content from context as long as the URL is preserved; drop a document's bytes as long as its path remains. Manus's rule: never irreversibly compress, because you cannot reliably predict which observation will become critical ten steps later.

This is a **harder rule** than Anthropic's compaction technique. Anthropic's compaction summarizes (lossy); Manus's compression keeps a pointer (lossless). The trade-off: pointer-preservation requires the original resource still to exist (URL still resolves, file still in sandbox), whereas summary survives even if the underlying source is gone.

Speculation worth noting: Manus muses that **file-based memory might unlock agentic State Space Models** — if SSMs offloaded long-range state to the file system instead of holding it in attention, their speed/efficiency advantage might compensate for their weaker long-range attention. No empirical follow-through as of 2025-07; an open thread for [[Augmented LLM]].

## The substrate underneath (per Anthropic 2026-04)

[[Scaling Managed Agents]] introduces [[Session as Event Log]] — an append-only event log living outside the context window — as the **durable foundation** all three techniques sit on. Compaction can be replayed from the log; structured notes can be derived from events; sub-agent orchestration uses the same event substrate for coordination.

Reframed:

- **Session log** = the system-managed truth (durable, complete)
- **Compaction / notes / sub-agents** = three views or distillations of the log surfaced to the brain

This split is consequential because it moves *durability* from the agent's responsibility to the runtime's responsibility. See [[Meta-Harness]].

## Harness as the runtime mechanism (per Anthropic 2026-05)

[[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]] grounds the three long-horizon techniques in concrete harness responsibilities:

- **Compaction** is owned by the context layer of the harness — not the model. The harness decides when and how to compact; the model should never be aware that compaction is happening (i.e., no silent truncation).
- **Structured note-taking** is enabled by the execution layer's sandbox and the context layer's JIT retrieval from the event log. The harness must ensure the model's writes actually land in durable storage.
- **Sub-agent architectures** are coordinated by the orchestration layer — a distinct layer above session management, responsible for provisioning, routing, and terminating sub-agent sessions.

Key harness constraint: **silent truncation** (dropping context without notifying the model or logging the event) is the most common production failure mode for long-horizon agents. The harness must always log truncation events and optionally surface them to the model as structured events.

## Connections

- Mother concept: [[Context Engineering]]
- Pairs with: [[Just-in-Time Context Retrieval]] (JIT keeps active window small; long-horizon mgmt preserves continuity across windows)
- Variant device: [[Recitation]] (file-system memory used for attention, not capacity)
- Substrate: [[Augmented LLM]] (memory leg) · [[Session as Event Log]] (durable foundation)
- Sub-agent technique: [[Multi-Agent Systems]]
- Recursive context-decomposition technique: [[Recursive Language Models]] (sibling to sub-agents; different decomposition axis — see [[Context Decomposition vs Problem Decomposition]])
- Runtime: [[Meta-Harness]] · [[Managed Agents]]
- Cost discipline: [[Token Economics]] · [[KV-Cache Discipline]] (compaction destroys cache — pay the cost knowingly)

## Open questions

- Compaction vs note-taking — at what task complexity does the LLM-driven summary diverge enough from explicit structured notes to matter?
- Auto-compaction policies — when should compaction trigger? Token-count threshold, semantic-coherence, or agent self-decision?
- Memory drift — do agents reliably re-read their own notes? Failure modes documented anywhere?

## Context Anxiety as a compaction trigger

[[2025-10-01 - Anthropic - Harness Design Long Running Apps]] documents a specific failure mode that compaction addresses: **[[Context Anxiety]]**. Claude Sonnet 4.5 would prematurely terminate tasks as its context window approached saturation. The harness-level fix was context resets (compaction-adjacent). This behavior was absent in Claude Opus 4.5 — the harness assumption went stale. This is the canonical example of [[Harness Staleness]].

Implication: compaction is not just a capacity technique — it can also be a behavioral intervention for models that exhibit context anxiety. As models improve, such interventions should be re-validated.

## Sources

- [[Effective context engineering for AI agents]] (Anthropic, 2025-09-29)
- [[2025-10-01 - Anthropic - Harness Design Long Running Apps]] (Anthropic, ~2025)
- [[Scaling Managed Agents]] (Anthropic, 2026-04-08)
- [[2025-07-18 - Manus - Context Engineering for AI Agents]] (Manus, 2025-07-18)
- [[2025-10 - Zhang Khattab - Recursive Language Models]] (Zhang & Khattab, 2025-10)
- [[2026-05-13 - Anthropic - Effective Harnesses for Long-Running Agents]] (Anthropic, 2026-05-13)
