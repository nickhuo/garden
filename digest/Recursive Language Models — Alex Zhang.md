---
type: digest
title: Recursive Language Models (RLM)
author: Alex L. Zhang
co_author: Omar Khattab (advisor)
affiliation: MIT OASYS / DSG
source: https://alexzhang13.github.io/blog/2025/rlm/
paper: https://arxiv.org/abs/2512.24601v1
code: https://github.com/alexzhang13/rlm
minimal: https://github.com/alexzhang13/rlm-minimal
tweet: https://x.com/a1zhang/status/1978469116542337259
date_digested: 2026-05-08
relevance_score: 10
scoring_basis: interest_graph.md
layers_hit:
  - L1-LLM-Agents
  - L1-System-Design
  - L2-RAG
  - L2-Context-Engineering
modifiers:
  - +benchmark-data
  - +career-leverage
  - +indie-repo
tags:
  - digest
  - rlm
  - agents
  - long-context
  - context-rot
  - inference-scaling
  - repl
  - omar-khattab
  - mit
related_topics:
  - "[[self-improving-agent]]"
  - "[[evaluation]]"
status: idea
---

# Recursive Language Models — Alex Zhang

## TL;DR

Alex Zhang and Omar Khattab propose **Recursive Language Models (RLMs)**: an inference-time scaffold where the root LM never sees the full context — instead, it gets a query plus a Python REPL whose memory holds the context as a variable, and it can spawn recursive LM sub-calls (`depth=1` in this paper) to peek, grep, partition, and map over chunks. On OOLONG `trec_coarse` at 132k tokens, **RLM(GPT-5-mini) beats GPT-5 by ~114%** at comparable cost; on BrowseComp-Plus with **1,000 documents (~10M+ tokens)**, RLM(GPT-5) is the only method that holds near-perfect recall. The bet: future inference-time scaling will be recursion over context, not bigger context windows.

## The Core Idea

A standard LM call is `M(q, C) → str`. An RLM call is `RLM_M(q, C) → str` with the same input/output type — drop-in replacement for `gpt5.completion(...)`. Inside, the root LM sees only `q` and is told the context lives in a REPL variable. It writes Python, reads cell output, and can fire `RLM_M(q̂, Ĉ)` recursively. It terminates with `FINAL(answer)` or `FINAL_VAR(varname)`.

Two non-obvious design choices carry the paper:

1. **Context-as-variable, not context-as-prompt.** The LM treats the haystack as data to be programmatically inspected, not as text to be read.
2. **REPL can call back into LMs.** This is what separates RLM from CodeAct — sub-queries are first-class citizens.

The recursive depth in all experiments is 1. Multi-level recursion is left as future work but is "a relatively easy change."

## Empirical Claims (and what they really show)

| Benchmark | Setup | Headline number |
|---|---|---|
| **OOLONG** `trec_coarse` @ 132k | RLM(GPT-5-mini) vs GPT-5 | **+34 pts (~114% relative)**, slightly cheaper median query |
| **OOLONG** `trec_coarse` @ 263k | RLM(GPT-5-mini) vs GPT-5 | **+15 pts (~49% relative)**, cheaper per query |
| **BrowseComp-Plus** @ 1k docs | RLM(GPT-5) vs everything | Only method at perfect score; non-recursive REPL ablation hits 90% |

Caveats Zhang acknowledges:
- BrowseComp-Plus results are over **20 random queries**, not the full benchmark. He flags this explicitly.
- Counting subtasks in OOLONG degrade as context grows (RLM included).
- ReAct + BM25 baseline indexes per query, which is *more* favorable than indexing the full corpus.
- No prefix caching, no async — each RLM call is blocking and slow (seconds to minutes).

## Why This Matters (Beyond the Numbers)

The conceptual move is the part to internalize. Frame:

- **Agents** decompose by *task* (human-coded scaffolds: ReAct, ROMA, Cursor's context-pruning).
- **RLMs** decompose by *context* (the LM picks the partition strategy at test time).

This collapses two genres of hack we already do — context summarization (Cursor, Claude Code) and tool-augmented retrieval (BM25 + ReAct loops) — into a single API surface that looks like `chat.completion`. If it generalizes, agent frameworks shrink from "orchestrator + memory + tools" to "RLM call + environment definition."

The other underrated claim: **RLMs improve as base LMs improve, multiplicatively**. If a frontier LM handles 10M tokens natively, an RLM over that LM handles ~100M. This is the same compounding argument that made CoT and ReAct durable.

## Critical Take

**Where it's strong:**
- The framing is genuinely new. "Context-centric vs problem-centric decomposition" is the right vocabulary and previously fuzzy.
- The OOLONG result is the kind of thing that makes inference-time scaling believers turn it into a research agenda. GPT-5-mini beating GPT-5 by 2x is a real signal, not a Goodhart artifact — OOLONG's distributional queries are exactly what context rot kills.
- BrowseComp-Plus at 10M+ tokens without retrieval indexing is the load-bearing systems claim.

**Where to be skeptical:**
- **n=20 on BrowseComp-Plus is a screenshot, not a benchmark.** The 100% line at 1k docs is suggestive, not conclusive. Until the full sweep lands, treat the 10M-token claim as a working hypothesis.
- **Cost scaling is hand-waved.** "Scales reasonably" — fine, but the median-vs-mean cost gap they admit ("outlier expensive queries") matters at production scale. No P99 latency or cost reported.
- **Depth=1 is doing a lot of quiet work.** Most failure modes of recursive systems show up at depth ≥2 (loops, cost blowup, mode collapse on summaries). The paper admits this is unexplored.
- **The REPL is the real tool.** Stripping recursion (REPL ablation) only loses ~10%. That suggests the headline win is "let the LM grep over context" plus "smaller LM" — the recursion is icing, not foundation. Worth probing.
- **No comparison to long-context-trained frontier models** (Gemini 1.5 Pro / 2.5 at 1M+, Claude Sonnet at 200k with sliding context). They tested against GPT-5 only. The comparison Nick should care about is RLM vs Gemini-native-long-context on the same OOLONG split.

## Connections to Nick's Interest Graph

| Layer hit | Why it scores |
|---|---|
| **L1 LLM Agents 架构层** (+5) | Direct competitor to ReAct/MCP-style agent scaffolds; new orchestration primitive |
| **L1 System Design 现代化** (+5) | REPL-as-environment + recursive LM calls is a fresh inference-engine design problem |
| **L2 RAG / Hybrid retrieval** (+3) | Explicitly positioned against BM25 + ReAct on multi-hop retrieval |
| **L2 Context Engineering** (+3) | Context rot is the named adversary; this is engineering, not vibes |
| **+benchmark-data** (+2) | OOLONG, BrowseComp-Plus with concrete numbers |
| **+career-leverage** (+3) | Khattab is ColBERT author, MIT DSG; RLM will be in AIE interview small-talk by Q3 2026 |

**Composite: 10/10 (capped). This is a Linear-Issue-mandatory item per `interest_graph.md` §7.**

## Action Triggers (5 channels)

### 🐦 Twitter Thread (high priority — strike while novel)
**Hook draft:**
> The next inference-time scaling axis isn't longer context. It's recursive context.
>
> Alex Zhang's RLM gives a small LM a Python REPL holding the haystack as a variable, lets it spawn sub-LM calls, and beats GPT-5 by 2x on OOLONG. CoT → ReAct → RLM is the trajectory.
>
> Three reasons this is more than a clever scaffold: [thread]

Pin to original tweet (https://x.com/a1zhang/status/1978469116542337259) for engagement carry. Adversarial angle to consider: the depth=1 ablation showing recursion only buys 10% — argue the real innovation is "context-as-variable," not recursion itself.

### ✍️ Blog (nickhuo.com) — Tiered Writing
**Working title:** "Context Rot Is a Type System Problem, Not a Memory Problem"

**Outline:**
- Section 1 — Why "longer context window" stopped solving long-context. (set up the failure mode with OOLONG-style example)
- Section 2 — The two decomposition philosophies: task-centric (ReAct, agents) vs context-centric (RLM). Why the field defaulted to the wrong one.
- Section 3 — RLM mechanism walkthrough with the GPT-5-mini vs GPT-5 result.
- Section 4 — Honest skepticism: n=20 caveats, depth=1 limit, missing Gemini comparison.
- Section 5 — What to build on top: depth ≥2, async REPL, RL on the trajectory.
- Section 6 — The compounding bet: RLMs over frontier LMs scale multiplicatively.

Status: `idea` → promote to `outline` after benchmarking the depth-1 ablation claim independently.

### 🔧 GitHub
- **Primary target:** `alexzhang13/rlm-minimal` — likely <1k stars, intentionally minimal. Good first contributions: async REPL execution, prefix caching for repeated sub-queries, hooking up Anthropic / Gemini backends (paper only tests OpenAI). Both are listed limitations in the post.
- **Secondary:** Run their OOLONG split with Claude Sonnet and Gemini 2.5 as the root LM. Publish the comparison. This is a high-leverage solo PR — fills the gap the authors admit.
- Verify star count and open-issue surface before committing — the repo URLs are claims from the post, not verified by me.

### 💼 Career / Interview
**Resume / talking points:**
- Add RLM to "AI Eng watchlist" — appropriate for any company that's hit context-window pain (Cursor, Cognition, Codeium, Replit, Anthropic context-engineering team, Modal).
- **Interview frame:** if asked about long-context, do *not* default to "use Gemini 1M" or "RAG." The sophisticated answer in mid-2026 is: "Context rot makes raw window size insufficient. RLM-style recursive scaffolds let smaller models beat larger ones — the trade is latency for accuracy. I'd benchmark both on the actual workload." This positions Nick as up-to-date with the inference-scaling research frontier.
- **Target companies that will care:** Anthropic (context engineering team explicitly cited in the post), Cursor, Cognition (Devin's long-horizon failure mode is exactly this), Modal (will care about the systems opportunity Zhang flags for "GPU MODE community").

### 📊 Investment
Weak signal. No direct trade. Indirect: if RLM-style inference compute becomes default, **per-query token consumption goes up 2–5x** (root + sub-call traffic). Marginally bullish for inference infra (Coreweave, AVGO) and bearish for "context window race" as a moat. Not actionable today.

## Open Questions Worth Tracking

1. **Depth ≥2 behavior.** Does recursion compose without loops, or do you need explicit depth/cost budgets? This is where most clever-scaffold papers die.
2. **RL'd RLM trajectory.** Zhang gestures at "the trajectory is learnable, can be RL'd." First lab to actually do this (DeepMind? OpenAI?) gets the next reasoning-models-shaped capability jump.
3. **Comparison vs native long-context frontier models.** OOLONG result is GPT-5-only. The honest test is RLM(GPT-5-mini) vs Gemini 2.5 Pro at native 1M, on the same split.
4. **Generalization of the "context-as-variable" intuition** beyond text. The paper claims it works for any modality loadable into memory. Multimodal RLM is a paper waiting to be written.
5. **Cost variance.** Median-vs-mean gap is real. Nobody runs production on a system whose P99 cost is a black box.

## Linear Issue (proposed)

**Title:** Investigate RLM scaffold — depth-1 ablation, Anthropic/Gemini backend port, blog post draft
**Priority:** P1
**Labels:** `agent-research`, `blog-pipeline`, `oss-contribution`
**Description:**
- [ ] Read full arxiv (2512.24601v1) when accessible; verify n, methodology
- [ ] Clone `rlm-minimal`, run their OOLONG sample locally
- [ ] Port to Anthropic Claude API (or Gemini); rerun on a 5-query OOLONG sample
- [ ] Write blog draft "Context Rot Is a Type System Problem"
- [ ] Open PR to `rlm-minimal` for whichever gap (async / Anthropic backend / prefix cache) lands first
- [ ] Post X thread when blog publishes

## Citation

```bibtex
@article{zhang2025rlm,
  title   = "Recursive Language Models",
  author  = "Zhang, Alex and Khattab, Omar",
  year    = "2025",
  month   = "October",
  url     = "https://alexzhang13.github.io/blog/2025/rlm/"
}
```

## Cross-References

- [[self-improving-agent]] — RLM is a candidate primitive for self-improving systems: the trajectory of recursive calls is RL-able as a scalar reward.
- [[evaluation]] — OOLONG and BrowseComp-Plus are the testbeds. Nick's eval thesis directly applies; RLM moves the goalpost from "model passes long-context eval" to "system passes."
- [[Paradigm Thesis Notes]] — context-as-variable is a reliability layer: bounded per-call context = bounded per-call failure modes. Worth tying into Paradigm Fellowship application as supporting evidence for the "reliability layer for agent systems" thesis.
