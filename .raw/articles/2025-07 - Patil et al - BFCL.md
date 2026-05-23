---
source_url: https://proceedings.mlr.press/v267/patil25a.html
fetched: 2026-05-22
---

# The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models

**Authors:** Shishir G. Patil, Huanzhi Mao, Fanjia Yan, Charlie Cheng-Jie Ji, Vishnu Suresh, Ion Stoica, Joseph E. Gonzalez (UC Berkeley — Sky Computing Lab / Gorilla project).

**Venue:** ICML 2025 (Proceedings of the 42nd ICML, PMLR vol. 267, pp. 48371–48392), Jul 13–19 2025.

**Live leaderboard:** https://gorilla.cs.berkeley.edu/leaderboard.html
**Repo:** https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard

## Problem

Function calling (= tool use) is an LLM's ability to invoke external functions/APIs/user-defined tools. No standardized benchmark existed for evaluating it across the diversity of real-world scenarios. BFCL fills that gap and has become the de facto standard for evaluating function calls.

## Core evaluation method

**Abstract Syntax Tree (AST) evaluation** — parse the model's generated function call into an AST and structurally compare against ground truth (function name, required params, types, value constraints). Scales to thousands of functions, doesn't require execution, language-agnostic across Python/Java/JavaScript/REST.

Two evaluation modes:
- **AST** — structural match against expected call.
- **Executable** — actually run the call and check the returned output.

## Test categories

- **Simple** — one function, one call.
- **Multiple** — choose the right function from several candidates.
- **Parallel** — one prompt requires multiple simultaneous calls.
- **Parallel-multiple** — combination of the above.
- **Relevance / irrelevance detection** — should the model **abstain** when no provided function fits? Tests over-eager calling.
- **Multi-turn** (V3) — stateful sequential function calls with context retention across turns.
- **Agentic** (V4) — holistic agentic evaluation: web search integration, memory persistence, format sensitivity. Format-sensitivity cases only apply to prompt (non-FC) models.

Overall accuracy = unweighted average across subcategories. Models evaluated in both native function-calling (FC) and prompt-based modes.

## Version evolution

- **V1** — foundation; AST as the evaluation metric.
- **V2** — enterprise + OSS-contributed (user-contributed) functions; reduces data contamination / bias from synthetic functions.
- **V3** — multi-turn interactions; stateful, sequential calls.
- **V4** — holistic **agentic** evaluation (web search, memory, format sensitivity).

## Headline findings

SOTA LLMs excel at single-turn calls but **memory, dynamic decision-making, and long-horizon reasoning remain open challenges**. The agentic, multi-step, stateful settings expose the gap. Abstention (knowing when *not* to call a function) is a distinct, hard capability.
