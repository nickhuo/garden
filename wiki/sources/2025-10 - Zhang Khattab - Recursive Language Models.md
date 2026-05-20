---
type: source
title: Recursive Language Models
created: 2026-05-10
updated: 2026-05-10
tags:
- ai-agents
- context
- long-context
- inference-strategy
- academic
status: mature
related: []
sources:
  - "[[.raw/articles/2025-10 - Zhang Khattab - Recursive Language Models.md]]"
- '[[03_Resources/.raw/articles/2025-10 - Zhang Khattab - Recursive Language Models.md]]'
source_type: blog
author: Alex L. Zhang & Omar Khattab (MIT OASYS Lab)
date_published: 2026-05-10
url: https://alexzhang13.github.io/blog/2025/rlm/
confidence: medium
key_claims: []
---

# Recursive Language Models

## Summary

First academic source in the wiki. Alex Zhang (MIT EECS PhD) and Omar Khattab (advisor; ColBERT, DSPy) propose **Recursive Language Models (RLMs)**: an inference strategy where a "root LM" never sees long context directly. The context is stored as a Python REPL variable; the root LM interacts via code (peek, grep, partition, summarize) and can spawn **recursive LM sub-calls as ordinary function calls** inside the REPL.

API surface is identical to a base model call (`rlm.completion(messages)` swaps for `gpt5.completion(messages)`). Recursive depth=1 in the published experiments — root LM calls leaf LMs, no RLM-of-RLM. Arxiv companion paper at 2512.24601v1.

The architectural commitment is the headline: **decompose the context, not the problem.** This is the cleanest articulation of an axis the wiki has touched implicitly across multiple sources but never named — see new concept page [[Context Decomposition vs Problem Decomposition]].

## Key points (Nick's words)

- **RLM is a thin scaffold, not a model.** Root LM gets only the query + an indication that the (large) context exists as a REPL variable. It writes code to interact. Sub-LM calls handle bounded slices and return distilled results.
- **No model call should ever require handling a huge context.** Long-context capability becomes an *architectural composition* property, not a single-model capability. This is the strongest structural claim in the post.
- **"Context rot" is sidestepped, not solved.** Author's framing: the problem is that long sequences are out-of-distribution for model training; RLMs avoid the problem rather than fix it.
- **Empirical surprise: smaller models in an RLM beat larger models alone.** RLM(GPT-5-mini) > GPT-5 by **+34 points (~114%↑)** on OOLONG `trec_coarse` 132k context, at roughly equivalent per-query cost.
- **Scales to 10M+ tokens without performance degradation** per the author. Independent verification not yet available.
- **Recursion is load-bearing.** Ablation: removing recursion (REPL-only, no sub-LM calls) drops RLM performance ~10% on OOLONG. The recursive sub-calls aren't decorative.
- **Five emergent strategies observed** in RLM trajectories: peeking, grepping, partition+map, summarization, long-input→long-output (programmatic processing like diff tracking).
- **General-purpose inference-time scaling axis.** Author positions RLM alongside CoT-style reasoning and ReAct-style agent scaffolds as a third axis — and notes the recursion-trajectory is "entirely learnable" / RL-trainable.

## Evidence

- **OOLONG `trec_coarse` 132k context (~100 queries):** RLM(GPT-5-mini) +34 pts (~114%↑) vs GPT-5; comparable per-query cost. RLM(GPT-5) without recursion drops ~10pts.
- **OOLONG `trec_coarse` 263k context:** RLM(GPT-5-mini) +15 pts (~49%↑) vs GPT-5; cheaper on average.
- **BrowseComp-Plus (20 random queries, doc-corpus retrieval):** RLM(GPT-5) holds ~100% at 10 / 50 / 100 / 1000 documents in context. GPT-5 (full / truncated / pre-query BM25) and ReAct+BM25 all degrade as docs scale.
- **Author claim:** RLM "does not degrade in performance when given 10M+ tokens at inference time."
- **Ablation:** REPL alone (no recursive sub-calls) underperforms RLM-with-recursion by ~10pts on semantic-mapping queries.

Sample sizes are small (20 queries on BrowseComp-Plus, ~100 on OOLONG slice). Author flags this as preliminary.

## Connections

- New concepts: [[Recursive Language Models]] · [[Context Decomposition vs Problem Decomposition]]
- Sister concept (same REPL primitive, different object): [[Programmatic Tool Calling]]
- Extreme instance of: [[Just-in-Time Context Retrieval]]
- Fourth technique alongside compaction/notes/sub-agents: [[Long-Horizon Context Management]]
- Adjacent but distinct from: [[Multi-Agent Systems]] (recursive composition ≠ multi-agent)
- New data point for: [[Token Economics]] (smaller-model RLM beats larger model alone)
- Pressure on (but doesn't falsify): [[Workflows Beat Agents for Most Production]]
- Prior art cited: CodeAct (inspiration; explicitly distinguished), MemGPT, MemWalker, LADDER, ROMA, THREAD, TRM, Recursive LLM Prompts, RSA
- Author orbit: Omar Khattab → DSPy, ColBERT (future ingest candidates). MIT DSG group (Tim Kraska). Funded partly by Laude Institute.

## Open questions

- **Sample size.** OOLONG slice (~100 queries) and BrowseComp-Plus subset (20 queries) are small. Replication across model families and benchmarks needed before treating the +114% number as robust.
- **The author's claim of "no degradation at 10M+ tokens" is the load-bearing one.** It's unverified by independent benchmarks as of source date. Watch for replication or contradiction.
- **Cost guarantees.** RLM has no upper-bound on total API cost or runtime per call; the model decides depth-of-recursion + chunk-size. Production deployments need cost ceiling primitives that don't exist yet.
- **Async / prefix-caching.** Reference impl is blocking and doesn't use caching. Systems-side optimization headroom is large; what's the cost story after optimization?
- **RL-ifying the recursion trajectory.** Author hints that the decomposition strategy can be RL-trained. No model exists yet that's been trained this way.
- **Recursion depth.** Experiments use depth=1. Does depth=N introduce coordination failure modes that depth=1 doesn't?
- **How well does it work on non-extractive long-context tasks?** OOLONG and BrowseComp-Plus are both retrieval / aggregation flavored. What about long-form generation, multi-turn dialogue with long histories, or code-editing over large repos?
- **Where does RLM lose?** Author doesn't publish failure modes. The ablation shows recursion is load-bearing for semantic mapping; what about tasks where the REPL itself adds noise?
- **Interaction with [[Tool Search Tool]] and [[Logit Masking]].** All three are different responses to context-scale. RLM defers context-processing to code; Tool Search defers tool defs; Logit Masking constrains action space. Do they compose, conflict, or one-dominate?

## Sources

- self (this source page)
