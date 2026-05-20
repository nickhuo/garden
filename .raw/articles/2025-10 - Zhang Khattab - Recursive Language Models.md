# Recursive Language Models

**Source:** https://alexzhang13.github.io/blog/2025/rlm/
**Authors:** Alex L. Zhang (MIT EECS PhD, OASYS Lab) & Omar Khattab (advisor)
**Date:** October 2025 (per citation block); arxiv companion 2512.24601v1
**Citation (blog):** Zhang, Alex and Khattab, Omar. "Recursive Language Models." October 2025.
**Code:** https://github.com/alexzhang13/rlm · minimal: https://github.com/alexzhang13/rlm-minimal
**Funding ack:** Laude Institute. Thanks to MIT OASYS labmates + MIT DSG group (Tim Kraska et al.).

---

## tl;dr

Recursive Language Models (RLMs): an inference strategy where a "root LM" never sees long context directly — instead, the context is stored as a variable in a Python REPL environment, and the root LM interacts with it programmatically (peek, grep, partition, summarize) AND can spawn **recursive LM sub-calls** as code-level function calls to delegate semantic processing on sub-regions.

API is a drop-in replacement: `rlm.completion(messages)` instead of `gpt5.completion(messages)`. Recursive depth=1 in the published experiments (root LM calls leaf LMs, no RLM-of-RLM).

## Core thesis claims

1. **Context-centric decomposition, not problem-centric.** Prior agent frameworks (ROMA, CodeAct, MemGPT, MemWalker, LADDER) decompose the *problem*. RLMs decompose the *context*. The model decides at inference time how to chunk and recurse over its own input.
2. **No model call should ever require handling a huge context.** The root LM only sees the query plus an indication that a (large) context exists. Sub-LM calls handle bounded slices. Long-context performance becomes an *architectural composition* property, not a single-model capability.
3. **General-purpose inference-time scaling axis.** RLMs sit alongside CoT-style reasoning and ReAct-style agent scaffolds as a third axis. The control flow (how to interact with and recurse over context) is "entirely learnable" and "can be RL-ified".

## Empirical results (preliminary, single author + advisor)

**OOLONG benchmark (`trec_coarse` split, ~100 queries):**
- 132k tokens: RLM(GPT-5-mini) outperforms GPT-5 by **+34 points (~114%↑, more than double correct answers)** at roughly the same per-query API cost.
- 263k tokens: RLM(GPT-5-mini) still beats GPT-5 by **+15 points (~49%↑)** and is cheaper on average.
- Ablation: removing recursion (REPL-only, no sub-LM calls) drops RLM performance ~10% — recursion is load-bearing for semantic-mapping queries.
- ReAct + GPT-5 + BM25 baseline performs poorly here — retrieval doesn't fit the task.

**BrowseComp-Plus (20 random queries, document-corpus retrieval):**
- RLM(GPT-5) holds perfect performance up to **1000 documents** in context.
- GPT-5, GPT-5 (truncated), GPT-5 + Pre-query BM25, ReAct + GPT-5 + BM25 all degrade as docs scale.
- Claims RLM "does not degrade in performance when given 10M+ tokens at inference time."

## Mechanism (the REPL environment)

- Context loaded as a Python variable; root LM gets only the query and a reference to the variable's existence.
- Root LM outputs code blocks; REPL executes them; truncated output returned to root LM context.
- Recursive sub-calls: `RLM_M(q̂, Ĉ)` spawns an isolated sub-instance with new query and context slice.
- Termination: root LM emits `FINAL(answer)` or `FINAL_VAR(var_name)` to return a value built up in the REPL.

## Emergent strategies (described from RLM trajectories)

- **Peeking** — grab first 2000 chars to understand structure
- **Grepping** — regex/keyword filtering to narrow search space (cheaper than embedding retrieval)
- **Partition + Map** — chunk context, fire recursive sub-LM calls for semantic mapping, aggregate
- **Summarization** — recursive sub-call to summarize a region for the root LM
- **Long-input → long-output** — programmatic processing (e.g., diff-tracking on LoCoDiff benchmark)

## Stated limitations

- No async / no prefix caching in the reference implementation; queries can take minutes
- No strong guarantees on total API cost or runtime per call
- Recursion depth=1 only in published experiments
- "Low-hanging fruit" for systems-side optimization

## Positioning vs prior work

- **CodeAct** — RLMs cited as inspiration but argue for a fundamentally different view: code execution is in service of *understanding context*, not orchestrating tool calls.
- **MemGPT / MemWalker / LADDER** — defer context-management decisions to the model (MemGPT) or impose tree/problem structure (MemWalker / LADDER). RLMs defer entirely without imposing structure.
- **ROMA** — closest analog: a recursive agent that decomposes problems. RLMs decompose context, not problems.
- **THREAD / TRM / Recursive LLM Prompts / RSA** — all use "recursion" in different senses; RLMs are distinct from each.

## Author's framing (verbatim where load-bearing)

> "Agents are designed based on human / expert intuition on how to break down a problem to be digestible for an LM. RLMs are designed based on the principle that fundamentally, LMs should decide how to break down a problem to be digestible for an LM."

> "no single language model call should require handling a huge context"

> "RLMs improve as LMs improve. … If tomorrow, the best frontier LM can reasonably handle 10M tokens of context, then an RLM can reasonably handle 100M tokens of context (maybe at half the cost too)."

## Acknowledgements + provenance

MIT OASYS Lab. Khattab advisor — known for ColBERT (IR) and DSPy (LM programming framework). Anonymous OOLONG benchmark authors provided dataset on request. Funded partly by Laude Institute.

## Notes for the wiki

- First academic-source ingest (prior 5 were Anthropic engineering + Manus product blog)
- First Khattab-orbit source — likely shifts DSPy onto the radar as a future ingest candidate
- Empirical results are early/preliminary; small sample sizes (20 queries on BrowseComp-Plus, ~100 on OOLONG slice)
- Direct sister/competitor to [[Programmatic Tool Calling]] — same primitive (sandboxed REPL), different object (context vs tools)
- Maps cleanly onto Manus's "file system as context" with REPL substituted for filesystem
